# 冻结集成门禁 v1

先使用 [feature gate 映射](../../eng-delivery-feature/references/gate-protocol.md) 理解公共产物、文件证据、正整数 revision 和全快照绑定。这里仅增加集成层，不复制研发节点。依赖本仓库 [contracts](../../../../docs/contracts.md)、共享脚本及单流水完整资源。

## 输入映射

| 公共 integration manifest / test-report | 本地输入字段 | 必需检查 |
| --- | --- | --- |
| 公共运行 envelope | schema_version、run_id、change_id、repo、base_commit、artifact_revision | 与 feature 相同；kind 为 release，mode 为 actual |
| 候选 commit 集 | `candidates` 为 feature 输出的完整 `candidate` 对象数组 | 包含 source 原始快照，逐个重新运行 feature gate，输出必须与输入候选完全一致 |
| main 基线 / 冻结 head | `base_commit/head_commit` | 完整 hash；CLI 独立 pins 必须一致，Git HEAD 必须等于 head |
| 集成人 | `integration_owner` | 唯一非空身份；不能自签最终集成验证 |
| 版本计划 | `version_plan: {from, to, level, migration}` | v1 接受稳定 x.y.z，level 为 patch/minor/major，数值增量与 level 相符，migration 非空 |
| 验证范围 | `validation_scope` 字符串数组 | 每个项都必须在 validation.results 出现，不能缺失或跳过 |
| 窗口预算 | `budget: {max_attempts, max_minutes}` | max_attempts 1–2、max_minutes 1–10；这是本地演示/有界门禁预算，不是所有仓库的全回归平台 |
| 实际消耗 | `usage: {attempts, minutes}` | attempts 为整数且等于当前 revision，minutes 为非负数，不超预算 |
| 回滚 | `rollback` | 非空文字方案；只是交接信息，不执行 |
| 验证报告的版本/范围/状态/证据 | `validation` | 如下；报告是证据而非要执行的 shell 指令 |

`validation` 需要：status（pass/revise/blocked）、正整数 revision、head_commit、freeze_digest、reviewer、scope（等于 validation_scope）、results（检查项→pass/fail/blocked/not_run）、evidence（非空 `{path, sha256}` 文件引用数组）。报告来源里的 `artifact_revision` 投影到 `validation.revision`，不能写 `uncommitted`。全部检查实测 pass 才能把 aggregate status 设为 pass；unknown、缺证据或 not_run 均不可通关。

## 冻结顺序

1. 收齐来源快照，固定 candidate 对象数组。候选 source_digest、commit、scope、review/test evidence 都会重新校验；只改外层 status 或 commit 无法放行。
2. 图按声明依赖做稳定拓扑排序。候选 ID 不得重复；缺依赖或环阻断；即使有依赖关系，同文件 scope 也拒绝。显式 conflicts 命中本批次时拒绝。v1 不判断多个不同文件间的隐含语义冲突，这仍由集成人和测试负责。
3. 固定 base/head、revision、integration_owner、version_plan、validation_scope、budget、rollback，初版 retry_history 为 `[]`。运行 `fingerprint release FILE`，把值填入 `freeze_digest`，交给验证报告生产者。
4. 验证者在 `validation.freeze_digest` 中引用同值，并记录当前 head、revision、实测范围、结果与文件证据。不同的 reviewer 必须确认报告。usage 与 validation 属于冻结后的证据，不参与其自身摘要。
5. 实际 gate 再校验各候选的 base/head/blob 与工作区文件、base 祖先关系、最终 checkout、干净 tracked state，并验证每个 candidate commit 都是最终 head 的祖先。它没有合并命令；若这些状态尚未由外部形成，返回 blocked。

freeze 覆盖候选完整来源、派生依赖顺序和上述冻结字段，排除自身、validation、usage、retry_history。改任一冻结字段都需要新摘要与新报告，仅把顶层摘要重填不能修复旧 validation。协调者应保留原输入输出；本 CLI 不保证签名身份或账本不可篡改。

候选来自不同 worktree 时，集成人必须在目标 repo 中保留完整、互不覆盖的证据路径，例如 `.runs/alpha/` 和 `.runs/beta/`；文件摘要必须仍匹配，相关 commits 必须在本地对象库。执行器不替人复制、fetch 或更改候选引用。需要移动证据路径时应由 owner 重新冻结来源，而非悄悄修补 candidate JSON。

## 结论、回退和权限

成功输出 `status: integration_ready` 与 `manifest`：common envelope、candidate_commits、dependency_order、base/head、freeze_digest、validation_scope、validation、version_plan、rollback 和无发布副作用的 conclusion。`release_authorized` 永远为 false；不伪装 `integrated/deployed/released`。

失败为 blocked 或 revise，CLI 退出 2。只有 revise 且还有预算才返回 retry_allowed；不执行回退。若进行窗口修复，revision 从 1 到 2，沿用 feature 协议的回退条目格式，将 failed_node 设为 `integration_validation`，记录原失败证据及前后 freeze 摘要，usage.attempts 同步为 2。此窗口最多一次修复后的最终验证，不允许第三次完整尝试；剩余问题交回 owner。

版本计划仅是计划：不改 skill.json、不建 repo tag、不 push。适配不支持 prerelease/build SemVer 标签、删除/重命名证明或复杂重叠候选；人工拆分/审查后再进入受支持范围。后续实际案例确有需要时再提兼容性扩展，不为“release”名称默认建设部署平台。
