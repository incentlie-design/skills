# Filled 示例：幂等键变化后的增量报告

来源为 [QUALITY-002 原始 fixture](../tests/cases.json)。这是**模拟输入的分类示例**，没有执行库存代码；下列 pass/fail 是 fixture 给出的观测，不是本 skill 的实测验收。命令、时间、真实代码 hash 不存在，明确留 null，不编造。文中 r2/r3 只是场景称呼，revision 字段实际为整数 2/3。

## 共同 envelope

以下每个产物都携带本头；这里仅为阅读合并展示。真实拆分文件时逐份加入。

```yaml
schema_version: 1
run_id: fixture-stock-02
change_id: stock-reserve
repo: fixture://inventory
base_commit: uncommitted
artifact_revision: 3
source_artifacts: [{path: fixture://design/stock-r3, revision: 3}]
subject:
  commit: uncommitted
  content_summary: "fixture: r3 将 reserve 幂等键格式改变；checkout 消费者受影响"
  digest_manifest: null
  environment_fingerprint: null
execution_origin: fixture
stage: feature
read_set: [fixture://design/stock-r3, fixture://logs/r3-unit, fixture://logs/r2-contract]
write_scope: []
allowed_actions: [read_fixture, draft_report]
```

真实运行前必须有可检查 repo、代码/测试/配置摘要和环境指纹；此示例只有内容摘要，不具备真实 candidate 准入资格。

## 1. 方案与用例（补充的场景设计也属 fixture）

目标 AC-001：同一购买请求重复提交只扣一次库存，checkout 不因新键格式重复预占。非目标：平台迁移、压测、部署。

| case / 层级 | 前提、数据与步骤 | 预期断言 | 必需 / owner |
| --- | --- | --- | --- |
| TC-001 unit | 本地隔离库存为 10；两次处理同一 request_id、数量 1 | 库存最终 9，扣减计数 1 | 是 / inventory-dev |
| TC-002 feature | 具备 sandbox；同一个订单重复点击购买 | 第二次返回原预占 ID；不重复扣减 | 是 / feature-owner |
| TC-003 integration | 同一 sandbox；checkout 用新键调用 reserve，模拟响应重试 | 消费者与服务识别同一请求，订单只关联一次预占 | 是 / integration-owner |
| TC-004 smoke | 本地产物可运行；加载 reserve 模块 | 加载成功并可构造处理器 | 是 / inventory-dev |

环境：本地 sandbox 缺失。实际命令尚未提供，CMD-001（TC-001）、CMD-002（TC-002/003）、CMD-003（TC-004）只是**计划槽位**，不可执行。计划要求先从目标 repo 核对测试选择器和副作用。初始预算 3 命令/10 分钟；输入声明剩余预算 0，当前不再运行。integration 因幂等键契约影响 checkout 而触发；release regression 未触发。

## 2. 计划 review（fixture）

```yaml
status: blocked
reviewer: fixture-plan-reviewer
reviewed_revision: 3
scope: fixture://test-plan/stock-r3，AC-001 与 TC-001至004
findings:
  - id: REV-001
    severity: blocking
    evidence: "test-plan#environment: TC-002/003 缺 sandbox；commands 只有槽位"
    impact: 无法验证重复购买及checkout契约，不能把旧版绿灯用于新版
    minimal_fix: 提供本地sandbox、可核对的有界命令及获批剩余预算
    owner: feature-owner
    acceptance: 能定位当前repo/摘要和测试配置，并确认隔离环境可用于TC-002/003
non_blocking_suggestions: []
```

## 3. 增量计划

| case | 旧证据 | r3 影响 | 本轮选择与理由 |
| --- | --- | --- | --- |
| TC-001 | 无 | 幂等计算改变 | 已有 r3 fixture 失败观测，需开发修复；当前不重跑 |
| TC-002 | r2 pass，fixture://logs/r2-contract | 键格式改变直接影响此断言 | 原证据 stale，不复用；当前环境缺失=blocked |
| TC-003 | 无 | checkout 跨边界交互 | 必需，但无 sandbox=blocked |
| TC-004 | 无 | 新产物可加载前提 | 仍必需，预算耗尽未开始=not_run，不得改成非必需 |

## 4. 执行记录（观察转录，不是执行）

```yaml
case_id: TC-001
attempt: 1
execution_origin: fixture
freshness: current
source_revision: 3
subject_digest_before: null
subject_digest_after: null
executor: fixture-observer
command_id: null
cwd: null
command_or_steps: null
started_at: null
ended_at: null
exit_code: 1
observed_assertions: ["duplicate reservation: expected one debit, got two"]
evidence_paths: [fixture://logs/r3-unit]
status: fail
reason: fixture提供断言失败；没有真实执行命令、时间、代码摘要
reuse_analysis: null
```

TC-002 的历史行保留 `source_revision=2/status=pass/freshness=stale/origin=fixture/exit_code=0`，不是 r3 当前行。r3 的 TC-002/003 行为 blocked，TC-004 为 not_run；它们的执行时间/退出码均为 null。

## 5. 最终报告 / handoff（fixture）

```yaml
scope: 模拟stock-r3增量证据；不含真实研发验证、发布或生产环境
plan_review: {path: fixture://plan-review/stock-r3, reviewed_revision: 3, status: blocked}
results:
  - {case_id: TC-001, required: true, status: fail, execution_origin: fixture, freshness: current, evidence: fixture://logs/r3-unit}
  - {case_id: TC-002, required: true, status: blocked, execution_origin: fixture, freshness: current, reason: 缺sandbox且旧证据stale}
  - {case_id: TC-003, required: true, status: blocked, execution_origin: fixture, freshness: current, reason: 缺sandbox}
  - {case_id: TC-004, required: true, status: not_run, execution_origin: fixture, freshness: current, reason: 预算耗尽未开始}
counts:
  required: {pass: 0, fail: 1, blocked: 2, not_run: 1}
  optional: {pass: 0, fail: 0, blocked: 0, not_run: 0}
excluded_evidence: [{case_id: TC-002, source_revision: 2, status: pass, freshness: stale, reason: 幂等键格式已变}]
not_selected: [{layer: release_regression, reason: 非发版且无全回归授权}]
gaps:
  - {owner: inventory-dev, issue: 幂等失败, next_trigger: 最小修复形成新revision}
  - {owner: feature-owner, issue: sandbox/命令/真实摘要/预算缺失, next_trigger: 明确输入与授权后另一次有界执行}
status: revise
conclusion: fixture中已有必需失败，不能交接；仍有环境阻断和未运行项，绝非真实测试通过
handoff:
  status: revise
  artifacts: [fixture://test-plan/stock-r3, fixture://test-report/stock-r3]
  evidence: [fixture://logs/r3-unit, fixture://logs/r2-contract]
  unresolved: [幂等失败, sandbox缺失, 预算耗尽, 缺真实执行与版本摘要]
  next_owner: feature-owner
```

一次报告即停止：不替开发者修幂等逻辑，不索取生产凭据，不因阻断改跑全量。修复后增 revision，并只重验受影响集合；下一责任人另行决策，不自动派发。
