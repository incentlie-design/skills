---
name: eng-workspace-governance
description: Organize local Git repos, worktrees, branches, projects, sessions and parallel agents for isolated exploration and reusable delivery. 用于多 agent 工作区、Git 交接与分支规范；不为每次探索创建新项目，不自动发布。
---

# 本地多 agent 工作区规范

输入：目标 repo、任务/探索目的、基线、现有 dirty state、并行写入者及文件范围。输出：工作区分配/任务交接、分支/commit、冲突与集成候选清单。只读咨询仅给方案，不执行 Git 写入。

## 概念边界

| 概念 | 责任/寿命 | 不等同于 |
| --- | --- | --- |
| project | 长期业务目标及入口，一个项目可含多个有正当边界的 repo | 每天一次实验 |
| repo | 单一版本历史、共享契约/资产的权威来源 | 每个 skill/agent 一个仓库 |
| directory | 文件系统位置，执行前需验证所属 repo/worktree | 项目或独立 Git 历史 |
| worktree | 同一 repo 的隔离检出，给一个并行 writer | 独立仓库或权限沙箱 |
| branch | 一条变更/假设的提交线 | 文件夹、agent 身份 |
| session | 有目标与上下文的一次连续工作，可复用未结束的分支 | 自动创建新项目的理由 |
| agent | 受委派的执行者，有 owner/write_scope/预算 | 长期事实来源或集成负责人替身 |

## 工作步骤

1. 读取 `pwd`、`git rev-parse --show-toplevel`、`git status --short --branch`、`git worktree list --porcelain`。确认工作目录、基线、dirty paths 和已有人负责的写入；不自动 stash/reset 他人改动。
2. 日常同一目标复用现有 project/repo。只在独立生命周期、权限或交付产品有明确要求时提议新 repo；本 skill-creator 的 skills 永不单开 repo。
3. 需要持久修改才创建分支；并行 writer 使用 linked worktree。建议 `session/YYYYMMDD/topic`、`agent/change-id/role`，集成用 `integrate/YYYYMMDD-batch`；无真实发版不建 release 分支。
4. 基线必须是明确 commit。若任务依赖 dirty 内容，先经原 owner 形成 checkpoint，或明示不可用部分并阻断；不要伪装分支已含未提交修改。
5. 派发一个可闭合子任务，声明 read_set/write_set、输入路径与 revision、AC、依赖、禁止动作、成本预算和停止条件。共享协议先冻结；重叠 writer 串行。不同端口、缓存、临时目录和测试数据也必须隔离。
6. 核心资产放 repo 的公共目录（例如 docs/contracts、templates、src/shared），skill 条件引用；不在每条分支复制一套“最终版”。跨任务发现仅通过简短 handoff/ADR 回收，不能把整个聊天当新 agent 的必读上下文。
7. 验证按 repo 风险规则：局部 unit/feature + smoke；跨边界验证在明确候选或集成点进行。非发版不自动全回归。
8. 只暂存所属文件并提交；交接 base/head、scope、AC、证据、依赖、已知限制。由一个集成人收齐候选、按依赖合并，冻结 head 后验证，通过才 fast-forward 稳定基线。

具体操作/清单见 [本地协作手册](references/workspaces.md)，仅在实际分配或集成时读取。跨 skill handoff 采用 [公共契约](../../../docs/contracts.md)。

## 停止与安全

探索允许保留、不合入；阻断分支不能因“流程完整”而提升。commit 交接后不改写历史。Git worktree 不隔离秘密、网络或用户权限；工具授权仍独立约束。默认不 push、发布、删分支或删除 worktree。清理须明确目标且确认 dirty/未合入内容并获授权；不 `reset --hard`、不强制覆盖。

常规任务只建必要 writer 数；一个人串行的紧密探索可以复用同一 session。达到候选条件就停止，不自动启动后续发布或更多 agent。
