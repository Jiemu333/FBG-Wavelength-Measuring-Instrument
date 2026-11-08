# 输入工程使用说明

`models/` 保存仿真输入。已完成的结果工程见 [`../results/runs/README.md`](../results/runs/README.md)。

## `source/tw_modulator_DEVICE_HEAT_original.ldev`

### 算例做了什么

组员交接的原始截面模型，包含几何、材料、p 区与 p++ 区掺杂、电极及 CHARGE/HEAT 设置；用于核对器件原始配置。本文件是输入原件，不能据此认定后续计算已经完成。

### 工程打开后使用方法

在 DEVICE 用 **File → Open** 打开本文件，对照下方“在输入工程中检查配置”表逐项查看；需修改时先另存副本。

### 可以得到的结果（及截图）

可查看文件内保存的结构、掺杂与边界配置；若已有 Result View 数据，仅代表交接时文件所含内容。后续核验过的求解结果应从 [`../results/runs/`](../results/runs/README.md) 打开。

## `baseline/heater_temperature_fixed.ldev`

### 算例做了什么

以交接工程为基础修正温度监视器设置，作为后续电热计算的固定输入基准；它本身不是一轮新的求解结果。

### 工程打开后使用方法

在 DEVICE 用 **File → Open** 打开本文件，检查 `CHARGE`、`temperature_monitor` 和求解设置；新计算从副本启动。

### 可以得到的结果（及截图）

可核对输入配置和监视器范围。已完成的电流、发热和温度数据在 [`../results/runs/`](../results/runs/README.md) 的对应 `.ldev` 工程中查看。

## 在输入工程中检查配置

| 要核对什么 | 在 DEVICE 中怎么找 |
| --- | --- |
| 硅、氧化层、电极等几何和材料 | **Objects Tree → geometry / materials**；逐个选中对象查看属性窗口 |
| p 区和 p++ 区掺杂 | **Objects Tree → CHARGE → pepi、p implant left/right、p++ left/right**；查看掺杂类型、浓度及作用区域 |
| 电学边界和偏压 | **Objects Tree → CHARGE → boundary conditions**；检查 anode、cathode 及其扫描设置 |
| 温度监视器 | **Objects Tree → CHARGE → temperature_monitor**；检查监视范围与保存设置 |

检查后若要看电流、功率或温度的**已求解数值**，请打开 [`results/runs/`](../results/runs/README.md) 中对应的成功工程。
