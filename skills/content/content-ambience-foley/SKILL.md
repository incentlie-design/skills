---
name: content-ambience-foley
description: Design environmental beds, room tone, and motivated Foley so 60–120s narrated episodes have a place without masking speech. Use for 环境音、背景音、拟音、room tone、现场声; not for score/BGM, loudness delivery, or live sound-effect APIs.
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

1. **三层，不要糊成一条「氛围」。**  
   - **Room tone / 底噪：** 该空间在无人说话时的空气（空调、远交通）。每地点一条，跨镜连续。  
   - **Ambience / 环境床：** 可识别的世界声（雨、市场、虫鸣），标 diegetic。  
   - **Foley / 拟音：** 与画面动作对齐的脚步、布料、门、物件。无对应动作则不配。
2. **听得见谁。** 环境声默认 diegetic。非叙事的转场 whoosh 才是 non-diegetic，且短制里要克制，避免游戏 UI 音色。
3. **地点身份。** 同一 `locationId` 十集复用同一 room tone 家族；时间/天气变化写变量，不换「另一个世界」。
4. **先画面锁定再钉拟音。** 动作峰值对齐切点；旁白段只保留底噪+极淡环境，把冲击声让给无旁白的动作格。
5. **循环与接缝。** 环境床必须可无缝循环或有明确淡入淡出。硬跳的循环是失败，不是风格。
6. **权利。** 库素材、CC、现场录音、生成 SFX 分栏记账。无权的电影扒轨禁止。生成环境声与音乐床一样：许可未审不得发布。

## 输出

`artifact_kind=ambience-foley-plan`：每地点 room tone、环境床、每镜拟音动机、与说话人的让路、权利、循环要求。

## 停止

不写配乐 cue（交给音乐床 Skill），不测最终 LUFS（交给混音 probe），不把「加一点氛围」当成完成。
