# 60k 细化上限网格截图核验

工程：`../../runs/20261102_100139_948571/charge_mesh_cap60k.ldev`；日志：`../../logs/20261102_100139_948571/driver.log`。日志确认求解成功、原生数据集存在。均为仿真结果。

| 截图 | 结果项 | 判断 |
|---|---|---|
| [cap60k_iv.png](cap60k_iv.png) | CHARGE:anode `I` 对 0–1 V | 连续递增，约 0–0.67 µA；可作电学基线 |
| [cap60k_Q.png](cap60k_Q.png) | CHARGE:integrated `Q` 对 0–1 V | 连续递增；不是光学 Q |
| [cap60k_E_0V.png](cap60k_E_0V.png) | electrostatics `E`，Magnitude，0 V | 结果项正确，但 0–8×10⁷ 色标和较大 z 范围使目标区域近乎全蓝；不适合检验局部场 |
| [cap60k_E_1V.png](cap60k_E_1V.png) | 同一项，1 V | 同上；与 0 V 图不能有效区分局部变化 |
| [cap60k_Ec_0V.png](cap60k_Ec_0V.png) | bandstructure `Ec`，0 V | 二维导带数据可见，但不是完整能带图 |
| [cap60k_Ec_1V.png](cap60k_Ec_1V.png) | bandstructure `Ec`，1 V | 数据可见；两图色标范围不同，不能直接用颜色比较 |
| [cap60k_T_1V.png](cap60k_T_1V.png) | temperature_monitor `T`，1 V | 中央热点可见；色标只显示“300”，需从原生工程读取实际温升 |

与论文图 2 对比时优先查看后续 s12 的局部电场与完整能带截图。本组电场图视觉失效不等于求解失败。
