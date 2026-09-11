# Content catalog security screen

Ticket: https://github.com/incentlie-design/narrated-drama/issues/112

Probe sources are **untrusted data**. Inclusion in `index.json` does not authorize
execution, install, paid calls or copying their prompts into production.

## Always exclude from callable Skills

| Class | Why | Index handling |
| --- | --- | --- |
| Jailbreak / “ignore previous instructions” | Treats untrusted text as authority | `security=exclude`, `include=no` |
| Credential harvest, `.env` dumps, key in examples | Secrets must not enter Git | quote the *pattern*, never the secret |
| Exploit / malware / attack PoC | Out of content scope | exclude |
| Sexual content involving minors | Hard stop | exclude; do not summarize |
| Voice-clone “any speaker from 3 seconds” as a default | Biometric-like; rights/consent missing | method may be `review`; Skill default is freeze a licensed `voice_id` |
| Lip-sync of real people without rights | Deepfake-adjacent | `review`; Skill requires documented likeness rights |
| “Retry the paid API on timeout” | Double spend | exclude that advice |
| Unverified binary / auto-download weights with no license | Supply chain | `review` or `exclude` |

## Always keep in Skills

- Exact refs, fail-closed, named reviewer ≠ author.
- Duration from actual bytes.
- Provider-neutral profiles; product owns Provider pick.
- License: distill methods, cite URL, do not paste chapters.

## Quality bar for the index

Prefer: GitHub stars ≥200 **or** official standards **or** canonical craft texts
(McCloud, EBU, StudioBinder, Save the Cat official, widely cited adaptation essays).

Lower-star Skill repos may be listed when they uniquely document a method we need;
mark `quality` honestly (`stars=N` or `unverified`). Do not invent counts.

## Music / ambience rights

Callable music and ambience Skills must:

- record license class (`licensed-library` / `cc-with-attribution` / `original-commission` / `generated-research-only`);
- not treat Creative Commons as unconditional commercial use;
- not treat MusicGen/Stable Audio **weights** (often NC/research) as a product Provider or release bed;
- not strip copyrighted film/TV stems as “reference ambience”.

## RVC / clone / lip-sync

High-star engineering (GPT-SoVITS, RVC, Wav2Lip, SadTalker, OpenVoice) is indexed
as **method evidence**, not as a product Provider. Callable Skills must say:

- do not add a third Voice Provider;
- do not clone a real person without written rights;
- do not treat lip-sync of a living person as default 解说剧 pipeline.
