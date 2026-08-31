# 输出结构与可生成帧的写法

这是可由文件交接的设计 schema，不是旧 Drama 应用或供应商 JSON schema。四类产物共用一次输入快照；不复制 Registry/CAS/校验器。字段无对象时用空数组并给理由，不用臆造实体填齐。

## 共同字段

落盘产物采用 [公共 envelope](../../../../docs/contracts.md) 和 [内容补充](../../../../docs/content-production-contract.md)：`schema_version=1, run_id, change_id, repo, base_commit, artifact_revision`。未提交版本写 `artifact_commit=uncommitted` 加内容摘要，不能用当前 HEAD 冒充新内容；咨询答复不造 envelope 事实。

每份产物还含：`artifact_kind, scope, input_refs, readiness, open_questions, consumers, handoff`。`readiness=provisional|prompt_ready`：前者仍有未决设计/时间项；后者仅表示提示词所需文本及引用已齐。选定文本资产可以支持文本计划，但不能声称已检查图像；若下游需要尚缺的参考图，列生成阻断。`execution_status=not_run` 是本 Skill 的媒体执行状态。

一个 `ref` 写 `{source, entity_id, revision, authority, selected_by, representation}`。source 定位到目标 repo 相对路径/章节或明确命名的输入片段；revision 未知写 `unknown`，authority 用实际的 `user_selected|approved|provisional|unknown`，representation 区分 `text_design|image|audio|script` 等。未知不得假称已锁定；fixture 保留标识。新 ID 标 proposed，不是登记操作。

## 四类产物

| artifact_kind / 文件 | 核心字段 |
| --- | --- |
| `scene-breakdown` / scene-breakdown.json | `scenes[]`: scene_id, order, script_refs, line_ids, movement_ids, objective/obstacle/turn, location_ref, style_ref, time/weather（未知则明示）, characters, state_in/out, axis/zones, attention_priority, prop_states, transition_to_next, audio_notes, timing_basis。台词/动作归属不重复、不遗漏；声音桥可跨场引用同一 line。 |
| `storyboard` / storyboard.json | `shots[]`: shot_id, scene_id, order, source_refs, function, visible_subjects, speaker/listener/reaction_of, line_bindings, scale/angle/axis, action_in/out, frame_ids, cut_motivation/match_point, motion_intent, timing。可选 `planning_board` 明示 kind、page_id、panel→frame_ids、注释；示意页不能列为已生成成片资产。 |
| `frame-prompts` / frame-prompts.json | `frames[]`: 下节完整帧字段及 prompt_sections；每帧可独立消费，不靠相邻 prompt 补全身份或画幅。共享 refs 可集中定义但每帧必须显式引用其精确 ID/版本，并可展开解析。 |
| `shot-register` / shot-register.json | `entries[]`: shot_id, scene_id, ordered_frame_ids, source_line/movement_refs, asset_refs（含可见、画外角色及用途）, line_bindings, timing_basis, planned_asset_kind, readiness, downstream_needs。无媒体时 media_ref=null，不编文件名假称存在。名称中的 register 只是镜头清单，不是应用注册。 |

`line_bindings[]` 至少包含 `line_ref, speaker_id, listener_ids, visible_subject_ids, reaction_of, sound_role, visibility, timing`。sound_role 可为 dialogue/narration/silence；visibility 明确 on_screen/off_screen。无台词的动作片段允许空 line_refs 并保留 movement_ref；纯环境场景不强塞 speaker。reaction_of 定位触发 line/action 和主体，不让反应者变说话者。

`timing` 包含 `basis=measured|planned|estimated|untimed`、依据 ref、所用区间及其单位/零点；没有区间用 null 和原因。实测仅来自实际媒体/时码。估算区间应覆盖目标范围且不重叠（明确声音桥例外），别以小数位制造精度。多帧的状态点可以是镜头内相对时刻，不承诺每帧独立播放，也不复制原音频。实际素材到来后由声音/剪辑责任人校准。

## 每帧必填 schema

| 字段 | 应写的可观察内容 |
| --- | --- |
| `frame_id, shot_id, scene_id, sequence, frame_role` | 稳定关联；frame_role 如 start/contact/end/reaction。区分同镜头多帧与新增切镜。 |
| `kind, layout` | kind=final_frame（候选目标用途，不代表媒体存在）；layout 含 aspect_ratio、single_frame、fill=native_full_bleed、safe_regions及裁切/补边决定。画幅来源指 brief；安全区未知可空数组+原因，不能偷设通用9:16。 |
| `source_refs, asset_refs` | 本帧对应的剧本动作/台词，精确角色/风格/地点/出现道具版本；背景和画外角色也按实际用途标明。传递属性 allowlist 与禁止转移项。 |
| `narrative_function, subjects` | 观众读到的一个信息变化；谁是主动作主体、谁是次反应，不能只有“电影感”。 |
| `camera, composition, screen_axis` | 景别、角度/高度、主体前中后景与画面位置、运动或固定机位的理由。按叙事选，不照抄参考照。远景身份依轮廓/服饰等可读特征，非强制正脸。 |
| `attention[]` | 每个可见人物的 character_id、gaze_target、motivation、head/body_orientation、reaction_stage。无可见人物则空数组+原因。直视镜头要与已定表现意图相符，不默许；旁观者不默认同向凝视。 |
| `action_state, body_topology` | 当前唯一主动作、起止/相邻状态、左右手脚/接触关系，必要时注明嘴部/手势是否可见及角色是否说话。禁止一个静帧同时处在互斥动作阶段。 |
| `props[]` | prop_id/ref、owner、hand、position/vector、contact、condition、action_stage；手交接过程中各帧单独说明接触者，不让道具凭空换手/复制。没有道具写空数组+理由。 |
| `background` | 地点具体层次、已知时间/天气、允许的环境/人物、来源风格下的材质/光/色；背景人数未知不能随意填人。 |
| `continuity_in/out` | 对齐上一/下一状态的站位、朝向、手持物、服装/湿伤变化、动作阶段；边界未给时明确未知，不编上集剧情。静帧的in/out是状态衔接，不要求图里同时显示两态。 |
| `audio_binding, negative` | 引用 line_bindings；可检查禁止项，例如错误出镜者、听者张口、轴线翻转、额外道具/文字/水印。禁止项针对本帧，不添加文化、体貌或供应商通用刻板规则。 |
| `prompt_sections` | 按下述顺序写离线文本；无上传/工具请求；不得偷偷放宽上述结构限制。 |

## Prompt 编排与复核

1. 引用绑定：按用途列 character/style/location/prop refs 及允许转移的身份、材质或空间属性；不把参考图的姿态/构图当角色不变量。
2. 画面：用途和原生 layout → 叙事功能 → 主体/机位/轴线 → 当前动作/注意力/道具接触 → 背景/动机光和色彩。
3. 连续性：本帧与前后帧的实际变化，哪些保持不变。视频意图可写起止姿态和局部运动，但每张状态帧只画当前一态。
4. 禁止项：把最易漂移的内容写成可核对限制；生成结果尚未出现时只能检查 prompt/引用是否一致，不能判断最终观感。

当 schema 已完整清楚时，prompt_sections 可复用有名字段引用而不重复大段文字，但须能单独展开成无缺项的 prompt。以“同上”省略人物、布局或道具状态不算可交接。

## Handoff

`handoff.json` 附公共字段、status=pass/revise/blocked、各产物路径/revision/摘要、实际输入 refs、覆盖范围、needs_input/open_questions、未执行项及下一责任人。列 scene/shot/frame→line/movement→asset 的可追溯关系；改版时给最小变更集合、保留项及需重核的下游 refs。

缺上游权威或画幅只可交接明确标 provisional 的已知计划；不输出声称直接生成的完整包。齐备时交 prompt/design candidate；生成、音频校时、独立视觉/连续性验收和注册均由下一责任人决定。不可把作者自查或文本结构通过写成最终批准。
