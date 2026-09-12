# 镜号卡

一镜一行。缺 `duration_s` 不能当 animatic。

| 字段 | 规则 |
| --- | --- |
| `shot_id` | 新建 `proposed:` |
| `scene_id` | 场 |
| `line_id` | 绑定的旁白/对白；可空但要写理由 |
| `size` `angle` `move` | 只用摄影词表 |
| `duration_s` | 正数；全表合计 ∈[60,120] |
| `sound_music` `sound_ambience` `sound_foley` | 指针，不在此设计床 |
| `cut_in` `cut_out` | 动作/认知点 |
| `axis` | 继承场轴线 |

一镜一个主动作。需要视频时先定 start frame。
