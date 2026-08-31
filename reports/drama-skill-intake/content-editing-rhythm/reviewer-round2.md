**TC-001｜定向重演结果**

三份产物共用：`artifact_revision=2`、`readiness=candidate`；范围仅本段局部修订；输入为 `fixture://C09/{brief,lines,shots,audio,words,timeline}@1`。speech/word/picture 均以 provided fixture 为依据，未实测。删gap是用户决定；字幕布局为候选提议。

`edit-rhythm-plan`：

| line／画面主体／镜头 | 原镜头区间 → 候选区间，ms | 原因 |
|---|---|---|
| L01／C01／S01@1 | `[0,3000)`→`[0,4400)` | 静帧延长，覆盖完整介绍及400 ms停留 |
| L02／C02／S02@1 | `[3000,9000)`→`[4400,8200)` | 在L02起点切入老二 |

新总长 **8200 ms**。两句speaker仍为旁白 `V01@3`，不换成画面角色。4400处人物与台词交接，环境声carry；无新增镜头。

`subtitle-spec`：

| cue／镜头／原样文本 | 源cue → 目标cue | 稳定token：源 → 目标 |
|---|---|---|
| L01／S01／老大守住门口。 | `[0,4000)`→不变 | L01.w01 老大 `[0,800)`；w02 守住 `[800,2000)`；w03 门口。`[2000,4000)`，均不变 |
| L02／S02／老二跑向出口。 | `[5200,8200)`→`[4400,7400)` | L02.w01 老二 `[5200,6000)`→`[4400,5200)`；w02 跑向 `[6000,6800)`→`[5200,6000)`；w03 出口。`[6800,8200)`→`[6000,7400)` |

显示文本对应所给spoken text；标点附词。非活动白色，活动词在自身半开区间内黄色，结束恢复白色；cue外隐藏。原生1920×1080，安全矩形 `(96,54,1584,918)` px。提议56 px、最多两行、底部居中、内边距24 px，实测行宽≤1536 px。字体、裁切及格式待确认；25fps下上述端点均落帧，无须舍入。

`sync-change-plan`：

- 拟议组SG01关联两句、两镜、两take、全部词与AMB01。保留 `[4000,4400)`，删除 `[4400,5200)`；此前不变，删除段标deleted，此后统一减800 ms。
- AMB旧 `[0,4400)` 与 `[5200,9000)` 分别接成新 `[0,4400)`、`[4400,8200)`。S02跨删除段先分段映射，再将新 `[3000,4400)` 明确交给S01覆盖。
- 保留approved `T01@1`：文件4000 ms、source `[0,4000)`；`T02@1`：文件3000 ms、source `[0,3000)`；两者原率1、voice `V01@3`及审批来源均不变。hash未提供，不补造。
- 保留原timeline@1供恢复；旧切点、字幕及AMB拼接下游待更新。无music/SFX，相关处理不适用。

三份计划交剪辑、字幕执行者及音画复核者，`handoff.status=pass`，仅限文字方案完备。开放项为字体、裁切和执行格式；真实语音尾部、AMB接缝、字幕溢出/遮挡及高亮支持均待实际复核，未生成媒体。

独立 review envelope：

```json
{
  "schema_version": 1,
  "run_id": "C09-forward-r2",
  "change_id": "DRAMA-SKILL-C09",
  "repo": "skill-creator",
  "base_commit": "8271786fd12cc4a35339d56fb26d8635af50fa0c",
  "candidate_commit": "35a6081fcd3bde5bc3ad0e3fe87af5b18a2be293",
  "artifact_revision": 2,
  "reviewed_revision": 2,
  "status": "pass",
  "reviewer": "/root/c09_forward_review",
  "scope": "仅TC-001定向重演；TC-002/TC-003未重跑",
  "findings": [],
  "non_blocking_suggestions": [],
  "limitations": [
    "本轮实际执行一次TC-001文字演练。补充的source区间与playback_rate消除了首轮该例的源片段信息缺口；时间映射、新总长和三域关联纸面检查通过。",
    "依据委派明确声明仅补充TC-001 fixture，SKILL.md、skill.json、reference和公共契约均未变，首轮C09-forward-r1中TC-002/TC-003的文字演练证据可按该影响范围复用；这不表示两例在revision 2重新执行。",
    "冻结commit及文档未变信息由委派提供。本轮遵守0命令约束，未重新读取文件、Git状态、测试、作者答案或报告。",
    "所有时间依据均为provided fixture；未试听、渲染或验证真实媒体、字体排版、环境声接缝和执行器高亮支持。",
    "未调用网络、付费服务或媒体生成，未写入文件；本结论不签集成、媒体质量或最终批准。"
  ]
}
```
