**TC-D03-001 — actual_output**

以下是离线 fixture 文本候选，全部在答复内交付，无文件或媒体生成。

共同定义：四类产物的 `artifact_revision=1`、`scope=SC01/MV01/LINE01`、`readiness=provisional`（时间为估算、调度为候选）、`execution_status=not_run`。输入仅来自本请求；没有目标仓库，不编造运行 envelope、文件路径或内容 commit。新增 SH01、SH02、F01–F04、PB01 均为 proposed ID，不代表登记。

输入引用 R：每项均含 `authority=user_selected、selected_by=本请求用户、fixture=true`。

| 引用 | source / entity_id / revision / representation |
|---|---|
| B | 本请求/brief / brief / 1 / brief |
| S | 本请求/script / SC01、MV01、LINE01 / 3 / script |
| C1、C2 | 本请求/selected-assets / CHAR01、CHAR02 / 2、1 / text_design |
| Y、L、P | 本请求/selected-assets / STYLE01、LOC01、PROP01 / 4、2、1 / text_design |
| I、A | 本请求/state-in、audio-plan / state-in、audio-plan / 1、1 / text_plan |

资产选择清单自身 revision=2，不覆盖各资产实际版本。没有图片或音频引用。

共享时间 T：`basis=estimated`；依据 B@1、A@1；单位秒、零点为片段开始。总区间 [0,8]；SH01 [0,5)，SH02 [5,8]。F01/F02/F03/F04 的状态点分别为 1/3/4/6 秒，不是四段独立播放时长。实际音频到来后由声音/剪辑校准。

共享台词绑定 LB01：`line_ref=LINE01@3，speaker_id=CHAR02，listener_ids=[CHAR01]，visible_subject_ids=[CHAR01]，sound_role=dialogue，visibility=off_screen`；估算播放 [0,2]，依据 A@1。`reaction_of={subject:CHAR01,trigger:LINE01@3,阶段:松手后}`。全片只播放一次；反应镜头引用触发来源，不重播。

**scene-breakdown.json**

`artifact_kind=scene-breakdown；input_refs=R；consumers=摄影/调度、连续性复核；open_questions=外部天气未知但不影响本段；handoff=H`。

`scenes=[SC01]`：

- order=1；script_refs=S；line_ids=[LINE01]；movement_ids=[MV01]，各归属此场一次。
- objective=将盒子放到桌中央；obstacle=未提供，不补造；turn=盒子由右手支撑变为桌面支撑，随后 CHAR01 转移视线。
- location_ref=LOC01@2；style_ref=STYLE01@4；time=室内傍晚；weather=unknown。人物 CHAR01 可见，CHAR02 仅画外。
- state_in=I@1；state_out=盒子闭合干燥、留在桌中央；CHAR01 双手空，身体仍朝左，视线指向画外 CHAR02。
- axis/zones=保持桌前同一侧观察；窗在画左、桌居中、CHAR01 在右、CHAR02 在左侧画外。注意力先落右手与盒子，再落 CHAR01 的眼神。
- prop_states=右手悬持→盒底接桌且右手仍持→右手脱离→盒子静置。
- transition_to_next=本段结束，不推断下一场；audio_notes=LB01 后静默；timing_basis=T。

**storyboard.json**

`artifact_kind=storyboard；input_refs=R；consumers=摄影/调度、连续性复核；open_questions=机位及分配时长待实际执行复核；handoff=H`。

| shot | 来源、功能与人物 | 画面、动作与承接 |
|---|---|---|
| SH01 / SC01 / order 1 | MV01@3、LINE01@3；功能：读清放置过程；visible_subjects=[CHAR01]；speaker=CHAR02（画外），listener=CHAR01；line_bindings=[LB01] | 桌前中景，略俯使盒底与桌面关系可读，不越轴。action_in=右手持盒悬停，action_out=盒子静置、右手收回。frame_ids=[F01,F02,F03]。机位固定的原因是方便比较接触状态。切点：完成松手后，把注意力交给眼神；match_point=盒子位置、身体朝向。timing=T/SH01。 |
| SH02 / SC01 / order 2 | LINE01@3（仅反应来源）、MV01@3（松手后的状态）；功能：读清视线移向画外同事；visible_subjects=[CHAR01]；当前 speaker=null，源台词 speaker=CHAR02；listener=CHAR01；reaction_of=LINE01 与 MV01 松手完成；line_bindings=[] | 同轴稍近中景，面部与桌中央盒子可见；action_in=看盒子，action_out=看画外 CHAR02。frame_ids=[F04]。不为身份展示强转正脸；固定机位让视线变化可读。结束保持结果，不增剧情。timing=T/SH02。 |

`planning_board={kind:planning_board,page_id:PB01,panels:[1→F01“悬停”,2→F02“接桌仍持”,3→F03“松手收回”,4→F04“静默转视线”]}`。这只是单页多格设计，不是成片素材，也没有生成页面。

**frame-prompts.json**

`artifact_kind=frame-prompts；input_refs=R；consumers=获授权生成适配器、连续性复核；open_questions=实际输出规格及适配器是否需要图片参考尚未验证；handoff=H`。

以下采用可展开结构：`完整帧=公共字段 C + 对应帧记录`；每帧的 `prompt_sections` 按模板 Q 引用自己的展开字段，没有依赖前一帧 prompt 的“同上”。

C：

- `scene_id=SC01；kind=final_frame`，仅表示候选目标用途。
- layout={aspect_ratio:16:9,source:B@1,single_frame:true,fill:native_full_bleed,safe_regions:[]（brief 未指定）,crop:none,padding:none}。每帧独立原生画面，不能从 PB01 裁取或加黑边补齐。
- asset_refs 的用途：CHAR01 为唯一可见人物；CHAR02 为画外声音/注意力目标；STYLE01 管风格；LOC01 管空间；PROP01 为可见盒子。
- 参考转移 allowlist：C1 的短黑发、灰工作衫、成年修理师、无帽；C2 只转移说话者身份；Y 的自然写实、低饱和暖灰和窗光唯一主光；L 的小修理间与既定空间关系；P 的无标记小金属盒。不转移未经给定的姿势、视线、构图或路人；文本资产不冒充看过图片。
- composition/screen_axis：CHAR01 在右，桌中央和盒子在中下部，窗在左；CHAR02 保持左侧画外，不翻轴。background=室内傍晚小修理间，只有既定人物和物件；不补造工具、陈设或背景人；天气未知、不展示天气事件。
- body_topology 公共约束：CHAR01 身体朝左；左手空闲自然垂放，不接触盒子；双脚不展示，不新增迈步；嘴部不说话。服装与身份保持，未提供湿伤变化，不添加。
- props 公共约束：唯一 PROP01@1，闭合干燥；owner=unknown（未提供产权），当前持有/支撑关系逐帧给出。
- negative 公共项：无 CHAR02 出镜、无 CHAR01 对白口型、无新增人物/道具/文字/水印、无轴线反转、无复制盒子、无同时出现互斥动作阶段。
- Q：①引用绑定=`asset_refs+用途+allowlist/禁止转移`；②画面=`kind/layout+narrative_function+subjects+camera/composition/screen_axis+action_state/body_topology+attention+props+background`；③连续性=`continuity_in/out`；④禁止项=`negative`。四帧均取此有序 `prompt_sections=Q(本帧展开记录)`。

F01：

- `shot_id=SH01，sequence=1，frame_role=start`；source_refs=[SC01@3,MV01@3,LINE01@3]；asset_refs=[CHAR01@2,CHAR02@1,STYLE01@4,LOC01@2,PROP01@1]。
- narrative_function=盒子尚未由桌面支撑；subjects=主动作 CHAR01，无次反应。camera=SH01 中景/略俯/固定。
- action_state=右手持盒悬在桌中央上方；右手接触盒侧，盒底与桌面有清楚间隙；props={holder:CHAR01,hand:右,position:桌中央上方,vector:朝桌面,contact:右手而非桌面,stage:悬停}。
- attention=[CHAR01：看盒子以对准位置，头略低、身体朝左，reaction_stage=尚未转视线]。
- continuity_in=I@1；out=下一状态保持位置与握持，仅盒底下降接桌。audio_binding=LB01，状态点 T/1 秒；附加禁止=盒底提前接桌。

F02：

- `shot_id=SH01，sequence=2，frame_role=contact`；source_refs=[SC01@3,MV01@3]；asset_refs=[CHAR01@2,CHAR02@1,STYLE01@4,LOC01@2,PROP01@1]。
- narrative_function=盒底已经接桌、手尚未松；subjects=主动作 CHAR01，无次反应。camera=SH01 中景/略俯/固定。
- action_state=盒底平接桌中央，右手仍持盒侧；props={holder:CHAR01,hand:右,position:桌中央,vector:下降结束,contact:右手+桌面,stage:接触未释放}。
- attention=[CHAR01：看盒底落点确认接触，头略低、身体朝左，reaction_stage=未回应]。
- continuity_in=悬停后下降；out=盒子位置不变，下一状态右手脱离。audio_binding={line_bindings:[],sound_role:silence}，T/3 秒；附加禁止=悬空、右手提前收回。

F03：

- `shot_id=SH01，sequence=3，frame_role=end`；source_refs=[SC01@3,MV01@3]；asset_refs=[CHAR01@2,CHAR02@1,STYLE01@4,LOC01@2,PROP01@1]。
- narrative_function=放置完成、右手释放；subjects=主动作 CHAR01，无次反应。camera=SH01 中景/略俯/固定。
- action_state=右手已离盒并向身体方向收回，画面定格在脱离后的单一状态；props={holder:null,hand:none,position:桌中央,vector:静止,contact:仅桌面,stage:已释放}。
- attention=[CHAR01：仍看盒子确认放稳，头略低、身体朝左，reaction_stage=转视线之前]。
- continuity_in=接桌且仍持；out=右手收至身体旁、双手空，盒子不移动。audio_binding={line_bindings:[],sound_role:silence}，T/4 秒；附加禁止=手仍抓盒、盒子随手移动。

F04：

- `shot_id=SH02，sequence=4，frame_role=reaction`；source_refs=[SC01@3,MV01@3,LINE01@3]；asset_refs=[CHAR01@2,CHAR02@1,STYLE01@4,LOC01@2,PROP01@1]。
- narrative_function=视线已从盒子移向画外同事；subjects=主动作 CHAR01 的视线变化，无次反应。camera=同轴稍近中景/眼高/固定，盒子仍在下方可读位置。
- action_state=右手已收回、双手空，头轻转左侧、视线落在画外 CHAR02；props={holder:null,hand:none,position:桌中央,vector:静止,contact:仅桌面,stage:放置后}。
- attention=[CHAR01：因 LINE01 在松手后看向 CHAR02，头朝左且身体不转轴，reaction_stage=静默回应]。
- continuity_in=F03 完成收手、仍看盒子；out=看画外同事，片段结束。audio_binding={line_bindings:[],sound_role:silence,reaction_of:LINE01@3,playback:false}，T/6 秒；附加禁止=直视镜头、张口说台词、再次抓盒。

**shot-register.json**

`artifact_kind=shot-register；input_refs=R；consumers=声音/剪辑、获授权适配器、主控；open_questions=实际媒体未提供；handoff=H`。

- SH01/SC01：ordered_frame_ids=[F01,F02,F03]；source_line/movement_refs=[LINE01@3,MV01@3]；asset_refs=[CHAR01@2 可见,CHAR02@1 画外说话,STYLE01@4 风格,LOC01@2 空间,PROP01@1 动作道具]；line_bindings=[LB01]；timing_basis=T/SH01。
- SH02/SC01：ordered_frame_ids=[F04]；source_line/movement_refs=[LINE01@3 反应来源,MV01@3 完成状态]；asset_refs=[CHAR01@2 可见,CHAR02@1 画外视线目标,STYLE01@4 风格,LOC01@2 空间,PROP01@1 静置道具]；line_bindings=[]；timing_basis=T/SH02。

两项均 `planned_asset_kind=单独成片帧候选；readiness=provisional；media_ref=null`。downstream_needs=声音/剪辑按真实音频校时；适配器确认输入要求，若必须图片参考则先补选图片，不能把这些文本当图片。

H / **handoff.json**：`status=pass` 仅指本段文本计划完成；四类同名答复结构 revision=1，来源 R，SC01→SH01/F01–03→MV01、LINE01 与 SH02/F04→MV01 结果、LINE01 反应可追溯。当前文本范围 needs_input=[]；开放问题如各产物所列。全部仍是 candidate；摄影/调度及连续性责任人复核后，获授权执行者另行决定生成。媒体生成、音频实测、视觉验收、应用加载与注册均 `not_run`。

**TC-D03-002 — actual_output**

`status=blocked；readiness=provisional`。现有信息不能交付直接生成或已批准的最终包；不能选择最大版本作权威，不能补造对白、房间和竖屏决定。

可保留的意向骨架只有“进入旧屋→听见呼喊→回头”，尚不是已定剧本或正式场景。最少 needs_input：

1. 写作责任人确认这段具体动作、喊话内容和说话者；缺现成 ID 时可再提出 proposed ID 映射。
2. 用户确认成片画幅及目标时长或节奏。
3. 资产责任人明确选定角色、风格、地点 refs 与实际版本，不以 v5 大于 v2 作为依据。
4. 本段必要 state-in；如承接上一集，提供相关结束状态。

本次仅答复，无需先补仓库；没有生成、审批或写入记录。

**TC-D03-003 — actual_output**

这一步由上游单集剧本写作责任人负责对白，由人物开发责任人确认动机；当前不触发分镜 Skill，也不调用其他 agent。

最少还需：谁送回谁的失物、人物彼此关系与各自想得到什么，以及“更可疑”具体体现在哪个可观察事实、片段应结束在哪个变化点。无需先准备镜头或媒体资产。

**独立 review envelope**

`status=pass；reviewer=/root/d03_forward_review；reviewed_revision=1`。

scope：指定 Skill、元数据、输出契约及公共契约的三例离线实际作答；冻结候选标识使用委派提供的 `bbc1fe9e12782d739f8cadcb328b4db6743cc08d`。

findings=[]；non_blocking_suggestions=[]。本轮实际执行了正常、缺输入、非触发三例；正常例交出了四类文本产物、三个同镜头动作帧和一个反应帧。未读取作者测试预期或其他报告。Git 一致性核验、文件写入、媒体调用、运行时兼容检查及独立视觉验收均 not_run。本结论仅是候选行为演练意见，最终接纳由主任务集成人决定。
