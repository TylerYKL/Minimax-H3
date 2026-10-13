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
2. Enable Shared Params. Upload `../references/A-team.png` as **Picture 1**, and `../references/B-scale-final.png` as **Picture 2**.
3. Paste [common-prompt.txt](common-prompt.txt) into the shared prompt field. It supplies `subject_definitions` and the fixed Subject 1–5 identities.
4. For each group, paste its file from [groups/](groups/). These are prompt tails, not standalone full requests. Any leading definitions continue the shared `subject_definitions` section before the group's `summary`.
5. Attach only the local assets shown below. Keep Picture 1 and Picture 2 clear in the group, so the shared identities are not overwritten.

|Group|Target duration|Local Picture 3|Local Picture 4|
|---|---:|---|---|
|01|6s|—|—|
|02|4s|—|—|
|03|6s|C-blade-contact|—|
|04|4s|—|—|
|05|8s|—|—|
|06|8s|C-blade-contact|—|
|07|7s|C-blade-contact|—|
|08|6s|D-tail-contact|—|
|09|4s|D-tail-contact|—|
|10|6s|E-barrier|—|
|11|6s|E-barrier|—|
|12|10s|F-shield-fracture|E-barrier|

Local Picture 3 intentionally varies by group and is defined in that group's text. Subject identities stay fixed. Subject 6 is the dome; Subject 7 is the final energy fracture. Early groups explicitly keep the shared titan out of the visible cast.

This supersedes the earlier suggestion to share all six action/state images. Keeping damage and dome references local reduces conflicting visual states; it is a production choice, not a Director limitation.

Do not paste the original complete prompts from `../prompts/` after this common prompt: that would duplicate `subject_definitions` and use incompatible per-clip Picture numbers. The original standalone prompts remain available as a separate mode with shared params disabled.

## Timing and rendering limits

The repository documents a **17k+5 frame grid** and gives 5 seconds as 124 frames at 24 fps. Nominal seconds therefore need verification against the actual emitted frames. The 75-second manifest is an editorial target. Its 25-step default sampler configuration is not evidence for 4-step Turbo settings; keep the user's proven LoRA workflow configuration.

No ComfyUI render was performed. Prompt concatenation, field order, reference resolution and local-slot overrides were checked against the reviewed source helpers. Static art still requires continuity review for perspective, equipment side, bridge damage and projected-shield state.

Director also supports `.mmxpack.zip` import/export. This folder and its manifest are manual setup materials, not an importable pack or node workflow. No existing Director timeline has been modified.
