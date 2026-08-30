# 方法卡模板

复制本模板到授权知识库的 `cards/<stable-id>-<slug>.md`；填写后删除字段提示。每卡一个可独立使用的拍摄判断，章节固定以便人工比对。来源摘要与原创内容分栏；无可核验来源时不伪填已核验卡。

```markdown
# VDL-NNN｜方法名称

- schema_version: 1
- revision: 1
- evidence_status: verified_summary / needs_review / conflicted（择一）
- tags: [主题, 技法, 平台或阶段]
- source_ids: [SRC-NNN]
- last_verified_access_date: YYYY-MM-DD（仅实际读正文后填）
- exercise_status: not_run（有实拍证据时另附路径和日期）

## 来源

- title: 原文标题
- url: [来源](公开完整 URL)
- publisher: 发布机构
- author: 署名；没有则 unknown
- access_date: YYYY-MM-DD
- published_or_updated: 原文显示的日期及精度；没有则 unknown
- source_type: 官方建议 / 创作者原文 / 品牌案例自述等
- locator: 支持本卡主张的具体章节；没看视频不写时间码

## 来源实际支持的要点

- F1（定义/来源建议/案例自述，择一）：少量中文转述，对应上述章节。
- 若多来源，逐条写 source ID 与 locator，不只在文末堆链接。

## 原创归纳（非来源原话）

说明从 F1 到本方法的推导；指出哪些训练参数是本地选择。
原文未支持的推断与不确定性写在这里，不能冒充直接事实。

## 适用 / 不适用

- 适用：受众、平台、创作目标、设备等必要条件。
- 不适用：失效边界、必须另查证的情形，不承诺销售或完播结果。

## 操作步骤（原创）

1. 可执行且能观察结果的动作。
2. 需要的镜头、人员或约束。

## 可拍摄练习（原创，尚未执行）

场景与道具、时长/时间预算、拍摄方式、交付镜头/短片或记录。
不需要新增付费设备；涉及人员/地点先取得拍摄许可。

## 检查点

- 可观察的判断，而非“高级感”或保证营销提升。
- 区分理解/画面检查与真正效果实验；无实拍证据不写已通过。

## 版权与更新

- rights: 原文与原始素材归原权利人；未确认可再分发许可。
- storage: 仅摘要、链接和原创练习；不保留原图/全文/视频。
- review_when: 下次实际使用且需核实，或来源变动/被反例挑战时有界刷新。
- conflicts: 无已知冲突 / 关联卡与双方证据；未核实不写“无冲突”。
- change_log: YYYY-MM-DD r1；创建原因、访问情况；后续 old→new。
```

`verified_summary` 不是“方法效果已验证”。更新/去重/不可访问的处理使用技能中的 [维护规则](../../skills/content/content-video-director-learning/references/maintenance.md)。
