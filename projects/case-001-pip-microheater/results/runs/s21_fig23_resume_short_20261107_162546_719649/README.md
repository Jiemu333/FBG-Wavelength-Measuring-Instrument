# 小步长续算至 2.140625 V

## `pip_fig23_resume_short.ldev`

### 算例做了什么

从前一阶段已求解工程继续小步长推进 CHARGE/HEAT，取得 2.140625 V 的电流、发热、温度及局部场结果，作为 s23 的输入。此工程仅完成本段接续，未达到 20 V。

### 工程打开后使用方法

在 DEVICE 打开本目录的 `pip_fig23_resume_short.ldev`，选 `CHARGE`；在 Result View 打开 `anode`、`integrated`、`thermal` 或局部监视器，在 Visualizer 选择 `V_anode=2.140625 V`、`V_cathode=0 V`。

### 可以得到的结果（及截图）

| 结果 | 工程内入口 | 核验重点 |
| --- | --- | --- |
| 电流与功率 | `CHARGE → anode → I`；`integrated → Q` | 目标偏压点及有限数值 |
| 温度与热源 | `CHARGE → thermal → T/Q` | 截面和色标单位 |
| 局部电场/能带 | `CHARGE → paper_E_xz / paper_bandline` | 检查该偏压是否有监视数据 |

手动截图放在 `results/figures/s21_fig23_resume_short_20261107_162546_719649/`。求解器日志和原生结果集已核验；截图如未提供，不等于图形已核验。
