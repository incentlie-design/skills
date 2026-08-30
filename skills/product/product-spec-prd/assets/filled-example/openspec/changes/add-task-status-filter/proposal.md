# 记住待办状态筛选

本文件及同目录产物统一绑定 [handoff](handoff.json) 中的 `artifact_revision: 1`；原始输入见 [raw-input](../../../raw-input.md)。fixture，仅规划。

## Why

待办使用者希望先处理未完成项，而不必每次从混合列表中逐条寻找。保留当前浏览器上的筛选选择，减少重复选择。

## What Changes

- 提供全部、未完成、已完成三个筛选；不修改待办和既有顺序。
- 空结果可清除筛选；浏览器保存/读取偏好失败时仍能使用列表。
- 同浏览器重新加载恢复合法选择；默认或非法值回到全部。
- 非目标见 [PRD](prd.md)：不做登录、后端、跨设备同步、搜索或埋点。

## Capabilities

### New Capabilities

- `task-status-filter`：列表按完成状态筛选及本地偏好的失败恢复；见 [delta](specs/task-status-filter/spec.md)。

### Modified Capabilities

无。fixture 基线明确没有现行筛选 spec，不用 MODIFIED 猜造旧需求。

## Impact

未来涉及本地待办列表界面、偏好读写及局部测试，不改变数据接口或待办数据结构，无新增依赖/网络请求。本次仅写 change 文档；代码范围见 [design](design.md)，不是当前实现授权。
