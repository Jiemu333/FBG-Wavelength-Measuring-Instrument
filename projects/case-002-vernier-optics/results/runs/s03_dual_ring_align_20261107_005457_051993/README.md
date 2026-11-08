# 双微环静态谐振对齐

## `dual_ring_static_aligned.icp`

### 算例做了什么

在 s02 冷态电路基础上，选取 1550 nm 参考点附近的两个单环谐振，给 ring2 加入约 0.00672576 的静态有效折射率偏置，使 Drop2 共同峰移到约 1551.71 nm。偏置是光学模型参数，尚未由加热电压标定。

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
| `aligned_drop2.png` | `ONA → input 3 → mode 1 → transmission` | 共同谐振峰是否移入选定的 1550 nm 参考波长附近、主峰与旁峰 |
| `aligned_schematic.png` | 原理图 | 两环连接及三个输出端口 |

截图由用户手动保存到本算例 `results/figures/` 下与本运行目录同名的文件夹。
此次对齐目标共振波长为 `1551.709091 nm`，
`ring2` 的静态有效折射率增加量为 `0.00672575676`。这些量来自本次仿真计算，
并非热仿真测得的电压、功率或温度。只有在 CHARGE/HEAT 结果通过核验后，
才能建立电压到折射率和通带波长的关系。
