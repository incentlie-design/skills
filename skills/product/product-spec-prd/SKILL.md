---
name: product-spec-prd
description: Turn raw product requirements into a bounded PRD, OpenSpec proposal/spec deltas/design and owner-scoped tasks. 用于原始需求澄清、PRD 与验收任务拆解；支持无 CLI 的本地文件流，不实现应用，不替代独立产品或技术评审。
---

# 原始需求到可交接规格

把用户想解决的问题变成最小可评审 change，而不是把一句愿望扩展成整个产品。采用 OpenSpec 的变更文件结构；本项目的产品评审门禁不是 OpenSpec 原生强制流程。

## 输入、权限与输出

- 必需输入：原始诉求/来源、目标用户及场景、目标 repo 与基线、可读材料、文档 write_scope、允许动作。已有产品还需当前相关 spec/行为证据；不能把“没提供”当成“从零开始”。
- 可默认：一个有边界的 change、最小文档规划、无 CLI 手工模式、不执行实现。`change_id` 可提出可读的 kebab-case 候选；业务目标、成功阈值、合规约束、owner 和授权不能擅自默认。
- 缺口：可以先给明确标注假设的 draft；缺用户成功条件、既有行为或会影响范围/方案的决策时返回 `blocked`，附 `needs_input` 和最少问题。owner/write_scope/依赖未定的任务不能标 `ready`。无写入授权只在回复里交付草案。
- 只读：相关原始材料、当前 specs、必要代码/历史与既有设计。写入仅限确认的 change 文档和交接文件；保留现有改动。不得执行应用实现、安装 CLI、改全局配置、创建新 repo、推送、发布或写外部系统。

先读 [公共契约](../../../docs/contracts.md)；准备本地写入时读依赖 [工作区规范](../../engineering/eng-workspace-governance/SKILL.md)。依赖按 repo commit 锁定，不意味着自动安装或调用整条流水线。

默认在目标 repo 的 `openspec/changes/<change_id>/` 交付：

| 文件 | 内容与消费者 | 归属 |
| --- | --- | --- |
| `proposal.md` | 动机、改变、capabilities、影响；供评审者对齐范围 | OpenSpec 默认结构 |
| `specs/<capability-path>/spec.md` | 行为增量、规范性 requirement 和场景；供实现/测试 | OpenSpec 默认结构 |
| `design.md` | 基线、替代方案、选定权衡、接口/数据、风险、回滚与 REQ 映射；供技术评审 | OpenSpec 结构；本项目要求至少简短设计交接 |
| `tasks.md` | 编号 checkbox 与任务分派细节；供协调者/实现者/测试者 | checkbox 为原生格式；任务责任字段为项目扩展 |
| `prd.md` | 原始输入引用、目标/非目标、旅程、REQ/AC、约束、未知项、风险、指标 | 项目扩展，不是 OpenSpec 原生 artifact |
| `handoff.json` | 公共运行绑定、产物路径、证据、未决问题、下一责任人 | 项目扩展，不是 CLI 自动生成的批准 |

路径相对目标 repo，所有产物通过 handoff 绑定同一 `run_id/change_id/base_commit/artifact_revision`。`artifact_revision` 是从 1 开始的正整数，行为/范围修订递增；`reviewed_revision` 与它同型，不使用版本字符串或 `uncommitted`。只有 commit 类字段未形成提交时才能用 `uncommitted`，并附内容摘要，不编 hash。当前事实 `openspec/specs/` 不因提出需求而改变。输出消费者为产品评审、技术评审、测试规划和单 feature 协调者；handoff 的 `pass` 只表示规划产物可交接，不是产品批准或实施授权。

## 工作方法

1. **定界。** 保留原话及出处，分清事实、用户决定、推断、未知项。给出一个用户收益、非目标与最小验收边界。核对旧 spec 和相邻 change，避免重复或冲突。纯技术比较转技术评审；仅审现有 PRD 转产品评审，不创建新 change。
2. **写旅程和 AC。** 对范围内主旅程写入口/前置条件、用户动作、系统反馈、成功结果；再写相关失败、空状态及恢复/退出路径。每条 REQ 对应可观察 AC、输入/期望结果和验证方式。指标没有基线就写未测及采样方式；不要编业务收益，指标采集也不自动授权新增埋点。
3. **写原生产物。** 首次采用 OpenSpec 或遇到版本/格式问题，读 [官方来源与手工适配](references/openspec.md)。proposal capabilities 与 delta 路径对应；spec 描述外部行为，内部实现决策放 design。既有 Requirement 的 MODIFIED 必须包含完整替换块和保留场景；没有原文就停止该项，不猜写。
4. **作最小设计交接。** 只依据已知项目约束选择方案，注明替代项为何不用、数据/接口影响和回滚。若重大未知项会改变任务边界，先回责任人，不把它藏在“后续优化”里。技术可行性仍由技术评审判断。
5. **分解任务。** 保留 `- [ ] 1.1 ...` 原生编号 checkbox，描述中包含可观察完成条件；旁列项目 `task_id`、`owner`、`dependencies`、`write_scope`、输入/输出、AC、预算、停止条件。依赖必须无环且实际存在；外部依赖标负责人和解除条件。共享文件只能有一个 writer，必要时串行；新建任务不是派发 agent 的授权。
6. **交接后停止。** 一次自查 REQ→AC→scenario→task 覆盖、范围和源 revision；最多一次有证据的定向修正。交给独立产品评审者及按需技术评审，不自签通过、不替实现者勾选任务。范围/行为改变要提高 artifact_revision 并将受影响评审/测试标 stale。

只把服务当前目标的必要缺口纳入修复。登录、通知、跨端同步等可选产品改进进入单独建议，注明价值/成本/取舍；没有用户批准不得变成 AC、任务或实施。

## 手工完成与验证边界

无 OpenSpec CLI 时，以 `apply_patch` 在获准目录创建相同 Markdown 文件；无需初始化或伪造 CLI 输出。人工核对结构、capabilities 与场景，以及公共任务字段。若已有 CLI，先核实版本/help 再依来源卡做单 change 验证；CLI 通过只证明其检查范围，不证明 PRD 闭环。

达到可评审且可交接的最小规格即停止；关键未知、冲突、缺权限或超预算输出 `blocked`，证据不足不输出“ready for implementation”。若上游流水线约定每 run 最多 3 次修订，这是预算约束，不把 revision 的正整数类型改成枚举或字符串。默认不 apply、sync、archive，不改变当前事实。

## 例子与行为用例

需要一个具体基线时，读 [完整原始输入](assets/filled-example/raw-input.md) 及其链接的产物。它是已填实的本地待办筛选 fixture，不是真实客户事实、运行日志或应用实现；不要把其中的路径/owner 当作新任务的默认值。`tests/cases.json` 的 fixture 路径均相对本 skill 目录。创建期证据见 [有界验证记录](references/validation.md)。
