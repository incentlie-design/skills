---
name: content-episode-writing-narration
description: "Write one 60–120s narrated-drama episode script with narration/dialogue budget and asset IDs. Use for 单集剧本、旁白、解说、对白时长; not for storyboards, TTS, or changing the season outline."
---

# 单集旁白剧本

把已冻结大纲中的一集写成可生产的旁白/对白稿，并做时长预算。只写指定 ordinal。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

### 门禁

必须能读到该 `episode_ordinal` 的 outline 行，以及 `series_canon_ref`、`character_voice_profiles_ref`。本 Skill 不改大纲、不调用 TTS。

### 拆工作

1. **只写一集。** `episode_ordinal` 锁死。四拍：Hook / Pressure / Crack / Aftermath。60–120s 无支线。
2. **拍 → 行。** 每拍拆成 `line_id`。`mode` 只能是 `narration` 或 `dialogue`。旁白：时间跳跃、看不见的因果、物件意义。对白：冲突与关系。禁止旁白复述画面已说清的事。
3. **说话人。** 对白绑 `character_id`；旁白用 narrator 槽。声口必须能对上 profiles。
4. **时长预算。** 每拍和整集写 `duration_s_budget`。中文旁白约 4–5 字/秒只是预算；最终以音频实测为准。超窗先删事件。
5. **资产。** 地点/道具用稳定 ID。未解析 ID 进 `unresolved_ids`，此时 `maturity` 不得 `design-ready`。
6. **状态。** `state_in` / `state_out` 与 outline 对齐。E05→E06 只允许一份交接。

### 产物字段

`episode-script`：`episode_ordinal` `beats` `line_id` `character_id` `spoken_text` `mode` `duration_s_budget` `state_in` `state_out` `unresolved_ids`。

### 失败分支

对白违反声口样本 → `revise`。想加快语速塞事件 → 禁止，回大纲 Skill。

## 输出

`artifact_kind=episode-script`：ordinal、旁白/对白文本、说话人、预计秒数、资产依赖、入出状态、未解析依赖。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `story_director`。`r_alignment` = R3。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `season_outline_ref` | yes | ref | 指向 season-outline 产物 |
| `series_canon_ref` | yes | ref | 指向 series-canon 产物 |
| `character_voice_profiles_ref` | yes | ref | 指向 character-voice-profiles |
| `episode_ordinal` | yes | integer | 1..10 |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `character_visual_lock_ref` | no | ref | 指向 character-visual-lock |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `episode-script` | `visual_director`, `audio_director`, `editor`, `validator` |

禁止：`provider_submit`, `rewrite_outline`, `call_tts`。

## 停止

不改大纲，不写镜头表（交给分镜 Skill），不调用 TTS。
