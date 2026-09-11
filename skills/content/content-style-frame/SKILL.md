---
name: content-style-frame
description: "Lock series look: medium, line, palette family, texture, contrast — separate from character bone structure. Use for 画风锁、style frame、lookdev; not for copying a living artist's work, generating hero art, or minting product schema."
---

# 系列画风锁

人物锁骨相，画风锁媒介。两套锁不能混成一句 prompt。

读 [内容契约](../../../docs/content-production-contract.md) 与 [I/O 契约](../../../docs/content-skill-io.md)。

## 何时用

R2 系列资产；或评价发现每集画风跳。`media_form` 含画面时必做。

## 方法

### 门禁

`series_canon_ref` + `rights_status`。参考图若是在世作者作品，默认不可当可复制风格。

### 拆工作

1. **媒介。** `medium`：still-comic / painted-bg-photo-char / flat-cel / documentary-still。只选一个主媒介。
2. **线与质。** `line_weight`、`texture`（纸、胶片粒、无）。
3. **家族色。** `palette_family` 与 color-script 的节拍色板兼容，但不代替它。
4. **对比。** `contrast_band`：低/中/高。解说剧旁白段避免全黑看不清字幕。
5. **禁仿。** `do_not_copy` 列出不可模仿的在世作者/商业 IP。
6. **版本。** `lock_revision` 与人物 visual-lock 分开计数。

### 产物字段

`style-frame-lock`：`medium` `line_weight` `palette_family` `texture` `contrast_band` `do_not_copy` `lock_revision`。

### 失败分支

`copy_living_artist`。把画风句写进人物 `lock_sentence` → 回 visual-lock 拆开。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`, `producer`。`r_alignment` = R2, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `series_canon_ref` | yes | ref | 指向 series-canon 产物 |
| `rights_status` | yes | enum:rights_status | source 或参考资产权利：allowed / unresolved / denied |
| `character_visual_lock_ref` | no | ref | 指向 character-visual-lock |
| `reference_image_refs` | no | ref[] | 有权利的外形参考图 |
| `media_form` | no | enum:media_form | 成品形态 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `style-frame-lock` | `visual_director`, `producer`, `validator` |

禁止：`copy_living_artist`, `media_generate`, `mint_product_schema`。

## 停止

不生成英雄图。风格锁是文字+可选已有授权帧引用。
