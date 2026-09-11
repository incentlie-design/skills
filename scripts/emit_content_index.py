#!/usr/bin/env python3
"""Emit skills/content/index.json and INDEX.md. Data only; not a runtime dependency."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "skills" / "content" / "index.json"
OUT_MD = ROOT / "skills" / "content" / "INDEX.md"

# id, title, url, type, category, quality, r_alignment, include, security, why
RAW = [
    ("SRC-001", "anthropics/skills", "https://github.com/anthropics/skills", "collection", "meta-format", "stars=175810", ["R4"], "maybe", "none", "SKILL.md 格式与渐进披露；不当影视方法权威"),
    ("SRC-002", "agentskills/agentskills spec", "https://github.com/agentskills/agentskills", "collection", "meta-format", "stars=25236", ["R4"], "maybe", "none", "可移植 Skill 规范"),
    ("SRC-003", "openai/skills", "https://github.com/openai/skills", "collection", "meta-format", "stars=26903", ["R4"], "maybe", "none", "第二套官方 catalog 包装"),
    ("SRC-004", "vercel-labs/agent-skills", "https://github.com/vercel-labs/agent-skills", "collection", "meta-format", "stars=31064", ["R4"], "maybe", "none", "包装质量对照，非内容方法"),
    ("SRC-005", "huggingface/skills", "https://github.com/huggingface/skills", "collection", "meta-format", "stars=11038", ["R4"], "maybe", "none", "论文/模型检索 skill，非制片"),
    ("SRC-006", "NVIDIA/SkillSpector", "https://github.com/NVIDIA/SkillSpector", "tool", "safety", "stars=16951", ["R4"], "yes", "none", "安装前扫描注入与供应链"),
    ("SRC-007", "trailofbits/skills", "https://github.com/trailofbits/skills", "collection", "safety", "stars=7042", ["R4"], "maybe", "review", "安全审计模式有用；不导入 exploit skill"),
    ("SRC-008", "obra/superpowers", "https://github.com/obra/superpowers", "collection", "production-planning", "stars=285216", ["R4"], "maybe", "none", "验证门与可组合 skill；工程方法"),
    ("SRC-009", "addyosmani/agent-skills", "https://github.com/addyosmani/agent-skills", "collection", "production-planning", "stars=93534", ["R4"], "maybe", "none", "分阶段 define/plan/build/verify"),
    ("SRC-010", "ComposioHQ/awesome-claude-skills", "https://github.com/ComposioHQ/awesome-claude-skills", "collection", "meta-format", "stars=74867", ["R4"], "maybe", "review", "最大索引；含会真实动作的 connect，勿整包安装"),
    ("SRC-011", "hesreallyhim/awesome-claude-code", "https://github.com/hesreallyhim/awesome-claude-code", "collection", "meta-format", "stars=53879", ["R4"], "maybe", "none", "Claude Code 资源精选"),
    ("SRC-012", "VoltAgent/awesome-agent-skills", "https://github.com/VoltAgent/awesome-agent-skills", "collection", "meta-format", "stars=34093", ["R4"], "maybe", "review", "跨运行时大清单，只作发现层"),
    ("SRC-013", "VoltAgent/awesome-openclaw-skills", "https://github.com/VoltAgent/awesome-openclaw-skills", "collection", "safety", "stars=52497", ["R4"], "no", "exclude", "5400+ 未审 skill，尾部高风险，禁止整包"),
    ("SRC-014", "sickn33/agentic-awesome-skills", "https://github.com/sickn33/agentic-awesome-skills", "collection", "safety", "stars=46280", ["R4"], "no", "exclude", "含 pentest 改编与大规模拷贝"),
    ("SRC-015", "Fission-AI/OpenSpec", "https://github.com/Fission-AI/OpenSpec", "collection", "production-planning", "stars=67996", ["R4", "R5"], "yes", "none", "explore→propose→apply 门禁，产物为真相"),
    ("SRC-016", "calesthio/OpenMontage", "https://github.com/calesthio/OpenMontage", "skill-repo", "production-planning", "stars=57191", ["R3", "R4", "R5"], "yes", "review", "高星制片工作台；密钥只在环境，不进制品"),
    ("SRC-017", "calesthio/generative-media-skills", "https://github.com/calesthio/generative-media-skills", "skill-repo", "image-gen", "stars=170", ["R4"], "yes", "none", "OpenMontage 伴生工艺 skill，星低但领域贴合"),
    ("SRC-018", "SamurAIGPT/Generative-Media-Skills", "https://github.com/SamurAIGPT/Generative-Media-Skills", "skill-repo", "image-gen", "stars=4262", ["R4"], "yes", "none", "图像/视频/音频 prompt 操作层"),
    ("SRC-019", "eternityspring/shuohao-skills", "https://github.com/eternityspring/shuohao-skills", "skill-repo", "story", "stars=3206", ["R1", "R2", "R3"], "yes", "none", "大纲/人设/剧本/分镜门禁，最接近 R1–R4"),
    ("SRC-020", "zenstory-ai/drama-skills", "https://github.com/zenstory-ai/drama-skills", "skill-repo", "story", "stars=1795", ["R1", "R3", "R5"], "yes", "none", "短剧技能链含独立 review"),
    ("SRC-021", "nolanx-ai/nolanx.ai", "https://github.com/nolanx-ai/nolanx.ai", "skill-repo", "directing", "stars=1783", ["R2", "R3"], "yes", "none", "镜头语言、身份锁、连续性 bible"),
    ("SRC-022", "liangdabiao/Seedance2-Storyboard-Generator", "https://github.com/liangdabiao/Seedance2-Storyboard-Generator", "skill-repo", "storyboard", "stars=2314", ["R3", "R4"], "yes", "none", "小说到多集分镜/提示词"),
    ("SRC-023", "YouMind-OpenLab/awesome-seedance-2-prompts", "https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts", "collection", "cinematography", "stars=1971", ["R4"], "yes", "none", "镜头词表与角色一致性笔记"),
    ("SRC-024", "HITsz-TMG/VideoClaw", "https://github.com/HITsz-TMG/VideoClaw", "tool", "directing", "stars=1789", ["R4", "R5"], "yes", "none", "导演规划/摄影生成/评审重试编排"),
    ("SRC-025", "wuwangzhang1216/DirectorSKILL", "https://github.com/wuwangzhang1216/DirectorSKILL", "skill-repo", "directing", "stars=89", ["R3", "R4"], "yes", "none", "导演分析到 QC 的紧凑包"),
    ("SRC-026", "HBAI-Ltd/Toonflow-app", "https://github.com/HBAI-Ltd/Toonflow-app", "tool", "manga-anime", "stars=15486", ["R3", "R4"], "yes", "none", "高星漫剧桌面流水线"),
    ("SRC-027", "HKUDS/ViMax", "https://github.com/HKUDS/ViMax", "paper-code", "directing", "stars=12346", ["R4"], "yes", "none", "多 agent 影视生成论文代码"),
    ("SRC-028", "Narcooo/inkos", "https://github.com/Narcooo/inkos", "tool", "story", "stars=9719", ["R1", "R3"], "yes", "none", "小说/剧本/IP 上游 bible"),
    ("SRC-029", "Forget-C/Jellyfish", "https://github.com/Forget-C/Jellyfish", "tool", "production-planning", "stars=6361", ["R3", "R4"], "yes", "none", "脚本到一致性到成片工作区"),
    ("SRC-030", "ArcReel/ArcReel", "https://github.com/ArcReel/ArcReel", "tool", "visual-consistency", "stars=4428", ["R2", "R4", "R6"], "yes", "none", "资产/分镜/跨镜一致性/成本"),
    ("SRC-031", "xuanyustudio/LocalMiniDrama", "https://github.com/xuanyustudio/LocalMiniDrama", "tool", "manga-anime", "stars=1603", ["R4"], "yes", "none", "本地故事到视频的短剧工作流"),
    ("SRC-032", "LingyiChen-AI/AIComicBuilder", "https://github.com/LingyiChen-AI/AIComicBuilder", "tool", "manga-anime", "stars=1858", ["R3", "R4"], "yes", "none", "脚本到人设到动态漫画"),
    ("SRC-033", "wonderunit/storyboarder", "https://github.com/wonderunit/storyboarder", "tool", "storyboard", "stars=3837", ["R3"], "maybe", "none", "专业分镜 previz，非生成模型"),
    ("SRC-034", "remotion-dev/skills", "https://github.com/remotion-dev/skills", "skill-repo", "editing", "stars=4543", ["R4"], "yes", "none", "程序化视频装配与字幕"),
    ("SRC-035", "Vincentwei1021/video-shotcraft", "https://github.com/Vincentwei1021/video-shotcraft", "skill-repo", "cinematography", "stars=8076", ["R3", "R4"], "yes", "none", "镜头配方卡与节奏/音效方法"),
    ("SRC-036", "smixs/visual-skills", "https://github.com/smixs/visual-skills", "skill-repo", "directing", "stars=352", ["R3", "R4"], "yes", "none", "戏剧结构+模型语法分层"),
    ("SRC-037", "agentara/skills", "https://github.com/agentara/skills", "skill-repo", "storyboard", "stars=461", ["R3", "R4"], "yes", "none", "分镜强制跨格身份/服装/场景锁定"),
    ("SRC-038", "RainLib/AI-Storyboard", "https://github.com/RainLib/AI-Storyboard", "skill-repo", "storyboard", "stars=49", ["R3"], "maybe", "none", "Beat board 与 4C；星低但方法完整"),
    ("SRC-039", "aicontentskills/ai-video-storyboard-skill", "https://github.com/aicontentskills/ai-video-storyboard-skill", "skill-repo", "storyboard", "stars=48", ["R3"], "maybe", "none", "共享视觉主题与后期清单"),
    ("SRC-040", "majiayu000/claude-skill-registry", "https://github.com/majiayu000/claude-skill-registry", "collection", "storyboard", "stars=604", ["R3"], "maybe", "none", "含小说转分镜表 skill"),
    ("SRC-041", "JimLiu/baoyu-skills", "https://github.com/JimLiu/baoyu-skills", "collection", "visual-consistency", "stars=25839", ["R4"], "maybe", "review", "版式矩阵有用；发布类 skill 需凭据"),
    ("SRC-042", "tencent-ailab/IP-Adapter", "https://github.com/tencent-ailab/IP-Adapter", "paper-code", "visual-consistency", "stars=6684", ["R2", "R4"], "yes", "review", "图像作条件；FaceID 有克隆风险"),
    ("SRC-043", "cubiq/ComfyUI_IPAdapter_plus", "https://github.com/cubiq/ComfyUI_IPAdapter_plus", "tool", "visual-consistency", "stars=6124", ["R4"], "yes", "none", "本地身份图工作流"),
    ("SRC-044", "instantX-research/InstantID", "https://github.com/instantX-research/InstantID", "paper-code", "visual-consistency", "stars=11991", ["R2", "R4"], "yes", "review", "单图身份锁；禁止当任意换脸默认"),
    ("SRC-045", "ToTheBeginning/PuLID", "https://github.com/ToTheBeginning/PuLID", "paper-code", "visual-consistency", "stars=3549", ["R2", "R4"], "yes", "review", "身份保真且少破坏原模型行为"),
    ("SRC-046", "cubiq/PuLID_ComfyUI", "https://github.com/cubiq/PuLID_ComfyUI", "tool", "visual-consistency", "stars=910", ["R4"], "yes", "none", "PuLID 本地节点"),
    ("SRC-047", "JackAILab/ConsistentID", "https://github.com/JackAILab/ConsistentID", "paper-code", "visual-consistency", "stars=1026", ["R2"], "yes", "none", "细粒度五官身份"),
    ("SRC-048", "lllyasviel/ControlNet", "https://github.com/lllyasviel/ControlNet", "paper-code", "image-gen", "stars=34114", ["R4"], "yes", "none", "姿态/深度与身份解耦"),
    ("SRC-049", "Comfy-Org/ComfyUI", "https://github.com/Comfy-Org/ComfyUI", "tool", "image-gen", "stars=132559", ["R4"], "yes", "none", "本地图工作流宿主，非产品选型"),
    ("SRC-050", "huggingface/diffusers", "https://github.com/huggingface/diffusers", "tool", "image-gen", "stars=34497", ["R4"], "yes", "none", "扩散管线库"),
    ("SRC-051", "black-forest-labs/flux", "https://github.com/black-forest-labs/flux", "paper-code", "image-gen", "stars=25946", ["R4"], "yes", "none", "开源图像骨干之一"),
    ("SRC-052", "Stability-AI/generative-models", "https://github.com/Stability-AI/generative-models", "paper-code", "image-gen", "stars=27282", ["R4"], "maybe", "none", "SD3/SVD 系列参考"),
    ("SRC-053", "AUTOMATIC1111/stable-diffusion-webui", "https://github.com/AUTOMATIC1111/stable-diffusion-webui", "tool", "image-gen", "stars=164895", ["R4"], "maybe", "review", "高星宿主；扩展生态混杂"),
    ("SRC-054", "kohya-ss/sd-scripts", "https://github.com/kohya-ss/sd-scripts", "tool", "visual-consistency", "stars=7233", ["R2"], "maybe", "none", "角色 LoRA 训练方法，重"),
    ("SRC-055", "cloneofsimo/lora", "https://github.com/cloneofsimo/lora", "paper-code", "visual-consistency", "stars=7556", ["R2"], "maybe", "none", "LoRA 适配原论文实现"),
    ("SRC-056", "HVision-NKU/StoryDiffusion", "https://github.com/HVision-NKU/StoryDiffusion", "paper-code", "continuity", "stars=6456", ["R2", "R4"], "yes", "none", "跨提示一致注意力，故事序列"),
    ("SRC-057", "FireRedTeam/StoryMaker", "https://github.com/FireRedTeam/StoryMaker", "paper-code", "character", "stars=720", ["R2"], "yes", "none", "多角色衣服发型身体整体一致"),
    ("SRC-058", "NVlabs/consistory", "https://github.com/NVlabs/consistory", "paper-code", "continuity", "stars=425", ["R2", "R4"], "yes", "none", "训练无关共享注意力"),
    ("SRC-059", "TencentARC/PhotoMaker", "https://github.com/TencentARC/PhotoMaker", "paper-code", "character", "stars=10088", ["R2"], "maybe", "review", "堆叠 ID；记录已知失败模式"),
    ("SRC-060", "Tencent-Hunyuan/InstantCharacter", "https://github.com/Tencent-Hunyuan/InstantCharacter", "paper-code", "character", "stars=1043", ["R2"], "yes", "none", "单张角色图换姿态换场景"),
    ("SRC-061", "google/dreambooth", "https://github.com/google/dreambooth", "paper-code", "character", "stars=1029", ["R2"], "maybe", "review", "稀有 token 绑定；过重且易被滥用"),
    ("SRC-062", "elevenlabs/elevenlabs-python", "https://github.com/elevenlabs/elevenlabs-python", "tool", "voice", "stars=3093", ["R4"], "yes", "review", "现有 ElevenLabs 叶的 SDK 形状；密钥只租用"),
    ("SRC-063", "QwenLM/Qwen3-TTS", "https://github.com/QwenLM/Qwen3-TTS", "paper-code", "voice", "stars=13300", ["R4"], "yes", "review", "CustomVoice/Design/Clone 三模式；clone 需权利"),
    ("SRC-064", "FunAudioLLM/CosyVoice", "https://github.com/FunAudioLLM/CosyVoice", "paper-code", "voice", "stars=23600", ["R4"], "maybe", "review", "instruct+说话人缓存；非第三 Provider"),
    ("SRC-065", "myshell-ai/OpenVoice", "https://github.com/myshell-ai/OpenVoice", "paper-code", "voice", "stars=37500", ["R2", "R4"], "maybe", "review", "音色与风格解耦；禁止任意克隆默认"),
    ("SRC-066", "coqui-ai/TTS", "https://github.com/coqui-ai/TTS", "tool", "voice", "stars=46000", ["R4"], "no", "review", "历史多说话人参考；许可与组织停更"),
    ("SRC-067", "RVC-Boss/GPT-SoVITS", "https://github.com/RVC-Boss/GPT-SoVITS", "tool", "voice", "stars=61687", ["R4"], "maybe", "review", "高星克隆工具；需同意与权利，非产品叶"),
    ("SRC-068", "RVC-Project/Retrieval-based-Voice-Conversion-WebUI", "https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI", "tool", "voice", "stars=38171", ["R4"], "no", "review", "歌声/说话人转换；默认识别为克隆栈"),
    ("SRC-069", "openai/whisper", "https://github.com/openai/whisper", "tool", "audio", "stars=108901", ["R5"], "yes", "none", "旁白可懂度/字幕校对候选"),
    ("SRC-070", "facebookresearch/demucs", "https://github.com/facebookresearch/demucs", "tool", "audio", "stars=10361", ["R4"], "maybe", "none", "人声/伴奏分轨研究工具"),
    ("SRC-071", "OpenTalker/SadTalker", "https://github.com/OpenTalker/SadTalker", "tool", "audio", "stars=14077", ["R4"], "maybe", "review", "口型相关；需 likeness 权利"),
    ("SRC-072", "Rudrabha/Wav2Lip", "https://github.com/Rudrabha/Wav2Lip", "paper-code", "audio", "stars=13200", ["R4"], "maybe", "review", "音频驱动口型；默认不进解说剧"),
    ("SRC-073", "SWivid/F5-TTS", "https://github.com/SWivid/F5-TTS", "paper-code", "voice", "stars=15200", ["R4"], "maybe", "review", "开源零样本 TTS，非当前 Provider"),
    ("SRC-074", "fishaudio/fish-speech", "https://github.com/fishaudio/fish-speech", "paper-code", "voice", "stars=32700", ["R4"], "no", "review", "研究许可偏严，不作库依赖"),
    ("SRC-075", "2noise/ChatTTS", "https://github.com/2noise/ChatTTS", "tool", "voice", "stars=39800", ["R4"], "no", "none", "对话腔不稳，不适合长旁白"),
    ("SRC-076", "index-tts/index-tts", "https://github.com/index-tts/index-tts", "paper-code", "voice", "stars=23900", ["R4"], "maybe", "review", "中文工业 TTS；权重许可另计"),
    ("SRC-077", "yl4579/StyleTTS2", "https://github.com/yl4579/StyleTTS2", "paper-code", "voice", "stars=6300", ["R2"], "maybe", "none", "风格向量想法可蒸馏"),
    ("SRC-078", "TencentARC/GFPGAN", "https://github.com/TencentARC/GFPGAN", "tool", "image-gen", "stars=37673", ["R4"], "maybe", "none", "脸修复；可能抹平人设细节"),
    ("SRC-079", "lllyasviel/Fooocus", "https://github.com/lllyasviel/Fooocus", "tool", "image-gen", "stars=unverified", ["R4"], "maybe", "none", "简化文生图宿主"),
    ("SRC-080", "wshobson/agents", "https://github.com/wshobson/agents", "collection", "meta-format", "stars=39570", ["R4"], "maybe", "none", "多宿主 skill 包装"),
    ("SRC-081", "github/awesome-copilot", "https://github.com/github/awesome-copilot", "collection", "meta-format", "stars=38901", ["R4"], "maybe", "none", "Copilot 包装对照"),
    ("SRC-082", "PatrickJS/awesome-cursorrules", "https://github.com/PatrickJS/awesome-cursorrules", "collection", "meta-format", "stars=40767", ["R4"], "maybe", "none", "短持久规则 vs 按需 skill"),
    ("SRC-083", "garrytan/gstack", "https://github.com/garrytan/gstack", "collection", "production-planning", "stars=132566", ["R5"], "maybe", "none", "角色分离的评审环"),
    ("SRC-084", "affaan-m/ECC", "https://github.com/affaan-m/ECC", "collection", "production-planning", "stars=256341", ["R4"], "maybe", "review", "巨大工具转储；只挑具名媒体 skill"),
    ("SRC-085", "travisvn/awesome-claude-skills", "https://github.com/travisvn/awesome-claude-skills", "collection", "meta-format", "stars=15033", ["R4"], "maybe", "none", "较小 Claude skill 目录"),
    ("SRC-086", "BehiSecc/awesome-claude-skills", "https://github.com/BehiSecc/awesome-claude-skills", "collection", "meta-format", "stars=10119", ["R4"], "maybe", "none", "含 Media & Content 分区"),
    ("SRC-087", "SkyworkAI/Skywork-Skills storyboard", "https://github.com/SkyworkAI/Skywork-Skills/blob/main/skywork-design/scenarios/storyboard.md", "skill", "continuity", "stars=204", ["R2", "R4"], "yes", "none", "身份描述逐帧复用"),
    ("SRC-088", "linyqh/speclip-skills", "https://github.com/linyqh/speclip-skills", "skill-repo", "story", "stars=107", ["R3"], "maybe", "none", "解说/口播剪辑语法"),
    ("SRC-089", "drasstry/shortdrama-pipeline", "https://github.com/drasstry/shortdrama-pipeline", "tool", "production-planning", "stars=116", ["R4", "R5"], "maybe", "none", "剧本/人设/视频人闸"),
    ("SRC-090", "waooAI/waoowaoo", "https://github.com/waooAI/waoowaoo", "tool", "directing", "stars=14048", ["R4"], "maybe", "review", "代理制片平台；许可非标准"),
    ("SRC-091", "dramaclaw/dramaclaw", "https://github.com/dramaclaw/dramaclaw", "tool", "manga-anime", "stars=5646", ["R4"], "maybe", "none", "漫剧引擎，许可不明"),
    ("SRC-092", "YvonneMovingon/short-drama-skills", "https://github.com/YvonneMovingon/short-drama-skills", "skill-repo", "story", "stars=78", ["R3"], "maybe", "none", "领域贴合的小 SOP"),
    ("SRC-093", "StoryDiffusion paper", "https://arxiv.org/abs/2405.01434", "paper", "continuity", "citations=unverified", ["R2", "R4"], "yes", "none", "Consistent Self-Attention"),
    ("SRC-094", "IP-Adapter paper", "https://arxiv.org/abs/2308.06721", "paper", "image-gen", "citations=unverified", ["R2"], "yes", "none", "图像提示适配器论文"),
    ("SRC-095", "InstantID paper", "https://arxiv.org/abs/2401.07519", "paper", "character", "citations=unverified", ["R2"], "yes", "review", "零样本身份保持"),
    ("SRC-096", "PuLID paper", "https://arxiv.org/html/2404.16022v1", "paper", "character", "citations=unverified", ["R2"], "yes", "none", "对比对齐的 ID 定制"),
    ("SRC-097", "PhotoMaker paper", "https://arxiv.org/abs/2312.04461", "paper", "character", "citations=unverified", ["R2"], "maybe", "none", "堆叠 ID embedding"),
    ("SRC-098", "ConsiStory paper", "https://arxiv.org/abs/2402.03286", "paper", "continuity", "citations=unverified", ["R4"], "yes", "none", "SIGGRAPH 训练无关一致性"),
    ("SRC-099", "StoryMaker paper", "https://arxiv.org/abs/2409.12576", "paper", "character", "citations=unverified", ["R2"], "yes", "none", "整体多角色一致性"),
    ("SRC-100", "1Prompt1Story paper", "https://arxiv.org/abs/2501.13554", "paper", "continuity", "citations=unverified", ["R3"], "yes", "none", "故事提示并入同一上下文"),
    ("SRC-101", "Video Storyboarding paper", "https://arxiv.org/abs/2412.07750", "paper", "continuity", "citations=unverified", ["R4"], "yes", "none", "多镜 T2V 角色一致"),
    ("SRC-102", "DreamBooth paper", "https://arxiv.org/abs/2208.12242", "paper", "character", "citations=unverified", ["R2"], "maybe", "review", "主体微调经典方法"),
    ("SRC-103", "CosyVoice 2 paper", "https://arxiv.org/abs/2412.10117", "paper", "voice", "citations=unverified", ["R4"], "maybe", "none", "流式+instruct 统一"),
    ("SRC-104", "StyleTTS2 paper", "https://arxiv.org/abs/2306.07691", "paper", "voice", "citations=unverified", ["R2"], "maybe", "none", "风格潜变量"),
    ("SRC-105", "Linda Seger The Art of Adaptation", "https://lindaseger.com/books-3/art-of-adaptation/", "book", "story", "canonical-book", ["R1"], "yes", "none", "改编是第二原创，思想变动作或正当旁白"),
    ("SRC-106", "StudioBinder how to adapt a book", "https://www.studiobinder.com/blog/how-to-adapt-a-book-into-a-screenplay/", "article", "story", "unverified-views", ["R1"], "yes", "none", "三遍阅读与可见性过滤"),
    ("SRC-107", "Save the Cat official beat sheet", "https://savethecat.com/tips-and-tactics/the-blake-snyder-beat-sheet-the-bs2", "article", "story", "page-signal=28948", ["R1", "R3"], "yes", "none", "15 beats 可按百分比缩放到 90s"),
    ("SRC-108", "Save the Cat how to write a screenplay", "https://savethecat.com/how-to-write-a-screenplay", "article", "story", "canonical-method", ["R1"], "yes", "none", "Opening Image 到 Final Image 的官方说明"),
    ("SRC-109", "Save the Cat Wikipedia", "https://en.wikipedia.org/wiki/Save_the_Cat", "article", "story", "encyclopedia", ["R1"], "yes", "none", "方法谱系与批评"),
    ("SRC-110", "Pixar 22 rules recap ScreenCraft", "https://screencraft.org/blog/pixars-22-rules-storytelling-with-movie-stills/", "article", "story", "canonical-essay", ["R1", "R3"], "yes", "none", "简化、先结局、因果链"),
    ("SRC-111", "Emma Coats Pixar rules archive", "https://archive.internationalpsychoanalysis.net/2012/06/20/pixars-22-rules-for-storytelling/", "article", "story", "canonical-essay", ["R1"], "yes", "none", "2011 推文法则较早转载"),
    ("SRC-112", "Kenn Adams story spine / Pixar rule 4", "https://www.aerogramme.com.au/2013/03/pixars-22-rules-of-storytelling/", "article", "story", "unverified-views", ["R1"], "maybe", "none", "Once/Every day/One day 骨架"),
    ("SRC-113", "Syd Field paradigm worksheet", "https://sydfield.com/syd_resources/the-paradigm-worksheet/", "article", "story", "canonical-method", ["R1"], "yes", "none", "三幕与情节点可映射十集而非塞进 15 秒"),
    ("SRC-114", "Robert McKee Story webinar hub", "https://mckeestory.com/webinars/story/", "article", "story", "canonical-book", ["R1", "R5"], "yes", "none", "场景必须翻转价值；解说不能偷懒解释"),
    ("SRC-115", "Robert McKee Dialogue book", "https://mckeestory.com/books/dialogue/", "book", "character", "canonical-book", ["R2", "R3"], "yes", "none", "对白是战术；解说是叙述者行动"),
    ("SRC-116", "Dan Harmon Story Circle", "https://channel101.fandom.com/wiki/Story_Structure_101:_Super_Basic_Shit", "essay", "story", "canonical-essay", ["R3"], "yes", "review", "为短集设计的八步圆；站点其他短片或 NSFW"),
    ("SRC-117", "Hero with a Thousand Faces Wikipedia", "https://en.wikipedia.org/wiki/The_Hero_with_a_Thousand_Faces", "article", "story", "encyclopedia", ["R1"], "yes", "none", "只作季弧祖先，不往 90s 贴 17 阶段"),
    ("SRC-118", "Writer's Journey Wikipedia", "https://en.wikipedia.org/wiki/The_Writer%27s_Journey:_Mythic_Structure_for_Writers", "article", "character", "encyclopedia", ["R2"], "yes", "none", "原型是功能不是服装"),
    ("SRC-119", "Scott McCloud Understanding Comics site", "https://scottmccloud.com/2-print/1-uc", "book", "manga-anime", "canonical-book", ["R3"], "yes", "none", "gutter 闭合与图文组合"),
    ("SRC-120", "Understanding Comics Wikipedia", "https://en.wikipedia.org/wiki/Understanding_Comics", "article", "manga-anime", "encyclopedia", ["R3"], "yes", "none", "顺序艺术定义"),
    ("SRC-121", "Panel-to-panel notes", "https://gordonbrander.com/notes/panel-to-panel/", "article", "manga-anime", "unverified-views", ["R3"], "yes", "none", "六种转场可操作摘要"),
    ("SRC-122", "Comic panel types guide", "https://benargon.com/comic-panel-tools-techniques/", "article", "manga-anime", "unverified-views", ["R3"], "yes", "none", "格、gutter、转场教学"),
    ("SRC-123", "Neil Cohn Visual Language Lab", "https://www.visuallanguagelab.com/", "article", "manga-anime", "academic", ["R3"], "yes", "none", "视觉语言语法，不默认好莱坞覆盖"),
    ("SRC-124", "VLRC corpus", "https://www.visuallanguagelab.com/vlrc", "article", "manga-anime", "academic", ["R3"], "yes", "none", "跨文化分格标注"),
    ("SRC-125", "Cohn comics page layout myths", "https://www.visuallanguagelab.com/2016/08/dispelling-myths-about-comics-page-layout.html", "article", "manga-anime", "academic", ["R3"], "yes", "none", "Z 路径并非万能"),
    ("SRC-126", "Construction of manga panels ImageTexT", "https://imagetextjournal.com/the-construction-of-panels-koma-in-manga/", "article", "manga-anime", "academic", ["R3"], "yes", "none", "コマ割り控制时间"),
    ("SRC-127", "180-degree rule Wikipedia", "https://en.wikipedia.org/wiki/180-degree_rule", "article", "cinematography", "encyclopedia", ["R3"], "yes", "none", "轴线与左右关系"),
    ("SRC-128", "30-degree rule Wikipedia", "https://en.wikipedia.org/wiki/30-degree_rule", "article", "cinematography", "encyclopedia", ["R4"], "yes", "none", "同对象跳切阈值"),
    ("SRC-129", "Continuity editing Wikipedia", "https://en.wikipedia.org/wiki/Continuity_editing", "article", "editing", "encyclopedia", ["R3", "R4"], "yes", "none", "隐形剪辑语法"),
    ("SRC-130", "Learn About Film 180 rule", "https://learnaboutfilm.com/film-language/sequence/180-degree-rule/", "article", "cinematography", "film-school", ["R3"], "yes", "none", "视线空间与朝向"),
    ("SRC-131", "Learn About Film continuity sequence", "https://learnaboutfilm.com/film-language/sequence/", "article", "directing", "film-school", ["R3"], "yes", "none", "master/singles 覆盖配方"),
    ("SRC-132", "Filmmakers Academy eyeline match", "https://www.filmmakersacademy.com/glossary/eyeline-match/", "article", "editing", "film-school", ["R3"], "yes", "none", "看向切到被看物"),
    ("SRC-133", "Wolfcrow 15 continuity rules", "https://wolfcrow.com/the-15-essential-rules-of-film-continuity/", "article", "continuity", "practitioner", ["R3", "R6"], "yes", "none", "相机连续 vs 制作连续"),
    ("SRC-134", "Descript continuity editing", "https://www.descript.com/blog/article/the-importance-of-continuity-editing-in-film-and-video", "article", "editing", "unverified-views", ["R4"], "yes", "none", "动作峰值上切"),
    ("SRC-135", "StudioBinder camera shots guide", "https://www.studiobinder.com/blog/ultimate-guide-to-camera-shots-framing-angles/", "article", "cinematography", "high-visibility-blog", ["R3"], "yes", "none", "景别/角度/运动三轴词表"),
    ("SRC-136", "StudioBinder blocking", "https://www.studiobinder.com/blog/what-is-blocking-in-film-definition/", "article", "directing", "high-visibility-blog", ["R3"], "yes", "none", "先平面后镜头"),
    ("SRC-137", "StudioBinder coverage", "https://www.studiobinder.com/blog/what-is-coverage-in-film-definition/", "article", "directing", "high-visibility-blog", ["R3"], "yes", "none", "有界覆盖包"),
    ("SRC-138", "StudioBinder shot list", "https://www.studiobinder.com/shot-list-storyboard/", "article", "storyboard", "high-visibility-blog", ["R3"], "yes", "none", "镜号表不是分镜也不是日程"),
    ("SRC-139", "StudioBinder animation shot list", "https://www.studiobinder.com/templates/shot-list/animation-shot-list-template/", "article", "storyboard", "high-visibility-blog", ["R3"], "yes", "none", "动画先板后表"),
    ("SRC-140", "StudioBinder animatic template", "https://www.studiobinder.com/templates/storyboards/storyboard-animatic-template/", "article", "storyboard", "high-visibility-blog", ["R3", "R4"], "yes", "none", "板+时长+VO 先于付费生成"),
    ("SRC-141", "Toon Boom storyboard structure", "https://docs.toonboom.com/help/storyboard-pro-25/storyboard/structure/about-storyboard-structure.html", "docs", "storyboard", "industry-docs", ["R3"], "yes", "none", "panel⊂scene⊂sequence 命名"),
    ("SRC-142", "Toon Boom Storyboard Pro product", "https://www.toonboom.com/products/storyboard-pro", "docs", "storyboard", "industry-docs", ["R3"], "yes", "none", "稳定 panel ID 跨部门"),
    ("SRC-143", "Toon Boom layout export", "https://docs.toonboom.com/help/storyboard-pro-25/storyboard/reference/dialogs/export-layout-window.html", "docs", "cinematography", "industry-docs", ["R4"], "yes", "none", "layout 是带相机的生产图"),
    ("SRC-144", "Toon Boom asset management", "http://learn.toonboom.com/modules/project-creation2/topic/about-asset-management1", "docs", "production-planning", "industry-docs", ["R2"], "yes", "none", "设计库权威，场次消费"),
    ("SRC-145", "EBU R128", "https://tech.ebu.ch/publications/r128", "standard", "audio", "official-standard", ["R4"], "yes", "none", "节目响度 −23 LUFS 权威"),
    ("SRC-146", "EBU R128 PDF", "https://tech.ebu.ch/docs/r/r128.pdf", "standard", "audio", "official-standard", ["R4"], "yes", "none", "R128 正文"),
    ("SRC-147", "EBU R128 s1 short-form", "https://tech.ebu.ch/publications/r128s1", "standard", "audio", "official-standard", ["R4"], "yes", "none", "短内容响度补充"),
    ("SRC-148", "EBU R128 s2 streaming", "https://tech.ebu.ch/docs/r/r128s2.pdf", "standard", "audio", "official-standard", ["R4"], "yes", "none", "流媒体/手机可到 −16"),
    ("SRC-149", "EBU Tech 3343", "https://tech.ebu.ch/publications/tech3343", "standard", "audio", "official-standard", ["R4"], "yes", "none", "制作指南含短制与对白比"),
    ("SRC-150", "EBU Tech 3342 LRA", "https://tech.ebu.ch/publications/tech3342", "standard", "audio", "official-standard", ["R4"], "yes", "none", "响度范围描述符"),
    ("SRC-151", "ITU-R BS.1770", "https://www.itu.int/rec/R-REC-BS.1770", "standard", "audio", "official-standard", ["R4", "R5"], "yes", "none", "LUFS/真峰值算法"),
    ("SRC-152", "Apple Podcasts audio requirements", "https://podcasters.apple.com/support/893-audio-requirements", "standard", "audio", "official-docs", ["R4"], "yes", "none", "口语 −16 LKFS 候选"),
    ("SRC-153", "ElevenLabs TTS best practices", "https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices", "docs", "voice", "official-docs", ["R4"], "yes", "review", "声音>模型>设置；示例含 key 头勿抄"),
    ("SRC-154", "ElevenLabs text to dialogue", "https://elevenlabs.io/docs/overview/capabilities/text-to-dialogue", "docs", "voice", "official-docs", ["R2", "R4"], "yes", "review", "多角色分 turn，需切块"),
    ("SRC-155", "ElevenLabs voice design", "https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/voice-design", "docs", "voice", "official-docs", ["R2"], "maybe", "review", "预览后冻结 voice_id；产品已 defer remix"),
    ("SRC-156", "Qwen-TTS blog", "https://qwenlm.github.io/blog/qwen-tts", "docs", "voice", "official-docs", ["R4"], "yes", "none", "托管 Qwen 声线族"),
    ("SRC-157", "Alibaba Qwen-TTS help", "https://www.alibabacloud.com/help/en/model-studio/qwen-tts-realtime", "docs", "voice", "official-docs", ["R4"], "yes", "review", "区域 endpoint 与租用密钥"),
    ("SRC-158", "invideo novel to AI micro-drama", "https://invideo.io/blog/novel-to-ai-micro-drama/", "article", "story", "unverified-views", ["R1"], "yes", "none", "一章可拆可并；可见动作过滤器"),
    ("SRC-159", "BU short-form serial drama", "https://www.bu.edu/com/research/the-short-form-scripted-serial-drama/", "article", "story", "academic", ["R1"], "yes", "none", "短制连续剧诗学"),
    ("SRC-160", "one-page micro short", "https://scriptandpad.com/how-to-write-a-one-page-short-film/", "article", "story", "unverified-views", ["R3"], "yes", "none", "一页三拍模型"),
    ("SRC-161", "Sundance Collab micro-series course note", "https://www.instagram.com/sundancecollab/p/DctsQ8XoFu7/", "article", "story", "unverified-views", ["R1", "R3"], "maybe", "none", "60–120s 竖屏剧集写作课宣传"),
    ("SRC-162", "LivingWriter novel to screenplay", "https://livingwriter.com/blog/how-to-turn-a-novel-into-a-screenplay-4-simple-steps/", "article", "story", "unverified-views", ["R1"], "maybe", "none", "三幕切书实用步骤"),
    ("SRC-163", "Shore Scripts screenplay to podcast", "https://www.shorescripts.com/how-to-adapt-my-screenplay-into-a-podcast/", "article", "voice", "unverified-views", ["R3"], "yes", "none", "只用声音重述；旁白正当化"),
    ("SRC-164", "广电译配角色声线一致转载", "https://news.qq.com/rain/a/20220526A03G0Z00", "article", "voice", "unverified-views", ["R2"], "yes", "none", "一角一声、声线对比"),
    ("SRC-165", "有声漫画配音方向", "https://aipiaxi.com/article-detail/995851", "article", "voice", "unverified-views", ["R2", "R3"], "yes", "none", "有声漫补对象感、先定人设"),
    ("SRC-166", "旁白与角色分轨", "https://www.sohu.com/a/957202353_122541036", "article", "voice", "unverified-views", ["R4"], "yes", "review", "方法有用；忽略工具推销"),
    ("SRC-167", "影视配音实用教程摘要", "https://yueyin.zhipianbang.com/news/detail-54897.html", "article", "voice", "unverified-views", ["R3"], "yes", "none", "解说体裁 vs 角色通过线"),
    ("SRC-168", "ComfyUI consistent characters guide", "https://www.media.io/image-tips/comfyui-consistent-characters.html", "article", "visual-consistency", "unverified-views", ["R2", "R4"], "yes", "none", "IP-Adapter/PuLID/LoRA 分层选用"),
    ("SRC-169", "PuLID vs InstantID vs FaceID 2026", "https://aiofm.info/en/guides/pulid-vs-instantid-vs-faceid", "article", "visual-consistency", "unverified-views", ["R4"], "yes", "none", "按变化幅度选最轻身份法"),
    ("SRC-170", "danjdewhurst/story-skills revision-continuity", "https://github.com/danjdewhurst/story-skills/blob/main/skills/revision-continuity/SKILL.md", "skill", "continuity", "unverified-stars", ["R3", "R6"], "yes", "none", "知识/死亡顺序/承诺检查"),
    ("SRC-171", "danjdewhurst story-init", "https://github.com/danjdewhurst/story-skills/blob/main/skills/story-init/SKILL.md", "skill", "canon", "unverified-stars", ["R1", "R2"], "yes", "none", "bible 与注册表交叉引用"),
    ("SRC-172", "fcsouza character-design-narrative", "https://github.com/fcsouza/agent-skills/blob/main/skills/character-design-narrative/SKILL.md", "skill", "character", "unverified-stars", ["R2"], "yes", "none", "character bible 结构"),
    ("SRC-173", "theneoai ai-production-designer", "https://github.com/theneoai/awesome-skills/blob/main/skills/persona/media/ai-production-designer/SKILL.md", "skill", "worldbuilding", "unverified-stars", ["R2"], "yes", "none", "场景规则书与禁忌表"),
    ("SRC-174", "RainLib scriptwriter-skill", "https://github.com/RainLib/AI-Storyboard/blob/main/.claude/skills/scriptwriter-skill/SKILL.md", "skill", "story", "stars=49-repo", ["R3"], "yes", "none", "视觉优先与系列连续性清单"),
    ("SRC-175", "Adityaraj0421 cinematic director plugin", "https://github.com/Adityaraj0421/ai-cinematic-video-director-claude-skill", "skill-repo", "directing", "stars=2", ["R4"], "maybe", "none", "先静帧、一镜一动作、锁定句不改写"),
    ("SRC-176", "smkrv/character-bible", "https://github.com/smkrv/character-bible", "skill-repo", "character", "stars=0", ["R2"], "maybe", "review", "事实/推断分栏好；星为零且可触发付费生成"),
    ("SRC-177", "ACX audiobook requirements summary", "https://www.acx.com/help/acx-audio-submission-requirements/201456300", "standard", "audio", "official-docs", ["R4"], "maybe", "none", "头尾静音与底噪；勿用 RMS 替代 LUFS"),
    ("SRC-178", "agentskills.io", "https://agentskills.io", "docs", "meta-format", "official-docs", ["R4"], "maybe", "none", "Skill 标准站点"),
    ("SRC-179", "Midjourney character reference docs", "https://docs.midjourney.com/hc/en-us/articles/32106164419213-Character-Reference-cref", "docs", "visual-consistency", "official-docs", ["R2", "R4"], "maybe", "none", "cref 作为闭源身份锁对照；非产品依赖"),
    ("SRC-180", "ffmpeg loudnorm filter docs", "https://ffmpeg.org/ffmpeg-filters.html#loudnorm", "docs", "audio", "official-docs", ["R4", "R5"], "yes", "none", "本地响度探针候选，非产品选型"),
    ("SRC-181", "facebookresearch/audiocraft", "https://github.com/facebookresearch/audiocraft", "paper-code", "music", "stars=23620", ["R4"], "yes", "review", "MusicGen/AudioGen 方法；权重多为 NC，不作产品 Provider"),
    ("SRC-182", "haoheliu/AudioLDM", "https://github.com/haoheliu/AudioLDM", "paper-code", "ambience", "stars=2907", ["R4"], "yes", "review", "文本生成环境/音效；非发布默认"),
    ("SRC-183", "haoheliu/AudioLDM2", "https://github.com/haoheliu/AudioLDM2", "paper-code", "ambience", "stars=2642", ["R4"], "yes", "review", "更完整的 TTA/TTM；许可需单独审"),
    ("SRC-184", "Stability-AI/stable-audio-tools", "https://github.com/Stability-AI/stable-audio-tools", "tool", "music", "stars=3856", ["R4"], "yes", "review", "Stable Audio 训练/推理工具；样本与音效设计"),
    ("SRC-185", "librosa/librosa", "https://github.com/librosa/librosa", "tool", "audio", "stars=8600", ["R4"], "maybe", "none", "分析/切片循环床的本地库，非生成器"),
    ("SRC-186", "MTG/essentia", "https://github.com/MTG/essentia", "tool", "music", "stars=3718", ["R4"], "maybe", "none", "音乐信息检索，可检主题/能量而非听感验收"),
    ("SRC-187", "LCAV/pyroomacoustics", "https://github.com/LCAV/pyroomacoustics", "tool", "ambience", "stars=1937", ["R4"], "maybe", "none", "房间声学模拟；diegetic 空间感方法"),
    ("SRC-188", "BinWang28/audio-ai-hub", "https://github.com/BinWang28/audio-ai-hub", "collection", "music", "stars=953", ["R4"], "maybe", "none", "音乐/环境生成论文与模型索引"),
    ("SRC-189", "Diegetic music Wikipedia", "https://en.wikipedia.org/wiki/Diegetic_music", "article", "music", "encyclopedia", ["R2", "R4"], "yes", "none", "角色能听到 vs 观众轨配乐"),
    ("SRC-190", "Diegesis Wikipedia", "https://en.wikipedia.org/wiki/Diegesis", "article", "music", "encyclopedia", ["R3"], "yes", "none", "叙事内外声音的总定义"),
    ("SRC-191", "BBC Maestro diegetic vs non-diegetic", "https://www.bbcmaestro.com/blog/diegetic-vs-non-diegetic-sound", "article", "ambience", "unverified-views", ["R3", "R4"], "yes", "none", "环境/对白/score 的可听边界"),
    ("SRC-192", "Foley filmmaking Wikipedia", "https://en.wikipedia.org/wiki/Foley_(filmmaking)", "article", "ambience", "encyclopedia", ["R4"], "yes", "none", "拟音对齐可见动作"),
    ("SRC-193", "Room tone Wikipedia", "https://en.wikipedia.org/wiki/Room_tone", "article", "ambience", "encyclopedia", ["R2", "R4"], "yes", "none", "地点底噪连续性"),
    ("SRC-194", "MusicGen paper", "https://arxiv.org/abs/2306.05284", "paper", "music", "citations=unverified", ["R4"], "yes", "review", "可控文本配乐；商用受权重许可限制"),
    ("SRC-195", "AudioGen paper", "https://arxiv.org/abs/2209.15352", "paper", "ambience", "citations=unverified", ["R4"], "yes", "review", "文本引导环境声生成"),
    ("SRC-196", "Freesound", "https://freesound.org/", "docs", "ambience", "canonical-library", ["R4"], "yes", "review", "CC 环境/拟音库；逐条许可不是一刀免费"),
    ("SRC-197", "BBC Sound Effects Rewind", "https://sound-effects.bbcrewind.co.uk/", "docs", "ambience", "official-library", ["R4"], "yes", "review", "BBC 音效库；遵守其非商用/署名条款"),
    ("SRC-198", "Incompetech royalty-free music", "https://incompetech.com/music/royalty-free/", "docs", "music", "canonical-library", ["R2", "R4"], "yes", "review", "CC-BY 音乐床常见来源；必须署名且气质要对片种"),
    ("SRC-199", "video-shotcraft sound-design notes", "https://github.com/Vincentwei1021/video-shotcraft/blob/main/references/sound-design.md", "skill", "music", "stars=8076-repo", ["R4"], "yes", "none", "先锁画面再铺 BGM 再钉 SFX；禁游戏 UI 音色"),
    ("SRC-200", "guoyww/AnimateDiff", "https://github.com/guoyww/AnimateDiff", "paper-code", "manga-anime", "stars=12241", ["R4"], "yes", "review", "图生运动方法证据；不作产品动画 Provider，一镜一动作"),
]


def main() -> None:
    seen_urls = set()
    entries = []
    for item in RAW:
        ident, title, url, typ, category, quality, r_alignment, include, security, why = item
        if url in seen_urls:
            raise SystemExit(f"duplicate url {url}")
        seen_urls.add(url)
        entries.append(
            {
                "id": ident,
                "title": title,
                "url": url,
                "type": typ,
                "category": category,
                "quality": quality,
                "r_alignment": r_alignment,
                "include": include,
                "security": security,
                "why": why,
            }
        )
    if len(entries) > 200:
        raise SystemExit(f"too many entries {len(entries)}")
    payload = {
        "schema_version": 1,
        "ticket": "https://github.com/incentlie-design/narrated-drama/issues/112",
        "skills_baseline": "5bfe09d6073207d76a362977f1c38d93dfd79198",
        "quality_observed_at": "2026-09-12",
        "note": "Index of public sources. Inclusion is not a callable Skill and not a product Provider choice. Star counts from GitHub API or agent snapshots on 2026-09-12; unverified where marked.",
        "entries": entries,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    by_cat: dict[str, list] = {}
    for entry in entries:
        by_cat.setdefault(entry["category"], []).append(entry)
    lines = [
        "# Content source index",
        "",
        "Ticket: https://github.com/incentlie-design/narrated-drama/issues/112",
        "",
        f"机器可读副本：[index.json](index.json)（{len(entries)} 条，上限 200）。",
        "质量数字能核到的写在 `quality`；核不到标 `unverified`。",
        "`include=yes` 只表示方法值得蒸馏，不是拷贝授权。",
        "",
        "| include | count |",
        "| --- | --- |",
    ]
    for key in ("yes", "maybe", "no"):
        lines.append(f"| {key} | {sum(1 for e in entries if e['include'] == key)} |")
    lines.append("")
    for category in sorted(by_cat):
        lines.append(f"## {category}")
        lines.append("")
        lines.append("| ID | Title | Type | Quality | R | Include | Security | Why |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for entry in by_cat[category]:
            r = ",".join(entry["r_alignment"])
            title = f"[{entry['title']}]({entry['url']})"
            lines.append(
                f"| {entry['id']} | {title} | {entry['type']} | {entry['quality']} | {r} | {entry['include']} | {entry['security']} | {entry['why']} |"
            )
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(entries)} entries")


if __name__ == "__main__":
    main()
