---
name: content-character-visual-lock
description: "Lock reusable character visual identity: face, body, wardrobe, palette, signature detail, and allowed episode variation. Use for 人设图、三视图、角色一致性、character sheet; not for generating images or choosing a model."
---

# 人物视觉锁定

定义「观众靠什么认出是同一个人」。产出可复用的身份矩阵与可变规则，供分镜和生成引用。不调用图像模型。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **身份矩阵先于 prompt。** 脸型、眼型与间距、眉、鼻、唇、颌、发长/质、肤色范围、年龄感、体型剪影、体态、**一个签名细节**（疤、饰品、发缝）。
2. **必要视图。** 需要画面时：正面、侧面、3/4；表情与服装变体另列，不替换基础型。
3. **锁定字符串 verbatim。** 身份句一旦冻结，后续 prompt **整句复用，禁止同义改写**。改写是换脸的主因。
4. **可变清单。** 情绪、临时外套、伤、灯光可变；骨相、发色、签名细节默认不可变。每项写 first-use 集。
5. **多角色反撞车。** 相邻角色至少改五个矩阵维度，避免「同一张网文脸」。
6. **权利。** 参考图必须有 hash 与 rights；无权的真人照片不得当身份源。

## 输出

`artifact_kind=character-visual-lock`：矩阵、锁定句、可变规则、参考图 refs/hash/rights、禁止项。

## 停止

不生成图，不把 lock 当成 #95 schema。无权利 → `blocked`。
