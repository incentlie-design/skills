# 工作包、分配与预算 v1（skill 0.2.0 可选扩展）

原始 goal、REQ/AC 与任务的 DAG 仍是唯一目标结构。每 goal 一份台账，不另建 agent 平台。一个 TASK 是工作项，一个 assignment 是某次执行分配；agent 是执行者，session 是其所在会话，两者不能用任务标题或 owner 名字替代。所有字段来自明确交接，PM 不调用分派工具。

## 工作目标与 work breakdown

先由原始目标抽取用户结果 REQ，再为每个结果写可观察 AC，包括必要的失败与恢复条件，最后拆出能单独交接和验证的工作包。用 task→子 task 继续拆大项，用 precedes 表达真实前置条件；没有依赖的工作保持可并行。每个任务要能回答：支撑什么 AC、要留下什么产物、何时停止。PM 建议的拆解先标 proposal，不冒称已获批准。

任务可选 work_package 对象；对象一旦出现，以下字段必需：

| 字段 | 含义 |
| --- | --- |
| objective | 这项工作要达成的具体结果 |
| done_when | 该工作包可观察的完成条件；上层 AC 仍单独验证 |
| input_artifacts[] | 输入索引 ID，未知输入先作为缺口记录 |
| output_artifacts[] | 非空预期产物 ID，必须包含在 node.artifacts，才能受证据绑定 |
| write_scope[] | 相对当前 repo 的允许修改路径，不允许逃逸 |
| stop_conditions[] | 非空停止条件，例如预算耗尽、范围变化、必需输入缺失 |

未提供 work_package 的旧节点使用 title 作展示回退，objective_basis=legacy_title_only、done_when=null，并进入 work_package_gaps。不能把这种回退当作完整 WBS。工作目标表 goal_dag 保留原文与约束、REQ、AC、全部任务目标、当前分配与预算。一个任务可支撑多个 AC；通过唯一 TASK/assignment ID 汇总，不能沿每条 AC 路径重复计数。

## management 对象

可选顶层 management 含 schema_version=1、assignments[]、usage[]、deliveries[]；可选 goal_budget 和 decision。缺整个对象时 recording_status=not_recorded；不从旧 owner/session 字段推断实际分配。

assignment 字段：

| 字段 | 含义 |
| --- | --- |
| id / task_id | 稳定分配 ID / 本 goal 中的 TASK ID |
| agent_id / session_id | 明确的执行者及会话 ID；未知用 null，并告警 |
| role | implementation / review / coordination |
| status | proposed / assigned / running / completed / released / cancelled |
| source_id / assigned_at | 来源及带时区的分配时间 |
| expected_artifacts[] | 该分配承诺的索引 ID；artifact.tasks 必须含同一 task，空数组明确未记录 |
| budget_limits | 各计量单位的授权上限；缺省或 null 为未知 |
| reason | released/cancelled 必需，记录移交或取消原因 |

proposed 只是建议，不列入实际使用量汇总；assigned/running 为当前分配。一个叶子工作包同时最多一个活跃 implementation；协作可拆子任务，review/coordination 可另设分配。此规则只校验本地记录，不授予创建 agent 的权限。

已分配的任务/agent/session/role/assigned_at 不能原地改写。转交时把旧分配标 released 并写原因，创建新 ID；completed/released/cancelled 不重新打开。历史交付和消耗属于旧分配，不能随当前 owner 转移。父任务的协调工作可以单独计量，但不得再导入一次已经分摊给子任务的总消耗。

刷新 assignments（新增、状态、承诺资产、预算）或 goal_budget，必须给新的 decision={approved_by, source_id, reason}；该 source_id 必须是本次新增的来源。它记录用户/主 agent 已做出的决定，不证明权限真实，也不是 PM 自批预算。首次接入的已有分配由 source_id 说明来源；不能借“首次接入”伪造真实执行者。

仅分配/预算变化增加 ledger_revision，不使未变实现的测试无故失效；工作目标、完成条件、输入输出、范围改变仍需 artifact_revision 升版和 scope_decision。所有旧记录保留。

## 用量与预算

支持同口径的 tokens、minutes、commands、cost_usd；tokens/commands 为非负整数，minutes/cost_usd 为有限非负数。minutes 是各分配的工作耗时，跨并行执行者相加代表工作量，不是项目墙钟时长。cost_usd 只接收来源明确的美元记录，不推测价格或换汇。预算和用量的口径要写在 source 说明中；来源不可比较时保持未知。

goal_budget={limits, source_id} 保存该 goal 的授权总上限。每个 assignment 的 budget_limits 保存它的授权额度；两者是总额和分配额，不能相加当作总预算。

usage 中每条观测含 id、assignment_id、metric、amount、kind（observed/estimated）、source_id、observed_at。amount 是该分配在该指标上的累计值，不是增量。每 assignment/metric/kind 取最新观测，早先 100、后来 160 只计 160；同时间冲突或 observed 累计回退拒绝，历史观测不能改写。真实计量需要更正时先退回来源，不静默抹去消耗。估算可更新，但永不计入实测消耗。

只有来源与观测都新鲜时，current_used 和 remaining 才有值。未报告、估算而无实测、过期或 partial 的用量不能显示为 0；明确观察到零消耗才可记 0。reported_used 是最后一次实测声明，可在过期后继续展示历史值，并附 freshness；它不是实时计数器。

按任务（含子任务）、agent、session 的汇总均对 assignment ID 去重。只汇总已实际分配的记录；任一明细用量未知时 current_used=null，另给 known_current_usage_subtotal 和 unknown_usage_assignments，不把已知小计当总量。会话总 token 若不能准确归属到任务，不可重复贴到会话内每个 assignment；未归属用量必须在来源/报告中指出，不能宣称预算总览完整。

goal_budget 指标输出：

- current_used：去重的所有实际分配累计消耗，包含已结束/移交的分配。
- remaining_to_goal_limit：goal 上限减当前可核查消耗；缺上限/明细/新鲜来源时为 null。
- active_allocated_limit：assigned/running 分配的授权上限合计；历史额度不算仍可使用。
- active_remaining_allocation：当前分配尚可使用额度，耗尽则按 0 算预留。
- unallocated：goal 剩余减当前预留；负数显示 overallocated。remaining 为负显示 over_budget，为 0 显示 exhausted。

超支/超额分配是管理告警，不自动改变业务任务的 reported status 或原生 goal。PM 按停止条件提出暂停新工作、补齐来源或退回批准人的建议，不自动充值/加预算。按 agent/session 的预算视图没有独立 goal 上限，关注累计用量、当前分配额及各 assignment 的剩余额度。

## 交付资产与查询

deliveries 每条含 id、assignment_id、artifact_id、artifact_revision、sha256、source_id、observed_at。只能交付本分配 expected_artifacts 中的资产；记录只追加。查询核对索引中的当前版本、真实文件 hash、来源新鲜度，展示 current / stale_or_unverified / unreported，文件本身另有 present/missing/changed 等状态。

文件存在不证明是谁产出；没有交付记录就保持 unreported。转交后文件仍在，但新执行者未交付不能继承旧交付。completed 分配若缺当前交付会告警；交付记录本身不代替执行/评审证据，也不令 task/goal 自动完成。

query --agent / --session 可反查分配、资产与预算；两者并用取交集。query --node 给该工作包与子任务的去重汇总；brief 提供 DAG 目标表、agent/session 分配、资产和预算的 Markdown 视图。所有视图保留原目标、来源时间和版本；不存在跨 goal 或跨会话用量的隐式读取。

完整可执行 fixture 见 tests/test_pm.py 的 managed_fixture：两位执行者、共享 AC、产物交付、预算和累计观测。示例数值不代表当前会话实测。新字段为可选兼容扩展，旧消费者若忽略它们只能展示旧功能，不能声称自己完成了分配/预算管理。
