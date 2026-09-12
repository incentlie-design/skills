---
name: content-looping-background
description: "Design seamless looping backgrounds and ambient motion plates for stills-plus-audio episodes. Use for 循环背景、loop、环境层; not for hard-cut loops, drifting characters into the plate, or Provider submit."
---

# 循环背景

静帧剧靠可循环的世界层活着。人物层与背景层必须分开，避免背景 cycle 把脸带跑。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

`media_form=stills_plus_audio`，地点需要风/雨/车流/呼吸光，而不是全片死静。

## 方法

### 门禁

`location_id`、`media_form`、`duration_s_range`。`audio_only` → `blocked`。

### 拆工作

1. **地点。** 一地点一计划，复用同一 `location_id` 的 room tone 家族。
2. **运动。** `motion_class` 只能 cycle 或 hold。人物 acting 不进背景层。
3. **时长。** `loop_seconds` 应能整除或交叉淡入覆盖 `duration_s_range` 上界。
4. **接缝。** `seam_rule`：相位对齐或 crossfade。硬跳 → `hard_cut_loop`。
5. **安全。** `identity_safe=true`：背景不得含可认脸。`hold_vs_cycle` 写清哪些层静、哪些层循环。
6. **声画。** 有 ambience 计划时，视觉 cycle 不得与环境床冲突（无声的树叶狂舞）。

### 产物字段

`looping-background-plan`：`location_id` `loop_seconds` `seam_rule` `motion_class` `hold_vs_cycle` `identity_safe`。

### 失败分支

人物画进循环板 → `drift_character_into_bg`。submit 生成 → `provider_submit`。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`, `audio_director`。`r_alignment` = R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `location_id` | yes | id | 稳定地点 slug |
| `media_form` | yes | enum:media_form | 成品形态 |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `style_frame_ref` | no | ref | style-frame-lock 产物 |
| `ambience_foley_plan_ref` | no | ref | ambience-foley-plan |
| `fps_budget` | no | number | 动画预算帧率，如 8/12/24；不是产品播放器承诺 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `looping-background-plan` | `visual_director`, `editor`, `audio_director` |

禁止：`hard_cut_loop`, `drift_character_into_bg`, `provider_submit`。

## 停止

不产出最终视频。循环计划交给合成，不在此选型工具。
