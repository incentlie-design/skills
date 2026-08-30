# 基础 skills 独立行为记录

日期：2026-08-31。执行者：独立 subagent Bohr（`01a0536a-49d3-7431-9e63-efe46a6f2fe3`），不是两个 skill 的作者。仅得到原始场景、skill 入口与最小源资料，未读既有 `tests/cases.json` 的 expect 或作者验收结论。主协调者查看实际输出后判定；本报告不是逐字聊天转录。

执行方式：真实源 repo 只读，需要产物时写临时目录 `/tmp/skill-forward-test.cQgCNr`。没有模拟真实 Git 写入/安装/远端操作已经发生。基线 skills 内容来自 `5e1da80`，后续公共契约澄清见下文。

| Case | 实際可观察结果 | 判定 |
| --- | --- | --- |
| META-001 | 生成 `personal-meeting-actions` 草稿目录、SKILL.md、skill.json、3 个案例及公共索引合并文案；只用粘贴笔记生成本地待办，未连接账号、未创建 repo、未改真实 registry。owner 未提供，维持 draft | 主要行为断言满足；额外 handoff 检查发现 revision 歧义，见下文 |
| META-002 | 明确新增必填账号 ID 是破坏性输入变更，拒绝记作 patch；请求旧 skill/版本/契约，停在 needs_input，没有假造迁移成功 | pass |
| META-003 | 对附加笔记“周五前小陈补充API文档”直接返回待办，保留相对期限；不进入 skill 开发，不创建提醒或写文件 | pass |
| WS-001 | 产出两个 writer、两个 linked worktree 的方案；API A/B 串行分支探索，文档独立写入；共享 schema 单 owner，统一集成人只选择一个 API 实现。真实业务基线未给，明确 draft，不真的创建 | pass |
| WS-002 | 指出 main 的新分支不会携带同事未提交 schema；要求原 owner checkpoint 或暂停。只读实查没有该 schema，明确场景假设并未被证实，不 stash/reset/代提交 | pass |
| WS-003 | 解释 repo 与 worktree 共享历史、分别检出；明确不是权限沙箱；未执行文件或 Git 操作 | pass |

主协调者实际检查了临时 `META-001/candidate/skills/personal/personal-meeting-actions/SKILL.md`、`META-001/DELIVERY.md` 和 `WS-001/WORKSPACE-AND-HANDOFF.md`。临时草稿不是本项目新增的第 10 个 skill，也不算已集成能力；长期登记仍为 9 个。

## 有证据的定向修正

META-001 和 WS-001 的临时 handoff 将 `artifact_revision` 写成 `uncommitted`。原公共契约仅列字段、没有明确 revision 的类型，无法保证流水线一致消费。协调者在 `efa8de8` 收紧 `docs/contracts.md`：revision 是从 1 开始的正整数；未提交状态只用于 commit 类字段。同步通知所有作者，导演采集记录也按此修正。

这是一轮契约修正，不改原始场景，不对其他已通过行为反复测试。另交独立执行者一个首次未提交草稿 handoff 题做定向复验，结果计入最终验收报告。原始有歧义输出保留为失败证据，不改写临时记录成“初次全部通过”。

## 限制

META-001 中新生成 skill 的 3 个用例仅为被测 meta skill 的产物，没有继续递归执行这些新用例。此次验收不证明真实 App 自动加载、其他业务 repo 集成、第三方账号联通或任意长对话下都能稳定路由。
