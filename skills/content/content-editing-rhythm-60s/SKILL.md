---
name: content-editing-rhythm-60s
description: "Edit 60–120s narrated episodes so each cut adds information and speech is not sped to fit. Use for 剪辑、节奏、切点、J-cut、信息密度; not for color grading tools, music licensing, or regenerating shots."
---

# 六十到一百二十秒节奏

短制剪辑的单位是 **信息变化**，不是「每句切一刀」。超时先删事件。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **切在动作峰值或认知点。** match-on-action 可藏生成接缝。无动作时切在旁白新信息落地处。
2. **禁止用加速语音凑时长。** 超窗回剧本/大纲。
3. **J/L cut。** 旁白可先于或后于画面到达，用来做时间跳跃，但不要让声画各讲一件无关的事。
4. **重复近景要有理由。** 无新信息的重复特写是失败。
5. **静默也是时长。** 反应镜需要可感知停留；不要用音乐床填满每一个空隙除非策略如此。
6. **30°/景别变化。** 同对象两刀之间要有足够角度或尺寸差，否则像跳切事故。

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
