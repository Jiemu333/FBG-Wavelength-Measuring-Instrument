# MZI 独立标尺设计对比

## 工程打开后使用方法

### mzi_ruler_dL_050um.icp

在 Ansys Lumerical INTERCONNECT 中打开此工程。选中 `ONA`，在 Result View 展开 `input 1` → `mode 1` → `transmission` 并双击查看；横轴是波长，曲线的复数模长平方对应功率透射率。通过相邻干涉峰的间距比较该臂长差下的 FSR。

### mzi_ruler_dL_100um.icp

在 Ansys Lumerical INTERCONNECT 中打开此工程。选中 `ONA`，在 Result View 展开 `input 1` → `mode 1` → `transmission` 并双击查看；横轴是波长，曲线的复数模长平方对应功率透射率。通过相邻干涉峰的间距比较该臂长差下的 FSR。

## ONA 自动 FSR 结果

在 Result View 中展开 `ONA` → `input 1` → `mode 1` → `peak` → `free spectral range` 查看自动识别的峰间距。透射功率曲线在 `input 1` → `mode 1` → `transmission`；Visualizer 的 `Scalar operation` 选择 `Abs^2`。

## 可以得到的结果

| 结果 | 工程 | 在工程中查看 | 用途 |
|---|---|---|---|
| MZI 透射谱 | `mzi_ruler_dL_050um.icp`、`mzi_ruler_dL_100um.icp` | `ONA → input 1 → mode 1 → transmission`；Visualizer 选 `Abs^2` | 比较两种臂长差的周期条纹和条纹密度 |
| 自动 FSR | 两个 `.icp` 工程 | `ONA → input 1 → mode 1 → peak → free spectral range` | 查看相邻峰间距，验证 MZI 波长标尺周期 |
| 波导基模场分布 | `mzi_waveguide_mode.lms` | `FDE` 的 mode 1 结果 | 检查 MZI 波导横截面所用模式 |

## 成果截图

请从 Lumerical 窗口手动截图，不需要运行脚本生成图片。截图统一存放在：

`D:\SRTP_Work\projects\case-002-vernier-optics\results\figures\s01_mzi_ruler_20261106_172434\`

如果该目录尚不存在，请先新建。建议保存以下截图：

| 截图文件名 | 打开的工程 | 截图内容与核验重点 |
|---|---|---|
| `mzi_dL050um_transmission.png` | `mzi_ruler_dL_050um.icp` | ONA 的 `transmission` 透射谱；横轴为波长，Visualizer 使用 `Abs^2` |
| `mzi_dL050um_fsr.png` | `mzi_ruler_dL_050um.icp` | ONA 的 `peak → free spectral range` 结果 |
| `mzi_dL100um_transmission.png` | `mzi_ruler_dL_100um.icp` | ONA 的 `transmission` 透射谱；与 50 µm 工程比较条纹密度 |
| `mzi_dL100um_fsr.png` | `mzi_ruler_dL_100um.icp` | ONA 的 `peak → free spectral range` 结果；与 50 µm 工程比较峰间距 |
| `mode_waveguide_cross_section.png`（可选） | `mzi_waveguide_mode.lms` | FDE mode 1 的横截面场分布 |

已核验的线上截图还包括 [50 µm 自动 FSR](../../figures/s01_mzi_ruler_20261106_172434/mzi_dL050um_fsr.png)、[100 µm 自动 FSR](../../figures/s01_mzi_ruler_20261106_172434/mzi_dL100um_fsr.png)、[FDE mode 1 强度场](<../../figures/s01_mzi_ruler_20261106_172434/屏幕截图 2026-11-06 214331.png>) 和 [mode 1 有效折射率](<../../figures/s01_mzi_ruler_20261106_172434/屏幕截图 2026-11-06 214407.png>)。FSR 图只有少数离散点，因为可见波长范围内只检测到少数相邻峰间距；它不是连续扫描曲线。

本轮采用理想 50:50 耦合器；还未加入实际耦合器偏差、传播损耗、工艺误差、温度漂移或双微环联调。50 µm 和 100 µm 是初步对比参数，不是最终版图尺寸。
