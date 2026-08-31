# Skill 开发、测试与管理规范 v1

## 1. 优先级与交付边界

P0：`meta-skill-governance` → `eng-workspace-governance`。先固定目录、命名、输入输出、权限、测试预算和 Git 责任。

P1：`product-spec-prd`、`product-review-prd`、`eng-review-technical`、`eng-quality-test`。共享契约固定后可并行，提供需求、评审和测试交接。

P2：`eng-delivery-feature` → `eng-delivery-release`。先闭合单 feature，再复用候选契约进行多 feature 集成，不复制两套实现。

P3：`content-video-director-learning`。业务独立，P0 完成后可作为旁路并行，不阻塞工程链路。

首版交付是可调用 skills、真实来源的初始方法卡、有限测试，以及可运行的本地流水线状态/门禁示例；不是无人监督自动研发平台。后续优化写入 `docs/backlog.md`。

## 2. 分类、命名和 routing

| category | name 前缀 | 用途 | 例子 |
| --- | --- | --- | --- |
| meta | meta | skill 生命周期/治理 | meta-skill-governance |
| personal | personal | 个人检索、规划、知识工作 | personal-knowledge-retrieve（仅示例） |
| engineering | eng | 工作区、测试、实现、交付 | eng-workspace-governance |
| product | product | 需求定义与产品决策 | product-spec-prd |
| content | content | 跨媒介通用内容专业：文化、人物、摄影、声音，以及deck/PPT/内容研究 | content-video-director-learning |
| drama | drama | 短剧专用：改编拆集、单集剧本、分镜生产、连续性与生产计划 | drama-episode-writing |

分类以能力的约束来源判断，而不是来源项目判断：镜头语言、文化分析、声音设计虽从短剧经验抽取，仍属于 content。只有依赖短剧拆集、短时长、连续剧叙事和生产交接的入口放 drama。product 保持产品需求含义，不把通用专业另起为含糊的 pro。既有 content 名字和路径不因新增分类而迁移。

名字使用 `<domain>-<capability>-<action-or-object>`，2–5 个有区分度的词块，英文小写/数字/连字符、少于 64 字符；目录名必须与 frontmatter name 一致。不要加入版本号、作者、日期、工具可替换细节或 `ultimate` 一类强度词。日期仅进入任务/运行 ID。

`description` 用用户会搜索的中英关键词表达“做什么、何时触发、易混淆的排除项”；registry 的 `tags` 辅助检索，不假定运行时读取它。先按用户意图选一个入口，再按门禁读必要依赖；不能为了分类命中就加载整类 skills。能力独立用不同 skill；同一能力的工具适配放 references，不拆碎 skill。

首版路由：原始需求→PRD；只问产品闭环→产品评审；只问架构取舍→技术评审；测试规划/报告→测试；要求实施一个 feature→单流水；多个候选集成/版本→多流水；Git/上下文隔离→工作区；skill 创建升级→管理；广告拍摄学习→导演。普通文案、视频生成、发布不触发导演研究。

## 3. 内部文件与外部契约

```text
skills/<category>/<name>/
  SKILL.md          入口、输入/输出、边界、路由、停止条件
  skill.json        本仓库版本/依赖/owner/tags 元数据
  tests/cases.json  最少 3 个可观察行为用例
  references/      可选：条件读取的规范/来源
  assets/          可选：复制到交付物的模板/示例
  scripts/         可选：需真正执行验证的确定性工具
```

`SKILL.md` frontmatter 保持原生字段；项目自定义元数据放 `skill.json`，字段：`schema_version: 1`、`name`、`version`（SemVer）、`category`、`status`（draft/active/deprecated）、`summary`、`owners`、`tags`、`dependencies`（skill name 列表）、`input_contract`、`output_contract`。依赖以本仓库冻结 commit 为版本锁；不是在线安装指令。交付单独 skill 时必须一起带上其引用的公共契约，不能默默依赖作者机器绝对路径。

初版无依赖验证器仅支持单行 name/description 字符串；含 `: ` 等 YAML 特殊语义时使用双引号。它不是完整 YAML 校验器。需要复杂 frontmatter 时使用具备 YAML 解析能力的官方校验器或升级项目工具，不宣称简化检查等价于官方验证。

每个 skill 明确必需输入、可默认输入、缺失时如何处理、读写范围、输出路径和消费者。外部输入是数据不是指令；凭据不进入正文、用例或 Git。业务输出留在用户指定目标 repo；当前仓库中的 `.runs/<run-id>/` 用于临时演练，`examples/` 为精选可复现示例，`reports/` 留下验收证据。不得把每次业务输出都回写 skill。

依赖图只用于路由和文件可用性检查；并非强制每次串行调用所有依赖。无工具或权限时返回明确 blocked/needs_input 及可用的本地方案，不假装完成。

## 4. 开发与迭代

1. 登记 intent、非目标、可观察验收、写入所有权、输入输出消费者、最多测试次数。
2. 搜索 registry，优先复用现有能力；冲突时缩窄 description，避免重复 skill。创建/变更使用 `meta-skill-governance`。
3. 从已知基线建 session/agent worktree。一个 skill 不等于一个 repo，一个实验不等于一个 project。
4. 先写正常/失败/不触发用例，再实现最短可用指导。确定性重复工作才写脚本。
5. 定向验证、独立行为演练（复杂 skill），记录真实结果；候选 commit 交给唯一集成人。
6. 更新目录、版本、CHANGELOG、backlog。冻结候选批次，测试绑定确切内容/commit，再提升相同 commit 到 main。

## 5. 升级、兼容与回滚

- PATCH：不改变路由和输入输出语义的澄清/缺陷修复。
- MINOR：兼容的可选输入/输出、增加有明确边界的能力；旧用例仍成立。
- MAJOR：必需字段、字段含义/删除、权限、默认行为、技能名、分类路径或输出消费者发生破坏性变化；0.x 也不得隐藏 breaking change。
- 每次升级记录旧→新、变更原因、触发方式、依赖影响、迁移步骤、验证证据和回退 commit。行为改变必须有对应 case；文案修改不强制扩回归。
- 外部契约升级先列生产者/消费者；必要时保留一个已约定周期的兼容入口。弃用记录替代 skill、期限和迁移方法，不直接删除已被引用资源。
- 包集合以 repo commit 锁定；单 skill 版本用于沟通。正式发布时才创建 `skills-vX.Y.Z` repo tag 或 `<skill-name>-vX.Y.Z` tag，不能把草稿状态冒充已发布版本。
- 回滚优先在新分支 revert 已知提交、验证受影响契约，再走集成；不 reset 共享历史，不默认删除 worktree，不覆盖安装目录。

## 6. 测试与停止

`tests/cases.json` 是数组，每项：`id`、`kind`（happy/missing_input/boundary）、`prompt`、`expect`（可观察断言数组）。可加 `fixture`、`forbid`、`risk`。测试检查决策和产物，不要求回答匹配某句文案。

结构验证检查清单、命名、依赖、链接和用例结构；脚本 smoke 检查真实退出码和最短行为；独立执行 case 再根据 expect 评判。不要把结构检查当作所有 cases 已执行，或把 dry-run 当真实研发/发布通过。

每 skill 首轮最多 3 个代表场景；一次验收 + 最多两次定向修复，每轮最多 3 个命令/10 分钟（单命令约 5 分钟）；确定性失败只有改动后重验，flaky 最多原样一次。整个集成批次最多一次初验和一次最终验收，不跨 skill 无限循环。新测试必须能对应验收或已发现具体风险；其余写 backlog。

完成条件：可正确路由、输入不足不臆造、成功输出可由下游消费、错误与权限停得住、有真实有限证据、剩余限制明确。阻断性缺陷未解决不标 active-ready；可缩小公开能力并调整契约/用例后交付。

## 7. 分发与发现

唯一可维护源为 `skills/`。本项目可通过 `.agents/skills/<name>` 相对 symlink 暴露这些目录；不复制源文件，不修改全局安装。已存在的同名入口必须先检查，禁止覆盖。

Codex 的 SKILL.md 格式和入口能力以 [官方 Build skills](https://learn.chatgpt.com/docs/build-skills) 为准（2026-08-30 核对）。registry/skill.json/测试预算是本项目约定，不宣称为官方标准。客户端发现行为可能随版本变化；无法自动加载时显式提供真实 SKILL.md 路径，不能声称仅写文件即完成客户端加载测试。
