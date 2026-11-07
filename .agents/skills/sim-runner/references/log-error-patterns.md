# Lumerical 日志判读速查

| 日志原文或标志 | 含义 | 下一步 |
| --- | --- | --- |
| `Simulation completed successfully` | 求解器已结束；尚不能证明结果字段齐全或物理模型正确 | 打开 `.ldev`，核对所需结果和用户截图 |
| `Refinement limit exceeded for auto-refinement` | 网格有效，但可能细化不足 | 记录警告；后续用加密网格比较敏感结果 |
| `Simulation failed` 或异常 | 运行未正常结束 | 保留完整日志，查找第一个具体错误及相关设置、许可证状态 |
| `SIM_DONE_STATUS=0` | 驱动脚本以成功状态结束 | 仍须检查求解日志与 `.ldev` 结果 |
| `SIM_DONE_STATUS` 为非零值 | 驱动脚本失败 | 查看 `results/logs/<运行编号>/driver.log` 和求解器日志 |

不能仅凭日志文件或工程文件存在就认定仿真成功。
