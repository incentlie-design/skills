**TC-001：实际答复**

以下是《晨钟》的全剧方案候选，不是单集成稿或批准版本。

共同元数据 M1：四份产物均为 `artifact_revision=1`，覆盖全文 S1–S6；`open_questions=[]`；共同交接见 H1。输入引用：

- R1：`fixture://morning-bell`，revision=1，定位 S1–S6。
- R2：`fixture://culture-brief`，revision=2，定位 U-1。
- R3：本次用户请求，revision=unknown，定位“4集／每集90–120秒／成人普通观众／中文／国王第一人称偏好”。

**1．series-brief**

`artifact_kind=series-brief`；继承 M1；消费者：单集作者、生产计划。

- **前提与核心问题**：一个渴望父亲认可的儿子，为赶回家而违反钟亭规则；弟弟的停留与帮助救回了他。他最后能否放下独占功劳的念头，让一家人正视长期偏爱的伤害？
- **形式**：4集中文短剧，成人普通观众，每集目标90–120秒。按“付出—冒险—寻找—救援与坦白”四次状态变化拆集；具体秒数尚未经过台词或录音验证。
- **调性**：克制的家庭寓言。保留岚对父亲的爱和真实付出，不把他简化成争功反派；保留汐帮助他人的实际行动。
- **保留边界**：保留断粮、明知规则仍提前敲钟、石像能听不能动、汐修船获水与规则、日出救援、日光下治愈、岚坦白和父亲认错。
- **文化约束 U1｜user_decision｜R2#U-1**：架空王国，不对应现实民族；钟是信号器具，不设计现实宗教法器。直接继承，不新增研究。
- **AP1｜adaptation_proposal｜R1#S1–S6、R3**：顺时序呈现四集，压缩重复赶路和返程。目的为给关键选择与反应留空间，不删因果节点；候选待下游确认。
- **AP2｜adaptation_proposal｜R1#S6、R3**：国王的第一人称旁白统一来自“两个儿子报告旅途之后”。旅途细节以事后听闻为依据；岚未明说的内心由行动与反应表现，不让国王直接断言。旁白随当集揭示推进，不提前透露救援、坦白与认错。
- **可观察验收**：六段来源都有去向；救援前已出现规则和水；国王旅途当时仍不知情；终集同时完成身体救援与家庭关系变化。

**2．story-bible**

`artifact_kind=story-bible`；继承 M1；消费者：人物发展、单集作者、连续性评审。

以下 F1–F6 均为 `source_fact`，分别引用 R1 的同号段落：

| ID／来源 | 必须保持的事实 |
|---|---|
| F1／S1 | 国王失聪；医者提出晨钟与日出后鸣钟的条件；岚既爱父亲又想得到认可；国王答应等三日。 |
| F2／S2 | 岚用绳索和口粮换来渡夫帮助，修出可过人的桥；过河后断粮；国王不知道旅途经过。 |
| F3／S3 | 日出前鸣钟会化石；只有日出时浇温泉水才能解除。岚看到规则，仍怕晚归而提前敲钟，化为能听不能动的石像。 |
| F4／S4 | 三日后岚未归，汐出发；汐帮疲惫的渡夫修船，说明寻找哥哥，得到温泉水及规则，连夜登山见到石像。 |
| F5／S5 | 汐在日出时救回岚；岚意识到弟弟的停留与帮助成就了结果；两人带钟回宫，在日光下鸣钟，国王复听。 |
| F6／S6 | 岚本想只报成功，最后承认汐救了自己；兄弟报告旅途，国王此时才知道细节，并承认长期偏夸造成的伤害。 |

实体 ID 均为本候选 `proposed`，未注册：C-K国王、C-L岚、C-X汐、C-F渡夫；L-P宫中、L-B桥边、L-T钟亭；P-B晨钟、P-W温泉水、P-I石刻。

| 人物 | 欲望、策略与选择 | 代价与终局 |
|---|---|---|
| C-L 岚 | 爱父亲、求认可；以赶路和自我付出证明本领；先选择违反规则，最后选择承认弟弟的救援。依据 F1–F3、F5–F6。 | 失去口粮、身体行动自由，最后放弃独占功劳，承认帮助。 |
| C-X 汐 | 寻找哥哥；途中停下修船，获得救援条件；到日出按规则救兄。依据 F4–F5。 | 修船占用行程时间是 IN1 `inference`，依据“停下帮忙”，不添加具体耗时或险情。终局与哥哥共同归来。 |
| C-K 国王 | 开端等待寻钟结果；习惯偏夸汐；听完兄弟报告后承认自己伤害了岚。依据 F1、F6。 | 身体复听之后，还须面对自己的关系责任；不能只用治愈结束人物弧线。 |

受保护事件：F5救援须以 F3规则、F4水和日出为前置；F6坦白须保留“本想只报成功→承认救援”的选择；父亲认错发生在获知旅途之后。

知识表中，旁白时点一律为 F6之后；这不改变角色当时的知识：

| fact_ref | story_time | audience_reveal | character_acquisition | narrator_basis | holdback |
|---|---|---|---|---|---|
| F1 | 出发前 | EP01 | 国王、岚知道寻钟条件；岚自己的欲望属于岚 | 国王亲历条件与三日承诺；不替岚断言未表达的心念 | 父亲认错留EP04 |
| F2 | 岚渡河 | EP01 | 岚、渡夫亲历；国王到F6才获知 | F6旅途报告 | 后续成石不提前透露 |
| F3 | 岚抵钟亭之夜 | EP02 | 岚读石刻并亲历化石；汐于F4听渡夫说明规则；国王于F6得知 | F6旅途报告 | 展示解救条件，不展示救援结果 |
| F4 | 三日已过后 | EP03 | 汐、渡夫知道修船与给水；汐登山见石像；国王于F6得知细节 | F6旅途报告 | 实际浇水与复原留EP04 |
| F5 | 救援日出及回宫后 | EP04前段 | 兄弟亲历救援；国王亲历复听，但尚未听完旅途 | 救援来自报告；复听为亲历 | 坦白和认错留本集后段 |
| F6 | 回宫报告时 | EP04后段 | 国王在此取得旅途知识；兄弟听见父亲承认伤害 | 国王亲历 | 无 |

**3．series-outline**

`artifact_kind=series-outline`；继承 M1；消费者：单集作者、连续性评审。

故事引擎：岚越想用赶路证明自己，越难容忍等待；他最后必须承认，结果依靠了弟弟愿意停下来的选择。父亲也须从评价孩子的本领，走向承认自己的偏爱。

因果转折：

1. F1的认可需求与三日承诺推动岚出发；F2的实际付出使“求功”同时具有爱与代价。
2. F3中，岚读懂危险仍提前鸣钟，因此无法归来；不能改写为不知道规则的意外。
3. F4中，汐在哥哥失联后寻找，并因修船与说明来意获得水及规则；不能把这些条件自动归功于岚先前的交换。
4. F5解决救援与听觉问题；F6再解决谁值得承认、谁需要承担伤害的问题。

源事件去向：

| event_ref | 集／处理 | 原因与影响 |
|---|---|---|
| EV01＝R1#S1 | EP01／retain | 建立失聪、动机与期限。 |
| EV02＝R1#S2 | EP01／retain | 保留桥、交换与断粮，压缩重复行路。 |
| EV03＝R1#S3 | EP02／retain | 单独保护读规则、犹疑、违规与化石反应。 |
| EV04＝R1#S4 | EP03／retain | 保留三日后出发、修船、给水、传规则及见石像。 |
| EV05＝R1#S5 | EP04／retain | 救援、领悟、返宫、复听；仅压缩返程过程。 |
| EV06＝R1#S6 | EP04／retain | 保留岚的坦白选择与父亲承认伤害。 |

回收计划：

| setup_id | promise_or_rule／source_refs | setup_episode | payoff_episode_or_open | responsible_character | prerequisites | status |
|---|---|---|---|---|---|---|
| SU1 | 晨钟与日出后复听条件／F1、F5 | EP01 | EP04 | C-L、C-X、C-K | 取回钟、日光下鸣钟 | planned/protected |
| SU2 | 求认可与长期偏夸／F1、F6 | EP01 | EP04 | C-L、C-K | 救援发生；岚坦白；国王听完经过 | planned/protected |
| SU3 | 三日等待／F1、F4 | EP01 | EP03 | C-K、C-X | 三日已过，岚未归 | planned |
| SU4 | 提前鸣钟化石、日出温泉水解除／F3–F5 | EP02 | EP04 | C-L、C-X | 汐得到水和规则，到达石像，等到日出 | planned/protected |
| SU5 | 渡夫与互助行动／F2、F4 | EP01 | EP03 | C-F、C-X | 汐另行修船并说明找哥哥 | planned |
| SU6 | 温泉水进入汐手中／F4–F5 | EP03 | EP04 | C-X | 带水抵达钟亭，日出浇水 | planned/protected |

结局关闭寻钟、救兄、复听与家庭坦白主线；无新增悬而未决的故事线。表中均为计划，未声称任何集已经写成或拍摄。

**4．episode-map**

`artifact_kind=episode-map`；继承 M1；消费者：单集作者、生产计划。采用线性故事时序；各集 `open_questions=[]`。

- **EP01／sequence=1／R1#S1–S2／focal_character_id=C-L**
  - `entry_state`：国王失聪，岚渴望认可。`dramatic_question`：他愿为寻钟付出什么？
  - `goal→obstacle→choice→price→changed_state`：寻找晨钟→桥被洪水冲断→用绳索和口粮交换协助→断粮→渡河继续赶路。
  - `opening_hook`：失聪与三日等待的承诺。`closing_hook`：岚付出了口粮，仍把及时归来视为获得认可的机会。
  - `next_dependency`：他的赶路意愿将与钟亭要求等待的规则冲突。
  - `must_include=F1,F2`；`forbidden_early_events=F3化石、F5救援、F6坦白`；`protected_future_refs=SU2,SU3,SU4`。
  - `knowledge_and_reveal=知识表F1,F2`；国王不在旅途当时知情。
  - `setup_refs=SU1,SU2,SU3,SU5`；`payoff_refs=[]`。
  - `duration_target_or_range=90–120秒`；`density_note`：重点给请命动机与交出口粮的选择，修桥过程作简洁动作段落。

- **EP02／sequence=2／R1#S3／focal_character_id=C-L**
  - `entry_state`：岚独自赶路后夜抵钟亭。`dramatic_question`：他能否为了安全等待日出？
  - `goal→obstacle→choice→price→changed_state`：尽快取钟归家→石刻规定必须等待→怕父亲失望，提前敲钟→失去行动自由→成为能听不能动的石像。
  - `opening_hook`：钟就在面前，却不能立刻敲。`closing_hook`：岚无法归去，宫中的等待将怎样结束？
  - `next_dependency`：三日未归促成汐出发。
  - `must_include=F3全部规则及岚的知情选择`；`forbidden_early_events=F4给水、F5救援、F6认错`；`protected_future_refs=SU3,SU4,SU6`。
  - `knowledge_and_reveal=知识表F3`；观众知道存在解救条件，但不知道救援已经成功。
  - `setup_refs=SU4`；`payoff_refs=[]`。
  - `duration_target_or_range=90–120秒`；`density_note`：用等待、犹疑和化石后的听觉反应支撑时长，不新增追兵或死亡假象。

- **EP03／sequence=3／R1#S4／focal_character_id=C-X**
  - `entry_state`：三日已过，岚未回。`dramatic_question`：汐寻找哥哥时，是否愿意为别人停下来？
  - `goal→obstacle→choice→price→changed_state`：寻找岚→渡夫疲惫、船需修理→停下帮忙并说明来意→投入行程时间（IN1）→获得水与规则，登山找到石像。
  - `opening_hook`：等待结束，哥哥仍未出现。`closing_hook`：汐已带来水和办法，日出时能否救回哥哥？
  - `next_dependency`：日出到来，才能实施解救。
  - `must_include=F4`；`forbidden_early_events=F5实际复原与复听、F6坦白`；`protected_future_refs=SU1,SU2,SU4,SU6`。
  - `knowledge_and_reveal=知识表F4`；汐从渡夫取得规则，不凭空知道。
  - `setup_refs=SU6`；`payoff_refs=SU3,SU5`。
  - `duration_target_or_range=90–120秒`；`density_note`：保留停下帮忙的决定与给水传规则，连夜登山压缩为过渡。

- **EP04／sequence=4／R1#S5–S6／focal_character_id=C-X→C-L、C-K**
  - `entry_state`：汐带水守在哥哥石像前。`dramatic_question`：救回身体之后，岚和父亲能否说出各自应承认的真相？
  - `goal→obstacle→choice→price→changed_state`：救兄并完成寻钟→必须遵守日出条件，岚又想只报成功→汐依规救援，岚承认获救→岚放下独占功劳，父亲面对偏爱造成的伤害→兄弟共同归来，国王恢复听觉并认错。
  - `opening_hook`：日出，解救条件终于齐备。`closing_hook`：以坦白后的关系变化闭合，不另开险情。
  - `next_dependency=none`：原文主线均已结束。
  - `must_include=F5,F6`；`forbidden_early_events`：不得先让国王知道旅途，再让兄弟报告；不得把父亲认错移到救援之前。
  - `protected_future_refs=[]`；`knowledge_and_reveal=知识表F5,F6`。
  - `setup_refs=[]`；`payoff_refs=SU1,SU2,SU4,SU6`。
  - `duration_target_or_range=90–120秒`，初步按上限规划；`density_note`：救援与岚反应约25秒、返宫与鸣钟约20秒、坦白及父亲回应约60秒、收束约10秒，均为计划估计。实际成稿若超长，先压返程和重复说明，不删领悟、坦白或父亲回应。

**H1：共同交接**

`status=pass`，仅表示上述四份 revision=1 方案具备交接内容，不表示独立审批。下一责任人：单集作者；可按 EP01→EP04 写作，连续性评审沿用 F、SU 与知识表引用。

已自查：S1–S6去向、选择与后果、救援前置、国王得知渠道、终局回收。未检查：成稿台词长度、实际表演时长、任何视觉或音频效果。未落盘，未生成媒体，未注册资产，未改变已有文化约束。

---

**TC-002：实际答复**

`status=blocked`

目前没有《雾海王冠》的可读来源，无法交付忠实的24集全剧方案，也不能把按记忆补出的情节写成原著事实。

`needs_input`：请提供覆盖全文、结局与关键后续回收的原文，以及版本信息；版本不详可明确标为 unknown，粘贴文本可使用临时段落定位。

已保留“忠实改编、24集、仅答复交付”的目标。未补造原著情节，未联网，未落盘。

---

**TC-003：实际答复**

这句可改为：**“他决定接着往前走。”**

这是仅针对该句的文本候选；剧情、集数、角色及批准大纲保持不变，不重做全剧方案。

TTS生成与权威资产注册为 `blocked`：它们超出 drama-series-adaptation 的范围；目前也没有供应商、voice ID、已配置凭据或 Registry 写入入口。后续需将这些执行条件交给获授权的声音／资产执行者。尚未生成音频，也未注册或替换任何权威资产。

---

本次演练记录：

- 冻结候选：`78595ccf9d8a0cd785cb139287377befb2cd3c9e`。使用两条只读命令，通过 `git show` 读取该提交中的以下五个路径：
  - [SKILL.md](/Users/jiajun.lai/.codex/worktrees/4681/skill-creator/skills/drama/drama-series-adaptation/SKILL.md)
  - [skill.json](/Users/jiajun.lai/.codex/worktrees/4681/skill-creator/skills/drama/drama-series-adaptation/skill.json)
  - [output-contract.md](/Users/jiajun.lai/.codex/worktrees/4681/skill-creator/skills/drama/drama-series-adaptation/references/output-contract.md)
  - [contracts.md](/Users/jiajun.lai/.codex/worktrees/4681/skill-creator/docs/contracts.md)
  - [content-production-contract.md](/Users/jiajun.lai/.codex/worktrees/4681/skill-creator/docs/content-production-contract.md)
- 实际执行：依次独立处理三条原始 prompt；以上保留实际文本产物与阻断回复。TC-002、TC-003未继承《晨钟》故事输入。
- 未执行：未读取 cases、作者报告或其他任务；未修改或提交文件；未派生 agent；未联网、调用媒体或付费服务、安装、应用或注册资产；未进行单集写作与实际时长验证。
- Skill 本身导致的具体歧义：无。
- 本记录不评分，也不替代主任务最终验收。
