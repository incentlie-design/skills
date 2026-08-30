# 分配、同步与交接

下面是模板，不应盲目执行尖括号参数。`git worktree add` 只在确认目标路径不存在、分支名未占用后执行。`git worktree list` 检查哪个分支已被检出。

```sh
git worktree add .worktrees/feature-a -b agent/change-a/implementation <base-commit>
git -C .worktrees/feature-a status --short --branch
```

所有 worktree 指向同一 common git dir；禁止在 worktree 内 git init。`.worktrees/` 在主仓库 ignore，防止把另一检出提交成嵌套仓库；也可采用用户指定的统一外部 worktrees 根目录。单个 repo 不要求新建 App project 才能使用 worktree。

任务 handoff 至少写：`task_id, purpose, base_commit, worktree, branch, owner, read_set, write_scope, inputs, outputs, acceptance, depends_on, validation_budget, stop_conditions`。例如产品 agent 只写 `changes/C1/prd.md`，实现 agent 读已冻结 PRD，仅写指定 src/tests；schema 和注册表由协调者单写。

未共享私有分支可按用户/项目约定 rebase；一旦交接 commit 或作为依赖，后续用新 commit/merge。依赖新基线才同步，避免每次对话都 rebase。强耦合同文件任务改串行，而非用冲突解决掩盖共享写入。

候选集成默认依赖顺序 merge，保留提交责任；选取少量明确提交才 cherry-pick，记录来源。冲突是业务语义时退回 owner。冻结候选列表、base 和 head；验证与 head 绑定。若 main 变化或增加候选，旧结果 stale，需新预算内定向验证；预算不足保留候选不提升。

本 repo 的轻量技能集成只需结构/路由/受影响脚本和有限行为演练，不要求所有应用的 release regression。多功能真实交付读 `eng-delivery-release`，测试层级读 `eng-quality-test`。不在每个 agent 合入后跑完整回归。

结束记录 `done/candidate/blocked/abandoned`；有用探索保存简短决策与复用资产位置。无授权不删除任何 worktree；保留分支并说明清理建议。
