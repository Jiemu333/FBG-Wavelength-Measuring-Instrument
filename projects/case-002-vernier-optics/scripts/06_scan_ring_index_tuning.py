"""Scan the aligned ring's effective index and save native INTERCONNECT projects.

The sweep is optical only. It does not infer voltage, temperature, or heater power.
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
CONFIG = CASE / "config" / "07_index_tuning_scan.json"
API = Path(r"D:\Program Files\Lumerical\v242\api\python")


def load_alignment_module():
    path = CASE / "scripts" / "04_dual_ring_static_alignment.py"
    spec = importlib.util.spec_from_file_location("ring_alignment", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load alignment module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    fractions = [float(x) for x in scan["index_offset_fractions"]]
    if not fractions or len(set(fractions)) != len(fractions):
        raise ValueError("index_offset_fractions must be nonempty and distinct")
    if any(not math.isfinite(x) or x < 0 for x in fractions):
        raise ValueError("Every fraction must be finite and nonnegative")
    prefix = scan["run_prefix"]
    if not isinstance(prefix, str) or not prefix.replace("_", "").isalnum():
        raise ValueError("Invalid run prefix")

    aligner = load_alignment_module()
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
        adjusted_ring, lower_peak, chosen_peak = "ring1", peak1, peak2
    else:
        adjusted_ring, lower_peak, chosen_peak = "ring2", peak2, peak1
    alignment_offset = ng * (chosen_peak - lower_peak) / lower_peak
    if not math.isfinite(alignment_offset) or alignment_offset <= 0:
        raise RuntimeError("No finite positive alignment offset was found")
    logging.info("FDE neff=%g ng=%g; tuned ring=%s; alignment offset=%g",
                 neff, ng, adjusted_ring, alignment_offset)

    rows = []
    for fraction in fractions:
        label = f"{fraction:.3f}".replace(".", "p")
        project = run_dir / f"dual_ring_index_fraction_{label}.icp"
        ic = None
        try:
            ic = lumapi.INTERCONNECT(hide=True)
            aligner.build_cascaded(ic, helper, cold, neff, ng,
                                   adjusted_ring, fraction * alignment_offset)
            ic.run()
            for port in (1, 2, 3):
                helper.validate_ona_spectrum(ic, port)
            wave, power = aligner.spectrum(ic, 3)
            candidates = aligner.local_maxima(wave, power)
            nearest = int(candidates[np.argmin(np.abs(wave[candidates] - chosen_peak))])
            peak_nm = float(wave[nearest] * 1e9)
            peak_power = float(power[nearest])
            ic.save(str(project))
            logging.info("fraction=%g; delta_neff=%g; nearest Drop2 peak=%g nm; peak power=%g; project=%s",
                         fraction, fraction * alignment_offset, peak_nm, peak_power, project)
            rows.append((fraction, project.name, peak_nm, peak_power))
            print(f"COMPLETED_PROJECT={project}", flush=True)
        finally:
            if ic is not None:
                ic.close()

    table = "\n".join(f"| {f:g} | `{name}` | {w:.6f} | {p:.6g} |"
                      for f, name, w, p in rows)
    screenshots = "\n".join(
        f"| `fraction_{f:.3f}.png` | `{name}` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |"
        for f, name, _, _ in rows)
    readme = f"""# 双微环折射率扫描

本次只扫描电路模型中 `{adjusted_ring}` 的有效折射率。折射率改变量等于
`fraction × {alignment_offset:.9g}`；1.0 对应 s05 的静态对齐输入。
各 fraction 是配置中的探索值，不代表电压、温度或实测数据。

## 工程文件

| fraction | 原生工程 | 就近 Drop2 峰位 (nm) | 峰值功率透射率 |
|---:|---|---:|---:|
{table}

## 工程打开后使用方法

用 Lumerical INTERCONNECT 打开上表对应的 `.icp`，在原理图选 `ONA`。
在 Result View 展开 `input 3 → mode 1 → transmission`，双击并在
Visualizer 把 `Scalar operation` 设为 `Abs^2`、横轴设为 wavelength，
得到 Drop2 功率透射谱。`input 1` 为 Through，`input 2` 为 Drop1。

## 可以得到的结果（及截图）

| 截图 | 对应工程和位置 | 重点 |
|---|---|---|
{screenshots}

截图由用户保存到 `results/figures/{run_id}/`。不同图使用相同波长范围和 `Abs^2` 标度。
"""
    (run_dir / "README.md").write_text(readme, encoding="utf-8")
    print(f"LOG_DIRECTORY={log_dir}", flush=True)
    print(f"SCREENSHOT_DIRECTORY={CASE / 'results' / 'figures' / run_id}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        logging.exception("Index scan failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
