# 跨 skill 交接契约 v1

所有运行绑定 `schema_version=1`、`run_id`、`change_id`、`repo`、`base_commit`、`artifact_revision`。`artifact_revision` 是从 1 开始的正整数，`reviewed_revision` 与它同型；它不是 Git 提交状态或版本字符串。路径相对目标 repo；commit 未形成前只能在 commit 类字段写 `uncommitted`，同时附内容摘要，不能编造 hash，也不能把 `artifact_revision` 写成 `uncommitted`。实际已提交候选仍必须给出真实完整 commit。

## 核心产物

| 产物 | 生产者 | 必需内容 | 消费者 |
| --- | --- | --- | --- |
| change brief / PRD | product-spec-prd | 原始输入、目标、非目标、用户旅程、产品约束、REQ/AC、未知项、风险、指标 | 产品评审/单流水 |
| design | 方案节点 | 基线/历史、替代方案、选定权衡、接口/数据、写入范围、回滚、REQ→设计映射 | 技术评审/实现 |
| tasks | PRD/规划节点 | task_id、依赖、owner、write_scope、输入、输出、AC、预算、停止条件 | 多 agent |
| test-plan | eng-quality-test | AC→case→层级映射、数据/环境、命令/人工步骤、预算、触发、评审结论 | 执行/集成 |
| review | 两类评审/测试方案评审 | 下述 review envelope | 门禁/责任人 |
| candidate | eng-delivery-feature | commit、baseline、scope、AC、review/test evidence、依赖/冲突、回滚 | eng-delivery-release |
| test-report | eng-quality-test | revision、范围、实测 pass/fail/blocked/not_run、证据、缺口、结论 | 候选/集成 |
| integration manifest | eng-delivery-release | 候选 commit 集、依赖顺序、main 基线、冻结 head、验证范围、结论、版本计划 | 集成人 |

## Review envelope

状态固定为 `pass`、`revise`、`blocked`。每条发现含 `id`、`severity`（blocking/major/minor）、`evidence`（文件/章节/行为）、`impact`、`minimal_fix`、`owner`、`acceptance`。每份评审另有 `reviewer`、`reviewed_revision`、`scope`、`findings`、`non_blocking_suggestions`。缺关键证据不能 pass；建议不自动变成实施授权。产品/技术/测试各有判定所有权，不互相替代。

## 任务与状态

任务生命周期 `draft → ready → running → review → done`，任何阶段可以 `blocked`；`cancelled` 保留理由。AC 使用 `AC-001`，任务使用 `TASK-001`，用例使用 `TC-001`，发现使用 `REV-001`。保留映射；编号不代替可观察标准。

范围发生变化时增加 artifact_revision，标记受影响评审与测试为 stale；未受影响项只能有明确影响分析才复用。下游读取来源 revision，不能消费上一版 pass 来放行新版实现。

## 节点交接与预算

节点输入必须含上游产物路径/版本、读写集合、允许动作。输出含 `status`（pass/revise/blocked）、产物路径、证据、未解决问题、下一责任人。每个阶段设置有界重试；重复失败停止回主协调者，不递归创建新流水线。

没有必需输入返回 needs_input/blocked 并列最小缺口；示例数据标为 fixture。`candidate` 表示可进入集成，不表示发布；`integrated` 不表示已部署。mock、dry-run、真实执行必须明确区分。任何远端动作都在单独授权之后。
