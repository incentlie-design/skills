---
name: content-ambience-foley
description: "Design environmental beds, room tone, and motivated Foley so 60–120s narrated episodes have a place without masking speech. Use for 环境音、背景音、拟音、room tone、现场声; not for score/BGM, loudness delivery, or live sound-effect APIs."
---

# 环境声、背景音与拟音

背景音先让观众知道 **在哪**，拟音让可见动作有重量。二者都不得盖过旁白。不调用 SFX API，不选定产品音频工具。

读 [内容契约](../../../docs/content-production-contract.md)。

## 何时用

- 静帧+音轨或 audio-only 需要「空间」而不是干声
- 分镜 `sound` 列要落地为环境/动作声
- 跨集同一地点必须听得出是同一间房

## 输入

必需：地点/场景 ID 或明确缺失、哪些动作可见、旁白是否连续。建议：视觉锁定与分镜时长。

## 方法

### 门禁

要有 `episode_script_ref`。不写配乐 cue。无权电影扒轨禁止。

### 拆工作

1. **地点列表。** 从剧本收 `location_id`。同一地点十集共用 `room_tone_family`。
2. **三层。** 不要糊成一条氛围：`room_tone_family`（无人时的空气） / `ambience_bed`（可识别世界声，默认 diegetic） / `foley_cues`（只对可见动作）。
3. **whoosh。** 非叙事转场才可 non-diegetic，短制克制，禁游戏 UI 音色。
4. **天气变量。** 时段/天气是变量，不换「另一个世界」。
5. **对齐。** 有 `shot_list_ref` 时拟音钉在动作峰值；旁白段只留底噪+极淡环境。
6. **循环。** `loop_rule`：无缝循环或明确淡入淡出。硬跳失败。
7. **许可。** 每层 `license_class`。

### 产物字段

`ambience-foley-plan`：`location_id` `room_tone_family` `ambience_bed` `foley_cues` `loop_rule` `license_class`。

### 失败分支

写音乐功能 → `write_music_cues`。无对应动作的拟音删掉。

## 输出

`artifact_kind=ambience-foley-plan`：每地点 room tone、环境床、每镜拟音动机、与说话人的让路、权利、循环要求。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `audio_director`。`r_alignment` = R2, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `shot_list_ref` | no | ref | shot-list |
| `location_ids` | no | id[] | 本集出现的地点 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `ambience-foley-plan` | `audio_director`, `editor` |

禁止：`write_music_cues`, `provider_submit`, `media_generate`。

## 停止

不写配乐 cue（交给音乐床 Skill），不测最终 LUFS（交给混音 probe），不把「加一点氛围」当成完成。
