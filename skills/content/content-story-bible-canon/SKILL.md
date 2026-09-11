---
name: content-story-bible-canon
description: "Build a series canon / story bible that separates source facts, adaptation choices and inferences. Use for story bible、canon、谁知道什么、世界观规则; not for character portraits, scripts, or product Character schema."
---

# 系列 Canon 与故事圣经

维护跨十集可引用的事实表。目标是让并行写者**不必猜**世界规则和角色知识。不拥有 #95 的产品契约，只提供方法与交接字段。

读 [内容契约](../../../docs/content-production-contract.md)。

## 输入

必需：source 引用、改编策略/outline（可 `provisional`）。建议：已有 Cast 草案。

## 方法

1. **三栏记账。** 每条 canon 记录 `from_source` / `adaptation_choice` / `inference`。推断不得升级为源事实。
2. **知识边界。** 对每个重要角色维护「已知道 / 不知道 / 误以为」。无人能依据自己没学到的信息行动。
3. **稳定 ID。** 人物、地点、道具用稳定 slug；无 ID 时 `proposed:`。禁止用「最新一版」指代。
4. **可变 vs 不变量。** 世界规则、核心关系、主线承诺默认不变量。服装、临时场地、情绪是变量，必须标明 first-use 集。
5. **死亡/受伤/离场。** 若发生，记录 `status` 与 `as_of_episode`。后续出场必须是闪回/提及，并在连续性审查里可检出。

## 输出

`artifact_kind=series-canon`：

- 实体表（id、kind、不变特征、可变特征、first-use）
- 知识表（character × fact × learned_in）
- 开放承诺/未兑现钩子
- 禁止清单（破坏世界观的视觉/声音元素）

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `story_director`。`r_alignment` = R1, R2。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `source_ref` | yes | ref | 不可变源小说身份 |
| `adaptation_strategy_ref` | yes | ref | 指向 adaptation-strategy 产物 |
| `season_outline_ref` | no | ref | 指向 season-outline 产物 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `series-canon` | `story_director`, `visual_director`, `audio_director`, `validator` |

禁止：`provider_submit`, `media_generate`, `mint_product_schema`。

## 停止

缺关键源事实时 `blocked`。不生成画像，不把 canon 写成产品 JSON schema。
