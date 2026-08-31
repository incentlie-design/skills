# 单集文件交接

写三份产物或局部修订时使用。字段是本库的轻量内容交接，不是旧应用的 JSON schema、Ledger 或运行时注册协议。Markdown 表格与 JSON 均可，不能只列字段而缺真正剧本。

## 共同来源与状态

每份产物声明 `artifact_kind`（三个输出名之一）、`episode_id`、目标/范围、正整数 `artifact_revision`、`input_refs`、`open_questions`、`consumers` 和 `handoff`；也可引用同一清楚可定位的共同元数据块。

每条输入 ref 至少含 `source`（路径/章节/用户 brief 标识）、`revision`、实际用到的实体/范围及性质（原著事实/研究事实/用户决定/创作推断）。未知 revision 明写 `unknown`，推断不能变成批准事实。原始内容不明时不用“锁定”补洞。

落盘运行通过公共 envelope 绑定 `schema_version=1`、`run_id`、`change_id`、`repo`、`base_commit`、`artifact_revision`。新内容未提交时 `candidate_commit=uncommitted` 并附实际内容摘要；已提交候选用真实完整 commit。仅回复的草稿可省 repo/commit，不捏造运行。结构化 handoff 含 `status=pass/revise/blocked`、产物路径或回复内定位、未决问题、证据限制、下一责任人；作者不能把自查写成独立评审通过。

## 三份产物的最小可消费形状

### episode-script

- 集头：人物问题、开场/结尾状态、本集解决与留待后集的事件。
- 每场：稳定 `scene_id`、`location_id`、时间/现实或梦境、在场人物、相关 `beat_id`、可表演行动与结果、进出转场。地点或道具未定义时可提出局部 ID，明确 `proposed`，不创建系列权威。
- 按演出顺序写全文。每句口播标 `line_id`、speaker 和 mode（dialogue/narration/internal）；动作、表情、音效提示、停顿另列。无台词的行动也要写清楚，不因 line-register 没有行而遗漏。
- 尾部：保留事件、新伏笔和状态变化；不另起无任务的新集。

### beat-sheet

每个 beat 含 `beat_id`、所属 `scene_id`、主要人物、目标、阻碍、行动策略、`from_state → to_state`、导致变化的选择/结果、到下一 beat 的因果与可感桥、planned duration/range。无下一 beat 时写结束，不编桥。

另列开场钩子、关键选择/代价、高潮、新状态和闭场钩子对应的 beat；是功能索引，不强制一功能一 beat。梦中场景不能用来填“现实已发生”的事实。保护事件逐项写未消费或发现越界；未知事件由上游补充，不能自定为无。

时长汇总注明目标、估算区间、估算依据、动作/台词重叠方式和最大不确定项。角色驻留用具体动作/选择/反应检查，不凭空报实测出镜比例；分镜未做时镜头数、平均镜长和切换率不适用。

### line-register

每条口播至少：

| 字段 | 内容 |
| --- | --- |
| `line_id`, `scene_id`, `beat_id` | 稳定引用；script 与 register 一一对应 |
| `character_id`, `speaker` | 已知人物 ID 与可读名；无形旁白也有明确身份/视角 |
| `mode`, `spoken_text` | dialogue/narration/internal；仅实际要说的话，不把指导送入配音 |
| `story_function` | 此句怎样改变欲望、关系、冲突、选择、反应或必要信息 |
| `direction` | 对谁、想达到什么、具体情绪/动作变化；不规定供应商参数 |
| `handoff_cue` | 接下一句或收束的动作/声音/反应；可写自然换气，不能默认零停顿 |
| `knowledge_basis` | 旁白的亲历/梦/回忆/后来获知来源及对应 ref/beat；其他行可注明不适用原因 |

`spoken_text` 在剧本和 register 中逐字一致；不对两份分别润色。已定资产可加实际 `voice_ref/asset_ref` 及版本，没有则明确未选择；不能拿角色名猜 voice ID。没有音频时不提供伪实测 start/end 或词级时间戳；确需排演时标 planned 的时间窗，留给声音/剪辑实测校正。

## 修订与下游影响

沿用不变对象的 ID，不按新位置重编号；新对象用新 proposed ID，删掉的 line 列 retired；同一句改变内容保留 ID 并增加产物 revision，使下游按 `(line_id, revision)` 区分。指出来源 revision、改动/保留清单与旧证据是否 stale，不覆盖已批准稿。

下游影响只提出 `retain / revalidate / regenerate / invalidate` 建议，并给具体对象和理由；例如改台词使声音与字幕待复核，改动作可能影响分镜，改揭示顺序影响连续性。没有下游产物就写待首次制作，不谎称已失效的成品存在。实际注册、提升或再生成归获授权执行者。
