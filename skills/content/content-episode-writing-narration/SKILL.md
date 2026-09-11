---
name: content-episode-writing-narration
description: "Write one 60–120s narrated-drama episode script with narration/dialogue budget and asset IDs. Use for 单集剧本、旁白、解说、对白时长; not for storyboards, TTS, or changing the season outline."
---

# 单集旁白剧本

把已冻结大纲中的一集写成可生产的旁白/对白稿，并做时长预算。只写指定 ordinal。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **四拍而不是三幕填满。** Hook → Pressure → Crack → Aftermath。60–120s 不允许支线。
2. **旁白与对白分工。** 旁白负责时间跳跃、内心无法被看见的因果、物件意义；对白负责冲突与关系。禁止旁白复述画面已说清的事。
3. **时长预算。** 先写预计秒数：旁白、对白、静默/音乐。中文旁白可按约 4–5 字/秒作**预算**，最终以音频实测为准。超预算先删事件，不标「TTS 加快」。
4. **绑定资产。** 每个说话人、地点、关键道具引用稳定 ID/revision。未解析 ID 阻止该集 `design-ready`。
5. **入出状态。** 写清本集开始时谁知道什么、结束时什么变了、交给下一集的钩子。E05→E06 的状态只有一份。

## 输出

`artifact_kind=episode-script`：ordinal、旁白/对白文本、说话人、预计秒数、资产依赖、入出状态、未解析依赖。

## 停止

不改大纲，不写镜头表（交给分镜 Skill），不调用 TTS。
