# 全剧方案输出与引用

写四类产物时读取。可压缩为同一答复的四个区块；不要为了满足标题制造空文件。这是创作交接字段，不是旧应用 JSON schema 或运行时验证器。

## 共同约定

每份产物带 `artifact_kind`、目标/覆盖范围、实际 `input_refs`、正整数 `artifact_revision`、`open_questions`、`consumer` 和 `handoff`（或定位到共同 handoff 的引用）。落盘时沿用公共 envelope；可放在用户输出目录的 `adaptation/r<revision>/`，名称为四类产物名及 `handoff.json`。没有文件写入请求就在答复中交付，不伪造 repo、commit、读取记录或媒体状态。

- source ref 最少含路径/URI、章节/段落/实体定位和已知 revision；未知写 `unknown`，临时定位标 `provisional`。只引理解/校核所需短摘录，不复制全书。源段落编号可自行提出，但不能伪称原书章号。
- 每项关键主张有 ID、类别、引用；类别区分 `source_fact`、`research_fact`、`user_decision`、`inference`、`adaptation_proposal`、`unknown`。推断附理由，提议附目的/影响/待决状态；研究结论不能被写成原著事实。
- 已有 `character_id/location_id/prop_id` 沿用选定版本；没有时提出稳定 ID 并标 `proposed`，不等于注册。仅保留当前全剧决策所需实体；不在拆集阶段凭空创建 shot/line 资产。episode/event/claim/setup 使用稳定局部 ID，供后续回指。
- 新候选不能覆盖批准内容。修改时写父 revision、实际改变/保留项、受影响来源与下游；未改文件可明确引用旧版本，不无端复制或重生成。

## 四类产物

| artifact_kind | 最小可用内容 | 消费者 |
| --- | --- | --- |
| `series-brief` | premise、核心戏剧问题、观众/形式目标、覆盖范围、集数与时长依据、调性/语言、旁白及叙述时点、保留/可变边界、约束来源、可观察验收与未知 | 单集作者/生产计划 |
| `story-bible` | 世界规则与关键源事实；主要人物欲望/策略/关键选择/代价/终局；核心关系变化；受保护事件及必要前置条件；知识边界表和不可违反项 | 人物发展/单集作者/连续性评审 |
| `series-outline` | 故事引擎；有因果引用的阶段/转折；人物与关系弧线；源事件去向表；跨集 setup/payoff；结局与开放线 | 单集作者/连续性评审 |
| `episode-map` | 有序单集任务，使用下面字段；未定集数时先给阶段映射和待决拆法，不强行承诺精确集数 | 单集作者/生产计划 |

## 单集任务的可消费字段

- `episode_id` / `sequence` / `source_refs` / `focal_character_id`：本集定位和主要人物。
- `entry_state` / `dramatic_question`：从上一集继承什么状态，本集回答什么问题。
- `goal` / `obstacle` / `choice` / `price` / `changed_state`：谁主动做什么、为何做、造成什么后果。非线性叙事分别标故事时序和呈现顺序。
- `opening_hook` / `closing_hook` / `next_dependency`：如何接续、完成哪项局部承诺、留下哪个具体问题；终集可关闭主线，next_dependency 可为有理由的 none。
- `must_include` / `forbidden_early_events` / `protected_future_refs`：必需桥梁、不得提前消费的事件、后续正典前置条件。
- `knowledge_and_reveal`：本集新增观众信息；相关人物/旁白的得知时点与依据；故意暂缓的信息及理由。可引用 story-bible 的知识表，不能只写“有限视角”。
- `setup_refs` / `payoff_refs` / `open_questions`：使用稳定条目 ID，不靠模糊的“以后再讲”。
- `duration_target_or_range` / `density_note`：用户时长目标或 provisional 建议，说明给人物选择/反应留出的空间；未有台词/录音不声称实际秒数已验证。

知识表的每个关键条目至少有 `fact_ref, story_time, audience_reveal, character_acquisition, narrator_basis, holdback`。把“国王事后听到报告”写为旁白依据，不能据此让旅途当时的国王作出知情决策。

回收表每行至少有 `setup_id, promise_or_rule, source_refs, setup_episode, payoff_episode_or_open, responsible_character, prerequisites, status`；status 使用 `planned/open/protected` 等计划状态，不把未来回收写成生产完成。源事件去向表记录 `event_ref → episode/stage → retain/reorder/merge/omit → reason/impact`，删改重要正典须明确用户决定，不能靠压缩自动放行。

## Handoff 与验收边界

handoff 沿用公共 `status=pass/revise/blocked`：`pass` 只表示范围内方案可交接，不能代表独立审批或已生成；重大取舍待定用 `revise`，关键来源不可用用 `blocked` 并附 `needs_input`。列产物路径/区块与 revision、已检查的范围、未检查项、下一责任人、最小问题和影响集。不为每个未知启动研究，不为交接调用全部专业 Skill。

交接前检查：关键源事件都有去向；主要转折有前因；人物有选择/后果；每个揭示符合角色与旁白得知渠道；计划回收有已设置的前置条件；时长目标未以删动机或提前消耗后续救援来凑数。自查结果与独立评审状态分开记录。
