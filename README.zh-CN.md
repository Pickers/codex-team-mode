<p align="right">
  <a href="./README.md">English</a> · <strong>简体中文</strong>
</p>

<p align="center">
  <img src="./assets/readme/agent-map.webp" width="100%" alt="小队模式把探索、边界执行和独立复审交给不同角色，主线程负责带队、决策与最终验收。">
</p>

`team-mode`（小队模式）是一个负责协调三个工作 Agent 的 Codex Skill，适用于有一定规模的开发、调研、分析、规划、文档、数据和内容任务。主线程保留尚未解决的决策并负责最终验收；子 Agent 负责适合专注上下文、较低成本、安全并行或独立判断的工作。另有一个低成本 `default` 哨兵，专门拒绝任何漏传 `agent_type` 的派发。

它是按任务价值调度的指南，不要求每次走固定流程。

## 三个角色

- **Explorer（探索者）· Luna Medium · 只读**：从当前网页、文档、数据集、代码库、架构、API、日志和配置中查找证据。
- **Executor（执行者）· Luna High · 可写**：在范围、验收标准和安全边界明确后，完成清晰、有边界的工作，也包括有一定规模但边界明确的实现。
- **Reviewer（复审者）· Terra Medium · 只读**：使用全新上下文独立检查稳定的代码、报告、方案、分析、数据和其他产物。

每次派发都必须通过 `agent_type` 显式传入上面三个名称之一。`task_name` 只是标签，`default` 永远不是工作角色。

Luna 以 Medium 完成探索、以 High 完成边界执行；Terra 提供全新且独立的复审，架构决策和最终验收仍留在主线程。

TOML 里的 sandbox 是 profile 默认值，不是绝对隔离边界；父线程的实时权限覆盖可能重新应用到子 Agent。使用任务级 usage 报告核对每个 session 的实际 sandbox。

## 怎么调度

- 当委派、并行、上下文隔离、低成本执行或独立复审有明确价值时，开启小队模式。
- 小队模式也可以不启动任何子 Agent。简单明确的工作由主线程直接完成，不为了补齐流程而调用 Agent。
- 每次派发前先说明它带来的实际收益，并把 brief、检查、等待和返工计入协调成本。明确调用小队模式不代表必须启动子 Agent。
- 每个子 Agent 都要收到包含 `Outcome`、`Benefit`、`Sources`、`Scope`、`Checks`、`Stop when` 和 `Return` 的 dispatch packet；字段不完整或收益不足以覆盖协调成本时，任务留在主线程。
- 当两个或更多互不依赖的切片已经准备好时，优先并行派发。团队规模按任务价值动态调整，不固定 Agent 数量，也没有强制顺序。
- 需要一定范围的只读探索时交给 `Explorer`；主线程可以等待结果，不重复做同样的工作。
- 探索完成后，主线程根据上下文、成本、风险和协调价值，决定自己继续还是委派。
- 架构、验收标准和安全边界明确后，把局部或有一定规模但边界明确的实现交给 `Executor`。全新架构、弱验证或视觉验收、导出器/编译器，以及高后果的安全或回滚判断留在主线程。
- 只有独立判断确实有价值时才使用 `Reviewer`。每次新的 Reviewer 都不继承历史对话，并在 packet 中列出具体未解决风险、精确证据、已通过检查和有边界的停止条件。
- 标准 Team Mode 的所有派发都留在主线程；子 Agent 不再创建后代 Agent。
- 只有互不依赖的工作才并行，同一个共享目标只保留一个写入者。
- 子 Agent 报错或中断后先检查共享产物，再决定是否重试；已有结果可以恢复时不重复执行。
- 主线程检查真实来源、产物、改动和验证结果，再决定是否接受子 Agent 的工作。

普通聊天、简单查询，以及调度成本高于任务本身的工作，留在主线程直接完成。

## 安装

可以把仓库地址交给 Agent：

```text
请帮我安装这个 Skill：https://github.com/oil-oil/codex-team-mode
```

也可以通过命令安装 Skill：

```bash
npx skills add oil-oil/codex-team-mode
```

三个工作 Agent 配置和默认开启的 `default` 派发哨兵与 Skill 分开安装。个人使用时，把 [`agents/`](./agents) 里的四个 TOML 模板复制到 `~/.codex/agents/`；只给单个项目使用时，复制到 `<repository>/.codex/agents/`。onboarding 只在首次配置、Profile 缺失，或用户明确要求修复与验证时运行一次。

准确文件名、安全安装、验证、修复和模型调整都写在[自定义 Agent 配置说明](./skills/team-mode/references/custom-agents.md) 里。如果安装后没有立即显示新的 Agent，可以新建一个 Codex 任务或重启 Codex。

onboarding 完成后，Codex 会主动说明安装了什么，以及怎样只关闭哨兵。关闭操作是把 `default.toml` 可恢复地移出活动 `agents` 目录，三个工作 Profile 会继续保留。

## 使用

任务达到一定规模时，这个 Skill 可以自动触发。你也可以明确调用：

```text
使用 $team-mode 完成这个任务。选择按价值足够的最小小队，互不依赖的切片优先并行，尚未解决的决策和最终验收留在主线程。
```

用户不用逐个指定 Agent。主线程会按任务价值动态选择够用的最小团队，并对汇总后的结果负责。

## 复杂任务与复审人数

三个角色的默认模型保持不变。复杂任务先区分输入、验收、环境和推理问题；主线程保留关键判断，必要时才在宿主支持并验证生效的前提下做单次模型升级，不要求常驻第四个工作角色。

一般变更默认由一名 Reviewer 检查相关风险。代码质量、性能、复用是视角，不是三个人数配额；只有不同风险的证据范围可独立检查、并行确有收益时才增加复审者。最终交接和自动测试通过都不代替真实效果验收。

## 本地用量与验证

用量诊断需要 Python 3.10+，默认读取本地活动和归档会话，只输出聚合与运行元数据，不上传日志。模型处理任务本身仍遵循宿主的模型服务与数据设置。统计会去除可确认的重复计数快照，最终回复与完成事件分别展示；费用使用带日期的固定Standard费率，不是账单或质量分数。`--days` 按本地会话创建日期过滤，并非统计期间所有事件；旧任务续跑用 `--task-id` 或 `--all`。

```bash
python3 skills/team-mode/scripts/usage_by_model.py --days 7 --by-agent --json
python3 -m unittest discover -s tests
```

Windows 可使用 `py -3`；当前在macOS验证，其他操作系统尚未实机验证。安装命令依赖Node.js/npx，核心用量脚本仅用Python标准库；没有子Agent能力时由主线程完成，不宣称小队已运行。

## 自定义

你可以修改 `agents/*.toml` 中的 `model` 和 `model_reasoning_effort`。角色边界建议保留：Explorer 和 Reviewer 只读，修改权限只交给 Executor，新的复审使用全新上下文，最终验收留在主线程。

## 仓库结构

```text
codex-team-mode/
├── agents/                  # 三个工作 Profile 与一个派发哨兵
├── assets/readme/           # README 视觉素材与可编辑源文件
├── skills/team-mode/        # 可以安装的 Skill
│   ├── agents/openai.yaml
│   ├── references/          # Agent 配置与评估方法
│   ├── scripts/usage_by_model.py
│   └── SKILL.md
├── tests/                   # Agent、路由与用量回归测试
├── LICENSE
└── README.md
```

<p align="center">
  <a href="https://github.com/oil-oil/beautify-github-readme"><img src="./assets/readme/made-with-beautify.svg" width="300" alt="README made with beautify-github-readme"></a>
</p>

MIT License
