---
name: content-character-visual-lock
description: "Lock reusable character visual identity: face, body, wardrobe, palette, signature detail, and allowed episode variation. Use for 人设图、三视图、角色一致性、character sheet; not for generating images or choosing a model."
---

# 人物视觉锁定

定义「观众靠什么认出是同一个人」。产出可复用的身份矩阵与可变规则，供分镜和生成引用。不调用图像模型。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

矩阵维度见 [identity-matrix](references/identity-matrix.md)。

### 门禁

`rights_status=allowed` 才能用真人参考图。无权 → `blocked`。本 Skill 不调用图像模型。

### 拆工作

1. **矩阵。** 每人写 `matrix`：脸型、眼型与间距、眉、鼻、唇、颌、发长/质、肤色范围、年龄感、体型剪影、体态、一个签名细节。
2. **锁定句。** `lock_sentence` 一旦冻结，下游 **整句复用**。同义改写视为换脸。
3. **视图。** 需要画面时 `views` 含正面、侧面、3/4。表情/服装进 `variants`，不替换基础型。
4. **可变。** `variants` 写清可变更（情绪、外套、伤、灯光）与不可变（骨相、发色、签名细节），每项 `first_use`。
5. **反撞车。** 相邻角色至少五个矩阵维度不同。
6. **权利。** 每张 `reference_image_refs` 绑定 hash 与 `rights_status`。

### 产物字段

`character-visual-lock`：`character_id` `matrix` `lock_sentence` `views` `variants` `first_use` `rights_status`。

### 失败分支

无权利参考图却当身份源 → `blocked`。不得 mint #95 schema。

## 输出

`artifact_kind=character-visual-lock`：矩阵、锁定句、可变规则、参考图 refs/hash/rights、禁止项。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`。`r_alignment` = R2。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `character_voice_profiles_ref` | yes | ref | 指向 character-voice-profiles |
| `rights_status` | yes | enum:rights_status | 该 source 是否允许改编/生成 |
| `reference_image_refs` | no | ref[] | 有权利的外形参考图 |
| `series_canon_ref` | no | ref | 指向 series-canon 产物 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `character-visual-lock` | `visual_director`, `producer`, `validator` |

禁止：`media_generate`, `mint_product_schema`。

## 停止

不生成图，不把 lock 当成 #95 schema。无权利 → `blocked`。
