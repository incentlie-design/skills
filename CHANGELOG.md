# Changelog

## 0.1.0 — 2026-08-31（本地初版，未远端发布）

- 建立单一 skill-creator repo、分类命名、路由登记、内部资源与外部契约规范。
- P0 优先形成 skill 生命周期与 Git/worktree/project/session/agent 协作基础。
- 在冻结公共契约后并行制作需求、评审、测试、流水线与广告导演学习能力；完整清单见 README。
- 新增 skill 元数据、每 skill 三类测试场景、标准库验证器、本地流水线和有限验收记录。
- 本 repo 采用受影响 unit/feature/smoke + 冻结批次 integration；不继承旧规则中的自动全回归。

兼容性：首次引入，没有覆盖或迁移现有全局已安装 skills。`skill.json` 与 `registry.json` 是本项目格式。运行时产物契约 v1，首版不承诺 ADK 原生执行或无人值守研发。

升级/回退：后续升级参照 docs/skill-standard.md；本轮精确提交和验证范围由 Git 历史与 reports 记录。没有 push、远端仓库、正式 tag 或发布。回退使用新的 revert 候选，不改写共享历史。
