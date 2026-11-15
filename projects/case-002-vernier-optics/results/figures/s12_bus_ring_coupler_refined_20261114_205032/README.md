# s12 局部耦合成果截图核验

| 截图 | 对应原生工程及结果 | 核验依据 | 结论 |
|---|---|---|---|
| `01_bus_reference.png` | `bus_only_reference_varfdtd.lms`：`bus_guided → expansion for field → T_forward` | 图中 1550 nm 约 0.9983；`driver.log` 记录 11 点范围 0.998306–0.998340。 | 无环直波导导模透射率与日志一致。截图未显示结果数据集名称，工程对应关系主要依据布局与日志。 |
| `02_ring1_guided.png` | `ring1_bus_coupler_varfdtd.lms`：`ring_guided → expansion for field → T_forward` | 图中 1550 nm 约 0.0168；日志记录 11 点范围 0.0161872–0.0174635。 | 10 μm 环局部导模功率约 1.68%；与日志一致。 |
| `03_ring2_guided.png` | `ring2_bus_coupler_varfdtd.lms`：`ring_guided → expansion for field → T_forward` | 图中 1550 nm 约 0.0188；日志记录 11 点范围 0.0181187–0.0195447。 | 11 μm 环局部导模功率约 1.88%；与日志一致。 |
| `04_coupler_E_1550nm.png` | `ring1_bus_coupler_varfdtd.lms`：`coupler_field → E` | 图中参数栏显示 `coupler_field:E`、`lambda = 1549.98`（约 1550 nm）、`z = -1.5e-7 m`，且有 XY 坐标与色标；直波导附近场强、环附近较弱。 | 约 1550 nm 的场分布截图通过核验。色标反映此图的场幅值显示，不能直接从颜色读出导模耦合功率。 |
| `05_geometry_and_index.png` | `ring1_bus_coupler_varfdtd.lms`：`effective_index_map → index` | 图中 x/y 坐标及 1–2.83 色标完整；一条直波导与一段弯曲环清楚分开。`driver.log` 记录间隙 200 nm，且原生工程含 `index` 结果。截图未显示数据集名称和工程标题。 | 折射率分布与工程几何相符；可确认两波导未相交。精确 200 nm 间隙以配置及日志为准，不能从截图定量量取。 |

以上均为 Lumerical **仿真结果**，不是实测数据。s12 是局部 2.5D 耦合模型；不代表完整双环光谱、加热调谐或最终器件耦合系数。
