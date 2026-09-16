# Team Mode 小队模式

这是Codex专用Skill，使用三个自定义工作角色协调有一定规模的任务。主线程负责未决判断、集成与最终验收；Explorer查证据，Executor实现有明确边界的工作，Reviewer独立检查稳定产物。团队规模由任务决定，简单任务可以不派子Agent。

## 安装与依赖

可以告诉 Agent：“请帮我安装 https://github.com/oil-oil/codex-team-mode”。也可以运行 `npx skills add oil-oil/codex-team-mode`。命令安装需要Node.js/npx；用量诊断使用Python 3.10+标准库，Windows入口为 `py -3`。

Skill与角色配置分开安装。安装范围、角色模型和派发哨兵见[配置说明](references/custom-agents.md)。正常使用不需要额外API密钥，使用宿主已配置的模型服务。当前验证平台为macOS，其他系统未实机验证。

## 使用与边界

请求：“使用 $team-mode 完成这个任务，选择最小有用的小队。”结果是经过主线程验收的统一交付，不要求每次按探索、实现、复审顺序运行。缺少自定义Agent派发能力时由主线程完成；更高模型和更多复审者不保证更高质量。

本地用量脚本默认读取活动与归档日志，不上传日志；模型执行遵循宿主的数据设置。统计输出不证明质量或账户实际费用；`--days` 按本地创建日期筛会话，旧任务续跑用 `--task-id` 或 `--all`。按需运行 `python3 scripts/usage_by_model.py --days 7 --by-agent --json`，真实效果评估见[评估说明](references/evaluation.md)。

源码、测试与完整安装入口见[项目中文说明](https://github.com/oil-oil/codex-team-mode/blob/main/README.zh-CN.md)。
