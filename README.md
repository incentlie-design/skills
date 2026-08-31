# skill-creator

统一管理个人 skills 的源仓库：一个 repo、分类目录、共享契约、独立 worktree、有界测试。不会为每个 skill 新建仓库，也不会为每次探索创建新项目。

当前登记 24 个本地源 Skill，均为 `0.1.0` / `active`：原有 10 个入口保持，新接纳短剧专用 5 个、通用内容专业 9 个。`active` 表示已完成本库有界源码/行为验收，不表示媒体生成质量、应用接线或当前客户端自动加载已经验证。

## Skill 清单与路由

| 优先级 | 分类 | Skill | 何时使用 |
| --- | --- | --- | --- |
| P0.1 | meta | [meta-skill-governance](skills/meta/meta-skill-governance/SKILL.md) | skill 开发、分类、测试、升级、停用 |
| P0.2 | engineering | [eng-workspace-governance](skills/engineering/eng-workspace-governance/SKILL.md) | Git/repo/worktree/branch/project/session/agent 的职责与隔离 |
| P1 | product | [product-spec-prd](skills/product/product-spec-prd/SKILL.md) | 原始需求转 OpenSpec 风格 PRD、spec 与多 agent 任务 |
| P1 | product | [product-review-prd](skills/product/product-review-prd/SKILL.md) | 产品闭环、防扩张与有边界的优化建议 |
| P1 | engineering | [eng-review-technical](skills/engineering/eng-review-technical/SKILL.md) | 技术闭环、历史一致性、架构与成本取舍 |
| P1 | engineering | [eng-quality-test](skills/engineering/eng-quality-test/SKILL.md) | 增量测试规划、评审、用例、执行和报告 |
| P1 | engineering | [eng-project-manager](skills/engineering/eng-project-manager/SKILL.md) | 长程 goal 的接入、DAG/阻塞查询、刷新对账与四层产物索引；不改原生 goal |
| P2.1 | engineering | [eng-delivery-feature](skills/engineering/eng-delivery-feature/SKILL.md) | 单一 feature 的需求→设计/测试→评审→实现→候选 |
| P2.2 | engineering | [eng-delivery-release](skills/engineering/eng-delivery-release/SKILL.md) | 多 feature 候选、repo 版本与冻结集成批次 |
| P3 | content | [content-video-director-learning](skills/content/content-video-director-learning/SKILL.md) | 广告拍摄方法研究、来源采集与本地方法卡 |
| P3 | content | [content-cultural-research](skills/content/content-cultural-research/SKILL.md) | 文化背景、适配距离、有界研究、来源冲突与可操作约束；非短剧专属 |
| P3 | content | [content-character-development](skills/content/content-character-development/SKILL.md) | 人物动机、关系、选择与代价、心理弧线；不以外形代替人物理解 |
| P3 | content | [content-visual-worldbuilding](skills/content/content-visual-worldbuilding/SKILL.md) | 项目视觉风格、时代材质、灯光色彩、地点尺度和道具状态 |
| P3 | content | [content-character-visual-design](skills/content/content-character-visual-design/SKILL.md) | 人物身份、年龄皮肤、轮廓服饰、允许变体与视角化提示词 |
| P3 | content | [content-cinematography](skills/content/content-cinematography/SKILL.md) | 叙事视角、景别构图、轴线、运镜与原生画幅；不强制正脸 |
| P3 | content | [content-scene-blocking](skills/content/content-scene-blocking/SKILL.md) | 走位、目光、反应、道具持有与接触/释放动作状态 |
| P3 | content | [content-voice-design](skills/content/content-voice-design/SKILL.md) | 年龄、地域口音、音色身份、候选比较与选定；供应商细节条件读取 |
| P3 | content | [content-audio-production](skills/content/content-audio-production/SKILL.md) | 台词/指导分离、说话人与音色映射、表演、环境/音效/音乐及局部声音修复 |
| P3 | content | [content-editing-rhythm](skills/content/content-editing-rhythm/SKILL.md) | 镜头与台词同步、停顿修剪、时间映射、字幕及局部节奏调整 |
| P3 | drama | [drama-series-adaptation](skills/drama/drama-series-adaptation/SKILL.md) | 原著理解、全剧因果、拆集目标、伏笔回收与正典来源 |
| P3 | drama | [drama-episode-writing](skills/drama/drama-episode-writing/SKILL.md) | 单集完整剧本、人物递进、旁白知识边界、转场与台词注册表 |
| P3 | drama | [drama-storyboard-production](skills/drama/drama-storyboard-production/SKILL.md) | 场景→镜头→帧状态，台词/人物/资产引用及可交接分镜提示词 |
| P3 | drama | [drama-continuity-review](skills/drama/drama-continuity-review/SKILL.md) | 叙事、身份、知识、道具、声画跨集连续性；只评有证据的范围 |
| P3 | drama | [drama-production-planning](skills/drama/drama-production-planning/SKILL.md) | 按缺口选择 Skill，串行多集计划、预算、局部变更影响与交接 |

`content-*` 可用于小说、游戏、电影、广告等；`drama-*` 才依赖短剧拆集、单集时长及连续叙事。沿用已有 `product-*` 表示产品需求，不把通用专业另命名为含糊的 `pro-*`。表中优先级用于能力建设，不要求每次全量调用。

`personal`（个人效率）为保留类别，目前没有占位 skill。内容类未来可用 `content-deck-*`、`content-ppt-*`、`content-video-*`；只有真实能力才建目录。`registry.json` 为清单源；每个 `skill.json` 保存版本、tags、依赖和输入输出摘要，它是本项目元数据，不是 Codex 原生配置。

## 如何开始

在当前项目任务中调用名字，例如：

```text
使用 $product-spec-prd，把以下原始需求整理成一个可交接的 change，先不实现。
使用 $eng-review-technical，评审 changes/C1/design.md，模式为实现优先。
使用 $eng-quality-test，为这个局部 feature 制定增量计划，不进入发版回归。
使用 $eng-project-manager，接入指定主任务的 goal 和交接快照，核对原始目标、依赖阻塞及主要产物。
使用 $eng-delivery-feature，按已确认的 C1 需求走单 feature 闭环。
使用 $content-video-director-learning，检索“产品质感布光”，最多读 4 个公开页面。
使用 $drama-series-adaptation，把授权范围内的原著整理成全剧故事与拆集方案，保留来源和推断区别。
使用 $content-character-development，分析人物渴望、关系、选择代价与弧线，不生成形象。
使用 $drama-storyboard-production，将选定剧本、人物/风格引用转成分镜脚本；只做前置设计，不调用媒体模型。
使用 $content-cinematography，为这个横屏电影场景设计镜头语言，不套用短剧画幅。
使用 $drama-production-planning，检查已有产物缺口，安排串行多集前置制作；不要执行生成。
```

本项目 `.agents/skills/` 使用相对 symlink 指向 `skills/`，只保留一份源文件。Codex 官方说明支持该 repo 发现目录和 symlink；如当前会话尚未显示新 skill，可新开任务/重启客户端，或明确提供上表 `SKILL.md` 路径。没有修改用户级 skills 或把本项目 skills 安装到其他项目。[官方加载规则](https://learn.chatgpt.com/docs/build-skills)

检索示例（在项目根目录执行）：

```sh
rg 'worktree|branch|session' registry.json skills -g SKILL.md -g skill.json
rg '布光|分镜|镜头' knowledge/video-director
python3 scripts/validate_skills.py --check-discovery
python3 -m unittest discover -s tests
python3 scripts/pipeline.py --help
```

验证器使用 Python 标准库。它检查登记、受限 frontmatter 格式、依赖、链接和 cases 结构，**不会把定义用例算作执行通过**；独立行为执行证据另见 reports。官方 quick_validate 另需 PyYAML；本次项目经理 skill 检查通过，首版当时的依赖限制保留在原验收报告中。

## 最小闭环

```text
原始需求 → PRD/spec/tasks → 产品/技术/测试计划评审 → 实现
                                                       ↓
多条 feature → 固定候选 commit ← 独立 review + 定向测试
                     ↓
           冻结批次与 head → 集成验证 → 稳定基线
```

流水线脚本是无外部调用的本地节点/门禁实现。它消费产物和证据，演示模式使用明确标记的 fixture；不自动写代码，不代表已运行真实应用测试，不执行 Git 合并/远端发布。实际工作由人或获授权 agent 完成节点，再提供相应版本的产物。Google ADK 适配、模型调用与调度服务不在初版范围内。

## 维护入口

- [AGENTS.md](AGENTS.md)：本项目强制边界、协作规则和 skill 登记。
- [开发、测试、升级规范](docs/skill-standard.md)：命名、内外契约、版本迁移与停止条件。
- [公共交接契约](docs/contracts.md)：REQ/AC/task/review/candidate/test-report。
- [后续迭代 backlog](docs/backlog.md)：有触发条件和验收的优化项。
- [CHANGELOG](CHANGELOG.md)：版本变更与兼容性记录。
- [短剧/通用专业整理验收](reports/drama-skill-intake/integration-report.md)：14 个独立任务、分类结果、真实行为证据与未测范围。
- [独立任务索引](changes/DRAMA-SKILLS-20260831/sessions.json)：每个 Skill 的独立任务 ID、分支、worktree 和冻结候选 commit。
- [短剧整理任务边界](changes/DRAMA-SKILLS-20260831/brief.md)：目标、验收、所有权；[任务清单](changes/DRAMA-SKILLS-20260831/tasks.json) 保留来源和交接记录。
- [旧入口迁移映射](docs/drama-skill-migration.md)：旧生产系统、narrated-drama 与个人音色 Skill 的保留/拆分/合并关系，不自动替换安装。
- [内容生产交接](docs/content-production-contract.md)：来源、身份/台词/镜头引用、设计与真实生成证据的边界。
- [首版验收报告](reports/validation-20260831.md)：27 个原始行为场景、1 次治理定向复验、22 项通过的程序测试，以及明确未执行的检查。
- [项目经理 skill 独立验收与产出索引](reports/eng-project-manager/independent-review.md)：专属任务、原始目标核对、DAG、四层文件索引、六个程序场景及真实接入重放；[候选验证](reports/eng-project-manager/validation.md) 保留历史证据。
- `reports/`：本轮真实验收、覆盖范围与未执行检查；业务运行临时文件放 `.runs/`，不进入 Git。

工作分支允许局部 unit/feature 和 smoke；跨 feature 批次再做受影响 integration；只有明确发版才做 release regression。默认一次验收、最多两次定向修复，批次完整验收最多两轮。完成外部契约即交付，不无限优化内部实现。

源文件在本仓库，业务产物放对应业务 repo。所有并行 agent 的工作树共用本 repo 的 Git 对象库；本地候选 commit 不等于已发布版本。外部写入、生产操作、全局安装与删除清理仍需明确授权。
