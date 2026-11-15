# s11 直波导—微环局部耦合：粗网格

## 算例做了什么

| 项目 | 内容 |
|---|---|
| 目的 | 用 MODE varFDTD 计算 200 nm 间隙处的局部电磁耦合，作为细网格复核的对照。 |
| 输入 | `config/13_bus_ring_coupler_varfdtd.json`；环半径 10、11 μm，波导宽 450 nm、高 220 nm。 |
| 范围 | 1545–1555 nm，共 11 点；网格覆盖耦合区，局部步长 x=40 nm、y=20 nm。 |
| 结构限制 | 耦合区只含直波导、弯曲环和 BOX；没有掺杂侧翼、金属和包层设计。此为局部近似，不代表整环或整机结果。 |

## 工程打开后使用方法

| 工程 | 打开位置与用途 |
|---|---|
| `bus_only_reference_varfdtd.lms` | 在 MODE 打开，用 `bus_reference` 和 `bus_through` 对照无环时的波导传输。 |
| `ring1_bus_coupler_varfdtd.lms` | 在 MODE 打开，查看 10 μm 环。 |
| `ring2_bus_coupler_varfdtd.lms` | 在 MODE 打开，查看 11 μm 环。 |

选中对象后，在左下 `Result View` 展开结果，右键 `Visualize`。`ring_output → T` 是环端总通量；`coupler_field → E` 是耦合区电场；`effective_index_map → index` 用来检查等效折射率分布。

## 可以得到的结果（及截图）

| 校验项 | 位置与判断 |
|---|---|
| 求解状态 | 三个 `.lms` 均有 11 点透射率和电场；日志在 `../../logs/s11_bus_ring_coupler_20261114_204336/`。 |
| 无环对照 | 输入与直通透射率均约 0.999，说明输入主模与监视器设置可用。 |
| 网格复核 | 与 `../s12_bus_ring_coupler_refined_20261114_205032/` 比较环端总通量；细网格结果为本轮推荐查看版本。 |

本目录不需要单独截图；截图要求见 s12 细网格工程 README。
