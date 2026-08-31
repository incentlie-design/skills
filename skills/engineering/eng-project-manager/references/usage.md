# 接入、刷新、查询

以下从目标项目根目录运行。PM 指向本 skill 中真实的 pm.py；不安装全局命令。先按 [契约](contract.md) 准备 snapshot.json，台账父目录需已存在且属于本次允许写入范围。复制的示例是 fixture，切勿改标签冒充真实运行。

~~~sh
python3 "$PM" validate --snapshot .pm/goal-a/snapshot.json
python3 "$PM" init --snapshot .pm/goal-a/snapshot.json --state .pm/goal-a/ledger.json --event-id intake-001 --reason '接入主 agent 交接 r1'
python3 "$PM" query --state .pm/goal-a/ledger.json
python3 "$PM" query --state .pm/goal-a/ledger.json --node TASK-002
python3 "$PM" query --state .pm/goal-a/ledger.json --agent agent-api
python3 "$PM" query --state .pm/goal-a/ledger.json --session session-api
python3 "$PM" query --state .pm/goal-a/ledger.json --agent agent-api --session session-api
python3 "$PM" brief --state .pm/goal-a/ledger.json
python3 "$PM" dag --state .pm/goal-a/ledger.json
python3 "$PM" index --state .pm/goal-a/ledger.json
python3 "$PM" refresh --snapshot .pm/goal-a/snapshot-r2.json --state .pm/goal-a/ledger.json --expected-revision 1 --event-id handoff-002 --reason '主 agent 更改实现，旧证据失效'
~~~

query 同时给总体和 focus。看 focus.blocked_by 定位直接障碍；upstream/downstream 是依赖链，ancestors/descendants 是目标分解链，affected_acceptance 是连带影响。沿 blocked_by 找到可行动根因，再根据 next_actions 的 owner/session 交给主 agent，不凭空估算工期或通知别人。需要原始历史时读取 ledger.history；每次 query 的派生状态不会改写历史。

0.2.0 的 query 还给 goal_dag（原目标、REQ/AC、工作包目标/完成条件/产出/分配）和 management（分配明细、by_agent、by_session、goal_budget、缺口和告警）。--agent/--session 使用准确 ID 过滤，结果在 assignment_focus；两个参数同时使用时取交集。--node 的 focus.work_package 含该任务及子任务的去重分配/预算，未知节点仍拒绝，未知执行者返回 not_recorded，不捏造身份。

brief 是上述信息的 Markdown 简报：DAG 工作目标表、任务/agent/session 与交付资产、预算、四层索引。它不是后台自动刷新页面。dag 的任务标签在记录存在时附具体工作目标和当前执行者，不把历史分配误认为仍在运行。

例如 TASK-001 未验证、TASK-002 依赖它，结果中 TASK-002.status=blocked，即使主 agent 报 done 也不放行。TASK-001 的文件变更后旧 pass 的 problems 含 stale_binding；若主 agent 升 artifact_revision，旧证据还会含 stale_revision。只有同版的新报告、完整绑定及 AC 验证齐备才能恢复。所有 task done 但 AC 没有证据时，goal_status=incomplete。

可重放的三个真实程序行为场景：

~~~sh
python3 skills/engineering/eng-project-manager/tests/test_pm.py
~~~

这条命令用临时目录生成合成项目，真实运行 init/query/refresh 与断言，打印观察输出并退出；不会创建后台服务。它验证脚本行为，不替代独立 agent 对 SKILL 路由与语义判断的审查。

三个原场景保留旧版断言，并扩展分配/预算：两位 agent 消耗 160 和 40 tokens，goal 累计 200，不能把早先累计 100 再加一次；共享两个 AC 也不能重复收费。移交给新 agent 后，旧 agent 仍记 160，新 agent 有明确零用量记录才显示 0；文件存在不自动算新 agent 已交付。完整可执行样例由 tests/test_pm.py 的 managed_fixture 生成，所有数值为 fixture，不是本会话实际用量。

## 返回给主 agent

使用公共 envelope，再给一段有依据的管理交接，例如：

~~~json
{
  "schema_version": 1,
  "run_id": "pm-query-003",
  "change_id": "goal-a",
  "repo": "/absolute/target-repo",
  "base_commit": "uncommitted",
  "content_summary": "主 agent r2 已修改实现，验收尚未复核",
  "artifact_revision": 2,
  "status": "blocked",
  "ledger_revision": 3,
  "artifacts": [".pm/goal-a/ledger.json"],
  "evidence": ["source-handoff-002", "EV-001: stale_revision"],
  "unresolved": ["AC-001 缺 r2 验证"],
  "next_owner": "main-agent"
}
~~~

以上为格式示例，路径与身份必须替换为真实值；不能把该示例的 blocked 套到实际任务。推荐先说明原始目标、未闭合 AC、根因和恢复所需输入，再附索引和图。

发现入口依照 [官方 Build skills](https://learn.chatgpt.com/docs/build-skills)（2026-08-31 实际打开）。本 repo 使用相对 .agents/skills symlink；文件存在和结构通过并不证明当前客户端已自动加载。工具能力说明以本次实际 tool schema 为证，文档不承诺跨会话原生 goal 访问。
