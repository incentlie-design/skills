独立执行者：`d04_blind_review`，与材料作者 `fixture-author` 不同。本次为 fixture 行为演练，仅检查指定文件和三个 prompt 内嵌材料；未读取预期答案、未写文件、未联网、未生成或检查媒体，也未改变任何批准状态。

**D04-001**

共享绑定与范围：

```yaml
schema_version: 1
run_id: D04-fixture-001
change_id: E02-draft
repo: fixture:canal-drama
base_commit: uncommitted
content_summary: prompt内嵌的E01收尾、正典、选定设计及E02文稿与计划摘要
artifact_revision: 3
reviewer: d04_blind_review
reviewed_revision: 3
scope: E01至E02的知识、身份、道具连续性，以及E02分镜、声音和相关剪辑映射文稿
```

实际输入 refs 均为 prompt 内嵌的虚构定位符，未访问对应业务文件：

- `brief.md@revision1`
- `canon.md@revision2#knowledge,#identity`
- `e01/handoff.md@revision1#end`
- `design/selected.md@revision2`，其中载明 `design/an.md@revision1,2`、`design/min.md@revision1`、`voices/an.md@revision2`、`voices/min.md@revision1` 的选定关系或设计摘要；未独立读取这些设计原文件。
- `e02/script.md@revision3`、`e02/shots.md@revision3`、`e02/audio.md@revision3`、`e02/edit.md@revision3`
- `reviews/script-r2.json@revision1` 的旧结论和所附脚本差异摘要。

来源区分：密码知情时点是材料明确给出的原著事实及改编决定；身份、选定设计和允许省略对白停顿属于项目约定。以下问题来自文稿之间的比对，不是对实际画面或声音的观察。

`artifact_kind: continuity-review`

`status: revise`。当前文稿包有四项需要修正的问题。

| id / severity | evidence | impact | minimal_fix | owner | acceptance |
|---|---|---|---|---|---|
| REV-001 / major | `canon.md@r2#knowledge` 指定 C-AN 首次获知密码在 E02-L003；`script.md@r3#E02-L002` 却先让他精确说出“北灯”。 | 人物在获得信息前使用该信息，破坏既定揭示顺序。 | 删除 L002 新增的密码句，保留“收好了。”；维持 L003 首次告知。 | script-owner | 新稿及最小 diff 显示 L003 前 C-AN 不再精确使用密码，首次获得信息仍可定位至 L003。 |
| REV-002 / major | `selected.md@r2` 选定 C-AN 的 `design/an.md@r2`，明确 r1 是无疤且不可生产使用的旧候选；`shots.md@r3#E02-SH002` 引用了 r1。 | SH002 的生产引用违背已选身份及永久下颌疤要求。 | 仅将 SH002 的 C-AN 视觉 ref 改为已选 r2，保留下颌疤要求。 | shot-owner；visual-owner 提供选定来源核对 | 新 SH002 明确绑定 `design/an.md@r2`；检查引用和设计要求一致。实际脸像仍须有图像后另检。 |
| REV-003 / major | `script.md@r3#L001`、`shots.md@r3#SH001` 将钥匙交给 C-AN 右手；紧接的 SH002 改成左手，SH003 又是右手，均无换手解释。brief 只允许不展示对白停顿。 | 相邻镜头计划出现无解释的两次持物手变化。 | 将 SH002 的持钥匙手改为右手，与 SH001、SH003 接续。 | shot-owner | 新 SH001→SH002→SH003 状态链均为 C-AN 右手持钥匙，且不新增矛盾。 |
| REV-004 / major | `script.md@r3#L002` 的 speaker 是 C-AN；`audio.md@r3#L002` 却填写 C-MIN 和 `voices/min.md@r1`。选定的 C-AN 声音是 `voices/an.md@r2`。 | 台词被分配给错误角色及声音身份。 | 将音频计划 L002 改为 C-AN、`voices/an.md@r2`，并同步采用修订后的 L002 文本。 | audio-owner | L002 的脚本 speaker、声音身份、字幕文本及 SH002 映射一致；不要求修改其他角色声音。 |

`non_blocking_suggestions: []`。

实际检查：知识获得顺序、钥匙交接及相邻镜头持物手、选定身份与声音引用、三条台词的 speaker 和 shot 覆盖、旧 pass 对当前版本的适用性。对白不必逐句露脸；SH004 无台词不构成缺失覆盖。

未检查：真实脸像、动作接点、口音、音色自然度、试听、响度、口型及精确字幕同步，均为 `not_run`，因为没有媒体或实测数据。环境声、音效、音乐为 `not_applicable`，因为本轮明确未要求评审。

开放问题：未提供包外依赖清单，不能判断包外消费者是否受影响；这不妨碍确认上述四项局部问题。下游消费者为脚本、分镜、视觉、声音原 owner。handoff 位于本回复 D04-001 的发现表；证据见各行，未解决项为 REV-001～004，下一责任人为对应 owner，由 production-owner 协调。

`artifact_kind: impact-set`

目标、范围及实际 refs 继承上述共享声明。以下均为修改或复核建议，未执行任何状态写入。

**已发生变化造成的失效或引用问题：**

- `reviews/script-r2.json@r1` 的 pass 只覆盖 `script@r2`。L002 已发生内容变化，因此该 pass 对当前 `script@r3` 的放行用途已 stale；保留旧报告对 r2 的原记录。关联 REV-001，production-owner 负责安排新版本评审。
- SH002 当前引用的 `design/an.md@r1` 已被选定 r2 替代，不能继续用于该镜头生产。关联 REV-002；保留旧候选记录，不覆盖或删除它。
- 当前下游均声明绑定 `script@r3`，不存在已知的“仍挂 script r2”问题。不能把建议修改之后才会产生的重绑定需求说成已经发生。

**采纳修复后才需处理的影响：**

| finding_id | changed_ref | affected_refs / action / reason | owner / recheck |
|---|---|---|---|
| REV-001 | `script@r3#L002` 的新候选 | 更新音频 L002、沿用脚本的字幕文本及编辑长度计划；复核 SH002 的对应台词。原因是删除了密码句。 | script-owner 修改；audio-owner、shot-owner 更新直接依赖；剪辑/字幕 owner 待 production-owner 指定。按 L002→声音→字幕→SH002 链复核。 |
| REV-002 | `shots@r3#SH002` 的角色视觉 ref | 将旧候选引用重绑定至已选 r2；若存在引用该镜头计划的下游产物，再对对应项定向复核。 | shot-owner；visual-owner 核对来源。不得推定已生成图片或要求全剧重做。 |
| REV-003 | `shots@r3#SH002` 的持物手描述 | 复核 SH001→SH002→SH003 的直接动作接点及相关编辑计划。 | shot-owner；剪辑 owner 待指定。确认右手状态连续。 |
| REV-004 | `audio@r3#L002` 的 speaker、voice ref | 修正该行声音身份；核对其 SH002 及字幕映射。若已有声音或剪辑产物，只复核实际引用该行的部分。 | audio-owner；相关剪辑 owner 待指定。确认 C-AN→`voices/an.md@r2`。 |

可保留项及依据：

- L001、L003 的台词、speaker 和 C-MIN 声音引用不受已知脚本 diff 影响。
- SH001、SH003 的已选视觉引用及右手状态可复用，但须参与 SH002 接点复核。
- SH004 无人物、钥匙和台词，位置与光线接续 SC02；其空镜内容可保留。
- 以上是内容可复用判断。若脚本产生新包 revision，所有声明依赖旧脚本包的计划仍须由 owner 重绑定新来源，并记录哪些内容未变。

未知依赖：没有媒体文件、take、包外消费者或生成记录，不能列出确定的重生成任务。production-owner 只需在涉及包外处理时补充相关依赖清单。

下游消费者为 production-owner 及上述原 owner。handoff 位于本回复此影响表；下一步提交新 revision、最小 diff 和“finding→修改→证据”映射，再进行一次有证据的定向复审。开放问题为未提供的包外依赖与剪辑/字幕 owner，不改变 Registry 或旧审批记录。

`artifact_kind: stage-readiness`

目标、范围及实际 refs 继承共享声明。

| 请求阶段/维度 | status | 检查状态 | 证据与未满足条件 |
|---|---|---|---|
| E01→E02 文稿连续性 | revise | executed | REV-001 的提前知情及 REV-003 的钥匙状态需要修正。 |
| 分镜计划 | revise | executed | REV-002 的旧身份引用和 REV-003 的接点问题未解决。 |
| 声音计划 | revise | executed | REV-004 的 speaker/voice 串人未解决；须同步修订 L002。 |
| 局部 line→shot 覆盖 | pass | executed | L001～L003 各有对应 SH001～SH003，SH004 无台词；此结论仅覆盖映射存在性，不放行相关内容。 |

当前只能支持交原 owner **定向修订**，不能将该文稿包作为已通过的生产输入。修复并完成独立定向复审后，可支持所列范围的分镜、声音及剪辑规划。

媒体检查为 `not_run`；环境声、音效、音乐为 `not_applicable`。媒体不存在不另行阻断本次文稿判断，但文稿评审不能证明图像身份稳定、声音已试听、实际 timing、口型、混音、字幕精准、注册完成或发布就绪。成片 QC 和发布不在本次可放行范围。

开放问题及未解决项为 REV-001～004、包外依赖未知。下游消费者是 production-owner 和后续独立复核者；handoff 为本回复三项产物，下一责任人是各修复 owner，随后交独立 reviewer。

**D04-002**

`status: blocked`，原因是 `needs_input`。不能沿用旧 pass 写成可发布，也不能把当前实际评审者伪记为原作者。实际执行者仍是 `d04_blind_review`；作者自查不能替代独立终审。

以下仅为沟通层结果，不伪造完整运行 envelope，也不从“final-r5”推定数值 revision：

- `artifact_kind: continuity-review`：目标为 E07 新版发布前评审。实际 ref 只有本 prompt 的口述；新版稿件、真实 `reviewed_revision`、选定声音 ref 和旧报告本体均未提供。仅执行了输入完备性与独立性检查，内容检查为 `not_run`；无法提出有文件证据的正文 findings，也不能据此认为没有缺陷。开放问题是新版究竟改了什么、依据何种旁白权限和声音选择。
- `artifact_kind: impact-set`：依据“旁白可知范围和主角声音身份已改变”的口述，旧 r4 pass 不能覆盖这些变更后的对象；保留旧版记录，不宣称旧版内容错误。待取得 diff 后，最小追踪范围是改变的旁白行、主角受影响声音行及实际关联的字幕、shot 和剪辑。未见依赖证据，不能宣布全剧 stale，也不能保证其余部分可复用。
- `artifact_kind: stage-readiness`：请求阶段为发布，`status: blocked`。稿件连续性、选定声音核对及媒体终检均为 `not_run`。当前仅支持补齐材料和安排独立评审，不支持发布。

最小补充项：新版 E07 稿件及真实正整数 revision、相关正典/旁白权限、相对旧版的最小 diff、实际选定声音 ref、旧报告及相关依赖映射；同时明确 repo、运行绑定、内容摘要、read_set 和独立 reviewer。若仍要求发布就绪结论，还需提供对应版本的实际成片与必要媒体映射。

三个沟通产物的消费者均为制作协调者及脚本/声音原 owner；具体 owner 未提供，待协调者指定。handoff 位于本回复 D04-002，证据限于口述，下一责任人为材料提供者及制作协调者。没有更改任何批准状态。

**D04-003**

该请求不触发 `drama-continuity-review`：它要求创作、修改正典、注册资产、付费生产和自动批准，没有连续性或阶段评审任务。因此不生成评审报告，也不虚构输入、revision 或批准证据。

剧情与正典变更应交编剧和正典负责人；Registry 与付费生成交相应获授权执行者，批准交承担该范围的独立复核者。本次未创作剧集、未改正典、未写 Registry、未调用 TTS/视频生成，也未将任何内容设为 approved。三个样例处理结束。
