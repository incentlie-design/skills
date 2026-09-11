---
name: content-music-bed-design
description: Design series-level music beds, themes, and cue function for 60–120s narrated drama without covering speech. Use for BGM、配乐、主题曲、音乐床、underscore; not for mixing loudness probes, Foley, TTS, or picking a music Provider.
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

1. **先定功能，后选气质。** 每个 cue 只回答一件事：建立世界、加压、释放、转场、主题回忆。禁止用「史诗/燃」当参数。
2. **剧情内 vs 观众轨。** 角色能听到的（收音机、现场演奏）是 diegetic，要带空间/介质（喇叭、房间）；角色听不到的 score 是 non-diegetic。混用必须写明切换点，不能让听众以为角色在听主题曲。
3. **系列不变量。** 十集共用：调性/织体家族、主题动机（可短到 2–4 小节）、禁止音色（例如游戏 UI pluck）。每集可变：能量、密度、是否有鼓。换主题 = 系列身份失效，需重评已通过集。
4. **给旁白留空。** 有旁白的段落：低频简单、少人声采样、少歌词。歌词与旁白抢语义一律删词或静音。Duck 深度与目标响度交给混音 Skill，这里只标「须让路」。
5. **60–120s 结构。** 写 intro 淡入、中段是否可循环、outro 是否在钩子前收。禁止用加速或硬切循环掩盖没有结构的床。
6. **权利记账。** 每条床：`licensed-library` / `cc-with-attribution` / `original-commission` / `generated-research-only`。生成结果默认 `provisional`，未审许可不得标 `design-ready`。

## 输出

`artifact_kind=music-bed-plan`：系列音乐身份、每集 cue 表（功能、diegetic 与否、起止、须让路的说话人）、权利/许可、禁止项。

`r_alignment` 含 R2 与 R4。

## 停止

不混最终母带，不生成音频，不把 CC 曲当无条件免费商用。超时不得建议重放付费 API。
