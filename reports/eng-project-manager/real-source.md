# 真实接入来源：PM-SKILL-001

本文件是 2026-08-31 委派中的明确交接摘要与原文留存，非 fixture、非本子会话 get_goal 的返回值。父任务 ID 为 01a05360-3ad2-7211-a3b5-48d7fe3189df；父任务标题为「制定skill规范并创建配套skills」。

## 用户原始需求（原文）

“构建一个项目经理的角色，现在经常有很多长程运行的goal，跑着跑着就乱了。在goal后，项目经理接入，对主agent拆解的任务项，进行管理和跟踪。我需要一个项目经理skill，帮我管理和查询当前goal的进展，他需要zoom out出来，结合项目原始目标，进行查询。原始目标和拆解过程，应该是一个DAG，帮助我了解卡在哪里。整理当前的主要的产出文件，以及分层的结构：产品文档，技术文档，需求列表，问题列表。”

委派进一步说明：该用户需求含“创建一个单独的session”，当前专属会话就是该实现会话，不另建任务或 subagent。

## 完整交付要求（按委派保留）

1. 可在 goal 建立或进行中接入主 agent 的原始目标、约束、任务拆解、依赖、session/owner 与现有证据。明确项目/goal 身份，多个 goal 不能混淆；保护原始目标和拆解沿革，不能为了局部完成重定义成功。
2. 用机器可读 DAG 表达原始目标→需求/验收→任务的分解关系和任务依赖，明确边类型/方向及 DAG 校验；可输出人能读的 DAG（如 Mermaid），查询总体进度、单任务状态、阻塞原因、上下游影响、目标遗漏/偏离和下一责任人。缺依据、未执行、过期证据与已验证完成分开，不凭任务数声称产品目标完成。
3. 管理不是一次性摘要：提供接入、刷新/对账、查询的可重复闭环；主 agent 事件/交接更新可追踪 revision/时间/来源，旧证据不能给新实现放行。项目经理提出推进建议，不替主 agent 写业务实现，不未经授权改变 goal/任务/远端状态。
4. 生成主要产出文件索引，至少分为产品文档、技术文档、需求列表、问题列表；关联需求、任务、owner、证据与修订，路径可用、缺失显式展示，不复制全部产物或强行搬迁原项目目录。
5. Codex 能力须以实际可用工具为准。get_goal 通常只读调用会话，不能伪造跨会话访问；可用 task 查询工具读取指定主任务，否则使用明确来源的导出快照/交接文件并标明新鲜度。不要读取未公开内部数据库或假造 CLI/API。不要因为创建 skill 就创建后台自动化；未来用户明确要求定期跟踪时才用产品支持机制。
6. 按 skill-creator、本项目 meta-skill-governance、docs/skill-standard.md、docs/contracts.md 开发。输出 SKILL.md、skill.json、tests/cases.json，必要时加脚本/模板/示例；统一源放 skills/engineering/eng-project-manager/，相对 .agents/skills 暴露，更新四个登记文件；唯一 writer，不改其他 skills。
7. 每项要求有验收证据，至少正常、缺失/失败、越界 3 个实际行为案例。脚本实跑，覆盖 DAG/阻塞、刷新/过期证据、分层索引。一次验收+最多两次定向修复；不扩展为平台。提供真实 worktree/branch/commit、命令结果、样例输出、未测限制，留本地 candidate；不 push、发布、安装、合并 main。父任务独立全范围验收后才完成。

## 已观测来源与限制

- 委派明确告知：父任务刚在自身调用 get_goal，确认 active goal 为以上用户需求。本任务只保留此交接，不宣称自己跨会话调用成功。
- 本任务实际调用 read_thread(threadId=上述 ID, turnLimit=3, includeOutputs=true)：返回 identity、cwd=/Users/jiajun.lai/Documents/workspaces/skill-creator、当前 active 状态；最近两轮 items=[]，更早一轮是九个旧 skills 的工作记录。旧记录不是本次 PM goal 的完成证据。
- 因最近正文不可得，real-intake 的主来源标 partial。goal_id=PM-SKILL-001 是委派给出的本地跟踪 ID，不是伪造的 native goal ID。
- 实际本地 Git 读取：父 main 与本 worktree 初始均为 78667f7cb54adb7e5a85c8c7d3b418e7634b7786；本 worktree 位于 /Users/jiajun.lai/.codex/worktrees/1e05/skill-creator，分支 codex/eng-project-manager。文件索引以该实际 worktree 为根。
- real-intake 的 REQ/AC/TASK 是 PM 为本次演练整理的管理拆解，标为 proposal，不写入父任务计划。task/AC 不登记 done，evidence 为空；文件存在不代表 skill 已独立验收。
- 父任务稍后独立复现祖先 blocked 被汇总覆盖的缺陷，作者已据此修正。父任务通知：修正后脚本 SHA256=58e399a57e64e56b0bf42b1da8cd39c5df720f8547d9f72aee4ee0a845a9970d，独立三场景 0.047s 通过；该结果不构成全范围验收。
