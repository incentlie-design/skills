# DRAMA-SKILL-C09 用例先行记录

- 目标：创建跨短剧、电影、广告可用的剪辑节奏与字幕同步设计 Skill；不提供渲染器或旧应用 runtime。
- owner：dedicated-session:content-editing-rhythm。
- 初始 HEAD：cd990aaec765fcbd1731af970233484377c873aa；干净 detached worktree 建立 codex/drama-skill-c09 后，已 fast-forward 至 8271786fd12cc4a35339d56fb26d8635af50fa0c。
- 只写 skills/content/content-editing-rhythm/ 与 reports/drama-skill-intake/content-editing-rhythm/；公共文件由主任务维护。
- 实施前定义三个原始 prompt：tests/cases.json 的 TC-001 横屏广告缩 gap/人物错位；TC-002 电影缺 timing/速度目标；TC-003 不触发及附件权限边界。均为 synthetic fixture，不是真实媒体。
- 验收：三个目标产物可交接，原 take/音色/时长与 source revision 可追溯，缺 timing 不编数值，权限止步。
- 验证预算：首轮三个 case，每轮至多三个命令/十分钟；最多两次有证据定向修复。一个独立 reviewer 只收冻结运行文档和原始 prompt，不看 expect 或作者答案，不再委派；作者不签最终验收。
- 非目标：注册/安装/发布/源应用修改、媒体生成/试听、全仓回归、生产一集。

## 有证据的定向修复 1（测试输入）

独立 reviewer 首轮指出 TC-001 未单列 source in/out、原播放率，虽然纸面计算与缺口处理正确，但正常例精确执行资料不足。只补充该 fixture 的 T01/T02 源区间与播放率；不改 expect、SKILL.md、metadata 或 reference。原始三个 prompt 保留于 82cefc46ff8482fc212001723fcb6f6c12530c2c，首轮输出原样保留于 reviewer-round1.md。

补充事实为 synthetic fixture，不是从真实媒体得出。仅 TC-001 定向重演；TC-002/003 的 prompt、运行文档和判断均不变，明确复用首轮独立证据。第二轮预算仍至多三命令/十分钟，不扩媒体验证。
