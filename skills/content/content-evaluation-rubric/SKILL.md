---
name: content-evaluation-rubric
description: "Define and apply PASS/REWORK/ABANDON rubrics that separate technical validity from content quality. Use for 评价量表、验收、返工、放弃; not for authoring the candidate, minting Stage Gates, or substituting tests for human review."
---

# 评价量表

代表集与十集必须能被拒绝。技术有效 ≠ 值得看。作者不能当独立评价人。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

本 Skill 可产出政策或一次评价。作者不得当 `reviewer_id`。

### 门禁

要有 `evaluation_subject_ref` 与 `reviewer_id`。无政策时先交 `evaluation-policy`，再评。

### 拆工作

1. **两票。** `tech_ballot`：可播放、时长、hash/probe、资产依赖、effect 安全。`product_ballot`：叙事、旁白、一致性、成本、旁白是否被音乐/环境盖住、地点是否听得出连续。
2. **阈值先写。** `thresholds` 必须可观察，写完再看片子。
3. **绑定。** 评价对象是 exact `evaluation_subject_ref`，不是「这一集感觉」。
4. **三结论。** `verdict`：PASS 才能规模化；REWORK 必须填 `rework_to`（回流的 R 或 Skill）和新 candidate；ABANDON 放弃策略。禁止「再跑模型」当唯一回流。
5. **代表性。** E01 过简不得外推十集。

### 产物字段

- `evaluation-policy`：`tech_ballot` `product_ballot` `thresholds` `reviewer_id_rule`
- `review-record`：`verdict` `evaluation_subject_ref` `tech_result` `product_result` `rework_to` `reviewer_id`

### 失败分支

作者自评当独立接受 → `author_self_accept`。CI 绿当人类接受 → 禁止。

## 输出

`artifact_kind=evaluation-policy`（冻结量表）或 `review-record`（一次评价：verdict、subject refs、理由、回流）。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `validator`, `producer`。`r_alignment` = R1, R5。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `evaluation_subject_ref` | yes | ref | 被评价的 exact bytes 或脚本 revision |
| `reviewer_id` | yes | string | 具名评价人，不得等于作者 |
| `evaluation_policy_ref` | no | ref | 已冻结评价量表 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `evaluation-policy` | `producer`, `validator` |
| `review-record` | `producer` |

禁止：`author_self_accept`, `treat_ci_green_as_acceptance`。

## 停止

不改候选内容。不把 CI 绿当人类接受。
