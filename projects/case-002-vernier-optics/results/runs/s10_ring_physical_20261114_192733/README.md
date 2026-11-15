# s10：双微环物理几何与弯曲模式

| 工程 | 算例做了什么 | 工程打开后使用方法 | 可以得到的结果（及截图） |
|---|---|---|---|
| `dual_ring_physical_layout.lms` | 用文献给定的 10/11 µm 环、450 nm 波导和 200 nm 总线间隙构建三条总线、两环的可查看几何。两环沿总线方向错开，环形 slab 在耦合区留开口。没有执行全器件电磁求解。 | 用 MODE 打开；切换 `XY view`，在 Objects Tree 查看 `ring1_ridge`、`ring2_ridge`、`through_bus`、`inter_ring_bus`、`drop2_bus`。 | 截图 `dual_ring_layout.png`：完整双环与三条总线；分别放大环 1、环 2 与中间总线的耦合位置，截 `ring1_bus_gap.png`、`ring2_bus_gap.png`。 |
| `straight_control_mode.lms` | 对与微环相同的局部截面求直波导 FDE 主模，作为弯曲对照。 | 用 MODE 打开，进入 `FDE → data → mode1`；在 Eigenmode Solver Analysis 的 Mode list 查看 `effective index`，并选 `Modal fields → Intensity`。 | 截图 `straight_mode.png`：Mode 1、有效折射率和 x/z 场分布。 |
| `ring1_bent_mode.lms` | 在 10 µm 半径下求环波导局部弯曲 FDE 模式。 | 同上；在 Modal analysis 核对 `bent waveguide`、`bend radius = 10 µm`、`bend orientation = 90°`。 | 截图 `ring1_bent_mode.png`：模式列表、弯曲设置、场分布。 |
| `ring2_bent_mode.lms` | 在 11 µm 半径下求环波导局部弯曲 FDE 模式。 | 同上；核对 `bend radius = 11 µm`。 | 截图 `ring2_bent_mode.png`：模式列表、弯曲设置、场分布。 |

以上截图由用户手动保存到 `results/figures/s10_ring_physical_20261114_192733/`，无需一次截完。原生数值和模式图在 `.lms` 中查看；求解记录在 `results/logs/s10_ring_physical_20261114_192733/driver.log`。

| MODE/FDE 结果 | 有效折射率，1550 nm |
|---|---:|
| 相同截面直波导 | 2.397494931 |
| 10 µm 环弯曲模式 | 2.398312535 |
| 11 µm 环弯曲模式 | 2.398170194 |

本轮通过脚本状态、原生工程文件、FDE Mode 1 有限结果及三个工程中非零且有限的 `E` 场数据核验；两个弯曲工程保存的半径分别为 10/11 µm，弯曲方向均为 90°。场型、颜色标尺及结构位置尚待截图复核。

文献依据：Zhou 等（2013），第 3、4、6 页 / 图 1、图 2；文献原件位于 `D:\个人\srtp项目\项目\可调谐光滤波\文献\Tunable_Vernier_Microring_Optical_Filters_With_p-i_-p-Type_Microheaters\`。总线延伸长度、两环的水平错位、环形 slab 宽度及耦合区 slab 开口角度是可视化布局假设，不是文献或 PDK 尺寸。掺杂、金属和热串扰未进入本轮 MODE 光学求解。200 nm 间隙尚未转换为耦合系数，不要将 s05 的 0.055 当成该间隙的仿真结果。
