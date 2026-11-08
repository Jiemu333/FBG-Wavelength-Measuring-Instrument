"""Scan both ring indices together after optical alignment; save native ICP files."""
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
CONFIG = CASE / "config" / "08_common_mode_tuning.json"
API = Path(r"D:\Program Files\Lumerical\v242\api\python")


def alignment_module():
    path = CASE / "scripts" / "04_dual_ring_static_alignment.py"
    spec = importlib.util.spec_from_file_location("ring_alignment_common", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load alignment module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(ic, helper, aligner, cfg, neff, ng, aligned_ring, alignment_offset, common_offset):
    frequency = 299792458.0 / float(cfg["wavelength_center_m"])
    loss = float(cfg["waveguide_loss_db_per_cm"]) * 100.0
    couplings = [float(x) for x in cfg["coupling_power_ratios"]]
    radii = [float(x) for x in cfg["ring_radii_m"]]
    for i, radius in enumerate(radii, start=1):
        ring = f"ring{i}"
        index = neff + common_offset + (alignment_offset if ring == aligned_ring else 0.0)
        helper.add_ring(ic, ring, radius, index, ng, frequency, loss, couplings)
    aligner.configure_ona(ic, cfg, 3)
    ic.connect("ONA", "output", "ring1", "port 1")
    ic.connect("ring1", "port 3", "ONA", "input 1")
    ic.connect("ring1", "port 2", "ring2", "port 1")
    ic.connect("ring2", "port 3", "ONA", "input 2")
    ic.connect("ring2", "port 2", "ONA", "input 3")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=CONFIG.name)
    args = parser.parse_args()
    scan_config = (CASE / "config" / args.config).resolve()
    if not scan_config.is_relative_to((CASE / "config").resolve()) or not scan_config.is_file():
        raise FileNotFoundError("Scan config is unavailable or outside this case")
    scan = json.loads(scan_config.read_text(encoding="utf-8-sig"))
    config_path = (CASE / "config" / scan["alignment_config"]).resolve()
    if not config_path.is_relative_to((CASE / "config").resolve()):
        raise ValueError("Alignment config must stay within this case")
    offsets = [float(x) for x in scan["common_index_offsets"]]
    if not offsets or len(set(offsets)) != len(offsets):
        raise ValueError("common_index_offsets must be nonempty and distinct")
    if any(not math.isfinite(x) or x < 0 for x in offsets):
        raise ValueError("Common offsets must be finite and nonnegative")
    tracking_window = float(scan["passband_tracking_window_m"])
    if not math.isfinite(tracking_window) or tracking_window <= 0:
        raise ValueError("passband_tracking_window_m must be positive and finite")
    prefix = scan["run_prefix"]
    if not isinstance(prefix, str) or not prefix.replace("_", "").isalnum():
        raise ValueError("Invalid run prefix")

    aligner = alignment_module()
    align, cold = aligner.load_config(config_path)
    helper = aligner.load_cold_builder()
    run_id = f"{prefix}_{datetime.now():%Y%m%d_%H%M%S_%f}"
    run_dir = CASE / "results" / "runs" / run_id
    log_dir = CASE / "results" / "logs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w",
                        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    print(f"CONFIG={scan_config}", flush=True)
    print(f"RUN_DIRECTORY={run_dir}", flush=True)
    if not API.is_dir():
        raise FileNotFoundError(f"Lumerical API unavailable: {API}")
    sys.path.insert(0, str(API))
    import lumapi

    neff, ng = helper.load_fde_indices(lumapi)
    radii = [float(x) for x in cold["ring_radii_m"]]
    target = float(align["target_wavelength_m"])
    peaks1 = aligner.single_ring_peaks(lumapi, helper, cold, radii[0], neff, ng)
    peaks2 = aligner.single_ring_peaks(lumapi, helper, cold, radii[1], neff, ng)
    peak1 = float(peaks1[np.argmin(np.abs(peaks1 - target))])
    peak2 = float(peaks2[np.argmin(np.abs(peaks2 - target))])
    if peak1 <= peak2:
        aligned_ring, lower_peak, chosen_peak = "ring1", peak1, peak2
    else:
        aligned_ring, lower_peak, chosen_peak = "ring2", peak2, peak1
    alignment_offset = ng * (chosen_peak - lower_peak) / lower_peak
    if not math.isfinite(alignment_offset) or alignment_offset <= 0:
        raise RuntimeError("No finite positive alignment offset was found")
    logging.info("FDE neff=%g ng=%g; aligned ring=%s; alignment offset=%g",
                 neff, ng, aligned_ring, alignment_offset)

    records = []
    for offset in offsets:
        label = f"{offset:.6f}".replace(".", "p")
        project = run_dir / f"dual_ring_common_offset_{label}.icp"
        ic = None
        try:
            ic = lumapi.INTERCONNECT(hide=True)
            build(ic, helper, aligner, cold, neff, ng, aligned_ring,
                  alignment_offset, offset)
            ic.run()
            for port in (1, 2, 3):
                helper.validate_ona_spectrum(ic, port)
            wave, power = aligner.spectrum(ic, 3)
            indices = aligner.local_maxima(wave, power)
            # Follow the main passband by selecting the strongest Drop2 peak near the target.
            nearby = indices[np.abs(wave[indices] - chosen_peak) < tracking_window]
            if nearby.size == 0:
                raise RuntimeError("No Drop2 peak found near the reference passband")
            index = int(nearby[np.argmax(power[nearby])])
            peak_nm = float(wave[index] * 1e9)
            peak_power = float(power[index])
            ic.save(str(project))
            logging.info("common delta_neff=%g; Drop2 peak=%g nm; peak power=%g; project=%s",
                         offset, peak_nm, peak_power, project)
            records.append((offset, project.name, peak_nm, peak_power))
            print(f"COMPLETED_PROJECT={project}", flush=True)
        finally:
            if ic is not None:
                ic.close()

    rows = "\n".join(f"| {o:g} | `{name}` | {w:.6f} | {p:.6g} |"
                     for o, name, w, p in records)
    screenshots = "\n".join(
        f"| `offset_{o:.6f}.png` | `{name}` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |"
        for o, name, _, _ in records)
    readme = f"""# 双微环协同折射率扫描

在 s05 静态对齐基础上，两个环的有效折射率同时增加配置中的 common offset。
这是光学电路参数扫描，**不是**电压、温度或实测标定。

## 工程文件

| common Δneff | 原生工程 | Drop2 峰位 (nm) | 峰值功率透射率 |
|---:|---|---:|---:|
{rows}

## 工程打开后使用方法

用 Lumerical INTERCONNECT 打开上表中的 `.icp`，选原理图中的 `ONA`，
在 Result View 展开 `input 3 → mode 1 → transmission` 并双击。
在 Visualizer 中选择 `Scalar operation = Abs^2`，横轴为 wavelength。
`input 1` 是 Through，`input 2` 是 Drop1。

## 可以得到的结果（及截图）

| 截图名 | 工程内查看位置 | 核验重点 |
|---|---|---|
{screenshots}

截图由用户存入 `results/figures/{run_id}/`，各张图使用相同波长范围与功率标度。
"""
    (run_dir / "README.md").write_text(readme, encoding="utf-8")
    print(f"LOG_DIRECTORY={log_dir}", flush=True)
    print(f"SCREENSHOT_DIRECTORY={CASE / 'results' / 'figures' / run_id}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        logging.exception("Common-index scan failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
