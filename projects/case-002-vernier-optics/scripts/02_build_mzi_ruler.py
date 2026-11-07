"""Build and run standalone C-band MZI wavelength-ruler design cases.

The waveguide cross-section is taken from config/01_cold.json. Candidate path
imbalances and sweep range are supplied by config/02_mzi_ruler.json.
No plots or exported result tables are generated; spectra stay in .icp files.
"""
from __future__ import annotations

import importlib.util
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
API = Path(r"D:\Program Files\Lumerical\v242\api\python")
RUNS = CASE / "results" / "runs"
LOGS = CASE / "results" / "logs"


def load_builder():
    path = CASE / "scripts" / "01_build_mode_cross_section.py"
    spec = importlib.util.spec_from_file_location("mode_cross_section_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load MODE cross-section builder: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scalar_neff(mode, mode_index: int) -> complex:
    last_error = None
    for result_name in (f"FDE::data::mode{mode_index}", f"FDE::mode{mode_index}"):
        try:
            raw = mode.getresult(result_name, "neff")
            if isinstance(raw, dict):
                raw = raw.get("neff", next(iter(raw.values())))
            arr = np.asarray(raw).squeeze()
            return complex(arr.item())
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Cannot read effective index for FDE mode {mode_index}: {last_error}")


def compute_waveguide_indices(cfg: dict, mode_builder, run_dir: Path) -> tuple[float, float]:
    import lumapi

    mode_project = run_dir / "mzi_waveguide_mode.lms"
    session = None
    try:
        session = lumapi.MODE(hide=True)
        mode_builder.build(session, mode_builder.load_config(CASE / "config" / "01_cold.json"))
        wl0 = float(cfg["wavelength_center_m"])
        dwl = float(cfg["wavelength_derivative_step_m"])
        neff = []
        for wl in (wl0 - dwl, wl0, wl0 + dwl):
            session.switchtolayout()
            session.setnamed("FDE", "wavelength", wl)
            session.findmodes()
            candidates = []
            for idx in range(1, int(mode_builder.load_config(CASE / "config" / "01_cold.json")["fde"]["trial_modes"]) + 1):
                try:
                    value = scalar_neff(session, idx)
                    if np.isfinite(value.real):
                        candidates.append((idx, value))
                except Exception as exc:
                    logging.info("Could not read FDE mode %d at %.12g m: %s", idx, wl, exc)
            if not candidates:
                raise RuntimeError(f"FDE found no usable mode at wavelength {wl:.9g} m")
            # The highest-index guided solution is used as the fundamental-mode candidate.
            idx, value = max(candidates, key=lambda item: item[1].real)
            neff.append(value.real)
            logging.info("FDE wavelength %.12g m, selected mode %d", wl, idx)
        ng = neff[1] - wl0 * (neff[2] - neff[0]) / (2.0 * dwl)
        if not np.isfinite(ng) or ng <= 0:
            raise RuntimeError(f"Computed group index is invalid: {ng}")
        session.switchtolayout()
        session.setnamed("FDE", "wavelength", wl0)
        session.findmodes()
        session.save(str(mode_project))
        logging.info("Computed waveguide indices at %.9g m: neff=%.9f, ng=%.9f", wl0, neff[1], ng)
        return float(neff[1]), float(ng)
    finally:
        if session is not None:
            session.close()


def run_mzi_case(lumapi, cfg: dict, run_dir: Path, delta_l: float,
                 neff: float, ng: float, case_number: int) -> Path:
    wavelength_start = float(cfg["wavelength_start_m"])
    wavelength_stop = float(cfg["wavelength_stop_m"])
    if not 0 < wavelength_start < wavelength_stop:
        raise ValueError("Wavelength sweep limits must be positive and increasing")
    project = run_dir / f"mzi_ruler_dL_{round(delta_l * 1e6):03d}um.icp"
    session = None
    try:
        session = lumapi.INTERCONNECT(hide=True)
        session.addelement("Mach Zehnder Interferometer Unidirectional")
        session.set("name", "MZI_ruler")
        session.set("length 1", 0.0)
        session.set("length 2", float(delta_l))
        session.set("effective index 1", neff)
        session.set("group index 1", ng)
        session.set("coupling coefficient 1 1", float(cfg["coupling_power_ratios"][0]))
        session.set("coupling coefficient 1 2", float(cfg["coupling_power_ratios"][1]))

        session.addelement("Optical Network Analyzer")
        session.set("name", "ONA")
        session.set("input parameter", "start and stop")
        session.set("start frequency", 299792458.0 / wavelength_stop)
        session.set("stop frequency", 299792458.0 / wavelength_start)
        session.set("number of points", int(cfg["sample_points"]))
        session.set("plot kind", "wavelength")
        session.set("orthogonal identifier", 1)
        session.set("number of input ports", 1)
        session.set("peak analysis", "multiple")
        session.set("peak at maximum", True)

        # Element library variants may expose either numbered or directional ports.
        input_port = None
        for candidate in ("port 1", "input", "input 1", "port_1"):
            try:
                session.connect("ONA", "output", "MZI_ruler", candidate)
                input_port = candidate
                break
            except Exception:
                continue
        if input_port is None:
            raise RuntimeError("Could not identify the MZI optical input port")
        output_port = None
        for candidate in ("port 3", "output", "output 1", "output 2"):
            try:
                session.connect("MZI_ruler", candidate, "ONA", "input 1")
                output_port = candidate
                break
            except Exception:
                continue
        if output_port is None:
            raise RuntimeError("Could not identify the MZI optical output port")
        session.run()
        result = session.getresult("ONA", "input 1/mode 1/transmission")
        if not isinstance(result, dict) or not result:
            raise RuntimeError("ONA completed without returning the expected input 1/mode 1 spectrum")
        wavelengths = np.asarray(result.get("wavelength"), dtype=float).squeeze()
        transmission = np.asarray(result.get("TE transmission")).squeeze()
        if (wavelengths.size < 2 or transmission.size < 2
                or not np.isfinite(wavelengths).all()
                or not np.isfinite(transmission).all()):
            raise RuntimeError("ONA spectrum is empty or contains non-finite samples")
        logging.info("Verified ONA spectrum: %d wavelengths, %.12g to %.12g m",
                     wavelengths.size, float(np.min(wavelengths)), float(np.max(wavelengths)))
        try:
            peak_fsr = session.getresult("ONA", "input 1/mode 1/peak/free spectral range")
            logging.info("ONA peak FSR result is available; data fields=%s",
                         list(peak_fsr.keys()) if isinstance(peak_fsr, dict) else type(peak_fsr).__name__)
        except Exception as exc:
            logging.info("ONA peak-FSR result unavailable for this span: %s", exc)
        session.save(str(project))
        logging.info("MZI case %d completed: delta_L=%.9g m; ONA result keys=%s",
                     case_number, delta_l, list(result.keys()))
        return project
    finally:
        if session is not None:
            session.close()


def main() -> int:
    config_path = CASE / "config" / "02_mzi_ruler.json"
    cfg = json.loads(config_path.read_text(encoding="utf-8-sig"))
    candidates = [float(x) for x in cfg["arm_length_differences_m"]]
    if not candidates or any(x <= 0 for x in candidates):
        raise ValueError("arm_length_differences_m must contain positive values")
    run_id = f"s01_mzi_ruler_{datetime.now():%Y%m%d_%H%M%S}"
    run_dir = RUNS / run_id
    log_dir = LOGS / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    print("| Task | Inputs and operation | Native result |", flush=True)
    print("|---|---|---|", flush=True)
    print("| Standalone MZI ruler | C-band; 50/100 um path imbalance; neff/ng from MODE FDE | INTERCONNECT .icp |", flush=True)
    print(f"| Config | {config_path} | {run_dir} |", flush=True)
    print(f"RUN_ID={run_id}", flush=True)
    print(f"RUN_DIRECTORY={run_dir}", flush=True)
    sys.path.insert(0, str(API))
    import lumapi
    mode_builder = load_builder()
    neff, ng = compute_waveguide_indices(cfg, mode_builder, run_dir)
    projects = []
    for i, delta_l in enumerate(candidates, start=1):
        projects.append(run_mzi_case(lumapi, cfg, run_dir, delta_l, neff, ng, i))
    readme = run_dir / "README.md"
    rows = ["# MZI 独立标尺设计对比", "", "## 工程打开后使用方法", ""]
    for project in projects:
        rows.extend([f"### {project.name}", "", "在 Ansys Lumerical INTERCONNECT 中打开此工程。选中 `ONA`，在 Result View 展开 `input 1` → `mode 1` → `transmission` 并双击查看；横轴是波长，曲线的复数模长平方对应功率透射率。通过相邻干涉峰的间距比较该臂长差下的 FSR。", ""])
    rows.extend(["## ONA 自动 FSR 结果", "", "在 Result View 中展开 `ONA` → `input 1` → `mode 1` → `peak` → `free spectral range` 查看自动识别的峰间距。透射功率曲线在 `input 1` → `mode 1` → `transmission`；Visualizer 的 `Scalar operation` 选择 `Abs^2`。", "", "## 可以得到的结果", "", "- 两种臂长差的 MZI 周期透射谱，用于比较 FSR 与条纹密度。", "- MODE 截面工程 `mzi_waveguide_mode.lms`，可查看 1.55 µm 处选中模式的场分布和 FDE 结果。", "- 当前模型采用理想 50:50 耦合器；尚未纳入实际耦合器偏差、传播损耗、工艺误差和温度漂移。", ""])
    readme.write_text("\n".join(rows), encoding="utf-8")
    print(f"OPEN_IN_INTERCONNECT={projects[0]}", flush=True)
    print(f"OPEN_IN_MODE={run_dir / 'mzi_waveguide_mode.lms'}", flush=True)
    print(f"LOG_DIRECTORY={log_dir}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        logging.exception("MZI wavelength-ruler simulation failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
