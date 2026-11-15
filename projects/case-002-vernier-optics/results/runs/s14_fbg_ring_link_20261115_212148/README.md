# s14 FBG 反射与双微环光路

## fbg_reflection_dual_ring.icp

### 算例做了什么

从已保存的 [s13 双环工程](../s13_local_coupling_circuit_20261115_205936_021858/README.md)读取双环和 ONA 配置，保留原有双环、耦合系数及扫描范围。在 ONA 与 ring1 之间接入环形器和 Bragg 光栅：`ONA output → CIR port 1 → CIR port 2 → FBG port 1`；FBG 反射经 `CIR port 3` 进入 ring1，同时接入 ONA input 4；原有三个双环观察端保持为 ONA input 1/2/3。FBG 中心设置为原工程 Drop2 在 1550 nm 参考点附近的已保存主峰，即 1551.709091 nm。

FBG 使用 Ansys INTERCONNECT Bragg Grating 元件的示范参数：长度 0.005 m，有效/群折射率 1.447/1.447，交流折射率调制 0.0004。这些是模型输入，不是实测 FBG 参数；本算例只验证纯光学连接与频谱，尚未接入探测器、控制器或电热调谐。

### 工程打开后使用方法

用 Ansys Lumerical INTERCONNECT 打开 `fbg_reflection_dual_ring.icp`。在原理图选中 `ONA`，到左侧 Result View 展开 `input 4 → mode 1 → transmission` 看 FBG 返回到环形器第 3 端口的反射谱；展开 `input 3 → mode 1 → transmission` 看经过双环 Drop2 的谱。Visualizer 横轴选 wavelength，`Scalar operation` 选 `Abs^2`，得到功率透射率。可同样查看 input 1/2 的 Through/Drop1。

### 可以得到的结果（及截图）

| 工程内结果 | 观察重点 | 用户截图建议 |
|---|---|---|
| `ONA → input 4 → mode 1 → transmission` | FBG 反射带中心、带宽、波长范围 | `01_fbg_reflection.png` |
| `ONA → input 3 → mode 1 → transmission` | 反射谱通过双环后的 Drop2 主峰与旁峰 | `02_fbg_filtered_drop2.png` |
| `ONA → input 1/2 → mode 1 → transmission` | 双环其他端口谱 | `03_through_drop1.png`（可选） |
| 原理图、FBG/CIR Property View | 连接关系与输入参数 | `04_schematic_parameters.png` |

原生结果核验：ONA input 4 在 1551.699 nm 附近的功率反射率约 0.9988，在 1540 nm 附近约 3.12×10⁻⁵；经过双环的 input 3 在 1551.7 nm 附近有窄峰，全谱最大功率透射率约 0.573。数值取自已保存工程，不是预设目标。`r`n`r`n用户截图目录：`results/figures/s14_fbg_ring_link_20261115_212148/`。所有谱为仿真数据；将来接入真实 FBG 时应以器件参数或实测 S 参数替换这里的示范光栅。
