# Content Skills

Ticket: https://github.com/incentlie-design/narrated-drama/issues/112

Content Skills are a **second catalog**. They do not replace the nine engineering Skills
and they are **not** counted against that engineering cap.

They serve narrated-drama content work (REQ-75 R1–R6): 10 episodes, 60–120s, 解说剧 /
漫剧 / 漫画-adjacent production. Methods were distilled from a bounded public probe
(GitHub + articles + standards). Third-party text is data, not a copy-paste library.

| Read this | When |
| --- | --- |
| [TAXONOMY.md](TAXONOMY.md) | 分类与 R1–R6 映射 |
| [SECURITY.md](SECURITY.md) | 安全筛查规则与排除类 |
| [INDEX.md](INDEX.md) | 人类可读索引 |
| [index.json](index.json) | 机器可读索引（≤200） |
| [registry.json](registry.json) | 可调用 content Skills |
| [I/O 契约](../../docs/content-skill-io.md) | 共享字段、信封、角色路由 |
| [io/](io/) | fields / skills / roles JSON |
| [content production contract](../../docs/content-production-contract.md) | 安全与禁止事项 |

## Routing

Load **one** Skill for the current action. Do not load the whole catalog.

| Action | Skill |
| --- | --- |
| 小说 → 十集 60–120s 改编策略与大纲 | [content-adaptation-shortform](content-adaptation-shortform/SKILL.md) |
| 系列 canon / story bible / 谁在何时知道什么 | [content-story-bible-canon](content-story-bible-canon/SKILL.md) |
| 人物动机、对白声口、角色区分 | [content-character-development](content-character-development/SKILL.md) |
| 人物外形锁定、三视图、可变项 | [content-character-visual-lock](content-character-visual-lock/SKILL.md) |
| 单集旁白/对白剧本与时长预算 | [content-episode-writing-narration](content-episode-writing-narration/SKILL.md) |
| 分镜表、镜号、切点 | [content-storyboard-shotlist](content-storyboard-shotlist/SKILL.md) |
| 景别、轴线、画幅、运镜动机 | [content-cinematography-shortform](content-cinematography-shortform/SKILL.md) |
| 场面调度、站位、视线 | [content-scene-blocking](content-scene-blocking/SKILL.md) |
| 漫画格、gutter、转场类型 | [content-manga-panel-language](content-manga-panel-language/SKILL.md) |
| 跨集连续性审查 | [content-continuity-review](content-continuity-review/SKILL.md) |
| 旁白/角色声音身份 | [content-voice-narration-design](content-voice-narration-design/SKILL.md) |
| 配乐、BGM、主题音乐床 | [content-music-bed-design](content-music-bed-design/SKILL.md) |
| 环境音、背景音、拟音、room tone | [content-ambience-foley](content-ambience-foley/SKILL.md) |
| 混音、响度、duck、60–120s 实测 | [content-audio-mix-probe](content-audio-mix-probe/SKILL.md) |
| 生成图身份一致性（方法，非选型） | [content-image-identity-consistency](content-image-identity-consistency/SKILL.md) |
| 60–120s 剪辑节奏 | [content-editing-rhythm-60s](content-editing-rhythm-60s/SKILL.md) |
| PASS/REWORK/ABANDON 量表 | [content-evaluation-rubric](content-evaluation-rubric/SKILL.md) |
| 系列不变量与变化规则 | [content-series-identity-lock](content-series-identity-lock/SKILL.md) |
| 提示词安全与 provenance | [content-prompt-safety-provenance](content-prompt-safety-provenance/SKILL.md) |
| 短制制作计划与并行边界 | [content-production-plan-shortform](content-production-plan-shortform/SKILL.md) |
| 有限动画、hold/cycle/smear | [content-limited-animation](content-limited-animation/SKILL.md) |
| 静帧驱动 I2V、一镜一动作 | [content-image-to-video](content-image-to-video/SKILL.md) |
| Animatic 时码预览 | [content-animatic-timing](content-animatic-timing/SKILL.md) |
| 色彩脚本与主光方向 | [content-color-lighting](content-color-lighting/SKILL.md) |
| 系列画风锁（与人物骨相分开） | [content-style-frame](content-style-frame/SKILL.md) |
| 竖屏字幕安全区 | [content-subtitle-layout](content-subtitle-layout/SKILL.md) |
| 转场种类与理由 | [content-transition-design](content-transition-design/SKILL.md) |
| 循环背景层 | [content-looping-background](content-looping-background/SKILL.md) |
| 表情表（默认闭口，非唇形克隆） | [content-expression-sheet](content-expression-sheet/SKILL.md) |
