---
name: content-storyboard-shotlist
description: "Compile a timed shot list and storyboard from a locked episode script. Use for 分镜、镜号、shot list、animatic; not for generating images, mixing audio, or rewriting dialogue."
---

# 分镜与镜号表

把已锁剧本编译成可交给生成/合成的镜头表。镜头是生产单位；格/panel 不是集。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **先动画、后镜头表。** 60–120s 先用旁白时间轴切拍，再填画面。禁止先出美图再倒推剧情。
2. **一镜一动作。** 复杂动作拆镜，不在单次生成里堆情节。
3. **镜号字段。** scene、shot_id、size、angle、move、duration_s、sound（分 music / ambience / foley，可空）、cut_in/out、asset_ids、axis/screen_direction。缺时长的板子不能当 animatic。声音功能细节交给音乐床与环境声 Skills。
4. **先静帧。** 需要视频时：先生成/选定 start frame，再运动。禁止盲 text-to-video。
5. **覆盖有上限。** 每场默认 master + 必要 singles/inserts。无限变体既烧钱也毁身份。

## 输出

`artifact_kind=shot-list` 与可选 `storyboard-notes`。每镜绑定脚本行与资产 ID。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `visual_director`。`r_alignment` = R3, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `episode_script_ref` | yes | ref | 单集 episode-script |
| `duration_s_range` | yes | int_pair | 每集体测秒数闭区间，固定 [60, 120] |
| `camera_treatment_ref` | no | ref | camera-treatment |
| `blocking_plan_ref` | no | ref | blocking-plan |
| `character_visual_lock_ref` | no | ref | 指向 character-visual-lock |
| `aspect_ratio` | no | string | 如 9:16 或 16:9；未选则不得宣称原生构图完成 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `shot-list` | `visual_director`, `audio_director`, `editor` |
| `storyboard-notes` | `visual_director` |

禁止：`rewrite_dialogue`, `media_generate`。

## 停止

不改对白，不调用模型，不把 panel 叫成 Episode。
