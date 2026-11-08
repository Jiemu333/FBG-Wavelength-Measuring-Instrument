# 论文图 2 截面监视器工程

## `pip_fig2_0to1.ldev`

### 算例做了什么

在 0～1 V 的 CHARGE 工程中加入局部电场、能带和空穴截线监视器，用于复现论文图 2(b–e) 的 0 V/1 V 截面对照。本工程未计算论文图 2(a) 的 0～20 V 全范围 I–V。

### 工程打开后使用方法

在 DEVICE 打开本目录的 `pip_fig2_0to1.ldev`，选 `CHARGE`；在 Result View 双击下表对象，在 Visualizer 中分别选择 `V_anode=0 V` 和 `1 V`，保持 `V_cathode=0 V`。

### 可以得到的结果（及截图）

| 论文图/结果 | 工程内入口 | 核验重点 |
| --- | --- | --- |
| 图 2(b)(c) 电场 | `CHARGE → paper_E_xz → E` | xz 截面，0 V/1 V 同一固定色标；避免顶角尖峰掩盖主体 |
| 图 2(d)(e) 能带 | `CHARGE → paper_bandline → Ec/Ev/Efn/Efp` | 同一 x 截线上的四条曲线；检查截线位于硅 slab |
| 空穴基准 | `CHARGE → paper_holeline → charge → p` | x 截线、单位和 0 V 偏压 |

手动截图存放在 `results/figures/s12_fig2_0to1_20261105_145819_844533/`；具体图名及色标设置见上级 [`README.md`](../README.md)。
