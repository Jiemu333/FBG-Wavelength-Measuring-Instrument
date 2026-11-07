# 已完成工程：打开与查结果

在 **Ansys Lumerical DEVICE → File → Open** 打开下面各工程的 `.ldev`。这些文件保存了原生仿真结果；查看已有结果无需重新点击 Simulation。隐藏的时间戳目录是工程内部引用使用的 Windows Junction 兼容路径，日常从下文的 `sNN_...` 目录打开工程。`models/` 中的输入工程用途见 [`../../models/README.md`](../../models/README.md)。

## s01_baseline_20261101_101141/heater_charge_0to1V.ldev

CHARGE，0～1 V，11 个偏压点。作为 0～1 V 结果参照。

### 工程打开后使用方法

在 DEVICE 中打开 [`s01_baseline_20261101_101141/heater_charge_0to1V.ldev`](s01_baseline_20261101_101141/heater_charge_0to1V.ldev)。在 **Objects Tree** 选对象，**Result View** 双击数据集；Visualizer 下方 **Attributes** 选物理量，**Parameters** 选 `V_anode`（`V_cathode` 保持 0 V）。

### 可以得到的结果

| 结果 | 入口 | 查看 |
| --- | --- | --- |
| 阳极电流 I–V | `CHARGE → anode` | Attribute 选 `I`，Line / xy，横轴 `V_anode`。不要把 `Vs`、`Vc` 误当电流 |
| 总发热功率 | `CHARGE → integrated` | Attribute 选 `Q`，Line / xy，横轴 `V_anode` |
| 温度空间分布 | `CHARGE → temperature_monitor → temperature` | Attribute 选 `T`，Image / xz，选 0 V 或 1 V，保留色标读数 |

已有截图：[`../figures/20261101_101141_668681`](../figures/20261101_101141_668681)。对应求解日志：`results/logs/20261101_101141_668681/`。

## s02_mesh_compare_20261102_090510/charge_mesh_medium.ldev

CHARGE，0～1 V，11 个偏压点，中等网格。

### 工程打开后使用方法

在 DEVICE 中打开 [`s02_mesh_compare_20261102_090510/charge_mesh_medium.ldev`](s02_mesh_compare_20261102_090510/charge_mesh_medium.ldev)。查看方法同 s01；可与 s03 的同偏压数据比较网格影响。

### 可以得到的结果

I–V、发热功率 Q、温度 T（入口同 s01 表格）。已有截图：[`../figures/20261102_090510_512039`](../figures/20261102_090510_512039)。日志：`results/logs/20261102_090510_512039/`。

## s03_mesh_cap60k_20261102_100139/charge_mesh_cap60k.ldev

CHARGE，0～1 V，11 个偏压点，自动网格细化上限 60000。

### 工程打开后使用方法

在 DEVICE 中打开 [`s03_mesh_cap60k_20261102_100139/charge_mesh_cap60k.ldev`](s03_mesh_cap60k_20261102_100139/charge_mesh_cap60k.ldev)。查看方法同 s01；与 s02 对照看网格影响。也是脚本 12 的输入工程。

### 可以得到的结果

I–V、Q、T（入口同 s01 表格）。已有截图：[`../figures/20261102_100139_948571`](../figures/20261102_100139_948571)。日志：`results/logs/20261102_100139_948571/`。

## s05_continue2p1_20261102_190815/charge_continue_2p1.ldev

CHARGE，续算至 2.1 V。

### 工程打开后使用方法

在 DEVICE 中打开 [`s05_continue2p1_20261102_190815/charge_continue_2p1.ldev`](s05_continue2p1_20261102_190815/charge_continue_2p1.ldev)。查看文件内已保存的 2.1 V 结果。注意：其原续算输入路径已不在当前目录中，不要直接把本文件当成可重跑的续算配置。

### 可以得到的结果

2.1 V 处的 I、Q、T 和载流子分布。暂无截图；需要留证时手动保存至 `results/figures/20261102_190815_641493/`。日志：`results/logs/20261102_190815_641493/`。

## s12_fig2_0to1_20261105_145819_844533/pip_fig2_0to1.ldev

CHARGE，0～1 V，含论文图 2(b–e) 所需的局部电场、能带和空穴截线监视器。

### 工程打开后使用方法

在 DEVICE 中打开 [`s12_fig2_0to1_20261105_145819_844533/pip_fig2_0to1.ldev`](s12_fig2_0to1_20261105_145819_844533/pip_fig2_0to1.ldev)。首次打开时核对 `paper_bandline`/`paper_holeline` 截线确实穿过硅 slab（z=0.03 µm 应为 60 nm slab 的中部）。查看方法同 s01，`V_anode` 在 0 V 与 1 V 之间切换。

### 可以得到的结果

| 论文图 | 入口 | 查看 |
| --- | --- | --- |
| 图 2(b)(c) 0/1 V 局部电场 | `CHARGE → paper_E_xz` | E 的 **Magnitude**，Image / xz；0 V、1 V 各一张；放大 z≈0～0.22 µm 的硅 slab 与两侧结区；**两张图都要点开色标、把上下限手动固定为 0～1.2×10⁶ V/m**——自动色标会被 p++ 顶角约 7.9×10⁷ V/m 的尖峰拉满、主体全蓝；设 3×10⁶ 也会盖住变化（0→1 V 的变化全部发生在 1.2×10⁶ 以下）。固定后结区亮带饱和成亮块属正常；1 V 时右侧从波导边缘到右结整片变亮、左侧偏暗，即论文所述"higher electric field at the right i-p junction" |
| 图 2(d)(e) 0/1 V 能带 | `CHARGE → paper_bandline` | 同一图显示 `Ec、Ev、Efn、Efp`，Line / xy，横轴 x；0 V、1 V 各一张 |
| slab 空穴截线（图 3(c) 的 0 V 基准） | `CHARGE → paper_holeline → charge → p` | Line / xy，横轴 x；单位核对为 cm⁻³ |

截图保存到 [`../figures/s12_fig2_0to1_20261105_145819_844533/`](../figures/s12_fig2_0to1_20261105_145819_844533/)，每张须显示曲线或云图、Attributes、Parameters、坐标和色标：`fig2b_E_0V.png` / `fig2c_E_1V.png`（局部电场，0/1 V，同一截面及可比色标）；`fig2d_bands_0V.png` / `fig2e_bands_1V.png`（`paper_bandline` 上的 `Ec、Ev、Efn、Efp` 一维曲线）。

日志：`results/logs/s12_fig2_0to1_20261105_145819_844533/`。

## 高压续算链（进行中）：s18 0～1.7 V → 小步长续算 → 最终 0～20 V 工程

### 工程打开后使用方法

在 DEVICE 中打开 [`s18_fig23_stage_0to1p7_20261105_192615/pip_fig23_stage_0to1p7.ldev`](s18_fig23_stage_0to1p7_20261105_192615/pip_fig23_stage_0to1p7.ldev)（CHARGE，0～1.7 V，18 个偏压点），查看方法同 s01。它同时是续算脚本 `--plan fig23_cont` 的输入（`continuation_from`），**不要移动、改名或重新求解**。续算链完成后，本节会替换为最终 0～20 V 工程的路径与查看方法。

### 可以得到的结果

s18 现在可得：0～1.7 V 的 I–V、Q、T 和载流子分布。日志：`results/logs/s17_fig23_0to20_20261105_192615_907096/`。

链完成后的截图清单（保存到脚本终端输出的 `SCREENSHOT_DIRECTORY`，每张须显示 Attributes、Parameters、坐标和色标）：`fig2a_IV_0to20V.png`（图 2(a) I–V，横轴实际到 20 V）、`fig3a_Q_10V.png`（图 3(a) 发热密度，色标 W/m³）、`fig3b_p_10V.png`（图 3(b) 空穴分布）、`fig3c_p_line_0_10V.png`（图 3(c) 0 V 与 10 V 的 `p` 截线）、`fig3d_T_0_10V.png`（图 3(d) 0 V 与 10 V 温度读数）。

图 3(e)（有效折射率和附加损耗）尚需另行建立 MODE 光学工程，本工程不提供。
