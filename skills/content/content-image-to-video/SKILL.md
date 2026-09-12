---
name: content-image-to-video
description: "Plan image-to-video from a locked start frame: one action, camera versus character motion, explicit end. Use for I2V、图生视频、首帧驱动; not for blind text-to-video, multi-action clips, or Provider submit."
---

# 静帧驱动运动

先有合格静帧，再运动。一镜一个主动作。本 Skill 出计划，不调用 I2V 模型。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

分镜已要求运动，且存在 `start_frame_ref`。无首帧 → 回静帧生成，不盲 text-to-video。

## 方法

### 门禁

`start_frame_ref`、`shot_list_ref`、`character_visual_lock_ref` 必填。`rights_status` 若涉及真人 likeness 必须 `allowed`。

### 拆工作

1. **一对一。** 每 `shot_id` 一条计划，绑同一 `start_frame_ref`。
2. **一个动作。** `one_action` 一句话。第二动作拆下一镜。
3. **谁在动。** `camera_vs_character`：camera / character / both。both 必须写主从，默认不要 both。
4. **结束条件。** `end_condition`：动作完成、到达构图、或时长帽。`max_seconds` 短于分镜 `duration_s` 时，余下 hold。
5. **身份。** `identity_lock_ref` 整句复用；I2V 提示不得改写脸。
6. **衔接。** 下一镜若接动作，本镜结束姿态必须可当下一 `start_frame`。

### 产物字段

`image-to-video-plan`：`shot_id` `start_frame_ref` `one_action` `camera_vs_character` `end_condition` `identity_lock_ref` `max_seconds`。

### 失败分支

无首帧做 T2V → `text_to_video_blind`。一镜多动作 → `multi_action_clip`。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`。`r_alignment` = R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `start_frame_ref` | yes | ref | 已锁静帧，I2V/有限动画的第一帧 |
| `shot_list_ref` | yes | ref | shot-list |
| `character_visual_lock_ref` | yes | ref | 指向 character-visual-lock |
| `fps_budget` | no | number | 动画预算帧率，如 8/12/24；不是产品播放器承诺 |
| `rights_status` | no | enum:rights_status | source 或参考资产权利：allowed / unresolved / denied |
| `limited_animation_ref` | no | ref | limited-animation-plan |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `image-to-video-plan` | `visual_director`, `editor`, `producer` |

禁止：`text_to_video_blind`, `multi_action_clip`, `provider_submit`。

## 停止

不 submit、不安装权重。有限动画的 hold/cycle 交给 `content-limited-animation`。
