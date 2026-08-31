# DRAMA-SKILL-C01 候选说明

已完成 `content-cultural-research@0.1.0`，保持 `draft`。写入仅限本 Skill 和本报告目录。候选用于主任务最终审阅；作者不自签最终行为验收。

## 交付与版本

- 起始 main：`cd990aaec765fcbd1731af970233484377c873aa`；工作区初始干净，已 fast-forward 到 foundation `8271786fd12cc4a35339d56fb26d8635af50fa0c`。
- 原始 case 先于实现冻结：`b6467d9bbde00c74762aab8c1c01ec5508588e92`。
- Skill 冻结候选：`acef6cb8e80d1212bd372fe0d16e91b46ab38524`。本报告不自引用其最后提交 hash；最终包含报告的 commit 在最终答复给出。
- 分支：`codex/drama-skill-c01-cultural-research`；worktree 与公共 envelope 见 [handoff.json](handoff.json)。
- 入口：[SKILL.md](../../../skills/content/content-cultural-research/SKILL.md)；元数据、三用例及唯一必要 reference 一并交付。无新脚本、应用 schema 或项目预设。

## 方法与来源

先比较时代、地域、受众/语言、媒介变化、争议风险及已有证据，再选择 `not_applicable`、`local_only` 或获准的 `external_scoped`。明确预算/实际动作/停搜条件，原著事实、用户要求、研究事实、创作推断分开，冲突不能靠多数或新旧消解。输出为 culture-brief、source-ledger、adaptation-constraints，可单文档交接；约束关联依据、实体、revision、消费者和解除条件。

只读来源为 drama-agents 的 `052fc44dcaafb9c2c10d6365f391dc422918a146`，读取时工作区干净。完整定位与读取范围见 handoff 的 source_provenance。

| 来源 | 提取的方法 | 未迁入的部分 |
| --- | --- | --- |
| production-cultural-research | 来源/主张分离、时代地域、相反证据、权利边界；明确旧版只包装 captures | verifier、receipt、私有 schema、编译器与批准运行时 |
| episode-localization-direction | 称谓/语域/语言切换，物质和声音文化约束，按消费者交接 | 每角色强制口音结构、固定同步模式、旧应用 authority |
| knowledge/audio/sound-and-timeline.md | 地域声音不可泛化为跨文化拼贴 | 历史故事、乐器清单、时长及媒体生产默认 |

来源脚本仅阅读定位原功能，没有执行或复制。未访问 drama-skills、个人 ElevenLabs 源、外网或媒体；这些不属于本任务必要输入。新入口不是旧私有 JSON 的直接替换，旧源及安装保持原样。

## 有限证据

[结构 smoke](structure-smoke.json) 记录确切命令、退出码、官方 quick_validate、JSON/链接/用例检查以及四个 Skill 文件的 SHA-256。结构结果 pass，`behavior_cases_executed=0`，没有将它写成行为通过。

[独立演练全文](rehearsal-round-1.md) 来自临时执行者 `/root/c01_blind_rehearsal`，未继承对话，只获冻结 Skill、公共契约和 [原始 prompts](original-prompts.json)，未看 expect/作者答案，无写入权、无再分派。三例均实际答复，以下只作证据定位，最终判断留主任务。

| case | 执行状态 | 实际结果 |
| --- | --- | --- |
| TC-001 / happy | executed | local_only，产出三类内容，研究结论 revise；明确 fixture、冲突/未知、四类依据和可继续/暂缓约束 |
| TC-002 / missing_input | executed | blocked + needs_input；不确认真实群体传统，列出恢复所需材料 |
| TC-003 / boundary | executed | 仅一句口语改写；不启动研究，执行说明确认为无文化适配问题 |

只进行首轮三例，无定向修复；行为执行只读命令1条、作者结构 smoke 1条、打包完整性检查1条，共3条。打包检查确认冻结 Skill 摘要未变、分支/基线匹配、全部改动在所属目录、报告 JSON/revision/链接有效，结果 pass，命令和输出保存在 handoff.validation.packaging。未增加媒体/付费调用或全仓回归。最终行为验收状态为 not_run，下一责任人为主任务集成人，不把“已演练”写成“已批准”。

## 未测与最小交接缺口

未测试真实联网采集、现实文化真实性/社群认可、媒体生产、客户端加载、发现入口、共享注册或跨 Skill 集成。这些不在当前授权/写入范围。所给例子全部是 fixture，不是现实文化事实。

没有因本轮演练发现需修复的实现阻断。主任务仍需审阅实际输出、统一登记和执行注册验证；本分支保持 draft，不修改 registry、README、AGENTS、CHANGELOG、公共 docs/scripts 或 `.agents`。不合 main、不 push、不全局安装，保留当前 session 与 worktree 供后续维护。
