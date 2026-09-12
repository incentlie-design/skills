---
name: content-character-development
description: "Design distinct character psychology, speech, and relationships for a 10-episode narrated drama. Use for 人物塑造、声口、动机、对白区分; not for portraits, TTS provider choice, or locking visual sheets."
---

# 人物塑造与声口

让听众**不看名字也能分辨**谁在说话，并让行为有动机。视觉外形交给 `content-character-visual-lock`；声音 Provider 交给产品。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

### 门禁

要有 `series_canon_ref` 与 `source_ref`。本 Skill 不写外形 prompt，不选 `voice_id`。

### 拆工作

1. **名单。** 常驻角色来自 canon，不凭感觉加主角。每人 `character_id`、`first_episode`。
2. **Want / need。** `want` 公开目标；`need` 隐藏需求。十集每人最多一条清晰 `want`。
3. **对比矩阵。** 相邻角色至少五项 `contrast_axes`：年龄感、语速、用词层级、句长、口头禅、信息策略（直说/隐瞒/反讽）。禁止全员网文旁白腔。
4. **声口。** `speech_rules` + `sample_lines` 恰好 3 句，同场景换人会出戏。
5. **旁白。** `narrator_profile` 独立；不是主角内心。
6. **关系。** 用「对谁做什么」，不用形容词人设。
7. **破格。** 出戏行为必须能指到本集事件，并回写 canon 知识表；否则 `revise`。

### 产物字段

`character-voice-profiles`：`character_id` `want` `need` `speech_rules` `sample_lines` `contrast_axes` `first_episode` `narrator_profile`。

### 失败分支

只有一个声口能写出来 → 未完成对比矩阵，不得 `pass`。缺源依据的年龄/身份标 `inference`，不升级为源事实。

## 输出

`artifact_kind=character-voice-profiles`：每角色 id、want/need、说话规则、例白、与其他角色的区分点、出场集。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `story_director`。`r_alignment` = R2, R3。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `source_ref` | yes | ref | 不可变源小说身份 |
| `series_canon_ref` | yes | ref | 指向 series-canon 产物 |
| `season_outline_ref` | no | ref | 指向 season-outline 产物 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `character-voice-profiles` | `story_director`, `audio_director`, `visual_director` |

禁止：`provider_submit`, `select_voice_id`, `write_visual_prompt`。

## 停止

不写外形 prompt，不选 ElevenLabs/Qwen voice_id（那是产品选择）。缺源依据的年龄/身份标 `inference`。
