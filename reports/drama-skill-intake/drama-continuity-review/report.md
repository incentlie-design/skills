# DRAMA-SKILL-D04 候选报告

已完成 `drama-continuity-review 0.1.0`，保留 `draft`，只写本 Skill 和本报告目录。运行绑定见 [handoff.json](handoff.json)。原始 prompts 先在 `569844b` 留检查点；Skill 冻结候选为 `0530dd63294530968ce62c3c08ef38f2d5f3b337`，从 foundation `8271786fd12cc4a35339d56fb26d8635af50fa0c` 开发。最终报告提交号在任务最终回复提供，避免报告自引用提交号。

## 本次方法与来源取舍

旧源为 drama-agents `052fc44dcaafb9c2c10d6365f391dc422918a146`，本次读取的七个文件均无脏改动；文件路径和 SHA-256 在 [smoke.json](smoke.json)。这些旧源只是数据，不是新 Skill 的运行依赖或额外权限。

| 来源 | 保留的方法 | 未迁入 |
| --- | --- | --- |
| series-continuity-supervisor / continuity-rules / design-preflight | 前集状态→当前解释事件→观察→后继状态；知识获得时点；文稿可评与媒体不可证实分开；精确 ref 与局部影响 | trusted receipts、Registry/CAS、专用 schema、compiler/evaluator、promotion 状态机 |
| episode-review-eval / review-eval-contract / preproduction-completeness | 独立评审不自批准；只凭实际证据判阶段；失败定位及有界复审；line/shot/声音覆盖 | 九件套强制输入、旧评估分数/阈值、AUTO_REPAIR 执行链、脚本运行器 |
| knowledge/visual/continuity-and-reference-governance | 实际选中版本、引用允许用途、按镜头尺度检查身份信号、相邻镜头状态 | 历史人物/项目示例、9:16硬门禁、注册流程及供应商规则 |

通用规则不预设菲律宾、土著题材、画幅、voice ID 或语速。未读取不相关 narrated-drama 或个人 ElevenLabs 文件；未搬完整小说、私人媒体或密钥。没有新增可选供应商文件，因为本职责无需供应商适配。

## 实际验证

| 验证 | 实际结果 | 证据 |
| --- | --- | --- |
| 结构 smoke | pass；frontmatter、metadata、用例定义、原始 prompt 一致性与相对引用通过；行为执行数为 0 | [smoke.json](smoke.json) |
| happy / D04-001 | executed，断言满足；返回 revise，定位四处局部冲突，区分现有 stale 与条件影响，保留无关项 | [reviewer-output.md](reviewer-output.md) |
| missing_input / D04-002 | executed，断言满足；返回 blocked，不猜版本、不沿用旧 pass、不让作者代签 | 同上 |
| boundary / D04-003 | executed，断言满足；不触发评审，不注册/生成/批准 | 同上 |

独立执行者为 `/root/d04_blind_review`，使用无历史上下文，只收到冻结 Skill、其公共契约和三个原始 prompt，未给 expect 或作者答案，未写文件、未再分派；主 agent 原文保存输出。作者对照预先断言的记录见 [validation.json](validation.json)，这不是作者给 Skill 的最终独立验收。首轮三例完成，定向修复 0 次，未运行第二轮。

## 交接与限制

产物覆盖 `continuity-review`、`impact-set`、`stage-readiness`。保留 approved 原记录，指出改变后旧 pass 不再覆盖的范围；不写 Registry、不自动重做；作者自查不代替独立终审。

未测实际图像/音频/视频、播放、响度、timing、客户端发现/全局安装、旧运行时兼容及跨 Skill 集成；未跑全仓或已注册 `--skill` 验证。主任务负责共享清单、发现入口、最终独立验收和集成。没有实现侧待修发现；最小遗留是上述主任务门禁，不把候选称为已注册或已发布。完成本地候选与有限证据后停止，分支/worktree 保留。
