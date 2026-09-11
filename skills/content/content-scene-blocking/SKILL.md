---
name: content-scene-blocking
description: "Plan actor and camera positions, eyelines, and screen direction for a scene. Use for 调度、站位、走位、blocking; not for rewriting dialogue, picking lenses as product truth, or generating media."
---

# 场面调度

用站位与走位编码关系：谁靠近、谁占高、谁被挡住。图像模型默认居中肖像，没有调度就会变成幻灯片。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **先平面图，后镜头。** 锚点（门、桌、窗）+ 每人位置 + 朝向。
2. **视线高度匹配。** 反打时不要让演员改看向；改的是相机。
3. **屏幕方向。** 运动体 L→R / R→L 写入场次，供连续性审查。
4. **关系即空间。** 权力变化用距离/遮挡/高低，而不是旁白宣布。
5. **不改已锁对白。** 调度与台词冲突时 `blocked` 回剧本写者。

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
