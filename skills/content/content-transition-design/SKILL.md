---
name: content-transition-design
description: "Choose cut, dissolve, wipe, or still-hold transitions with a narrative reason and frame duration. Use for 转场、dissolve、wipe、硬切; not for dissolving every cut or speeding speech to hide bad joins."
---

# 转场设计

默认硬切。花转场必须有叙事理由。本 Skill 不管剪辑信息密度（那是 editing-rhythm）。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

分镜已有切点，需要决定 **怎么接**；或 animatic 里接缝难看。

## 方法

### 门禁

`shot_list_ref` 与 `episode_script_ref`。无理由的 dissolve 全片禁用。

### 拆工作

1. **默认真切。** 只在需要时填表，不必每刀一行。
2. **类型。** `transition_type`：cut / dissolve / fade / wipe / still-hold / match-cut。match-cut 必须写匹配物。
3. **理由。** `narrative_reason`：时间跳跃、地点跳、主观、情绪释放。没有理由就 cut。
4. **时长。** `duration_frames` 对非 cut 必填；短制 dissolve 通常极短，长溶解吃掉信息。
5. **对。** `from_shot` → `to_shot` 必须存在于分镜。
6. **与格。** 若有 `panel_plan_ref`，scene 类转场才用 fade/wipe。

### 产物字段

`transition-plan`：`from_shot` `to_shot` `transition_type` `duration_frames` `narrative_reason`。

### 失败分支

每刀 dissolve → `default_every_cut_dissolve`。用变速语音遮接缝 → 禁止。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `editor`, `visual_director`。`r_alignment` = R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `shot_list_ref` | yes | ref | shot-list |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `edit_decision_ref` | no | ref | edit-decision-notes |
| `panel_plan_ref` | no | ref | panel-plan |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `transition-plan` | `editor`, `visual_director` |

禁止：`default_every_cut_dissolve`, `speed_speech_to_fit`。

## 停止

不生成转场特效素材。
