# 双微环折射率扫描

本次只扫描电路模型中 `ring2` 的有效折射率。折射率改变量等于
`fraction × 0.00672575676`；1.0 对应 s05 的静态对齐输入。
各 fraction 是配置中的探索值，不代表电压、温度或实测数据。

## 工程文件

| fraction | 原生工程 | 就近 Drop2 峰位 (nm) | 峰值功率透射率 |
|---:|---|---:|---:|
| 0.75 | `dual_ring_index_fraction_0p750.icp` | 1551.699192 | 0.0134573 |
| 1 | `dual_ring_index_fraction_1p000.icp` | 1551.709091 | 0.83181 |
| 1.25 | `dual_ring_index_fraction_1p250.icp` | 1551.718990 | 0.0135032 |

## 工程打开后使用方法

用 Lumerical INTERCONNECT 打开上表对应的 `.icp`，在原理图选 `ONA`。
在 Result View 展开 `input 3 → mode 1 → transmission`，双击并在
Visualizer 把 `Scalar operation` 设为 `Abs^2`、横轴设为 wavelength，
得到 Drop2 功率透射谱。`input 1` 为 Through，`input 2` 为 Drop1。

## 可以得到的结果（及截图）

| 截图 | 对应工程和位置 | 重点 |
|---|---|---|
| `fraction_075_drop2.png` | `dual_ring_index_fraction_0p750.icp` 的 `ONA → input 3` | 谱线、峰位和波长轴 |
| `fraction_100_drop2.png` | `dual_ring_index_fraction_1p000.icp` 的 `ONA → input 3` | 与两侧状态对比 |
| `fraction_125_drop2.png` | `dual_ring_index_fraction_1p250.icp` 的 `ONA → input 3` | 主峰是否随折射率变化 |

截图由用户保存到 `results/figures/s06_ring_index_tuning_20261107_160617_463134/`。不同图使用相同波长范围和 `Abs^2` 标度。

## 原生结果判断

三个工程的 `ONA` 各有 8001 个有效波长采样点。只调 `ring2` 时，
1551.7 nm 附近的 Drop2 峰值功率在 fraction=1 达到约 0.832，
而 fraction=0.75 与 1.25 仅约 0.0135。就近峰位分别为
1551.699、1551.709 和 1551.719 nm。此扫描主要体现双环对齐导致的
通带强度变化，不应据此声称完成宽范围波长扫描。
