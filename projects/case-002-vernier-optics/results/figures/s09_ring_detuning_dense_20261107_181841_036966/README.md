# s09 单环静态失谐：截图核验

| 项目 | 结论 |
| --- | --- |
| 数据性质 | INTERCONNECT 光学电路仿真；fraction 是 ring2 有效折射率偏置的比例，不是电压或实测量 |
| 工程目录 | [s09 原生工程](../../runs/s09_ring_detuning_dense_20261107_181841_036966/README.md) |
| 结果入口 | 打开下表对应 `.icp` → 选 `ONA` → Result View 的 `input 3 / mode 1 / transmission` → 功率透射率用 `Abs^2` 查看 |
| 核验依据 | 逐张查看用户截图；对照本地 `results/logs/s09_ring_detuning_dense_20261107_181841_036966/driver.log`，每个端口均有 8001 点，波长约 1520–1600 nm |
| 截图限制 | 截图没有显示 ONA 数据集名和 `Scalar operation`；来源与运算方式还需在对应原生工程中复查 |

| fraction | 截图 | 对应原生工程 | 日志中 1551.7 nm 附近峰位 (nm) | 局部峰值功率透射率 | 核验结论 |
| ---: | --- | --- | ---: | ---: | --- |
| 0.900 | [图](fraction_0.900.png) | `dual_ring_index_fraction_0p900.icp` | 1551.68 | 0.0840373 | 截图局部峰约 0.08–0.10，相符 |
| 0.920 | [图](fraction_0.920.png) | `dual_ring_index_fraction_0p920.icp` | 1551.65 | 0.133755 | 相符 |
| 0.940 | [图](fraction_0.940.png) | `dual_ring_index_fraction_0p940.icp` | 1551.61 | 0.250804 | 相符 |
| 0.960 | [图](fraction_0.960.png) | `dual_ring_index_fraction_0p960.icp` | 1551.65 | 0.442002 | 相符 |
| 0.980 | [图](fraction_0.980.png) | `dual_ring_index_fraction_0p980.icp` | 1551.68 | 0.693006 | 相符 |
| 1.000 | [图](fraction_1.000.png) | `dual_ring_index_fraction_1p000.icp` | 1551.71 | 0.83181 | 峰值最高，相符 |
| 1.020 | [图](fraction_1.020.png) | `dual_ring_index_fraction_1p020.icp` | 1551.74 | 0.701978 | 相符 |
| 1.040 | [图](fraction_1.040.png) | `dual_ring_index_fraction_1p040.icp` | 1551.77 | 0.450038 | 相符 |
| 1.060 | [图](fraction_1.060.png) | `dual_ring_index_fraction_1p060.icp` | 1551.81 | 0.255414 | 相符 |
| 1.080 | [图](fraction_1.080.png) | `dual_ring_index_fraction_1p080.icp` | 1551.77 | 0.136096 | 相符 |
| 1.100 | [图](fraction_1.100.png) | `dual_ring_index_fraction_1p100.icp` | 1551.75 | 0.0852469 | 相符 |

11 张图的坐标统一为 1520–1600 nm、纵轴 0–1；主峰在 fraction=1 附近最高，两侧失谐时减弱。本组验证的是固定波段附近的通带强度敏感性，不能当作调谐电压扫描或全谱最大峰位曲线。
