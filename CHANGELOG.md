# Changelog

## eng-project-manager 0.2.0 — 2026-08-31（draft candidate）

- 按用户补充新增可选 work_package：每 goal 的 DAG 工作目标、完成条件、输入输出资产、修改范围和停止条件。
- 新增有来源的 agent/session 分配与移交历史、预期资产与实际交付、预算上限及累计实测/估算用量；按任务/agent/session 去重汇总，旧执行者的成本和产出不移给新执行者。
- query 增加 --agent/--session 和 goal_dag/management 输出，新增只读 brief；明确未知预算、过期用量、超支及超额分配，不自动调度、分派或改变原生预算。
- 兼容性：0.1.0 → 0.2.0 MINOR，v1 snapshot/ledger 与旧行为保留，新字段可选；旧台账缺管理明细显式 not_recorded。工作目标改变仍升 artifact_revision；纯分配/预算调整只增 ledger_revision 并记录新决策来源。
- 无重命名、分类、依赖或公共契约变更，registry/AGENTS 路由无需迁移。候选基线 cd990aaec765fcbd1731af970233484377c873aa；回退用新 revert 候选，不重写历史。已安装用户入口仍指向主仓库已验收 0.1.0，不把上一版独立验收沿用到本版。
- 作者三个扩充场景与旧版三个兼容场景通过，结构和官方格式检查通过；新一轮独立接受 pending。实际输出、载荷 hash 和展示样例见 [增量候选报告](reports/eng-project-manager-resources/validation.md)。

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
