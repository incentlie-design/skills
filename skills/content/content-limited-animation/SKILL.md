---
name: content-limited-animation
description: "Plan limited animation for narrated stills-plus-motion episodes: holds, cycles, smears, budgeted fps. Use for 有限动画、动态漫画、hold、循环层; not for full 24fps episode animation, blind text-to-video, or changing identity lock sentences."
---

# 有限动画

解说剧/动态漫画默认 **少动**。60–120s 全片逐帧是失败，不是品质。本 Skill 只写运动预算，不 submit 生成。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

`media_form` 为 `stills_plus_audio` 或需要「静帧微动」的 `audiovisual`。旁白段优先 hold。

## 方法

词表见 [motion-classes](references/motion-classes.md)。

### 门禁

要有 `shot_list_ref`、`character_visual_lock_ref`、`media_form`。`audio_only` → `blocked`（没有画面可动）。身份句不得改写。

### 拆工作

1. **按镜分级。** 每 `shot_id` 选 `motion_class`：hold / cycle / smear / camera-only / character-acting。旁白信息段默认 hold。
2. **预算。** `fps_budget` 常用 8 或 12，不是产品播放 fps。全片 24fps 逐帧标 `full_animate_episode`。
3. **Hold。** `hold_frames` 写清停在哪一帧、停到哪个 `line_id` 结束。
4. **Cycle。** 风、呼吸、循环背景用 `cycle_id`，必须能无缝；人物骨相不得在 cycle 里漂移。
5. **Smear。** 仅动作峰值 1–2 帧，`smear` 说明方向；不能当每镜默认。
6. **身份。** `identity_lock_ref` 指向同一 `lock_sentence` revision。
7. **静帧优先。** 有 `start_frame_ref` 则运动从该帧出发，不另起一张脸。

### 产物字段

`limited-animation-plan`：`shot_id` `motion_class` `hold_frames` `cycle_id` `smear` `fps_budget` `identity_lock_ref`。

### 失败分支

全片 character-acting → `revise`。submit 模型 → `provider_submit`。改 lock 句 → `change_lock_sentence`。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`。`r_alignment` = R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `shot_list_ref` | yes | ref | shot-list |
| `character_visual_lock_ref` | yes | ref | 指向 character-visual-lock |
| `media_form` | yes | enum:media_form | 成品形态 |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `fps_budget` | no | number | 动画预算帧率，如 8/12/24；不是产品播放器承诺 |
| `start_frame_ref` | no | ref | 已锁静帧，I2V/有限动画的第一帧 |
| `panel_plan_ref` | no | ref | panel-plan |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `limited-animation-plan` | `visual_director`, `editor` |

禁止：`full_animate_episode`, `provider_submit`, `change_lock_sentence`。

## 停止

计划写完即停。不生成视频，不把 12fps 预算写成播放器规格。
