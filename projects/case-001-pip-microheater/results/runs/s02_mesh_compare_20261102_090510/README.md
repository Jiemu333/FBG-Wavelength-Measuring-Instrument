# 中等网格对照工程

## `charge_mesh_medium.ldev`

### 算例做了什么

在 0～1 V、11 个偏压点条件下以中等网格重新计算 CHARGE，供与 s01 和 s03 的同偏压结果对照，检查网格对结果的影响。

### 工程打开后使用方法

在 DEVICE 打开本目录的 `charge_mesh_medium.ldev`，选 `CHARGE`；在 Result View 打开 `anode`、`integrated` 或 `temperature_monitor`，Visualizer 中选择 `V_anode`，保持阴极 0 V。

### 可以得到的结果（及截图）

| 结果 | 工程内入口 | 核验重点 |
| --- | --- | --- |
| I–V | `CHARGE → anode → I` | 与 s01/s03 的同偏压点比较 |
| 功率与温度 | `CHARGE → integrated → Q`；`temperature_monitor → temperature → T` | 比较数值及空间分布 |

截图见 `results/figures/20261102_090510_512039/`。本算例只改变网格设置，不是新的器件结构。
