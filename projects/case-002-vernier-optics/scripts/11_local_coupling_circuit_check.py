"""Compare the saved local MODE coupling results in the existing INTERCONNECT ring circuit."""
from __future__ import annotations

import json
import logging
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
CONFIG = CASE / "config" / "15_local_coupling_circuit.json"
API = Path(r"D:\Program Files\Lumerical\v242\api\python")


def within_case(relative: str) -> Path:
    path = (CASE / relative).resolve()
    if not path.is_relative_to(CASE.resolve()) or not path.is_file():
        raise FileNotFoundError(f"Input project unavailable within case: {relative}")
    return path


def extract_coupling(lumapi, project: Path, wavelength: float) -> tuple[float, float]:
    mode = lumapi.MODE(hide=True)
    try:
        mode.load(str(project))
        result = mode.getresult("ring_guided", "expansion for field")
        wave = np.asarray(result["lambda"], dtype=float).reshape(-1)
        forward = np.asarray(result["T_forward"]).reshape(-1)
        if (wave.size < 3 or wave.size != forward.size or
                not np.isfinite(wave).all() or not np.isfinite(forward).all()):
            raise RuntimeError(f"Incomplete native ring_guided spectrum: {project}")
        selected = int(np.argmin(np.abs(wave - wavelength)))
        spacing = float(np.min(np.diff(np.sort(wave))))
        if abs(float(wave[selected]) - wavelength) > spacing / 2:
            raise ValueError(f"Requested wavelength is not represented by a saved spectral point: {project}")
        value = float(np.real(forward[selected]))
        if not math.isfinite(value) or not 0 < value < 1:
            raise RuntimeError(f"Saved guided-mode power is outside its physical range: {project}")
        logging.info("MODE %s wavelength=%0.12g m; T_forward=%0.12g", project, wave[selected], value)
        return value, float(wave[selected])
    finally:
        mode.close()


def validate_ona(ic, label: str) -> None:
    for port in (1, 2, 3):
        result_name = f"input {port}/mode 1/transmission"
        result = ic.getresult("ONA", result_name)
        wave = np.asarray(result["wavelength"], dtype=float).reshape(-1)
        transfer = np.asarray(result["TE transmission"]).reshape(-1)
        if (wave.size < 3 or wave.size != transfer.size or
                not np.isfinite(wave).all() or not np.isfinite(transfer).all()):
            raise RuntimeError(f"Invalid ONA result: {label} {result_name}")
        logging.info("%s ONA port=%d samples=%d wavelength_min=%g m wavelength_max=%g m",
                     label, port, wave.size, np.min(wave), np.max(wave))


def write_readme(run_dir: Path, wave: float, ring1: float, ring2: float) -> None:
    content = f"""# s13 局部耦合系数接入双微环电路对照

## 算例做了什么

| 项目 | 内容 |
|---|---|
| 输入 | s05 已对齐双环电路；s12 两只环的 `ring_guided → T_forward` 原生结果；配置 `config/15_local_coupling_circuit.json`。 |
| 改动 | 在 {wave * 1e9:.3f} nm 的已保存谱点读取功率耦合：ring1 为 {ring1:.8f}，ring2 为 {ring2:.8f}；各环的第一、第二总线暂设为相同耦合值。其余电路参数沿用 s05。 |
| 目的 | 比较物理局部耦合估计与 s05 已保存的 Q 拟合耦合值对双环透射谱的影响。 |
| 范围 | 这是参数敏感度对照。s12 仅模拟一个局部耦合区；第二总线、完整环、掺杂、金属及热驱动未由本工程验证。 |

## 工程打开后使用方法

| 工程文件 | 操作 |
|---|---|
| `dual_ring_local_coupling_check.icp` | 用 INTERCONNECT 打开；点击 `ring1` 和 `ring2`，在 Property View 展开 Waveguide/Mode 1，查看 `coupling coefficient 1 1` 和 `coupling coefficient 1 2`；在 Result View 打开 `ONA → input 1/2/3 → mode 1 → transmission`。Visualizer 的 `Scalar operation` 选 `Abs^2`。 |

## 可以得到的结果（及截图）

| 结果 | 工程内入口 | 核验重点与建议截图 |
|---|---|---|
| Through（可选） | `ONA → input 1 → mode 1 → transmission` | 对比 s05 的 Through 谱；截图 `01_through.png`。 |
| Drop1（可选） | `ONA → input 2 → mode 1 → transmission` | 对比 s05 的第一环输出；截图 `02_drop1.png`。 |
| Drop2（必需） | `ONA → input 3 → mode 1 → transmission` | 对比 s05 的共同峰波长、峰高和线宽；截图 `03_drop2.png`。 |
| 电路参数（必需） | `ring1`、`ring2` 的两个功率耦合系数 | 截图 `04_parameters.png`，画面含工程标题与 Property View。 |

请将手动截图放入 `results/figures/{run_dir.name}/`。s05 基准仍在 `results/runs/s05_ring_q_aligned_20261107_105136_874630/dual_ring_static_aligned.icp`。原生输出为仿真数据，不是实测数据。不要把本轮当作已完成的 200 nm 间隙全器件校准。
"""
    (run_dir / "README.md").write_text(content, encoding="utf-8")


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    if cfg["assume_same_coupling_at_both_buses"] is not True:
        raise ValueError("This comparison requires an explicit same-coupling assumption")
    baseline = within_case(cfg["baseline_project"])
    ring_paths = {name: within_case(cfg["ring_mode_projects"][name]) for name in ("ring1", "ring2")}
    wavelength = float(cfg["coupling_wavelength_m"])
    if not math.isfinite(wavelength) or wavelength <= 0:
        raise ValueError("Invalid reference wavelength")
    name = str(cfg["output_project_name"])
    if Path(name).name != name or not name.endswith(".icp"):
        raise ValueError("Output project must be a local .icp filename")
    run_id = f"{cfg['run_prefix']}_{datetime.now():%Y%m%d_%H%M%S_%f}"
    run_dir = CASE / "results" / "runs" / run_id
    log_dir = CASE / "results" / "logs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    logging.info("Configuration=%s baseline=%s", CONFIG, baseline)
    if not API.is_dir():
        raise FileNotFoundError(API)
    sys.path.insert(0, str(API))
    import lumapi

    couplings = {}
    selected_waves = {}
    for ring in ("ring1", "ring2"):
        couplings[ring], selected_waves[ring] = extract_coupling(lumapi, ring_paths[ring], wavelength)
    if not np.isclose(selected_waves["ring1"], selected_waves["ring2"], rtol=0, atol=1e-12):
        raise RuntimeError("The two source MODE projects use different selected wavelengths")

    ic = lumapi.INTERCONNECT(hide=True)
    try:
        ic.load(str(baseline))
        validate_ona(ic, "baseline")
        for ring in ("ring1", "ring2"):
            for bus in (1, 2):
                key = f"coupling coefficient 1 {bus}"
                logging.info("Baseline %s %s=%s", ring, key, ic.getnamed(ring, key))
        if int(np.asarray(ic.designmode()).squeeze()) == 0:
            ic.switchtodesign()
        for ring in ("ring1", "ring2"):
            for bus in (1, 2):
                key = f"coupling coefficient 1 {bus}"
                ic.setnamed(ring, key, couplings[ring])
                actual = float(np.asarray(ic.getnamed(ring, key)).squeeze())
                if not math.isclose(actual, couplings[ring], rel_tol=1e-8, abs_tol=1e-12):
                    raise RuntimeError(f"INTERCONNECT did not accept {ring} {key}")
        ic.run()
        validate_ona(ic, "local_coupling")
        project = run_dir / name
        ic.save(str(project))
        if not project.is_file() or project.stat().st_size == 0:
            raise RuntimeError("Native INTERCONNECT project was not saved")
        write_readme(run_dir, selected_waves["ring1"], couplings["ring1"], couplings["ring2"])
        logging.info("Saved native project=%s", project)
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
        logging.exception("Local coupling circuit comparison failed")
        print(f"SIMULATION_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
