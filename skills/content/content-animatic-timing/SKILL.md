---
name: content-animatic-timing
description: "Assemble a timed animatic from shot list, script, and optional audio probe so 60–120s can be watched before finish animation. Use for animatic、动态分镜、预览时长; not for replacing locked audio, speeding speech, or generating hero shots."
---

# Animatic 时码

用占位画面 + 真实或预算音轨，先看出 60–120s 是否成立。占位不是成片。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

分镜已有时长列，需要可播预览或给评价人看结构。W1 代表集前强烈建议。

## 方法

### 门禁

`shot_list_ref`、`episode_script_ref`、`duration_s_range` 必填。有 `audio_probe_ref` 时以实测音频时长为准，不得重塑语速。

### 拆工作

1. **顺序。** `reel_order` 继承分镜，不重排剧情。
2. **占位。** 每镜 `placeholder_kind`：start-frame / panel / color-block / title-card。优先已锁静帧。
3. **时长。** `held_duration_s` 先取分镜 `duration_s`；有音轨则按 `audio_line_id` 对齐，禁止 `speed_speech_to_fit`。
4. **对白条。** 可烧临时字幕，但不改 `spoken_text`。
5. **合计。** `sum_duration_s` 必须落入 [60,120]。超窗回分镜或剧本，不在 animatic 里加速。
6. **标记。** 未到设计完成的镜标 `provisional`。

### 产物字段

`animatic-plan`：`reel_order` `shot_id` `held_duration_s` `audio_line_id` `placeholder_kind` `sum_duration_s`。

### 失败分支

替换已锁音轨 → `replace_locked_audio`。用 animatic 冒充成片评价技术票的画面品质 → 在评价 Skill 分开。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `editor`, `visual_director`。`r_alignment` = R4, R5。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `shot_list_ref` | yes | ref | shot-list |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `audio_probe_ref` | no | ref | audio-probe-report |
| `edit_decision_ref` | no | ref | edit-decision-notes |
| `start_frame_ref` | no | ref | 已锁静帧，I2V/有限动画的第一帧 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `animatic-plan` | `editor`, `producer`, `validator` |

禁止：`replace_locked_audio`, `speed_speech_to_fit`, `media_generate`。

## 停止

不生成英雄镜头。结构看完即停。
