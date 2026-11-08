# 双微环协同折射率扫描

## 算例做了什么

把 s07 的双环共同偏置扫描加密为 13 个点（0–0.003，间隔 0.00025），供用户逐个打开原生工程，检查 Drop2 主峰连续移动及峰值稳定性。这仍是光学参数扫描，没有电压、温度或 FBG 输入。

在 s05 静态对齐基础上，两个环的有效折射率同时增加配置中的 common offset。
这是光学电路参数扫描，**不是**电压、温度或实测标定。

## 工程文件

| common Δneff | 原生工程 | Drop2 峰位 (nm) | 峰值功率透射率 |
|---:|---|---:|---:|
| 0 | `dual_ring_common_offset_0p000000.icp` | 1551.709091 | 0.83181 |
| 0.00025 | `dual_ring_common_offset_0p000250.icp` | 1551.808090 | 0.826814 |
| 0.0005 | `dual_ring_common_offset_0p000500.icp` | 1551.897200 | 0.832042 |
| 0.00075 | `dual_ring_common_offset_0p000750.icp` | 1551.986320 | 0.829069 |
| 0.001 | `dual_ring_common_offset_0p001000.icp` | 1552.085354 | 0.830874 |
| 0.00125 | `dual_ring_common_offset_0p001250.icp` | 1552.174496 | 0.831288 |
| 0.0015 | `dual_ring_common_offset_0p001500.icp` | 1552.273554 | 0.828316 |
| 0.00175 | `dual_ring_common_offset_0p001750.icp` | 1552.362717 | 0.832114 |
| 0.002 | `dual_ring_common_offset_0p002000.icp` | 1552.451891 | 0.827709 |
| 0.00225 | `dual_ring_common_offset_0p002250.icp` | 1552.550985 | 0.83154 |
| 0.0025 | `dual_ring_common_offset_0p002500.icp` | 1552.640180 | 0.830516 |
| 0.00275 | `dual_ring_common_offset_0p002750.icp` | 1552.739298 | 0.829571 |
| 0.003 | `dual_ring_common_offset_0p003000.icp` | 1552.828514 | 0.831935 |

## 工程打开后使用方法

用 Lumerical INTERCONNECT 打开上表中的 `.icp`，选原理图中的 `ONA`，
在 Result View 展开 `input 3 → mode 1 → transmission` 并双击。
在 Visualizer 中选择 `Scalar operation = Abs^2`，横轴为 wavelength。
`input 1` 是 Through，`input 2` 是 Drop1。

## 可以得到的结果（及截图）

| 截图名 | 工程内查看位置 | 核验重点 |
|---|---|---|
| `offset_0.000000.png` | `dual_ring_common_offset_0p000000.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.000250.png` | `dual_ring_common_offset_0p000250.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.000500.png` | `dual_ring_common_offset_0p000500.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.000750.png` | `dual_ring_common_offset_0p000750.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.001000.png` | `dual_ring_common_offset_0p001000.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.001250.png` | `dual_ring_common_offset_0p001250.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.001500.png` | `dual_ring_common_offset_0p001500.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.001750.png` | `dual_ring_common_offset_0p001750.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.002000.png` | `dual_ring_common_offset_0p002000.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.002250.png` | `dual_ring_common_offset_0p002250.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.002500.png` | `dual_ring_common_offset_0p002500.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.002750.png` | `dual_ring_common_offset_0p002750.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.003000.png` | `dual_ring_common_offset_0p003000.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |

截图由用户存入 `results/figures/s08_ring_common_dense_20261107_181503_872760/`，各张图使用相同波长范围与功率标度。

### 连续切换截图的统一设置

按上表从 `0p000000` 到 `0p003000` 的顺序逐个打开工程、截图。13 张图建议统一使用
`wavelength = 1551.4～1553.1 nm`、功率透射率纵轴 `0～1`，并保持同一窗口尺寸；
Visualizer 的 `Scalar operation` 均选 `Abs^2`。每张图保留横纵轴、`ONA` 结果名称，
截图文件名按上表的 `offset_*.png` 保存。以上坐标范围仅用于展示，不改变仿真输入或结果。

### 原生结果核验

13 个工程都保存了 Through、Drop1、Drop2 各 8001 个有效光谱采样点。
Drop2 主峰按偏置顺序从 1551.709091 nm 连续移动到 1552.828514 nm，
每步约 0.09 nm；峰值功率透射率约 0.83。此结果仍是有效折射率输入扫描，
不是电压到波长的热调谐标定。
