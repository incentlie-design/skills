---
name: content-subtitle-layout
description: "Place narration and dialogue captions in a safe area so vertical 60–120s episodes stay readable without covering faces. Use for 字幕、安全区、解说条; not for rewriting lines, karaoke without timing, or burning unapproved text."
---

# 字幕与安全区

竖屏解说剧字幕是可读性，不是花字。默认避开脸和签名细节。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

`subtitle_mode` 不是 `none`；或评价说「字挡脸/看不清」。

## 方法

### 门禁

`episode_script_ref`、`aspect_ratio`、`subtitle_mode` 必填。无 `aspect_ratio` 不得宣称原生安全区完成。

### 拆工作

1. **模式。** `subtitle_mode`：narration / dialogue / mixed。旁白常开；对白是否上屏由计划决定。
2. **安全区。** `safe_area` 按画幅写边距；9:16 优先中下，避开平台 UI。
3. **容量。** `max_chars` 按一行可读；超了回剧本断句，不缩小到不可读。
4. **对行。** 每条字幕绑 `line_id`。有 `audio_probe_ref` 才可谈逐词；否则只做布局。
5. **避让。** `avoid_faces=true` 默认。签名细节、道具线索同样避开。
6. **烧录。** `burn_in` 默认 false；烧录是交付选择，不是本 Skill 授权。

### 产物字段

`subtitle-layout`：`subtitle_mode` `safe_area` `max_chars` `line_id` `avoid_faces` `burn_in`。

### 失败分支

挡脸 → `cover_faces`。无时码做 karaoke → `karaoke_without_timing`。改对白 → 回写作。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `editor`。`r_alignment` = R4, R5。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `aspect_ratio` | yes | string | 如 9:16 或 16:9；未选则不得宣称原生构图完成 |
| `subtitle_mode` | yes | string | none / narration / dialogue / mixed；竖屏安全区相关 |
| `shot_list_ref` | no | ref | shot-list |
| `audio_probe_ref` | no | ref | audio-probe-report |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `subtitle-layout` | `editor`, `validator` |

禁止：`cover_faces`, `karaoke_without_timing`, `rewrite_dialogue`。

## 停止

不发明产品字幕 schema。无实测音频不承诺逐词高亮。
