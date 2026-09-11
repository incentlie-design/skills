---
name: content-voice-narration-design
description: "Design distinct narration and character voice identities without selecting a TTS Provider. Use for 旁白声线、角色声音、cast voice、解说语气; not for ElevenLabs/Qwen adapter code, cloning real people, or paid TTS calls."
---

# 旁白与角色声音身份

产品已有 Voice Provider 路径；本 Skill 只定义 **听感身份**。不新增第三 Provider，不默认声音克隆。

读 [内容契约](../../../docs/content-production-contract.md)。

## 方法

不发起 TTS，不把 API 密钥写入示例。产品已有 Voice 路径；此处只定义听感身份。

### 门禁

要有 `character_voice_profiles_ref`。克隆默认否。

### 拆工作

1. **旁白。** `narrator` 独立：语气、距离、是否知情，不是主角内心。
2. **一角一声。** 每 `character_id` 全季同一身份。一人分饰多角除非改编策略写明。
3. **可听轴。** `axes`：音高带、语速、停顿、用词、信息策略。填 `contrast_matrix`，相邻角色必须可辨。
4. **中性档案。** `provider_neutral_profile`：年龄感、口音是否允许、能量、稳定优先还是表演优先。不在此选产品 `voice_id`。
5. **读音。** 数字/日期/专名规则留在剧本侧，不把词典当秘密。
6. **分轨。** 旁白与角色分轨生成再剪。
7. **克隆。** `clone_allowed` 默认 false；无书面权利保持 false。

### 产物字段

`voice-identity-pack`：`character_id` `narrator` `axes` `contrast_matrix` `provider_neutral_profile` `clone_allowed`。

### 失败分支

建议超时重放 TTS → `forbidden`。无权克隆 → `blocked`。

## 输出

`artifact_kind=voice-identity-pack`：每说话人 profile、对比说明、禁止项、是否允许 clone（默认否）。

## 参数

字段名以 [I/O 契约](../../../docs/content-skill-io.md) 为准。`role` 只能是 `audio_director`。`r_alignment` = R2, R4。

### 输入

| 字段 | 必填 | 类型 | 含义 |
| --- | --- | --- | --- |
| `character_voice_profiles_ref` | yes | ref | 指向 character-voice-profiles |
| `series_canon_ref` | no | ref | 指向 series-canon 产物 |

缺必填字段 → `status=blocked`，`needs_input` 填字段名。

### 输出

先返回共享 envelope（`status` / `maturity` / `input_refs` / `open_questions` / `consumers`），再给下列 payload。

| artifact_kind | consumers |
| --- | --- |
| `voice-identity-pack` | `audio_director`, `producer`, `validator` |

禁止：`provider_submit`, `call_tts`, `clone_without_rights`。

## 停止

不发起 TTS，不把 API key 写入示例，不建议超时重放。
