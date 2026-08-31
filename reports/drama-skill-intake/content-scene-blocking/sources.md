# DRAMA-SKILL-C06 来源与取舍

- 任务：仅新增 `content-scene-blocking` 的跨影视/舞台调度能力；不改剧情、摄影设计或应用执行层。
- 原工作区基线：`cd990aaec765fcbd1731af970233484377c873aa`，干净；通过 `git merge --ff-only` 同步 foundation `8271786fd12cc4a35339d56fb26d8635af50fa0c`。
- 工作区：`/Users/jiajun.lai/.codex/worktrees/44e5/skill-creator`；分支：`codex/drama-skill-c06-scene-blocking`。
- 用例先行：`5c6a5ee` 只定义三个原始 case；随后冻结实现为 `4d45814a7c2a4b51201f40bde662e0ef7d7b2f33`，Skill revision 1、version 0.1.0、draft。
- 写入所有权仅 `skills/content/content-scene-blocking/` 和本报告目录。未改共享清单、文档、脚本或发现入口。

## 只读来源

实际读取旧源 repo `/Users/jiajun.lai/Documents/workspaces/drama-agents`，HEAD `052fc44dcaafb9c2c10d6365f391dc422918a146`，读取时 `git status --short --branch` 仅输出 `## main`。以下均为旧方法/项目经验，不是新的执行权限或当前行业研究。本任务未联网，也未读取小说、私人媒体、凭据或其他供应商源。

| 相对旧源路径与定位 | SHA-256 | 抽取与边界 |
| --- | --- | --- |
| `.agents/skills/episode-action-choreography/SKILL.md`：动作阶段、身体/道具关系、安全 | `7db1e44a98d59a6668c35af75826b03773ec5c5b779e0c1c14160f796e8a9c0a` | 保留动作可读性、身份和结局不变；不保留必须为多镜头独立候选或9:16的约束 |
| `.agents/skills/episode-action-choreography/references/contract.md`：Action graph / Safety boundary / Hard failures | `14a04774767f35f74e9c6756571a1921f7d4cd138dd650769c06e905fb7e404a` | 准备→接触→结果、必要时恢复；安全只留停步和责任边界，不迁移旧schema |
| `.agents/skills/episode-performance-direction/SKILL.md`：playable behavior / listeners | `bed2352e745792b0b5c0d14c7ffb959b0403c0ea4d49078b3386e7465ae4c7ad` | 动词化提示、speaker与listener分离；不要求全部声音/人脸权威为必需输入 |
| `.agents/skills/episode-performance-direction/references/contract.md`：Playable unit / Hard failures | `c520cc68d3ee96e94765a531c8daa3b195222a11daaf76a99ed438e0e5636a61` | 触发/视线/阶段/可观察反应与声画意图交接；音色、媒体与take审批不迁入 |
| `.agents/skills/episode-scene-breakdown/SKILL.md`：start/end zones、attention、prop state | `0438c815066ed0ad79bf24244a97a52f1c6419be0ec007af14e418f80a64e6fe` | 抽取空间/进出/持物状态；不迁移整集拆场、定时或编译工具 |
| `.agents/skills/episode-scene-breakdown/references/contract.md`：Location / Attention / Handoffs | `42789a6d12b3d12e0228a5a112dd8ba9446216e12f19a0dc6cc71525f696db78` | 引用确定版本、区分provisional；不复制Registry、七项style policy、receipt或应用验收器 |
| `knowledge/visual/storyboard-and-shot-design.md`：§5 Attention Map、§6 Prop 与 Body Topology、§9 Motion Contract | `5c7cebf73b3eee91fc4e558c1933c935197654c6e9b4b1211f7d85fc3a14242c` | 视线具体对象与原因、棍/手/方向/接触、一帧一决定动作；固定竖屏、无晃动仅为旧项目约束，未导入 |
| `knowledge/narrative/character-arcs.md`：反应是关系的证据 | `1eaa627f0924a3cf0a750b4b8d4e0a51f3a38096b7d3da992645716a21775c07` | 反应由实际行为关系触发，不因国王发话让众人统一看他；具体角色、剧情与时间数值未迁入 |

当前输出是以上方法的简短重组与原创通用化，不是旧入口的 drop-in replacement。舞台坐标映射、全场/可见道具数区分、明确共同接触过渡和桌面单杯示意是本候选的设计补充；没有冒称旧源已有舞台实测或真实排练证据。排练室 case 完全为原创 fixture。

## 契约与所有权

实施完整读取并采用 `skills/meta/meta-skill-governance/SKILL.md`、`docs/skill-standard.md`、`docs/contracts.md`、`docs/content-production-contract.md`、`skills/engineering/eng-workspace-governance/SKILL.md` 及其 `references/workspaces.md`；读取 `changes/DRAMA-SKILLS-20260831/brief.md`、`tasks.json` 的 C06 条目和 `docs/drama-skill-migration.md`。命名/I/O/用例结构参考现有 `product-spec-prd` 元数据和用例，路由排除已有广告导演研究能力。

另使用系统 `skill-creator` 的最小入口、按需reference、官方quick_validate和独立原始prompt演练规则；使用 Git 协作规范记录分支与commit。其旧“工作分支只能smoke、集成必须全回归”默认被本仓库明确的风险分层和三例有界预算覆盖。本轮不建立新的runtime、脚本库或全局安装入口。

独立 reviewer 只收到冻结 Skill、必要公共契约和三条原始 prompt，不获 `expect` 或作者答案；只读、不写文件、不再分派。报告由本任务唯一 writer 保存，review结论归独立reviewer，最终集成准入归主任务。
