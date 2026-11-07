"""由用户检查后手动运行：只调整自动细化上限，重试一档 CHARGE 网格。"""

from __future__ import annotations

import json
import logging
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


CASE = Path(__file__).resolve().parents[1]
CONFIG = CASE / "config/03_charge_refine_cap_retry.json"
RUNS = CASE / "results/runs"
LOGS = CASE / "results/logs"
FIGURES = CASE / "results/figures"
LUMERICAL_API = Path(r"D:\Program Files\Lumerical\v242\api\python")
CHARGE = "::model::CHARGE"
TEMPERATURE = CHARGE + "::temperature_monitor"
REQUIRED_RESULTS = {"anode", "cathode", "electrostatics", "bandstructure", "integrated"}


def read_config() -> tuple[Path, str, int]:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    source = (CASE / str(data["source_project"])).resolve()
    if not source.is_relative_to(CASE.resolve()) or not source.is_file():
        raise FileNotFoundError("Source project is missing or outside the case directory")
    name = str(data["level_name"])
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name):
        raise ValueError("Level name must be an ASCII identifier")
    value = data["max_refine_steps"]
    steps = int(value)
    if isinstance(value, bool) or steps < 1 or float(value) != steps:
        raise ValueError("max_refine_steps must be a positive integer")
    return source, name, steps


def solver_message(log_file: Path) -> tuple[bool, str]:
    if not log_file.is_file():
        return False, "Solver log was not created"
    lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in lines:
        if "Solver terminated" in line or "Convergence Failure" in line:
            return False, line.strip()
    if any("Simulation completed successfully" in line for line in lines):
        return True, "Solver reported successful completion"
    return False, "Solver log has no successful completion marker"


def main() -> int:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    run_dir = RUNS / run_id
    log_dir = LOGS / run_id
    figure_dir = FIGURES / run_id
    for directory in (run_dir, log_dir, figure_dir):
        directory.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=str(log_dir / "driver.log"), filemode="w",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    device = None
    try:
        if not CONFIG.is_file() or not LUMERICAL_API.is_dir():
            raise FileNotFoundError("Configuration or Lumerical Python API is missing")
        source, name, steps = read_config()
        project = run_dir / f"charge_mesh_{name}.ldev"
        solver_log = run_dir / f"charge_mesh_{name}_p0.log"
        shutil.copy2(source, project)
        sys.path.insert(0, str(LUMERICAL_API))
        import lumapi

        logging.info("Source=%s; config=%s; project=%s", source, CONFIG, project)
        print(f"Run ID: {run_id}; native project: {project}", flush=True)
        device = lumapi.DEVICE(str(project), hide=True)
        device.switchtolayout()
        if device.getnamed(CHARGE, "temperature dependence") != "coupled":
            raise RuntimeError("Source CHARGE solver is not coupled to heat")
        if "T" not in str(device.getnamed(CHARGE, "spatial results")).split(":"):
            raise RuntimeError("Source CHARGE solver does not save T")

        old_steps = int(device.getnamed(CHARGE, "max refine steps"))
        mesh_edges = device.getnamed(CHARGE, ["min edge length", "max edge length"])
        left_edge = device.getnamed(CHARGE + "::mesh left", "max edge length")
        right_edge = device.getnamed(CHARGE + "::mesh right", "max edge length")
        logging.info("Inherited mesh edges=%s; left=%s; right=%s; refine steps=%s -> %s",
                     mesh_edges, left_edge, right_edge, old_steps, steps)
        device.setnamed(CHARGE, "max refine steps", steps)
        device.save(str(project))

        print(f"Running CHARGE level {name}; inspect solver log if it fails", flush=True)
        device.run("CHARGE")
        completed, message = solver_message(solver_log)
        logging.info("Solver status for %s: %s", name, message)
        if not completed:
            raise RuntimeError(message)

        charge_results = set(str(device.getresult(CHARGE)).splitlines())
        temperature_results = set(str(device.getresult(TEMPERATURE)).splitlines())
        if not REQUIRED_RESULTS.issubset(charge_results) or "temperature" not in temperature_results:
            missing = sorted(REQUIRED_RESULTS - charge_results)
            raise RuntimeError(f"Solver completed but native results are missing: {missing}; "
                               f"temperature present={'temperature' in temperature_results}")
        device.save(str(project))
        logging.info("Required native datasets are present")
        print(f"Completed; open {project} in Lumerical", flush=True)
        print(f"Solver logs: {log_dir}", flush=True)
        print(f"Place screenshots in: {figure_dir}", flush=True)
        return 0
    except Exception as exc:
        logging.exception("Single-level mesh retry failed")
        print(f"Simulation failed: {exc}", file=sys.stderr, flush=True)
        print(f"Inspect logs in: {log_dir}", file=sys.stderr, flush=True)
        return 1
    finally:
        if device is not None:
            try:
                device.close()
            except Exception:
                logging.exception("Could not close Lumerical session")
        for log_file in run_dir.glob("*.log"):
            try:
                shutil.move(str(log_file), str(log_dir / log_file.name))
            except Exception:
                logging.exception("Could not move solver log: %s", log_file)


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        logging.exception("Unhandled driver error")
        print(f"Simulation failed: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
