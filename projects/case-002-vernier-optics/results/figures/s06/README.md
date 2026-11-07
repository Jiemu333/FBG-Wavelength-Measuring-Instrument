# s06 单环折射率偏置截图核验

工程：`../../runs/s06_ring_index_tuning_20261107_160617_463134/`；日志：`../../logs/s06_ring_index_tuning_20261107_160617_463134/driver.log`。fraction 为环 2 静态折射率偏置的比例，是仿真输入，不是电压或温度。

| 截图 | 打开的工程 | 可核对结果 | 判断 |
|---|---|---|---|
| [dual_ring_index_fraction_0p750.png](dual_ring_index_fraction_0p750.png) | `dual_ring_index_fraction_0p750.icp` | ONA input 3 / mode 1，`Abs^2`；日志在 1551.699 nm 附近峰值 0.0134573 | 单图通过；比较图待补 |
| [dual_ring_index_fraction_1p000.png](dual_ring_index_fraction_1p000.png) | `dual_ring_index_fraction_1p000.icp` | 同一结果项；日志在 1551.709 nm 附近峰值 0.83181 | 单图通过；比较图待补 |
| [dual_ring_index_fraction_1p250.png](dual_ring_index_fraction_1p250.png) | `dual_ring_index_fraction_1p250.icp` | 同一结果项；日志在 1551.719 nm 附近峰值 0.0135032 | 单图通过；比较图待补 |

| 比较限制 | 建议补拍 |
|---|---|
| 三张截图的纵轴自动缩放：0.75、1.25 的上限约 0.14，1.00 的上限约 0.85，图上峰高不能直接比较。 | 在三个工程的 Visualizer 中都固定横轴 1551.4–1552.1 nm、纵轴 0–1，保持 `Abs^2`，再截图。现有结果只说明静态失谐对通带的影响。 |
