---
name: content-production-plan-shortform
description: "Plan bounded short-form production: media form, parallel writers, cost stops, and whole-episode rework. Use for 制作计划、并行、成本上限、返工; not for Architecture changes, Provider live runs, or Stage Gates."
---

# 短制制作计划

把 R4/R6 的生产策略写成可执行边界：谁写哪集、什么算失败、何时停。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

### 门禁

要有 `media_form`、`season_outline_ref`、`budget_limits`。本 Skill 不授权 paid/live。

### 拆工作

1. **形态树。** `media_form`：`audio_only` / `stills_plus_audio` / `audiovisual`。未选不得假设视频。静帧+音轨还要 `audio_layers`：dry / dry+ambience / +music-bed。
2. **自动化。** `automation_level`：全自动 / 人锁资产后自动 / 人工 fallback。未知后禁止自动换 Provider。
3. **写者。** `writer_map`：一人一集一目录。plan、资产定义、总清单单写者。
4. **返工。** `rework_policy`：无局部 revision 时整集重做，保留旧 evidence。
5. **上限。** `limits`：调用、成本、时间、query，以及音乐/环境 `license_class` 停止条件。
6. **窗口。** `w1_w2_gate`：代表集未 PASS 不得批量。

### 产物字段

`production-plan`：`media_form` `audio_layers` `automation_level` `writer_map` `rework_policy` `limits` `w1_w2_gate`。

### 失败分支

宣称十个文件即 1.0 → `claim_release`。付费 live → `paid_live_authorize`。

## 输出

`artifact_kind=production-plan`：形态、并行表、上限、失败策略、provenance 标记（hybrid/manual/live 候选）。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `producer`。`r_alignment` = R4, R6。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `media_form` | yes | enum:media_form | 成品形态 |
| `season_outline_ref` | yes | ref | 指向 season-outline 产物 |
| `budget_limits` | yes | object | 调用/成本/时间上限与停止条件 |
| `series_identity_rules_ref` | no | ref | series-identity-rules |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `production-plan` | `producer`, `story_director`, `visual_director`, `audio_director`, `editor` |

禁止：`paid_live_authorize`, `claim_release`。

## 停止

不授权 paid/live。不把十个文件叫 1.0。
