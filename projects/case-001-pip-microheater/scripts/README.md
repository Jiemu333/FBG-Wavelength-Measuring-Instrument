# 论文图 2 与图 3(a–d) 脚本说明

论文：Zhou 等，*Tunable Vernier Microring Optical Filters With p-i-p-Type Microheaters*，IEEE Photonics Journal 5(4), 2013，图 2、图 3。脚本只使用本案例已有的二维 CHARGE 工程；生成的数值留在 Lumerical 原生 .ldev 中，不生成表格或图片。

| 配置 | 功能 | 输入 | 输出 |
| --- | --- | --- | --- |
| [fig2_0to1.json](../config/fig2_0to1.json) | 重新计算 0～1 V，增加局部电场、硅 slab 水平能带和空穴截线监视器；用于图 2(b–e) | [已完成的 s03 工程](../results/runs/s03_mesh_cap60k_20261102_100139/charge_mesh_cap60k.ldev) | 新的 `results/runs/s12_fig2_0to1_<时间>/pip_fig2_0to1.ldev` |
| [fig23_0to20.json](../config/fig23_0to20.json) | 尝试 0～20 V CHARGE 电热扫描；保存图 2(a) 与图 3(a–d) 所需原生数据 | 同一只读 s03 工程 | 新的 `results/runs/s17_fig23_0to20_<时间>/pip_fig23_0to20.ldev` |

两个任务各自复制源工程，输出目录独立。可以在两个终端分别启动；同时求解会占用更多内存与许可证。如果高压任务未覆盖配置要求的 0、1、10、20 V 点，脚本返回 `SIM_DONE_STATUS=1`，不把输出标为完成成果。

## 复现命令

脚本已由 Codex 按本案例工作流程执行和核验。日后需要复现时，在 PowerShell 中执行对应命令：

```powershell
Set-Location 'D:\SRTP_Work'
python '.\projects\case-001-pip-microheater\scripts\12_pip_figures_charge.py' --plan fig2_0to1
```

```powershell
Set-Location 'D:\SRTP_Work'
python '.\projects\case-001-pip-microheater\scripts\12_pip_figures_charge.py' --plan fig23_0to20
```

终端先显示脚本功能表，再显示运行编号、工程路径和状态标志。**只有 `SIM_DONE_STATUS=0` 且在 DEVICE 中能看到目标偏压及数据集，才算完成。**脚本不会在终端打印仿真数值。

各论文图要打开哪个工程、如何在工程内查看结果，以及用户截图清单，见 [`../../results/runs/README.md`](../results/runs/README.md)。

## 输入设置与边界

| 项目 | 当前设置及核验 |
| --- | --- |
| slab 截线 | `x=-4.5～4.5 µm, z=0.03 µm`；对应论文 60 nm slab 的中间高度。首次打开工程时核对它确实穿过硅 slab |
| 局部电场监视器 | `x` 跨度 9 µm、`z` 跨度 0.30 µm；用于避免原全域图中的结区被压成细线 |
| 高压收敛控制 | 配置文件给出步长、回退下限、迭代上限和混合方式；仅是求解输入，**不保证** 20 V 收敛 |
| 论文器件参数 | 波导宽 0.45 µm、高 220 nm、slab 60 nm、重 p 掺杂约 10²⁰ cm⁻³、波导轻 p 掺杂约 10¹⁵ cm⁻³、重掺杂区距波导约 0.6 µm、载流子寿命 100 ns。现有工程的几何、掺杂、材料和边界需逐项核对，脚本不擅自改写 |
