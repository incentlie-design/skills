---
name: content-audio-mix-probe
description: "Mix and probe 60–120s spoken-word episode audio for intelligibility, loudness, and measured duration. Use for 混音、响度、LUFS、时长probe、可听度、duck; not for writing BGM/Foley plans, choosing ffmpeg as a product dependency, or calling live TTS."
---

# 混音与时长探针

可播放与时长以 **实际 bytes** 为准。本 Skill 给方法与候选本地工具，不选定产品 MediaProbe 实现。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **可懂度优先。** 旁白/对白盖过音乐床、环境床和拟音。对白与掩蔽声的关系先用耳朵，再用响度描述符。
2. **分轨再合。** 至少分开：旁白、对白、music bed、ambience/room tone、foley。音乐与环境的功能设计分别交给 `content-music-bed-design` 与 `content-ambience-foley`；本 Skill 只处理让路、响度与时长。
3. **响度目标是产品选择。** 记录候选：广播 EBU R128 −23 LUFS；流媒体/手机解说常落在 −20 到 −16；播客常见 −16 LKFS。Skill 不擅自宣布产品标准。床与环境是艺术 stem，不必每条都对准同一 LUFS，但说话人段必须让路（duck）。
4. **短制。** 关注 true peak 与短时过响。冲击拟音不要与旁白峰值重叠。
5. **时长。** 用实际媒体 duration；∈[60,120] 秒。文件名、sidecar、Provider success 都不能升级为合格。负例：59s、121s、空文件、非媒体。
6. **头尾。** 避免无声过长或瞬间削波开头。音乐/环境淡入淡出不得把节目时长撑出窗。
7. **候选工具。** 本地可用 ffprobe / loudnorm 作探针夹具；**ffmpeg 不是已选产品工具**。

## 输出

`artifact_kind=audio-probe-report`：byteLength、hash、durationSeconds、playable、loudness 若测了则写方法与数值、负例结果。

## 停止

零网络默认。不把 mock WAV 标成 live Provider。超预算或无授权不得建议付费重跑。
