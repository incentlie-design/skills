# C08 来源抽取记录

任务：DRAMA-SKILL-C08。只读来源；方法归纳不构成对源应用的兼容承诺，也不授予源脚本的运行权限。未读取小说、私人媒体或凭据，未运行旧 validator/compiler。

## 治理与基线

- 当前源仓库：skill-creator。原 main 基线 `cd990aaec765fcbd1731af970233484377c873aa`；本任务干净 worktree 已 fast-forward 到 foundation `8271786fd12cc4a35339d56fb26d8635af50fa0c`。
- 已完整读取当前 `skills/meta/meta-skill-governance/SKILL.md`、`docs/skill-standard.md`、`docs/contracts.md`、`docs/content-production-contract.md`、`skills/engineering/eng-workspace-governance/SKILL.md` 及 `references/workspaces.md`，以及 brief、tasks 中 C08 条目、迁移表。
- 参照 product-review-prd 的 I/O、独立性、停止与 review envelope；参照 eng-quality-test 的 metadata 形式。使用 skill-creator 创建规范与 quick_validate。Git 协作 Skill 的全量集成默认值由本仓库明确的风险分层规则覆盖。
- registry 中未有此能力，已有广告学习入口不接管音频生产。声音身份归并行的 content-voice-design 责任人，文件交接不形成强制运行依赖。

## 专业来源

drama-agents 根路径 `/Users/jiajun.lai/Documents/workspaces/drama-agents`，本次实际读取 HEAD 为 `052fc44dcaafb9c2c10d6365f391dc422918a146`，读取时该工作区干净。下表路径相对此源根目录；这些路径只用于追溯，交付 Skill 运行时不依赖它们。

| 已读文件 | 采用的方法 | 不迁入内容 |
| --- | --- | --- |
| `.agents/skills/episode-audio-performance/SKILL.md`（源 metadata 0.4.0） | 计划与已生成证据分开、speaker/voice绑定、连续表演 | Compiler/Registry/可信receipt/旧AudioContract执行入口 |
| `.agents/skills/episode-audio-performance/references/audio-production-plan.md` | 计划cue及估时不能充当take/测量；offline意图 | 固定三种上游Artifact门禁与应用closed schema |
| `.agents/skills/episode-audio-performance/references/audio-contract.md` | 原词与指导分离、逐句追溯、时间线关联 | 固定-16 LUFS、四个stem强制非空、运行时权威验证 |
| `.agents/skills/episode-audio-performance/references/production-plan.md` | 相邻句电平、房间底声、人声避让、因果拟音、保留原take的局部修复 | 固定间隙/交叉淡化阈值、七类枚举闭集、全字段强制填写 |
| `.agents/skills/series-audio-bible/SKILL.md` 与 `references/contract.md`（源 metadata 0.2.0） | 身份与表演所有权分离、旁白知识边界、声响动机文化来源 | portrayal anchor/voice catalog投影与注册协议；重新设计音色身份 |
| `knowledge/audio/sound-and-timeline.md` | 声音先行刻画人物、语义连续、短语内突降分链诊断、随beat变化的环境、停顿修改联动 | 250–700ms等案例值、EP2实例、特定乐器/歌曲/前现代默认 |
| `knowledge/audio/voice-and-accent.md` | 身份连续不只看voice ID；表演指令不能进入声音；邻句连续性 | 菲律宾口音配方、人物年龄/具体角色、固定preview长度 |
| `knowledge/workflow/provider-and-cost-lessons.md` | 能力与授权不由模型名或已有密钥推定；局部修复避免扩大成本 | provider任务/预算token/CAS/并行runner运行机制 |

个人只读来源：`/Users/jiajun.lai/.codex/skills/elevenlabs-voice-design/SKILL.md`，revision=unknown（本次未查询其Git历史/文件摘要）。仅核对 Design/Remix/TTS 的职责分离与选声后再生产边界；不复制 API 参数、脚本、voice ID、密钥或强制调用依赖。未核对当前供应商文档，交付没有新增供应商适配承诺。

`narrated-drama-*` 仅做路径发现，未读取内容：C08 指定方法已由 episode-audio-performance 与 series-audio-bible 覆盖，无需额外迁入 workspace/runtime 管理。

## 本次归纳与限制

旁白/对白保留独立逻辑层，可按目标混到voice bus；不用的声音层允许有理由地省略。缺文化证据时hold特定文化cue或明确给无文化归属的创作纹理。没有媒体时可完成设计交接，实际响度、自然度、短语突降和同步仍是未测项。这些是本次跨媒介归纳，不冒充原著事实或已生产结论。

不更新 registry、AGENTS、README、CHANGELOG、docs、scripts 或发现入口；注册及批次兼容验证由主任务统一完成。旧源保持原名、原路径与已安装状态，本候选不是旧schema的drop-in替代品。
