# s02 双微环冷态结果截图校验

| 项目 | 核验依据 | 结论 |
| --- | --- | --- |
| 对应工程 | `../../runs/s02_dual_ring_cold_20261107_000643_250729/dual_ring_cold.icp` | 与四张截图所示的 INTERCONNECT 双环电路一致 |
| 求解记录 | `../../logs/s02_dual_ring_cold_20261107_000643_250729/driver.log` | ONA 的 input 1、2、3 均有 8001 个波长采样点，覆盖约 1520～1600 nm |
| 图像设置 | 三张光谱的 `Scalar operation` 均为 `Abs^2`，横轴为 `wavelength (nm)` | 可作为功率透射率截图；纵轴为线性比例 |
| 使用范围 | `config/03_dual_ring_cold.json` 的初始冷态电路 | 仅证明冷态级联双环模型产生了可读光谱；不代表 1550 nm 对齐、热调谐或实测性能 |

| 截图 | 核对内容 | 结论 |
| --- | --- | --- |
| [dual_ring_schematic.png](dual_ring_schematic.png) | ONA 输入、两个级联环和三个 ONA 返回端可见；ring1、ring2 的长度分别约为 62.83 µm、69.12 µm | 通过 |
| [dual_ring_through.png](dual_ring_through.png) | `ONA:input 1/mode 1`；`TE transmission`；`Abs^2`；有连续谐振凹口 | 通过 |
| [dual_ring_drop1.png](dual_ring_drop1.png) | `ONA:input 2/mode 1`；`TE transmission`；`Abs^2`；有多条窄峰 | 通过 |
| [dual_ring_drop2.png](dual_ring_drop2.png) | `ONA:input 3/mode 1`；`TE transmission`；`Abs^2`；约 1524～1525 nm 有明显主峰，其他峰很弱 | 通过；说明两环在该波段已有共同峰，但目标 1550 nm 附近尚未对齐 |

这里的“冷态”指未在光学电路中施加加热或电压响应；它不是实测环境温度的声明。s02 将两环设为同一 FDE 主模有效折射率 2.39749，半径分别为 10 µm 和 11 µm。s03 的独立环检查显示，1550 nm 附近的环 1 谐振在 1551.71 nm、环 2 在 1549.21 nm，相差约 2.50 nm；之后才给环 2 增加约 0.00672576 的静态有效折射率偏置，使目标共同峰出现在约 1551.71 nm。这不代表 s02 在所有波长都没有共同谐振。

三个输出端的结果名称、连接关系与[工程说明](../../runs/s02_dual_ring_cold_20261107_000643_250729/README.md)一致。求解日志记录的功率范围分别为 input 1：0.00363～0.99953，input 2：约 1.96×10⁻⁶～0.88582，input 3：约 1.75×10⁻⁷～0.77536；截图中的凹口和峰值量级与之相符。以上数值来自仿真日志，不是实测数据。
