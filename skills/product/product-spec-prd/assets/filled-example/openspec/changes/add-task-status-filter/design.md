# Design：本地筛选偏好

## Context

基线是 [raw-input](../../../raw-input.md) 给定的本地列表，不是真实代码审计；repo/base/revision 见 [handoff](handoff.json)。WHY 见 proposal，行为见 [delta](specs/task-status-filter/spec.md)。尚未实施或通过技术评审。

## Goals / Non-Goals

保持列表组件局部变化、不改变待办数据。无新状态管理依赖、后端、迁移服务或网络请求。

## Decisions

- D-001（REQ-001/002）：在列表派生可见项，以内存枚举 `all|open|done` 过滤；选择 all 即清除。不删除、重排或重写源数据。对比维护另一份已筛选数据，派生方式避免两份列表不同步。
- D-002（REQ-003）：偏好适配器只读写 `localStorage` 键 `task-list.status-filter.v1`，值为上述枚举。读取返回有效值或 all，以及可选读取错误；写入返回成功/失败，不吞掉错误状态。对比后端偏好，本地方案满足单浏览器边界，不引入账号/API。
- D-003（REQ-003）：UI 先更新内存选择再尝试保存，失败时保留选择并提示；只在下一次显式选择时再写。对比先成功持久化再更新 UI，这不会让存储故障阻断当前任务。清除筛选也是显式选择 all。

接口为本地偏好读取/写入，不新增 HTTP API。输入是筛选枚举；输出是枚举与读写结果。只持久化枚举，无用户身份或待办正文；遇非法历史值回 all，无需迁移数据。

## Risks / Trade-offs

- 禁用/清除浏览器存储会丢失偏好 → 当前筛选继续工作，刷新按 AC-004 回退；不承诺跨设备或跨浏览器恢复。
- 组件需兼顾空结果与存储错误 → 两种提示含义分开，按 AC-002/003 验收，不用全页错误遮挡列表。

## Migration Plan / Rollback

本次只提交规划，不部署。未来实施无需数据迁移；回滚由获授权实现者撤回本功能改动，列表恢复显示全部，旧枚举键可留存但不再读取；不自动清除浏览器数据。

## Planned Write Scope

`src/task-list/filterPreference.ts` 归 implementer-state；`src/task-list/StatusFilter.tsx` 与 `src/task-list/TaskList.tsx` 归 implementer-ui；`tests/task-list/` 归 quality-owner。依赖与验收见 tasks。上述为未来任务约束，不是本次允许修改的文件。

## Open Questions

本 fixture 无影响任务边界的未决项；真实项目必须先核实已有组件/测试环境，若不符则回协调者修订 revision，不自选新框架。
