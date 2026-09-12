---
name: content-continuity-review
description: "Audit cross-episode continuity of knowledge, costume, props, geography, injuries, and screen direction. Use for 连续性、穿帮、E05到E06交接; not for rewriting story, regenerating media, or independent QA acceptance."
---

# 连续性审查

在并行写集之后，检查十集是否仍是同一世界。作者自检不是独立评价。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

轴清单见 [audit-axes](references/audit-axes.md)。作者自检不是本 Skill。不热修候选。

### 门禁

要有 `episode_script_refs` 与 `series_canon_ref`。未看过的图/片不得宣称画面一致。

### 拆工作（轴可并行，报告一次汇总）

对每个 `axis` 出 finding 或明确 `checked_scope=unrun`：

1. `knowledge` 与误用未学信息；闪回标 mentions。
2. `wardrobe` / `props` / `injury`：camera vs production continuity。
3. `geography` / `axis_screen`。
4. `identity_string`：视觉句与声线未被改写。
5. `e05_e06`：只一份交接，两边各改一版 → `blocked`。
6. `day_night` / `travel`。

每条 finding：`axis` `episode_ordinal` `conflict` `severity` `owner_role`。

### 产物字段

`continuity-report`：`findings` `axis` `episode_ordinal` `conflict` `severity` `owner_role` `checked_scope`。

### 失败分支

在审查里改剧本 → `hot_fix_candidate`。未看媒体宣称一致 → `claim_unseen_media`。

## 输出

`artifact_kind=continuity-report`：问题列表（id、集、事实冲突、建议回流的 R 或写者）、无问题项也要写已检查范围。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `validator`。`r_alignment` = R3, R6。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_refs` | yes | ref[] | 多集脚本，连续性用 |
| `series_canon_ref` | yes | ref | 指向 series-canon 产物 |
| `character_visual_lock_ref` | no | ref | 指向 character-visual-lock |
| `voice_identity_pack_ref` | no | ref | voice-identity-pack |
| `shot_list_refs` | no | ref[] | 多集分镜 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `continuity-report` | `producer`, `story_director`, `visual_director` |

禁止：`hot_fix_candidate`, `claim_unseen_media`。

## 停止

不在审查里热修剧本。回流到唯一 owner。不宣称画面一致，除非实际看过图/片。
