# s13 局部耦合系数接入双微环电路对照

## 算例做了什么

| 项目 | 内容 |
|---|---|
| 输入 | s05 已对齐双环电路；s12 两只环的 `ring_guided → T_forward` 原生结果；配置 `config/15_local_coupling_circuit.json`。 |
| 改动 | 在 1549.984 nm 的已保存谱点读取功率耦合：ring1 为 0.01681339，ring2 为 0.01881758；各环的第一、第二总线暂设为相同耦合值。其余电路参数沿用 s05。 |
| 目的 | 比较物理局部耦合估计与 s05 中 Q 拟合值 0.055 对双环透射谱的影响。 |
| 范围 | 这是参数敏感度对照。s12 仅模拟一个局部耦合区；第二总线、完整环、掺杂、金属及热驱动未由本工程验证。 |

## 工程打开后使用方法

| 工程文件 | 操作 |
|---|---|
| `dual_ring_local_coupling_check.icp` | 用 INTERCONNECT 打开；点击 `ring1` 和 `ring2`，在 Property View 展开 Waveguide/Mode 1，查看 `coupling coefficient 1 1` 和 `coupling coefficient 1 2`；在 Result View 打开 `ONA → input 1/2/3 → mode 1 → transmission`。Visualizer 的 `Scalar operation` 选 `Abs^2`。 |

## 可以得到的结果（及截图）

| 结果 | 工程内入口 | 核验重点与建议截图 |
|---|---|---|
| Through（可选） | `ONA → input 1 → mode 1 → transmission` | 对比 s05 的 Through 谱；截图 `01_through.png`。 |
| Drop1（可选） | `ONA → input 2 → mode 1 → transmission` | 对比 s05 的第一环输出；截图 `02_drop1.png`。 |
| Drop2（必需） | `ONA → input 3 → mode 1 → transmission` | 对比 s05 的共同峰波长、峰高和线宽；截图 `03_drop2.png`。 |
| 电路参数（必需） | `ring1`、`ring2` 的两个功率耦合系数 | 截图 `04_parameters.png`，画面含工程标题与 Property View。 |

两份原生工程在 1548–1555 nm 内的 Drop2 主峰对照：

| 工程 | 两环各自的总线功率耦合系数 | Drop2 主峰波长 | 主峰功率透射率 |
|---|---|---:|---:|
| s05 Q 拟合基准 | 均为 0.055 | 1551.709 nm | 0.832 |
| s13 局部耦合参数对照 | ring1：0.01681339；ring2：0.01881758 | 1551.709 nm | 0.574 |

两个工程均有 1520–1600 nm、8001 点的原生 ONA 结果。局部耦合值减小时，模型中共同峰位置不变、峰值降低；这是当前电路参数敏感度，不是实测现象或最终器件定标。s12 的复数模式系数 `a/b` 已保存在 `.lms` 中；本轮 INTERCONNECT 环元件只使用功率耦合参数。

请将手动截图放入 `results/figures/s13_local_coupling_circuit_20261115_205936_021858/`。s05 基准仍在 `results/runs/s05_ring_q_aligned_20261107_105136_874630/dual_ring_static_aligned.icp`。原生输出为仿真数据，不是实测数据。不要把本轮当作已完成的 200 nm 间隙全器件校准。
