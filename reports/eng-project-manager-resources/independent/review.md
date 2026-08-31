# PM-SKILL-002 有界独立验收

- schema_version: 1
- run_id: PM-SKILL-002-independent-20260831
- change_id: PM-SKILL-002
- repo: /Users/jiajun.lai/.codex/worktrees/1e05/skill-creator
- base_commit: cd990aaec765fcbd1731af970233484377c873aa
- artifact_revision: 1
- reviewed_revision: 1（本次增量交付的版本号，不是旧业务台账 revision）
- author / next_owner: 工程实践-eng-project-manager / 01a055de-2854-7bf3-a26f-e916849ba46a
- reviewer: 01a05360-3ad2-7211-a3b5-48d7fe3189df；未参与本次增量实现
- subject_commit: 3c502bb7720d002842ee0b4ecd803c7f5464a281
- observed_integration_head: 8d2b607aaeef9cc0cda30c53e9d590065dfa7c20
- status / handoff: pass（仅本次载荷及下述有界独立验收；不等于已合并、安装、部署）
- findings: []

## 范围和独立性

依据用户补充的原始需求：管理 TASK 分给哪些 agent/session、各自资产和预算、每个 goal 的明确 DAG 目标。先读主入口、数据/工作包/预算契约、现有公共契约和相关实现，再自建搜索功能的合成数据与断言。未读取或导入作者 tests/cases.json、tests/test_pm.py 或其 factory；完成测试后才核对 intent 和作者报告头的 artifact_revision。

只读候选、登记文件及其他 skills；仅在本临时目录建立测试源、合成数据、台账和日志。没有创建任务/subagent/repo/自动化，没有修改原生 goal、预算、main 或全局入口。未读取无关项目和内部数据库。

## 真实执行与对象绑定

执行命令（cwd 为本临时目录）：

`python3 -B /tmp/pm-skill-002-review.lxfV7q/independent_acceptance.py`

- 实际退出码：0；三场景全部执行通过，非零测试/仅结构检查。
- 开始：2026-08-31T15:35:28.390553+00:00；结束：2026-08-31T15:35:30.368787+00:00。
- 环境：本机 Python 3.14.2，标准库，CLI 子进程，`-B` 避免源码目录 cache 写入。
- 一条顶层行为验证命令，内部 19 次短 CLI 调用；每次命令、退出码、stdout/stderr 在 execution.json，不隐藏拒绝输入的 exit 2。
- 随后一次有界对象一致性检查：`git diff --exit-code 3c502bb7720d002842ee0b4ecd803c7f5464a281 HEAD -- skills/engineering/eng-project-manager/SKILL.md skills/engineering/eng-project-manager/scripts/pm.py skills/engineering/eng-project-manager/references/contract.md skills/engineering/eng-project-manager/references/assignments-and-budgets.md skills/engineering/eng-project-manager/references/usage.md`，退出码 0。
- 初读 HEAD 为候选 3c502bb；集成人在本次审查期间切换到集成 head 8d2b607，五个受审文件与候选完全相同。脚本执行前后 SHA256 一致。结论绑定这些载荷，不借此宣称其他 skills 或所有集成路径经过重验。
- 本次约三分钟内完成，没有修复或重跑；未使用剩余测试额度。

| 文件 | SHA256 |
| --- | --- |
| scripts/pm.py | ad3fbee160826d795bbf1d9f18e5b15f4a50a155ed047e165638aa3f8508bc3e |
| SKILL.md | 42cab20b03ee37f11fa2adf76ef550cb1e60fefb6697553067474af7bad1ef36 |
| references/contract.md | 5515c4f37ac172316e2e324aae0c3a2cfe7becc0912c0c6c997d6e17f67ab1e9 |
| references/assignments-and-budgets.md | 4d3e1333aee8fdbe60d97a75f29ec2d51dc85d8ed2126f5260f08148e6d4b7d4 |
| references/usage.md | b0418c3c4c4dd72b540c13d12a98367bc731e33e866fc14b4db32452c06da698 |
| 独立测试源 independent_acceptance.py | 1478c492b42d8a9984098336ab15d5298cbee8b7d21d33613d7633092cac46fe |

## 三个场景的观察

| 场景 | 可观察断言及结果 | 状态 |
| --- | --- | --- |
| 正常：共享任务、两位执行者与明确转交 | 两个 AC 复用 T1；两项 work_package 有具体目标/完成条件/资产/范围/停止条件。累计 80→120 加另一分配 35，goal 只计 155，不加历史 80、不沿两个 AC 重复计。T2 受未完成 T1 阻塞。转交新增 AS-C，旧 AS-A 保留 120 和 current 交付；新执行者明确零观测才计 0，未继承旧资产交付。goal 未分配余额 130；artifact_revision 保持 1、ledger_revision 增至 2，旧快照保留。agent/session 交集筛选及 brief 输出通过。无完成证据，goal 仍 incomplete。 | pass |
| 缺失/失败：旧台账、身份/实测/资产缺口与过期 | 无 management/work_package 的旧 v1 台账正常读取，显示 not_recorded 和两个工作包缺口，不从 owner 冒造分配。缺 session 告警；另一任务只有估算 60，不计实际消耗，总量/剩余 null，已知小计 120、未知清单 AS-B。删除合成 asset 后交付 stale_or_unverified。48 小时后保留历史 reported_used=120，current_used=null。 | pass |
| 越界：拒绝非法变更且不损坏台账 | ../ 路径、依赖环、累计消耗回退、跨 goal TASK、原地改 agent、无新批准来源加预算、覆盖原始 goal 共七项均 exit 2 / needs_input；每次台账字节完全未变，无残留 lock。 | pass |

上表是实际程序行为测试，数据为独立合成 fixture。不是对真实用户预算、原生 agent 分配或产品 goal 完成的证明。各子步骤的完整原始 JSON 输出保存在 execution.json。

## 技术闭环与取舍

- WBS/DAG：沿唯一原始 goal→REQ→AC→TASK 建模，共享工作项保持一个 ID；工作包定义具体目标和停止点，缺项明确作为 gap。typed DAG 和完成依赖图分别防环；work_package 范围变化纳入已有 revision/scope_decision 门禁。正常和越界场景覆盖了关键路径。
- 分配与历史：assignment 身份不等于 owner，也不等于 session；转交使用新 ID，历史使用量/交付只追加且不迁到新执行者。新增/调整预算依赖新来源 decision，脚本只记录授权，不证明实际授权。实际执行验证了身份保护、转交和无批准预算调整拒绝。
- 资产：expected_assets 是承诺；带 assignment ID、revision、hash 和来源的 receipt 是交付声明；文件可用性与任务验收分开。交付不自动把任务置 done。删除资产和转交不继承覆盖这一边界。
- 预算：累计 observed 与 estimated 分列，按 assignment ID 去重；不同单位不相加；未知/过期不当零。goal 限额与执行分配不双计。预算告警不自动更改 goal、预算或业务状态。超支/超额分配公式和有限非负数字校验作了代码审查，本次未新增其运行时场景。
- 历史兼容：0.2.0 以可选 work_package/management 扩展 v1；旧台账的读取回退已执行，未重新批准旧版所有行为。原始目标不变和有来源证据的语义仍保留。
- 权限：入口明确排除分派、消息、原生 goal 修改和调度；pm.py 无网络、shell 执行、产品工具调用路径。只支持本地读取和显式 state 写入。资料里的命令不构成权限。
- 选择：复用既有 snapshot/ledger/验证链、增加小范围管理字段；不改则无法满足分配和预算需求，仅以自由文本维护又无法稳定去重、保留沿革和校验。未引入新运行依赖或后台平台。真实工具计量接入、并发性能优化等维持明确非目标。

## 未测边界与后续责任

未实跑真实 Codex agent/session 读取、原生计量接入、后台自动化、全局 discovery 刷新、远端动作、全仓回归、完整旧版证据矩阵、多进程并发或大台账性能。minutes/commands/cost_usd 的运行时算术、预算超支/超额分配等未另开场景；仅审查共享实现。这些不扩大本次明确的本地记录管理验收。

没有阻断发现，不追加推测性优化。唯一集成人应封存本测试源和原始结果、完成自己的冻结集成检查及状态文档更新；如果提升载荷改变，重新作影响分析，不能无条件沿用本报告。注册/合入 main 由原任务负责，本评审未执行或授权额外外部动作。
