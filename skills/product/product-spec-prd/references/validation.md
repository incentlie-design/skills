# 创建期有界验证记录

日期：2026-08-31。任务：product skill 首版；worktree：`.worktrees/product`；分支：`agent/skill-system/product`；基线：`a9b20de16e8e1603606f09db3a940186a15e1708`。只编辑两个 product skill，README/registry/公共 docs 留给集成人。此记录不代表独立评审或正式发布。

## 实际环境检查

- 当前 `python3` 为 `/usr/local/bin/python3`，Python 3.14.2。
- 实际执行 `python3 -c 'import importlib.util; print(importlib.util.find_spec("yaml") is not None)'` 的同等环境探测，输出 `PyYAML available: False`；已读取官方 `quick_validate.py`，其入口依赖 `import yaml`。
- 官方 quick_validate：**not_run**，因为当前解释器缺 PyYAML；没有安装依赖，也没有把失败前置条件当验证通过。
- `command -v openspec` 没有返回可执行文件，退出码 1；OpenSpec CLI 校验 **not_run**。只完成官方文档联网核对与手工文件流示例，没有假日志。

## 定向检查范围

使用主协调者 build worktree 的 `scripts/validate_skills.py`，显式 `--root` 指向 product worktree，`--skill` 仅选两个 product skill；没有复制脚本到本分支或跑全仓验证。该检查只校验 metadata/frontmatter/cases/依赖与本地文档链接，不执行行为用例。

创建过程中把已有 TASK 编号明确列为 `task_id` 字段；一次自查检查原始诉求→REQ/AC→delta→task 的覆盖和权限。没有改变六条原始 case prompt。

首轮定向验证器退出码 **1**：检查 2 个 skill、定义 6 cases、执行 0 个行为 case；仅报告 proposal/prd/design 三个 raw-input 相对链接多退一层目录。按该证据定向修正，从 `../../../../raw-input.md` 改为 `../../../raw-input.md`，不扩围。随后同一范围复验退出码 **0**：`status=pass, skills_checked=2, cases_defined=6, behavior_cases_executed=0, errors=[]`。

补充 fixture 结构 smoke 退出码 **0**：JSON/envelope 字段和路径有效；三项未完成任务具备 owner/依赖/write_scope/AC/预算/停止字段，依赖有序无环、写入范围不重叠，PRD/delta/tasks 的 AC-001 至 AC-004 标识覆盖一致。这不是场景执行或 OpenSpec 语法认证。

随后主协调者明确收紧公共 revision 类型；完整读取 build worktree 更新后的 contracts，仅对自己两个 skill 做本轮唯一契约修正：`artifact_revision/reviewed_revision` 为正整数，fixture 均为 1，`uncommitted` 仅在 commit 类字段。公共 docs 未修改，集成需包含主协调者的这项契约更新。

按收敛要求做**最后一次定向 smoke**，退出码 **0**：通过 `runpy` 调用同一只读验证器 `validate(root, ['product-spec-prd', 'product-review-prd'])`，并检查两个 revision 字段的精确 int 类型/正值、fixture 路径、每 skill 恰好三 cases；六条原始 prompt 的 SHA-256 与修正前完全一致。结果仍为 `2 skills / 6 defined / 0 behavior executed / 0 errors`。只修改相关断言以符合新类型，没有改 prompt 或增加用例。

## 未执行与交接

- 两个 skill 各有 happy/missing_input/boundary 三个原始用例。**behavior_cases_executed = 0**；定义断言不等于执行通过。
- 当前可用工具没有独立 subagent 执行器，未创建额外用户 task 代替 subagent。交给主协调者安排独立盲测；不得由实现者签最终评审。
- 盲测只提供原始 prompt、skill 和所需 raw artifacts，不提供 expect、此验证记录或评审示例的预期结论；PRD 正常例输入取 raw-input 的需求/基线，不把已填输出当新产物。
- 不验证应用、客户端自动发现、OpenSpec 安装、sync/archive、全量集成或远端动作。active 是首版登记状态，不是 active-ready/已集成认证。

## 给主协调者的 backlog

1. 冻结候选后执行现有三个原始用例的独立行为演练；有真实缺陷才回传定向修复。
2. 将官方 quick_validate 留给已有 PyYAML 的受控验证环境；将 CLI 兼容性留给已有明确 OpenSpec 版本的环境，不为本次自动安装。
3. 若实际用户出现 brownfield MODIFIED 场景，再用真实基线追加有证据的覆盖；本轮只交付既定三个代表 case，不扩测试矩阵。
