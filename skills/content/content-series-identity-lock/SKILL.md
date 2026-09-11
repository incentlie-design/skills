---
name: content-series-identity-lock
description: "Freeze series-level invariants versus allowed episode variation for cast, look, voice, and locations. Use for 系列身份、十集一致性、什么可以变; not for implementing Cast schema or regenerating failed episodes."
---

# 系列身份锁定

观众靠什么认出「这是同一部」。十集不是把 E01 复制九次，也不是每集换一套脸。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **不变量。** 主 Cast 骨相与签名细节、旁白身份、核心场景规则、色彩语言、**系列音乐家族**（主题动机/禁音色）、**地点 room tone 家族**。
2. **变量。** 情绪、临时服装、后出场配角、一次性道具、单集配乐能量、天气/时段环境层。每项写 first-use 与是否需要重评已通过集。
3. **一份策略。** 并行写者只读同一 lock revision。竞争方案从同一 R1 出发，PIC 只选一套。
4. **失效。** 替换脸/声线/主题音乐/主地点底噪必须枚举受影响集；已通过评价的集要重评，不得静默覆盖。
5. **W1 前锁 E01 全部依赖与跨集关键项。**

## 输出

`artifact_kind=series-identity-rules`：不变量、变量、first-use、失效规则。

## 停止

不发明产品 CharacterRevision 字段名当事实。不生成媒体。
