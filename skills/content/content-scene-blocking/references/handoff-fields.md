# 调度交接字段与检查方法

需要可消费文件或多专业交接时使用。字段服务于当前范围，可用 Markdown 表格或 JSON；没有镜头、台词或接触时写 `NOT_APPLICABLE` 及原因，不为填表创造它们。下列是设计字段，不是应用 runtime schema。

## 公共头

结构化运行采用 [公共 envelope](../../../../docs/contracts.md)：`schema_version=1, run_id, change_id, repo, base_commit, artifact_revision`。`artifact_revision` 从 1 起；未提交只能在 commit 类字段写 `uncommitted`，并给实际内容摘要，不能用旧 HEAD 代表新增内容。

每个逻辑产物声明：`artifact_kind`、目标/范围、`input_refs`、本产物 revision、`status`、`maturity`、`open_questions`、`consumer`、`handoff`。可共享一个公共头，以子产物 ID 引用。仅咨询不落盘时按 [内容交接约定](../../../../docs/content-production-contract.md) 直接回答，不伪造 repo/hash。

`input_refs` 至少包含路径或输入段落定位、实体/章节和已知 revision；标出 `source_fact/user_decision/creative_inference/unknown`。原著事实与研究事实应能分别回溯。相同名字不证明版本相同，新增 ID 标 `proposed`；不要为了“精确”发明 Registry URI、资产版本或已锁定状态。

## blocking-plan

| 字段 | 要回答的问题 |
| --- | --- |
| scene/location/source refs | 哪个场景、哪个输入版本、哪些不可改变的动作/台词？ |
| medium + coordinate_basis | 世界坐标、观众/既定机位在何方？屏幕/舞台方向如何对应？未知哪个？ |
| action_id + source beat/line | 当前动作属于哪段输入；新增动作 ID 是否 proposed？ |
| character_id + start/end | 人从哪来、面向哪里、去哪、经哪个出口？他移动还是只转眼/转头？ |
| gaze_target + motivation | 看的具体人/物/环境 cue；为何看，是否已感知？ |
| audience_attention + readability | 观众此刻要读到谁的哪件事？谁会遮住手/接触点/反应？ |
| invariants / change_set | 哪些剧情、身份和状态保留；本候选只改哪些 refs，哪些下游需复核？ |

影视中只有视点明确，才能把世界东西换成屏幕左右；不要擅自决定新机位/焦段。舞台中“舞台左/右”以演员面向主要观众时为固定参照：若观众在南，舞台右=西、舞台左=东。即使演员背向观众，术语不翻转。环形或多面舞台用方位/区域和观众区，不强套这一换算。

## action-state-map

按动作单元给 `before → event → after`。同时给关键帧选择 `selected_instant`，不将动作链缩成一个相互矛盾的静态姿态。

| 状态字段 | 最小内容 |
| --- | --- |
| action/source/phase | 动作ID、源 beat/line/cue；准备、接触/释放、结果或恢复 |
| actor → target | 人物及左/右手或身体部位 → 具体对象/接触点 |
| body/prop state | 人体朝向/姿态；prop_id、全场/可见数量、持有人、手别、接触/支撑、位置、条件、可见性 |
| vector + frame/stage relation | 起点→终点的世界方向；已知时注明屏幕/舞台方向、进出画/场；留场与离场分开 |
| trigger → consequence | 引发变化的具体事件、反应cue；下一个动作为何能开始 |
| unresolved / handoff | 哪个状态缺证据；摄影/分镜、舞监、声音或连续性负责人需核对什么 |

可用“未变，继承 ACTION-x.after”省去重复，但被交接的状态必须能唯一还原。`offscreen` 仍计入场景道具总数；真正退场另记谁带走及出口。一个道具若由两人暂时共同接触，必须列各接触手与释放事件，不能写成两根或两个互相冲突的最终持有人。

**最小安全例（原创方法示意，非来源事实）**：单杯 `PROP-CUP` 从甲右手到桌面。

| 时刻 | 持有人/手 | 接触与支撑 | 数量/结果 |
| --- | --- | --- | --- |
| 准备 | 甲/右手 | 手握杯；杯底未碰桌 | 全场1、可见1 |
| 杯底落桌 | 甲仍接触/右手 | 杯底由桌面支撑，手未松 | 同一只杯；若选此关键帧，不同时画空手离开 |
| 释放后 | 无人 | 杯在桌面，甲右手空 | 全场1、可见1；后续取杯从这里开始 |

后果发生前不能先写成后果状态。预判反应只能由准备阶段已有的可见/可听线索触发；离画人物听到声音可以反应，但要记录感知渠道。

## reaction-cues

每条关键台词/沉默/事件分别记录，避免一个“表演描述”混掉责任。

| 组 | 字段 |
| --- | --- |
| 来源与触发 | scene/line/action/cue refs；谁能看见/听见刺激、触发前后关系；文本与speaker保留原样 |
| speaker action | `speaker_id`、当下对象/目的、可演动作动词、身体/手势、眼神、嘴部可见性（有需要时）；无台词写不适用 |
| listener reaction | `character_id`、`stimulus_ref`、感知依据、`gaze_target`、阶段、外显行为、入口→出口变化 |
| audience attention | 观众应跟随的事件/结果、保持可读所需的停留或遮挡约束；不等于所有角色都看同一点 |
| downstream cue | 声音需要的事件先后/意图与可见动作；不代做TTS、音色身份、口型/字幕毫秒同步 |

触发是门外声音时，可以有人看门、有人守着手里物件、有人暂时不反应；取决于各自可感知信息及当前目标，而不是职位高低。每个被选作关键反应的提示都应让演员知道“发生什么后，做什么”，同时给分镜或舞台负责人可检查的视线目标。

## 交付检查

逐条沿 action-map 还原持物和人物位置；对 reaction-cues 沿刺激顺序走读。对无法还原的状态标 `revise`，来源/结局或输入冲突无法解决则 `blocked/needs_input`。交接列保留项、最小改动、受影响下游及未验证的视线/现场风险；无实物、画面或排练证据时，只能说明文本设计检查完成。
