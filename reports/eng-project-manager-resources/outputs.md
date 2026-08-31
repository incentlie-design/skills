# PM-SKILL-002 实际程序输出

2026-08-31，在 codex/eng-project-manager-resources 未提交候选上执行；受测内容 hash 见 [验证报告](validation.md)。程序真实执行，业务数据均为 fixture。旧版 probe 是原独立作者的测试源由当前实现者重放，不是新版本的独立审查签字。

## 三个作者场景

```text
test_boundary (__main__.PMCases.test_boundary) ... ok
test_happy (__main__.PMCases.test_happy) ... ok
test_missing (__main__.PMCases.test_missing) ... ok

----------------------------------------------------------------------
Ran 3 tests in 1.061s

OK
{"case": "PM-003-management", "invalid_budget": "rejected", "double_assignment": "rejected", "identity_overwrite": "rejected", "budget_without_decision": "rejected", "usage_rewrite_or_reset": "rejected", "work_objective_change_without_revision": "rejected", "ledger_unchanged": true}
{"case": "PM-003", "cross_goal": "rejected", "unauthorized_scope": "rejected", "stale_writer": "rejected", "path_escape": "rejected", "history_tamper": "detected", "sentinel_created": false, "authorized_revision_history": 2}
{"case": "PM-001-management", "goal_used_tokens": 200, "goal_remaining_tokens": 800, "agent_api_used": 160, "agent_next_used": 0, "shared_AC_no_double_count": true, "old_asset_owner": "ASN-001", "current_assignment": "ASN-003"}
{"case": "PM-001", "initial_blocked_by": ["TASK-001"], "all_tasks_without_AC": "incomplete", "refresh_evidence": "stale", "final": "simulated_complete", "ledger_revisions": 4, "missing_index": "missing"}
{"case": "PM-002-management", "unknown_remaining": null, "estimate_not_charged": null, "assignment_overrun": 1, "stale_remaining": null, "missing_asset": "missing"}
{"case": "PM-002", "missing_identity": "rejected_without_write", "cycle": "rejected", "owner": "assign_owner", "ancestor_block_and_fail": "G/REQ preserved; goal incomplete", "not_run": "not_run", "missing_evidence": "missing_evidence", "changed_file": ["stale_binding:A-CODE"]}
```

## 仓库结构检查

```text
{
  "status": "pass",
  "skills_checked": 10,
  "cases_defined": 30,
  "behavior_cases_executed": 0,
  "errors": []
}
```

## 官方格式检查

```text
Skill is valid!
```

## 旧版独立 probe 兼容重放

```text
test_dependency_and_explicit_goal_blocker (__main__.OriginalGoalAcceptance.test_dependency_and_explicit_goal_blocker) ... ok
test_missing_invalid_and_identity_boundaries (__main__.OriginalGoalAcceptance.test_missing_invalid_and_identity_boundaries) ... ok
test_refresh_staleness_and_four_layer_index (__main__.OriginalGoalAcceptance.test_refresh_staleness_and_four_layer_index) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.044s

OK
{
  "happy": {
    "dependency_blocker": "T1",
    "impacted_acceptance": "AC2",
    "goal_and_requirement_blocker_preserved": true,
    "recovery": "simulated_complete"
  },
  "boundaries": {
    "missing_original_goal_rejected": true,
    "cyclic_DAG_rejected": true,
    "path_escape_rejected": true,
    "cross_goal_project_rejected": true,
    "original_goal_immutable": true,
    "reported_done_not_verified": true
  },
  "incremental": {
    "four_layers_present": true,
    "query_read_only": true,
    "changed_content_rejected": true,
    "old_revision_stale": true,
    "history_revisions": 2,
    "same_event_idempotent": true
  }
}
```
