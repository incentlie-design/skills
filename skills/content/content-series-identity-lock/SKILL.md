---
name: content-series-identity-lock
description: "Freeze series-level invariants versus allowed episode variation for cast, look, voice, and locations. Use for 系列身份、十集一致性、什么可以变; not for implementing Cast schema or regenerating failed episodes."
---

# 系列身份锁定

观众靠什么认出「这是同一部」。十集不是把 E01 复制九次，也不是每集换一套脸。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

### 门禁

要有 `character_visual_lock_ref` 与 `voice_identity_pack_ref`。并行写者只读同一 `lock_revision`。

### 拆工作

1. **不变量。** `invariants` 至少覆盖：Cast 骨相与签名细节、旁白身份、核心场景规则、色彩语言、系列音乐家族、地点 room tone 家族。
2. **变量。** `variables`：情绪、临时外套、后出场配角、一次性道具、单集配乐能量、天气/时段。每项 `first_use` 与是否重评已通过集。
3. **单锁。** 竞争方案从同一 R1 出发，producer 只选一套 `lock_revision`。
4. **失效。** `invalidation`：换脸/声线/主题音乐/主地点底噪时枚举受影响集；已评集必须重评，禁止静默覆盖。
5. **W1。** 代表集前锁 E01 全部依赖与跨集关键项。

### 产物字段

`series-identity-rules`：`invariants` `variables` `first_use` `invalidation` `lock_revision`。

### 失败分支

mint 产品 CharacterRevision 字段当事实 → `mint_product_schema`。生成媒体禁止。

## 输出

`artifact_kind=series-identity-rules`：不变量、变量、first-use、失效规则。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `producer`, `visual_director`, `audio_director`。`r_alignment` = R2, R6。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `character_visual_lock_ref` | yes | ref | 指向 character-visual-lock |
| `voice_identity_pack_ref` | yes | ref | voice-identity-pack |
| `music_bed_plan_ref` | no | ref | music-bed-plan |
| `ambience_foley_plan_ref` | no | ref | ambience-foley-plan |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `series-identity-rules` | `producer`, `visual_director`, `audio_director`, `validator` |

禁止：`media_generate`, `mint_product_schema`。

## 停止

不发明产品 CharacterRevision 字段名当事实。不生成媒体。
