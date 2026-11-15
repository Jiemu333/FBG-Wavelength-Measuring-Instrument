# 脚本说明

## `11_local_coupling_circuit_check.py`：s13 局部耦合接入电路对照

| 输入工程与配置 | 脚本功能 | 运行与原生输出 | 校验点 |
|---|---|---|---|
| `config/15_local_coupling_circuit.json`；s12 的两只 MODE 环局部耦合工程；s05 已对齐双环 INTERCONNECT 工程 | 在约 1550 nm 的已保存谱点读取 `ring_guided → T_forward`，替换 s05 两只环的功率耦合参数，保留其他电路设置后重新求解 | 在 `D:\SRTP_Work` 运行 `python '.\projects\case-002-vernier-optics\scripts\11_local_coupling_circuit_check.py'`；新 `.icp` 在 `results/runs/s13_local_coupling_circuit_*/`，日志在同名 `results/logs/` | 校验原生波长、耦合参数写入值，以及 ONA 三个输出均有有限光谱；在运行目录 README 查看工程和截图入口 |

这是局部耦合参数的电路敏感度对照。配置明确假设每只环的两个总线耦合区相同；现有 s12 只直接模拟了其中一个局部耦合区，因此本轮不证明完整器件已完成物理校准。终端仅输出状态和路径，不生成图片或自制结果表格。

## `10_bus_ring_coupler_varfdtd.py`：s11/s12 局部电磁耦合

| 输入与参数来源 | 脚本功能 | 原生输出与校验 |
|---|---|---|
| `config/13_bus_ring_coupler_varfdtd.json` 或继承它的 `config/14_bus_ring_coupler_varfdtd_refined.json`；几何来自 `config/11_ring_physical.json` | 用 MODE varFDTD 建直波导、200 nm 间隙和 10/11 μm 弯曲环；先跑无环对照，再跑两只环；监测总通量、电场、有效折射率和导模功率 | 每次独立保存 3 个 `.lms` 于 `results/runs/`，日志在 `results/logs/`；校验 11 个谱点、有限值、无环基准、功率传输和粗细网格差异。打开工程与截图位置见成功运行目录 README |

在 `D:\SRTP_Work` 执行粗网格：`python '.\projects\case-002-vernier-optics\scripts\10_bus_ring_coupler_varfdtd.py'`。细网格执行：`python '.\projects\case-002-vernier-optics\scripts\10_bus_ring_coupler_varfdtd.py' --config 14_bus_ring_coupler_varfdtd_refined.json`。终端只显示状态和路径，结果在 `.lms` 工程内。当前细网格原生结果见 [s12 工程说明](../results/runs/s12_bus_ring_coupler_refined_20261114_205032/README.md)。

本轮使用窄带等效折射率，适用于 1545–1555 nm 的首轮局部检查；它不等于完整 1520–1600 nm 的宽带校准，也不能替代 3D FDTD 或最终掺杂与金属布局的验证。

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
## `08_ring_physical_mode.py`

| 输入 | 功能 | 原生输出 | 核验 |
|---|---|---|---|
| `config/11_ring_physical.json`；文献给出的环半径、截面和 200 nm 间隙 | 建立两环三总线 MODE 几何；对同截面直波导及 10/11 µm 弯曲波导分别求 FDE 主模 | `results/runs/s10_ring_physical_*/` 内 4 个 `.lms`；日志在对应 `results/logs/` | 检查脚本状态、四个工程文件、三项 Mode 1 结果；几何间隙和场分布待用户截图复核 |

从 `D:\SRTP_Work` 运行 `python '.\projects\case-002-vernier-optics\scripts\08_ring_physical_mode.py'`。本脚本只保存原生工程与日志，不生成图片或结果表格。工程分别如何打开、查看哪些结果及截图存放处，见 [s10 工程说明](../results/runs/s10_ring_physical_20261114_192733/README.md)。

## `12_fbg_ring_optical_link.py`

| 输入工程 | 配置 | 功能 | 原生输出与校验 |
|---|---|---|---|
| s13 双环 `.icp` | `config/16_fbg_ring_link.json` | 在双环前接入环形器与软件内置 Bragg 光栅，同时保留反射谱观察端 | `results/runs/s14_fbg_ring_link_*/fbg_reflection_dual_ring.icp`；核验 ONA 四个端口的原生频谱；日志在 `results/logs/` |

从 `D:\SRTP_Work` 运行 `python '.\projects\case-002-vernier-optics\scripts\12_fbg_ring_optical_link.py'`。原理图中名为 `FBG` 的对象只是 Ansys 元件的示范模型，并非项目已有的真实 FBG；中心取 s13 已保存的 1550 nm 附近 Drop2 峰，仅用于纯光学链路测试。工程查看入口与截图清单见成功运行目录 README。
