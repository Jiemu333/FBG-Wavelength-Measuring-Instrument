# MZI 独立标尺设计对比

## 算例做了什么

| 工程 | 本轮工作 |
|---|---|
| `mzi_ruler_dL_050um.icp` | 用 50 µm 臂长差生成独立 MZI 透射条纹。 |
| `mzi_ruler_dL_100um.icp` | 用 100 µm 臂长差生成透射条纹，比较臂长差对条纹周期的影响。 |

这是中间版本；后续推荐使用 `../s01_mzi_ruler_20261106_172434/` 中带自动 FSR 结果的工程。

## 工程打开后使用方法

### mzi_ruler_dL_050um.icp

在 Ansys Lumerical INTERCONNECT 中打开此工程。选中 `ONA`，在 Result View 展开 `input 1` → `mode 1` → `transmission` 并双击查看；横轴是波长。Visualizer 的 `Scalar operation` 选 `Abs^2` 后，纵轴显示功率透射率。通过相邻干涉峰的间距比较该臂长差下的 FSR。

### mzi_ruler_dL_100um.icp

在 Ansys Lumerical INTERCONNECT 中打开此工程。选中 `ONA`，在 Result View 展开 `input 1` → `mode 1` → `transmission` 并双击查看；横轴是波长。Visualizer 的 `Scalar operation` 选 `Abs^2` 后，纵轴显示功率透射率。通过相邻干涉峰的间距比较该臂长差下的 FSR。

## 可以得到的结果

- 两种臂长差的 MZI 周期透射谱，用于比较 FSR 与条纹密度。
- MODE 截面工程 `mzi_waveguide_mode.lms`，可查看 1.55 µm 附近选中模式的场分布和 FDE 结果。
- 当前模型采用理想 50:50 耦合器；尚未纳入实际耦合器偏差、传播损耗、工艺误差和温度漂移。
