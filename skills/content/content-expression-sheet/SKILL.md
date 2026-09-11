---
name: content-expression-sheet
description: "Plan reusable facial expressions on a locked character without default lip-sync cloning. Use for 表情表、口型关闭、表演强度; not for changing bone structure, generating sheets, or treating lip-sync of real people as default."
---

# 表情与表演表

表情是变体，不是换脸。默认闭口；口型同步不是解说剧默认管线。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

有限动画或 I2V 需要「说话/反应」但不想动骨相；或评价说表情全是同一张微笑。

## 方法

### 门禁

`character_visual_lock_ref` 与 `character_voice_profiles_ref`。真人口型克隆默认禁止。

### 拆工作

1. **名单。** 每 `character_id` 一套表，绑 `lock_sentence_ref`。
2. **表情槽。** `expression_id` 建议闭集：neutral / listen / strain / suppress / decide。不要 50 个微表情。
3. **强度。** `intensity` 低/中/高。旁白段常用 listen+低。
4. **口。** `mouth_closed_default=true`。`lip_sync` 默认 `off`。对口型需要书面 likeness + 另授权，仍不在此 submit。
5. **声口一致。** 表情不得违背 profiles 的信息策略（隐瞒者不默认夸张瞪眼）。
6. **骨相。** 任何表情不得改 `matrix` 骨相维。

### 产物字段

`expression-sheet`：`character_id` `expression_id` `mouth_closed_default` `intensity` `lock_sentence_ref` `lip_sync`。

### 失败分支

默认唇形克隆 → `clone_lip_sync_default`。表情改骨相 → `change_bone_structure`。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`, `story_director`。`r_alignment` = R2, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `character_visual_lock_ref` | yes | ref | 指向 character-visual-lock |
| `character_voice_profiles_ref` | yes | ref | 指向 character-voice-profiles |
| `episode_script_ref` | no | ref | 单集 episode-script |
| `rights_status` | no | enum:rights_status | source 或参考资产权利：allowed / unresolved / denied |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `expression-sheet` | `visual_director`, `editor` |

禁止：`clone_lip_sync_default`, `change_bone_structure`, `media_generate`。

## 停止

不生成表情图。表是计划，生成走身份一致性 Skill 且仍须授权。
