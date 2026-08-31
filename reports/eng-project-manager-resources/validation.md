# PM-SKILL-002 分配、资产、预算与 DAG 工作目标候选

本页保留作者候选形成时的历史状态；后续独立验收与集成结果见 [本地集成记录](integration.md)。下文 pending 不代表当前状态，也不将历史 fixture 改写成真实用量。

用户补充要求已实现为 eng-project-manager 0.2.0 可选扩展。作者三个行为场景、旧版三个兼容场景、结构和官方格式检查通过。新版本独立验收仍 pending；本页不是作者自签的最终评审。此前 0.1.0 的验收签字不用于放行新行为。

## 身份与范围

- schema_version: 1；run_id: PM-SKILL-002-validation-20260831；change_id: PM-SKILL-002；artifact_revision: 1。
- 原始增量要求和非目标：[intent](../eng-project-manager-resources-intent.md)。目标 repo 是本 skill-creator 单仓库；不把 fixture-goal 当本任务的原生 goal。
- base_commit: cd990aaec765fcbd1731af970233484377c873aa（main 已验收 0.1.0）。
- worktree: /Users/jiajun.lai/.codex/worktrees/1e05/skill-creator；branch: codex/eng-project-manager-resources。
- 测试在本地未提交候选内容上执行；下表 SHA256 锁定实际载荷。候选 commit 在 Git 历史和交付消息中给出，不编造未来 commit。
- 只修改本 skill、README、CHANGELOG 和本次 reports；名称、分类、路径、依赖均未变，registry/AGENTS 已有入口保持有效，无路由迁移。没有改其他 skills、公共契约或历史 0.1.0 报告。

## 用户补充要求的验收证据

| 要求 | 实现和实际观察 | 结论 |
| --- | --- | --- |
| 任务分给哪些 agent/session | assignment 独立 ID 关联 TASK、agent、session、角色、来源、时间和状态；query 反查；PM-001 实跑筛选与转交 refresh，TASK-001 当前分配从 ASN-001 变 ASN-003，首个快照仍保留 running | 本地记录/查询通过；不自动创建执行者，不臆造工具 ID |
| 每个执行者的产出资产 | 分配关联 expected_artifacts；delivery 绑定分配、产物 revision/hash/来源；输出实际路径、文件可用性与交付状态；PM-001 旧分配交付 current，新执行者未继承交付，PM-002 删除真实 fixture 文件后 missing/stale_or_unverified | 分配与实际交付分开，文件存在不证明谁交付，更不代表验收通过 |
| 每个执行者和 goal 的预算 | caps + 有来源累计 observed/estimated；任务/agent/session/goal 是同一组分配的去重视图；PM-001 从累计 100→160 加另一分配 40 得 200，goal 剩余 800；转交后旧执行者仍 160，新执行者凭明确零观测才为 0 | 累计观测/共享 AC 不重复计量；没有来源则未知 |
| 每个 goal 拆解后的 DAG 目标 | goal→REQ→AC→TASK/子 TASK；work_package 记录具体目标、done_when、输入/输出、范围和停止条件；PM-001 同一任务关联两个 AC，输出目标、资产和当前分配；PM-003 未升 revision 擅改 done_when 拒绝 | 每 goal 明确工作目标表；旧台账没有完整工作包时显示缺口，不用标题假装完整拆解 |
| 缺失、失败与边界 | PM-002 缺身份告警、估算不作实测、过期剩余 null、超支 -1、goal 超额分配；PM-003 负数/bool/NaN 上限、跨 goal task、双活跃 implementation、原地改执行者、无新决策改预算、改旧用量/累计回退均拒绝且 ledger 字节不变 | 缺失和越界保持可观察，不给不完整数据放行 |
| 原有目标/证据规则不退化 | 原作者三场景保留全部旧断言；独立作者的旧 probe 重放通过祖先阻塞、依赖影响、内容/revision 过期、索引、原文/身份不变、查询只读和幂等 | 兼容回归通过；不是新版本独立验收 |

完整字段约定见 [工作包、分配与预算](../../skills/engineering/eng-project-manager/references/assignments-and-budgets.md)。只有一次明确接入/刷新改变本地台账；查询、DAG、brief 不回写业务文件、原生 goal、会话状态或实际预算。

## 三次有界验证调用

2026-08-31 在上述 worktree 执行一次验收，共三次顶层验证调用。第二次包含两条格式检查，第三次含兼容 probe 与合成展示生成；没有失败重跑、定向修正轮次或其他 skills 行为回归。完整 stdout/stderr 已保存为 [实际输出](outputs.md)。

第一次：

```sh
python3 skills/engineering/eng-project-manager/tests/test_pm.py
```

exit 0，3 tests，1.061s，OK。每个既有场景增加本次管理断言，没有把标题/关键词存在当行为通过。测试真实执行临时文件读写、init/query/refresh、分配转交及非法刷新拒绝。

第二次：

```sh
python3 scripts/validate_skills.py --check-discovery
python3 /Users/jiajun.lai/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/engineering/eng-project-manager
```

exit 0。前者 pass，skills_checked=10、cases_defined=30、behavior_cases_executed=0、errors=[]；后者 Skill is valid!。30 是定义数，不是执行了全仓 30 个用例。未安装依赖。

第三次的兼容检查：

```sh
python3 reports/eng-project-manager/independent_probe.py skills/engineering/eng-project-manager/scripts/pm.py
```

exit 0，3 tests，0.044s，OK。测试源由此前父任务独立编写且本次未改；本次由实现者执行，所以只能称兼容重放，不能称新功能独立评审。

同次调用的展示生成通过 importlib 读取 tests/test_pm.py 的 managed_fixture，在新的 .runs/PM-SKILL-002/example/fixture-project/ 创建合成文件，序列化 snapshot 后实际 subprocess 调用：

```sh
python3 skills/engineering/eng-project-manager/scripts/pm.py init --snapshot .runs/PM-SKILL-002/example/snapshot.json --state .runs/PM-SKILL-002/example/ledger.json --event-id fixture-intake-001 --reason 'Synthetic example for assignment and budget display'
python3 skills/engineering/eng-project-manager/scripts/pm.py query --state .runs/PM-SKILL-002/example/ledger.json --at '2026-08-31T04:00:00+00:00'
python3 skills/engineering/eng-project-manager/scripts/pm.py brief --state .runs/PM-SKILL-002/example/ledger.json --at '2026-08-31T04:00:00+00:00'
python3 skills/engineering/eng-project-manager/scripts/pm.py dag --state .runs/PM-SKILL-002/example/ledger.json --at '2026-08-31T04:00:00+00:00'
```

四条子进程均 exit 0。实际调用使用同位置的绝对路径。命令供查阅；如需重新生成输入，先在新的目录调用 managed_fixture，不覆盖已有台账。这里的 as_of 是固定历史回放时点，非实时数据。结果 goal_status=incomplete，current_used=200 tokens，remaining_to_goal_limit=800，unallocated=0；未把有分配/文件/预算当作目标完成。原始 query/ledger/brief/dag 留在被忽略的 .runs，精选实际输出见 [展示样例](example.md)。

## 实测载荷 SHA256

下列实现、契约和用例在首轮验证后未修改；之后仅封存报告和文档入口。

| 文件 | SHA256 |
| --- | --- |
| skills/engineering/eng-project-manager/scripts/pm.py | ad3fbee160826d795bbf1d9f18e5b15f4a50a155ed047e165638aa3f8508bc3e |
| skills/engineering/eng-project-manager/tests/test_pm.py | dcc4311474d0c5da3c042e43675a877b99470d5f4fc811e5846c666e2a974e72 |
| skills/engineering/eng-project-manager/tests/cases.json | 7fcb256bf487e2686c6cffdb08646c1c90df5ef25199afa83725f95bc36e80ea |
| skills/engineering/eng-project-manager/references/assignments-and-budgets.md | 4d3e1333aee8fdbe60d97a75f29ec2d51dc85d8ed2126f5260f08148e6d4b7d4 |
| reports/eng-project-manager/independent_probe.py（旧测试源未改） | 42c488bb67758ee3dbdbf2d7f84b4a61ad5bd5e45cc910cb985ad548d787d0ef |

## 兼容、入口与待独立验收

0.1.0→0.2.0 MINOR，snapshot/ledger v1 继续读取；新增 work_package/management 为可选字段，缺省不推断分配或预算，旧文件没有被批量迁移。添加或改工作目标遵守原有 scope_decision + artifact_revision；只改分配/预算需要新的明确 management 决策来源，增加 ledger_revision，不无故使未改实现失效。

本 worktree 的相对 .agents/skills 入口可读候选；用户级 /Users/jiajun.lai/.agents/skills/eng-project-manager 仍指向主仓库已验收版本。没有把全局入口切到此候选，也没合并 main。回退采用基线之上的 revert 候选，不重写历史。

按 AGENTS.md 的“实现者不得自签最终评审”及 meta-skill-governance 的独立行为验收规则，本候选 skill.json 保持 draft。没有授权新建任务/agent，因此只留下可由既有独立审查者接手的候选，不自动派生审查任务。尚缺本次增量原始目标的独立语义审查及新场景执行；下一责任人为用户指定的独立审查者/集成人，收到独立结果后才能提升同一受测载荷。

## 未测项与限制

- 未读取真实 agent/session 的用量遥测，也未创建真实分配。所有预算和交付数字均是 fixture；脚本校验来源、时间、revision、hash，不能证实输入来源中的权限、计量或业务结果真实。实际接入需使用可用工具返回或明确来源的交接，不访问内部数据库/未公开 API。
- 不能把会话总用量同时记到多个任务。无法归属的消耗需要在交接中显式披露，不能据此声称预算总览完整。支持 tokens/minutes/commands/cost_usd，但本轮预算数值路径主要实测 tokens/minutes；未接入账单、货币换算、实时定额、自动加预算或计费服务。
- 只做有界来源新鲜度；过期时显示历史报告值并使当前已用/剩余未知。没有后台轮询。文件存在和 delivery current 均不替代 task/AC 验证。
- 没有新一轮独立模型端到端语义/路由测试、真实生产项目分配/预算接入、并发进程竞争、大 DAG 性能或故障注入。旧版的真实父目标演练保持历史状态，不改成当前结果。
- 本轮没有已知阻断失败需要修正。上述遥测、规模与并发方向仅作为有实际需求后再立项的 backlog，不扩大本次实现。
- 未创建任务/subagent/项目/独立仓库/自动化；未 push、发布、全局替换或自行合并 main。

## 本次产出索引

| 层级 | 产出 | 关联 |
| --- | --- | --- |
| 产品目标/需求 | [增量 intent](../eng-project-manager-resources-intent.md)；本页需求证据表 | PM-SKILL-002 的三项用户补充与边界 |
| 技术文档 | [工作包/分配/预算契约](../../skills/engineering/eng-project-manager/references/assignments-and-budgets.md)、[使用说明](../../skills/engineering/eng-project-manager/references/usage.md)、[pm.py](../../skills/engineering/eng-project-manager/scripts/pm.py) | 目标、分配、资产、预算记录及派生查询 |
| 需求/验收列表 | [三个 cases](../../skills/engineering/eng-project-manager/tests/cases.json)、[执行源](../../skills/engineering/eng-project-manager/tests/test_pm.py)、[实际输出](outputs.md) | 正常、缺失/失败、越界 |
| 问题列表 | 本页“待独立验收”与“未测项与限制” | 独立接受 pending；不虚构新 reviewer/session 或真实预算 |

上述源文件 owner 为本任务唯一实现者；验证证据以本页 hash 锁定 revision。展示用业务资产另见 example.md 的四层索引，不复制/搬迁真实项目产物。
