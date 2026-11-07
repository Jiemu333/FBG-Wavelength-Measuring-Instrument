# 耦合 CHARGE/HEAT 续算

## `charge_to2p2.ldev`

### 工程打开后使用方法

用 Lumerical DEVICE 打开本目录的 `charge_to2p2.ldev`。选 `CHARGE`，在 Result View
双击 `anode`、`integrated` 或 `thermal`。在 Visualizer 的 Parameters 中选
`V_anode`；`V_cathode` 保持 0 V。

### 可以得到的结果（及截图）

| 结果 | 工程内位置 | 核验点 |
|---|---|---|
| I–V | `CHARGE → anode → I` | 横轴 `V_anode`，检查本段终点 2.2 V |
| 发热功率 | `CHARGE → integrated → Q` | 功率数据随偏压存在且有限 |
| 温度与发热密度 | `CHARGE → thermal → T/Q` | 在终点偏压查看温度和热源分布 |
| 局部场与能带 | `CHARGE → paper_E_xz / paper_bandline` | 检查监视器是否有本段数据 |

输入接续工程：`D:\SRTP_Work\projects\case-001-pip-microheater\results\runs\s21_fig23_resume_short_20261107_162546_719649\pip_fig23_resume_short.ldev`。本段设定：2.14062→2.2 V，
初始步长 0.003125 V。各参数均来自 `config/23_charge_to20_stages.json`。
本段仅是分段工程，完整 0–20 V I–V 曲线仍需在所有阶段完成后统一核验。
