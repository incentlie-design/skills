# 流水线 skills 独立行为记录

日期：2026-08-31。独立执行者 Feynman（`01a05373-27d8-7960-8880-3db56fd721ed`），未读 cases expect、单元测试源码或作者结论。源 repo 只读，产物写 `/tmp/eng-forward-test.fIUd4M`。只执行三条门禁 CLI，没有执行业务实现、测试命令、Git 写或远端动作。

| Case | 实际结果 | 断言判定 |
| --- | --- | --- |
| FEATURE-001 | demo feature 退出 0，完整九节点检查输出 mock candidate；同一 mock 输入送实际 gate 退出 2，原因 `mock/unknown mode cannot enter actual gates`。缺真实业务输入/评审/测试时不声称完成实际 feature | pass，限 fixture 门禁与正确拒绝实际放行 |
| FEATURE-002 | skill 决策 blocked，revision 1 review 对 revision 2 stale，缺当前 test-report；不先标 candidate、不伪造重试链 | pass，决策执行而非该案 CLI 测试 |
| FEATURE-003 | 路由只读算法解释，缺算法内容返回 needs_input；不启动 feature 实施或执行附件 curl | pass |
| RELEASE-001 | 独立 demo release 退出 0，mock integration_ready，alpha→beta，0.1.0→0.2.0/minor，冻结摘要绑定候选与验证范围；真实窗口材料缺失，保持 blocked | pass，限 fixture 集成与权限边界 |
| RELEASE-002 | 分别拒绝未提交依赖、循环、同文件冲突；替换 commit 后旧 freeze/report 失效，退回 owner、保留预算账本 | pass，skill 决策；相应 CLI 分支由程序单元测试覆盖 |
| RELEASE-003 | 普通修复回单 feature 入口，不因 mock 通过而组织发版、push/tag/deploy | pass |

三条实际命令：`python3 -B scripts/pipeline.py demo feature`；`feature <临时mock-source.json> --repo <源repo> --base <mock-a> --head <mock-b>`；`demo release`。退出码依次 0、2、0。第二条在 mode 检查即停止，不能宣称由这一条命令验证了真实 Git、所有 review 或实际业务 AC。

副作用观察：执行者的 HEAD、refs、索引与原有文件摘要不变，所有自身产物在临时目录。它同时观察到协调者新增 `behavior-director.md` 和 `behavior-quality.md`，如实记录外部并行变化，而非声称整个工作区完全未变；这两个报告由主协调者有意写入，不是 gate 副作用。

## P1 交接的实际投影

独立执行者读取原 PRD/handoff/spec 与质量模板，生成 `P1-mapping.json`：

- 保留 artifact_revision=1、base_commit=uncommitted；规划 pass 不变成业务门禁 pass。
- 实際计算 PRD 文件 SHA-256：`7dc0e29ad53353c1a16f30db02269635b52706bf1fd961b397d137d288388b73`，连同相对路径投影到 `nodes.spec.artifacts`。
- AC-001 的 criterion 为：t1/t3=open、t2=done，依次选择 open/done/all 时显示相应 id，保持源数据和顺序。
- test-report 仅形成 `not_run`、空 evidence 和缺 scope 的诊断片段，不编造已执行记录，也不把规划目录当实施 scope。这不是完整 gate-ready 输入。

主协调者另外将产品独立评审实际使用的结构化建议（suggestion/value/cost/tradeoff）投影到有效 mock 节点。初次实际返回 `blocked: review suggestions: invalid value`，发现 P1 合法输出与 gate 只收字符串不兼容。已作有界修正：接受非空字符串或带 `suggestion` 的对象，保留所有取舍字段并纳入摘要；新增一条程序测试同时验证完整保留和缺 suggestion 的对象被拒绝。没有重写原 reviewer 结论或增加业务能力。

## 首版验收范围

六个原始场景均实际演练过，但不是六个真实应用端到端运行。覆盖的是指令路由、mock 门禁执行、错误/权限停止和局部 P1 映射；真实单 feature 代码实现、所有 P1 产物到真实完整候选、真实多 commit 合并/集成环境仍未运行。身份与报告真实性仍依赖可信人/agent；脚本不是签名审批或权限沙箱。删除、重命名、复杂交叠候选和 ADK/model 调度见 backlog，不在初版能力承诺中。
