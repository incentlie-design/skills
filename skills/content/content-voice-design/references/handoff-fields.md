# 声音身份交接字段

用于实际产物交接，不是新应用 schema、Registry 或执行引擎。纯咨询可使用下列简表，不伪造 repo/commit；落盘沿用 [公共 envelope](../../../../docs/contracts.md) 与 [内容约定](../../../../docs/content-production-contract.md)。每份文件顶层含 `schema_version=1`、`run_id`、`change_id`、`repo`、`base_commit`、正整数 `artifact_revision`；新增内容尚未提交时，内容的 commit 字段为 `uncommitted` 并附实际摘要，基线 HEAD 不能代表新增内容。

每个产物含 `artifact_kind`、目标/`scope`、`input_refs`（路径/章节/实体及已知 revision）、自身 revision、`open_questions`、`consumers`、`handoff`。同文件多产物可共享顶层绑定，每个产物仍保留 kind/范围/来源。来源无版本写 unknown/provisional；用户在当前请求中给的事实可以绑定“当前请求/角色卡/指定 revision”，不能伪装为已批准资产。

| artifact_kind | 最少可消费内容 | 消费者 |
| --- | --- | --- |
| `voice-bible` | 角色/旁白 ID 与来源；适用媒介/语言/地域；年龄、音域、共鸣、质感、力度、节奏；身份不变量、允许的情绪/身体状态变体、禁止漂移；专名发音意图/缺口；旁白知识边界（适用时）；旧选中版本或 proposed 新方向 | 声音表演/制作、连续性复核、导演/选角 |
| `voice-design-prompt` | proposed 候选 ID、目标与保留轴、Design/Remix 意图及来源权限、结构化声音描述、可直接使用的 prompt；分开的统一试读文本与 revision；供应商适配状态/未知设置；禁项；与 voice-bible 的 ref/revision | 授权生成适配器、演员/选角试听组织者 |
| `comparison-lock-record` | 候选及音频 ref/revision（未生成则明示）；比较条件和差异、试听人/证据/片段、已知取舍与未测项；selection_intent/具体选择/选型人；选中参考 take、实际参数与处理链；允许变体；外部保存/注册状态；受影响下游和下一责任人 | 用户/选型人、授权资产管理员、声音制作与连续性复核 |

分开四类依据：`source_facts`（角色材料）、`research_facts`（有出处的语音/文化资料）、`user_decisions`、`creative_proposals`；`unknowns` 不充当事实。声音质感提案不能反写成角色资料事实。

## 比较条件

对每个实际样本记录以下可用字段；供应商不支持的写 `not_applicable` 并说明原因，未收集写 `unknown`，不要猜默认值：

- 候选/源声音 ID 与版本、模式、provider/endpoint、model/API version、prompt 及试读文本原文/revision；若存在另记规范化后文本。
- seed、guidance/enhancement、stability/similarity/style/speaker boost/speed 等实际设置（只记录适用字段）、语言/发音词典版本、前后文本/音频上下文。
- 媒体路径与摘要、原始/处理后版本、格式/采样率、剪辑/变速/EQ/压缩等处理顺序与参数；若有响度测量，附方法/值，否则写未测。
- 试听者、日期、环境/播放音量可比性、片段标识与反馈来源。用户反馈可用但标明“用户报告”，不能冒充 agent 直接试听。不能测量的声学项明确 not_run。

## 状态不要互相替代

`status=pass|revise|blocked` 是交接范围结论，另列事实字段：

- `design_state`：proposed / design_ready。
- `generation_state`、`listening_state`：not_run / executed；executed 必须有对应媒体或试听记录。可以写“用户试听 executed，agent 试听 not_run”。
- `selection_state`：pending / intent_only / selected；selected 要绑定有权选型者与精确候选。
- `lock_state`：not_locked / record_complete。record_complete 只表示可复用锁定记录具备选中媒体、生成条件、允许变体、决定证据；不意味着外部注册已执行，也不保证随机生成逐次相同。
- `external_registration`：not_requested / pending / confirmed；confirmed 需实际回执。没有真实 voice ID 不填写示例 ID 冒充供应商结果。

设计已完成但无音频时，可将文档交接 `pass` 且保留 not_run/pending/not_locked；要求直接听选而缺材料时 `blocked`，给最小补充清单。作者自查不等于独立评审；选择权归用户/指定选型人，最终接收归下游责任人。

`handoff` 最少列产物路径/章节、实际证据、未解决问题、下一责任人、允许的下一步与禁止动作。局部修订生成新 revision，标记哪些下游仍需复核；不自动作废所有角色或替换批准 take。
