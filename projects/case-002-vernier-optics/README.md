# 双微环与 MZI 光学模型

当前组合光学基准：[`s05_ring_q_aligned_20261107_105136_874630`](results/runs/s05_ring_q_aligned_20261107_105136_874630/README.md)。已合并 Q 校准和静态峰对齐；原生结果已核验，待用户截图复核。

耦合参数校准成果：[`s04_ring_q_fit_20261107_104133_622055`](results/runs/s04_ring_q_fit_20261107_104133_622055/README.md)。原生光谱已核验，待截图复核；Q 接近论文报告值，消光比仍有差异。

双微环静态对齐成果：[`s03_dual_ring_align_20261107_005457_051993`](results/runs/s03_dual_ring_align_20261107_005457_051993/README.md)。原生结果已核验，待截图复核；此结果尚不代表已完成电热调谐。

双微环冷态成果：[`s02_dual_ring_cold_20261107_000643_250729`](results/runs/s02_dual_ring_cold_20261107_000643_250729/README.md)。原生光谱已生成，待截图复核。

| 目录 | 内容 |
|---|---|
| `config/` | 截面和 MZI 参数配置 |
| `models/source/` | 接收的原始模型；当前为空 |
| `models/baseline/` | 固定基准模型；当前为空 |
| `scripts/` | MODE 截面建模和 MZI 仿真脚本，见目录内 README |
| `results/runs/` | Lumerical 原生工程，见目录内 README 和各工程文件夹 README |
| `results/logs/` | 运行日志 |

当前推荐成果：[`s01_mzi_ruler_20261106_172434`](results/runs/s01_mzi_ruler_20261106_172434/README.md)。
