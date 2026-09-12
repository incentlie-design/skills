---
name: content-cinematography-shortform
description: "Design camera language for 60–120s narrated episodes, including shot size, axis, aspect ratio, and motivated movement. Use for 摄影、景别、轴线、运镜、竖屏构图; not for storyboards, blocking execution, or image generation."
---

# 短制镜头语言

把「观众此刻该发现什么」写成可拍摄/可生成的镜头选择。横竖屏各自原生构图，禁止裁切冒充。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

词表见 [shot-vocab](references/shot-vocab.md)。本 Skill 不编译分镜表、不调度走位、不生成图。

### 门禁

必须有 `episode_script_ref`。无 `aspect_ratio` 不得宣称原生构图完成，`aspect_strategy` 标 `unspecified`。

### 拆工作

1. **信息。** 按剧本 beat 列：观众已知 / 本镜新增 / 仍未知。
2. **注意力。** `attention_plan`：在场每人看谁/看物；反应不得早于触发。
3. **覆盖功能。** 每镜只选一个：establishing / action / insert / reaction。
4. **三轴。** `size` `angle` `move` 只用封闭词表。
5. **轴线。** 每场 `axis` + `axis_side`。
6. **画幅。** 每种请求比例写 `aspect_layout`：主体、视线空间、字幕区。竖屏用纵深/上下，禁止横屏填边冒充。
7. **运动策略。** `movement_policy`：默认静止；动则写起止与跟随。

### 产物字段

- `camera-treatment`：`attention_plan` `axis` `aspect_strategy` `movement_policy`
- `shot-language-notes`：`shot_id` `scene_id` `size` `angle` `move` `eyeline` `axis_side` `aspect_layout`

### 失败分支

台词冲突 → `blocked` 回剧本。无 `location_id` 不伪造地理。

## 输出

`artifact_kind=camera-treatment` 与 `shot-language-notes`。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`。`r_alignment` = R3, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `aspect_ratio` | no | string | 如 9:16 或 16:9；未选则不得宣称原生构图完成 |
| `location_id` | no | id | 稳定地点 slug |
| `character_visual_lock_ref` | no | ref | 指向 character-visual-lock |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `camera-treatment` | `visual_director`, `editor` |
| `shot-language-notes` | `visual_director` |

禁止：`rewrite_dialogue`, `media_generate`。

## 停止

不改剧本，不编译逐帧，不生成媒体。
