# 双微环与 MZI 光学模型

密集单环微调成果：[`s09_ring_detuning_dense_20261107_181841_036966`](results/runs/s09_ring_detuning_dense_20261107_181841_036966/README.md)。11 个原生工程已核验；对齐点的 Drop2 峰值功率透射率约 0.832，偏离对齐后下降。它用于对齐敏感度比较，待用户截图复核。

密集协同调谐成果：[`s08_ring_common_dense_20261107_181503_872760`](results/runs/s08_ring_common_dense_20261107_181503_872760/README.md)。13 个原生工程已核验，Drop2 主峰随共同折射率偏置从 1551.709 nm 连续移动到 1552.829 nm；待用户逐图截图复核。工程 README 给出统一显示范围与截图顺序。

双环协同调谐成果：[`s07_ring_common_tuning_20261107_161037_819605`](results/runs/s07_ring_common_tuning_20261107_161037_819605/README.md)。原生谱线和[三张截图](results/figures/s07/README.md)已核验：共同折射率增量 0、0.001、0.002 时，Drop2 主峰约为 1551.709、1552.085、1552.452 nm。它尚未换算成驱动电压。

单环对齐敏感度成果：[`s06_ring_index_tuning_20261107_160617_463134`](results/runs/s06_ring_index_tuning_20261107_160617_463134/README.md)。原生谱线和[三张截图](results/figures/s06/README.md)已核验：偏离对齐状态时主峰功率大幅下降；截图纵轴尚需统一后才能直接比较峰高。

当前组合光学基准：[`s05_ring_q_aligned_20261107_105136_874630`](results/runs/s05_ring_q_aligned_20261107_105136_874630/README.md)。已合并 Q 校准和静态峰对齐；原生结果和[截图](results/figures/s05/README.md)已核验。

耦合参数校准成果：[`s04_ring_q_fit_20261107_104133_622055`](results/runs/s04_ring_q_fit_20261107_104133_622055/README.md)。原生光谱和[截图](results/figures/s04/README.md)已核验；Q 接近论文报告值，消光比仍有差异。Q 数值来自日志，当前全波段截图不能直接量取。

双微环静态对齐成果：[`s03_dual_ring_align_20261107_005457_051993`](results/runs/s03_dual_ring_align_20261107_005457_051993/README.md)。原生结果已核验，待截图复核；此结果尚不代表已完成电热调谐。

双微环冷态成果：[`s02_dual_ring_cold_20261107_000643_250729`](results/runs/s02_dual_ring_cold_20261107_000643_250729/README.md)。原生光谱和[截图](results/figures/s02/README.md)已核验；约 1524–1525 nm 有共同峰。1550 nm 是本轮模型选定的参考波长，申报书未指定固定的 FBG 中心波长；在该参考波长附近，两环谐振尚未重合。

| 目录 | 内容 |
|---|---|
| `config/` | 截面和 MZI 参数配置 |
| `models/source/` | 接收的原始模型；当前为空 |
| `models/baseline/` | 固定基准模型；当前为空 |
| `scripts/` | MODE 截面建模和 MZI 仿真脚本，见目录内 README |
| `results/runs/` | Lumerical 原生工程，见目录内 README 和各工程文件夹 README |
| `results/logs/` | 运行日志 |

当前推荐成果：[`s01_mzi_ruler_20261106_172434`](results/runs/s01_mzi_ruler_20261106_172434/README.md)。
