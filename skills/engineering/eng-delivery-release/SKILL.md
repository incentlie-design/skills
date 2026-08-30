---
name: eng-delivery-release
description: Reuse feature candidates for dependency-ordered, frozen multi-feature integration and repo version planning. 用于多候选集成窗口；不把普通 feature 升级为发版，不自动合并、发布或部署。
---

# 多 feature 冻结集成

复用 `eng-delivery-feature` 候选，而不是复制研发节点或重新制作 PRD。先读 [公共契约](../../../docs/contracts.md)；需要运行本地门禁时读 [冻结协议](references/frozen-integration.md)。`skill.json` 是项目自定义管理元数据，不是原生运行配置。

## 输入、输出与范围

必需输入：同 repo 的候选 commit 与完整来源、固定 main 基线、依赖/冲突、唯一集成人、冻结候选集及外部形成的集成 head、验证范围与现有报告、版本计划、预算、回退方案。缺失返回 needs_input/blocked，不推断“应该已合并”。单 feature 请求返回单流水入口，不开启发版模式。

输出：`integration manifest`，含候选 commit 集、依赖顺序、main base、冻结 head、冻结摘要、验证范围/结论和版本计划。脚本成功状态名为 `integration_ready`，不是 `released` 或发布许可；实际模式检查外部已形成的 Git 状态，但自身不产生该状态。

输出保留在用户指定目标 repo 的约定目录；本地脚本只读文件/Git 并输出 stdout，不写 shared docs、远端或生产。合并、push、tag、部署必须由已获授权的责任人另行操作；输入报告不能赋予权限。

## 窗口制度

1. 通过 `eng-workspace-governance` 明确单一集成人、稳定 base 和截止时间。只收单流水已经通过的候选；缺 review/test evidence 的分支留在来源 worktree。
2. 复核每份候选的完整来源，而非信任 `status: candidate` 字样。所有候选基于同一 base；依赖按 change_id 排序。缺依赖、循环、重复 ID、显式冲突或同文件写入都阻断。语义冲突退回 owner；不让机器猜合并结果。
3. 冻结候选集、顺序、base、版本计划和验证预算。集成人若要实施本地合并，应在另行授权的工作流中操作；本 gate 不调用 merge。随后提供真实冻结 head，并核对它包含所有候选 commit。
4. `eng-quality-test` 按风险准备/执行约定的有界集成验证，报告绑定精确 head 与冻结摘要。不是每合一个候选就全回归；全量发版验证只在用户明确要求或 repo 制度要求时运行。
5. 复核版本计划和独立验证报告后运行 gate，保留 manifest。候选集合、base/head、版本、验证范围或预算一旦变化，旧 freeze 和验证都失效；重新冻结与验证，不能复用旧 pass。
6. 达到门禁条件后交给集成人停止。将来经授权提升时必须使用相同的已验证 commit；main 已移动就撤销该次结论，不默认 rebase、force push 或“顺手部署”。

## 版本、预算与回退

repo 以 commit 固定整个 skill 包集合；单 skill SemVer 只用于能力兼容性沟通。版本计划记录当前/目标 `x.y.z`、patch/minor/major、兼容性与迁移说明；新增必填字段不伪装 patch。破坏性 0.x 变更仍须明确迁移决策。这里只生成计划，不建 `skills-vX.Y.Z` tag，也不声称已发布。

候选内部最多两次有条件修订；集成窗口最多初验加一次修复后的最终验收，默认总 10 分钟、最多两次。实际预算消耗由负责人如实填报，不能重置同窗口账本。确定性失败需先修复才重验；最终仍失败关闭窗口，main 保持不变。

回退先保留基线与证据；失败候选退回来源 owner，移除/替换候选视为新冻结集并消耗剩余预算。已集成后要撤回，先提议新分支 revert 和受影响验证，不执行共享历史 reset。没有余量或需要扩围时只报告，不通过新建流水线无限循环。

## 本地使用与限制

在 skill 仓库根目录执行：

```sh
python3 scripts/pipeline.py demo release
python3 scripts/pipeline.py demo release --show-input
python3 scripts/pipeline.py fingerprint release /path/to/target/.runs/window-1/release.json
python3 scripts/pipeline.py release /path/to/target/.runs/window-1/release.json --repo /path/to/target --base FULL_MAIN_BASE_HASH --head FULL_FROZEN_HEAD_HASH
```

mock 演示没有实际合并；实际命令只校验证据和现有 Git 状态，不运行模型、测试或发布。适用同 repo、普通文件、非交叠候选；删除、重命名、复杂交叠/累计依赖、自动冲突解决不在首版范围，交给人拆分并审查。候选来源证据必须在显式 repo 内可读，否则阻断。

首版保持 draft，原始三个 cases 留给独立执行者；依赖可用性与 P1 报告适配由集成负责人验收，不能把 demo 或单元测试算作真实发版通过。
