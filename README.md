# SRTP_Work 目录说明

| 路径 | 内容 |
| --- | --- |
| `AGENTS.md` | 协作规则 |
| `.agents/skills/sim-runner/` | 仿真工作流程 |
| `projects/case-001-pip-microheater/README.md` | 本案例参数、可用脚本和成功成果索引 |
| `projects/case-001-pip-microheater/models/` | 原始工程与输入基准 |
| `projects/case-001-pip-microheater/results/runs/` | 已完成的原生工程 |
| `projects/case-001-pip-microheater/results/logs/` | 对应求解日志 |
| `projects/case-001-pip-microheater/results/figures/` | 用户提供的截图 |
| [`projects/case-002-vernier-optics/README.md`](projects/case-002-vernier-optics/README.md) | 双微环与 MZI 光学模型、已完成算例索引 |

后续案例各自使用独立目录；只有成功且可用的脚本和工程进入索引。

## 在线查看

| 内容 | 入口 | 当前范围 |
| --- | --- | --- |
| p-i-p 微加热器 | [案例 001](projects/case-001-pip-microheater/README.md) · [0～1 V 电流曲线](projects/case-001-pip-microheater/results/figures/20261101_101141_668681/01_iv.png) | 截面电热仿真的阶段性结果；尚非论文全部偏压范围 |
| MZI 波长标尺 | [案例 002](projects/case-002-vernier-optics/README.md) · [50 μm 光谱](projects/case-002-vernier-optics/results/figures/s01_mzi_ruler_20261106_172434/mzi_dL050um_transmission.png) · [100 μm 光谱](projects/case-002-vernier-optics/results/figures/s01_mzi_ruler_20261106_172434/mzi_dL100um_transmission.png) | 独立 MZI 模型的阶段性结果 |

此仓库用于在线浏览说明、配置、脚本与已核验截图。Lumerical 原生工程、求解日志和运行中数据保存在本地算例目录；仓库中的原生工程路径仅用于定位本机文件。仿真结果不是实测数据。
