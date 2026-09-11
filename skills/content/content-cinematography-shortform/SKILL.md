---
name: content-cinematography-shortform
description: "Design camera language for 60–120s narrated episodes, including shot size, axis, aspect ratio, and motivated movement. Use for 摄影、景别、轴线、运镜、竖屏构图; not for storyboards, blocking execution, or image generation."
---

# 短制镜头语言

把「观众此刻该发现什么」写成可拍摄/可生成的镜头选择。横竖屏各自原生构图，禁止裁切冒充。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **先注意力，后覆盖。** 每个在场人物看谁/看物；反应不得早于触发。
2. **景别/角度/运动是三轴。** 用封闭词表（ELS–ECU、平/俯/仰、固定/推/摇/随），不要用「电影感」当参数。
3. **轴线。** 每场一条 axis；越轴必须有观众可见过渡。生成图是独立样本，不写轴线就会左右对调。
4. **画幅。** 每种请求画幅单独安置主体、视线空间、字幕区。竖屏用纵深/上下层级，不把横屏填边当原生竖屏。
5. **运动要有动机。** 无必要时固定。运动写清起止、跟随对象、停止点。生成提示的焦段不是实测镜头。

## 输出

`artifact_kind=camera-treatment` 与 `shot-language-notes`。

## 停止

不改剧本，不编译逐帧，不生成媒体。
