# 短剧与通用专业 Skill 整理 · 集成交付

变更：`DRAMA-SKILLS-20260831`。治理：`meta-skill-governance`，沿用现有 eng/product 的所有权、公共 envelope、版本和有界测试规则。

## 当前结论

14 个独立 Skill 候选已完成实现、原始 case 演练和源码接纳；5 个短剧专用、9 个跨媒介通用专业。候选已合入隔离集成分支，登记与发现入口已准备。**冻结后的集成检查待执行，当前不能据此宣称主分支交付完成。**

现有 10 个 Skill 入口保留，总数为 24。没有发布、全局安装、旧 runtime 替换或媒体生产。

## 分类与使用边界

- `drama-*`：全剧改编、单集写作、短剧分镜、连续性评审、串行生产计划。
- `content-*`：文化研究、人物发展、视觉世界、人物视觉、摄影、场面调度、音色设计、音频制作、剪辑节奏。可被小说、电影、游戏、广告等消费。
- `eng-*` 与 `product-*`：原有工程/产品规范继续复用，不重命名为“专业”分类。
- 应用 Registry、文件锁、CAS、Outbox、运行时调度不搬进 Skill；设计完成不冒充真实注册或生成完成。

各 Skill 独立任务仅负责自己的目录和证据。共享文档/登记由主任务维护；任务、分支及 worktree 保留供后续维护，不自动删除或归档。

## 交付与行为证据

| Skill | 分类 | 冻结候选 | 原始行为证据 |
| --- | --- | --- | --- |
| [content-cultural-research](../../skills/content/content-cultural-research/SKILL.md) | 通用专业 | `2849ab8` | [演练](content-cultural-research/rehearsal-round-1.md) |
| [content-character-development](../../skills/content/content-character-development/SKILL.md) | 通用专业 | `13e7469` | [演练](content-character-development/reviewer-output.md) |
| [content-visual-worldbuilding](../../skills/content/content-visual-worldbuilding/SKILL.md) | 通用专业 | `07c9a93` | [演练](content-visual-worldbuilding/reviewer-output.md) |
| [content-character-visual-design](../../skills/content/content-character-visual-design/SKILL.md) | 通用专业 | `4e05332` | [演练](content-character-visual-design/independent-exercise.md) |
| [content-cinematography](../../skills/content/content-cinematography/SKILL.md) | 通用专业 | `26ff584` | [演练](content-cinematography/reviewer-round-1.md) |
| [content-scene-blocking](../../skills/content/content-scene-blocking/SKILL.md) | 通用专业 | `d2a4b74` | [演练](content-scene-blocking/independent-review-r1.md) |
| [content-voice-design](../../skills/content/content-voice-design/SKILL.md) | 通用专业 | `e1474b4` | [演练](content-voice-design/independent-exercise.md) |
| [content-audio-production](../../skills/content/content-audio-production/SKILL.md) | 通用专业 | `2c920ee` | [演练](content-audio-production/reviewer-output.md) |
| [content-editing-rhythm](../../skills/content/content-editing-rhythm/SKILL.md) | 通用专业 | `376fa2b` | [演练](content-editing-rhythm/reviewer-round2.md) |
| [drama-series-adaptation](../../skills/drama/drama-series-adaptation/SKILL.md) | 短剧专用 | `a8fdbb4` | [演练](drama-series-adaptation/independent-results.md) |
| [drama-episode-writing](../../skills/drama/drama-episode-writing/SKILL.md) | 短剧专用 | `4f8afeb` | [演练](drama-episode-writing/round-1-rehearsal.md) |
| [drama-storyboard-production](../../skills/drama/drama-storyboard-production/SKILL.md) | 短剧专用 | `4576796` | [演练](drama-storyboard-production/reviewer-output.md) |
| [drama-continuity-review](../../skills/drama/drama-continuity-review/SKILL.md) | 短剧专用 | `17043bd` | [演练](drama-continuity-review/reviewer-output.md) |
| [drama-production-planning](../../skills/drama/drama-production-planning/SKILL.md) | 短剧专用 | `478a823` | [演练](drama-production-planning/reviewer-output.md) |

42 个不同原始 case、43 次实际独立执行：每个 Skill 的正常/缺失输入/越界各一例，C09 额外定向重演一例。主集成人查看了真实产物，不把结构校验的 cases_defined 当作行为执行。跨 Skill 静态评审通过，无重大/阻断问题；这不是跨 Skill 实际端到端运行证据。

- C09：首轮剪辑输入缺源区间与原速。仅补测试输入，Skill 方法不变；第二轮只重演该例，保留首轮 revise，不重跑其他 Skill。
- D02：原始输出字数/口播估时不准确。独立补正为 136 字、约 45.3 秒；103–125 秒只是整段 beat 的计划范围，剩余动作窗口未验证，不能用空白凑时长。未改 Skill 方法、未重复行为轮次。
- C05：作者 3 条结构命令 + reviewer 3 条只读命令，合计 6；按聚合预算计不符合 3 命令上限。明确记录为非阻断流程偏差，不宣称全项规范零偏差。没有因此追加行为轮次或全回归；后续统一父子预算。

完整独立接纳记录见 [source-acceptance.json](source-acceptance.json)；交叉边界见 [cross-skill-review.json](cross-skill-review.json)。历史 handoff 中的 draft、final_acceptance=not_run 是当时状态，不回写旧日志。当前 lifecycle 接纳由本报告和集成证据覆盖。

## 验收映射

| 验收 | 当前证据与结论 |
| --- | --- |
| AC-001 独立任务/隔离 | 14 个真实任务、14 个 clean linked worktree，写入范围检查无越界；见任务索引 |
| AC-002 旧入口整理 | 23 个旧生产入口、narrated-drama 三入口、个人音色及已有导演入口均有迁移/保留映射 |
| AC-003 不是空壳 | 有具体创作方法、输入输出、必要 references；14 个独立原始演练产物已读 |
| AC-004 有界真实测试 | 42 distinct / 43 executions；C09 一次定向重演、D02 记录补正；C05 聚合命令预算偏差如实保留 |
| AC-005 统一登记 | 已编辑 registry/AGENTS/README/CHANGELOG，新增相对发现入口；冻结集成检查待执行 |
| AC-006 交接与边界 | source/entity/line/scene/shot/asset refs 与 revision；静态交叉评审通过，未执行真实生产链 |

## 集成验证

待冻结源码 commit 后执行且仅执行本批次三条命令：

1. `python3 -m unittest discover -s tests -p test_validate_skills.py`：受影响分类校验器与旧类别保护，9 项。
2. `python3 scripts/validate_skills.py --check-discovery`：24 Skill 登记、格式、依赖、链接、72 个用例定义及发现 symlink。该命令行为执行数必须仍为 0。
3. `git diff --check cd990aaec765fcbd1731af970233484377c873aa HEAD`：累计补丁格式。

最多一次初验、一次有证据的定向终验；不跑生产应用全回归。确切退出码、head 和日志将在本报告与 integration-evidence.json 登记。

## 沉淀了哪些经验

人物不是工具人：用欲望、关系、选择、代价与回收组织弧线；叙述者不能知道未见未闻之事；梦境靠环境/声音动机、转场及醒后余波连接。镜头不是“换一张正脸”：明确目光目标、反应触发、轴线、道具唯一持有与接触/释放、镜头内多个帧状态。声音区分身份、表演与可说文本，局部音量/节奏变化不能无依据重造音色。选择过的身份和风格版本比“最高版本号”更重要。

这些作为方法和可选案例保留。菲律宾口音、土著时代、9:16、无晃动、黄色字幕、某个倍速、具体 voice ID 均不成为跨项目默认值。

## 未测与后续

没有调用图片/视频/TTS 模型，没有实际试听、媒体渲染、真实小说全链路、客户端自动加载或旧应用兼容测试。本轮可交付的是可调用的专业指导与有界文本行为证据，不是新的无人值守生产运行时。

[独立优化票](follow-up-tickets.json) 保留两个非阻断交接措辞问题，以及一次预算聚合改进。[迁移映射](../../docs/drama-skill-migration.md) 中 MIG-01～04 涵盖应用适配、授权安装、项目 preset 和按真实使用再拆 Skill；本轮不自动执行。

## 索引与回退

- [完整入口/用法](../../README.md)
- [独立任务/分支索引](../../changes/DRAMA-SKILLS-20260831/sessions.json)
- [任务与历史来源](../../changes/DRAMA-SKILLS-20260831/tasks.json)
- [公共内容交接](../../docs/content-production-contract.md)

原主分支基线：`cd990aaec765fcbd1731af970233484377c873aa`；候选集合合并：`20dffae3b2d77dbe62cd151a0f26d2c5254c330b`。完整候选 hash 留于 source-acceptance 和 sessions。回退应在新分支创建 revert 候选并检查受影响入口，不重写 main、不删历史 worktree、不覆盖已安装副本。
