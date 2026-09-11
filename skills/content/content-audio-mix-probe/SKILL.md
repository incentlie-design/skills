---
name: content-audio-mix-probe
description: "Mix and probe 60–120s spoken-word episode audio for intelligibility, loudness, and measured duration. Use for 混音、响度、LUFS、时长probe、可听度、duck; not for writing BGM/Foley plans, choosing ffmpeg as a product dependency, or calling live TTS."
---

# 混音与时长探针

可播放与时长以 **实际 bytes** 为准。本 Skill 给方法与候选本地工具，不选定产品 MediaProbe 实现。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

本 Skill 测 bytes，不设计音乐/环境。ffmpeg 只是候选夹具，不是产品工具。

### 门禁

`media_ref` 必须能取 bytes 与 `sha256`。零网络默认。无 `loudness_target` 时只报告，不宣布产品标准。

### 拆工作

1. **身份。** 记 `sha256` `byte_length`。空文件/非媒体 → `playable=false`，走负例。
2. **分轨检查。** `stems_present`：旁白、对白、music、ambience、foley。缺轨记下，不替补设计。
3. **可懂度。** `speech_clear`：说话人盖过床。冲击拟音不得与旁白峰值重叠。
4. **时长。** `duration_seconds` 来自实际媒体，必须落入 `duration_s_range`。文件名/sidecar/Provider success 不能升级为合格。
5. **响度。** 仅当产品给了 `loudness_target` 才填 `loudness` 与 `true_peak`。床不必与对白同一 LUFS，但须 duck。
6. **头尾。** 过长无声、瞬间削波、淡入淡出把节目撑出窗 → 失败。
7. **负例。** `negative_cases` 至少考虑：59s、121s、空文件、非媒体。

### 产物字段

`audio-probe-report`：`sha256` `byte_length` `duration_seconds` `playable` `stems_present` `speech_clear` `loudness` `true_peak` `negative_cases`。

### 失败分支

建议付费重放 → `paid_replay`。把 mock 标 live → 禁止。

## 输出

`artifact_kind=audio-probe-report`：byteLength、hash、durationSeconds、playable、loudness 若测了则写方法与数值、负例结果。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `audio_director`, `editor`, `validator`。`r_alignment` = R4, R5。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `media_ref` | yes | ref | 实际媒体 bytes；须能 sha256 |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `music_bed_plan_ref` | no | ref | music-bed-plan |
| `ambience_foley_plan_ref` | no | ref | ambience-foley-plan |
| `loudness_target` | no | object | 可选；产品选择后的 LUFS/true-peak，Skill 不擅自宣布 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `audio-probe-report` | `editor`, `validator`, `producer` |

禁止：`provider_submit`, `paid_replay`, `select_ffmpeg_as_product`。

## 停止

零网络默认。不把 mock WAV 标成 live Provider。超预算或无授权不得建议付费重跑。
