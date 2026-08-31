# 三类计划与时间映射

准备交接时读取。以下为本 Skill 的可读文件契约，不是旧 Drama JSON schema 或可执行渲染指令；消费者可用表格/JSON，但须保留相同含义。

## 共用字段

每份产物含 `artifact_kind`（下述三个名字之一）、正整数 `artifact_revision`、目标/`scope`、`input_refs`（路径/章节/实体、已知 revision 或 unknown）、`timing_basis`、`readiness`（provisional/candidate）、事实/用户决定/推断、`open_questions`、`consumers`、`handoff`。

落盘的运行绑定用[公共 envelope](../../../../docs/contracts.md)；来源身份和缺失处理用[内容契约](../../../../docs/content-production-contract.md)。新增未提交内容以 `uncommitted` 加摘要识别，不能把已有 HEAD 当它的版本。仅咨询可用原始输入定位，不补造 repo/commit。

- `timing_basis` 分开记录 speech/word/picture：actual（实际观测并有证据）、provided（调用方提供，说明是否复核）、planned（符号/估算，非精准依据）、unknown。每项指向选用音频/timeline 版本和时基。fixture 时注明 fixture，不能称实测；换 take 或文本使对应 alignment stale。
- 已有输入时间可计算新时间，但计算不证明输入准确、接缝自然或媒体存在。未知时间为 `null`，符号锚点写独立字段；不要用 0 假装缺失值。若展示估算范围，须与执行时码分开并写依据。
- `handoff` 含 `status: pass|revise|blocked`、原因、路径/证据、未解决问题、下一 owner；这里 pass 仅表示所声明设计范围资料齐全，不是作者最终批准。缺精确输入可交 provisional，精确任务同时标 blocked/needs_input。
- 不适用内容注明理由，例如无音乐无需 music 变更；不是“音乐检查通过”。仅有单域请求可交其余域的 retain/不适用说明，不强行重做三套方案。

## edit-rhythm-plan → 剪辑执行者、分镜/音频 owner、复核者

每个事件/镜头行至少记录：`sync_group_id`、beat/连续事件（有则引用）、`line_ids`、speaker 与被指称人物、`shot_id`/已选媒体引用、当前和候选区间、`hold/cut`、原因及锚点、说话者/反应可读性、声音 carry/handoff、缺覆盖项。

切点可跨多句；一行也可覆盖多个有依据的动作阶段。需要改已选镜头边界时明确作为新 timeline 候选，并检查源余量；镜头目录本身不被隐式改写。列原总时长/候选总时长及依据，不把文件时长和 timeline 长度混用。

## subtitle-spec → 字幕编排/渲染执行者、语言和视觉复核者

记录原生 canvas/裁切方式、坐标单位和安全矩形 `x,y,width,height`；约束的出处、字体/字号/行数/行距候选、对齐/断行规则、样式及高亮模式。最大文字宽度应不超过安全矩形扣除内部 padding 后的宽度；在目标字体实测长行再折行，不能仅按字符数承诺无溢出。缺字体/画幅时具体尺寸或已适配结论待定。

每个 cue 包括 `line_id`、逐字保留的显示文本、spoken-text 对应关系、`shot_ids`、源/目标 cue 区间、`word_tokens`（稳定 token 序号/文本/源起止/目标起止/依据）。标点、空白可附前后词而不单独制造发音；token 重组需还原显示文本。翻译与配音内容不同且无映射时不能复用原语言逐词时码。

高亮规则依 brief：整行静态、逐词或其他指定样式。若要求白字逐词变黄，写明 inactive/active 颜色、活动词 `[start,end)`、结束恢复 inactive、词间空白保持 inactive，避免整句提前变黄。遇跨行/说话者重叠时交回明确的层/行策略，不偷偷挪时间。没有词时码可以交 token 顺序/样式，但起止为 null；即使有行时码也不能线性分配。

执行适配器按帧率/字幕格式量化时间，报告误差与所用精度，不让量化后的高亮越出行界；实际支持何种高亮由执行器验证。无格式信息时不预设 ASS、字幕烧录或播放器能力。最终检查目标分辨率长行/边缘/关键动作遮挡与高亮起止；未渲染只记录待检。

## sync-change-plan → 时间线执行者及受影响专业 owner

最少字段：反馈定位/基线 revision、修改类型（gap_trim/global_retime/picture_adjust/subtitle_only）、`retain`（take/已有 hash/voice revision/原文件时长/source in-out/原播放率/审批来源）、`changes`（实体 before/after/原因）、`time_map`、受影响/stale refs、复核项、恢复原 timeline 的引用、下一 owner。同组关联 line/shot/word/stem/action cue；不变更的成员也写 retain 理由。

### 缩 gap

统一用已声明时间单位的全局半开区间。将不相交、已确认无有效语音的删除区间 `[a_i,b_i)` 排序。区间之外：`t_new = t_old - Σ(b_i-a_i)`，求和仅计 `b_i <= t_old` 的区间。删除区间内部标 deleted，边界 a/b 在新时间线连接；新总长为原总长减删除长度总和。

保留的 speech segment 做等量平移，source in/out 和播放率不变；所有词端点同变换。跨删除区间的镜头/ambience/music 必须分段/调整覆盖长度再拼接，记录接点 carry/handoff 与待听检查，不能把覆盖整个段的 stem 单纯整体平移。与动作同步的 SFX 跟随其事件锚点；若删除区间碰到词或必要反应，先缩小删除范围或请求该修改，不擅剪。

### 整体变速（仅明确目标时）

对已确认范围 `[a,b)` 与正倍率 `r`，区间内 `t_new=a+(t_old-a)/r`，其后统一加 `(b-a)/r-(b-a)`；同时存在删 gap 时声明映射先后，不能重复减时。目标时长推倍率必须有当前可靠时长与明确作用范围；否则保留 provisional/needs_input。

全体声音、图片、字幕和事件锚点共用映射；源文件/原时长/原 take 保留，新播放率、目标片段时长另列。是否保音高/音色是用户目标与执行策略，不能保证变速后主观声音完全不变。视频检查音画口型、动作/边界，静帧检查停留与阅读时间；音质、呼吸、接缝和可读性须实际复核。涉及重录或新生成只作交回 owner 的缺口，不由本 Skill 执行。
