# 原始需求：记住待办状态筛选

这是已填实、可用于演练的 **fixture**，不是客户研究结论或已实现应用。目标 `repo = fixture://local-todo`；`base_commit = uncommitted`，不虚构 Git hash。下面的基线、角色和路径是本例输入数据，并未从真实应用代码验证。

## 用户原话

“我每天只想先看没做完的待办。列表上加‘全部 / 未完成 / 已完成’，首次默认全部。筛选不改待办内容，不重排。选项记在这台浏览器，下次打开恢复。没有匹配项要告诉我，也能一键清除筛选。浏览器不让保存时，筛选仍能用，告诉我偏好没保存；下次主动切换再尝试，不要循环重试。读取失败回到全部并提示，遇到旧的非法选项就回到全部。不要登录、后端、跨设备同步、新埋点或新的搜索功能。只做需求和任务规划，不写应用。”

## 明确基线与验收输入

- 当前只有本地列表，按既有顺序显示；没有筛选 capability，也没有相关现行 spec。这里的“没有”是 fixture 明确输入，不是因为缺文件而推断。
- 数据：`t1 买牛奶 completed=false`、`t2 寄快递 completed=true`、`t3 预约洗牙 completed=false`；另给全部已完成和零条待办两组验收数据。
- 既有代码位置约定：`src/task-list/TaskList.tsx`。允许未来新增同目录 `StatusFilter.tsx` 与 `filterPreference.ts`，局部测试位置 `tests/task-list/`。这些只是未来任务计划，不在本例实现。
- 责任角色：`product-owner` 确认目标与文档；`implementer-state` 处理偏好；`implementer-ui` 处理列表界面；`quality-owner` 验收；`product-reviewer` 独立产品评审。均为 fixture 角色，不是真人指派。
- 本次文档 write_scope：`openspec/changes/add-task-status-filter/`；read_set 为本文与上述基线说明。未来代码任务范围不是当前写入授权。
- 文档预算：一次生成、一次自查、最多一次修正。实施预算按 tasks 单列；未批准评审、未另授实现权限前任务保持 draft。
- 性能没有新增数值承诺；收益指标无实测基线。允许用本例验收数据做人工观察，不批准采集真实用户行为。

## 本例交付

change_id：`add-task-status-filter`；run_id：`fixture-task-filter-20260831`；artifact_revision：`1`（JSON 正整数，不是字符串）。既有原始 case prompt 把此样例称为 `example-r1`，那只是人类标签，不是 revision 字段值；数值身份以 handoff 为准。

- [proposal](openspec/changes/add-task-status-filter/proposal.md)
- [spec delta](openspec/changes/add-task-status-filter/specs/task-status-filter/spec.md)
- [design](openspec/changes/add-task-status-filter/design.md)
- [tasks](openspec/changes/add-task-status-filter/tasks.md)
- [PRD（项目扩展）](openspec/changes/add-task-status-filter/prd.md)
- [handoff（项目扩展，统一绑定）](openspec/changes/add-task-status-filter/handoff.json)

复用时把这里的原始输入与 change 复制到获准目标；真实 repo/base_commit/owner 必须重新确认。不要照搬 fixture 身份去批准业务任务。
