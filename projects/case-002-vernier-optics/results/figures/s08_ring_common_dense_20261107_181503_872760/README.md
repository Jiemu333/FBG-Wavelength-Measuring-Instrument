# s08 双微环共同折射率偏置：截图核验

| 项目 | 结论 |
| --- | --- |
| 数据性质 | INTERCONNECT 光学电路仿真；不是电压、温度或实测数据 |
| 工程目录 | [s08 原生工程](../../runs/s08_ring_common_dense_20261107_181503_872760/README.md) |
| 结果入口 | 打开下表对应 `.icp` → 选 `ONA` → Result View 的 `input 3 / mode 1 / transmission` → 功率透射率用 `Abs^2` 查看 |
| 核验依据 | 逐张查看用户截图；对照同一次运行的本地 `results/logs/s08_ring_common_dense_20261107_181503_872760/driver.log`。日志记录每个端口 8001 点，扫描波长约 1520–1600 nm |
| 截图限制 | 截图只包含谱线与坐标，未显示 ONA 数据集名和 `Scalar operation`；这些设置须在对应原生工程中复查 |

| 共同偏置 Δneff | 截图 | 对应原生工程 | 日志主峰 (nm) | 日志峰值功率透射率 | 核验结论 |
| ---: | --- | --- | ---: | ---: | --- |
| 0 | [图](dual_ring_common_offset_0p000000.icp.png) | `dual_ring_common_offset_0p000000.icp` | 1551.71 | 0.83181 | 图中主峰位置与高度相符 |
| 0.00025 | [图](dual_ring_common_offset_0p000250.icp.png) | `dual_ring_common_offset_0p000250.icp` | 1551.81 | 0.826814 | 相符 |
| 0.00050 | [图](dual_ring_common_offset_0p000500.icp.png) | `dual_ring_common_offset_0p000500.icp` | 1551.90 | 0.832042 | 相符 |
| 0.00075 | [图](dual_ring_common_offset_0p000750.icp.png) | `dual_ring_common_offset_0p000750.icp` | 1551.99 | 0.829069 | 相符 |
| 0.00100 | [图](dual_ring_common_offset_0p001000.icp.png) | `dual_ring_common_offset_0p001000.icp` | 1552.09 | 0.830874 | 相符 |
| 0.00125 | [图](dual_ring_common_offset_0p001250.icp.png) | `dual_ring_common_offset_0p001250.icp` | 1552.17 | 0.831288 | 相符 |
| 0.00150 | [图](dual_ring_common_offset_0p001500.icp.png) | `dual_ring_common_offset_0p001500.icp` | 1552.27 | 0.828316 | 相符 |
| 0.00175 | [图](dual_ring_common_offset_0p001750.icp.png) | `dual_ring_common_offset_0p001750.icp` | 1552.36 | 0.832114 | 相符 |
| 0.00200 | [图](dual_ring_common_offset_0p002000.icp.png) | `dual_ring_common_offset_0p002000.icp` | 1552.45 | 0.827709 | 相符 |
| 0.00225 | [图](dual_ring_common_offset_0p002250.icp.png) | `dual_ring_common_offset_0p002250.icp` | 1552.55 | 0.83154 | 相符 |

| 尚无截图的偏置 | 原生工程 | 日志主峰 (nm) | 状态 |
| ---: | --- | ---: | --- |
| 0.00250 | `dual_ring_common_offset_0p002500.icp` | 1552.64 | 求解结果已记录；截图待核验 |
| 0.00275 | `dual_ring_common_offset_0p002750.icp` | 1552.74 | 求解结果已记录；截图待核验 |
| 0.00300 | `dual_ring_common_offset_0p003000.icp` | 1552.83 | 求解结果已记录；截图待核验 |

已截图的 10 个点在统一的 1520–1600 nm、纵轴 0–1 视图中，主峰按偏置顺序向长波移动，峰高约 0.83。截图横轴范围较宽，细小位移需用原生数据或局部放大确认。
