# ElevenLabs 条件适配参考

仅在用户选用 ElevenLabs 或诊断网页/API 差异时读取。来自个人 `elevenlabs-voice-design` 方法快照及 `series-audio-bible` / `knowledge/audio/voice-and-accent.md` 的提炼；没有迁入脚本、密钥、账号声音或应用校验器，也不覆盖个人安装。供应商规则快照原标注 2026-08-18；本次未联网核实，以下不是当前接口保证。

## 模式与可执行边界

| 意图 | 历史经验及需核实项 |
| --- | --- |
| 从描述建立原创身份 | Voice Design；旧声音只能作为抽象特征参考，不写“保留此 voice”却调用新建模式 |
| 保留来源核心并调整年龄/口音 | Voice Remix；历史经验要求当前账户拥有的 custom voice，公开 Library 可用不等于拥有 Remix 权限。先核实来源资格；收到权限错误不原样重试，可提出原创 Design 替代，但不擅自新增付费调用 |
| 用已选声音读台词 | TTS；不是重新设计身份，交给制作执行。设计说明不进入 spoken text |

设计候选、生成预览、保存 custom voice、应用登记是分开的动作。历史 API 一次可返回多个预览；不把固定“三个”、参数范围或 voice ID 写成所有供应商的规则。无生成授权只交付 prompt 和请求计划，不能运行旧脚本的 dry-run 后声称已生成。

准备实际请求前，核对用户已有授权中的 mode、来源权限、模型、数量/成本上限、格式和目标位置；未明确部分仅在真正执行前补齐，不阻断已能完成的文档设计。密钥不写 prompt/spec/报告或 Git。

## 描述与试读

可用的历史描述结构为：语言/地域变体 → 性别呈现/年龄范围（适用时）→ 录音质量目标 → persona → 情绪范围 → 音色与自然节奏。它是供应商提示词经验，不是通用语音学标准。清洁录音的要求不能代替输出听检。

年龄写共鸣、颗粒、气息和力度；保持符合人物的交流速度。描述已经具体时，不把提高 guidance 当作默认修复，过强约束可能损害自然度；参数支持与值域在实际使用前查证。统一试读段落覆盖角色名、长短句和情绪变化，符合当前 API 长度限制；这里不固化字符数、种子、声速、输出格式或强口音为默认值。

若任务明确要求菲律宾英语，可把成长地区、母语影响、迁居/教育经历与用户希望的强度作为输入。Manila/Tagalog 只是可能的项目设定，不代表所有菲律宾人；节奏、元音、R 等细节需有该角色适用的说话样本或资料，不机械执行 F/V/TH 替换。其他地域同理。

## 网页与 API 对照

不要只对齐 voice ID。先收集 [交接字段中的比较条件](handoff-fields.md)，重点确认网页和 API 的 model、全部设置、同一文本与规范化、语言/发音词典、前后上下文、随机控制（若提供）、enhancement、输出格式与后处理是否一致。网页未暴露的设置写 unknown，不猜成 API 默认值。

同文本/同条件比较身份与口音；身份比较和情绪表演比较分开。不同处理版本保留源 take 与处理链；变速/EQ 不能声称改变了底层 voice 身份。候选预览 ID 与保存后的 voice ID 不混用；只有真实生成/保存回执才可记录，选择本身不授权保存或写 Registry。

## 当前一手资料入口

若要使用或改变 API 字段、模型/费用/长度限制，需按当前任务权限核对一手资料；离线任务保持“未验证”，不宣称本参考已查证当前 API：

- [Voice Design 指南](https://elevenlabs.io/docs/eleven-creative/voices/voice-design/)
- [Voice Design API](https://elevenlabs.io/docs/api-reference/text-to-voice/design)
- [Voices 能力与 Remix](https://elevenlabs.io/docs/overview/capabilities/voices)
- [提示词指南](https://elevenlabs.io/docs/best-practices/prompting)
