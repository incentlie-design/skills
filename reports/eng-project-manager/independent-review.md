# PM-SKILL-001 独立验收与产出索引

结论：`pass`。项目经理 skill 的原始需求已逐项实现和核验，可在本仓库按需接入、刷新和查询 goal。它不是常驻调度器，不替业务目标自动签字。

- reviewer / 主任务：`01a05360-3ad2-7211-a3b5-48d7fe3189df`，不是实现作者。
- 用户要求的专属任务：**工程实践-eng-project-manager**，ID `01a055de-2854-7bf3-a26f-e916849ba46a`。已用任务工具确认实际创建、执行完成并 idle。
- 实现 worktree：`/Users/jiajun.lai/.codex/worktrees/1e05/skill-creator`，分支 `codex/eng-project-manager`。
- 原始基线：`78667f7cb54adb7e5a85c8c7d3b418e7634b7786`。
- 作者候选：`58644e9fbe47a49e18c2b0d71e34a2990eb613d4`。
- 冻结集成受测 head：`c7730919e629036a09ecb091bbb1487eb7c6fda8`，分支 `integrate/20260831-pm`。
- 公共 envelope：schema_version=1，run_id=PM-SKILL-001-independent-20260831，change_id=PM-SKILL-001，artifact_revision=1，reviewed_revision=1；范围为新 skill 及必要登记、测试、验收文档。

## 原始目标核对

2026-08-31T03:45:54Z，本主任务实际调用自身 `get_goal`，返回当前 active 目标原文如下。这里没有使用子任务的 goal 冒充父任务，也没有以任务标题代替原文。

> 创建一个单独的session：
> 构建一个项目经理的角色，现在经常有很多长程运行的goal，跑着跑着就乱了。在goal后，项目经理接入，对主agent拆解的任务项，进行管理和跟踪。
> 我需要一个项目经理skill，帮我管理和查询当前goal的进展，他需要zoom out出来，结合项目原始目标，进行查询。原始目标和拆解过程，应该是一个DAG，帮助我了解卡在哪里。
> 整理当前的主要的产出文件，以及分层的结构：产品文档，技术文档，需求列表，问题列表

审查保留全部要求：不是只创建空任务、只做静态摘要，或仅把测试变绿。没有新增后台轮询、跨 repo 平台或远端管理授权。

| 用户要求 | 已检查的权威证据 | 结论 |
| --- | --- | --- |
| 单独 session、统一 repo | create_thread 返回并解析到上述实际任务 ID；list/wait 确认标题及实际 worktree；Git linked worktree、无新仓库 | 完成 |
| 项目经理在 goal 后接入、管理主 agent 拆解 | SKILL 明确接入/刷新/查询和主任务身份；init/refresh 实跑，保留原文、快照、owner/session、事件与 revision | 完成 |
| 查询当前进展、结合原始目标 zoom out | 显式工具/交接适配，来源时间及 partial/stale 可见；REQ/AC 覆盖、孤立/漏拆节点、alignment 原文审查，reported 与 verified 分开 | 完成；业务语义由 PM/独立评审实际阅读判断，不宣称脚本自动理解产品 |
| 原始目标与拆解过程构成 DAG | 机器 JSON 的 decomposes/precedes 边；展示和完成求值分别无环；Mermaid 实际输出；历史不删除旧节点或改原始 goal | 完成 |
| 知道卡在哪里 | 依赖阻塞、上游/下游、受影响 AC、下一 owner；独立复现并修正祖先显式 blocked 被覆盖的问题，goal/requirement 阻断均保留 | 完成 |
| 当前主要产出及四层结构 | index 实际检查文件存在性/hash/关联；真实演练有产品、技术、需求、问题四层，缺失明确；下表提供交付后的主仓库文件索引 | 完成；不搬迁、复制全部业务文件 |
| 测试、有界迭代、分类管理 | 每 skill 3 类自有 cases；作者 3 程序场景、另行构造的 3 独立场景、真实接入重放通过；registry/AGENTS/README/CHANGELOG 同步 | 完成；其他九个 skills 无行为变更 |

## 冻结集成实测

执行目录为 `/Users/jiajun.lai/Documents/workspaces/skill-creator/.worktrees/pm-integration`，在上述冻结 head、干净工作区中执行三条定向命令，均 exit 0：

1. `python3 skills/engineering/eng-project-manager/tests/test_pm.py`：3 tests，0.876s。正常/缺失/越界全部通过，包括真实 CLI 的 init/query/refresh/dag/index。
2. `python3 /tmp/pm-skill-review.LbQC1e/review_pm.py skills/engineering/eng-project-manager/scripts/pm.py`：3 tests，0.045s。该独立测试由父任务在未阅读作者案例/工厂预期前构造；源码原样存为 [independent_probe.py](independent_probe.py)，可用该路径替代临时路径重放。
3. `python3 skills/engineering/eng-project-manager/tests/replay_real.py --snapshot reports/eng-project-manager/real-intake.json --output /tmp/pm-skill-review.LbQC1e/real-integration`：真实业务文件、有来源的本次需求，ledger 1→2，输出四层索引、DAG 和单任务查询。`mode=real`、`goal_status=incomplete`、`source_freshness=partial`、7 review / 1 blocked、0 evidence，未借 fixture 或文件存在放行。

独立场景还直接断言：查询不改台账字节；内容变化即时使绑定 stale；revision 增加使旧证据 stale；相同事件幂等；原文缺失、循环、路径逃逸、跨 goal/project 混入和成功定义篡改均拒绝；无证据的 reported done 不计通过。

受测 `pm.py` SHA256：`58e399a57e64e56b0bf42b1da8cd39c5df720f8547d9f72aee4ee0a845a9970d`。独立测试 SHA256：`42c488bb67758ee3dbdbf2d7f84b4a61ad5bd5e45cc910cb985ad548d787d0ef`。

独立审查发现的严重问题仅一项，已定向修正并复验。冻结集成之后仅更新 active 元数据和验收/路由文档、保存独立测试源；运行脚本、入口行为、输入输出契约和原有用例不变。后续格式/登记检查不能冒充新一轮行为验证。

封存前实际检查通过：`python3 scripts/validate_skills.py --check-discovery` 返回 10 skills、30 个用例定义、0 errors（行为执行数明确为 0）；逐文件 SHA256 比对确认 8 个原受测文件中仅 skill.json 的 draft→active 改变，其他 7 个完全一致；独立测试副本摘要一致、报告链接检查及 `git diff --check` 均通过。没有因文档封存重复行为测试。

## 当前主要产出文件

| 层级 | 交付位置 | 用途 |
| --- | --- | --- |
| 产品文档 | [原始目标与需求来源](real-source.md) | 原文、完整交付要求和来源边界 |
| 技术文档 | [SKILL 入口](../../skills/engineering/eng-project-manager/SKILL.md)、[数据契约](../../skills/engineering/eng-project-manager/references/contract.md)、[使用说明](../../skills/engineering/eng-project-manager/references/usage.md) | 权限、状态与来源规则、命令及交接 |
| 技术实现 | [pm.py](../../skills/engineering/eng-project-manager/scripts/pm.py) | 台账、DAG 校验、对账、查询、索引 |
| 需求列表 | [REQ/AC/TASK 机器快照](real-intake.json)、[DAG](real-dag.mmd) | 七项委派要求与拆解关系；历史演练，不冒充实时状态 |
| 问题列表 | [问题及条件 backlog](issues.md) | 独立发现、解决记录、来源限制和未来触发条件 |
| 测试/验收 | [行为案例](../../skills/engineering/eng-project-manager/tests/cases.json)、[作者运行报告](validation.md)、本独立报告 | 可重复行为与逐项完成依据 |

历史 [查询](real-query.json)、[索引](real-index.md)、[摘要](real-summary.json) 保留采样时“未完成”的事实，不为了这次交付改写历史。它们的 repo 指向当时实际作者 worktree；上表相对路径是当前主仓库交付入口。再次查询其他 goal 需提供对应主任务和明确来源，不复用这次演练身份。

## 限制与停止

跨会话原生 goal 正文读取并非可保证能力；必要时按明确交接或导出快照接入。新鲜度和来源缺口必须显示。自然语言语义、业务报告真伪和授权真实性不能靠 hash 证明，PM 必须阅读原文/记录并保留既定独立产品与技术评审。

未测客户端自动发现 UI、后台定期跟踪、跨 repo 联合进度、并发崩溃、大图性能；本轮不建立这些能力，也不运行其他 skills 的业务回归。项目级 symlink、格式及结构验证与自动加载区分。相关后续只留有触发条件的 backlog。

本次没有远端写入、发布、全局安装、删除 worktree 或新增调度。达到验收即停止；专属任务留作后续使用和维护。
