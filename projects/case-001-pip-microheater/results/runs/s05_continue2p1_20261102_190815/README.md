# 2.1 V 短程续算

## `charge_continue_2p1.ldev`

### 算例做了什么

沿已有 CHARGE 解继续提高阳极偏压，得到 2.1 V 附近的短程续算结果，用于判断更高偏压计算的可行性；未形成完整 0～20 V 曲线。

### 工程打开后使用方法

在 DEVICE 打开本目录的 `charge_continue_2p1.ldev`，选 `CHARGE`；在 Result View 选择数据集，在 Visualizer 中确认所选 `V_anode`。原续算输入路径已迁移，本文件用于查看已保存的结果。

### 可以得到的结果（及截图）

| 结果 | 工程内入口 | 核验重点 |
| --- | --- | --- |
| 电流、功率 | `CHARGE → anode → I`；`integrated → Q` | 检查 2.1 V 数据点 |
| 温度、载流子 | `CHARGE → temperature_monitor → temperature → T`；`CHARGE → charge → p` | 核对选中的偏压和坐标 |

若手动留图，放入 `results/figures/20261102_190815_641493/`；当前未有核验截图。
