# s05 耦合校准与静态对齐截图核验

工程：`../../runs/s05_ring_q_aligned_20261107_105136_874630/dual_ring_static_aligned.icp`；日志：`../../logs/s05_ring_q_aligned_20261107_105136_874630/driver.log`。均为仿真结果。

| 截图 | 工程内查看位置 | 核验结果 |
|---|---|---|
| [aligned_schematic.png](aligned_schematic.png) | 原理图 | ONA 与两环串接，长度可见。通过；耦合系数需查属性或日志。 |
| [aligned_through.png](aligned_through.png) | ONA → input 1 / mode 1 / TE transmission | `Abs^2`，1520–1600 nm，谐振谷可见。通过。 |
| [aligned_drop1.png](aligned_drop1.png) | ONA → input 2 / mode 1 / TE transmission | `Abs^2`，1520–1600 nm，Drop1 峰可见。通过。 |
| [aligned_drop2.png](aligned_drop2.png) | ONA → input 3 / mode 1 / TE transmission | `Abs^2`，1520–1600 nm；主峰约 1551.71 nm，日志峰值 0.83181。通过。 |

| 结论 | 限制 |
|---|---|
| 同时使用耦合系数 0.055 和环 2 静态折射率偏置 0.00672576，得到对齐的 Drop2 主峰。 | 这是冷态光路模型，不是热调谐或电压响应。 |
