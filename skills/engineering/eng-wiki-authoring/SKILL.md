---
name: eng-wiki-authoring
description: Author dual-track (user/developer) project wikis with Diátaxis/k8s/React-style IA, diagram rules, and source-to-page compilation. Use for wiki/docs scaffolding or restructuring; do not own product architecture truth or Git mutation.
---
# Wiki authoring

项目 Wiki 编写（用户轨 + 开发者轨）。

Own the bounded wiki/docs authoring artifact only. Do not write any slice of [the shared governance contract](../../../docs/governance-contract.md) or take over surrounding governance decisions.

参考：Kubernetes docs（Concepts / Tasks / Tutorials / Reference）、React.dev（Learn / Reference）、Vue（Guide / Tutorial / API）、Diátaxis（Tutorial / How-to / Reference / Explanation）。本 skill 产出**可导航的 wiki 骨架与成稿规则**，不是一次性散文。

## 何时用

- 从零搭项目 wiki / docs 站点 IA
- 把产品说明、架构、数据流、API、仓库文档**编译**成双受众文档
- 统一图表、术语、交叉链接规范
- 审查现有 docs「写乱了 / 受众混了 / 图说不清」

## 核心原则（先读再写）

1. **双轨分流，永不混页**：一页只服务一种主要读者（用户/操作者 **或** 开发者/贡献者）。需要两边都看的主题 → 各写一页并互链，禁止在同一页一半推销一半讲端口实现。
2. **按意图分型（Diátaxis + k8s）**：
   | 类型 | 回答 | 写法 | 对标 |
   | --- | --- | --- | --- |
   | Tutorial / 教程 | 带我学会 | 有终点的学习路径，可照做 | React Learn、k8s Tutorials、Vue Tutorial |
   | How-to / Task | 我要完成 X | 短步骤、少解释 | k8s Tasks、Vue Examples/recipes |
   | Explanation / Concept | 这是什么、为何 | 概念与边界，少步骤 | k8s Concepts、Vue Guide |
   | Reference | 字段/命令/契约是什么 | 干、全、可检索，镜像真实结构 | React Reference、k8s API、Vue API |
3. **Learn 可省略边角；Reference 必须穷尽**（React 显式规则）：教程/概念不必覆盖所有字段；参考页与生成物负责完整真相。
4. **单一事实源（SSOT）**：可执行真相在代码/契约/架构叶子；wiki **投影**它们。优先 **git 版控的 docs 站点**（Hugo/VitePress/`docs/`），不要用 GitHub Wiki 当主 SSOT。
5. **先骨架后填肉**：先落目录与页面类型标签，再按「入门 → 核心概念 → 主路径 How-to → 参考」填。
6. **图服务于问题**：每张图只回答一个问题。禁止装饰图与无图注的大图。

## 输入盘点（编译前必做）

| 来源 | 典型路径 | 主要喂给 | 注意 |
| --- | --- | --- | --- |
| 产品/BD | pitch、roadmap、用户故事 | 用户轨 Explanation + Tutorial | 不写进 Reference |
| 架构 | `ARCHITECTURE` / `docs/architecture/*` | 开发者 Concept + 图 | 按问题叶子引用，勿整本粘贴 |
| 数据流 / 工作流 | topology、e2e、sequence | 双轨各一版（用户白话 / 开发者精确） | 用户版禁止内部类型名堆砌 |
| 领域模型 / ER | concepts、schema | 开发者 Concept；用户只需白话关系 |
| 公共命令 / API / CLI | contracts、OpenAPI、`--help` | Reference（尽量生成） | 手写易腐，标来源 commit |
| 仓库 README / ADRs | 根 README、ADR | 入门、决策 Explanation | ADR ≠ Concept 首页 |
| 旧 wiki / 静态页 | GitHub wiki、`docs/dev` | 迁移映射 | 标 deprecated，勿双份 |

先出 **Source → Wiki page** 映射表再开写。

## 推荐顶层 IA（完整骨架）

路径用稳定英文；导航可显示中文标签。

```text
docs/wiki/                    # 或网站 content/
  README.md                   # Hub：选路 + 版本戳
  _glossary.md
  _diagrams.md                # 图表规范与色板
  assets/diagrams/            # .mmd 源与/或 SVG
  user/                       # USER · 会用
    index.md
    getting-started/          # install + quickstart（<1 会话可跑通）
    tutorials/                # 多步骤学习目标
    how-to/                   # 单目标短步骤
    concepts/                 # architecture / data-flow / 产品对象
    reference/                # 用户可见配置、权限、导出格式
    troubleshooting/
  developer/                  # DEVELOPER · 会改
    index.md
    getting-started/          # local-dev、跑测试
    concepts/                 # 层、领域、生命周期（可深于用户）
    how-to/                   # 加绑定、接 Provider、排障
    reference/                # API/CLI/错误码/布局（优先生成）
    architecture/             # 链或摘编 architecture pack
    contributing/             # PR、文档门禁、docs-style
    design-decisions/         # ADR/RFC 索引
  shared/                     # release-notes、security、community
```

### 用户轨最小完备

1. `user/index.md` — 是什么 / 非目标 / 三条下一步  
2. `user/getting-started/quickstart.md` — Tutorial  
3. `user/concepts/overview.md` + `lifecycle.md`  
4. `user/how-to/main-path.md` — 主路径  
5. `user/reference/*` + `troubleshooting/`

### 开发者轨最小完备

1. `developer/index.md` — 代码地图与读序  
2. `developer/getting-started/local-dev.md`  
3. `developer/concepts/{architecture,domain,dataflow,lifecycles}.md`  
4. `developer/how-to/*` + `reference/*`  
5. `developer/architecture/*` + `contributing/*`

**链接策略**：用户页不依赖贡献者页；贡献者页可链产品 Concept/Reference 作真相。

## 页面骨架（k8s 结构）

| type | 建议小节 |
| --- | --- |
| Concept | overview → body → what’s next |
| Task / How-to | why → prerequisites → steps → discussion → what’s next |
| Tutorial | overview → prerequisites → objectives → lesson → cleanup → what’s next |
| Reference | synopsis → options/fields → examples → see also（生成优先） |

**Front matter 建议**：

```yaml
---
title: ...
linkTitle: ...          # 短导航名
weight: 20              # 同级排序，10/20/30…
audience: user | developer
type: tutorial | how-to | explanation | reference
status: draft | current | deprecated
source:                 # 架构叶子或契约路径
---
```

## 从素材「编译」流程

1. 定受众与成功标准  
2. 建骨架（空页 + front matter + TODO 来源）  
3. 术语表先行  
4. 按问题投影架构 / 数据流（用户白话 vs 开发者精确）  
5. 产品叙事进用户 Concept；路线图标时效，不进稳定 Reference  
6. 同步/生成 Reference  
7. Tutorial 生人压测  
8. 旧文迁移 banner；禁止双 SSOT  
9. 门禁勾选 + 版本戳

## 图表规范

| 图种 | 用途 | 优先 |
| --- | --- | --- |
| 分层/依赖 | import 方向 | SVG 或 mermaid flowchart |
| 序列/主路径 | 命令穿越 | mermaid sequenceDiagram |
| 状态机 | 生命周期 | mermaid stateDiagram-v2 |
| ER | 拥有/引用 | mermaid erDiagram 或 SVG |
| 用户管道 | 主路径步骤 | step 卡片 + 可选 SVG |

**硬规则**：

1. 一图一问（标题写成问题）  
2. **Figure N. 题注** + 正文「见图 N」回指（k8s 习惯）  
3. 用户图 / 开发者图分开；色义全站固定并写入 `_diagrams.md`  
4. 简单流用 **inline Mermaid**（便于 PR）；复杂定稿用 **SVG**，源文件进 `assets/diagrams/`  
5. 参与者不宜超过 ~9；ER 不堆字段（字段进 Reference）  
6. 改图必改题注与相关 Concept

## 文风

- 用户：短句、先结果；标识符放 `` code ``  
- 开发者：可验证；MUST/禁止与架构叶子一致  
- How-to 5–15 步；Concept 深链而非粘贴全书；Reference 可长但可锚点

## 质量门禁

- [ ] 每页有 audience + type + weight  
- [ ] 用户轨无未解释内部模块名堆砌  
- [ ] quickstart / 主路径可独立跑通  
- [ ] 架构/数据流可回溯源路径或 commit  
- [ ] 图有 Figure N 与题注；双轨图未混用  
- [ ] Reference 与代码冲突以代码为准  
- [ ] 旧文档有迁移链接；版本戳已更新  
- [ ] Learn/Concept 未假称穷尽；边角在 Reference

## 反模式

- 一个 README 打天下 / 受众混页  
- 只有架构无 Tutorial（或相反）  
- Wiki 与 architecture pack 双真相  
- GitHub Wiki 当主文档  
- 数据流画到导出却不声明 Accept 等为独立命令  
- 路线图写进稳定 Concept 不标时效

## 每次交付

1. Source → 页面映射表  
2. 目录树（含 type）  
3. 术语表草稿  
4. 优先 5 页（双首页、用户 quickstart、开发者 architecture、主路径 how-to）  
5. 图表清单（问题、受众、格式、路径）  
6. 正文或 PR 片段

## 执行口令

盘点输入 → IA + 映射表（若只要骨架可停）→ 按门禁填页 → 图与术语贯穿 → 勾选门禁并报告版本戳与 TODO。
