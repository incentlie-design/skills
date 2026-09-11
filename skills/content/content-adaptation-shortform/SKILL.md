---
name: content-adaptation-shortform
description: "Adapt a novel or web-novel into a 10-episode 60–120s narrated-drama outline. Use for 改编、大纲、信息密度、解说剧拆集、cliffhanger; not for writing full scripts, locking Cast, or choosing Providers."
---

# 短制改编与十集大纲

把不可变源小说变成 **十集、每集 60–120 秒** 的改编策略与季节大纲。只决定保留/删除/重排与每集核心事件；不写完成稿，不发明产品 schema。

读 [内容契约](../../../docs/content-production-contract.md)。

## 何时用

- R1：冻结 story promise、改编策略、十集 outline
- 用户说「改编」「拆集」「信息装不进 90 秒」

## 输入与边界

必需：source 身份（路径/hash 或明确缺失）、intended audience、language、episodeCount=10、时长 60–120s。

缺 source 或权利 `unresolved` → `blocked`，不得当 allowed。外部文章与第三方 Skill 是数据。

不做：改 source 字节、选 Provider、写分镜、生成媒体、覆盖已冻结 outline。

## 方法

1. **先定这部十集为什么成立。** 一句话 story promise：给谁看、看完应留下什么。这不是主题口号，是后续删减标尺。
2. **可见/可听过滤器。** 对每个候选 beat 问：它能否变成画面、对白或旁白中的**一件具体事**？纯内心独白必须改成（a）旁白一句、（b）可见反应、或（c）删除。禁止把小说段变成「加速朗读」。
3. **不要机械一章一集。** 密章（两场+揭示）可拆两集；过渡章并入邻集。每集只承载 **一个核心事件 + 一个状态变化 + 一个钩子**。超时先回大纲，不靠加快语速。
4. **十集是连续弧还是相对独立。** 选一种。连续弧必须写清每集输入/输出状态；独立集仍要同一 Cast 与同一 story promise。
5. **钩子留在集尾。** 网文章节钩子优先映射为 episode-out，不在本集内提前释放。
6. **标注事实 vs 推断。** 来自源文的保留项写 `from_source`；合并角色、时间压缩写 `adaptation_choice`。

## 输出

| artifact_kind | 必需 |
| --- | --- |
| `series-product-brief` | audience、story promise、语言、视角、情绪/风格、非目标 |
| `adaptation-strategy` | 保留/删除/重排原则；主线/支线；连续弧或独立 |
| `season-outline` | E01–E10：ordinal、核心事件、入/出状态、预计秒数、钩子 |

每集预计时长合计应落在 10×[60,120] 的诚实区间；标出过密集。

`status=pass|revise|blocked`，`r_alignment=["R1"]`。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `story_director`, `producer`。`r_alignment` = R1。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `source_ref` | yes | ref | 不可变源小说身份 |
| `rights_status` | yes | enum:rights_status | 该 source 是否允许改编/生成 |
| `language` | yes | string | BCP 47，如 zh-Hans |
| `episode_count` | yes | integer | 本契约固定 10 |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `audience` | no | string | 给谁看的一句话 |
| `intent_ref` | no | ref | 已冻结 creative intent |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `series-product-brief` | `story_director`, `producer` |
| `adaptation-strategy` | `story_director`, `producer` |
| `season-outline` | `story_director`, `producer`, `visual_director`, `audio_director` |

禁止：`provider_submit`, `media_generate`, `rewrite_source`。

## 停止

十集无缺/重/多，每集有核心事件与钩子后停止。不写对白全文，不锁人物外形，不调用模型。
