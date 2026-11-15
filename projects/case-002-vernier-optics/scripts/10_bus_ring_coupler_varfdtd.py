"""Run local 2.5D electromagnetic bus-to-ring coupling in native MODE projects."""
from __future__ import annotations

import json
import argparse
import logging
import math
import shutil
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
CONFIG = CASE / "config" / "13_bus_ring_coupler_varfdtd.json"
API = Path(r"D:\Program Files\Lumerical\v242\api\python")


def props(session, values):
    for name, value in values.items():
        session.set(name, value)


def build(mode, cfg, geo, radius, include_ring=True):
    width = float(geo["waveguide_width_m"])
    height = float(geo["waveguide_height_m"])
    gap = float(geo["bus_ring_gap_m"])
    center_y = radius + width + gap
    px = float(cfg["ring_x_m"])
    ring_y = center_y - math.sqrt(radius * radius - px * px)
    # Ring and bus must be separated at both output monitor planes.
    if ring_y - cfg["monitor_y_span_m"] / 2 <= width / 2:
        raise ValueError("Ring output monitor overlaps bus")
    mode.addrect()
    props(mode, {"name": "BOX", "material": geo["materials"]["oxide"],
                 "x": 0, "x span": cfg["x_span_m"] + 1e-6,
                 "y": (cfg["y_min_m"] + cfg["y_max_m"]) / 2,
                 "y span": cfg["y_max_m"] - cfg["y_min_m"] + 1e-6,
                 "z": -float(geo["box_thickness_m"]) / 2,
                 "z span": geo["box_thickness_m"]})
    mode.addrect()
    props(mode, {"name": "straight_bus", "material": geo["materials"]["silicon"],
                 "x": 0, "x span": cfg["x_span_m"] + 1e-6,
                 "y": 0, "y span": width, "z": height / 2, "z span": height})
    if include_ring:
        mode.addring()
        props(mode, {"name": "curved_ring_coupler", "material": geo["materials"]["silicon"],
                     "x": 0, "y": center_y, "z": height / 2, "z span": height,
                     "inner radius": radius - width / 2,
                     "outer radius": radius + width / 2,
                     "theta start": cfg["arc_theta_start_deg"],
                     "theta stop": cfg["arc_theta_stop_deg"]})
    mode.addvarfdtd()
    props(mode, {"x": 0, "x span": cfg["x_span_m"],
                 "y": (cfg["y_min_m"] + cfg["y_max_m"]) / 2,
                 "y span": cfg["y_max_m"] - cfg["y_min_m"],
                 "z": (cfg["z_min_m"] + cfg["z_max_m"]) / 2,
                 "z span": cfg["z_max_m"] - cfg["z_min_m"],
                 "simulation time": cfg["simulation_time_s"],
                 "x0": 0, "y0": -(cfg["y_min_m"] + cfg["y_max_m"]) / 2,
                 "bandwidth": cfg["effective_index_bandwidth"],
                 "polarization": "E mode (TE)"})
    mode.setglobalsource("wavelength start", cfg["wavelength_start_m"])
    mode.setglobalsource("wavelength stop", cfg["wavelength_stop_m"])
    mode.setglobalmonitor("frequency points", int(cfg["wavelength_points"]))
    mode.addmesh()
    props(mode, {"name": "coupler_mesh", "x": 0,
                 "x span": cfg["mesh_x_span_m"],
                 "y": (cfg["mesh_y_min_m"] + cfg["mesh_y_max_m"]) / 2,
                 "y span": cfg["mesh_y_max_m"] - cfg["mesh_y_min_m"],
                 "z": height / 2, "z span": height + 0.2e-6,
                 "dx": cfg["mesh_dx_m"], "dy": cfg["mesh_dy_m"]})
    mode.addmodesource()
    props(mode, {"name": "bus_input_TE", "injection axis": "x",
                 "direction": "Forward", "x": cfg["source_x_m"],
                 "y": 0, "y span": cfg["monitor_y_span_m"],
                 "mode selection": "fundamental mode"})
    for name, x, y in (("bus_reference", cfg["reference_x_m"], 0),
                       ("bus_through", cfg["through_x_m"], 0),
                       ("ring_left", -cfg["ring_x_m"], ring_y),
                       ("ring_output", cfg["ring_x_m"], ring_y)):
        mode.addpower()
        props(mode, {"name": name, "monitor type": "Linear Y",
                     "x": x, "y": y, "y span": cfg["monitor_y_span_m"]})
    mode.addpower()
    props(mode, {"name": "coupler_field", "monitor type": "2D Z-normal",
                 "x": 0, "x span": cfg["mesh_x_span_m"],
                 "y": (cfg["mesh_y_min_m"] + cfg["mesh_y_max_m"]) / 2,
                 "y span": cfg["mesh_y_max_m"] - cfg["mesh_y_min_m"]})
    mode.addeffectiveindex()
    props(mode, {"name": "effective_index_map", "x": 0,
                 "x span": cfg["x_span_m"],
                 "y": (cfg["y_min_m"] + cfg["y_max_m"]) / 2,
                 "y span": cfg["y_max_m"] - cfg["y_min_m"]})
    for expansion_name, monitor_name, monitor_y in (
        ("bus_guided", "bus_through", 0),
        ("ring_guided", "ring_output", ring_y),
    ):
        mode.addmodeexpansion()
        props(mode, {"name": expansion_name,
                     "monitor type": "Linear Y",
                     "x": cfg["through_x_m"], "y": monitor_y,
                     "y span": cfg["monitor_y_span_m"],
                     "mode selection": "fundamental mode"})
        mode.select(expansion_name)
        mode.setexpansion("field", monitor_name)
    logging.info("Radius=%g gap=%g ring_output_y=%g", radius, gap, ring_y)


def check(mode):
    for name in ("bus_reference", "bus_through", "ring_left", "ring_output"):
        data = mode.getresult(name, "T")
        if not isinstance(data, dict) or "T" not in data:
            raise RuntimeError(f"Missing native transmission dataset: {name}")
        transmission = np.asarray(data["T"]).squeeze()
        if transmission.size < 3 or not np.isfinite(transmission).all():
            raise RuntimeError(f"Invalid transmission dataset: {name}")
        logging.info("%s: %d samples; minimum=%g maximum=%g", name,
                     transmission.size, np.min(transmission), np.max(transmission))
    data = mode.getresult("coupler_field", "E")
    if not isinstance(data, dict) or "E" not in data:
        raise RuntimeError("Missing native electric-field dataset")
    logging.info("Source effective index: %s", mode.getresult("bus_input_TE", "neff")["neff"])
    logging.info("Effective-index monitor result names: %s", mode.getresult("effective_index_map"))
    for name in ("bus_guided", "ring_guided"):
        result = mode.getresult(name, "expansion for field")
        guided = np.asarray(result["T_forward"]).squeeze()
        if guided.size < 3 or not np.isfinite(guided).all():
            raise RuntimeError(f"Invalid guided-mode power result: {name}")
        logging.info("%s guided-mode samples=%d; minimum=%g maximum=%g",
                     name, guided.size, np.min(guided), np.max(guided))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=CONFIG.name)
    args = parser.parse_args()
    selected = CASE / "config" / args.config
    cfg = json.loads(selected.read_text(encoding="utf-8-sig"))
    if "base_config" in cfg:
        base = json.loads((CASE / "config" / cfg["base_config"]).read_text(encoding="utf-8-sig"))
        base.update(cfg)
        cfg = base
    geo = json.loads((CASE / "config" / cfg["source_geometry_config"]).read_text(encoding="utf-8-sig"))
    if list(map(float, cfg["ring_radii_m"])) != list(map(float, geo["ring_radii_m"])):
        raise ValueError("Coupler and layout ring radii differ")
    run_id = f"{cfg['run_prefix']}_{datetime.now():%Y%m%d_%H%M%S}"
    run_dir = CASE / "results" / "runs" / run_id
    log_dir = CASE / "results" / "logs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    logging.info("Configuration: %s", selected)
    if not API.is_dir():
        raise FileNotFoundError(API)
    sys.path.insert(0, str(API))
    import lumapi
    print(f"RUN_DIRECTORY={run_dir}", flush=True)
    cases = [("bus_only_reference", cfg["ring_radii_m"][0], False)]
    cases += [(f"ring{number}_bus_coupler", radius, True)
              for number, radius in enumerate(cfg["ring_radii_m"], 1)]
    for label, radius, include_ring in cases:
        project = run_dir / f"{label}_varfdtd.lms"
        session = None
        try:
            session = lumapi.MODE(hide=True)
            build(session, cfg, geo, float(radius), include_ring)
            logging.info("Saving initial MODE project %s", project)
            session.save(str(project))
            logging.info("Initial MODE project saved")
            print(f"RUNNING_VARFDTD={project}", flush=True)
            session.run()
            check(session)
            session.save(str(project))
            print(f"COMPLETED_VARFDTD={project}", flush=True)
        finally:
            if session is not None:
                session.close()
    for solver_log in run_dir.glob("*.log"):
        shutil.move(str(solver_log), str(log_dir / solver_log.name))
    print(f"LOG_DIRECTORY={log_dir}", flush=True)


if __name__ == "__main__":
    try:
        main()
        status = 0
    except BaseException as exc:
        logging.exception("varFDTD coupling simulation failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
