# 双微环冷态 Vernier 光谱

## `dual_ring_cold.icp`

### 工程打开后使用方法

用 Ansys Lumerical INTERCONNECT 打开本工程。电路为 `ONA → ring1 → ring2` 的级联双环：
`ring1` 的 Through 接 ONA `input 1`；`ring1` 的 Drop 进入 `ring2`；
`ring2` 的 Through 接 ONA `input 2`（Drop1）；`ring2` 的 Drop 接 ONA `input 3`（Drop2）。
ONA 的三个结果依次对应 Through、Drop1、Drop2。所有光谱在 Visualizer 的
`Scalar operation` 选 `Abs^2`，查看功率透射率，横轴选波长。

### 可以得到的结果（及截图）

| 截图名称 | 结果查找位置 | 校验重点 |
|---|---|---|
| `dual_ring_through.png` | `ONA → input 1 → mode 1 → transmission` | Through 谐振凹口、波长轴和功率值 |
| `dual_ring_drop1.png` | `ONA → input 2 → mode 1 → transmission` | 第一环输出经过第二环后的剩余谱 |
| `dual_ring_drop2.png` | `ONA → input 3 → mode 1 → transmission` | Vernier 共同谐振、主峰与旁峰 |
| `dual_ring_schematic.png` | 工程原理图 | 两环连接关系、三个输出端 |

截图请手动保存到本算例 `results/figures/` 下与本运行目录同名的文件夹。
`config/03_dual_ring_cold.json` 中的半径和损耗来自论文；耦合系数是待优化的初始输入。
本工程是 INTERCONNECT 电路模型，尚不含实际耦合间隙的 MODE/FDTD 提取结果、
加热调谐、光栅耦合器包络或 FBG 测量链路。
