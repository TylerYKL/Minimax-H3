# Side-view shield impact — skill-guided test

Purpose: test a visible causal chain: palm approach → shield contact → shield compression → elbow/shoulder recoil → initial leftward displacement. This is a new reference/prompt setup, not a controlled measurement of skill effectiveness. H3 rendering remains to be performed on the user's PC.

## Run

1. Import `side-impact-workflow.json` into MiniMax H3 Director.
2. Upload `frames/impact-start.png` and `frames/impact-end.png` into the first and last image slots; verify thumbnails.
3. Use the existing FL2VA model, 25 steps, CFG 1, res_multistep / simple, video shift 12, audio shift 3, seed 888, 864×480, 24fps. Turbo and Combat LoRA remain bypassed. Output is silent.
4. The requested UI duration is **2 seconds**, aligning to **56 frames / 2.333 seconds** with the Director rule verified in the preceding tests. Keep the UI request at 2; the prompt's 2.33 is effective output duration.
5. Render this single shot first. Check contact and recoil before tuning generation speed or creating additional shots.

## What changed

- A single lateral camera makes the approach gap, shield plane, and body displacement visible together.
- The attack starts close to the shield, reducing travel needed before contact.
- The prompt uses the H3 FL2VA alignment instruction and three-field format.
- Force is transmitted through palm, shield, right forearm, shoulder, torso and hips.
- Visual prompt text uses affirmative descriptions. The negative-prompt field is empty.

This shot starts after the shield is deployed. Shield deployment and the previous sword-to-shield transition are separate editorial beats. Long-distance knockback, overhead angle, and building collapse belong to following shots. Endpoints guide composition and pose; exact contact timing and intermediate anatomy still need render review.

## Skills used

- `minimax-h3-combat`: physical causality, scale, equipment and reaction continuity.
- `h3-prompt-writing`: FL2VA formatting and frame alignment.
- `fight-prompt-director/references/camera-guide.md`: lateral contact view and fixed screen direction.

These are copies available in the cloud workspace, not verified installations on the local PC. The user’s positive-only prompt preference overrides negative wording in skill examples.

## Review checklist

- Palm visibly closes the opening gap and meets the shield surface.
- Localized shield compression and an expanding ripple follow contact.
- Right elbow and shoulder react before the torso moves left.
- Leftward displacement is clear against stable background buildings.
- Hero armor, right-arm shield attachment, limbs and hand topology remain coherent.

A successful result here is a readable impact source shot. Brief editorial impact frames and fast knockback cuts can be added after this shot passes review.
