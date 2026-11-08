# 双微环折射率扫描

## 算例做了什么

本次只扫描电路模型中 `ring2` 的有效折射率。折射率改变量等于
`fraction × 0.00672575676`；1.0 对应 s05 的静态对齐输入。
各 fraction 是配置中的探索值，不代表电压、温度或实测数据。
此轮比较相邻短波谐振阶次与中心阶次的 Drop2 峰值变化；一个工程对应一个固定 fraction，
不同工程按 fraction 从小到大打开即可查看峰高交换，不生成动态图。

## 工程文件

| fraction | 原生工程 | 短波侧局部峰 nm / 功率 | 中心局部峰 nm / 功率 | 全带最高峰 nm / 功率 |
|---:|---|---:|---:|---:|
| 0.75 | `dual_ring_index_fraction_0p750.icp` | 1542.616 / 0.1243 | 1551.699 / 0.01346 | 1542.743 / 0.1387 |
| 0.8 | `dual_ring_index_fraction_0p800.icp` | 1542.596 / 0.04732 | 1551.699 / 0.02088 | 1542.880 / 0.05545 |
| 0.85 | `dual_ring_index_fraction_0p850.icp` | 1542.586 / 0.025 | 1551.689 / 0.0371 | 1551.353 / 0.04364 |
| 0.9 | `dual_ring_index_fraction_0p900.icp` | 1542.577 / 0.01544 | 1551.679 / 0.08404 | 1551.481 / 0.09627 |
| 0.91 | `dual_ring_index_fraction_0p910.icp` | 1542.577 / 0.01422 | 1551.669 / 0.1045 | 1551.511 / 0.1181 |
| 0.92 | `dual_ring_index_fraction_0p920.icp` | 1542.577 / 0.01314 | 1551.650 / 0.1338 | 1551.541 / 0.148 |
| 0.925 | `dual_ring_index_fraction_0p925.icp` | 1542.577 / 0.01265 | 1551.561 / 0.1674 | 1551.561 / 0.1674 |
| 0.93 | `dual_ring_index_fraction_0p930.icp` | 1542.577 / 0.01219 | 1551.580 / 0.1902 | 1551.580 / 0.1902 |
| 0.935 | `dual_ring_index_fraction_0p935.icp` | 1542.577 / 0.01175 | 1551.590 / 0.2178 | 1551.590 / 0.2178 |
| 0.94 | `dual_ring_index_fraction_0p940.icp` | 1542.577 / 0.01133 | 1551.610 / 0.2508 | 1551.610 / 0.2508 |
| 0.95 | `dual_ring_index_fraction_0p950.icp` | 1542.577 / 0.01056 | 1551.630 / 0.3343 | 1551.630 / 0.3343 |
| 0.96 | `dual_ring_index_fraction_0p960.icp` | 1542.577 / 0.00987 | 1551.650 / 0.442 | 1551.650 / 0.442 |
| 0.98 | `dual_ring_index_fraction_0p980.icp` | 1542.577 / 0.00868 | 1551.679 / 0.693 | 1551.679 / 0.693 |
| 1 | `dual_ring_index_fraction_1p000.icp` | 1542.577 / 0.007698 | 1551.709 / 0.8318 | 1551.709 / 0.8318 |

## 工程打开后使用方法

用 Lumerical INTERCONNECT 打开上表对应的 `.icp`，在原理图选 `ONA`。
在 Result View 展开 `input 3 → mode 1 → transmission`，双击并在
Visualizer 把 `Scalar operation` 设为 `Abs^2`、横轴设为 wavelength，
得到 Drop2 功率透射谱。`input 1` 为 Through，`input 2` 为 Drop1。

## 可以得到的结果（及截图）

| 截图 | 对应工程和位置 | 重点 |
|---|---|---|
| `fraction_0.750.png` | `dual_ring_index_fraction_0p750.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.800.png` | `dual_ring_index_fraction_0p800.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.850.png` | `dual_ring_index_fraction_0p850.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.900.png` | `dual_ring_index_fraction_0p900.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.910.png` | `dual_ring_index_fraction_0p910.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.920.png` | `dual_ring_index_fraction_0p920.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.925.png` | `dual_ring_index_fraction_0p925.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.930.png` | `dual_ring_index_fraction_0p930.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.935.png` | `dual_ring_index_fraction_0p935.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.940.png` | `dual_ring_index_fraction_0p940.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.950.png` | `dual_ring_index_fraction_0p950.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.960.png` | `dual_ring_index_fraction_0p960.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_0.980.png` | `dual_ring_index_fraction_0p980.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |
| `fraction_1.000.png` | `dual_ring_index_fraction_1p000.icp` → `ONA → input 3 → mode 1 → transmission` | 峰值功率、峰位和旁峰 |

截图由用户保存到 `results/figures/s09_ring_peak_transfer_20261108_214832_926296/`。逐张截图保持波长范围 1520～1600 nm、
功率透射率纵轴 0～1，Scalar operation 为 `Abs^2`。
表中“短波侧局部峰”按环 1 的 FSR 估算位置搜索，“中心局部峰”按静态对齐波长搜索；
“全带最高峰”直接取 ONA 结果中的最大功率点。三者不能混为同一条连续移动的峰。

## 本轮核验结论与查看顺序

| 顺序 | 打开的工程 | 全带最高峰 | 作用 |
|---:|---|---|---|
| 1 | `dual_ring_index_fraction_0p750.icp` | 1542.743 nm / 0.1387 | 1543 nm 一侧为主峰 |
| 2 | `dual_ring_index_fraction_0p800.icp` | 1542.880 nm / 0.05545 | 短波侧主峰减弱 |
| 3 | `dual_ring_index_fraction_0p850.icp` | 1551.353 nm / 0.04364 | 最高峰已转到中心一侧 |
| 4 | `dual_ring_index_fraction_0p900.icp` | 1551.481 nm / 0.09627 | 中心一侧增强 |
| 5 | `dual_ring_index_fraction_0p925.icp` | 1551.561 nm / 0.1674 | 继续增强 |
| 6 | `dual_ring_index_fraction_0p960.icp` | 1551.650 nm / 0.4420 | 接近对齐 |
| 7 | `dual_ring_index_fraction_1p000.icp` | 1551.709 nm / 0.8318 | 中心对齐主峰 |

其余 7 份工程见上表，可逐点补看。全带最高峰从 1543 nm 一侧切换到 1551 nm 一侧发生在 `fraction=0.80～0.85` 之间；这体现相邻谐振阶次的**主峰强弱交换**，不是同一条峰连续跨越约 9 nm。日志核对 14 份工程、每份 3 个 ONA 端口各 8001 个有效波长点，无报错。截图尚待用户在 Lumerical 中逐图核验。
