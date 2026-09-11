---
name: content-character-development
description: "Design distinct character psychology, speech, and relationships for a 10-episode narrated drama. Use for 人物塑造、声口、动机、对白区分; not for portraits, TTS provider choice, or locking visual sheets."
---

# 人物塑造与声口

让听众**不看名字也能分辨**谁在说话，并让行为有动机。视觉外形交给 `content-character-visual-lock`；声音 Provider 交给产品。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **Want vs need。** 公开目标与隐藏需求分开。十集短制里每人最多一条清晰外在目标。
2. **相邻角色至少五项不同。** 从年龄感、语速、用词层级、句长、口头禅、信息策略（直说/隐瞒/反讽）里选五项拉开。禁止全员同一「网文旁白腔」。
3. **声口样本。** 每名常驻角色给 3 句不可互换的例白（同场景下别人说会出戏）。旁白是独立声口，不是主角内心。
4. **关系是动作。** 用「对谁做什么」代替形容词人设。
5. **一致性优先于惊喜。** 破格必须由本集事件引起，并写入 canon 知识表。

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
