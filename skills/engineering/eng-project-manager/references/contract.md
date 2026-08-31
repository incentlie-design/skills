# PM 本地契约 v1

此格式由本 skill 定义，不是 Codex 原生 goal 或 task API。源码中的 validate 为可执行字段校验；完整实例可由 [fixture 工厂](../tests/test_pm.py) 生成。所有 JSON 使用 UTF-8。

## 快照

| 字段 | 语义 |
| --- | --- |
| schema_version | 固定 1 |
| run_id / change_id / repo / base_commit / artifact_revision / content_summary | 公共 envelope；repo 是当前产物根目录的绝对路径，base_commit 为真实 40 位 hash 或 uncommitted，revision 为正整数。PM 不猜 commit；uncommitted 必须有内容摘要 |
| project_id / goal_id / main_task_id | 三个不同概念，不能互换；与 repo、mode 一起构成台账固定身份 |
| mode | real 或 fixture；fixture 永不升级为 real |
| goal | node_id、original_text、constraints[]、source_id、identity_note；整个对象在刷新时不可修改 |
| source_id / sources[] | 当前主快照来源 ID / 不可覆盖的来源历史 |
| nodes[] / edges[] | 分解及依赖 DAG |
| artifacts[] / evidence[] | 文件索引 / 不可覆盖的观测证据 |
| alignment（可选） | status=aligned/drift/unreviewed、artifact_revision、source_id、note；需实际读原文做语义核对，不能以脚本自动签字 |
| scope_decision（修订拆解时必需） | approved_by、source_id、reason、artifact_revision；这是显式决策的记录，不是脚本能验证的权限凭证 |

每个 source 含 id、kind=goal_tool/task_tool/handoff/file/fixture、locator、source_revision（非空字符串，如导出版本或返回 cursor）、session_id、observed_at（带时区 ISO 时间）、completeness=complete/partial。source_revision 是来源自己的版本标记，不是 artifact_revision。没有源时钟则保守写实际能确定的导出时间，并标 partial；不能刷新旧来源的时间。

每个 node 含 id、kind=goal/requirement/acceptance/task、title（REQ 是要求，AC 是可观察验收标准）、owner/session_id（未知为 null）、status、source_id、artifacts[]。status 沿用公共 draft/ready/running/review/done/blocked/cancelled，后两者需 reason；这是主 agent 报告或来源快照的状态，不是 PM 的验证判定。额外说明可用 note（包括 proposal/未批准拆解）。

边是 {from, to, type}：

- decomposes：goal→requirement→acceptance→task，或 task→子 task；允许一个任务服务多个 AC。
- precedes：前置 task→后续 task。不要写成 dependent→prerequisite，也不要当作需求分解边。

所有边端点存在、ID 唯一、无自环/重边，组合图必须无环；完成求值时 child→parent 加 prerequisite→dependent 也须无环，避免“父任务依赖自己的子任务，同时子任务等父任务完成”的死锁。缺分解/孤立节点保留为 gap，不静默补齐。Mermaid 用内部安全 ID，实线与虚线区分边类型。

## 产物与证据

artifact 字段：id、category（product_docs/technical_docs/requirements/issues）、path（相对 repo，未知为 null）、role（subject/evidence/reference）、owner、requirements[]、tasks[]、artifact_revision、sha256（未取得为 null）。

只索引原文件，不复制正文、不强制目录搬迁。绝对路径、.. 和逃出 repo 的 symlink 拒绝读取。目录或文件不存在→missing；null→unlocated；无预期 hash→unhashed；hash 不同→changed；16 MiB 以上→unverified_large；读取错误→unreadable。大型证据需经授权做小型、可核对来源的摘要，不能把未 hash 文件当通过。索引 JSON 包含 resolved_path、actual_sha256、evidence_ids；Markdown 是便于阅读的投影。

evidence 字段：

- id、nodes[]、artifact_revision、source_id、observed_at、result=pass/fail/blocked/not_run、kind=execution/review/fixture。
- bindings 是 artifact ID→当时真实 SHA256；必须覆盖每个被验证 task/AC 的全部 node.artifacts，且至少一个 subject，才有完成依据。PM 应把足以代表验收范围的业务文件/文档列入节点，而不是挑一个无关小文件凑 hash。
- record_artifact 是 role=evidence 的索引 ID，record_sha256 是当时报告文件 hash；not_run/blocked 可以为 null（此时 record_sha256 也用 null）。

验证先核 revision、来源与观测时间，再核所有绑定文件及报告的实际内容 hash。每个节点选择最新观测，同时间 fail 优先于 blocked、not_run、pass，防止挑旧绿灯。旧观测全部保留。execution/review 是来源声明，脚本不会执行测试或理解报告的断言，PM 必须实际核对其覆盖、结果、作者及独立性。未执行不可记 execution pass。

有效 task/AC 完成需要 reported done + 当前 pass + 完整文件绑定 + 前置/子节点闭合。REQ/goal 由子项汇总，不凭自身 reported done 放行。source partial/stale/future、alignment 非同版已复核或任一 gap 都禁止整体 verified_complete。fixture 只能 simulated_complete。取消的要求不会被自动算成成功，需要显式范围决策和主 agent 对原始目标的重新判断；脚本保守保留 incomplete。

## revision、对账与历史

- artifact_revision 对应当前实现/验收范围；plan、subject 内容/路径/绑定、base_commit 改变必须升版。不改实现的状态/来源/证据更新可以保留同一 artifact_revision。
- ledger_revision 是每次成功导入的序号，与 artifact_revision 分离。来源和证据只追加新 ID；节点和索引 ID 不能删除，任务可保留 cancelled。原始 goal 不变。
- 拆解/边/title/artifacts 映射修改及取消需要同版 scope_decision；未批准的建议留在管理报告，不加入主计划。scope_decision 只能记录已存在的具体授权，不由 PM 自签授权。
- 每个历史条目存完整 snapshot、event{id, recorded_at, reason, source_id}、previous_hash、hash。重复相同 event ID 与内容返回 unchanged；内容冲突或 expected-revision 过时则拒绝且不改台账。
- 同目录排他锁和原子替换防止并发丢更新/半写。锁已存在时先检查实际 writer，不自动删除锁。hash 链能检出意外修改，不能抵抗有人重写整个链；需要防恶意篡改时用组织认可的签名/存储，本版不做平台化扩展。
- 来源/证据新鲜度默认 24 小时，调用者可披露参数。query 的 --at 是历史重放并输出 historical_replay=true，不能把指定旧时间的结果当实时结果。
- 只允许一个目标 repo 根；跨 repo 依赖通过有来源的交接/索引摘要纳入，未读取部分标 gap，不扩大本地路径白名单。迁移 worktree 时新建明确关联原台账的接入快照，不能偷换旧台账身份。

接口消费者是 PM/主 agent 和用户，脚本没有 tool handler、外部执行、调度或 goal 修改接口。退回 needs_input（exit 2）表示输入/状态问题；query exit 0 只表示查询完成，必须看 goal_status，不能当验收通过。
