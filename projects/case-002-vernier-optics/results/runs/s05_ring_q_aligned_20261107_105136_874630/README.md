# 双微环静态谐振对齐

## `dual_ring_static_aligned.icp`

### 算例做了什么

把 s04 选出的 0.055 耦合系数与 s03 的 ring2 静态折射率偏置合并，在同一个双环工程中得到约 1551.71 nm 的 Drop2 共同峰。它是后续折射率扫描的光学基准，尚非电压驱动的热调谐结果。

### 工程打开后使用方法

用 Ansys Lumerical INTERCONNECT 打开该 `.icp`。在原理图中，`ring1` 的 Drop
进入 `ring2`；`ring1` 的 Through 接 ONA `input 1`，`ring2` 的 Through 接
ONA `input 2`（Drop1），`ring2` 的 Drop 接 ONA `input 3`（Drop2）。
在 Result View 展开 `ONA → input 1/2/3 → mode 1 → transmission`，双击要看的结果，
Visualizer 的 `Scalar operation` 选 `Abs^2`，横轴选波长。

### 可以得到的结果（及截图）

| 截图名称 | 工程内查看位置 | 核验重点 |
|---|---|---|
| `aligned_through.png` | `ONA → input 1 → mode 1 → transmission` | 第一环谐振凹口和波长范围 |
| `aligned_drop1.png` | `ONA → input 2 → mode 1 → transmission` | 两环级联后的剩余谱 |
| `aligned_drop2.png` | `ONA → input 3 → mode 1 → transmission` | 共同谐振峰是否移入 1550 nm 附近、主峰与旁峰 |
| `aligned_schematic.png` | 原理图 | 两环连接及三个输出端口 |

截图由用户手动保存到本算例 `results/figures/` 下与本运行目录同名的文件夹。
此次对齐目标共振波长为 `1551.709091 nm`，
`ring2` 的静态有效折射率增加量为 `0.00672575676`。这些量来自本次仿真计算，
两个环的总线功率耦合系数均设为 `0.055`（第一总线）和
`0.055`（第二总线）。
并非热仿真测得的电压、功率或温度。只有在 CHARGE/HEAT 结果通过核验后，
才能建立电压到折射率和通带波长的关系。
