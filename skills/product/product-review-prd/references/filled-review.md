# 已填实的产品评审信封示例

输入是 [待办筛选原始需求](../../product-spec-prd/assets/filled-example/raw-input.md) 及其链接的 `artifact_revision: 1` 全部文件（原 case 的人类标签为 example-r1）。此处是**格式与决策说明 fixture**，不是本次实现者做出的独立最终评审；不会替代后续盲测或给真实应用签字。

本例没有捏造缺陷以填满 findings：PRD 明确了筛选成功、空结果清除、存储失败后的反馈、恢复和刷新默认值，delta 与任务有对应承接，所以演示产品文档范围的 pass。跨设备同步不在原始目标内，放入建议，不要求实现。技术可行性、实际 UI 和真实测试不在此 pass 内。

```json
{
  "schema_version": 1,
  "fixture": true,
  "run_id": "fixture-task-filter-20260831",
  "change_id": "add-task-status-filter",
  "repo": "fixture://local-todo",
  "base_commit": "uncommitted",
  "artifact_revision": 1,
  "content_summary": "与输入 handoff 一致：all/open/done、空结果清除、偏好读写失败恢复；REQ-001/002/003、AC-001/002/003/004、TASK-001/002/003。",
  "status": "pass",
  "reviewer": "fixture/product-reviewer（说明性角色，非真实独立签名）",
  "reviewed_revision": 1,
  "scope": ["原始产品目标与非目标", "成功/失败/恢复旅程", "REQ→AC→delta→task 承接", "责任与范围约束"],
  "findings": [],
  "non_blocking_suggestions": [
    {
      "id": "SUG-001",
      "suggestion": "若以后出现明确跨设备需求，可单独评估偏好同步。",
      "value": "减少换设备后的重复选择。",
      "cost_tradeoff": "会引入账号、后端与数据策略；当前本地方案足以满足原始目标。",
      "owner": "product-owner",
      "decision": "本版不采纳，不创建 AC/任务，不实施；需要新的用户确认。"
    }
  ],
  "artifacts": [
    "raw-input.md",
    "openspec/changes/add-task-status-filter/proposal.md",
    "openspec/changes/add-task-status-filter/prd.md",
    "openspec/changes/add-task-status-filter/specs/task-status-filter/spec.md",
    "openspec/changes/add-task-status-filter/design.md",
    "openspec/changes/add-task-status-filter/tasks.md",
    "openspec/changes/add-task-status-filter/handoff.json"
  ],
  "evidence": [
    "prd.md 用户旅程与 AC-001/002 对应 delta 的 Select each status、Empty result and clear；TASK-002/003 承接。",
    "prd.md AC-003/004 对应 delta 两个存储场景和 design D-002/D-003；TASK-001/002/003 承接失败、恢复及刷新。",
    "raw-input.md、prd.md 非目标和 design 无后端边界一致；tasks 的代码 writer 不重叠且所有 checkbox 未完成。"
  ],
  "unresolved_questions": [],
  "next_owner": "product-owner",
  "limitations": ["仅演示文档评审", "不是技术或测试通过证据", "未修改输入，未授权应用实现或发布"]
}
```

## 有缺口或新版本时如何闭环

若实际待审材料删去了 AC-003 的保存失败反馈，不能照抄上面的 pass。按真实路径/章节提出 `REV-001`，用 `major`、影响、最小修复、文档 owner 与可观察 acceptance 记录为 `revise`；由 owner 修订，不由 reviewer 改文档。这里是条件说明，不声称当前 fixture 有这个缺陷。

owner 回传新 revision、diff 和 REV-001 对应证据后，最多一次定向复审：看失败时筛选是否仍可操作、错误是否可见、恢复是否有动作，并核对受影响 delta/tasks。一致才关闭发现；其他未受影响结论只有明确影响分析才复用。若只说“r2 已修好”却不给内容，输出 `blocked`；旧 r1 pass 对受影响 r2 已 stale。
