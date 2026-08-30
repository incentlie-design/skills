# PRD 与产品评审 skills 独立行为记录

日期：2026-08-31。执行者 Noether（`01a05371-9e47-7982-8f3c-07aeab337241`），非原 skill/fixture 作者。未读 expect、作者 validation 或 filled-review；PRD-001 完成前仅读 raw-input，没有照抄已完成示例。六例各执行一次，无递归委派或真实 repo 写入。

| Case | 实际产物与决策 | 断言判定 |
| --- | --- | --- |
| PRD-001 | 临时生成 PRD/proposal/spec delta/design/tasks/handoff 六文件，5 REQ、9 个更细粒度 AC/场景、3 个 draft 任务。明确文档范围、非目标、角色、依赖、预算、停止点；revision=1，commit=uncommitted。规划交接 pass 不代表业务批准，无 CLI/实现宣称 | pass |
| PRD-002 | 缺 repo、现行 Requirement、目标时延、owner/write_scope；返回 blocked/needs_input，只保留“缩短导出等待”草案，不假写 MODIFIED 全量替换块、不标 ready | pass |
| PRD-003 | 架构取舍请求转技术评审，缺批准 AC 与现有约束时停止；没有新建 change、改 PRD 或写代码 | pass |
| PREVIEW-001 | 独立审阅原仓库完整 fixture，而非自己刚生成的临时 PRD；输出公共 review envelope，reviewed_revision=1，逐条引用成功/空状态/存储失败/恢复/任务承接证据。产品文档 scope 内 pass；同步建议保留 value/cost/tradeoff 且不转任务 | pass |
| PREVIEW-002 | 未提供新版文件与内容身份，拒绝继承旧 pass；将删去失败处理涉及的旧结论标 stale，请求真实 revision/diff，不从标签猜数值 | pass |
| PREVIEW-003 | 仅索引和事务方案不走产品评审；材料不足不签技术结论；不向远端工单发送 | pass |

PRD-001 临时根：`/tmp/forward-prd-001.kr8wEZ/openspec/changes/add-task-status-filter/`。协调者实际读取 `handoff.json` 与 `tasks.md`：任务只有计划，没有创建 src/tests；实现授权、真实代码基线和技术责任人仍是明确前置门禁。临时产物不是本仓库新增 skill，也没有改变原 fixture。

## 产品评审结果节选

```json
{
  "artifact_revision": 1,
  "reviewed_revision": 1,
  "status": "pass",
  "scope": "仅原 fixture 产品文档闭环；不包含技术正确性或运行结果",
  "findings": [],
  "non_blocking_suggestions": [
    {
      "suggestion": "登录后跨设备同步仅作为未来可选方向",
      "value": "减少换设备后的重复选择",
      "cost": "需要账号、后端、隐私及冲突处理",
      "tradeoff": "扩大当前纯本地边界；本次不纳入 AC 或任务"
    }
  ]
}
```

原 fixture 评审的内容集摘要为 `fcf04c9e3bad069003f0d4a7132bab8e88f4a2b46f108a40ffd17f52ac735885`（执行者实际计算，按相对路径排序并拼接每文件 SHA-256 后取摘要）。完整证据观察包括 PRD AC 表、delta 存储失败/恢复场景、design 的先更新内存与非破坏回退，以及 tasks 的无环分工。引用不意味着已运行应用。

未执行：OpenSpec CLI、真实代码/业务基线确认、临时规划的独立产品再评审、实现、应用测试、外部工单写入。临时规划与原 fixture 同为 revision 1 但内容不同，执行者明确不互用评审，这是内容身份检查的一部分。
