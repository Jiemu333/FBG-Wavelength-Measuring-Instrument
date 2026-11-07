# s04 耦合参数校准截图核验

工程：`../../runs/s04_ring_q_fit_20261107_104133_622055/dual_ring_q_calibrated.icp`；日志：`../../logs/s04_ring_q_fit_20261107_104133_622055/driver.log`。均为仿真结果。

| 截图 | 工程内查看位置 | 核验结果 |
|---|---|---|
| [q_calibrated_schematic.png](q_calibrated_schematic.png) | 原理图 | 两环和 ONA 连接可见；耦合系数 0.055 不在图面上，需查工程属性或日志。结构截图通过。 |
| [q_calibrated_through.png](q_calibrated_through.png) | ONA → input 1 / mode 1 / TE transmission | `Abs^2`，1520–1600 nm，谐振谷可见。通过；全波段截图无法直接量出线宽或 Q。 |
| [q_calibrated_drop2.png](q_calibrated_drop2.png) | ONA → input 3 / mode 1 / TE transmission | `Abs^2`，1520–1600 nm，冷态谱峰可见。通过。 |

| 日志结论 | 截图证据的边界 |
|---|---|
| 扫描耦合候选值后选 0.055，加载 Q ≈ 8878，消光比 ≈ 26.65 dB。 | Q 数值来自日志，不能从当前全波段截图直接复核。若要截图证明 Q，应放大目标谐振谷并显示半高宽/数据读数。此算例没有静态峰对齐，也没有热或电压调谐。 |
