"""按配置在独立副本中运行 p-i-p CHARGE，并将原生结果保存在 .ldev。"""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
RUNS = CASE / "results" / "runs"
LOGS = CASE / "results" / "logs"
FIGURES = CASE / "results" / "figures"
API = Path(r"D:\Program Files\Lumerical\v242\api\python")
CHARGE = "::model::CHARGE"
ANODE = CHARGE + "::boundary conditions::anode"


def load_plan(name: str) -> dict:
    if not re.fullmatch(r"fig2_0to1|fig23_0to20|fig23_cont", name):
        raise ValueError("Unknown plan")
    path = CASE / "config" / (name + ".json")
    plan = json.loads(path.read_text(encoding="utf-8-sig"))
    source = (CASE / plan["source_project"]).resolve()
    if not source.is_relative_to(CASE.resolve()) or not source.is_file():
        raise FileNotFoundError("Source project is unavailable or outside the case")
    plan["_source"] = source
    plan["_config"] = path
    if plan.get("continuation_from"):
        cont = (CASE / plan["continuation_from"]).resolve()
        if not cont.is_relative_to(CASE.resolve()) or not cont.is_file():
            raise FileNotFoundError("Continuation project is unavailable or outside the case")
        plan["_continuation"] = cont
    bias = plan["bias"]
    if not (0 <= bias["start_V"] < bias["stop_V"] <= 20):
        raise ValueError("Invalid voltage range")
    if not (0 < bias["interval_V"] <= bias["stop_V"] - bias["start_V"]):
        raise ValueError("Invalid voltage interval")
    if not (0 < bias["min_interval_V"] <= bias["interval_V"]):
        raise ValueError("Invalid minimum interval")
    solver = plan["solver"]
    if solver.get("solver_type") not in (None, "newton", "gummel"):
        raise ValueError("Invalid solver type")
    line = plan["line"]
    if not (line["x_min_m"] < line["x_max_m"] and
            line["x_min_m"] < 0 < line["x_max_m"]):
        raise ValueError("Line must cross the waveguide")
    roi = plan["field_roi"]
    if roi["x_span_m"] <= 0 or roi["z_span_m"] <= 0:
        raise ValueError("Invalid field monitor extent")
    plan.setdefault("keep_partial", False)
    return plan


def set_line_monitor(device, kind: str, name: str, line: dict) -> None:
    device.select(CHARGE)
    if kind == "band":
        device.addbandstructuremonitor()
    else:
        device.addchargemonitor()
    device.set("name", name)
    device.set("monitor type", "linear x")
    device.set("x", (line["x_min_m"] + line["x_max_m"]) / 2)
    device.set("x span", line["x_max_m"] - line["x_min_m"])
    device.set("y", line["y_m"])
    device.set("z", line["z_m"])


def configure(device, plan: dict) -> None:
    device.switchtolayout()
    if device.getnamed(CHARGE, "temperature dependence") != "coupled":
        raise RuntimeError("CHARGE is not in coupled electrothermal mode")
    if bool(device.getnamed(CHARGE, "enable continuation")):
        raise RuntimeError("Source depends on a continuation file")
    spatial = str(device.getnamed(CHARGE, "spatial results")).split(":")
    for field in ("Ec", "Efn", "Efp", "Ev", "E", "n", "p", "T", "Q"):
        if field not in spatial:
            spatial.append(field)
    device.setnamed(CHARGE, "spatial results", ":".join(spatial))
    line = plan["line"]
    set_line_monitor(device, "band", "paper_bandline", line)
    set_line_monitor(device, "charge", "paper_holeline", line)
    roi = plan["field_roi"]
    device.select(CHARGE)
    device.addefieldmonitor()
    device.set("name", "paper_E_xz")
    device.set("monitor type", 6)  # 2D y-normal
    device.set("x", roi["x_m"])
    device.set("x span", roi["x_span_m"])
    device.set("y", roi["y_m"])
    device.set("z", roi["z_m"])
    device.set("z span", roi["z_span_m"])

    bias = plan["bias"]
    device.setnamed(ANODE, "sweep type", "range")
    device.setnamed(ANODE, "range start", bias["start_V"])
    device.setnamed(ANODE, "range stop", bias["stop_V"])
    device.setnamed(ANODE, "range interval", bias["interval_V"])
    device.setnamed(ANODE, "range backtracking", bias["backtracking"])
    if bias["backtracking"] == "enabled":
        device.setnamed(ANODE, "range min interval", bias["min_interval_V"])
    controls = plan["solver"]
    device.setnamed(CHARGE, "global iteration limit", controls["global_iteration_limit"])
    device.setnamed(CHARGE, "gradient mixing", controls["gradient_mixing"])
    if "solver_type" in controls:
        device.setnamed(CHARGE, "solver type", controls["solver_type"])
    device.setnamed(CHARGE, "use default update limits",
                    1 if controls["use_default_update_limits"] else 0)
    if not controls["use_default_update_limits"]:
        device.setnamed(CHARGE, "dds max update", controls["dds_max_update"])
        device.setnamed(CHARGE, "poisson max update", controls["poisson_max_update"])
    if plan.get("_continuation"):
        device.setnamed(CHARGE, "enable continuation", 1)
        device.setnamed(CHARGE, "continuation filename", str(plan["_continuation"]))
    logging.info("Input=%s; bias=%s; solver=%s; line=%s; roi=%s; continuation=%s",
                 plan["_source"], bias, controls, line, roi,
                 plan.get("_continuation", "none"))


def solver_completed(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return ("Simulation completed successfully" in text
            and "Solver terminated" not in text)


def validate_native(device, plan: dict) -> None:
    names = set(str(device.getresult(CHARGE)).splitlines())
    required = {"anode", "bandstructure", "charge", "electrostatics",
                "thermal", "integrated"}
    if not required.issubset(names):
        raise RuntimeError("Required native result dataset is missing")
    anode = device.getresult(CHARGE, "anode")
    volts = np.asarray(anode["V_anode"], dtype=float).ravel()
    currents = np.asarray(anode["I"])
    if not np.all(np.isfinite(volts)) or not np.all(np.isfinite(currents)):
        raise RuntimeError("Nonfinite voltage or current data")
    for target in plan["required_bias_V"]:
        if not np.any(np.isclose(volts, target, rtol=0, atol=1e-6)):
            raise RuntimeError("A required bias point is absent from native results")
    thermal = device.getresult(CHARGE, "thermal")
    if not {"Q", "T"}.issubset(thermal):
        raise RuntimeError("Thermal Q or T was not saved")
    band = device.getresult(CHARGE, "bandstructure")
    if not {"Ec", "Efn", "Efp", "Ev"}.issubset(band):
        raise RuntimeError("Bandstructure components are missing")
    for name in ("paper_bandline", "paper_holeline", "paper_E_xz"):
        if not str(device.getresult(CHARGE + "::" + name)).strip():
            raise RuntimeError("Required local monitor has no native result")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True,
                        choices=("fig2_0to1", "fig23_0to20", "fig23_cont"))
    args = parser.parse_args()
    plan = load_plan(args.plan)
    run_id = f"s{plan['sequence']:02d}_{args.plan}_{datetime.now():%Y%m%d_%H%M%S_%f}"
    run_dir = RUNS / run_id
    log_dir = LOGS / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    project = run_dir / ("pip_" + args.plan + ".ldev")
    solver_log = run_dir / (project.stem + "_p0.log")
    device = None
    success = False
    try:
        if not API.is_dir():
            raise FileNotFoundError("Lumerical Python API not found")
        shutil.copy2(plan["_source"], project)
        sys.path.insert(0, str(API))
        import lumapi
        device = lumapi.DEVICE(str(project), hide=True)
        configure(device, plan)
        device.save(str(project))
        print("+-------------------+--------------------------------------------+", flush=True)
        print("| 项目              | 功能                                       |", flush=True)
        print("+-------------------+--------------------------------------------+", flush=True)
        print("| 输入              | 复制已完成的 CHARGE 工程                   |", flush=True)
        print("| 求解              | 按配置扫描偏压并保存 E/Q/T/载流子/能带    |", flush=True)
        print("| 截线              | 保存硅 slab 内的能带和空穴 1D 数据         |", flush=True)
        print("| 输出              | 仅保存原生 .ldev 和日志；不生成图表       |", flush=True)
        print("+-------------------+--------------------------------------------+", flush=True)
        print(f"PLAN={args.plan}; CONFIG={plan['_config']}", flush=True)
        print(f"RUN_ID={run_id}", flush=True)
        print(f"PROJECT={project}", flush=True)
        print("RUNNING_CHARGE=1", flush=True)
        device.run("CHARGE")
        if not solver_completed(solver_log):
            raise RuntimeError("Solver did not report successful completion")
        validate_native(device, plan)
        device.save(str(project))
        (FIGURES / run_id).mkdir(parents=True, exist_ok=False)
        logging.info("Native result datasets and requested bias points verified")
        print(f"OPEN_IN_DEVICE={project}", flush=True)
        print(f"LOG_DIRECTORY={log_dir}", flush=True)
        print(f"SCREENSHOT_DIRECTORY={FIGURES / run_id}", flush=True)
        success = True
        return 0
    except Exception:
        logging.exception("CHARGE run did not meet the requested completion criteria")
        print(f"CHECK_LOG={log_dir / 'driver.log'}", file=sys.stderr, flush=True)
        return 1
    finally:
        if device is not None:
            try:
                device.close()
            except Exception:
                logging.exception("Could not close DEVICE")
        for path in run_dir.glob("*.log"):
            try:
                shutil.move(str(path), str(log_dir / path.name))
            except Exception:
                logging.exception("Could not move solver log")
        if not success and run_dir.exists():
            if plan.get("keep_partial"):
                for path in run_dir.glob("*.ldev*"):
                    try:
                        shutil.move(str(path), str(log_dir / path.name))
                        logging.info("Partial project kept at %s", log_dir / path.name)
                        print(f"PARTIAL_KEPT={log_dir / path.name}", flush=True)
                    except Exception:
                        logging.exception("Could not keep partial project")
            if run_dir.parent.resolve() != RUNS.resolve():
                raise RuntimeError("Unsafe output path")
            shutil.rmtree(run_dir)


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        print(f"SETUP_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
