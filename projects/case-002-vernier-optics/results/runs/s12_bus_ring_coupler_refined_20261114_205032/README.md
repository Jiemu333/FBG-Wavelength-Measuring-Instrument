# s12 直波导—微环局部耦合：细网格

## 算例做了什么

| 项目 | 内容 |
|---|---|
| 目的 | 在 200 nm 间隙处用 MODE varFDTD 提取直波导到弯曲环的局部导模功率耦合，并与无环对照、粗网格比较。 |
| 输入 | `config/14_bus_ring_coupler_varfdtd_refined.json` 继承 `config/13_bus_ring_coupler_varfdtd.json`；几何来自 `config/11_ring_physical.json`。 |
| 几何 | 环半径 10、11 μm；波导宽 450 nm、高 220 nm；BOX 2 μm；空气上包层；直波导与环边缘间隙 200 nm。 |
| 数值 | 1545–1555 nm、11 点；耦合区 x=20 nm、y=10 nm；TE 模式；窄带等效折射率。 |
| 范围限制 | 模型只覆盖局部耦合段。未加入掺杂侧翼、金属与完整环；2.5D 结果需最终几何和 3D FDTD 复核。 |

## 工程打开后使用方法

| 工程文件 | 在 MODE 中查看什么 |
|---|---|
| `bus_only_reference_varfdtd.lms` | 选 `bus_guided`，在 `Result View` 展开 `expansion for field → T_forward`，看无环直通导模功率。 |
| `ring1_bus_coupler_varfdtd.lms` | 选 `ring_guided` 看 10 μm 环的 `expansion for field → T_forward`；选 `bus_guided` 看直通导模；选 `coupler_field → E` 看耦合区电场。 |
| `ring2_bus_coupler_varfdtd.lms` | 同上，查看 11 μm 环。 |

在 `Result View` 中对相应结果右键 `Visualize`。导模功率谱的横轴为波长，纵轴为相对输入源功率的功率透射率；如 Visualizer 提供 `Scalar operation`，对功率量 `T_forward` 选 `Re`，对电场分布 `E` 可选 `Abs^2`。查看电场时选 1550 nm 切片并保留 x/y 坐标与色标。

## 可以得到的结果（及截图）

| 校验项 | 原生结果与判断 | 请截图存放 |
|---|---|---|
| 无环基准 | `bus_only_reference_varfdtd.lms → bus_guided → expansion for field → T_forward`；1550 nm 附近约 0.998，确认直波导损耗很小。 | `results/figures/s12_bus_ring_coupler_refined_20261114_205032/01_bus_reference.png` |
| 10 μm 环耦合 | `ring1_bus_coupler_varfdtd.lms → ring_guided → expansion for field → T_forward`；1550 nm 约 0.0168，即约 1.68% 导模功率。 | 同目录 `02_ring1_guided.png` |
| 11 μm 环耦合 | `ring2_bus_coupler_varfdtd.lms → ring_guided → expansion for field → T_forward`；1550 nm 约 0.0188，即约 1.88% 导模功率。 | 同目录 `03_ring2_guided.png` |
| 场分布 | `ring1_bus_coupler_varfdtd.lms → coupler_field → E`，选择 1550 nm；核对场从直波导进入弯曲环，截图应含 x/y 坐标、色标、属性名。 | 同目录 `04_coupler_E_1550nm.png` |
| 模型与数值 | `ring1_bus_coupler_varfdtd.lms` 的 Objects Tree、XY 布局及 `effective_index_map → index`；确认 200 nm 间隙、TE 参考模式位于硅波导。 | 同目录 `05_geometry_and_index.png` |

数值日志位于 `../../logs/s12_bus_ring_coupler_refined_20261114_205032/`。无环直通约 0.998；两只环的直通导模功率约 0.980、0.978。与粗网格相比，环端总通量变化约 1%；这只说明本轮局部网格具有初步稳定性。

本轮输入模式有效折射率约 2.325；此前另一份 FDE 波导截面主模约 2.397。两者的截面建模和求解方法不同，不能把这两个数值视为同一结构的误差比较。

现有 INTERCONNECT 电路用 0.055 功率耦合系数做 Q 拟合。本轮物理局部模型的约 0.017–0.019 与它不同，原因尚不能单凭本轮结果确定；不要直接替换电路参数或宣称复现论文耦合强度。
