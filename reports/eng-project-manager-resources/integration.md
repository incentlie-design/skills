# eng-project-manager 0.2.0 本地集成与 Codex 入口

用户在本专属任务要求“合并了吗？注册到codex上”。本次由本任务负责唯一集成写入，复用此前父任务的独立只读评审职责；没有新建任务或 subagent。独立评审 pass、无阻断发现，冻结集成检查通过；0.2.0 标为 active，按授权 fast-forward 提升本地 main 并复用已有 Codex 入口，不 push。

## 冻结范围

- 稳定基线：cfe624f79152cb4680b1ab70db615b6278c62285。
- 作者候选：3c502bb7720d002842ee0b4ecd803c7f5464a281，原分支 codex/eng-project-manager-resources 保留。
- 集成分支：codex/integrate/eng-project-manager-020，在既有 /Users/jiajun.lai/.codex/worktrees/1e05/skill-creator 工作树串行操作。
- 合并与受测 head：8d2b607aaeef9cc0cda30c53e9d590065dfa7c20。候选与当前 main 只有 README/CHANGELOG 文档冲突，保留 main 的 24 个 Skill 清单及相关历史，更新项目经理说明；运行代码/契约/用例未改变。
- 相对稳定基线，仅本 Skill、README、CHANGELOG 和本次 reports 有改动；registry、AGENTS、公共契约、其他 23 个 Skill 及发现链接不改。

## 实际集成验证

三条检查在同一冻结 head 顺序执行，没有应用全量或发版回归：

1. python3 skills/engineering/eng-project-manager/tests/test_pm.py：exit 0，3 tests，1.112s。
2. python3 scripts/validate_skills.py --check-discovery：exit 0，24 skills / 72 定义 case / 0 errors。该结构检查实际执行行为 case 数为 0，不能算作 72 个行为通过。
3. 官方 quick_validate.py skills/engineering/eng-project-manager：exit 0，Skill is valid!。

原始 stdout/stderr、精确命令与受测文件 hash 保存在 [integration-evidence.json](integration-evidence.json)。上一轮作者候选验证与旧版兼容重放见 [历史候选报告](validation.md)，不改写历史 pending 或 fixture 的状态。

## 独立审查

评审者为既有父任务 01a05360-3ad2-7211-a3b5-48d7fe3189df，角色与作者分离。输入是本次三项原始增量需求及冻结候选；要求其独立设计正常、缺失/失败、越界场景，不使用作者测试工厂的预期作为答案。只允许临时目录的合成测试，不写 repo、不合并 main、不更改原生 goal。

实际命令 python3 -B /tmp/pm-skill-002-review.lxfV7q/independent_acceptance.py，2026-08-31T15:35:28Z–15:35:30Z，Python 3.14.2，exit 0。三个独立场景均 pass：共享 AC/累计用量/转交归属与筛选；旧 v1 兼容及身份、估算、资产、过期缺口；七种非法刷新均 exit 2 且台账字节未改变。报告 findings=[]；一次验收，没有修复重跑。

[独立评审原文](independent/review.md)、[独立测试源](independent/independent_acceptance.py)、[19 次 CLI 原始命令及输出](independent/execution.json) 均按原文件逐字封存；拷贝前后 SHA256 相同。评审者另验证入口、脚本和三份 reference 与原候选完全一致，结论绑定相同载荷。

测试源 SHA256 为 1478c492b42d8a9984098336ab15d5298cbee8b7d21d33613d7633092cac46fe，原始执行结果 SHA256 为 d444f4019624b9bd36409a208f7e193a66c2662d0148a8ef59b18891a868e192。本次独立结论只覆盖明确的本地记录/查询能力，不冒称真实计量、自动分派或客户端 UI 已验证。

## Codex 注册范围

既有用户级入口 /Users/jiajun.lai/.agents/skills/eng-project-manager 是 symlink，目标为 /Users/jiajun.lai/Documents/workspaces/skill-creator/skills/engineering/eng-project-manager。本次实际检查入口可读，没有同名 ~/.codex/skills 副本，也没有匹配该 Skill 的禁用配置；不需要另建复制目录或改配置。main 提升后从该入口核对 skill.json=0.2.0/active 与脚本 SHA256，不能只根据合并命令宣称入口已更新。

[OpenAI 官方加载规则](https://learn.chatgpt.com/docs/build-skills)（本次实际打开）支持用户级 .agents/skills 和 symlink，变更自动检测；若客户端未显示更新可重启。这里验证文件入口和版本可达性，不伪装已运行客户端 UI 加载测试。

## 限制与回退

只做本地合并/注册，不 push、发布或创建 tag。预算仍依赖来源明确的输入，没有本次真实会话用量遥测；合成场景不能声称真实项目 goal 已完成。数据新鲜度、业务语义和源声明真伪的限制保留在原契约中。

状态封存只修改 skill.json 的 draft→active、文档和报告；入口、运行脚本、契约与用例逐文件 hash 比较均与受测 head 相同，三份独立原始记录也与来源字节一致。封存后的结构核验 exit 0（24 skills / 72 定义 case / 0 errors），未重复行为回归。最终封存 commit 以 Git 历史和交付消息为准；只提升这条已核验提交线。若需回退，在新分支对本增量形成 revert 候选，不 reset 共享 main 或删除历史。
