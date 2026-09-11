---
name: content-music-bed-design
description: "Design series-level music beds, themes, and cue function for 60–120s narrated drama without covering speech. Use for BGM、配乐、主题曲、音乐床、underscore; not for mixing loudness probes, Foley, TTS, or picking a music Provider."
---

# 配乐与音乐床

解说剧里音乐是 **叙事功能轨**，不是「放一首好听的」。旁白/对白必须可懂。不调用生成模型，不选定产品 Music Provider。

读 [内容契约](../../../docs/content-production-contract.md)。

## 何时用

- R2：系列音乐身份（主题、禁区、跨集是否同一床）
- R3/R4：每集 cue（入/出、钩子、静默）
- 用户说 BGM、配乐、underscore、主题音乐

## 输入与边界

必需：episode 或 series 的叙事功能（hook/pressure/aftermath）、旁白是否为主轨、时长预算 60–120s。

缺权利/许可证 → `blocked`，不得当「先用再说」。生成模型权重的 NC/研究许可不能升级为可发布床。

不做：响度/时长 probe（`content-audio-mix-probe`）、环境声/拟音（`content-ambience-foley`）、改剧本、付费生成。

## 方法

### 门禁

要有 `episode_script_ref`。无 `license_class` 不得 `design-ready`。不写拟音，不测最终响度。

### 拆工作

1. **功能。** 每条 `cues[]` 只选一个 `function`：establish / pressure / release / transition / motif-recall。禁止「史诗/燃」。
2. **diegetic。** `diegetic=true` 当角色能听见（收音机、现场）；要带空间/介质。false 为观众轨 score。切换点必须写明。
3. **系列动机。** `series_motif`：调性/织体家族、2–4 小节动机、禁音色（游戏 UI pluck）。换主题 = 身份失效。
4. **让路。** `duck_against` 列出须让路的说话人/`line_id`。有旁白时低频简单、少人声采样、禁抢词歌词。Duck 深度交给混音 Skill。
5. **结构。** `structure`：intro 淡入、可否循环、outro 是否在钩子前收。禁止硬切循环冒充结构。
6. **许可。** 每条床 `license_class`。`generated-research-only` 默认 `provisional`。

### 产物字段

`music-bed-plan`：`series_motif` `cues` `function` `diegetic` `duck_against` `structure` `license_class`。

### 失败分支

把 CC 当无条件商用 → `assume_cc_commercial`。生成音频 → `media_generate`。

## 输出

`artifact_kind=music-bed-plan`：系列音乐身份、每集 cue 表（功能、diegetic 与否、起止、须让路的说话人）、权利/许可、禁止项。

`r_alignment` 含 R2 与 R4。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `audio_director`。`r_alignment` = R2, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `season_outline_ref` | no | ref | 指向 season-outline 产物 |
| `series_identity_rules_ref` | no | ref | series-identity-rules |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `music-bed-plan` | `audio_director`, `editor`, `producer` |

禁止：`provider_submit`, `media_generate`, `assume_cc_commercial`。

## 停止

不混最终母带，不生成音频，不把 CC 曲当无条件免费商用。超时不得建议重放付费 API。
