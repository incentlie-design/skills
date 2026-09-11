---
name: content-manga-panel-language
description: "Apply comics/manga panel grammar (closure, gutters, transitions) to narrated-drama still sequences. Use for 分格、漫画、条漫、动态漫画、gutter; not for full scripts, anime production management, or model choice."
---

# 漫画格语言

解说剧/动态漫画是 **有限运动的顺序图**。意义经常发生在格与格之间。旁白不要把读者已经补完的动作再讲一遍。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **六种转场。** moment / action / subject / scene / aspect / non-sequitur。默认多用 action 与 subject；aspect 用于情绪停顿；scene 用于时空跳跃。
2. **一拍一信息。** 一格（或一切）只新增一件观众必须知道的事。
3. **gutter 是语法。** 能靠闭合补上的过程不要画成连环重复近景。
4. **字图分工。** 旁白可与画面对位、对比或让一方主导；禁止双通道说同一句话。
5. **阅读路径不是万能 Z。** 条漫/竖屏是单列流；不要按双页漫画的 page-turn 假设来切。

## 输出

`artifact_kind=panel-plan`：每格信息变化、转场类型、旁白是否重复画面、时长暗示。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `story_director`, `visual_director`。`r_alignment` = R3。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `shot_list_ref` | no | ref | shot-list |
| `duration_s_range` | no | int_pair | 每集体测秒数闭区间，固定 [60, 120] |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `panel-plan` | `visual_director`, `editor` |

禁止：`replace_shot_list`, `media_generate`。

## 停止

不替代分镜表的生产字段，不把漫画理论当产品 UI。
