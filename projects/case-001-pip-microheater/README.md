# 案例 001：p-i-p 微加热器截面仿真

| 位置 | 内容 |
| --- | --- |
| `models/source/` | 组员交接原始工程，只读保留 |
| `models/baseline/` | 已修正温度监视器的输入基准 |
| `scripts/` | 已验证脚本和功能说明，见该目录 README |
| `results/runs/` | 已完成的 Lumerical 原生工程，见该目录 README |
| `results/logs/` | 对应求解器日志 |
| `results/figures/` | 用户提供的成果截图 |

## 成功工程

| 工程 | 已完成范围 | 查看重点 |
| --- | --- | --- |
| `results/runs/s01_baseline_20261101_101141/heater_charge_0to1V.ldev` | CHARGE 0～1 V，11 点 | `CHARGE > anode > I`、`integrated > Q`、温度监视器 `T` |
| `results/runs/s02_mesh_compare_20261102_090510/charge_mesh_medium.ldev` | CHARGE 0～1 V，11 点 | 中等网格下的 I、Q、T |
| `results/runs/s03_mesh_cap60k_20261102_100139/charge_mesh_cap60k.ldev` | CHARGE 0～1 V，11 点 | 细化上限 60000 下的 I、Q、T；脚本 03 的输出 |
| `results/runs/s05_continue2p1_20261102_190815/charge_continue_2p1.ldev` | CHARGE 至 2.1 V | 2.1 V 处的 I、Q、T 和载流子分布 |
| `results/runs/s12_fig2_0to1_20261105_145819_844533/pip_fig2_0to1.ldev` | CHARGE 0～1 V；新增局部电场、能带和空穴截线 | 图 2 的 0/1 V 电场与能带；具体入口见 `results/runs/README.md` |

以上为已完成的求解范围；物理模型是否与论文一致，需另行核对材料、几何、掺杂和边界条件。

脚本功能、配置和查看结果的方法分别见 `scripts/README.md` 与 `results/runs/README.md`。

## 线上可查看的截图

| 成果 | 截图 | 说明 |
| --- | --- | --- |
| 图 2(b) 局部电场，0 V | [查看](results/figures/s12_fig2_0to1_20261105_145819_844533/fig2b_E_0V.png) | 与 1 V 图使用同一截面和色标 |
| 图 2(c) 局部电场，1 V | [查看](results/figures/s12_fig2_0to1_20261105_145819_844533/fig2c_E_1V.png) | 仅代表 0～1 V 阶段结果 |
| 图 2(d) 能带截线，0 V | [查看](results/figures/s12_fig2_0to1_20261105_145819_844533/fig2d_bands_0V.png) | 沿硅 slab 截线 |
| 图 2(e) 能带截线，1 V | [查看](results/figures/s12_fig2_0to1_20261105_145819_844533/fig2e_bands_1V.png) | 沿同一截线 |

早期整区域电场图因色标范围过大而近乎全蓝，保留在本地作为过程记录，不用作图 2 的成果图。
