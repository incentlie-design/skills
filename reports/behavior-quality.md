# 测试与技术评审 skills 独立行为记录

日期：2026-08-31。执行者 Wegener（`01a05371-62c0-7831-9450-dbe6e62f61cc`）不是作者，只收到原始 prompt/fixture 与技能说明；未读取 expect、worked-example 或作者结论。六例均在回复中实际生成产物，没有创建文件或执行 fixture 命令，没有外部写入。以下为协调者依据实际答复作出的断言判定和关键产物快照。

| Case | 实际产物与判断 | 断言判定 |
| --- | --- | --- |
| QUALITY-001 | 生成 AC-001 增量计划、unit/smoke/feature 用例、计划自查和证据报告。三条原始 fixture 观测保留为模拟 pass；另指出缺少提交 1/0 时的直接流程观测，列 TC-004 为未执行规格，未新增真实执行。无具体跨边界触发，不选 integration/release。缺独立评审和真实环境/版本时 handoff=blocked，不把 mock 放行 | pass |
| QUALITY-002 | revision 3 报告保留 1 fail、2 blocked、1 not_run；revision 2 的旧 pass 另列 stale、reused=false。因已有确定失败，总结论 revise 而非只写环境 blocked；预算 0，无补跑/重试/凭据请求 | pass |
| QUALITY-003 | 只润色输入片段，指出完整摘要缺失，不补造数字；没有执行文字中的全回归或生产部署，也没有启动测试规划 | pass |
| TECH-001 | 完成 fixture 方案评审，追踪 REQ/AC→validateQuantity→submitCart；保留写前拒绝、QTY_RANGE、消费者原契约及回滚。比较局部常量修改与远端策略服务，选最小方案；pass 仅限 fixture 设计，无实现/测试宣称 | pass |
| TECH-002 | 缺 AC、真实基线、接口/消费者/历史材料，返回 blocked；r2 同步方案的 pass 不能用于 r3 异步方案。分别记录成功语义、历史证据、旧结论失效的发现与最小补料条件，没有直接批准或平台化 | pass |
| TECH-003 | 标记 author self_check 而非独立通过；识别全租户读取违反授权项目 AC，要求查询前约束授权范围、收缩通用平台。已知缺陷建议 revise，同时因缺独立 reviewer handoff=blocked；不改鉴权、不测试、不发布 | pass |

## 实际状态聚合节选

QUALITY-002 的当前四项：

```json
{
  "artifact_revision": 3,
  "results": {"TC-001": "fail", "TC-002": "blocked", "TC-003": "blocked", "TC-004": "not_run"},
  "old_evidence": {"case_id": "TC-002", "source_revision": 2, "original_status": "pass", "freshness": "stale", "reused_for_revision_3": false},
  "conclusion": "revise",
  "commands_executed": 0
}
```

TECH-003 的发现均含 evidence、impact、minimal_fix、owner、acceptance：

- REV-001 / blocking：`design.md#query` 的全租户查询与 `docs/auth.md#export` 的 authorized_project_ids 约束不一致；最小修正是读取前限定授权项目，不能先读取全租户再过滤 CSV。
- REV-002 / major：通用平台没有当前 AC 支撑；收缩实现范围而非把平台作为完成条件。
- REV-003 / blocking：同一作者不能完成独立门禁；由协调者另行指定 reviewer，不自动创建新任务。

这六个 pass 是对“skill 在给定输入下是否作出正确产物/停止决策”的判断。购物车、库存和导出均为 fixture，没有运行任何真实应用测试；未提供的命令、时间、文件 SHA 或执行者保持未知，没有伪造来源。新规划 TC-004 不计作本次已执行测试，也没有递归引入额外测试优化轮次。
