# 既有短剧 Skill 整理与兼容映射

本轮已在 skill-creator 登记 14 个新源入口，详见 [集成验收报告](../reports/drama-skill-intake/integration-report.md)。

本表是 source-library 重组，不会自动更改旧应用路由或已安装 Skill。旧源仍保留，当前没有弃用期限；新入口不能冒充旧 JSON schema 的 drop-in replacement。主控/Registry/运行时接线属于后续单独优化票。

只读来源：drama-agents/.agents/skills 和 knowledge（main 052fc44）；drama-skills/narrated-drama-*；个人 elevenlabs-voice-design。绝对开发路径只在变更工单记载，交付 Skill 的运行说明不得依赖作者机器。

| 旧入口 | 新归属 | 处理与边界 |
|---|---|---|
| production-cultural-research | content-cultural-research | 合并研究判定/证据方法；旧版只包装captures不等于已搜索 |
| episode-localization-direction | content-cultural-research | 本地化适配是研究的下游决定，不固定每集重调 |
| series-story-intelligence | drama-series-adaptation | 来源理解与事实映射 |
| series-story-architecture | drama-series-adaptation | 整体因果、拆集与回收 |
| series-character-bible | content-character-development | 跨媒介人物心理/关系/弧线 |
| series-character-visual-development | content-character-visual-design | 选定身份与视觉prompt；注册留应用 |
| series-visual-style-bible | content-visual-worldbuilding | 项目风格权威，不拷贝app envelope |
| series-location-prop-design | content-visual-worldbuilding | 地点/道具/材质/尺度与状态 |
| series-audio-bible | content-voice-design + content-audio-production | 身份与表演/声音层分别所有权 |
| episode-contract-planner | drama-episode-writing | 单集任务→完整剧本；DAG派发另属planning |
| episode-scene-breakdown | drama-storyboard-production + content-scene-blocking | 场景拆分归分镜，空间/动作规则归调度 |
| episode-audio-performance | content-audio-production | 台词指导分離、speaker与voice引用 |
| episode-visual-storyboard | drama-storyboard-production | 帧/镜头/台词映射与原生画幅 |
| series-continuity-supervisor | drama-continuity-review | 跨集正典、资产、知识边界 |
| episode-editing-rhythm | content-editing-rhythm | 同步/局部节奏修改 |
| episode-assembly-subtitle | content-editing-rhythm | 字幕与剪辑交接；渲染器不迁入 |
| episode-review-eval | drama-continuity-review | 叙事/阶段可评范围；代码测试仍eng-quality-test |
| artifact-manifest-lock | 应用工程，保留旧入口 | 文件锁、写Ledger、CAS不是创作方法；planning只消费事实 |
| episode-action-choreography | content-scene-blocking | 旧deferred候选的方法抽取，不宣称旧runtime已启用 |
| episode-performance-direction | content-scene-blocking | 目光/反应/动作表演 |
| episode-cinematography-direction | content-cinematography | 通用镜头语言 |
| episode-lighting-color-direction | content-visual-worldbuilding | 灯光色彩与材质风格 |
| series-costume-visual-design | content-character-visual-design | 服饰身份/变体，不另立竞争权威 |
| narrated-drama-brief | drama-series-adaptation | brief/bible/storyline知识；working指针不直接移植 |
| narrated-drama-assets | content-character-visual-design + content-visual-worldbuilding | 稳定ID/定义/允许变体与来源 |
| narrated-drama-skill | drama-production-planning | 版本与受影响范围方法；不搬目录管理runtime |
| elevenlabs-voice-design（个人安装） | content-voice-design 的供应商reference | 保留个人原名/安装，不复制密钥，不默认为同版替换 |
| content-video-director-learning（本仓库） | 原入口保留 | 广告研究/学习，不因新摄影入口扩大为制作工具 |

## 后续单独票

- MIG-01：明确一个业务应用的调用契约后，映射旧产物schema到本库设计产物；未做前保持旧runtime。
- MIG-02：用户选择目标安装范围后，才创建导出/安装和旧入口兼容别名；不得静默全局覆盖。
- MIG-03：项目preset管理：文化/语言/画幅/人物版本/voice lock 单独保存，不进通用Skill默认值。
- MIG-04：积累真实跨题材使用证据后，再决定需不需要拆出独立服装、灯光或音乐Skill；本轮不为未来能力造空目录。
