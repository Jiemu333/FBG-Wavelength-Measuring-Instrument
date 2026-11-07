# 双微环协同折射率扫描

在 s05 静态对齐基础上，两个环的有效折射率同时增加配置中的 common offset。
这是光学电路参数扫描，**不是**电压、温度或实测标定。

## 工程文件

| common Δneff | 原生工程 | Drop2 峰位 (nm) | 峰值功率透射率 |
|---:|---|---:|---:|
| 0 | `dual_ring_common_offset_0p000000.icp` | 1551.709091 | 0.83181 |
| 0.001 | `dual_ring_common_offset_0p001000.icp` | 1552.085354 | 0.830874 |
| 0.002 | `dual_ring_common_offset_0p002000.icp` | 1552.451891 | 0.827709 |

## 工程打开后使用方法

用 Lumerical INTERCONNECT 打开上表中的 `.icp`，选原理图中的 `ONA`，
在 Result View 展开 `input 3 → mode 1 → transmission` 并双击。
在 Visualizer 中选择 `Scalar operation = Abs^2`，横轴为 wavelength。
`input 1` 是 Through，`input 2` 是 Drop1。

## 可以得到的结果（及截图）

| 截图名 | 工程内查看位置 | 核验重点 |
|---|---|---|
| `offset_0.000000.png` | `dual_ring_common_offset_0p000000.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.001000.png` | `dual_ring_common_offset_0p001000.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |
| `offset_0.002000.png` | `dual_ring_common_offset_0p002000.icp` → `ONA → input 3 → mode 1 → transmission` | Drop2 主峰的波长、功率和旁峰 |

截图由用户存入 `results/figures/s07_ring_common_tuning_20261107_161037_819605/`，三张图使用相同波长范围与功率标度。
