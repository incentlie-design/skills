---
name: eng-delivery-feature
description: Deliver one scoped feature through spec, design, plan reviews, implementation and independent evidence gates. 用于实施单功能并交付 candidate；不用于只读解释、多候选集成或自动发布。
---

# 单 feature 最小流水线

把一个已授权的局部改动交给下游集成人。先读 [公共契约](../../../docs/contracts.md)；需要运行门禁或适配上游报告时读 [本地 gate 协议](references/gate-protocol.md)。仓库中的 `skill.json` 是自定义管理元数据，不是 Codex 原生配置。

## 输入、输出与权限

必需输入：原始需求、目标 repo、明确基线、目标/非目标、可观察 AC、约定写入范围、实施 owner 与独立 reviewer。缺失时返回 `needs_input/blocked`，列最小缺口；不猜需求、不伪造 reviewer 或证据。

可默认：单 feature 模式、一次初验加最多两次有证据的定向修复、不调用远端服务。缺测试环境时只做测试计划，结果写 `blocked/not_run`，不能作为 candidate。

业务输出放用户指定目标 repo 的约定路径；临时演练可放 `.runs/<run-id>/`，不回写 skill。脚本仅读取显式指定的本地 repo、JSON、产物和证据，向 stdout 输出 JSON，不写文件或 Git refs。调用者自行保存输出也不能越过写入授权。

输出给 `eng-delivery-release`：带完整来源快照的 `candidate`，包含 commit、baseline、scope、AC、review/test evidence、依赖、冲突及回滚。`candidate` 只表示可进入集成；退出码 0 不授权 push、tag、部署或发布。

## 人/agent 的节点交接

1. 通过 `product-spec-prd` 把原始输入整理为 spec/PRD，保留来源、用户旅程、REQ/AC、未知项、风险和指标；不因有原始文本就宣布 ready。
2. 写 design：目标/约束、基线与历史、替代方案、取舍、接口/数据、写入范围、回滚、REQ→设计映射。通过 `eng-quality-test` 写 AC→case→验证层级、数据环境、步骤与预算的 test-plan。委派时另按公共 tasks 契约列 owner、依赖、read/write set 和停止条件。
3. 由 `product-review-prd` 做产品评审，`eng-review-technical` 做方案评审，由独立测试计划责任人按 `eng-quality-test` 做计划评审。三项判定分别保留，不能拿技术评审代替产品判定。
4. 三项都 pass 才实施。通过 `eng-workspace-governance` 使用已分配的 worktree；仅修改约定文件，形成明确 commit。
5. 实施完成后做独立代码 review 和定向测试，两者可独立收集。实现者不能自签任何必需 review；测试记录实际结果，不能把计划中的命令当已运行。
6. 协调者收齐报告并核对修订，冻结一个完整快照，运行 gate。所有必需节点、AC 对应测试和证据都通过才得到 candidate。交接后停止，不自行启动集成或新 agent。

这是人的工作顺序，执行器只是收集后的门禁。它不会逐节点调用模型、生成代码、启动测试或自动创建 agent；并行 agent 必须另外获得授权。

## 修订、回退与停止

`artifact_revision`、节点 revision、`reviewed_revision` 从整数 `1` 开始。`uncommitted` 只可用于公共契约中的 commit 类字段；实际 candidate gate 要完整 commit hash，未提交状态会阻断。

状态只有 `pass/revise/blocked`。缺失、unknown、旧 revision、文件摘要变化、上游引用不一致、必需测试未运行，都不能 pass。`revise` 才可带失败证据、责任人和修复理由回退；`blocked` 先解决输入/权限问题，不自动重试。

单 run 最多初版加两次修订。每次回退更新 revision、保留相连快照摘要和失败证据，重新确认受影响判断。本执行器保守地绑定全部节点到同一快照，不支持凭局部影响分析自动复用旧 review。到上限仍未通过，停止交还协调者；不另建 run 绕过预算。

## 本地使用

以下命令在 skill 仓库根目录执行，仅需 Python 3.9+ 标准库；实际模式还需本地 Git。完整包必须一起携带公共 contracts、被引用的依赖 skills、共享脚本和示例，不能只复制本 skill 文件夹。

```sh
python3 scripts/pipeline.py demo feature
python3 scripts/pipeline.py demo feature --show-input
python3 scripts/pipeline.py fingerprint feature /path/to/target/.runs/run-1/feature.json
python3 scripts/pipeline.py feature /path/to/target/.runs/run-1/feature.json --repo /path/to/target --base FULL_BASE_HASH --head FULL_HEAD_HASH
python3 -m unittest discover -s tests -p test_pipeline.py
```

`demo` 明确使用 mock；`--show-input` 展示具体 JSON 结构，不能直接作为真实证据。`fingerprint` 仅计算摘要，不审核或背书。实际映射、冻结方法和限制见 [gate 协议](references/gate-protocol.md)。

当前为 draft：脚本测试不等于三个自然语言 case 已独立执行。保留原始 cases 给独立执行者；集成负责人负责依赖可用性、路由和行为验收。
