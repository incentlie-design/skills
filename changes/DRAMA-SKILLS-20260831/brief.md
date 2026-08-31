# 短剧与通用内容专业 Skill 整理

## 目标与边界

用户要求在 skill-creator 源仓库创建短剧相关 Skill，每个 Skill 有独立任务/session；区分短剧专用与可跨媒介复用的专业能力，并整理已有 Skill。统一遵循 meta-skill-governance，沿用 eng/product 的任务、交接、版本和有限验证规范。

本批次 14 个独立候选。只新增 drama 分类；通用专业沿用 content 分类，避免与 product 的简称混淆。已有 content-video-director-learning 是广告导演学习入口，保持名字/路径/行为不变；摄影、场面调度属于制作方法，不重复采集广告方法库。并行中的 presentation 类任务不在写入范围。

不修改 Drama 应用、已安装个人 Skill、已有工程/产品 Skill 的行为；不复制 Registry/CAS/Outbox/manifest 锁定脚手架；不联网采集、调用付费模型或生成一部真实剧集；不安装、发布、推送或删除历史版本。新源候选不是旧运行时自动替代品。

## 分层

| 层 | 内容 | 唯一职责 |
|---|---|---|
| drama / 短剧专用 | 全剧改编、单集写作、分镜生产、连续性评审、生产计划 | 短时长/拆集/串行推进/跨集回收与前置包 |
| content / 通用专业 | 文化、人物心理、视觉世界、人物视觉、镜头、调度、声音身份、声音编排、剪辑 | 不绑定某种题材、国家、供应商或画幅的专业方法 |
| 应用工程（不迁入） | 身份注册、Ledger、CAS、Outbox、job、权限、文件锁 | 消费 Skill 候选并管理执行事实，不由 Skill 假装完成 |

## 验收

- AC-001：14 个 Skill 各有独立任务、分支与 worktree；共享文件仅主任务写。
- AC-002：所有旧入口有“拆分/合并/保留/不迁移”的明确映射；不静默更名或覆盖安装。
- AC-003：每 Skill 具备可执行的方法、输入/输出、消费者、限制，不是描述性空壳；历史项目偏好只放案例/可选 preset。
- AC-004：每 Skill 至少三类原始行为用例，独立执行/评审区分结构与行为证据；每轮最多三命令/十分钟，最多两轮定向修复。
- AC-005：统一 registry、AGENTS、README、发现入口和 CHANGELOG；新类别校验不影响旧 content/eng/product。
- AC-006：前置包 handoff 使用稳定 source/entity/line/scene/shot/asset 引用和 revision；未经实际生产不得宣称已生成/已注册/已试听。

## 执行

主任务先提交 foundation（本 brief、分类与最小公共契约），子任务从该冻结 commit 快进后只写分配目录。task 的 sources 是只读资料，不是强制安装依赖。每任务 0.1.0 初版，验收前 draft；先本地候选再统一集成，不自合 main。

独立行为演练允许一个有界 reviewer 子 agent：只给冻结 Skill 与三条原始 case prompt，不给 expect/作者答案，不再分派。输出保留可检查产物。主任务最终检查候选范围、跨 Skill 边界和来源迁移，不重复跑 14 个完整生产流程。

完成候选即停止；不完整候选明确停在 draft/review。此处创建的任务是用户可继续维护的独立 session，不创建自动轮询任务。

## 任务

详见 tasks.json。共享文件 owner 为本主任务（短剧主agent），write_scope：AGENTS.md、README.md、CHANGELOG.md、registry.json、docs/skill-standard.md、docs/content-production-contract.md、docs/drama-skill-migration.md、scripts/validate_skills.py、tests/test_validate_skills.py、.agents/skills 新入口、changes/DRAMA-SKILLS-20260831/、reports/drama-skill-intake/ 汇总。
