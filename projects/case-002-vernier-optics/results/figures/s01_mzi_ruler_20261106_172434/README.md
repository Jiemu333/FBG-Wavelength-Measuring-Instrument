# s01 独立 MZI 标尺截图核验

原生工程位于 `../../runs/s01_mzi_ruler_20261106_172434/`；分别打开 `mzi_ruler_dL_050um.icp`、`mzi_ruler_dL_100um.icp`，模式工程为 `mzi_waveguide_mode.lms`。以下为仿真数据，非实测标尺。

| 截图 | 核验结果 | 判断 |
|---|---|---|
| [mzi_dL050um_transmission.png](mzi_dL050um_transmission.png) | ONA input 1 / mode 1，TE transmission，`Abs^2`；1530–1565 nm，条纹间距约 11.5 nm。 | 通过 |
| [mzi_dL100um_transmission.png](mzi_dL100um_transmission.png) | 同一数据项，1530–1565 nm，条纹间距约 5.7 nm；但运算设为 `Re`，与 50 µm 图的 `Abs^2` 不一致。 | 条纹周期通过；比较透射强度前需改为 `Abs^2` 重截 |
| [mzi_dL050um_fsr.png](mzi_dL050um_fsr.png) | ONA input 1 的 TE free spectral range，`Re`，纵轴单位为 m；仅 3 个间隔数据点，约 11.4–11.6 nm。 | 通过，点数少属于此波段内可识别间隔数量有限 |
| [mzi_dL100um_fsr.png](mzi_dL100um_fsr.png) | 同一 FSR 结果项，4 个间隔数据点，约 5.67–5.79 nm。 | 通过 |
| [屏幕截图 2026-11-06 214331.png](屏幕截图%202026-11-06%20214331.png) | MODE FDE 模式强度位于波导芯区；x/z 单位 µm，有 0–1 色标。 | 场分布通过；图内未显示 mode 1 或 neff 数值，须配合下一图 |
| [屏幕截图 2026-11-06 214407.png](屏幕截图%202026-11-06%20214407.png) | mode1 Result View 显示 neff=2.39749、ng=4.16704、TE polarization fraction=0.975912；y=0 的 x/z 截面。 | 数值通过 |

| 总结 | 限制 |
|---|---|
| 臂长差加倍后条纹间隔约减半，符合独立波长标尺模型。 | 透射对比图需统一 `Abs^2`；当前没有证明制作误差、热漂移或真实仪器标定精度。 |
