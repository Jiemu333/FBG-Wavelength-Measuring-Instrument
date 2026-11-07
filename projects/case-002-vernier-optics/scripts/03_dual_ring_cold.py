"""Build and solve a cold cascaded two-ring Vernier filter in INTERCONNECT.

All design inputs are read from config/03_dual_ring_cold.json or the saved
MODE FDE project. Spectra remain in the native .icp project.
"""
from __future__ import annotations

import json
import logging
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
API = Path(r"D:\Program Files\Lumerical\v242\api\python")
CONFIG = CASE / "config" / "03_dual_ring_cold.json"
MODE_PROJECT = (CASE / "results" / "runs" / "s01_mzi_ruler_20261106_172434"
                / "mzi_waveguide_mode.lms")
RUNS = CASE / "results" / "runs"
LOGS = CASE / "results" / "logs"


def load_config() -> dict:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    start = float(cfg["wavelength_start_m"])
    stop = float(cfg["wavelength_stop_m"])
    center = float(cfg["wavelength_center_m"])
    if not 0 < start < center < stop:
        raise ValueError("Wavelength limits must satisfy 0 < start < center < stop")
    if int(cfg["sample_points"]) < 3:
        raise ValueError("sample_points must be at least 3")
    radii = [float(x) for x in cfg["ring_radii_m"]]
    if len(radii) != 2 or any(x <= 0 for x in radii) or radii[0] == radii[1]:
        raise ValueError("ring_radii_m must contain two distinct positive radii")
    couplings = [float(x) for x in cfg["coupling_power_ratios"]]
    if len(couplings) != 2 or any(not 0 < x < 1 for x in couplings):
        raise ValueError("coupling_power_ratios must contain two values between 0 and 1")
    if float(cfg["waveguide_loss_db_per_cm"]) < 0:
        raise ValueError("waveguide_loss_db_per_cm must be nonnegative")
    return cfg


def read_mode_scalar(mode, key: str) -> float:
    errors = []
    for obj in ("FDE::data::mode1", "FDE::mode1"):
        for method in (mode.getdata, mode.getresult):
            try:
                value = method(obj, key)
                if isinstance(value, dict):
                    value = value[key]
                scalar = float(np.real(np.asarray(value).squeeze().item()))
                if math.isfinite(scalar) and scalar > 0:
                    return scalar
            except Exception as exc:
                errors.append(f"{obj}/{key}: {exc}")
    raise RuntimeError(f"FDE mode 1 has no usable {key}: {'; '.join(errors)}")


def load_fde_indices(lumapi) -> tuple[float, float]:
    if not MODE_PROJECT.is_file():
        raise FileNotFoundError(f"Saved waveguide mode project is missing: {MODE_PROJECT}")
    mode = None
    try:
        mode = lumapi.MODE(hide=True)
        mode.load(str(MODE_PROJECT))
        neff = read_mode_scalar(mode, "neff")
        ng = read_mode_scalar(mode, "ng")
        logging.info("Source FDE project=%s; neff=%g; ng=%g", MODE_PROJECT, neff, ng)
        return neff, ng
    finally:
        if mode is not None:
            mode.close()


def add_ring(ic, name: str, radius: float, neff: float, ng: float,
             frequency: float, loss_db_per_m: float, couplings: list[float]) -> None:
    ic.addelement("Double Bus Ring Resonator")
    ic.set("name", name)
    ic.set("configuration", "bidirectional")
    ic.set("frequency", frequency)
    ic.set("length", 2.0 * math.pi * radius)
    ic.set("orthogonal identifier 1", 1)
    ic.set("effective index 1", neff)
    ic.set("group index 1", ng)
    ic.set("loss 1", loss_db_per_m)
    ic.set("coupling coefficient 1 1", couplings[0])
    ic.set("coupling coefficient 1 2", couplings[1])


def configure_ona(ic, cfg: dict) -> None:
    ic.addelement("Optical Network Analyzer")
    ic.set("name", "ONA")
    ic.set("input parameter", "start and stop")
    ic.set("start frequency", 299792458.0 / float(cfg["wavelength_stop_m"]))
    ic.set("stop frequency", 299792458.0 / float(cfg["wavelength_start_m"]))
    ic.set("number of points", int(cfg["sample_points"]))
    ic.set("plot kind", "wavelength")
    ic.set("orthogonal identifier", 1)
    ic.set("number of input ports", 3)
    ic.set("peak analysis", "multiple")
    ic.set("peak at maximum", True)


def validate_ona_spectrum(ic, port: int) -> None:
    name = f"input {port}/mode 1/transmission"
    result = ic.getresult("ONA", name)
    if not isinstance(result, dict):
        raise RuntimeError(f"ONA {name} is unavailable")
    wave = np.asarray(result.get("wavelength"), dtype=float).squeeze()
    transfer = np.asarray(result.get("TE transmission")).squeeze()
    if (wave.size < 3 or wave.size != transfer.size
            or not np.isfinite(wave).all() or not np.isfinite(transfer).all()):
        raise RuntimeError(f"ONA {name} is missing or contains invalid samples")
    power = np.abs(transfer) ** 2
    if not np.isfinite(power).all() or not np.ptp(power) > 0:
        raise RuntimeError(f"ONA {name} has no varying power response")
    logging.info("Validated ONA %s: %d points; wavelength %.9g..%.9g m; power %.9g..%.9g",
                 name, wave.size, wave.min(), wave.max(), power.min(), power.max())


def write_run_readme(run_dir: Path) -> None:
    content = """# 双微环冷态 Vernier 光谱

## `dual_ring_cold.icp`

### 工程打开后使用方法

用 Ansys Lumerical INTERCONNECT 打开本工程。电路为 `ONA → ring1 → ring2` 的级联双环：
`ring1` 的 Through 接 ONA `input 1`；`ring1` 的 Drop 进入 `ring2`；
`ring2` 的 Through 接 ONA `input 2`（Drop1）；`ring2` 的 Drop 接 ONA `input 3`（Drop2）。
ONA 的三个结果依次对应 Through、Drop1、Drop2。所有光谱在 Visualizer 的
`Scalar operation` 选 `Abs^2`，查看功率透射率，横轴选波长。

### 可以得到的结果（及截图）

| 截图名称 | 结果查找位置 | 校验重点 |
|---|---|---|
| `dual_ring_through.png` | `ONA → input 1 → mode 1 → transmission` | Through 谐振凹口、波长轴和功率值 |
| `dual_ring_drop1.png` | `ONA → input 2 → mode 1 → transmission` | 第一环输出经过第二环后的剩余谱 |
| `dual_ring_drop2.png` | `ONA → input 3 → mode 1 → transmission` | Vernier 共同谐振、主峰与旁峰 |
| `dual_ring_schematic.png` | 工程原理图 | 两环连接关系、三个输出端 |

截图请手动保存到本算例 `results/figures/` 下与本运行目录同名的文件夹。
`config/03_dual_ring_cold.json` 中的半径和损耗来自论文；耦合系数是待优化的初始输入。
本工程是 INTERCONNECT 电路模型，尚不含实际耦合间隙的 MODE/FDTD 提取结果、
加热调谐、光栅耦合器包络或 FBG 测量链路。
"""
    (run_dir / "README.md").write_text(content, encoding="utf-8")


def main() -> int:
    cfg = load_config()
    run_id = f"s02_dual_ring_cold_{datetime.now():%Y%m%d_%H%M%S_%f}"
    run_dir = RUNS / run_id
    log_dir = LOGS / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    print("| 项目 | 本轮设置 | 原生结果 |", flush=True)
    print("|---|---|---|", flush=True)
    print("| 双微环冷态光谱 | 论文 10/11 um 双环；其余输入见配置 | INTERCONNECT .icp |", flush=True)
    print(f"CONFIG={CONFIG}", flush=True)
    print(f"MODE_INPUT={MODE_PROJECT}", flush=True)
    print(f"RUN_ID={run_id}", flush=True)
    print(f"RUN_DIRECTORY={run_dir}", flush=True)
    if not API.is_dir():
        raise FileNotFoundError(f"Lumerical Python API not found: {API}")
    sys.path.insert(0, str(API))
    import lumapi

    neff, ng = load_fde_indices(lumapi)
    ic = None
    project = run_dir / "dual_ring_cold.icp"
    try:
        ic = lumapi.INTERCONNECT(hide=True)
        frequency = 299792458.0 / float(cfg["wavelength_center_m"])
        loss_db_per_m = float(cfg["waveguide_loss_db_per_cm"]) * 100.0
        couplings = [float(x) for x in cfg["coupling_power_ratios"]]
        for index, radius in enumerate(cfg["ring_radii_m"], start=1):
            add_ring(ic, f"ring{index}", float(radius), neff, ng,
                     frequency, loss_db_per_m, couplings)
        configure_ona(ic, cfg)
        logging.info("ring1 ports=%s; ring2 ports=%s; ONA ports=%s",
                     ic.getports("ring1"), ic.getports("ring2"), ic.getports("ONA"))
        ic.connect("ONA", "output", "ring1", "port 1")
        ic.connect("ring1", "port 3", "ONA", "input 1")
        ic.connect("ring1", "port 2", "ring2", "port 1")
        ic.connect("ring2", "port 3", "ONA", "input 2")
        ic.connect("ring2", "port 2", "ONA", "input 3")
        ic.run()
        for port in (1, 2, 3):
            validate_ona_spectrum(ic, port)
        ic.save(str(project))
        write_run_readme(run_dir)
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
        logging.exception("Dual-ring cold simulation failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
