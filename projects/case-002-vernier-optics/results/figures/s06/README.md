# s06 单环折射率偏置截图核验

工程：`../../runs/s06_ring_index_tuning_20261107_160617_463134/`；日志：`../../logs/s06_ring_index_tuning_20261107_160617_463134/driver.log`。fraction 为环 2 静态折射率偏置的比例，是仿真输入，不是电压或温度。

| 截图 | 对应工程与结果入口 | 截图和日志核对 | 结论与范围 |
|---|---|---|---|
| [dual_ring_index_fraction_0p750.png](dual_ring_index_fraction_0p750.png) | `dual_ring_index_fraction_0p750.icp` → `ONA → input 3 → mode 1 → transmission` | 图中主峰约 1542.7 nm、0.139；日志的全带最大值 0.138737796，1551.7 nm 附近局部峰 0.0134573 | 与日志相符；主峰位于对齐基准的短波侧 |
| [dual_ring_index_fraction_1p000.png](dual_ring_index_fraction_1p000.png) | `dual_ring_index_fraction_1p000.icp` → 同一入口 | 图中主峰约 1551.7 nm、0.832；日志最大值 0.831809814 | 与日志相符；这是本扫描中最强的共同通带 |
| [dual_ring_index_fraction_1p250.png](dual_ring_index_fraction_1p250.png) | `dual_ring_index_fraction_1p250.icp` → 同一入口 | 图中主峰约 1560.7 nm、0.137；日志的全带最大值 0.136637916，1551.7 nm 附近局部峰 0.0135032 | 与日志相符；主峰位于对齐基准的长波侧 |

| 比较条件 | 适用范围 |
|---|---|
| 三图横轴均为 1520～1600 nm，纵轴均为 0～1；截图显示峰位和相对高度，日志给出功率透射率数值。 | 这些是静态折射率偏置的电路仿真结果，并非电压、温度或实测光谱。 |
| 当前截图是独立 Figure 窗口，未显示 `ONA` 结果树及 `Scalar operation` 选择。 | `input 3 / mode 1 / Abs^2` 由工程说明和数值日志交叉核对，截图本身不能独立证明该设置。 |

三个主峰相隔约 9 nm，接近半径 10 µm 环在 1551.7 nm 处按 `n_g=4.16704` 估算的单环 FSR（约 9.20 nm）。因此 1542.7 nm 和 1560.7 nm 是相邻谐振阶次附近的**较弱双环透射峰**，不能称为“没有谐振”。`fraction=1` 使 1551.7 nm 附近两环对齐最好；偏置到 0.75 或 1.25 后，共同透射峰转移到相邻阶次附近，但对齐不充分，峰高约 0.14。仅凭 Drop2 谱不能分别给出两只环的精确谐振中心；需要检查单环或各端口光谱。
