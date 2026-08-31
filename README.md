# skill-creator

统一管理个人 skills 的源仓库：一个 repo、分类目录、共享契约、独立 worktree、有界测试。不会为每个 skill 新建仓库，也不会为每次探索创建新项目。

当前登记 10 个本地可用 skills，均为 `0.1.0`，包括已完成独立验收的 `eng-project-manager`。实现顺序按依赖安排；P3 导演研究独立，可在基础规范完成后并行。

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
- [首版验收报告](reports/validation-20260831.md)：27 个原始行为场景、1 次治理定向复验、22 项通过的程序测试，以及明确未执行的检查。
- [项目经理 skill 独立验收与产出索引](reports/eng-project-manager/independent-review.md)：专属任务、原始目标核对、DAG、四层文件索引、六个程序场景及真实接入重放；[候选验证](reports/eng-project-manager/validation.md) 保留历史证据。
- `reports/`：本轮真实验收、覆盖范围与未执行检查；业务运行临时文件放 `.runs/`，不进入 Git。

工作分支允许局部 unit/feature 和 smoke；跨 feature 批次再做受影响 integration；只有明确发版才做 release regression。默认一次验收、最多两次定向修复，批次完整验收最多两轮。完成外部契约即交付，不无限优化内部实现。

源文件在本仓库，业务产物放对应业务 repo。所有并行 agent 的工作树共用本 repo 的 Git 对象库；本地候选 commit 不等于已发布版本。外部写入、生产操作、全局安装与删除清理仍需明确授权。
