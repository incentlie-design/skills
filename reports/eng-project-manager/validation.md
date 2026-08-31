# PM-SKILL-001 候选验证与交接

本页保留候选形成时的历史状态；后续父任务完成的独立验收与当前交付结论见 [独立验收](independent-review.md)，不要把下述当时 pending 的状态视为实时查询。

已实现 eng-project-manager 0.1.0，状态保留 draft candidate。作者有限测试通过，父任务独立脚本定向复验通过；真实项目目标的全范围验收仍由父任务负责。此报告不是作者自签的最终评审。

## 身份与修改范围

- worktree：/Users/jiajun.lai/.codex/worktrees/1e05/skill-creator
- branch：codex/eng-project-manager
- base_commit：78667f7cb54adb7e5a85c8c7d3b418e7634b7786
- schema_version：1；run_id：PM-SKILL-001-validation-20260831；change_id：PM-SKILL-001；artifact_revision：1。
- 实测发生在本地未提交内容上，内容摘要为“新增 PM skill、DAG/对账/索引脚本、测试与路由登记”。精确受测内容由 [tested-payload.json](tested-payload.json) 的 SHA256 绑定；最终本地 candidate commit 由 Git 与交付消息给出，不伪造预先不存在的 commit。
- 变更仅为 skills/engineering/eng-project-manager/、相对 .agents/skills/eng-project-manager、AGENTS.md、README.md、registry.json、CHANGELOG.md 和本次 reports。公共 docs/contracts.md、其他 skills、main 均未修改。

## 七项需求的实际证据

| 原始要求 | 实现与实际执行证据 | 判定与边界 |
| --- | --- | --- |
| 1. goal 身份、原意、约束、拆解、owner/session、沿革 | SKILL 输入契约；固定身份与 goal 对象；PM-001 四次快照/事件幂等；PM-003 跨 goal、主任务、原文改写拒绝；父任务另测跨 project | 本地契约通过；原生 goal ID 不可得时明确用有来源本地 ID |
| 2. typed DAG、进度、阻塞/上下游/遗漏/偏离、证据区分 | PM-001 实跑 query/dag，TASK-002 被 TASK-001 阻塞并给 AC/owner；PM-002 环/悬空/非法方向拒绝、遗漏/未分配 owner 可见、显式祖先 blocked/fail 保留 | 结构与状态通过；语义偏离需读取原文后由 PM 核对 alignment，不伪装自动语义审计 |
| 3. 重复接入/刷新/查询、版本来源、旧证据失效、建议边界 | PM-001 真正执行 init/refresh/query；旧 revision 及变更文件 hash 标 stale；新证据恢复的仅为 simulated_complete；PM-003 冲突不覆盖、原文保留、输入命令哨兵未创建 | 脚本闭环通过；无业务代码执行、原生 goal 写入或后台调度 |
| 4. 分层索引、关联和缺失 | PM-001 四层及真实解析路径断言；PM-003 绝对/.. /symlink 逃逸拒绝；真实演练 [索引](real-index.md) 有十个 present 和一个 missing | 通过；索引不复制原产物正文，也不搬目录 |
| 5. 实际工具能力、跨会话回退、新鲜度 | 本任务实际 read_thread 读取指定父任务；最新正文为空，保留 partial；[原始来源](real-source.md) 记用户交接、主任务 ID、工具返回范围；真实演练没有调用本子会话 get_goal 充当父 goal | 通过有来源回退路径；未声称跨会话 native get_goal 或当前产品自动加载 |
| 6. repo 治理、三必需文件、相对入口及登记 | 项目结构检查：10 skills / 30 case 定义 / 0 errors；官方 quick_validate：Skill is valid!；Git diff 仅所属路径 | 通过格式和登记；30 是定义数，不是本次执行了 30 个行为 case |
| 7. 有限真实测试/演练、证据、候选 commit | 作者三个程序行为场景全部通过；父任务自建原始场景三测通过；真实演练 ledger 1→2、goal incomplete、无 fixture 证据；本报告与 payload 摘要 | 候选交接齐备；全范围独立接受尚未完成，故不自改 active 或原生 goal |

## 实际命令与结果

执行位置均为上述 worktree。三次顶层验证命令调用；第二次顺序包含项目结构和官方格式检查。没有全仓程序回归、重复全量验收或新 agent。输出日志为实跑留存。

~~~sh
python3 skills/engineering/eng-project-manager/tests/test_pm.py
~~~

exit 0，3 tests，0.624s，OK。[完整输出](behavior.txt)；数据是临时目录中的 fixture，程序执行真实。关键观察：

~~~json
{"case":"PM-001","initial_blocked_by":["TASK-001"],"all_tasks_without_AC":"incomplete","refresh_evidence":"stale","final":"simulated_complete","ledger_revisions":4,"missing_index":"missing"}
{"case":"PM-002","missing_identity":"rejected_without_write","cycle":"rejected","owner":"assign_owner","ancestor_block_and_fail":"G/REQ preserved; goal incomplete","not_run":"not_run","missing_evidence":"missing_evidence","changed_file":["stale_binding:A-CODE"]}
{"case":"PM-003","cross_goal":"rejected","unauthorized_scope":"rejected","stale_writer":"rejected","path_escape":"rejected","history_tamper":"detected","sentinel_created":false,"authorized_revision_history":2}
~~~

~~~sh
python3 scripts/validate_skills.py --check-discovery
python3 /Users/jiajun.lai/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/engineering/eng-project-manager
~~~

两项 exit 0。项目检查 [输出](structure.json)：status=pass、skills_checked=10、cases_defined=30、behavior_cases_executed=0、errors=[]。官方检查实际输出 Skill is valid!。本次运行环境能提供所需依赖，未安装额外依赖，不改写早期报告的历史限制。

~~~sh
python3 skills/engineering/eng-project-manager/tests/replay_real.py --snapshot reports/eng-project-manager/real-intake.json --output .runs/PM-SKILL-001/real
~~~

exit 0，接入→刷新→单任务查询→Mermaid→索引均真实执行。[结果摘要](real-summary.json)、[查询投影](real-query.json)、[DAG](real-dag.mmd)、[四层索引](real-index.md)。

原始输入为 [real-intake.json](real-intake.json)。产物是当前实际 worktree 文件，mode=real，不复用 fixture 的 pass。查询时间为 2026-08-31T03:42:01Z；结果 ledger_revision=2、artifact_revision=1、goal_status=incomplete、source_freshness=partial、review=7、blocked=1、evidence_count=0；全范围验收 owner 为父任务。TASK-008 的七个上游未验证，最终评审文件 missing。示例保留采样时“候选尚未提交”的理由，最终提交不会篡改这份历史快照。

完整生成 ledger、两次快照和完整 query 保留在被忽略的 .runs/PM-SKILL-001/real/，不把全部运行态复制进 skill。重放时使用新的 output 目录；已有目录拒绝覆盖。未来文件变化会重新计算 hash，输出不是静态“通过”黄金文件。

## 独立发现与有界修正

父任务 01a05360-3ad2-7211-a3b5-48d7fe3189df 在作者首轮验收前，独立构造 G→R→AC→T，发现祖先 G 显式 blocked 被汇总覆盖，仍输出 simulated_complete；该断言实际 exit 1。作者只修正祖先显式阻断/失败的汇总和整体完成判定，并覆盖同类 requirement；同时完成已经计划的 DAG 完成求值环及 subject 绑定校验。

父任务随后发来明确复验结果：自行构造临时业务项目，未读取作者 cases/工厂预期；运行 /tmp/pm-skill-review.LbQC1e/review_pm.py，3 tests / 0.047s / exit 0；覆盖依赖/owner、祖先阻塞及恢复、四层索引、查询只读、文件/revision stale、沿革幂等、缺原文/环/逃逸/混入/目标改写拒绝和无证据 done。作者没有重跑父任务脚本或代签。

独立受测 pm.py SHA256：

~~~text
58e399a57e64e56b0bf42b1da8cd39c5df720f8547d9f72aee4ee0a845a9970d
~~~

与作者本次实测载荷一致。本次只有一轮有证据的实施修正，作者一次有限验收全通过；没有后续推测性优化。

## 未测与限制

- 未对其他九个 skills 运行行为回归；只有共享清单/链接/入口结构检查。未进入集成窗口，未合并 main。
- 父任务当前 goal 正文和 native ID 未通过本会话直接工具取得。任务 active 不能当作 goal active；仅使用明确交接，不读取内部数据库。
- 未做客户端重启/自动发现 UI 测试；相对 symlink 与格式通过不代表当前会话已加载。入口依据 [官方 Build skills](https://learn.chatgpt.com/docs/build-skills)（2026-08-31 实际打开），运行时工具可用性仍以本会话 schema 为准。
- 三个程序场景与父任务三个独立合成场景，不等于所有自然语言路由均经模型端到端验证；最终父任务语义和全范围审查 pending。
- 脚本核对结构、revision、hash、来源标签与时间，不验证报告内容的业务真伪、权限声明真伪或自动评估语义偏离。alignment 必须由主 agent/PM 看原文后给有来源判断；真实 product 验收保留既定独立评审。
- 单 repo 本地台账；hash 链检测意外修改，不提供密码签名；只检查不超过 16 MiB 的普通文件；没有实测并发进程竞争、进程崩溃注入、大图性能、跨 repo 联邦或后台定期任务。
- 不执行文件中的命令；未创建任务/subagent/项目/独立 repo/自动化；未 push、发布、全局安装或自行合并 main。

内部扩展仅记录在 [问题与条件 backlog](issues.md)，不作为当前实施任务。管理交接 status=pass 仅表示候选与证据齐备，真实 goal_status 保持 incomplete，下一责任人为父任务审查者。
