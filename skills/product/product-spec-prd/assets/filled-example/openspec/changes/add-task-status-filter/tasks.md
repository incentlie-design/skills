# Tasks：待办状态筛选

本例未实现；checkbox 均未勾选，状态均为 draft。OpenSpec 原生格式是编号 checkbox；下面的 TASK ID、owner、dependencies、write_scope、AC、预算和停止字段为项目扩展。所有任务引用 [handoff](handoff.json) 的 `artifact_revision: 1`。

共同门禁：独立产品评审、按需技术/测试规划及明确的实现授权完成后，协调者才可将任务转 ready。以下路径只描述未来分派，不能扩大本次文档 write_scope。

## 1. 偏好适配

- [ ] 1.1 TASK-001 提供本地筛选偏好读写；以有效值、非法值、读取异常、写入失败四组输入核对返回结果符合 AC-003/004。
  - task_id: TASK-001
  - owner: implementer-state
  - dependencies: []
  - write_scope: src/task-list/filterPreference.ts
  - inputs: design.md D-002；specs/task-status-filter/spec.md “Retain a usable local filter preference”；fixture 存储读写失败条件
  - outputs: 枚举偏好适配器、局部检查证据、失败/未知项；不写 UI 文件
  - AC: AC-003、AC-004（适配器部分，整体 UI 由 TASK-002/003 承接）
  - budget: 一个有界实现 session；局部 smoke 不超过 5 分钟；最多一次定向修正
  - stop: 输入/范围变化或既有接口冲突时 blocked 并交回协调者；不得安装依赖或设计远端偏好服务

## 2. 界面承接

- [ ] 2.1 TASK-002 接入筛选、空状态与偏好提示；用 t1/t2/t3、全完成、零任务及存储失败场景逐项检查 AC-001/002/003/004。
  - task_id: TASK-002
  - owner: implementer-ui
  - dependencies: [TASK-001]
  - write_scope: src/task-list/StatusFilter.tsx；src/task-list/TaskList.tsx
  - inputs: TASK-001 接口和证据；prd.md 旅程；design.md D-001/D-003
  - outputs: 列表局部交互、人工或既有测试环境的检查记录；不改偏好适配器所属文件
  - AC: AC-001、AC-002、AC-003、AC-004
  - budget: 一个有界实现 session；定向检查不超过 10 分钟/3 个命令；最多一次定向修正
  - stop: 必须更改 TASK-001 契约、共享文件或新增账号/后端时停止回责任人，不跨 owner 修复

## 3. 旅程验收

- [ ] 3.1 TASK-003 核对完整旅程与 AC 映射；记录真实 pass/fail/blocked/not_run 及对应 revision，不把 mock 结果当业务通过。
  - task_id: TASK-003
  - owner: quality-owner
  - dependencies: [TASK-001, TASK-002]
  - write_scope: tests/task-list/
  - inputs: prd.md AC 表、spec delta、实现 candidate revision、两项实现证据
  - outputs: 局部验收用例及 tests/task-list/acceptance-report.md；不改实现
  - AC: AC-001→TC-001（三种选择/不改数据）；AC-002→TC-002（空结果/清除/零数据）；AC-003/004→TC-003（失败/恢复/刷新）
  - budget: 这三组代表检查；局部验证最多 10 分钟；一次验收及最多一次定向复验，不跑全仓回归
  - stop: candidate/revision 缺失则 blocked；确定性失败不原样重跑；报告交回 owner，不擅自改实现

三个任务依赖无环，writer 文件不重叠。产品 scope 中每条 AC 均有实现承接和验收 owner，但本例没有执行任务或产生通过证据。
