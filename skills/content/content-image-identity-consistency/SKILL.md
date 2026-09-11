---
name: content-image-identity-consistency
description: "Choose the lightest identity-preserving image method that survives planned pose/scene change. Use for 人物一致性、IP-Adapter、cref、character lock in generation; not for installing ComfyUI, picking a product image Provider, or live paid generation."
---

# 生成图身份一致性

把「同一角色换场景仍可认」当成方法选择，而不是堆模型名。产品尚未必须上 image；本 Skill 供内容轨与以后的叶子使用。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

本 Skill 选型方法，不安装权重、不 submit Provider。

### 门禁

必须有 `character_visual_lock_ref`。无权真人参考 → `blocked`。

### 拆工作

1. **变化分级。** 每人 `variation_class`：同姿态微变 / 换场景 / 换年龄或画风。
2. **最轻方法。** `method` 选能活过该变化的最轻档：verbatim lock 句 → 参考图条件 → 结构条件 → 拒绝该变化。跨十集稳定 ≠ 单图变体。
3. **分通道。** `identity_sentence_ref`（谁）与 `pose_control`（怎么站）与 `style_control`（什么片子）分开。身份句禁止同义改写。
4. **结构。** 姿态/构图用 pose/depth/canny 一类，不把动作小说塞进身份句。
5. **批次。** `batch_rule`：同场多镜同批或显式 ref；跨集同一 lock revision。
6. **证据级。** 本地草稿 ≠ live Provider。

### 产物字段

`image-identity-plan`：`character_id` `variation_class` `method` `identity_sentence_ref` `pose_control` `style_control` `batch_rule`。

### 失败分支

计划变化会掉身份又不愿升级约束 → `revise` 或拒绝变化，不赌模型。

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
| `rights_status` | no | enum:rights_status | source 或参考资产权利：allowed / unresolved / denied |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `image-identity-plan` | `visual_director`, `producer` |

禁止：`provider_submit`, `install_weights`, `embed_secrets`。

## 停止

不安装权重，不写 API key，不把 IP-Adapter/PuLID/InstantID 写成产品依赖。
