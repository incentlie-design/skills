# 测试产物模板

字段遵循 [公共契约](../../../../docs/contracts.md)。以下是填写模板，不是已执行记录；替换字段后才交接。业务产物在授权目标 repo，路径均相对它；公共 envelope 放入每个独立产物，不只放首页。内嵌 review 也要能追溯其父 envelope。

## 0. 公共头与对象绑定

```yaml
schema_version: 1
run_id: 填本次运行ID
change_id: 填变更ID
repo: 填可定位的目标repo
base_commit: 填实际基线commit
artifact_revision: 1 # 从1开始的正整数，修订时递增；不是commit状态
source_artifacts:
  - path: 填PRD或design路径
    revision: 1 # 替换为来源产物的正整数revision
subject:
  commit: 填实际HEAD或uncommitted
  content_summary: 填变更内容摘要
  digest_manifest: 填实际SHA-256清单路径（含测试/配置/新增/删除）
  environment_fingerprint: 填运行时/配置/数据版本；不含秘密
stage: development / feature / integration / release（选一个）
read_set: []
write_scope: []
allowed_actions: []
```

没有真实 commit 时只在 commit 类字段保留 `uncommitted` 并附内容摘要；revision 字段保持正整数。没有可核验内容清单/环境就注明缺口，不能交真实通过报告。fixture 用 `execution_origin: fixture`，不得提供看似真实的编造 hash。

## 1. test-plan

```yaml
# 加公共头
goal: 填本阶段目标
non_goals: []
impact: [{path_or_contract: 填路径, change: 填语义变化, consumers: []}]
ac_case_map:
  - ac: AC-001
    case_id: TC-001
    layer: unit
    required: true
    risk: 填覆盖风险或smoke前提
environment: {requirements: [], availability_evidence: [], data: [], cleanup_scope: []}
commands_or_steps:
  - id: CMD-001
    cwd: 填相对repo目录
    source: 填真实测试配置路径/章节
    invocation: 填核对过的有界命令或人工步骤
    cases: [TC-001]
    expected_discovery: 填预期用例/断言识别方式，拒绝零测试误报
    timeout_seconds: 300
    side_effects: []
budget: {max_commands: 3, max_minutes: 10, max_command_minutes: 5, max_fix_rounds: 2}
triggers: {integration: 填具体边界或未触发理由, release_regression: 填授权/流程或未触发}
owners: {developer: 填owner, executor: 填owner, plan_reviewer: 填独立owner, gate_owner: 填owner}
review: 填同revision计划评审路径
stop_conditions: [必需输入或权限缺失, 预算耗尽, 确定性失败无改动, 当前阶段验收满足]
```

## 2. 测试方案 review

```yaml
# 加公共头；scope 限定测试方案，不替技术方案/产品评审
status: pass / revise / blocked（选一个）
reviewer: 填独立评审者
reviewed_revision: 1 # 替换为被评计划的正整数artifact_revision
scope: 填计划路径、版本、AC和边界
findings:
  - id: REV-001
    severity: blocking / major / minor（选一个）
    evidence: 填文件/章节/具体缺口或行为
    impact: 填影响的AC或风险
    minimal_fix: 填足够解除问题的最小改变
    owner: 填责任人
    acceptance: 填可观察解除条件
non_blocking_suggestions: []
```

无发现时 `findings: []`；缺评审者/输入不能借模板里的 pass 值放行。

## 3. 用例卡（每个 TC 一张）

```yaml
# 加公共头，或嵌于具有公共头的用例集合
id: TC-001
ac: [AC-001]
risk: 填错误如何影响验收
layer: unit / smoke / feature / integration / release_regression（选一个）
required: true
preconditions: []
data: 填隔离数据/fixture版本
steps: []
expected: [] # 具体输出/状态/错误/不发生的副作用，不能只写“正常”
command_id: CMD-001
cleanup: 填授权隔离目录内的恢复动作；没有则写无
owner: 填执行者
```

## 4. 增量计划 / delta

| case_id / AC | 原版本和结果证据 | 本次变化 | 选择：run/reuse/defer | 本阶段必需？ | 依据 / owner / 下一触发 |
| --- | --- | --- | --- | --- | --- |
| TC-001 / AC-001 | 填来源revision或无 | 填改变的函数/契约/数据 | run | 是 | 填理由 |
| TC-002 / AC-002 | 填原始日志及摘要 | 填明确不受影响的依据 | reuse | 是 | 填依赖/环境一致性和审核人 |

`defer` 只允许非必需项；必需项未执行仍留在报告且阻断。复用时不能把原命令时间写成当前时间。新旧候选变化同时记录 `frozen_head` 与候选 commit 集。

## 5. 执行记录

```yaml
# 加公共头，每次尝试保留一条，不覆盖旧失败
case_id: TC-001
attempt: 1
execution_origin: executed / reused / fixture / planned（选一个）
freshness: current / stale（选一个）
source_revision: 1 # 替换为实际被执行产物的正整数revision
subject_digest_before: 填实际内容摘要或null及原因
subject_digest_after: 填实际内容摘要或null及原因
executor: 填责任人
command_id: CMD-001
cwd: 填执行位置
command_or_steps: 填实际执行内容；未执行为null并写reason
started_at: 填时间或null
ended_at: 填时间或null
exit_code: null # 实际数值；未运行或手工操作不编造
observed_assertions: []
evidence_paths: []
status: pass / fail / blocked / not_run（选一个）
reason: 填失败、阻断、未运行或复用依据
reuse_analysis: null # 复用须含来源日志/版本、未受影响依据、环境/数据、审核人
```

## 6. 最终 test-report 和 handoff

```yaml
# 加公共头
scope: 填本阶段实际覆盖范围及明确排除项
plan_review: {path: 填路径, reviewed_revision: 1, status: 填实际状态} # revision需核对
results: [] # 引用执行记录，逐case保留status/origin/freshness/required
counts:
  required: {pass: 0, fail: 0, blocked: 0, not_run: 0}
  optional: {pass: 0, fail: 0, blocked: 0, not_run: 0}
excluded_evidence: [] # stale/fixture等不得作为真实通过证据，注明原结果
not_selected: [] # 未触发的层级/集合及理由；不是已执行pass
gaps: [] # 缺口、影响、owner、下一触发点
status: pass / revise / blocked（按门禁聚合，非case状态）
conclusion: 填证据支持的范围，不写“已上线”
handoff:
  status: 填同阶段门禁状态
  artifacts: []
  evidence: []
  unresolved: []
  next_owner: 填下一责任人；只提议，不自动派发
```

生成后检查 `required` 计数与逐 case 对齐；不同尝试不重复计为多个 case。已有必需 fail 优先给 revise，其他必需缺口保留；全部是 fixture/缺版本时不出真实 pass。只有独立计划 review 及当前必需证据满足，才能交本阶段 pass。
