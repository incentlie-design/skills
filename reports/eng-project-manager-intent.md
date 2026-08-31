# PM-SKILL-001 交付边界

- 原始委派：父任务 `01a05360-3ad2-7211-a3b5-48d7fe3189df`；用户要求新增 engineering / eng-project-manager，追踪长程 goal 的原始目标、拆解 DAG、阻塞与分层产物。
- 基线：`78667f7cb54adb7e5a85c8c7d3b418e7634b7786`；当前 linked worktree `/Users/jiajun.lai/.codex/worktrees/1e05/skill-creator`；分支 `codex/eng-project-manager`。
- 唯一 writer：本委派任务。所有权：新 skill、`.agents/skills/eng-project-manager`、registry/AGENTS/README/CHANGELOG 及本次 reports。其他 skills 和公共契约行为不变。
- 输入：父任务明确交接、现有仓库契约、当前真实产物；真实演练不使用本会话 get_goal 代替父任务 goal。
- 输出：可重复接入/刷新/查询的 skill、标准库本地脚本、机器可读 DAG、Mermaid、四层文件索引、三个实际执行场景、真实快照演练、候选 commit。
- 消费者：主 agent、用户、父任务独立审查者。PM 只更新用户指定本地台账，建议交给主 agent 执行；不是业务实现者、调度服务或完成门禁的最终签字人。
- 验收映射：身份/原意沿革→PM-001/003；DAG/查询/目标遗漏→PM-001/002；刷新/证据→PM-001/002；索引→PM-001/003；工具边界→PM-003及真实演练；登记→结构检查；真实测试→三场景与运行记录。
- 预算：一次验收、最多两次有证据定向修复；每轮最多三个验证命令、十分钟；只做相关 unit/feature + smoke，不跑全仓业务回归。
- 非目标：后台自动化、跨任务原生 goal API、私有数据库、远端写入、业务代码实现、全局安装、合并 main、新任务/subagent/项目/仓库。
- 停止：满足候选契约即交接父任务；独立验收 pending，作者不自签最终通过。
