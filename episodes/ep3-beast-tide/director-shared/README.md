# EP3 — MiniMax H3 Director Shared Params

Target: the latest default-branch revision of [AIMixer/ComfyUI_MiniMaxH3_Director](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director), re-fetched and verified on 2026-10-13: commit `4c6245e518dd8a494f3afc4f3cccd53f22d82d10` (upstream commit time 18:19:34, UTC+08:00). The user will install the latest version. This recorded commit is the reproducible baseline; later upstream changes require another check of import and merge behavior.

## Confirmed behavior

- In **r2v**, enable **Common/Shared Params**. The backend prepends the common prompt to each group prompt, separated by a blank line. It does not parse or deduplicate sections.
- Reference images, audio and videos merge by slot. A local asset in the same slot overrides the shared one. Additional local images keep their higher slot numbers; do not restart numbering at Picture 1.
- Collapsing the shared panel does not disable it. The enable flag determines whether it applies.
- In mixed mode, r2v and t2v shared blocks are separate; i2v/fl2v do not inherit those shared prompts.
- Shared text is repeated in each generation request. This is not persistent model memory or guaranteed visual continuity.

Sources: [README_EN reference groups](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director/blob/4c6245e518dd8a494f3afc4f3cccd53f22d82d10/README_EN.md#reference-groups-r2v--short-guide), [prompt concatenation and reference merge](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director/blob/4c6245e518dd8a494f3afc4f3cccd53f22d82d10/director/plan.py#L202), [generation-plan use](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director/blob/4c6245e518dd8a494f3afc4f3cccd53f22d82d10/director/gen_timeline.py#L543).

## EP3 setup

1. Select **Reference to Video (r2v)**, using the compatible **ref2va** model and audio VAE.
2. Enable Shared Params and attach the four fixed slots listed in [REFERENCE-MAP.md](REFERENCE-MAP.md).
3. Paste [common-prompt.txt](common-prompt.txt) once in Shared Params.
4. Paste the corresponding file from `groups/` into each group. Local definitions continue the shared subject_definitions section.
5. Attach the local images in REFERENCE-MAP.md, starting at Picture 5. Do not overwrite slots 1–4.

The complete `../prompts/` files now use exactly the same image numbering as the merged shared version. They are an alternative for Shared Params OFF; never append them after the common prompt.

## Timing and rendering limits

The repository documents a **17k+5 frame grid** and gives 5 seconds as 124 frames at 24 fps. Nominal seconds therefore need verification against the actual emitted frames. The 75-second manifest is an editorial target. Its 25-step default sampler configuration is not evidence for 4-step Turbo settings; keep the user's proven LoRA workflow configuration.

No ComfyUI render was performed. Prompt concatenation, field order, reference resolution and local-slot overrides were checked against the reviewed source helpers. Static art still requires continuity review for perspective, equipment side, bridge damage and projected-shield state.

Director also supports `.mmxpack.zip` import/export. This folder and its manifest are manual setup materials, not an importable pack or node workflow. No existing Director timeline has been modified.
