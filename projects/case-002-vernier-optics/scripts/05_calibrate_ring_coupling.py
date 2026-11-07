"""Compare candidate ring coupling values with a paper-reported loaded Q.

The paper value and all sweep inputs live in config/05_ring_coupling_q.json.
Only the selected native INTERCONNECT project and solver log are retained.
"""
from __future__ import annotations

import importlib.util
import json
import logging
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.signal import find_peaks, peak_prominences, peak_widths

CASE = Path(__file__).resolve().parents[1]
API = Path(r"D:\Program Files\Lumerical\v242\api\python")
CONFIG = CASE / "config" / "05_ring_coupling_q.json"
RUNS = CASE / "results" / "runs"
LOGS = CASE / "results" / "logs"


def load_helper():
    path = CASE / "scripts" / "03_dual_ring_cold.py"
    spec = importlib.util.spec_from_file_location("cold_ring_builder_for_q", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load ring builder: {path}")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return helper


def load_config() -> tuple[dict, dict]:
    fit = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    config_path = (CASE / "config" / fit["cold_config"]).resolve()
    if not config_path.is_relative_to((CASE / "config").resolve()):
        raise ValueError("cold_config is outside this case")
    cold = json.loads(config_path.read_text(encoding="utf-8-sig"))
    if fit["target_ring"] != "ring1":
        raise ValueError("This calibration uses the paper's first-ring Through port")
    if float(fit["paper_loaded_q"]) <= 0:
        raise ValueError("paper_loaded_q must be positive")
    candidates = [float(x) for x in fit["power_coupling_candidates"]]
    if not candidates or len(set(candidates)) != len(candidates):
        raise ValueError("power_coupling_candidates must be nonempty and distinct")
    if any(not 0 < k < 1 for k in candidates):
        raise ValueError("Every power coupling candidate must be between 0 and 1")
    if not float(cold["wavelength_start_m"]) < float(fit["target_wavelength_m"]) < float(cold["wavelength_stop_m"]):
        raise ValueError("target_wavelength_m must be within the scanned band")
    return fit, cold


def configure_ona(ic, cfg: dict, input_ports: int) -> None:
    ic.addelement("Optical Network Analyzer")
    ic.set("name", "ONA")
    ic.set("input parameter", "start and stop")
    ic.set("start frequency", 299792458.0 / float(cfg["wavelength_stop_m"]))
    ic.set("stop frequency", 299792458.0 / float(cfg["wavelength_start_m"]))
    ic.set("number of points", int(cfg["sample_points"]))
    ic.set("plot kind", "wavelength")
    ic.set("orthogonal identifier", 1)
    ic.set("number of input ports", input_ports)


def through_metrics(ic, target_wavelength: float) -> dict:
    result = ic.getresult("ONA", "input 1/mode 1/transmission")
    wavelength = np.asarray(result["wavelength"], dtype=float).ravel()
    transfer = np.asarray(result["TE transmission"]).ravel()
    if (wavelength.size < 3 or wavelength.size != transfer.size
            or not np.isfinite(wavelength).all() or not np.isfinite(transfer).all()):
        raise RuntimeError("Through spectrum is missing or nonfinite")
    power = np.abs(transfer) ** 2
    dips = find_peaks(-power)[0]
    if not dips.size:
        raise RuntimeError("Through spectrum has no resonance dip")
    index = int(dips[np.argmin(np.abs(wavelength[dips] - target_wavelength))])
    sample_step = abs(float(np.median(np.diff(wavelength))))
    width_samples = float(peak_widths(-power, [index], rel_height=0.5)[0][0])
    linewidth = width_samples * sample_step
    prominence = float(peak_prominences(-power, [index])[0][0])
    baseline = float(power[index]) + prominence
    if not linewidth > 0 or not baseline > 0 or not power[index] > 0:
        raise RuntimeError("Cannot calculate Q or extinction from Through dip")
    loaded_q = float(wavelength[index]) / linewidth
    extinction_db = 10.0 * math.log10(baseline / float(power[index]))
    if not math.isfinite(loaded_q) or not math.isfinite(extinction_db):
        raise RuntimeError("Calculated Through metrics are nonfinite")
    return {"resonance_m": float(wavelength[index]), "linewidth_m": linewidth,
            "loaded_q": loaded_q, "extinction_db": extinction_db}


def probe_candidate(lumapi, helper, cold: dict, coupling: float,
                    neff: float, ng: float, target: float) -> dict:
    ic = None
    try:
        ic = lumapi.INTERCONNECT(hide=True)
        helper.add_ring(ic, "ring1", float(cold["ring_radii_m"][0]), neff, ng,
                        299792458.0 / float(cold["wavelength_center_m"]),
                        float(cold["waveguide_loss_db_per_cm"]) * 100.0,
                        [coupling, coupling])
        configure_ona(ic, cold, 1)
        ic.connect("ONA", "output", "ring1", "port 1")
        ic.connect("ring1", "port 3", "ONA", "input 1")
        ic.run()
        metrics = through_metrics(ic, target)
        logging.info("Candidate coupling=%g; resonance=%g m; loaded_Q=%g; linewidth=%g m; extinction=%g dB",
                     coupling, metrics["resonance_m"], metrics["loaded_q"],
                     metrics["linewidth_m"], metrics["extinction_db"])
        return metrics
    finally:
        if ic is not None:
            ic.close()


def run_final(lumapi, helper, cold: dict, coupling: float,
              neff: float, ng: float, target: float, project: Path) -> dict:
    ic = None
    try:
        ic = lumapi.INTERCONNECT(hide=True)
        frequency = 299792458.0 / float(cold["wavelength_center_m"])
        loss_db_per_m = float(cold["waveguide_loss_db_per_cm"]) * 100.0
        for i, radius in enumerate(cold["ring_radii_m"], start=1):
            helper.add_ring(ic, f"ring{i}", float(radius), neff, ng,
                            frequency, loss_db_per_m, [coupling, coupling])
        configure_ona(ic, cold, 3)
        ic.connect("ONA", "output", "ring1", "port 1")
        ic.connect("ring1", "port 3", "ONA", "input 1")
        ic.connect("ring1", "port 2", "ring2", "port 1")
        ic.connect("ring2", "port 3", "ONA", "input 2")
        ic.connect("ring2", "port 2", "ONA", "input 3")
        ic.run()
        for port in (1, 2, 3):
            helper.validate_ona_spectrum(ic, port)
        metrics = through_metrics(ic, target)
        logging.info("Final dual-ring Through: loaded_Q=%g; extinction=%g dB",
                     metrics["loaded_q"], metrics["extinction_db"])
        ic.save(str(project))
        return metrics
    finally:
        if ic is not None:
            ic.close()


def write_run_readme(run_dir: Path, coupling: float, metrics: dict, fit: dict) -> None:
    content = f"""# 双微环耦合参数校准

## `dual_ring_q_calibrated.icp`

### 工程打开后使用方法

在 Ansys Lumerical INTERCONNECT 打开本工程。选中 `ONA`，在 Result View
展开 `input 1/2/3 → mode 1 → transmission`，分别对应 Through、Drop1、Drop2。
双击结果后在 Visualizer 的 `Scalar operation` 选 `Abs^2`，查看功率透射谱。

### 可以得到的结果（及截图）

| 截图名称 | 工程内查看位置 | 核验重点 |
|---|---|---|
| `q_calibrated_through.png` | `ONA → input 1 → mode 1 → transmission` | 1550 nm 附近的第一环谐振凹口、半高宽及功率基线 |
| `q_calibrated_drop2.png` | `ONA → input 3 → mode 1 → transmission` | 双环冷态共同峰和旁峰 |
| `q_calibrated_schematic.png` | 原理图 | 两环连接、三个输出端口、耦合系数属性 |

截图由用户手动保存到本算例 `results/figures/` 下与本运行目录同名的文件夹。

| 本轮记录 | 数值 | 说明 |
|---|---:|---|
| 两个总线耦合系数 | `{coupling:.6g}` | 电路模型的功率耦合系数，尚未由 200 nm 间隙直接提取 |
| Through 加载 Q | `{metrics['loaded_q']:.3f}` | 从原生光谱的半深度线宽计算 |
| Through 消光比 | `{metrics['extinction_db']:.3f} dB` | 从原生光谱的凹口深度计算 |
| 论文报告的加载 Q | `{float(fit['paper_loaded_q']):.0f}` | 文献参考，仅用于参数校准 |
| 论文报告的消光比 | `约 {float(fit['paper_through_extinction_db']):.0f} dB` | 对比项，未作为本轮单目标优化约束 |

本工程仍是冷态电路模型；耦合间隙、弯曲损耗、热调谐和光栅耦合器包络尚未由器件级仿真验证。
"""
    (run_dir / "README.md").write_text(content, encoding="utf-8")


def main() -> int:
    fit, cold = load_config()
    helper = load_helper()
    run_id = f"s04_ring_q_fit_{datetime.now():%Y%m%d_%H%M%S_%f}"
    run_dir = RUNS / run_id
    log_dir = LOGS / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    print("| 项目 | 功能 | 原生输出 |", flush=True)
    print("|---|---|---|", flush=True)
    print("| 微环耦合校准 | 在配置候选值中选择最接近论文加载 Q 的功率耦合系数 | INTERCONNECT .icp |", flush=True)
    print(f"CONFIG={CONFIG}", flush=True)
    print(f"RUN_DIRECTORY={run_dir}", flush=True)
    if not API.is_dir():
        raise FileNotFoundError(f"Lumerical API not found: {API}")
    sys.path.insert(0, str(API))
    import lumapi

    neff, ng = helper.load_fde_indices(lumapi)
    target = float(fit["target_wavelength_m"])
    candidates = [float(x) for x in fit["power_coupling_candidates"]]
    measurements = [probe_candidate(lumapi, helper, cold, k, neff, ng, target)
                    for k in candidates]
    best_index = min(range(len(candidates)),
                     key=lambda i: abs(measurements[i]["loaded_q"] - float(fit["paper_loaded_q"])))
    selected = candidates[best_index]
    logging.info("Selected coupling=%g from %d config candidates; paper Q=%g; simulated single-ring Q=%g",
                 selected, len(candidates), float(fit["paper_loaded_q"]),
                 measurements[best_index]["loaded_q"])
    project = run_dir / "dual_ring_q_calibrated.icp"
    final_metrics = run_final(lumapi, helper, cold, selected, neff, ng, target, project)
    write_run_readme(run_dir, selected, final_metrics, fit)
    print(f"OPEN_IN_INTERCONNECT={project}", flush=True)
    print(f"LOG_DIRECTORY={log_dir}", flush=True)
    print(f"SCREENSHOT_DIRECTORY={CASE / 'results' / 'figures' / run_id}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        logging.exception("Ring coupling calibration failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
