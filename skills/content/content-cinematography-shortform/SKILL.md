---
name: content-cinematography-shortform
description: "Design camera language for 60–120s narrated episodes, including shot size, axis, aspect ratio, and motivated movement. Use for 摄影、景别、轴线、运镜、竖屏构图; not for storyboards, blocking execution, or image generation."
---

# 短制镜头语言

把「观众此刻该发现什么」写成可拍摄/可生成的镜头选择。横竖屏各自原生构图，禁止裁切冒充。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **先注意力，后覆盖。** 每个在场人物看谁/看物；反应不得早于触发。
2. **景别/角度/运动是三轴。** 用封闭词表（ELS–ECU、平/俯/仰、固定/推/摇/随），不要用「电影感」当参数。
3. **轴线。** 每场一条 axis；越轴必须有观众可见过渡。生成图是独立样本，不写轴线就会左右对调。
4. **画幅。** 每种请求画幅单独安置主体、视线空间、字幕区。竖屏用纵深/上下层级，不把横屏填边当原生竖屏。
5. **运动要有动机。** 无必要时固定。运动写清起止、跟随对象、停止点。生成提示的焦段不是实测镜头。

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
