# 导演学习技能候选交接

- schema_version: 1
- run_id: 2026-08-31-director-validation
- change_id: skill-system-director
- task_id: TASK-DIRECTOR-001
- repo: .（已分配的 director linked worktree）
- branch: agent/skill-system/director
- base_commit: a9b20de16e8e1603606f09db3a940186a15e1708
- artifact_revision: uncommitted（验证记录写入时）；最终 commit 见提交交接。
- content_summary: 一个 0.1.0 active 技能、原始 3 个行为 case、维护规则、5 张种子卡、模板、索引与真实来源记录。
- write_scope: skills/content/content-video-director-learning/；knowledge/video-director/
- dependencies: []（与该基线 registry 一致）
- next_owner: 主协调者；共享 README/registry/AGENTS/CHANGELOG/backlog 与集成由其维护。

## 验收范围

- AC-001：入口包含触发/不触发、输入输出、权限、预算和停止条件。
- AC-002：4–6 张真实来源方法卡；每卡区分出处支持与原创归纳，含场景、步骤、练习、检查点、tags、版权/更新。
- AC-003：支持后续有界刷新、去重与冲突处理；索引和模板可复用；只有本地摘要，无原媒体和自动发布。
- AC-004：恰好 3 个原始行为 case，结构与链接做定向 smoke，不冒充盲测结果。
- AC-005：只显式暂存并提交 write_scope，无公共文件改动、无新 repo、无全局安装和 push。

## 实际验证与限制

| 项目 | 状态 | 证据 / 边界 |
| --- | --- | --- |
| 来源采集 | pass（人工） | 2026-08-31 已打开 5 个不同来源页面；4 份正文用于 5 张卡，ARRI 读取失败未采用；见知识库运行记录。 |
| Python 环境预检 | pass（检查执行成功） | `python3` 实际指向 `/usr/local/opt/python@3.14/bin/python3.14`；`importlib.util.find_spec("yaml")` 返回不存在。 |
| 官方 quick_validate | not_run | 官方脚本顶层依赖 `import yaml`，当前 Python 缺 PyYAML；未启动该脚本，未安装依赖。不能称官方校验通过。 |
| 无依赖定向结构 smoke | pass | 主协调者 build worktree 的 `scripts/validate_skills.py --root <director-worktree> --skill content-video-director-learning`，exit 0；skills_checked=1，cases_defined=3，behavior_cases_executed=0，errors=[]。 |
| 知识库与范围 smoke | pass | 一次 Python 标准库定向检查，exit 0；8 个知识库 Markdown 的本地链接、5 张卡的必填字段/日期/索引关联、恰好 3 cases、13 个变更文件均在 write_scope；行为执行仍为 0。 |
| DIRECTOR-001/002/003 | not_run | 仅定义，不执行或改写原始 prompt；留给后续独立执行者盲测。 |
| 拍摄练习与营销实验 | not_run | 只设计练习；没有拍摄、投放、观看原视频或验证效果。 |
| 客户端发现/全局安装/全仓回归 | not_run | 不在本委派范围。metadata active 是登记状态，不代表独立评审已通过或已发布。 |

定向验证绑定：验证器 SHA-256 为 `2d6136350134dd68c1a6909b9bddec1cfd15eab31446937900bc951c3f723506`。12 个交付内容文件（排除本自述记录）的摘要为 `6f56c1ea17b970dcfb626c776da8a8b1e63e238b076dabae379ff5b31b6afd32`；算法为按 repo 相对路径排序，依次拼接 UTF-8 路径、NUL、文件字节、NUL 后 SHA-256。三个原始 prompt 按 case 顺序用换行连接的 SHA-256 为 `752e4c132389888e71c13090048226653c4913f441ffd47197a5f672efe8c691`，未为盲测改写。

只做一次自查；未发现需要修改卡正文或 case 的结构问题。来源事实核对是实现者自查，不替代独立评审。最终补写本报告的实测结果，不据此重跑全仓或扩展案例。

## 交接与 backlog 建议

实现者仅自查，不自签最终评审。保持原始 3 个 case prompt；盲测执行者只取 prompt、技能和必要原始 fixture，不先看 expect/本实现者结论。候选尚未集成到 main，不 push。

后续按需处理：主协调者同步共享变更记录并对冻结候选盲测；有实际灯光问题时再补可访问的 ARRI 教学正文；收到真实拍摄反馈后再判断是否要修订练习。没有授权前不安装 PyYAML、不自动刷新、不扩充全网案例。回退由主协调者对确切候选 commit 使用 revert，不改写共享历史。
