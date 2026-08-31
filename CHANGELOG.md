# Changelog

## 短剧 Skill 整理 foundation — 2026-08-31（候选开发中）

- 新增 drama 分类；跨媒介专业仍使用 content，已有工程/产品/内容入口不更名。
- 规划 14 个独立 Skill 任务，来源整理覆盖旧生产 23 个入口、narrated-drama 三入口及个人音色设计。
- 新增最小内容交接与兼容映射；不修改旧runtime、安装或注册状态。
- 分类校验器兼容新增类别；公共 docs/contracts.md v1 和现有 Skill 版本保持不变。
- 新 Skill 的 0.1.0 状态与最终候选 commit 以独立验收/集成报告为准，不因本条记录宣称已可用。

## eng-project-manager 0.1.0 — 2026-08-31（本地验收完成，未远端发布）

- 新增 engineering 入口：接入既有 goal、原始目标与 typed DAG；查询阻塞、依赖影响、目标覆盖和下一 owner。
- 新增本地 JSON 台账、完整历史与来源、revision 对账、文件 hash 绑定、Mermaid 和四层产物索引。脚本不修改原生 goal、业务文件或远端状态，不带后台自动化。
- 新增三类有限行为场景与父任务真实交接演练；原始目标不改写、fixture 不放行真实完成，独立验收由父任务负责。
- 同步 registry、AGENTS、README 和相对 .agents/skills 入口。未修改其他 skills 的行为或公共契约。
- 父任务完成原始目标逐项独立验收；冻结集成候选上的作者三场景、独立三场景与真实接入重放均通过。修正祖先显式阻塞被汇总覆盖的问题；状态改为 active，验收证据见 reports/eng-project-manager/independent-review.md。

兼容性：新增 skill 与 eng-project-manager/v1 本地快照契约，无旧消费者迁移、无全局安装或发布；共享 docs/contracts.md v1 保持不变。版本依赖由本次候选 commit 锁定。回退基线为 78667f7cb54adb7e5a85c8c7d3b418e7634b7786；回退用新的 revert 候选，不重写共享历史。候选详情和未测范围见 reports/eng-project-manager/。

## 0.1.0 — 2026-08-31（本地初版，未远端发布）

- 建立单一 skill-creator repo、分类命名、路由登记、内部资源与外部契约规范。
- P0 优先形成 skill 生命周期与 Git/worktree/project/session/agent 协作基础。
- 在冻结公共契约后并行制作需求、评审、测试、流水线与广告导演学习能力；完整清单见 README。
- 新增 skill 元数据、每 skill 三类测试场景、标准库验证器、本地流水线和有限验收记录。
- 本 repo 采用受影响 unit/feature/smoke + 冻结批次 integration；不继承旧规则中的自动全回归。

兼容性：首次引入，没有覆盖或迁移现有全局已安装 skills。`skill.json` 与 `registry.json` 是本项目格式。运行时产物契约 v1，首版不承诺 ADK 原生执行或无人值守研发。

升级/回退：后续升级参照 docs/skill-standard.md；本轮精确提交和验证范围由 Git 历史与 reports 记录。没有 push、远端仓库、正式 tag 或发布。回退使用新的 revert 候选，不改写共享历史。
