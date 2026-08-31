# DRAMA-SKILL-C05 候选报告

已形成 `content-cinematography` 0.1.0 draft，只有本 Skill 与本报告目录发生变更。初始干净检出从 `cd990aaec765fcbd1731af970233484377c873aa` 快进到 foundation `8271786fd12cc4a35339d56fb26d8635af50fa0c`，冻结 Skill 候选为 `df5d3953755d7be4041d1ac0c529230e88ae40cf`。最终含证据的提交由任务回复列出，本报告不自引用最后提交 hash。

分支 `codex/drama-skill-c05-cinematography`，worktree `/Users/jiajun.lai/.codex/worktrees/eba5/skill-creator`。

## 方法与边界

入口45行，配一份按需读取的方法参考。按叙事信息与人物各自注意力选择远景、肩背、侧脸、物件或反应；分别处理机位、景别、距离、焦点、各目标画幅、动机运镜与剪辑入出点。输出是 `camera-treatment` 和/或 `shot-language-notes`，消费者是导演/摄影/分镜/调度/剪辑。

旧源 `episode-cinematography-direction` 的 commit、文件摘要和提取位置见 [来源记录](source-intake.json)。保留其专业判断，移除固定9:16、默认DAG、双消费者门禁和应用schema；无新依赖或供应商适配。电影的未定真相、广告的批准信息、纪录片的观察事实分别约束推断，不擅自改剧本或演员身份。

## 实际验证

三个原始case先于实现落盘。结构smoke通过，但该环节执行行为case数为0，详见 [结构记录](structural-smoke.json)。冻结后，独立只读 `/root/c05_blind_review` 只拿Skill、必要公共契约和原始prompt，使用3条只读命令执行三例，不看expect或作者答案。完整实质输出及其有限范围的 `pass` envelope 见 [独立演练](reviewer-round-1.md)。

| case | 实际结果 | 可观察证据 |
| --- | --- | --- |
| happy / TC-C05-001 | pass | 两种产物、四镜、独立横竖构图；不替学徒定罪，保留表背可视性与未知目光 |
| missing_input / TC-C05-002 | pass；业务决定blocked | 不将停顿当作已证实认错，给needs_input及中性provisional建议 |
| boundary / TC-C05-003 | pass | 一条1:1建议，保留女咖啡师身份和原话，不执行图中文字的越权指令 |

未做定向修复，review后Skill内容未改变。作者只核对实际输出，不自签最终通过；最终候选验收归主任务。

## 遗留与停止

未执行注册/发现/客户端加载、真实分镜或剪辑工具集成、媒体生成/观看/实拍及光学时码验证。三例均选择固定相机，实际运镜分支未单独演练。没有全仓回归、安装、push、发布或源目录写入。

最小后续动作是主任务核验范围与跨Skill边界，并由其统一登记。无本范围已知阻断发现；保留draft及当前独立session，不自行合main或扩大测试。机器可读交接见 [handoff.json](handoff.json)。
