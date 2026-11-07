# s03 双环静态对齐截图核验

工程：`../../runs/s03_dual_ring_align_20261107_005457_051993/dual_ring_static_aligned.icp`；日志：`../../logs/s03_dual_ring_align_20261107_005457_051993/driver.log`。均为仿真结果。

| 截图 | 工程内查看位置 | 核验结果 |
|---|---|---|
| [aligned_schematic.png](aligned_schematic.png) | 原理图 | 两环串接；长度分别为 62.83185307 µm 和 69.11503838 µm。通过。环 2 折射率偏置 0.00672576 未显示在截图中，以工程属性和日志为准。 |
| [aligned_through.png](aligned_through.png) | ONA → input 1 / mode 1 / TE transmission | `Abs^2`，1520–1600 nm，Through 谐振谷。通过。 |
| [aligned_drop1.png](aligned_drop1.png) | ONA → input 2 / mode 1 / TE transmission | `Abs^2`，1520–1600 nm，Drop1 谐振峰。通过。 |
| [aligned_drop2.png](aligned_drop2.png) | ONA → input 3 / mode 1 / TE transmission | `Abs^2`，1520–1600 nm；对齐主峰约 1551.71 nm。日志峰值 0.776345。通过。 |

| 结论 | 限制 |
|---|---|
| 静态折射率偏置让两环峰在约 1551.71 nm 对齐。 | 未施加温度或电压；不能作为热调谐结果。 |
