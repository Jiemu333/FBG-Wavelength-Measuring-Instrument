"""Align the cold two-ring Vernier passband by a simulated static index offset.

This is an optical alignment study. It does not convert electrical power or
voltage to temperature and does not use the unfinished CHARGE s20 run.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
API = Path(r"D:\Program Files\Lumerical\v242\api\python")
CONFIG = CASE / "config" / "04_dual_ring_alignment.json"
RUNS = CASE / "results" / "runs"
LOGS = CASE / "results" / "logs"


def load_cold_builder():
    path = CASE / "scripts" / "03_dual_ring_cold.py"
    spec = importlib.util.spec_from_file_location("dual_ring_cold_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load cold-ring builder: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_config(config_path: Path) -> tuple[dict, dict]:
    align = json.loads(config_path.read_text(encoding="utf-8-sig"))
    cold_path = (CASE / "config" / align["cold_config"]).resolve()
    if not cold_path.is_relative_to((CASE / "config").resolve()):
        raise ValueError("cold_config must stay within this case's config directory")
    cold = json.loads(cold_path.read_text(encoding="utf-8-sig"))
    if "coupling_power_ratios" in align:
        candidate_couplings = [float(x) for x in align["coupling_power_ratios"]]
        if len(candidate_couplings) != 2 or any(not 0 < x < 1 for x in candidate_couplings):
            raise ValueError("coupling_power_ratios override must contain two values in (0, 1)")
        cold["coupling_power_ratios"] = candidate_couplings
    target = float(align["target_wavelength_m"])
    if not float(cold["wavelength_start_m"]) < target < float(cold["wavelength_stop_m"]):
        raise ValueError("Target wavelength must lie inside the cold scan")
    if align["adjusted_ring"] != "auto":
        raise ValueError("This alignment script selects the warmed ring automatically")
    if align["adjustment_method"] != "warm_lower_nearby_resonance":
        raise ValueError("Unsupported adjustment method")
    return align, cold


def configure_ona(ic, cfg: dict, outputs: int) -> None:
    ic.addelement("Optical Network Analyzer")
    ic.set("name", "ONA")
    ic.set("input parameter", "start and stop")
    ic.set("start frequency", 299792458.0 / float(cfg["wavelength_stop_m"]))
    ic.set("stop frequency", 299792458.0 / float(cfg["wavelength_start_m"]))
    ic.set("number of points", int(cfg["sample_points"]))
    ic.set("plot kind", "wavelength")
    ic.set("orthogonal identifier", 1)
    ic.set("number of input ports", outputs)
    ic.set("peak analysis", "multiple")
    ic.set("peak at maximum", True)


def spectrum(ic, port: int) -> tuple[np.ndarray, np.ndarray]:
    path = f"input {port}/mode 1/transmission"
    result = ic.getresult("ONA", path)
    if not isinstance(result, dict) or not result:
        raise RuntimeError(f"ONA has no result {path}")
    wave = np.asarray(result["wavelength"], dtype=float).ravel()
    transfer = np.asarray(result["TE transmission"]).ravel()
    if (wave.size < 3 or wave.size != transfer.size
            or not np.isfinite(wave).all() or not np.isfinite(transfer).all()):
        raise RuntimeError(f"ONA {path} has missing or nonfinite samples")
    return wave, np.abs(transfer) ** 2


def local_maxima(wave: np.ndarray, power: np.ndarray) -> np.ndarray:
    indices = np.flatnonzero((power[1:-1] > power[:-2]) &
                             (power[1:-1] >= power[2:])) + 1
    if not indices.size:
        raise RuntimeError("No interior resonance peak was detected")
    return indices


def single_ring_peaks(lumapi, helper, cfg: dict, radius: float,
                      neff: float, ng: float) -> np.ndarray:
    ic = None
    try:
        ic = lumapi.INTERCONNECT(hide=True)
        helper.add_ring(ic, "ring", radius, neff, ng,
                        299792458.0 / float(cfg["wavelength_center_m"]),
                        float(cfg["waveguide_loss_db_per_cm"]) * 100.0,
                        [float(x) for x in cfg["coupling_power_ratios"]])
        configure_ona(ic, cfg, 1)
        ic.connect("ONA", "output", "ring", "port 1")
        ic.connect("ring", "port 2", "ONA", "input 1")
        ic.run()
        wave, power = spectrum(ic, 1)
        peaks = wave[local_maxima(wave, power)]
        logging.info("Standalone ring radius=%g m; resonance count=%d", radius, len(peaks))
        return peaks
    finally:
        if ic is not None:
            ic.close()


def build_cascaded(ic, helper, cfg: dict, neff: float, ng: float,
                   adjusted_ring: str, index_offset: float) -> None:
    frequency = 299792458.0 / float(cfg["wavelength_center_m"])
    loss = float(cfg["waveguide_loss_db_per_cm"]) * 100.0
    couplings = [float(x) for x in cfg["coupling_power_ratios"]]
    radii = [float(x) for x in cfg["ring_radii_m"]]
    helper.add_ring(ic, "ring1", radii[0], neff + (index_offset if adjusted_ring == "ring1" else 0), ng,
                    frequency, loss, couplings)
    helper.add_ring(ic, "ring2", radii[1], neff + (index_offset if adjusted_ring == "ring2" else 0),
                    ng, frequency, loss, couplings)
    configure_ona(ic, cfg, 3)
    ic.connect("ONA", "output", "ring1", "port 1")
    ic.connect("ring1", "port 3", "ONA", "input 1")
    ic.connect("ring1", "port 2", "ring2", "port 1")
    ic.connect("ring2", "port 3", "ONA", "input 2")
    ic.connect("ring2", "port 2", "ONA", "input 3")


def write_run_readme(run_dir: Path, chosen_wavelength: float,
                     adjusted_ring: str, index_offset: float,
                     coupling_power_ratios: list[float]) -> None:
    content = f"""# 双微环静态谐振对齐

## `dual_ring_static_aligned.icp`

### 工程打开后使用方法

用 Ansys Lumerical INTERCONNECT 打开该 `.icp`。在原理图中，`ring1` 的 Drop
进入 `ring2`；`ring1` 的 Through 接 ONA `input 1`，`ring2` 的 Through 接
ONA `input 2`（Drop1），`ring2` 的 Drop 接 ONA `input 3`（Drop2）。
在 Result View 展开 `ONA → input 1/2/3 → mode 1 → transmission`，双击要看的结果，
Visualizer 的 `Scalar operation` 选 `Abs^2`，横轴选波长。

### 可以得到的结果（及截图）

| 截图名称 | 工程内查看位置 | 核验重点 |
|---|---|---|
| `aligned_through.png` | `ONA → input 1 → mode 1 → transmission` | 第一环谐振凹口和波长范围 |
| `aligned_drop1.png` | `ONA → input 2 → mode 1 → transmission` | 两环级联后的剩余谱 |
| `aligned_drop2.png` | `ONA → input 3 → mode 1 → transmission` | 共同谐振峰是否移入 1550 nm 附近、主峰与旁峰 |
| `aligned_schematic.png` | 原理图 | 两环连接及三个输出端口 |

截图由用户手动保存到本算例 `results/figures/` 下与本运行目录同名的文件夹。
此次对齐目标共振波长为 `{chosen_wavelength * 1e9:.6f} nm`，
`{adjusted_ring}` 的静态有效折射率增加量为 `{index_offset:.9g}`。这些量来自本次仿真计算，
两个环的总线功率耦合系数均设为 `{coupling_power_ratios[0]:.6g}`（第一总线）和
`{coupling_power_ratios[1]:.6g}`（第二总线）。
并非热仿真测得的电压、功率或温度。只有在 CHARGE/HEAT 结果通过核验后，
才能建立电压到折射率和通带波长的关系。
"""
    (run_dir / "README.md").write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=CONFIG.name)
    args = parser.parse_args()
    config_path = (CASE / "config" / args.config).resolve()
    if not config_path.is_relative_to((CASE / "config").resolve()) or not config_path.is_file():
        raise FileNotFoundError("Alignment config is unavailable or outside the case")
    align, cold = load_config(config_path)
    helper = load_cold_builder()
    prefix = align.get("run_prefix", "s03_dual_ring_align")
    if not isinstance(prefix, str) or not prefix.replace("_", "").isalnum():
        raise ValueError("run_prefix must contain only letters, digits, and underscores")
    run_id = f"{prefix}_{datetime.now():%Y%m%d_%H%M%S_%f}"
    run_dir = RUNS / run_id
    log_dir = LOGS / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    print("| 项目 | 功能 | 原生输出 |", flush=True)
    print("|---|---|---|", flush=True)
    print("| 双环静态对齐 | 由单环谐振自动选择正向折射率偏置 | INTERCONNECT .icp |", flush=True)
    print(f"CONFIG={config_path}", flush=True)
    print(f"RUN_DIRECTORY={run_dir}", flush=True)
    if not API.is_dir():
        raise FileNotFoundError(f"Lumerical API not found: {API}")
    sys.path.insert(0, str(API))
    import lumapi

    neff, ng = helper.load_fde_indices(lumapi)
    radii = [float(x) for x in cold["ring_radii_m"]]
    peaks1 = single_ring_peaks(lumapi, helper, cold, radii[0], neff, ng)
    peaks2 = single_ring_peaks(lumapi, helper, cold, radii[1], neff, ng)
    target = float(align["target_wavelength_m"])
    peak1 = float(peaks1[np.argmin(np.abs(peaks1 - target))])
    peak2 = float(peaks2[np.argmin(np.abs(peaks2 - target))])
    if peak1 <= peak2:
        adjusted_ring = "ring1"
        lower_peak, chosen_peak = peak1, peak2
    else:
        adjusted_ring = "ring2"
        lower_peak, chosen_peak = peak2, peak1
    offset = ng * (chosen_peak - lower_peak) / lower_peak
    if not math.isfinite(offset) or offset < 0:
        raise RuntimeError("Calculated index offset is not a positive finite number")
    logging.info("Nearby ring1 peak=%g m; ring2 peak=%g m; adjust=%s; estimated positive delta_neff=%g",
                 peak1, peak2, adjusted_ring, offset)

    project = run_dir / "dual_ring_static_aligned.icp"
    ic = None
    try:
        ic = lumapi.INTERCONNECT(hide=True)
        build_cascaded(ic, helper, cold, neff, ng, adjusted_ring, offset)
        ic.run()
        for port in (1, 2, 3):
            helper.validate_ona_spectrum(ic, port)
        wave, power = spectrum(ic, 3)
        peak_indices = local_maxima(wave, power)
        closest = peak_indices[np.argmin(np.abs(wave[peak_indices] - chosen_peak))]
        grid_step = float(np.median(np.diff(np.sort(wave))))
        alignment_error = abs(float(wave[closest]) - chosen_peak)
        logging.info("Aligned Drop2 peak=%g m; target peak=%g m; error=%g m; grid step=%g m; power=%g",
                     wave[closest], chosen_peak, alignment_error, grid_step, power[closest])
        if alignment_error > 2 * grid_step:
            raise RuntimeError("Common Drop2 resonance was not aligned within two spectral samples")
        ic.save(str(project))
        write_run_readme(run_dir, chosen_peak, adjusted_ring, offset,
                         [float(x) for x in cold["coupling_power_ratios"]])
        print(f"OPEN_IN_INTERCONNECT={project}", flush=True)
        print(f"LOG_DIRECTORY={log_dir}", flush=True)
        print(f"SCREENSHOT_DIRECTORY={CASE / 'results' / 'figures' / run_id}", flush=True)
        return 0
    finally:
        if ic is not None:
            ic.close()


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        logging.exception("Static dual-ring alignment failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
