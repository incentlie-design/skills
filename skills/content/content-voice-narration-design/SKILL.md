---
name: content-voice-narration-design
description: "Design distinct narration and character voice identities without selecting a TTS Provider. Use for 旁白声线、角色声音、cast voice、解说语气; not for ElevenLabs/Qwen adapter code, cloning real people, or paid TTS calls."
---

# 旁白与角色声音身份

产品已有 Voice Provider 路径；本 Skill 只定义 **听感身份**。不新增第三 Provider，不默认声音克隆。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

1. **旁白是独立角色。** 语气（议论/讲解/陈述）、距离、是否知情，与主角内心分开。
2. **一角一声。** 全季同一角色同一 voice 身份；禁止一人分饰多角除非改编策略写明。角色之间要有可听对比（音高带、语速、停顿习惯）。
3. **先选身份，后映射 Provider。** 产出 provider-neutral profile（年龄感、口音/方言是否允许、能量、稳定优先还是表演优先）。具体 `voice_id` 由产品选择冻结。
4. **文本预处理。** 数字、日期、专名读音写入剧本侧；不要把 IPA 词典当 Git 秘密。
5. **多角色分轨。** 旁白与角色分开生成再剪，不要一条声线读完全集。
6. **克隆不是默认。** 真人参考音频需要书面权利与同意；否则 `blocked`。

## 输出

`artifact_kind=voice-identity-pack`：每说话人 profile、对比说明、禁止项、是否允许 clone（默认否）。

## 停止

不发起 TTS，不把 API key 写入示例，不建议超时重放。
