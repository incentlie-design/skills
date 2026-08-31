# 可消费的音频交接

用于输出三种计划，不是应用 Registry schema，也不替代上游脚本或声音身份。可以用 JSON 或等价表格；保持字段含义和逐行引用。输出文件建议在已授权目录的新 revision 子目录命名 `audio-script.json`、`performance-plan.json`、`sound-cue-sheet.json`；只回复时直接给相应表格，无需创建仓库。

## 共同绑定

落盘运行沿用公共 `schema_version=1, run_id, change_id, repo, base_commit, artifact_revision`；路径相对目标 repo，artifact_revision 是正整数。新内容未提交时相应 commit 字段为 uncommitted 加摘要，不把已有 HEAD 当成新文件版本。咨询不伪造这些运行事实，但仍标明下面的设计范围和来源。

每份产物保留：

- `artifact_kind`：audio-script / performance-plan / sound-cue-sheet；`scope`、`artifact_revision`、`stage`（design_ready / provisional / evidence_review）。
- `input_refs`：实际路径/章节/实体及已知 revision；版本未知标 unknown/provisional。输入仅以消息给出时引用该消息/段落，文件名是用户提供的定位信息，不声称已读取磁盘。
- `basis`：分别记录 source_fact、user_decision、research_fact、creative_inference、unknown。一个音乐提议不自动成为 research_fact。
- `open_questions`、`consumer`；`handoff` 含 `status=pass|revise|blocked`、status_scope、reason、保留项、待执行动作/证据、next_owner。未知个人写职责角色，不发明审批人。
- `checks`：只记录实际执行证据与来源；未测记 not_run，not_applicable 给理由。设计完整性与媒体质量是两个不同检查范围。

## audio-script：谁说哪些词

逐行记录 `line_id, scene_id, speaker, character_id, source_ref, voice_ref, spoken_text, mode`。source/voice ref 均含路径/实体与 revision；未选声音时 voice_ref=null、binding_status=needs_input。mode 可为 narration/dialogue；唱词或非语言发声只在输入要求时单列，不能把静默角色改成 TTS 角色。

原文与 speaker 以所选脚本版本为准。额外的导演注、发音表引用、场景上下文不进入 spoken_text。当原文明确要说“one connected thought”时保留原文；当它是表演备注时绝不口播，不能靠全局关键词删除解决。

## performance-plan：同一个声音如何行动

逐个语义 take group 记录：

- `group_id`（新建时标 proposed）、有序 `line_ids`、同一 speaker/voice_ref、逐行文本映射；不要合并后丢失 line ID。
- `objective`、对谁说/所求反应、阻力与 `turn`（策略变化）；按行给非口播的情绪强度、词重、速度变化、气息/句尾和身体动作。描述可执行行为，不堆“更感人、更戏剧化”。
- `context` 与 `pronunciation_ref` 分开；未提供发音知识就列问题，不把拼音/音标直接替换原词。
- `pause_or_handoff`：绑定前后 line/动作并给理由；`timing_basis`=untimed/estimated/measured。estimated 附估算方法、范围与置信度，measured 附音频版本/证据；不互相填充。

如为录音或生成适配器交接，分开 text_segments、identity_ref、performance_segments、context、pronunciation_ref；默认 offline、submit=false。消费者不支持非口播控制字段时，标 unsupported 并交人工导演/另行适配；不能把指导拼回 text 来绕过限制，也不能因此更换模型。

## sound-cue-sheet：声音为什么在此刻出现

区分 narration、dialogue、SFX/foley、ambience、music 逻辑层；可给 voice bus 汇总关系，但旁白与对白仍能分别定位。未用层记录 omission_reason，不强制非空四轨/五轨。

每个 cue 记录 `cue_id`（新建标 proposed）、layer、绑定 line/scene/动作/可选 shot 的 `anchor_refs`、叙事目的、空间距离/前后景、进入/退出条件、覆盖范围及声音优先级。计划无秒数时用“L04前的B门外话头”之类相对锚点；可估时间但不能伪造 actual_cue。实际声音资产只有输入已提供时才填 asset_ref/revision。

音乐另含 `cultural_basis`（确切来源/限制或明确无特定文化归属）、时代要求、动机如何随场景变化、人声出现时如何避让；缺来源的文化声称列 held cue，不输出伪造传统。环境声给叙事变化和连续空间衔接；拟音给导致声响的动作。

混音交接说明旁白/对白可懂度、相邻主观电平、留白的空间底声、非人声避让策略；仅在项目给定规范时绑定响度/峰值目标，否则列待定。消费者需回传实际 take、stem、时间线 revision、测量/试听范围，才能进入媒体验收。

## 局部修复交接

复用共同绑定，附 affected_line_ids/cue_ids、source_take/stem/timeline refs、观察与假设、保留项、最小动作、before/after 映射（未执行 after 留 planned）、受影响下游与待复核项。剪短停顿通常保留语音内容/身份，移动相关声音轨、字幕及画面锚点；是否真正同步由执行后证据证明。不要把 repair proposal 写成已修复文件。
