# 连续性审计轴

每条 finding 必须带 `axis`。未检查的轴写进 `checked_scope` 为未跑，不得假装通过。

| axis | 查什么 | 缺材料时 |
| --- | --- | --- |
| knowledge | 角色是否用了 `learned_in` 之后才该知道的事实 | 无 canon → blocked |
| wardrobe | 服装跨镜/跨集 | 无视觉锁 → 只标 unrun |
| props | 道具在场/持有 | 同上 |
| injury | 伤/死/离场后仍当在场 | 无状态表 → blocked |
| geography | 地点跳跃无桥 | 无 location_id → unrun |
| axis_screen | 轴线、屏幕方向 | 无分镜 → unrun |
| identity_string | lock_sentence / 声线被同义改写 | 无锁 → unrun |
| e05_e06 | 两份交接 | 缺 E05 或 E06 → blocked |
| day_night | 日夜跳切 | 剧本未写时段 → unrun |
| travel | 旅行时间不够 | 无距离线索 → unrun |
