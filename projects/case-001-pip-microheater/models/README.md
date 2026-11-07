# 输入工程使用说明

`models/` 保存仿真输入。已完成的结果工程见 [`../results/runs/README.md`](../results/runs/README.md)。

| 工程 | 用途 | 使用方法 | 结果在哪里看 |
| --- | --- | --- | --- |
| [`source/tw_modulator_DEVICE_HEAT_original.ldev`](source/tw_modulator_DEVICE_HEAT_original.ldev) | 组员交接原件；核对原始几何、材料、掺杂和边界条件 | 在 DEVICE 中用 **File → Open** 打开，只读对照；要修改时先 **File → Save As** 另存副本 | 这是输入原件，不当作已完成结果。打开后若 **Result View** 有数据，可查看文件内已有数据；已确认的求解结果在 `results/runs/` |
| [`baseline/heater_temperature_fixed.ldev`](baseline/heater_temperature_fixed.ldev) | 修正温度监视器后的固定输入基准 | 用 **File → Open** 检查 `CHARGE`、温度监视器和求解设置；新仿真从副本开始 | 这是输入基准。新仿真结果在 `results/runs/<运行编号>/*.ldev`；本基准文件本身不代表新一轮求解完成 |

## 在输入工程中检查配置

| 要核对什么 | 在 DEVICE 中怎么找 |
| --- | --- |
| 硅、氧化层、电极等几何和材料 | **Objects Tree → geometry / materials**；逐个选中对象查看属性窗口 |
| p 区和 p++ 区掺杂 | **Objects Tree → CHARGE → pepi、p implant left/right、p++ left/right**；查看掺杂类型、浓度及作用区域 |
| 电学边界和偏压 | **Objects Tree → CHARGE → boundary conditions**；检查 anode、cathode 及其扫描设置 |
| 温度监视器 | **Objects Tree → CHARGE → temperature_monitor**；检查监视范围与保存设置 |

检查后若要看电流、功率或温度的**已求解数值**，请打开 [`results/runs/`](../results/runs/README.md) 中对应的成功工程。
