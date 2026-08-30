# Skill 系统首版验收报告

## 结论与验收范围

9 个 `0.1.0` 本地初版 skills 已完成分类登记、外部契约、用例和必要资源。27 个原始行为场景已逐个实际演练；发现的问题已作有界修正，另有 1 条 revision 契约定向复验。最终整包结构检查通过，**22 项程序测试通过**。

这里的通过针对 skill 的路由、产物、输入不足/失败/权限停止和本地 gate 逻辑；不表示已经完成真实业务应用的端到端开发、真实多候选集成、投放效果验证或远端发布。风险级别为本地文档/规范及小型只读工具（L0/L1），没有生产操作。

首版承诺：可维护的技能包、明确输入输出与责任、可用示例、有实际运行的本地门禁、有限的证据和停止条件。不是 ADK 原生应用、无人值守研发平台或自动爬全网服务。

## 分工与仓库

所有源文件共用当前 skill-creator repo；没有按 skill 建仓库，没有新增 App 项目。主协调者先完成 meta/Git 基础规范，再将公共契约交给四个实现 subagent，并在一个独立集成 worktree 按候选收集。

| 候选 | 作者分支 | 已集成提交 |
| --- | --- | --- |
| 管理、命名、目录、公共契约、Git/worktree 基础 | session/20260830/skill-governance | efa8de8 |
| OpenSpec PRD 与产品评审 | agent/skill-system/product | 374d286 |
| 增量测试与技术评审 | agent/skill-system/quality | f65cc21 |
| 导演 skill 与 5 张来源卡 | agent/skill-system/director | 5ba02fd |
| 单/多 feature gate 与对应 skills | agent/skill-system/pipeline | 41fce1f |

集成分支：`integrate/20260831-initial`。linked worktree 保留为可恢复检查点，未删除或重写历史。业务规范中的个人效率类已保留分类，但没有虚构第 10 个 skill。临时行为测试产物不进入登记清单。

## 可重放程序验证

最终受测提交：`6acb62fd68f4f09b8265de0e95de303e327a0d68`。执行目录为本 repo 的 integration worktree。

| 检查 | 实际结果 |
| --- | --- |
| `python3 scripts/validate_skills.py --check-discovery` | pass；9 skills、27 cases 定义、0 errors；该工具明确报告自己执行的行为 cases 为 0 |
| `python3 -m unittest discover -s tests` | 22 tests，1.082 秒，OK；7 个管理验证器测试 + 15 个 gate 测试 |
| `git diff --check` | pass |

程序测试包含命名/依赖/路径边界、revision 类型、九节点成功/缺失/未知状态、独立 reviewer、stale 内容/上游引用、AC 覆盖、有限重试、候选依赖拓扑/环/冲突、冻结状态失效、版本与预算、mock 拒绝、只读 Git 核验以及不执行输入命令/不发布。新增结构化建议兼容测试会确认 value/cost/tradeoff 原样保留，缺 suggestion 的对象被拒绝。

第一轮冻结检查在 `46c037a`：整包结构 pass、当时的 20 个测试在 1.386 秒通过。随后只补了两个已观察到的外部契约问题及证据，最终第二轮为上述 22 个测试；没有第三轮整包程序回归，也没有无限原样重跑。

### 结案文档与验证结果绑定

本报告及 README 的验收导航是在测试完成后追加的文档。为避免结果文件自引用 commit，不将旧测试冒称运行在文档新增前不存在的 commit 上：22 项程序结果绑定上面的真实受测提交。

已受测载荷由以下 Git 路径对象组成：`skills scripts tests knowledge examples docs registry.json .agents AGENTS.md`。命令 `git ls-tree HEAD skills scripts tests knowledge examples docs registry.json .agents AGENTS.md | shasum -a 256` 在受测提交得到：

`c809e829b6bae278b5df4d674b4f7e08f6e17bcb60bc58ac511dcd074e1043ab`

提升前要求结案 diff 仅为 `README.md` 与本报告，复核载荷摘要不变、链接/登记和 diff 格式。仅复用未改变程序/skill/契约的测试证据，不为报告追加再跑全套回归。最终提升采用本地 fast-forward，不重新制造未经检查的 merge commit。

## 独立行为证据

五名独立执行 subagent 与作者分离；只给原始 prompt/fixture、入口及必要原始资料，不给 expect 或作者答案。主协调者查看实际输出后判定，不由作者自签。详细记录：

| 组 | 原始场景数 | 记录 |
| --- | ---: | --- |
| meta + 工作区 | 6 | [基础行为与初次歧义](behavior-foundations.md) |
| PRD + 产品评审 | 6 | [产品产物、闭环与不触发](behavior-product.md) |
| 测试 + 技术评审 | 6 | [真实状态分类与有界评审](behavior-quality.md) |
| 单 + 多 feature | 6 | [CLI 响应、路由、P1 局部投影](behavior-pipeline.md) |
| 导演学习 | 3 | [来源复核、去重、缺口、注入/限流](behavior-director.md) |

计数为 27 个原始案例 + 1 个治理定向复验；不是 28 次真实业务运行。自然语言决策、合成 fixture、真实 CLI 及真实网页读取在报告内分别标明。暂未采用无人监督的模型打分器或大规模 benchmark。

## 发现、修正与停止

1. 公共契约未明确 revision 类型，独立临时 handoff 将其写成 uncommitted。已统一正整数、分离 commit 状态、对齐各作者示例，独立 GOV-RECHECK 正确返回 revision=1/output_commit=uncommitted，并补验证器测试。
2. 产品评审的结构化非阻断建议进入 gate 会返回 `review suggestions: invalid value`。已接受带 suggestion 的对象、完整保留成本/取舍，并补程序测试；没有将建议自动升级为实施任务。
3. 产品作者首次发现示例本地链接问题，在其有界自查中修复；原失败记录保留于该 skill 的 references/validation.md，没有擦除历史。

以上均为观察驱动的定向修正。无已知范围内阻断未处理；内部扩展、真实业务连接、复杂 Git diff、签名/持久化和灯光方法缺口进入 [backlog](../docs/backlog.md)，不继续优化。

## 未执行与已知限制

- 官方 quick_validate：尝试时 Python 缺 PyYAML，未得到官方验证通过结果；未安装依赖。项目检查器是明确受限的标准库检查，不等价于完整 YAML/官方验证。
- OpenSpec CLI：本机无 CLI，未安装、未 init/apply/sync/archive；采用已核对官方来源的手工文件工作流，不能声称上游 CLI strict 验证通过。
- Codex 客户端自动加载：配置了 9 个 repo-scoped 相对 symlink 并检查目标，未做客户端重启或 UI 自动发现测试；需要时显式提供 SKILL.md 路径。
- 真实业务研发/集成：gate 演示、字段投影与自测不替代实际应用、独立签字、测试环境或真实集成；ADK/model handler、自动 merge/发布未实现。
- gate 首版只处理受支持的有限普通文件、同 base 非交叠候选；删除、重命名、复杂累计依赖走人工拆分审查。
- 导演库：5 张卡来源于 4 份实际正文，ARRI 读取失败未生成灯光卡。独立复核重新读取 3 个来源，所有练习均未实拍，无效果保证、无全文/视频下载。
- 没有 remote/push、正式 tag、部署、外部工单写入、全局安装或自动化；本地版本是初版能力包而非已发布产品。
