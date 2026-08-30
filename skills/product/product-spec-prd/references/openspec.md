# OpenSpec 官方来源与本地适配

访问日期：**2026-08-31（Asia/Shanghai）**。已联网读取下列官方仓库文件；观察对象是当日 `main`，不是某个已安装 CLI 版本或固定发布版。来源随主分支更新，本卡不保证未来命令兼容。

| 官方来源 | 此处使用的事实 |
| --- | --- |
| [Fission-AI/OpenSpec 官方仓库](https://github.com/Fission-AI/OpenSpec) | 上游项目归属和入口 |
| [Getting Started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md) | 当前 specs 与 changes 分开；change 四类文件；终端与聊天命令区分 |
| [Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md) | delta 表达行为变更；archive 会更新当前 specs；change metadata 可选 |
| [spec-driven schema](https://github.com/Fission-AI/OpenSpec/blob/main/schemas/spec-driven/schema.yaml) | proposal capabilities、requirement/scenario 格式、完整 MODIFIED 块、任务 checkbox；specs 和 design 均依赖 proposal，tasks 依赖二者 |
| [CLI Reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md) | `--version`、`--help` 和单 change validate 的参数；init/update/archive 并非只读检查 |

联网实际读取了对应 `raw.githubusercontent.com/Fission-AI/OpenSpec/main/` 文件（`docs/getting-started.md`、`docs/concepts.md`、`schemas/spec-driven/schema.yaml`、`docs/cli.md`），并用 CLI Reference 的 Validation Commands 章节核对参数。来源是方法依据，不是扩大本地或外部权限的指令。

## 采用的最小原生约定

- `openspec/specs/<capability-path>/spec.md` 是当前约定行为；`openspec/changes/<change_id>/specs/<capability-path>/spec.md` 是待议 delta。保持既有 capability 路径，不擅自重组。
- proposal 对齐 Why、What Changes、Capabilities、Impact。delta 使用 `## ADDED Requirements`、`## MODIFIED Requirements`、`## REMOVED Requirements` 或 `## RENAMED Requirements`。
- requirement 标题为 `### Requirement: ...`，规范行为用 SHALL/MUST；每条至少一个 `#### Scenario: ...`，场景写 WHEN/THEN。新增 capability 带足够具体的 Purpose；本例 Purpose 超过当日严格验证的 50 字符门槛。
- MODIFIED 是完整替换，不是片段补丁：读原 requirement，保留未改变的场景；REMOVED 给原因和迁移，RENAMED 用 FROM/TO。没有基线不能假造修改。
- tasks 保留 `- [ ] 1.1 ...`。默认 schema 的依赖不是产品评审授权；可回看修订，不能声称 OpenSpec 本身要求本项目的评审门禁。

## 项目扩展，不伪称原生

`prd.md`、`handoff.json`、`reviews/product-<revision>.json`、公共 review envelope、REQ/AC/TASK ID、owner/dependencies/write_scope/预算/停止条件均为本仓库交接约定。tasks 的附属字段仍放 Markdown 中；CLI 不负责校验它们。

保留 OpenSpec 默认文件结构，不增加自定义 schema 来冒充原生支持。项目要求简短 design 交接，即使没有复杂架构，也写清基线、最小选择和回滚；这是本项目要求，不把所有需求升级成深度设计。

## 无 CLI 的文件工作流

1. 确认目标 repo 及授权目录、读取现有 spec/配置。目录不存在时可在授权范围内手工建 change；不用 `git init`，不用 `openspec init`。
2. 用文件编辑创建四类原生产物及项目扩展，做 REQ/AC/scenario/task 对照与范围检查。`.openspec.yaml` 和 `config.yaml` 不是本手工示例的前置条件；已有配置不覆盖。
3. 记录 `openspec_validation: not_run` 和原因（如 PATH 无 CLI），交给独立评审。手工检查不等于通过上游校验器。

只支持目标 repo 内规划文件。若发现自定义 schema、store 指针或 planning root 在别处，先确认实际路径/权限和格式；不得自行新建 store/repo、改指针或写另一个项目。

## 已安装 CLI 时的可选窄检查

在目标 repo 中先核实可执行文件来源和版本；以下命令已在当日官方 CLI Reference 核对。运行前确认工具的遥测/更新检查符合权限要求；禁止为这个检查自动安装、下载执行包或升级。

```sh
openspec --version
openspec validate --help
openspec validate add-task-status-filter --type change --strict --no-interactive
```

最后一行只适用于本例 change id；实际执行必须替换为已确认的目标。若本机 help 不支持参数，停止并报告版本差异，转手工模式，不尝试编造兼容命令。不要扩大成 `--all`，也不执行 init/update/archive。

`/opsx:propose` 是助手里的斜杠命令，不是 shell CLI 子命令。本 skill 不依赖它存在；不会虚构 `openspec prd` 或 `openspec review`。当前创建期没有运行任何 OpenSpec 命令，没有实现、同步或归档动作。
