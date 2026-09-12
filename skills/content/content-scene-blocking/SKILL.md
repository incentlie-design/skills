---
name: content-scene-blocking
description: "Plan actor and camera positions, eyelines, and screen direction for a scene. Use for 调度、站位、走位、blocking; not for rewriting dialogue, picking lenses as product truth, or generating media."
---

# 场面调度

用站位与走位编码关系：谁靠近、谁占高、谁被挡住。图像模型默认居中肖像，没有调度就会变成幻灯片。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

### 门禁

要有 `episode_script_ref`。无 `location_id` 时平面图标 `provisional`，不得当锁景。不改对白。

### 拆工作

1. **锚点。** `anchors`：门、桌、窗、可重复的空间标记。
2. **站位。** `positions`：每人开场位置与朝向。
3. **视线。** `eyelines` 高度匹配。反打改相机，不改演员看向。
4. **屏幕方向。** 运动体 `screen_direction` L→R 或 R→L，供连续性。
5. **关系。** 权力用距离/遮挡/高低，不用旁白宣布。
6. **关键帧。** `keyframes`：走位的起止与穿过轴线与否。

### 产物字段

`blocking-plan`：`location_id` `anchors` `positions` `eyelines` `screen_direction` `keyframes`。

### 失败分支

调度与已锁对白冲突 → `blocked` 回 `story_director`。不生成图。

## 输出

`artifact_kind=blocking-plan`：平面描述、走位关键帧、视线、与镜头语言的依赖。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`。`r_alignment` = R3。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `location_id` | no | id | 稳定地点 slug |
| `camera_treatment_ref` | no | ref | camera-treatment |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `blocking-plan` | `visual_director` |

禁止：`rewrite_dialogue`, `media_generate`。

## 停止

不生成图，不发明新对白。
