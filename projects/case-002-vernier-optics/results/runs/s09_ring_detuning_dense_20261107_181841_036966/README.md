# 双微环折射率扫描

## 算例做了什么

把 s06 的单环失谐扫描加密为 11 个对齐比例点，只改变 ring2 的有效折射率，考察 Drop2 在对齐点附近的峰值功率变化。比例是光学模型输入，不是电压或温度。

本次只扫描电路模型中 `ring2` 的有效折射率。折射率改变量等于
`fraction × 0.00672575676`；1.0 对应 s05 的静态对齐输入。
各 fraction 是配置中的探索值，不代表电压、温度或实测数据。

## 工程文件

| fraction | 原生工程 | 就近 Drop2 峰位 (nm) | 峰值功率透射率 |
|---:|---|---:|---:|
| 0.9 | `dual_ring_index_fraction_0p900.icp` | 1551.679394 | 0.0840373 |
| 0.92 | `dual_ring_index_fraction_0p920.icp` | 1551.649698 | 0.133755 |
| 0.94 | `dual_ring_index_fraction_0p940.icp` | 1551.610105 | 0.250804 |
| 0.96 | `dual_ring_index_fraction_0p960.icp` | 1551.649698 | 0.442002 |
| 0.98 | `dual_ring_index_fraction_0p980.icp` | 1551.679394 | 0.693006 |
| 1 | `dual_ring_index_fraction_1p000.icp` | 1551.709091 | 0.83181 |
| 1.02 | `dual_ring_index_fraction_1p020.icp` | 1551.738789 | 0.701978 |
| 1.04 | `dual_ring_index_fraction_1p040.icp` | 1551.768489 | 0.450038 |
| 1.06 | `dual_ring_index_fraction_1p060.icp` | 1551.808090 | 0.255414 |
| 1.08 | `dual_ring_index_fraction_1p080.icp` | 1551.768489 | 0.136096 |
| 1.1 | `dual_ring_index_fraction_1p100.icp` | 1551.748689 | 0.0852469 |

## 工程打开后使用方法

用 Lumerical INTERCONNECT 打开上表对应的 `.icp`，在原理图选 `ONA`。
在 Result View 展开 `input 3 → mode 1 → transmission`，双击并在
Visualizer 把 `Scalar operation` 设为 `Abs^2`、横轴设为 wavelength，
得到 Drop2 功率透射谱。`input 1` 为 Through，`input 2` 为 Drop1。

## 可以得到的结果（及截图）

| 截图 | 对应工程和位置 | 重点 |
|---|---|---|
| `fraction_0.900.png` | `dual_ring_index_fraction_0p900.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.920.png` | `dual_ring_index_fraction_0p920.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.940.png` | `dual_ring_index_fraction_0p940.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.960.png` | `dual_ring_index_fraction_0p960.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.980.png` | `dual_ring_index_fraction_0p980.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_1.000.png` | `dual_ring_index_fraction_1p000.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_1.020.png` | `dual_ring_index_fraction_1p020.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_1.040.png` | `dual_ring_index_fraction_1p040.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_1.060.png` | `dual_ring_index_fraction_1p060.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_1.080.png` | `dual_ring_index_fraction_1p080.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_1.100.png` | `dual_ring_index_fraction_1p100.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |

截图由用户保存到 `results/figures/s09_ring_detuning_dense_20261107_181841_036966/`。不同图使用相同波长范围和 `Abs^2` 标度。

### 原生结果核验与截图设置

11 份工程均保存了三个 ONA 端口各 8001 个有效光谱采样点。
`fraction=1.000` 时，1551.709 nm 附近的 Drop2 峰值功率透射率约 0.832；
`fraction=0.900` 和 `1.100` 时，附近峰值分别约 0.084 和 0.085。
这一组展示单环失配导致的**通带强度变化**，不作为连续峰位移动的截图序列。
现有 11 张截图统一使用 1520～1600 nm 波长轴、0～1 纵轴，便于比较峰高；详细逐图核验见[截图目录说明](../../figures/s09_ring_detuning_dense_20261107_181841_036966/README.md)。截图未显示 ONA 结果名和 `Abs^2` 选项，复查时须在原生工程确认。
