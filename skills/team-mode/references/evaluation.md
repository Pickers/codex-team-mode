# Evaluate Team Mode

Read this reference only when the user asks to assess Team Mode's routing, Agent profiles, models, reasoning effort, cost, or practical value.

## Establish The Trial

1. Record the root task ID, repository or artifact baseline, acceptance checks, and installed role-to-model mapping.
2. Verify actual child runtime metadata from local traces: `agent_role`, `model`, `effort`, and effective sandbox. Configuration files alone do not prove runtime selection or isolation.
3. Treat a custom profile's TOML effort as authoritative unless the runtime trace proves an override. Passing `reasoning_effort` to `spawn_agent` does not by itself establish an A/B trial; use isolated CLI sessions or separately configured profiles when comparing effort levels.
4. Choose the smallest useful delegation. Keep a comparable slice in the main thread when the goal includes comparing delegation with direct work.
5. Give different Agents independent slices or one stable writer boundary. Do not create duplicate work solely to produce a benchmark.

## Measure What Happened

Use `python3 scripts/usage_by_model.py --task-id current --by-agent --by-session --json` after the relevant children have finished. Use its per-session time, terminal status, depth, and effective sandbox as trace evidence; continue to judge artifact quality and rework manually. Record:

- artifact correctness and requirement coverage;
- source completeness: whether a `fork_turns="none"` brief named every artifact needed for factual claims, and whether missing context caused placeholders, follow-up, or rework;
- dispatch completeness: whether `Outcome`, `Benefit`, `Sources`, `Scope`, `Checks`, `Stop when`, and `Return` were present before spawning;
- main-thread context avoided;
- briefing, waiting, inspection, and rework cost;
- time to a usable return, including interrupted sessions or sessions that consumed usage without a final report;
- wall-clock effect from useful parallelism;
- uncached input, cached input, output, reasoning output, and estimated Standard credits by session;
- permission or runtime differences from the configured profiles.
- transient failures, nested fan-out, partial shared artifacts, retries, and duplicated review.

Do not treat total input tokens as direct cost without separating cached input. Do not infer causality from daily or all-history aggregates. A child's opinion that its spawn was useful is not primary evidence; judge the returned artifact, the inspection needed, and task-scoped usage.

Likewise, a child recommending another Reviewer does not establish review value. If the main thread cannot provide a complete Reviewer packet with one concrete unresolved risk, exact evidence, passed checks, excluded revalidation, and a bounded stop condition, count the extra Reviewer as avoidable routing rather than mandatory assurance.

`terminal_status=completed` 仅表示完成生命周期事件；`final_report_present` 表示保留日志中有实际最终回复，`last_turn_final_report_present` 表示最后一轮有最终回复。三者都不等于主线程验收通过；较早轮次的回复不能证明中断后的最后一轮已交付。 Inspect interrupted or incomplete sessions before retrying, and record any usage that produced no usable return.

Compare `effective_sandbox` with the configured profile. When a parent live override produces `danger-full-access` for an Explorer or Reviewer, their read-only boundary is instructional rather than OS-enforced; do not count that route as security isolation.

Attribute missing facts before blaming the model. When a child correctly reports that required evidence was not present in a `fork_turns="none"` brief, count the omission as briefing cost; do not treat invented completion as the preferred behavior.

When a child fails, inspect the shared target before counting the attempt as lost or retrying. Record recoverable artifacts separately from the missing final report. Count child-created descendants as part of the initiating route, and flag any fan-out that the parent did not explicitly authorize.

## Interpret The Roles

- Keep `Explorer` on a lower-cost model when it reliably returns compact evidence and prevents noisy discovery from entering the main context. Remove it from short tasks whose sources the main thread must inspect anyway.
- Use `Executor` for both small and substantial bounded work when the main thread has fixed unresolved decisions and deterministic checks exist. Measure whether Luna High enables useful multi-file execution with little rework; do not assume Max is more reliable without completed-return evidence.
- Prefer improving decomposition and launching independent Executor slices in parallel before moving bounded implementation back into the main thread.
- 默认用一名 `Reviewer` 检查当前相关风险；代码质量、性能、复用是检查视角，不要求三个实例。只有证据范围可分离且并行有收益时才分开评估，不能把无发现报告自动判作浪费。

Evaluate an Executor inside the real controlled workflow, including the candidate, main-thread inspection, and bounded repair. Strong main-thread acceptance can close observable implementation gaps cheaply. It cannot reliably compensate for a plausible but product-weaker architecture that passes shallow checks, so keep novel architecture, weak or visual oracles, export/compiler behavior, and high-consequence rollback or security judgment in the main thread.

Prefer changing routing thresholds or brief quality before upgrading every role's model or reasoning effort. Change a profile only when repeated task-scoped evidence shows a role cannot meet its boundary.

## Report The Result

For each spawn, record role, runtime model and effort, purpose, outcome quality, rework, task-scoped usage, and keep/change verdict. Separate confirmed findings from one-off impressions and note that local logs omit unavailable or ephemeral sessions.

## 统计覆盖与决策记录

`--days` 按本地时区的会话创建日期选择会话，并汇总这些会话保留的用量，不是逐事件的日账单。旧任务跨日续跑需要使用 `--task-id` 或 `--all`；不能把最近N天创建的会话用量称作最近N天全部消耗。

历史诊断检查活动与归档目录的覆盖、会话ID去重、累计与增量快照的重复事件。缺少累计计数时，相同的增量也可能来自两次真实请求，不应仅按数值相等删除。计数重置、模型切换和压缩日志需要保留边界与未验证项；固定历史费率不等于当前账户账单。

跨模型或思考档的多行记录属于同一个会话；完成、中断和报告数量先按会话去重。线程总耗时包含复用、等待与空闲，不能相加当作并行墙钟，也不能直接当首次交付延迟。

较大任务在现有交接中记录实现直接通过、小修、重做、输入不足或外部阻塞，以及复审发现的采纳、驳回、重复或待验证。以主线程验收证据评价，不以子Agent自报评价；不要求普通小任务建立额外账本。

长期修改模型时，在外部选型记录中写明生效配置、证据、适用边界及被替代结论，并给旧报告标注失效状态。正式Skill只保留当前规则，不嵌入私人会话或单次评估过程。
