"""Build a physical two-ring MODE layout and solve isolated bent-waveguide FDE modes.

The layout makes dimensions and optical port routing inspectable. The FDE projects
solve a local ring cross section at the two radii; they do not solve the couplers.
"""
from __future__ import annotations

import json
import logging
import math
import shutil
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
CONFIG = CASE / "config" / "11_ring_physical.json"
RUNS = CASE / "results" / "runs"
LOGS = CASE / "results" / "logs"
API = Path(r"D:\Program Files\Lumerical\v242\api\python")


def load_config() -> dict:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    positive = ("wavelength_m", "waveguide_width_m", "waveguide_height_m",
                "slab_thickness_m", "box_thickness_m", "bus_ring_gap_m")
    for key in positive:
        if float(cfg[key]) <= 0:
            raise ValueError(f"{key} must be positive")
    radii = [float(x) for x in cfg["ring_radii_m"]]
    if len(radii) != 2 or not 0 < radii[0] < radii[1]:
        raise ValueError("ring_radii_m must contain two increasing radii")
    if not 0 < cfg["slab_thickness_m"] < cfg["waveguide_height_m"]:
        raise ValueError("slab thickness must be below waveguide height")
    if cfg["bus_ring_gap_m"] >= radii[0]:
        raise ValueError("gap is not compatible with the ring radii")
    return cfg


def add_rect(mode, name, material, x, xspan, y, yspan, z, zspan):
    mode.addrect()
    for key, value in {"name": name, "material": material, "x": x,
                       "x span": xspan, "y": y, "y span": yspan,
                       "z": z, "z span": zspan}.items():
        mode.set(key, value)


def add_ring(mode, name, material, x, y, inner, outer, z, zspan,
             theta_start=None, theta_stop=None):
    mode.addring()
    properties = {"name": name, "material": material, "x": x,
                       "y": y, "inner radius": inner, "outer radius": outer,
                       "z": z, "z span": zspan}
    if theta_start is not None:
        properties["theta start"] = theta_start
        properties["theta stop"] = theta_stop
    for key, value in properties.items():
        mode.set(key, value)


def build_layout(mode, cfg):
    r1, r2 = map(float, cfg["ring_radii_m"])
    w = float(cfg["waveguide_width_m"])
    h = float(cfg["waveguide_height_m"])
    slab = float(cfg["slab_thickness_m"])
    gap = float(cfg["bus_ring_gap_m"])
    extension = float(cfg["layout_assumptions"]["bus_extension_each_side_m"])
    slab_span = float(cfg["layout_assumptions"]["slab_radial_span_m"])
    x1, x2 = map(float, cfg["layout_assumptions"]["ring_center_x_positions_m"])
    trim = float(cfg["layout_assumptions"]["slab_coupler_clearance_deg"])
    if not 25 <= trim < 90:
        raise ValueError("slab coupler clearance must be in [25, 90) degrees")
    if math.hypot(x2-x1, (r1+w+gap)+(r2+w+gap)) <= r1+r2+slab_span:
        raise ValueError("Ring slab annuli overlap; increase horizontal offset")
    y1 = r1 + w + gap
    y2 = -(r2 + w + gap)
    top_bus = y1 + r1 + w + gap
    bottom_bus = y2 - r2 - w - gap
    xmin = min(x1-r1, x2-r2)-extension
    xmax = max(x1+r1, x2+r2)+extension
    xmid = (xmin+xmax)/2
    xspan = xmax-xmin
    yspan = top_bus - bottom_bus + 2 * extension
    silicon = cfg["materials"]["silicon"]
    oxide = cfg["materials"]["oxide"]
    add_rect(mode, "BOX_2um", oxide, xmid, xspan + 2*extension,
             (top_bus + bottom_bus)/2, yspan, -cfg["box_thickness_m"]/2,
             cfg["box_thickness_m"])
    for i, (radius, center_x, center_y) in enumerate(((r1, x1, y1),
                                                       (r2, x2, y2)), start=1):
        for arc, start, stop in (("A", 0, 90-trim),
                                 ("B", 90+trim, 270-trim),
                                 ("C", 270+trim, 360)):
            add_ring(mode, f"ring{i}_slab_{arc}", silicon, center_x, center_y,
                     radius-slab_span/2, radius+slab_span/2, slab/2, slab,
                     start, stop)
        add_ring(mode, f"ring{i}_ridge", silicon, center_x, center_y,
                 radius-w/2, radius+w/2, h/2, h)
    for name, y in (("through_bus", top_bus), ("inter_ring_bus", 0.0),
                    ("drop2_bus", bottom_bus)):
        add_rect(mode, name, silicon, xmid, xspan, y, w, h/2, h)
    return {"ring1_x": x1, "ring2_x": x2,
            "ring1_y": y1, "ring2_y": y2,
            "through_bus_y": top_bus, "inter_ring_bus_y": 0.0,
            "drop2_bus_y": bottom_bus}


def build_bend_cross_section(mode, cfg, radius):
    w = float(cfg["waveguide_width_m"])
    h = float(cfg["waveguide_height_m"])
    slab = float(cfg["slab_thickness_m"])
    fde = cfg["bend_fde"]
    silicon = cfg["materials"]["silicon"]
    oxide = cfg["materials"]["oxide"]
    xspan = float(fde["x_span_m"])
    add_rect(mode, "BOX", oxide, 0, xspan+1e-6, 0, 0.5e-6,
             -cfg["box_thickness_m"]/2, cfg["box_thickness_m"])
    add_rect(mode, "ring_slab", silicon, 0,
             cfg["layout_assumptions"]["slab_radial_span_m"], 0, 0.5e-6,
             slab/2, slab)
    add_rect(mode, "ring_ridge", silicon, 0, w, 0, 0.5e-6,
             (h+slab)/2, h-slab)
    mode.addfde()
    for key, value in {"solver type": "2D Y normal", "wavelength": cfg["wavelength_m"],
                       "number of trial modes": int(fde["trial_modes"]),
                       "x": 0.0, "x span": xspan,
                       "z": (fde["z_min_m"]+fde["z_max_m"])/2,
                       "z span": fde["z_max_m"]-fde["z_min_m"],
                       "x min bc": "PML", "x max bc": "PML",
                       "z min bc": "PML", "z max bc": "PML"}.items():
        mode.set(key, value)
    mode.addmesh()
    for key, value in {"name": "core_mesh", "dx": fde["mesh_dx_m"],
                       "dy": 0.05e-6, "dz": fde["mesh_dz_m"],
                       "x": 0.0, "x span": fde["mesh_x_span_m"],
                       "y": 0.0, "y span": 0.5e-6,
                       "z": (fde["mesh_z_min_m"]+fde["mesh_z_max_m"])/2,
                       "z span": fde["mesh_z_max_m"]-fde["mesh_z_min_m"]}.items():
        mode.set(key, value)
    if radius is not None:
        mode.setanalysis("bent waveguide", True)
        mode.setanalysis("bend radius", radius)
        mode.setanalysis("bend orientation", float(fde["bend_orientation_deg"]))


def validate_mode(mode, cfg, radius):
    candidates = []
    for idx in range(1, int(cfg["bend_fde"]["trial_modes"])+1):
        for path in (f"FDE::data::mode{idx}", f"FDE::mode{idx}"):
            try:
                neff = complex(np.asarray(mode.getdata(path, "neff")).squeeze().item())
                if math.isfinite(neff.real) and neff.real > 1.0:
                    candidates.append((idx, neff))
                break
            except Exception:
                continue
    if not candidates:
        raise RuntimeError(f"No usable mode at radius {radius} m")
    selected = max(candidates, key=lambda item: item[1].real)
    logging.info("bend radius=%s m; selected mode=%d; neff=%s",
                 radius, selected[0], selected[1])


def main() -> int:
    cfg = load_config()
    run_id = f"s10_ring_physical_{datetime.now():%Y%m%d_%H%M%S}"
    run_dir = RUNS / run_id
    log_dir = LOGS / run_id
    run_dir.mkdir(parents=True)
    log_dir.mkdir(parents=True)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    if not API.is_dir():
        raise FileNotFoundError(API)
    sys.path.insert(0, str(API))
    import lumapi
    print(f"CONFIG={CONFIG}", flush=True)
    print(f"RUN_DIRECTORY={run_dir}", flush=True)
    print("RUNNING=physical layout, straight control, and two bent FDE modes", flush=True)
    files = []
    mode = None
    try:
        mode = lumapi.MODE(hide=True)
        positions = build_layout(mode, cfg)
        layout_file = run_dir / "dual_ring_physical_layout.lms"
        mode.save(str(layout_file))
        files.append(layout_file)
        logging.info("Layout positions=%s", positions)
    finally:
        if mode is not None:
            mode.close()
    for label, radius in (("straight", None),
                          ("ring1", cfg["ring_radii_m"][0]),
                          ("ring2", cfg["ring_radii_m"][1])):
        mode = None
        try:
            mode = lumapi.MODE(hide=True)
            build_bend_cross_section(mode, cfg,
                                     None if radius is None else float(radius))
            mode.findmodes()
            validate_mode(mode, cfg,
                          None if radius is None else float(radius))
            project = run_dir / ("straight_control_mode.lms" if radius is None
                                 else f"{label}_bent_mode.lms")
            mode.save(str(project))
            files.append(project)
        finally:
            if mode is not None:
                mode.close()
    for file in files:
        if not file.is_file() or file.stat().st_size < 1000:
            raise RuntimeError(f"Native project missing or empty: {file}")
    for logfile in run_dir.glob("*.log"):
        shutil.move(str(logfile), str(log_dir / logfile.name))
    print(f"OPEN_LAYOUT={files[0]}", flush=True)
    print(f"OPEN_STRAIGHT_MODE={files[1]}", flush=True)
    print(f"OPEN_RING1_MODE={files[2]}", flush=True)
    print(f"OPEN_RING2_MODE={files[3]}", flush=True)
    print(f"LOG_DIRECTORY={log_dir}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        logging.exception("Physical ring simulation failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
