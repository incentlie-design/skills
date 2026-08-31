# DRAMA-SKILL-C04：实施前边界与原始用例

目标：将人物正典转为稳定身份、年龄/皮肤表达、服装变体及可引用提示词；仅交付 `content-character-visual-design@0.1.0 draft`。

- main 来源：`cd990aaec765fcbd1731af970233484377c873aa`。
- 实际开发基线：`8271786fd12cc4a35339d56fb26d8635af50fa0c`，干净检出已通过 `git merge --ff-only` 同步。
- 分支：`codex/drama-skill-c04-character-visual`。
- worktree：`/Users/jiajun.lai/.codex/worktrees/b2ef/skill-creator`。
- writer：本独立维护 session；只写 `skills/content/content-character-visual-design/` 与本报告目录。共享清单、发现入口和集成验证归主任务。

在实现 SKILL.md 前定义 `tests/cases.json`：TC-001 正常的两人水粉风格、选中旧版本、服装与湿衣状态；TC-002 无正典、未提供图像和选中版本；TC-003 仅注册/生成请求且权限不足。原始 prompt 自包含且为 fixture，不需要任何真实媒体。独立执行者只读冻结 Skill/必要公共契约和三条原始 prompt，不看 expect、作者答案或本文件。

验收：三种输出能被分镜/调度/连续性消费者定位；不因换衣换人、不猜最新版本；年龄/晒感/纹理服从风格；服饰文化与历史表述有来源或明确创作归属；不强迫正脸；缺输入与越界可停止。作者自查不签最终通过，候选交主任务最终审核。

验证预算：首轮三个行为 case、每轮最多三命令/十分钟；最多两轮有证据的定向修复。媒体调用、付费接口、全仓回归、安装、push、合 main 均为零。只读 reviewer 不写工作区，返回原始演练结果，由维护者原样保存在本报告目录。
