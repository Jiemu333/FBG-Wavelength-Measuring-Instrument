# 网格上限 60000 对照工程

## `charge_mesh_cap60k.ldev`

### 算例做了什么

在 0～1 V、11 个偏压点条件下，将自动网格细化上限设为 60000 后计算 CHARGE，用于与 s02 比较网格敏感性，并作为后续图 2 监视器工程的输入。

### 工程打开后使用方法

在 DEVICE 打开本目录的 `charge_mesh_cap60k.ldev`，选 `CHARGE`；在 Result View 打开电流、功率或温度数据集，Visualizer 中选择 `V_anode`，保持阴极 0 V。

### 可以得到的结果（及截图）

| 结果 | 工程内入口 | 核验重点 |
| --- | --- | --- |
| I–V | `CHARGE → anode → I` | 0～1 V 的 11 点及与 s02 的差异 |
| 功率与温度 | `CHARGE → integrated → Q`；`temperature_monitor → temperature → T` | 同偏压、同位置对照 |

截图见 `results/figures/20261102_100139_948571/`；不含高压扫描。
