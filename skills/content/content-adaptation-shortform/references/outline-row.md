# season-outline 行模式

每集一行，禁止用散文代替字段。

| 字段 | 规则 |
| --- | --- |
| `episode_ordinal` | 1–10，连续，不跳号 |
| `core_event` | 一件事，能被看见或听见 |
| `state_in` | 开集时谁知道什么、关系/伤/位置 |
| `state_out` | 相对 `state_in` 的唯一必要变化 |
| `hook` | 集尾未兑现，供下一集 `state_in` |
| `duration_s_budget` | 整数，∈[60,120] |
| `density_note` | 过密/过稀/合适；过密必须触发 cut/split |

E05 `state_out` 与 E06 `state_in` 必须能对上，只允许一份交接。
