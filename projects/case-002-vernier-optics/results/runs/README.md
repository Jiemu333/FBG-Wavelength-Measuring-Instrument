# 原生工程索引

`.icp` 用 Lumerical INTERCONNECT 打开，`.lms` 用 MODE 打开。工程内结果入口、截图清单见各运行目录 README；截图核验结论见 `../figures/` 下相应目录。以下均为仿真结果。

| 工程目录 | 状态与用途 | 查看说明 |
|---|---|---|
| [s12 细网格局部耦合](s12_bus_ring_coupler_refined_20261114_205032/README.md) | 3 个 MODE varFDTD 原生工程完成；导模功率、场和无环对照已核验，待用户截图 | 打开 `ring1_bus_coupler_varfdtd.lms`、`ring2_bus_coupler_varfdtd.lms`，看 `ring_guided → expansion for field → T_forward`；截图清单见该目录 README |
| [s11 粗网格局部耦合](s11_bus_ring_coupler_20261114_204336/README.md) | 3 个 MODE varFDTD 工程完成，用于网格对照 | 打开 `ring*_bus_coupler_varfdtd.lms`，看 `ring_output → T`；细网格为推荐版本 |
| [s10 双环物理几何与弯曲模式](s10_ring_physical_20261114_192733/README.md) | MODE 几何及 3 个 FDE 工程已生成并核对模式数值；待截图复核 | 打开 `dual_ring_physical_layout.lms` 看错位双环和三总线；打开两个 `ring*_bent_mode.lms` 看模式场与有效折射率 |
| [s09 单环密集失谐](s09_ring_detuning_dense_20261107_181841_036966/README.md) | 11 个原生工程已核验；待截图 | 对齐敏感度，Drop2 峰值功率变化 |
| [s08 双环密集共同偏置](s08_ring_common_dense_20261107_181503_872760/README.md) | 13 个原生工程已核验；待截图 | Drop2 主峰连续移动 |
| [s07 双环共同偏置](s07_ring_common_tuning_20261107_161037_819605/README.md) | 原生工程及三张截图已核验 | 三个偏置点的 Drop2 谱；[截图结论](../figures/s07/README.md) |
| [s06 单环失谐](s06_ring_index_tuning_20261107_160617_463134/README.md) | 原生工程及三张截图已核验；需统一纵轴补截图 | 三个比例的 Drop2 谱；[截图结论](../figures/s06/README.md) |
| [s05 Q 校准加静态对齐](s05_ring_q_aligned_20261107_105136_874630/README.md) | 原生工程及截图已核验 | 打开 `dual_ring_static_aligned.icp`；[截图结论](../figures/s05/README.md) |
| [s04 Q 校准](s04_ring_q_fit_20261107_104133_622055/README.md) | 原生工程及截图已核验 | 打开 `dual_ring_q_calibrated.icp`；[截图结论](../figures/s04/README.md) |
| [s03 静态对齐](s03_dual_ring_align_20261107_005457_051993/README.md) | 原生工程及截图已核验 | 打开 `dual_ring_static_aligned.icp`；[截图结论](../figures/s03/README.md) |
| [s02 双环冷态](s02_dual_ring_cold_20261107_000643_250729/README.md) | 原生工程及截图已核验 | 打开 `dual_ring_cold.icp`；[截图结论](../figures/s02/README.md) |
| [s01 MZI 标尺](s01_mzi_ruler_20261106_172434/README.md) | 原生工程及截图已核验；100 µm 透射图运算待统一 | 50/100 µm 臂长差；[截图结论](../figures/s01_mzi_ruler_20261106_172434/README.md) |

`s01_mzi_ruler_20261106_172434` 是唯一保留的 MZI 标尺运行目录，含 MODE 波导工程和两种臂长差的 INTERCONNECT 工程。
| [s14 示范光栅接入双环](s14_fbg_ring_link_20261115_212148/README.md) | 使用软件内置 Bragg 光栅示范参数的纯光学连接算例；并非实际 FBG 模型 | 打开 `fbg_reflection_dual_ring.icp`；`ONA input 4` 看示范反射，`input 3` 看双环 Drop2 |
