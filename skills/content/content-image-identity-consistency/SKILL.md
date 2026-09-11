---
name: content-image-identity-consistency
description: "Choose the lightest identity-preserving image method that survives planned pose/scene change. Use for 人物一致性、IP-Adapter、cref、character lock in generation; not for installing ComfyUI, picking a product image Provider, or live paid generation."
---

# 生成图身份一致性

把「同一角色换场景仍可认」当成方法选择，而不是堆模型名。产品尚未必须上 image；本 Skill 供内容轨与以后的叶子使用。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **拆开控制。** 身份（谁）/ 姿态结构（怎么站）/ 风格（什么片子）分通道。用同一句身份锁定句，禁止同义改写。
2. **选能活过计划变化的最轻方法。** 参考图快速变体 ≠ 跨十集稳定。姿态/年龄/画风大变时，轻量 adapter 会掉身份，应升级约束或拒绝该变化。
3. **结构用结构工具。** 姿态/构图用 pose/depth/canny 一类条件，而不是在身份句里塞动作小说。
4. **种子与批次。** 同场多镜尽量同批次或显式 ref；跨集必须引用同一 lock revision。
5. **权利。** 参考图 hash + rights；无权真人不得作身份源。
6. **不升级证据。** 本地草稿图不是 live Provider 结果。

## 输出

`artifact_kind=image-identity-plan`：每角色控制策略、允许变化、禁止变化、所需参考图、未选型声明。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`。`r_alignment` = R2, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `character_visual_lock_ref` | yes | ref | 指向 character-visual-lock |
| `shot_list_ref` | no | ref | shot-list |
| `reference_image_refs` | no | ref[] | 有权利的外形参考图 |
| `rights_status` | no | enum:rights_status | 该 source 是否允许改编/生成 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `image-identity-plan` | `visual_director`, `producer` |

禁止：`provider_submit`, `install_weights`, `embed_secrets`。

## 停止

不安装权重，不写 API key，不把 IP-Adapter/PuLID/InstantID 写成产品依赖。
