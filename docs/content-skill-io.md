# Content Skill 输入 / 输出契约

Ticket: https://github.com/incentlie-design/narrated-drama/issues/112

实现时只对照这份契约和 `skills/content/io/*.json`。各 `SKILL.md` 的「参数」表必须与 JSON 同名字段；JSON 是字段权威，Skill 正文是方法。

本契约**不是** narrated-drama 产品 public schema（#95 / T1–T5 仍归产品）。它是 content Skill **调用信封**：角色用同一套字段把产物交给下游。

## 机器可读文件

| 文件 | 权威 |
| --- | --- |
| [envelope.schema.json](../skills/content/io/envelope.schema.json) | 每次调用的输入信封与输出信封 |
| [fields.json](../skills/content/io/fields.json) | 跨 Skill 共享字段名、类型、枚举 |
| [skills.json](../skills/content/io/skills.json) | 每个 Skill 的必填/选填输入、artifact_kind、消费者 |
| [roles.json](../skills/content/io/roles.json) | 角色 → Skill；含 NovelAgent / DirectorAgent 等别名 |

## 共享信封

每次调用：

```json
{
  "schema_version": 1,
  "skill": "content-adaptation-shortform",
  "role": "story_director",
  "r_alignment": ["R1"],
  "inputs": {},
  "context": {
    "language": "zh-Hans",
    "episode_count": 10,
    "duration_s_range": [60, 120]
  }
}
```

每次返回：

```json
{
  "schema_version": 1,
  "skill": "content-adaptation-shortform",
  "role": "story_director",
  "status": "pass",
  "maturity": "provisional",
  "r_alignment": ["R1"],
  "input_refs": [],
  "artifacts": [{"artifact_kind": "season-outline", "artifact_revision": 1, "payload": {}}],
  "open_questions": [],
  "needs_input": [],
  "consumers": ["story_director", "producer"]
}
```

| 字段 | 枚举 / 规则 |
| --- | --- |
| `status` | `pass` / `revise` / `blocked` |
| `maturity` | `provisional` / `design-ready` |
| `r_alignment` | `R1`–`R6` 非空子集 |
| `artifact_revision` | 从 1 起的正整数；不是 git SHA |
| `needs_input` | `blocked` 时列出缺失的 **fields.json 字段名** |

`pass` 只表示本 Skill 范围交完，不是独立 QA、资产锁定、Provider 成功或人类接受。

## 引用对象 `ref`

所有 `*_ref` / `*_refs` 使用同一形状：

```json
{
  "id": "char-lin-wan",
  "kind": "character",
  "revision": 1,
  "uri": "optional/path",
  "sha256": "optional hex"
}
```

- 无稳定 ID 时 `id` 写成 `proposed:<slug>`。
- 无版本时 `revision` 为 `"unknown"` 或 `"provisional"`，禁止写 `latest`。
- `sha256` 仅在对应 bytes 存在时填写。

## 稳定实体 ID

跨 Skill 只用这些 ID 名，不发明同义字段：

`character_id` `location_id` `prop_id` `line_id` `scene_id` `shot_id` `voice_id` `episode_ordinal`

`episode_ordinal` 为 1–10 的整数。说话人用 `character_id` 或旁白槽 `narrator`。

## 角色别名

仓库内未找到名为 `narrated-skills` 且含 `NovelAgent` 类标识符的当前权威目录。下表把历史 drama-agents 研究里的专业角色（Story/Visual/Audio Director）与用户使用的别名对齐，作为 **Skill 路由**，不是 #108 产品 Agent 目录，也不是 runtime。

| role_id | 别名 | 适合的 Skill 类 |
| --- | --- | --- |
| `story_director` | NovelAgent, StoryDirector, Story | 改编、canon、人物声口、单集旁白剧本、漫画格（叙事） |
| `visual_director` | DirectorAgent, VisualDirector, Visual | 外形锁、摄影、调度、分镜、生成身份、漫画格（画面） |
| `audio_director` | AudioDirector, Audio | 声线、音乐床、环境/拟音、混音 probe |
| `editor` | EditorAgent, Editor | 剪辑节奏；消费分镜与混音报告 |
| `validator` | ValidatorAgent, ContinuityReviewer | 连续性、评价量表、prompt 安全 |
| `producer` | EpisodeAgent, PrincipalProducer, PIC-content | 制作计划、系列身份锁；选评价人 |

一次调用只选 **一个** `role` + **一个** `skill`。

## 方法扇出

`SKILL.md` 的「方法」必须按 **阶段**（`###`）拆开，禁止六条口号打天下。典型阶段：门禁 → 拆工作（可并行的分项）→ 产物字段 → 失败分支 → 交还自检。封闭词表、镜号卡、审计轴放在该 Skill 的 `references/`，不复制进 envelope。

`skills.json` 每个 `artifact_kind` 带 `payload_fields`；实现 payload 键必须用这些名字。

## 实现对照顺序

1. 用 `roles.json` 选角色允许的 Skill。
2. 用 `skills.json` 取必填输入；缺则不要调模型，返回 `blocked`。
3. 用 `fields.json` 校验类型/枚举。
4. 输出必须带 envelope；payload 键与对应 `artifact_kind` 文档一致。
5. 禁止项见各 Skill 的 `forbidden`（如 `provider_submit`、`media_generate`）。
