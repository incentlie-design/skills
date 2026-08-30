# v1 本地 gate 适配协议

这是 [公共交接契约](../../../../docs/contracts.md) 的一个收窄适配，不修改公共字段语义，也不是原生 ADK graph。代码位于 [共享执行器](../../../../scripts/pipeline.py)，完整 mock 输入可用 `demo feature --show-input` 查看。无需模型、API key、网络或付费服务。

## 公共产物如何进入快照

协调者保留原始文件，在内存或已授权的本地 JSON 中汇总以下字段；不能为了让 gate 通过而改写原 reviewer 的结论。

| 公共产物/字段 | gate 字段 | 适配约束 |
| --- | --- | --- |
| schema_version、run_id、change_id、repo、base_commit、artifact_revision | 顶层同名字段 | schema 为 1；repo 是一致的仓库标识；实际路径由显式 `--repo` 提供 |
| revision / artifact_revision | 顶层及 `nodes.<name>.artifact_revision` | 正整数，从 1 开始；本 run 上限 3 是预算，不是把 revision 改成字符串 |
| 最终实现 commit、候选 baseline | 顶层 `head_commit/base_commit`，输出 `commit/baseline` | 实际模式需 Git 可解析的完整 40/64 位 hash；`uncommitted` 不能生成候选 |
| PRD 原始输入、目标、非目标、旅程、约束、REQ/AC、未知项等 | `nodes.spec.artifacts` 文件引用；AC 另投影到顶层 `ac` | `ac` 是 `{id: "AC-001", criterion: "可观察标准"}` 数组；文件内容仍由产品评审判断 |
| design、test-plan | `nodes.design`、`nodes.test_plan` 的 artifacts | 目标/约束、设计与 AC 映射、环境、步骤和预算保留在原文，不臆造新 P1 格式 |
| 产品/方案/测试计划评审 | `product_review/design_review/test_plan_review.review` | 原 envelope 嵌入 `review`，保留 status、reviewer、reviewed_revision、scope、findings、non_blocking_suggestions |
| 实施产物、范围、owner | `nodes.implementation.artifacts`、顶层 `scope`、节点 `owner` | implementation artifacts 路径集必须等于 scope；实际模式 scope 等于 base→head 的 committed diff |
| 独立代码 review | `nodes.code_review.review` | reviewer 必须等于节点 owner，且不同于实施者和对应产物作者；revision 必须相同 |
| test-report 的 revision、范围、结果、证据、缺口、结论 | `nodes.targeted_test.test_report` | 映射为 revision、scope、results、gaps、conclusion，不能从 test-plan 推导 pass |
| test-report 中 case 状态 | `test_report.results[]` | `{id: "TC-001", ac: ["AC-001"], status: "pass", evidence: [...]}`；支持 pass/fail/blocked/not_run，未知状态阻断 |
| 下游依赖/已知冲突/回滚 | 顶层 dependencies、conflicts、rollback | 前两者为 change_id 数组；无依赖时显式 `[]`，回滚为非空操作计划，不执行 |

P1 文件可能采用 Markdown 或不同 JSON 排版：以上是显式投影，不声称能直接读取其他 skill 的任意报告。公共 review.scope 可是章节范围；gate v1 要求投影为顶层 `scope` 的完整路径数组，原审阅范围仍留在报告中。覆盖不够必须补 review，不能靠改字段扩大签字范围。跨多个 reviewer 的判断可分别保留原文件，但必需 gate 仍需明确责任 reviewer。

`non_blocking_suggestions` 接受字符串或含非空 `suggestion` 的对象数组；对象的 value/cost/tradeoff/decision 等附加字段原样保留并进入快照摘要。它们不会自动成为必做任务。不能为适配执行器而丢弃产品评审的成本、取舍或不采纳决定。

## 节点交接格式

九个节点必须齐全：`spec → design → test_plan → {product_review, design_review, test_plan_review} → implementation → {code_review, targeted_test}`。图中三项评审都读取前三项规划产物；实现读取三项评审。

每个节点均含：

- `status` 为 pass/revise/blocked；`owner`、`next_owner` 为非空身份标识；`artifact_revision` 为当前正整数。
- `artifacts` 与 `evidence` 均为非空 `{path, sha256}` 数组，path 相对目标 repo；真实文件必须存在，字节摘要匹配。报告本身可以作为证据，测试日志应由报告引用；摘要不证明报告中的断言是真的。
- `inputs` 是直接父节点名到 `{artifact_revision, artifacts}` 的映射，必须与来源完全一致。顶层 spec 用 `{}`。
- `read_set` 包含上游 artifact 路径和当前 evidence 路径；`write_set` 限定到自身 artifacts；`allowed_actions` 仅允许 `read/write_local`。评审与测试结果节点是只读观察者：`write_set: []`、`allowed_actions: ["read"]`；它们的报告已由外部执行者生成，gate 不写报告。
- `unresolved_issues` 是字符串数组；pass 必须为空。review 的 blocking/major findings 或未覆盖 AC 的 test-report 同样不能放行。
- `binding` 是整个规范化 feature 快照的 SHA-256，不是某一单文件版本。

这些读写声明用于检查交接一致性，不是权限沙箱，也不会启动动作。test-plan 中的命令、报告中的命令文本、额外 `command` 字段一律是数据；执行器不 eval、不调用 shell，不执行测试命令。

## 冻结与状态机

1. 各责任人先完成产物和判断，协调者按上述映射汇总 `kind: "feature"`、`mode: "actual"` 的完整快照。spec/design/test-plan 的目标与约束由对应 review 确认，程序不做语义审计。
2. 记录所有文件的字节 SHA-256；所有输入引用、scope、身份、状态与 review/test-report 先定稿。暂时省略节点 binding，初版 `retry_history: []`。
3. `fingerprint feature FILE` 输出摘要；其计算覆盖全部顶层字段与节点内容，只排除每个节点的 binding 和顶层 retry_history。把同一个摘要附到每个节点。此步骤是协调者的收集冻结，不代表重新产生或批准 review。
4. 原责任人须确认冻结内容仍在其真实签字范围。仅重算 binding 不等于获得新证据；任一来源/结论变化都应重审受影响内容，再形成全新快照。
5. 用独立记录的 `--base/--head` 调用实际门禁。它顺序检查 DAG，遇到第一个未通过节点或无效字段即停止。只有所有必需节点 pass 才输出 candidate；`trace` 是检查轨迹，不是 agent 执行日志。

实际模式检查：`--repo` 是 Git worktree 根；base/head 是存在的 commit 且 base 是 head 祖先；HEAD 等于固定 head；tracked worktree/index 无变化；committed diff 路径精确等于 scope；implementation 文件摘要还须匹配 head 中的 blob。未跟踪证据允许存在，但必须列入引用；忽略文件不是额外源码写入许可。Git 只运行固定的只读查询，禁用可选索引锁、外部 diff/textconv 与 fsmonitor。

`mode: "mock"` 只在内置 demo 路径允许，实际 CLI 没有 `--allow-mock` 开关。demo 用明确虚构的 hash、身份、报告和测试结果，不代表任何真实实施或验收。

## 有条件回退

门禁不自动循环或改文件；失败交给 next_owner。若确实得到 revise，下一快照将 revision 加 1，并在 `retry_history` 追加：

```json
{
  "from_revision": 1,
  "to_revision": 2,
  "from_snapshot": "前一快照的64位SHA-256",
  "to_snapshot": "修复后快照的64位SHA-256",
  "status": "revise",
  "failed_node": "code_review",
  "reason": "根据 REV-001 修复 AC-001 对应行为",
  "owner": "feature-owner",
  "evidence": [{"path": ".runs/run-1/revision-1-review.json", "sha256": "该证据的64位SHA-256"}]
}
```

示例中的中文摘要占位不是可运行 hash；用 fingerprint/真实文件摘要替换。最多两条，必须连续 1→2→3，摘要相连且不同、证据存在、owner/reason 非空；blocked/unknown 不能作为回退理由。证据归档必须留在原路径且不被修复覆盖。

该无状态 CLI 验证调用者提交的回退账本，不提供签名身份、不可篡改历史或跨新 run 的全局预算执法。协调者负责保存每次输入/输出，禁止清空历史、新建 run 绕过上限；不把 `retry_allowed` 当自动重试指令。

## 首版限制与交接 backlog

- 支持同 repo 中有限、存在的普通文件集合；8 MiB/文件，Python 3.9+。删除、重命名、submodule、复杂交叠/累计依赖 diff 不在验收范围。删除会因文件缺失阻断；重命名不提供识别、证明或自动冲突处理保证，须人工拆分/审查后回到受支持范围。
- 全快照绑定是保守门禁，不是增量 agent 调度器，也不是原生 ADK 实现；不调用模型、不写代码、不运行测试、不安装依赖。
- 真实文件、commit 和摘要一致性可以验证，reviewer 身份、报告真实性、需求完整性不能靠 JSON 自证。仍需独立评审和可信证据来源。
- 本地 Git 关系不等于发布许可；候选仅供下游重新校验。所有合并、push、tag、部署和发布均在执行器之外。
- 集成 backlog：P1 产物适配与六个原始 cases 的独立盲测；必要时再设计签名/持久化账本、删除/重命名支持和受影响证据复用。此版不为了这些扩建平台。
