---
name: content-production-plan-shortform
description: "Plan bounded short-form production: media form, parallel writers, cost stops, and whole-episode rework. Use for 制作计划、并行、成本上限、返工; not for Architecture changes, Provider live runs, or Stage Gates."
---

# 短制制作计划

把 R4/R6 的生产策略写成可执行边界：谁写哪集、什么算失败、何时停。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **先选成品形态。** audio-only / 静帧+音轨 / 完整音视频。形态未选不得假设必须出视频。静帧+音轨仍要决定：干声 / 干声+环境 / 再加音乐床。
2. **自动化程度。** 全自动 / 人锁资产后自动 / 人工 fallback。未知后禁止自动换 Provider。
3. **一人一集一目录。** 并行写者互不改 plan、资产定义、总清单。清单只有一个汇总者。
4. **整集重做。** 当前产品没有局部 revision 系统时，失败集整集返工，保留旧 evidence。
5. **数字上限。** 调用、成本、时间、query；超限停止或降级，不盲试。音乐/环境素材的许可证（CC、库、生成 NC）算进停止条件，不是事后补。
6. **W1 再 W2。** 代表集未 PASS 不得批量。

## 输出

`artifact_kind=production-plan`：形态、并行表、上限、失败策略、provenance 标记（hybrid/manual/live 候选）。

## 停止

不授权 paid/live。不把十个文件叫 1.0。
