# 高压续算起始阶段

## `pip_fig23_stage_0to1p7.ldev`

### 算例做了什么

对论文图 2/图 3 所需的电热工程先计算 0～1.7 V、18 个阳极偏压点，作为后续小步长向高压续算的起点。当前工程只覆盖到 1.7 V，不代表图 2(a) 的 20 V 曲线完成。

### 工程打开后使用方法

在 DEVICE 打开本目录的 `pip_fig23_stage_0to1p7.ldev`，选 `CHARGE`；在 Result View 选择电流、功率或温度数据集，并在 Visualizer 检查 `V_anode` 和 `V_cathode=0 V`。保留本工程路径供后续接续计算引用。

### 可以得到的结果（及截图）

| 结果 | 工程内入口 | 核验重点 |
| --- | --- | --- |
| I–V | `CHARGE → anode → I` | 横轴只到 1.7 V |
| 功率、温度 | `CHARGE → integrated → Q`；`thermal → T/Q` | 检查扫描点及单位 |
| 载流子 | `CHARGE → charge → p` | 选择实际已保存的偏压点 |

本阶段无已核验的截图清单；若手动留图，放到同编号的 `results/figures/` 目录。
