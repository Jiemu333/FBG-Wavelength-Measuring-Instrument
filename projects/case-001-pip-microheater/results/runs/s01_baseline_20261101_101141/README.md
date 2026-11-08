# 0～1 V 基线工程

## `heater_charge_0to1V.ldev`

### 算例做了什么

以微加热器截面为对象，完成 CHARGE 的 0～1 V、11 个偏压点计算，作为后续网格比较及续算的电学和温度基线。

### 工程打开后使用方法

在 DEVICE 打开本目录的 `heater_charge_0to1V.ldev`，选 `CHARGE`；在 Result View 双击对应数据集，在 Visualizer 的 Parameters 选择 `V_anode`，保持 `V_cathode=0 V`。

### 可以得到的结果（及截图）

| 结果 | 工程内入口 | 核验重点 |
| --- | --- | --- |
| I–V | `CHARGE → anode → I` | 横轴为 0～1 V 的 `V_anode` |
| 发热功率 | `CHARGE → integrated → Q` | 随偏压变化的数据 |
| 温度截面 | `CHARGE → temperature_monitor → temperature → T` | 0 V 与 1 V 的 xz 分布及色标 |

截图见 `results/figures/20261101_101141_668681/`；此工程不包含 1 V 以上的结果。
