# 脚本说明

## `06_scan_ring_index_tuning.py`：s09 单环密集微调配置

### 脚本用途

| 输入 | 功能 | 原生输出与校验 |
|---|---|---|
| `config/10_detuning_dense_scan.json`、`config/06_q_calibrated_alignment.json`、FDE 主模结果 | 只改变用于静态对齐的 `ring2` 有效折射率，扫描 11 个对齐比例，检查 Drop2 峰值功率对失配的敏感度 | `results/runs/s09_ring_detuning_dense_*/` 中 11 份 `.icp`；核验 ONA 三端口、附近峰值功率与波长。打开方法见该运行目录 README |

比例是光学电路探索输入，不是加热电压；脚本不制作图片或自制结果表格。

### 使用方法

在 `D:\SRTP_Work` 运行 `python '.\projects\case-002-vernier-optics\scripts\06_scan_ring_index_tuning.py' --config 10_detuning_dense_scan.json`。截图设置和结果入口见成功运行目录 README。

## `07_scan_common_mode_tuning.py`：s08 密集扫描配置

### 脚本用途

| 输入 | 功能 | 原生输出与校验 |
|---|---|---|
| `config/09_common_dense_scan.json`、`config/06_q_calibrated_alignment.json`、FDE 主模结果 | 在 s05 静态对齐基础上，对两环共同有效折射率给出 13 个递增偏置；检查 Drop2 峰是否逐步移动 | `results/runs/s08_ring_common_dense_*/` 内 13 份 `.icp`；每份核对 ONA 三端口、Drop2 峰位与功率。截图顺序和统一坐标见该运行目录 README |

配置偏置是探索输入，不是电压或实测温度；脚本不生成图片或自制结果表格。

### 使用方法

在 `D:\SRTP_Work` 运行 `python '.\projects\case-002-vernier-optics\scripts\07_scan_common_mode_tuning.py' --config 09_common_dense_scan.json`。打开工程与截图方法见成功运行目录 README。

## `07_scan_common_mode_tuning.py`

### 脚本用途

| 输入 | 功能 | 原生输出与校验 |
|---|---|---|
| `config/08_common_mode_tuning.json`、`config/06_q_calibrated_alignment.json`、波导 FDE 工程 | 在静态对齐后协同增加两环有效折射率，检查 Drop2 通带移动 | `results/runs/s07_ring_common_tuning_*/` 内三份 `.icp`；核验 `ONA` 的 Through、Drop1、Drop2、主峰位置和功率，具体见运行目录 README |

配置中的折射率增量是探索输入，不是已标定的电压或温度。脚本只保存原生工程和日志。

### 使用方法

在 `D:\SRTP_Work` 运行 `python '.\projects\case-002-vernier-optics\scripts\07_scan_common_mode_tuning.py'`。查看结果和截图清单见对应运行目录 README。

## `06_scan_ring_index_tuning.py`

### 脚本用途

| 输入 | 功能 | 原生输出与校验 |
|---|---|---|
| `config/07_index_tuning_scan.json`、`config/06_q_calibrated_alignment.json`、波导 FDE 工程 | 只改变被静态对齐的一个环，检查 Drop2 对失配的敏感度 | `results/runs/s06_ring_index_tuning_*/` 内三份 `.icp`；核验三个 ONA 端口、峰位和峰值功率，具体见运行目录 README |

此脚本检验对齐敏感度，不建立电压、温度或波长标定关系。

### 使用方法

在 `D:\SRTP_Work` 运行 `python '.\projects\case-002-vernier-optics\scripts\06_scan_ring_index_tuning.py'`。查看结果和截图清单见对应运行目录 README。

## `05_calibrate_ring_coupling.py`

### 脚本用途

| 输入 | 功能 | 输出 |
|---|---|---|
| `config/03_dual_ring_cold.json`、`config/05_ring_coupling_q.json`、波导 FDE 工程 | 对配置中的功率耦合系数逐个运行第一环 Through 光谱，按半深度线宽计算加载 Q，选择最接近论文报告值的候选值，再运行双环冷态电路 | `results/runs/s04_ring_q_fit_*/dual_ring_q_calibrated.icp` 和对应日志 |

论文参考加载 Q、消光比与候选耦合系数都放在配置文件，脚本不预设仿真结果。当前只用 Q 选参；消光比单独记录和核验。脚本不生成图片或自制结果表格。

### 使用方法

在 `D:\SRTP_Work` 运行：

```powershell
python '.\projects\case-002-vernier-optics\scripts\05_calibrate_ring_coupling.py'
```

终端显示原生工程路径和 `SIM_DONE_STATUS`。打开工程、查看结果和截图名称见对应成功运行目录的 `README.md`。

## `04_dual_ring_static_alignment.py`

### 脚本用途

| 输入 | 功能 | 输出 |
|---|---|---|
| `config/03_dual_ring_cold.json`、`config/04_dual_ring_alignment.json`、已求解的波导 FDE 工程 | 分别计算两环冷态共振，选取 1550 nm 附近的峰；只提高波长较短那一环的静态有效折射率，使两个峰重合 | `results/runs/s03_dual_ring_align_*/dual_ring_static_aligned.icp` 和对应日志 |

这一步只检查光学共同峰能否对齐，不使用尚未核验的 s20 电热结果，也不把折射率偏置换算成电压或功率。

### 使用方法

在 `D:\SRTP_Work` 运行：

```powershell
python '.\projects\case-002-vernier-optics\scripts\04_dual_ring_static_alignment.py'
```

终端输出 `SIM_DONE_STATUS=0` 表示脚本完成且共同峰通过谱点对齐检查。打开工程和截图清单见对应成功运行目录的 `README.md`。

将上一轮 Q 校准的 0.055 耦合参数与静态对齐合并时，使用另一份配置：

```powershell
python '.\projects\case-002-vernier-optics\scripts\04_dual_ring_static_alignment.py' --config 06_q_calibrated_alignment.json
```

该配置产生 `s05_ring_q_aligned_*` 原生工程；仍只验证光学峰对齐，不代表电热驱动已经验证。

## `03_dual_ring_cold.py`

### 脚本用途

| 输入 | 功能 | 输出 |
|---|---|---|
| `config/03_dual_ring_cold.json`；已求解的 `mzi_waveguide_mode.lms` | 建立论文 10/11 µm 双微环的冷态级联电路，扫描 1520–1600 nm，核验 Through、Drop1、Drop2 三个 ONA 原生光谱 | `results/runs/s02_dual_ring_cold_*/dual_ring_cold.icp` 和对应 `results/logs/` |

半径来自论文；3.5 dB/cm 是论文所报 3–4 dB/cm 区间的中值；两个 0.04 功率耦合系数仅用于首次电路探索，尚未根据 200 nm 间隙提取。脚本不生成图片或自制结果表格。

### 使用方法

在 `D:\SRTP_Work` 运行：

```powershell
python '.\projects\case-002-vernier-optics\scripts\03_dual_ring_cold.py'
```

终端显示运行路径和 `SIM_DONE_STATUS`；`0` 表示脚本完成并检查到三个有效原生光谱。具体打开哪个工程、每张图在哪里查看和截图清单，见成功运行目录内的 `README.md`。

## `01_build_mode_cross_section.py`

### 脚本用途

根据 `config/01_cold.json` 建立硅波导横截面并用 MODE FDE 求解导模。也作为 MZI 主脚本调用的几何构建模块。

### 使用方法

独立运行：

```powershell
python '.\projects\case-002-vernier-optics\scripts\01_build_mode_cross_section.py' --config 01_cold.json
```

查看该脚本生成的 `.lms` 工程，在 MODE 的 Objects Tree 选择 `FDE` 中的模态结果；求解日志位于对应 `results/logs/` 子目录。终端仅给出状态和文件路径。

## `02_build_mzi_ruler.py`

### 脚本用途

读取 `config/01_cold.json` 的硅波导截面，计算 1.55 µm 附近的有效折射率和群折射率；再用 INTERCONNECT 建立两种臂长差的独立 MZI 标尺，并核验 ONA 透射谱与自动峰值间距（FSR）数据。

### 使用方法

从 `D:\SRTP_Work` 运行：

```powershell
python '.\projects\case-002-vernier-optics\scripts\02_build_mzi_ruler.py'
```

参数来自 `config/02_mzi_ruler.json`。50 µm 和 100 µm 是初步对比用的臂长差，参考 [Ansys MZI/FSR 示例](https://optics.ansys.com/hc/en-us/articles/360042414214-Interferometer-Siemens-EDA-Interoperability)，不代表已确定的芯片版图尺寸。脚本只保存 MODE/INTERCONNECT 原生工程和运行日志，不生成结果图片或表格。成功工程的打开方法和透射谱、FSR 结果查找位置见 `results/runs/` 下对应工程 README。
