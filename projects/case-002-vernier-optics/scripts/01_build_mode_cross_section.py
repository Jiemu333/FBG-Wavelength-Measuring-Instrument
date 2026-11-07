"""按配置新建 MODE 截面模式工程：微环波导冷态截面 TE0 模式基准。

几何来自论文图 1 插图（0.45 um x 220 nm 波导 + 60 nm slab + 2 um BOX），
参数全部来自 config/01_cold.json，不在脚本中硬编码参考值。
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[1]
RUNS = CASE / "results" / "runs"
LOGS = CASE / "results" / "logs"
API = Path(r"D:\Program Files\Lumerical\v242\api\python")


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    wave = float(data["wavelength_m"])
    if not 1e-9 <= wave <= 1e-5:
        raise ValueError("wavelength_m must be in [1e-9, 1e-5]")
    geo = data["geometry"]
    for key in ("waveguide_width_m", "waveguide_height_m", "slab_thickness_m",
                "slab_half_width_m", "box_thickness_m", "air_thickness_m"):
        if float(geo[key]) <= 0:
            raise ValueError(f"geometry.{key} must be positive")
    fde = data["fde"]
    if fde["z_min_m"] >= fde["z_max_m"]:
        raise ValueError("fde.z_min_m must be below fde.z_max_m")
    mesh = data["mesh"]
    if mesh["z_min_m"] >= mesh["z_max_m"]:
        raise ValueError("mesh.z_min_m must be below mesh.z_max_m")
    return data


def build(m, cfg: dict) -> None:
    g = cfg["geometry"]
    mat = cfg["materials"]

    m.addrect()
    m.set("name", "box")
    m.set("material", mat["oxide"])
    m.set("x", 0.0)
    m.set("x span", 2 * g["slab_half_width_m"])
    m.set("y", 0.0)
    m.set("y span", 0.5e-6)
    m.set("z", -g["box_thickness_m"] / 2)
    m.set("z span", g["box_thickness_m"])

    m.addrect()
    m.set("name", "slab")
    m.set("material", mat["silicon"])
    m.set("x", 0.0)
    m.set("x span", 2 * g["slab_half_width_m"])
    m.set("y", 0.0)
    m.set("y span", 0.5e-6)
    m.set("z", g["slab_thickness_m"] / 2)
    m.set("z span", g["slab_thickness_m"])

    m.addrect()
    m.set("name", "waveguide")
    m.set("material", mat["silicon"])
    m.set("x", 0.0)
    m.set("x span", g["waveguide_width_m"])
    m.set("y", 0.0)
    m.set("y span", 0.5e-6)
    m.set("z", g["slab_thickness_m"] + (g["waveguide_height_m"] - g["slab_thickness_m"]) / 2)
    m.set("z span", g["waveguide_height_m"] - g["slab_thickness_m"])

    fde = cfg["fde"]
    m.addfde()
    m.set("solver type", "2D Y normal")
    m.set("wavelength", cfg["wavelength_m"])
    m.set("number of trial modes", int(fde["trial_modes"]))
    m.set("x", 0.0)
    m.set("x span", fde["x_span_m"])
    m.set("z", (fde["z_min_m"] + fde["z_max_m"]) / 2)
    m.set("z span", fde["z_max_m"] - fde["z_min_m"])

    mesh = cfg["mesh"]
    m.addmesh()
    m.set("name", "core_mesh")
    m.set("dx", mesh["dx_m"])
    m.set("dy", 0.05e-6)
    m.set("dz", mesh["dz_m"])
    m.set("x", 0.0)
    m.set("x span", 2 * mesh["x_half_span_m"])
    m.set("y", 0.0)
    m.set("y span", 0.5e-6)
    m.set("z", (mesh["z_min_m"] + mesh["z_max_m"]) / 2)
    m.set("z span", mesh["z_max_m"] - mesh["z_min_m"])


def mode_neff(m, index: int):
    for pattern in (f"FDE::data::mode{index}", f"FDE::mode{index}"):
        try:
            return m.getresult(pattern, "neff")
        except Exception:
            continue
    raise RuntimeError(f"Mode result for mode {index} was not found")


def select_te0(m, max_modes: int) -> tuple[int, complex, float]:
    best = None
    for i in range(1, max_modes + 1):
        try:
            neff = complex(mode_neff(m, i))
        except Exception:
            continue
        frac = 1.0
        try:
            for pattern in (f"FDE::data::mode{i}", f"FDE::mode{i}"):
                try:
                    e = np.asarray(m.getresult(pattern, "E"), dtype=float)
                    break
                except Exception:
                    continue
            e = np.squeeze(e)
            if e.ndim >= 2 and e.shape[-1] == 3:
                ex, ez = np.sum(e[..., 0] ** 2), np.sum(e[..., 2] ** 2)
                total = ex + ez
                if total > 0:
                    frac = ex / total
        except Exception:
            pass
        if best is None or neff.real > best[1].real:
            best = (i, neff, frac)
    if best is None or not np.isfinite(best[1].real):
        raise RuntimeError("No finite guided mode was found by the FDE solver")
    return best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config_path = (CASE / "config" / args.config).resolve()
    if not config_path.is_relative_to(CASE.resolve()) or not config_path.is_file():
        raise FileNotFoundError("Config file is unavailable or outside the case")
    cfg = load_config(config_path)
    run_id = f"s01_mode_cold_{datetime.now():%Y%m%d_%H%M%S_%f}"
    run_dir = RUNS / run_id
    log_dir = LOGS / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    log_dir.mkdir(parents=True, exist_ok=False)
    logging.basicConfig(filename=log_dir / "driver.log", filemode="w",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    project = run_dir / "mode_cold.lms"
    mode = None
    try:
        if not API.is_dir():
            raise FileNotFoundError("Lumerical Python API not found")
        sys.path.insert(0, str(API))
        import lumapi
        mode = lumapi.MODE(hide=True)
        build(mode, cfg)
        print("| Task | Solver | Native output |", flush=True)
        print("|---|---|---|", flush=True)
        print("| Cold waveguide cross-section | MODE FDE, 2D Y-normal | .lms project and log |", flush=True)
        print(f"CONFIG={config_path}", flush=True)
        print(f"RUN_ID={run_id}", flush=True)
        print(f"PROJECT={project}", flush=True)
        print("RUNNING_MODE=1", flush=True)
        mode.findmodes()
        index, neff, te_fraction = select_te0(mode, int(cfg["fde"]["trial_modes"]))
        mode.save(str(project))
        logging.info("Selected mode %s: neff=%s; Ex power fraction=%.3f",
                     index, neff, te_fraction)
        print(f"OPEN_IN_MODE={project}", flush=True)
        print(f"LOG_DIRECTORY={log_dir}", flush=True)
        return 0
    except Exception:
        logging.exception("MODE cold baseline did not meet the requested completion criteria")
        print(f"CHECK_LOG={log_dir / 'driver.log'}", file=sys.stderr, flush=True)
        return 1
    finally:
        if mode is not None:
            try:
                mode.close()
            except Exception:
                logging.exception("Could not close MODE")
        for path in run_dir.glob("*.log"):
            try:
                import shutil
                shutil.move(str(path), str(log_dir / path.name))
            except Exception:
                logging.exception("Could not move solver log")


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as exc:
        print(f"SETUP_ERROR={type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        status = 1
    print(f"SIM_DONE_STATUS={status}", flush=True)
    raise SystemExit(status)
