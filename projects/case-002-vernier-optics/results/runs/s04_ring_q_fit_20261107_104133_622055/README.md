# 双微环耦合参数校准

## `dual_ring_q_calibrated.icp`

### 算例做了什么

在冷态双环电路中扫描总线功率耦合系数，并选用 0.055，使 Through 谐振的加载 Q 接近论文报告的约 9000；本轮计算值约 8878。此算例尚未叠加 s03 的静态峰对齐，也未建立耦合间隙到系数的器件级映射。

### 工程打开后使用方法

在 Ansys Lumerical INTERCONNECT 打开本工程。选中 `ONA`，在 Result View
展开 `input 1/2/3 → mode 1 → transmission`，分别对应 Through、Drop1、Drop2。
双击结果后在 Visualizer 的 `Scalar operation` 选 `Abs^2`，查看功率透射谱。

### 可以得到的结果（及截图）

| 截图名称 | 工程内查看位置 | 核验重点 |
|---|---|---|
| `q_calibrated_through.png` | `ONA → input 1 → mode 1 → transmission` | 1550 nm 附近的第一环谐振凹口、半高宽及功率基线 |
| `q_calibrated_drop2.png` | `ONA → input 3 → mode 1 → transmission` | 双环冷态共同峰和旁峰 |
| `q_calibrated_schematic.png` | 原理图 | 两环连接、三个输出端口、耦合系数属性 |

截图由用户手动保存到本算例 `results/figures/` 下与本运行目录同名的文件夹。

| 本轮记录 | 数值 | 说明 |
|---|---:|---|
| 两个总线耦合系数 | `0.055` | 电路模型的功率耦合系数，尚未由 200 nm 间隙直接提取 |
| Through 加载 Q | `8878.177` | 从原生光谱的半深度线宽计算 |
| Through 消光比 | `26.650 dB` | 从原生光谱的凹口深度计算 |
| 论文报告的加载 Q | `9000` | 文献参考，仅用于参数校准 |
| 论文报告的消光比 | `约 20 dB` | 对比项，未作为本轮单目标优化约束 |

本工程仍是冷态电路模型；耦合间隙、弯曲损耗、热调谐和光栅耦合器包络尚未由器件级仿真验证。
