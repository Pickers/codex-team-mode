---
name: team-mode
description: "为复杂开发、研究、文档、数据和内容任务协调职责明确的子 Agent，按需要分配探索、执行与独立评审。当用户需要处理可独立拆分、并行或隔离上下文能改善结果的任务时使用；主 Agent 保留未决判断与最终验收，不用于简单问答和小任务。"
compatibility: Codex 专用，需要支持自定义 Agent 的派发能力；用量诊断需要 Python 3.10+ 和本地会话日志。缺少派发能力时由主线程完成，不宣称已运行小队。
---

# Team Mode

Lead the task in the main thread. Use the smallest useful parallel set of subagents to isolate noisy work, reduce expensive main-agent context, run independent work in parallel, or obtain a fresh review. Do not turn the roles into a mandatory pipeline.

## Dispatch Gate

Every `spawn_agent` call must explicitly pass `agent_type` as exactly one of `Explorer`, `Executor`, or `Reviewer`.

- Never omit `agent_type` and never pass `default`. The `default` profile is a fail-closed dispatch guard, not a working Agent.
- Never use `task_name` to select a profile; it only labels the child thread.
- If the intended custom profile is unavailable, keep the work in the main thread or repair the profiles. Do not silently use a generic child.
- If a child returns the dispatch-guard message or its trace shows `default` / `subagent/unknown`, reject its output and respawn only after selecting the intended custom profile explicitly.

Read [references/custom-agents.md](references/custom-agents.md) only when installing, repairing, or verifying the three working profiles and the `default` guard. The controlled onboarding self-test described there is the only time Team Mode deliberately omits `agent_type`.

## One-Time Onboarding

Do not inspect Agent files, load onboarding instructions, or repeat setup explanations during normal Team Mode routing. Treat the active `spawn_agent.agent_type` choices and descriptions as runtime readiness evidence. When all three working profiles are available and `default` is described as the dispatch guard, skip onboarding without mentioning it.

Only read [references/custom-agents.md](references/custom-agents.md) and start onboarding when a required profile or guard is unavailable, or when the user explicitly asks to install, repair, verify, move, disable, or customize them. Get authorization before writing personal or project configuration.

After a successful setup or repair, tell the user once what was installed, which models are assigned, that the guard affects omitted/default subagent dispatches in its installation scope, when restart or a new task is required, and how to disable or restore only the guard without removing the three working profiles.

## Required Rules

- When this Skill activates, immediately send one brief commentary update in the user's language, prefixed with `👾`. For Chinese, say `👾 已开启小队模式。`; translate naturally for other languages. Announce it once per task, not before every subagent call.
- Activating Team Mode does not require spawning any subagent. Keep genuinely short, single-slice work in the main thread when delegation would cost more than execution.
- For every substantial task, perform a brief decomposition pass before working locally. If two or more slices can finish independently with disjoint write ownership or read-only access, dispatch them together unless briefing and inspection clearly cost more than the saved time.
- 架构、产品、安全、范围与验收决策明确后，在主线程大规模修改前完成执行检查点：找出可隔离所有权、可独立验收的写入切片，交给一个或多个Executor。无法隔离、验收依赖主线程判断或委派没有实际收益时，留在主线程并简述原因。
- Before each spawn, identify one material benefit: useful parallelism, context isolation, lower-cost bounded execution, or independent judgment. Count briefing, inspection, rework, and waiting as coordination cost, but do not use coordination cost as a generic reason to serialize substantial independent work.
- Keep all routing and fan-out in the main thread. Under standard Team Mode, children never spawn descendants; they return evidence, artifacts, or blockers to the parent. Treat an explicit user request for recursive delegation as a separate scope expansion with its own permission, depth, and usage decision.
- 默认使用 `fork_turns="none"`。每次新建 `Reviewer` 前检查派发参数，必须显式为 `none`；不能省略或继承历史。若实际继承了作者上下文，结果只能作为补充检查，不能计作独立复审。
- Keep unresolved user intent, product, editorial, architecture, and safety decisions, plus final acceptance, in the main thread.
- Assign one current writer to every file, shared artifact, interactive session, or mutable-system boundary. Parallel writers in one working tree are encouraged only when ownership is disjoint and stable; tell every writer that others are active and unrelated edits must be preserved. When ownership changes, the main thread must stop the previous writer and state the handoff before the new writer starts.
- Inspect the actual artifacts, sources, diffs, and verification output before accepting delegated work.
- 派发工具拒绝请求时，子 Agent 返回父线程处理，不改用其他角色、后代 Agent 或 CLI 绕过限制。
- If a child errors, times out, or is interrupted, inspect shared artifacts and trace evidence before retrying. Retry a transient failure at most once and only when no usable result exists; otherwise recover in the main thread or re-scope the remaining work.
- Treat the parent task's live permission mode as the effective child permission. Do not infer read-only isolation from TOML alone; use the onboarding or diagnostic verification in the reference when permissions need confirmation.

When the user asks to evaluate Team Mode itself, compare models or reasoning effort, or measure whether delegation was worthwhile, read [references/evaluation.md](references/evaluation.md) before designing the trial.

## Dispatch Contract

Before every spawn, make the brief self-contained with these labeled fields:

- `Outcome`: the independently finishable result the child must return.
- `Benefit`: the material advantage over keeping this slice in the main thread.
- `Sources`: every path, URL, dataset, or raw artifact required for factual work.
- `Scope`: allowed reads or writes, ownership, exclusions, and external-action authority.
- `Checks`: acceptance criteria and validation the child owns.
- `Stop when`: the bounded completion, blocker, or evidence threshold that ends the turn.
- `Return`: the concise report or artifact format expected by the parent.

`Stop when` 必须写出可观察的检查终点、证据范围或阻塞条件，不能只写“完成任务”；简短任务可以用紧凑字段，不必生成额外交接文档。

Do not spawn while `Outcome`, `Benefit`, required `Sources`, `Checks`, or `Stop when` is missing. Keep a slice in the main thread when it is not independently finishable.

并行批次应整体比较墙钟与上下文收益，以及共同说明、等待、检查和返工成本，不逐个孤立否定有价值的并行切片。

For a `Reviewer`, also name one concrete `Unresolved risk`, the exact `Evidence` to inspect, `Checks already passed`, and `Do not repeat`. Ask for findings from that packet first and require a usable partial verdict if the stop condition arrives before exhaustive review.

## Route The Work

- `Explorer`（Luna Medium）: use for non-trivial read-only discovery. Give separate Explorers independent evidence slices and do not repeat their work in the main thread.
- `Executor`（Luna High）: use for both localized and substantial bounded execution after the main thread has fixed unresolved architecture, product, safety, scope, and acceptance decisions. Split independent modules, tests, migrations, documentation, or artifact production across multiple Executors with disjoint ownership.
- Main thread: keep the critical slice when it needs novel architecture, weak or visual verification, export/compiler design, security or rollback judgment, or when a plausible false success would be costly.
- `Reviewer`（Terra Medium）: use fresh read-only context for one concrete unresolved risk. For substantial code changes, use the Simplify review workflow below.

Do not wait for all discovery to finish before dispatching already-bounded independent slices. Let the main thread fix unresolved decisions, then actively look for additional independent execution slices.

## Simplify Review For Substantial Code Changes

产物稳定、针对性检查通过后，对共享接口、状态、持久化、并发、性能敏感路径等有明确回归风险的变更进行独立复审。用户明确要求审查或简化时也执行。文件数量只用于估计范围，不能单独决定是否派发或派几个人。

代码质量、性能、复用是三个检查视角（three independent lenses），不是三个人数名额。默认一名全新 `Reviewer` 检查与当前变更相关的视角；没有相关风险的视角可以说明理由后跳过，无发现也是有效结果。

只有两个或更多风险拥有可分离的证据范围、独立返回条件，且并行有明确收益时，才拆成两到三名 Reviewer。每份任务说明列出具体风险、当前稳定产物或版本、已覆盖范围及禁止重复的检查，不能为填满槽位重复审同一问题。

Reviewer 只报告按严重度排序、有证据的发现和最小修复方向；不编辑、不格式化、不提交，也不重跑已通过的广泛验证。主线程核实并去重，在现有交接中说明采纳、驳回及理由或待验证，不为小任务额外建报表。只对接受的必要修复重跑相关检查，避免扩成重构。

## 复杂任务与模型升级

保留三个工作角色，不按模型强弱新增常驻角色。主线程先区分输入缺失、验收不足、环境阻塞与推理难度；前面三类不能靠升级模型代替解决。

`Executor` 在证据与验收明确、完成一次有边界的修复后仍无法满足同一要求，或任务开始前已明确存在高后果判断时，主线程接管关键部分。仍有可靠验收的独立切片，可以评估单次更强模型执行；未决架构、安全和最终验收继续留在主线程。

只有宿主支持且实际运行记录已验证单次覆盖生效时，才对原角色使用可用的更强模型或更高思考档，并说明剩余风险、预期收益和停止条件。不能假定 `spawn_agent` 参数能覆盖固定 profile，也不能把更高思考档当作质量保证。覆盖不可用时留在主线程，不绕过派发限制另起 CLI，不自动修改全局配置。

只有同类任务反复证明默认角色不足，才按授权修改长期 profile；模型不可用、需要改安装配置或验证实际模型时，读取 [配置与定制说明](references/custom-agents.md)。每次长期调整同时记录生效配置、依据及替代的旧结论，避免报告与运行配置分离。

## Coordinate The Work

- Start with the smallest useful parallel batch, not automatically one Agent. Parallelize genuinely independent exploration, analysis, tests, triage, production, or review; do not duplicate work merely to keep Agents occupied.
- For coding tasks, explicitly test these split points before choosing serial work: independent modules, implementation versus tests, code versus documentation, separate platform targets, and separate verification surfaces.
- Before execution, state plainly what the result should be, what may be touched, what must remain unchanged, and how completion will be checked. Revise these requirements if new evidence conflicts with them.
- Verify in proportion to risk. Use independent review for complex, consequential, or difficult-to-check results rather than for every task.
- Reuse passed checks as evidence. Do not ask another Agent to repeat broad validation unless the integrity or relevance of those checks is itself the unresolved risk.

When a task depends on live UI, browser, device, or other interactive state that code inspection and automated checks cannot prove reliably, read [references/interactive-testing.md](references/interactive-testing.md). Do not load it for tasks that can be verified from code.

## Context And Reuse

- Give each new subagent a compact, self-contained brief containing only the objective, relevant sources or paths, scope, authority, exclusions, intended result, required checks, and return format. Never copy credentials into it.
- With `fork_turns="none"`, assume the child knows nothing from the parent conversation. Name every source artifact required for factual claims; if a source is missing, either provide its path, narrow the child to collecting that evidence, or keep the source-dependent slice in the main thread.
- Reuse an existing Explorer or executor when new work belongs to the same task, topic, business area, subsystem, artifact, or workstream and its prior context remains useful. Send only the new objective and changed constraints.
- Start fresh when prior context is stale or noisy, the role or authority changes, or independent judgment matters.
- Reuse a Reviewer only to clarify its existing report. Use a fresh Reviewer for a new review or for checking revised work.
- Do not give an Explorer an expected conclusion. Do not tell a Reviewer the prior debate, author, suspected findings, or desired verdict.

## Handle Findings

- Validate findings against the underlying sources, artifact, and intended outcome before acting.
- Let the main thread apply accepted repairs directly or delegate them according to scope, context, cost, and risk.
- When the risk assessment calls for independent review after consequential repairs, use a fresh Reviewer with only the updated artifact and neutral requirements.
- If a Reviewer crosses its `Stop when` condition without a usable return, request a partial verdict once, then interrupt it. Inspect the trace and existing evidence; do not automatically start another Reviewer.

## Inspect Local Usage

用户询问模型或子 Agent 消耗时，运行 `python3 scripts/usage_by_model.py`；这是按需诊断，不是每次调度的前置步骤。

- 当前任务使用 `--task-id current --by-agent --by-session`；历史使用 `--days N` 或 `--all`，结构化结果加 `--json`。`--days` 按本地创建日期筛会话，不是逐日账单；旧任务续跑用 `--task-id` 或 `--all`。默认包含活动和归档日志；显式自定义根目录按脚本参数处理。
- 同时报告 processed tokens、未缓存输入、缓存输入、输出、其中推理输出及估算 credits。Processed=输入+输出；缓存属于输入，推理属于输出，不能重复相加。
- 按模型和token类型使用随附费率，标注费率日期与Standard假设。未知模型的费用留空并说明缺口，不给统一credits/token兑换比例。
- 区分完成事件、实际最终回复与主线程验收；前两项都不能证明产物成功。检查覆盖范围、重复计数诊断、中断及可恢复文件，不直接把跨模型段的行数当会话数。
- 本地日志不含临时或不可用远端会话，未识别的Fast用量不在估算内；账户限额以 Codex `/usage` 为准。

## Guardrails

- Preserve unrelated user work and obey applicable project, domain, and tool instructions.
- Delegation does not expand authority. Do not commit, publish, deploy, send messages, change external state, or handle sensitive data beyond the user's request.
- For current or factual research, prefer primary sources, record relevant dates, cite evidence, and distinguish fact from inference.
- Keep private-data exploration narrow and return only the minimum evidence needed.
- Resolve conflicting claims against the strongest available evidence and return one coherent result to the user.
