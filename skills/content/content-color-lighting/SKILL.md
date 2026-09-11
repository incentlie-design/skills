---
name: content-color-lighting
description: "Design a per-beat color script and key-light direction that survives ten episodes without restyling identity. Use for 色彩脚本、光方向、色温、color script; not for grading that changes faces, or generating images."
---

# 色彩与灯光脚本

颜色是情绪与地点身份，不是滤镜包。换色温不得换脸。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

系列要跨集认出同一世界；或代表集评价发现「每集一个滤镜」。

## 方法

### 门禁

要有 `episode_script_ref` 与 `series_canon_ref`。无 `location_ids` 时地点光标 `provisional`。

### 拆工作

1. **节拍色板。** 每拍 `beat_palette` 3–5 色，来自世界规则而非随机流行色。
2. **主光。** `key_light_dir`：left/right/back/top/practical。与调度冲突则回 blocking。
3. **色温带。** `color_temp_band` 用 band（冷/中/暖）不是开尔文假装实测。
4. **连续。** `continuity_with` 指向相邻集已锁 color-script revision。
5. **禁看。** `forbidden_look`：霓虹赛博、美颜磨皮、与 lock 冲突的补光。
6. **调色边界。** 分级不得改变骨相与签名细节。

### 产物字段

`color-script`：`episode_ordinal` `beat_palette` `key_light_dir` `color_temp_band` `continuity_with` `forbidden_look`。

### 失败分支

用调色换脸 → `grade_as_identity_change`。生成概念图当锁 → 需另走 style-frame，且仍不 submit。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`。`r_alignment` = R2, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `series_canon_ref` | yes | ref | 指向 series-canon 产物 |
| `shot_list_ref` | no | ref | shot-list |
| `location_ids` | no | id[] | 本集出现的地点 |
| `style_frame_ref` | no | ref | style-frame-lock 产物 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `color-script` | `visual_director`, `editor`, `validator` |

禁止：`grade_as_identity_change`, `media_generate`。

## 停止

不输出 LUT 文件当产品依赖。
