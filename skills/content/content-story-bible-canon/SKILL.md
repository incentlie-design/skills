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

### 门禁

缺 `source_ref` 或 `adaptation_strategy_ref` → `blocked`。outline 可 `provisional`，但不得用它发明源事实。

### 拆工作

1. **实体登记。** 分 `character_id` / `location_id` / `prop_id`。无稳定名用 `proposed:`。禁止 `latest`。
2. **三栏事实。** 每条事实写 `fact_class`。`inference` 不得在下游当 `from_source`。
3. **知识表。** `knowledge_rows`：谁、知道哪条、`learned_in` 哪一集。另列不知道 / 误以为。无人能用未学到的信息行动。
4. **不变量 vs 变量。** 世界规则、核心关系、主线承诺默认不变。服装、临时场地、情绪是变量，写 `first_use` 集。
5. **身体状态。** 死亡/受伤/离场记录 `status` + `as_of_episode`。之后只能闪回或提及，否则连续性应检出。
6. **未兑现。** `open_promises` 列出钩子与应付集。
7. **禁止项。** `forbidden`：破坏世界观的视觉/声音元素。

### 产物字段

`series-canon` 必须含：`entities` `character_id` `location_id` `prop_id` `fact_class` `knowledge_rows` `learned_in` `open_promises` `forbidden` `first_use`。

### 失败分支

关键源事实互相冲突 → `blocked`，不要调和成第三个事实。不生成画像，不 mint 产品 Character schema。

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
