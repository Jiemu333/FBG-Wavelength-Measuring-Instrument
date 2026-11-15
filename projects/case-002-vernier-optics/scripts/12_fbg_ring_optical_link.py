"""Connect an illustrative Bragg-grating element to the saved ring circuit."""
from __future__ import annotations

import json
import logging
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
CONFIG = CASE / "config" / "16_fbg_ring_link.json"
API = Path(r"D:\Program Files\Lumerical\v242\api\python")


def project_within_case(relative: str) -> Path:
    path = (CASE / relative).resolve()
    if not path.is_relative_to(CASE.resolve()) or not path.is_file():
        raise FileNotFoundError(f"Saved input project is unavailable: {relative}")
    return path


def spectrum(ic, port: int) -> tuple[np.ndarray, np.ndarray]:
    result = ic.getresult("ONA", f"input {port}/mode 1/transmission")
    wave = np.asarray(result["wavelength"], dtype=float).reshape(-1)
    transfer = np.asarray(result["TE transmission"]).reshape(-1)
    if wave.size < 3 or wave.size != transfer.size or not np.isfinite(wave).all() or not np.isfinite(transfer).all():
        raise RuntimeError(f"ONA input {port} has no valid native spectrum")
    power = np.abs(transfer) ** 2
    if not np.isfinite(power).all():
        raise RuntimeError(f"ONA input {port} contains invalid power")
    return wave, power


def native_peak_near_reference(ic, reference: float) -> float:
    wave, power = spectrum(ic, 3)
    maxima = np.flatnonzero((power[1:-1] > power[:-2]) & (power[1:-1] >= power[2:])) + 1
    if maxima.size == 0:
        raise RuntimeError("Saved Drop2 spectrum has no interior peak")
    index = maxima[np.argmin(np.abs(wave[maxima] - reference))]
    logging.info("Saved Drop2 peak nearest %.12g m is %.12g m", reference, wave[index])
    return float(wave[index])


def validate_config(cfg: dict) -> None:
    if cfg["fbg_center"] != "nearest_saved_drop2_peak_to_reference":
        raise ValueError("FBG center selection is unsupported")
    for key in ("reference_wavelength_m", "fbg_length_m", "fbg_effective_index",
                "fbg_group_index", "fbg_effective_index_change_ac"):
        value = float(cfg[key])
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{key} must be positive and finite")
    if float(cfg["fbg_effective_index_change_dc"]) < 0:
        raise ValueError("FBG DC index change must be nonnegative")
    name = cfg["output_project_name"]
    if Path(name).name != name or not name.endswith(".icp"):
        raise ValueError("Output project must be a local .icp name")


def write_readme(run_dir: Path, baseline: Path, center: float, cfg: dict) -> None:
    content = f"""# s14 示范 Bragg 光栅反射与双微环光路

## fbg_reflection_dual_ring.icp

### 算例做了什么

从已保存的 [s13 双环工程](../s13_local_coupling_circuit_20261115_205936_021858/README.md)读取双环和 ONA 配置，保留原有双环、耦合系数及扫描范围。在 ONA 与 ring1 之间接入环形器和 Bragg 光栅：`ONA output → CIR port 1 → CIR port 2 → FBG port 1`；FBG 反射经 `CIR port 3` 进入 ring1，同时接入 ONA input 4；原有三个双环观察端保持为 ONA input 1/2/3。FBG 中心设置为原工程 Drop2 在 1550 nm 参考点附近的已保存主峰，即 {center * 1e9:.6f} nm。

原理图里名为 `FBG` 的对象，是我添加的 Ansys INTERCONNECT 内置 `Bragg Grating` 元件，并非已有的光纤光栅器件或实测数据。其长度 {cfg['fbg_length_m']} m、有效/群折射率 {cfg['fbg_effective_index']}/{cfg['fbg_group_index']} 和交流折射率调制 {cfg['fbg_effective_index_change_ac']} 均为示范输入；中心由已有双环峰指定。本算例只验证纯光学连接，不能据此宣称完成实际 FBG 建模；探测器、控制器与电热调谐尚未接入。

### 工程打开后使用方法

用 Ansys Lumerical INTERCONNECT 打开 `fbg_reflection_dual_ring.icp`。在原理图选中 `ONA`，到左侧 Result View 展开 `input 4 → mode 1 → transmission` 看 FBG 返回到环形器第 3 端口的反射谱；展开 `input 3 → mode 1 → transmission` 看经过双环 Drop2 的谱。Visualizer 横轴选 wavelength，`Scalar operation` 选 `Abs^2`，得到功率透射率。可同样查看 input 1/2 的 Through/Drop1。

### 可以得到的结果（及截图）

| 工程内结果 | 观察重点 | 用户截图建议 |
|---|---|---|
| `ONA → input 4 → mode 1 → transmission` | FBG 反射带中心、带宽、波长范围 | `01_fbg_reflection.png` |
| `ONA → input 3 → mode 1 → transmission` | 反射谱通过双环后的 Drop2 主峰与旁峰 | `02_fbg_filtered_drop2.png` |
| `ONA → input 1/2 → mode 1 → transmission` | 双环其他端口谱 | `03_through_drop1.png`（可选） |
| 原理图、FBG/CIR Property View | 连接关系与输入参数 | `04_schematic_parameters.png` |

用户截图目录：`results/figures/{run_dir.name}/`。所有谱为仿真数据；将来接入真实 FBG 时应以器件参数或实测 S 参数替换这里的示范光栅。
"""
    (run_dir / "README.md").write_text(content, encoding="utf-8")


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    validate_config(cfg)
    baseline = project_within_case(cfg["baseline_project"])
    run_id = f"{cfg['run_prefix']}_{datetime.now():%Y%m%d_%H%M%S}"
    run_dir = CASE / "results" / "runs" / run_id
    log_dir = CASE / "results" / "logs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    if not API.is_dir():
        raise FileNotFoundError(API)
    sys.path.insert(0, str(API))
    import lumapi

    ic = lumapi.INTERCONNECT(hide=True)
    try:
        ic.load(str(baseline))
        center = native_peak_near_reference(ic, float(cfg["reference_wavelength_m"]))
        ic.switchtodesign()
        ic.disconnect("ONA", "output", "ring1", "port 1")
        ic.setnamed("ONA", "number of input ports", 4)

        ic.addelement("Optical Circulator")
        ic.set("name", "CIR")
        ic.addelement("Bragg Grating")
        ic.set("name", "FBG")
        ic.set("length", float(cfg["fbg_length_m"]))
        ic.set("input parameter", "Bragg frequency")
        ic.set("frequency", 299792458.0 / center)
        ic.set("coupling parameter", "effective index change")
        ic.set("effective index change ac", float(cfg["fbg_effective_index_change_ac"]))
        ic.set("effective index change dc", float(cfg["fbg_effective_index_change_dc"]))
        # With Bragg frequency selected, INTERCONNECT derives the period and
        # disables direct editing of this index. Check its documented default.
        actual_neff = float(np.asarray(ic.getnamed("FBG", "effective index 1")).squeeze())
        if not math.isclose(actual_neff, float(cfg["fbg_effective_index"]), rel_tol=0, abs_tol=1e-9):
            raise RuntimeError("The saved FBG effective index differs from configuration")
        ic.set("group index 1", float(cfg["fbg_group_index"]))

        for connection in (("ONA", "output", "CIR", "port 1"),
                           ("CIR", "port 2", "FBG", "port 1"),
                           ("CIR", "port 3", "ring1", "port 1"),
                           ("CIR", "port 3", "ONA", "input 4")):
            ic.connect(*connection)
        ic.run()
        for port in (1, 2, 3, 4):
            wave, power = spectrum(ic, port)
            if not np.ptp(power) > 0:
                raise RuntimeError(f"ONA input {port} has a flat spectrum")
            logging.info("ONA input %d: %d samples, %.9g..%.9g m, power %.9g..%.9g",
                         port, wave.size, wave.min(), wave.max(), power.min(), power.max())
        project = run_dir / cfg["output_project_name"]
        ic.save(str(project))
        if not project.is_file() or project.stat().st_size == 0:
            raise RuntimeError("Native project was not saved")
        write_readme(run_dir, baseline, center, cfg)
        print(f"OPEN_IN_INTERCONNECT={project}", flush=True)
        print(f"LOG_DIRECTORY={log_dir}", flush=True)
        print(f"SCREENSHOT_DIRECTORY={CASE / 'results' / 'figures' / run_id}", flush=True)
        return 0
    finally:
        ic.close()


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        logging.exception("FBG and double-ring optical link failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
