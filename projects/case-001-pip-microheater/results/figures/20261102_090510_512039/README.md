# 中等网格截图核验

工程：`../../runs/20261102_090510_512039/charge_mesh_medium.ldev`；日志：`../../logs/20261102_090510_512039/charge_mesh_medium_p0.log`。求解成功，但日志提示自动细化达到上限。均为仿真结果。

| 截图 | 结果项 | 判断 |
|---|---|---|
| [medium_iv.png](medium_iv.png) | CHARGE:anode `I` 对 0–1 V，阴极 0 V | 曲线连续，约 0–0.67 µA；可作网格对照 |
| [medium_Q.png](medium_Q.png) | CHARGE:integrated `Q` 对 0–1 V | 曲线连续递增；是积分电荷，不是光学 Q |
| [medium_T_1V.png](medium_T_1V.png) | temperature_monitor `T`，1 V | 中央热点可见；色标刻度均显示为 300，不能据图判断温升大小 |

此组仅证明对应结果项存在；网格收敛需要和其他网格的原生数值定量比较，不能只凭曲线形状判断。
