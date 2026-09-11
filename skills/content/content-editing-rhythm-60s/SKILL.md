---
name: content-editing-rhythm-60s
description: "Edit 60–120s narrated episodes so each cut adds information and speech is not sped to fit. Use for 剪辑、节奏、切点、J-cut、信息密度; not for color grading tools, music licensing, or regenerating shots."
---

# 六十到一百二十秒节奏

短制剪辑的单位是 **信息变化**，不是「每句切一刀」。超时先删事件。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

### 门禁

要有 `episode_script_ref` 与 `duration_s_range`。`speech_speed_changed` 必须恒为 false。

### 拆工作

1. **信息表。** 按剧本列出每刀应新增的 `info_delta`。无新信息的重复近景删。
2. **切点。** `cut_reason`：action-peak / cognition / reaction。match-on-action 可藏生成接缝。
3. **绑定。** 每刀 `cut_id` 绑 `line_id` 与可选 `shot_id`。
4. **J/L。** 仅当声画讲同一事件。各讲各的禁止。
5. **角度差。** 同对象相邻刀要有景别或 ≥30° 差，否则像事故跳切。
6. **静默。** 反应镜要可感知停留；不要用音乐填满除非 production-plan 如此。
7. **合计。** 各刀 `duration_s` 之和落入窗口。超窗回剧本/大纲，不加速语音。

### 产物字段

`edit-decision-notes`：`cut_id` `line_id` `shot_id` `info_delta` `cut_reason` `duration_s` `speech_speed_changed`。

### 失败分支

加速语音 → 禁止。改身份 → `change_identity`。

## 输出

`artifact_kind=edit-decision-notes`：切点列表、每刀新增信息、预计秒数、与脚本行的绑定。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `editor`。`r_alignment` = R4, R5。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `shot_list_ref` | no | ref | shot-list |
| `panel_plan_ref` | no | ref | panel-plan |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `edit-decision-notes` | `editor`, `validator` |

禁止：`speed_speech_to_fit`, `media_generate`, `change_identity`。

## 停止

不改锁定身份，不调用生成，不把粗剪当验收。
