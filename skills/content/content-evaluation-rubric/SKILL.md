---
name: content-evaluation-rubric
description: Define and apply PASS/REWORK/ABANDON rubrics that separate technical validity from content quality. Use for 评价量表、验收、返工、放弃; not for authoring the candidate, minting Stage Gates, or substituting tests for human review.
---

# 评价量表

代表集与十集必须能被拒绝。技术有效 ≠ 值得看。作者不能当独立评价人。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **两票。** 技术票：可播放、时长、hash/probe、资产依赖、effect 安全。产品票：叙事、旁白、一致性、成本是否可接受。
2. **三结论。** PASS 才能规模化；REWORK 必须指出回流的 R/T 与新 candidate；ABANDON 放弃当前策略。禁止「再跑一次模型」当唯一回流。
3. **绑定 exact subject。** 评价对象是具体 bytes/hash/脚本 revision，不是「这一集感觉」。
4. **阈值先写后看。** 叙事钩子、角色可辨、60–120s 自然、声画是否互相解释，都要可观察。
5. **代表性。** E01 若过简，不得外推十集。

## 输出

`artifact_kind=evaluation-policy`（冻结量表）或 `review-record`（一次评价：verdict、subject refs、理由、回流）。

## 停止

不改候选内容。不把 CI 绿当人类接受。
