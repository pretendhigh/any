---
name: codex-pet-from-character
description: Use when a user wants to create a Codex custom pet from a character image, avatar, mascot, anime reference, OC, game character, or asks for "codex pet", "桌宠", "宠物", "根据人物形象生成 pet", including requests to customize actions, style, outfit, failed state, or animation rows.
---

# Codex Pet From Character

Create a Codex-compatible animated pet from one or more character reference images. Default to the Any project style unless the user overrides it: cute anime chibi, JK-friendly proportions when suitable, pixel-art-adjacent, thick dark outline, flat cel shading, readable at `192x208`.

## Output Contract

Produce a package:

```text
<pet-id>/
├── pet.json
└── spritesheet.webp
```

Atlas requirements:
- `1536x1872` WebP or PNG with alpha.
- 8 columns x 9 rows.
- Cell size `192x208`.
- Transparent background and transparent unused cells.

`pet.json` shape:

```json
{
  "id": "pet-id",
  "displayName": "Pet Name",
  "description": "One short sentence.",
  "spritesheetPath": "spritesheet.webp",
  "kind": "person"
}
```

## Default Rows

1. `idle` - sleepy/drowsy nodding idle.
2. `running-right` - 8-frame rightward walk/run with alternating knees and feet.
3. `running-left` - 8-frame leftward walk/run; mirror right row only when there is no text, logo, handed prop, or asymmetric identity issue.
4. `waving` - 4-frame cute hand wave, no wave marks.
5. `jumping` - 5-frame crouch, takeoff, peak, descent, settle.
6. `failed` - 8-frame failure gag; default is the character hiding inside a small trash bin.
7. `waiting` - 6-frame hopeful big-eyed blink with clasped hands.
8. `running` - 6-frame frantic coding/typing loop, not literal running.
9. `review` - 6-frame handheld magnifying-glass search loop.

If the user customizes any row, keep the same row order and frame counts unless they explicitly ask to change the Codex contract.

## Workflow

1. **Extract the concept.** Determine `pet-id`, display name, description, identity traits, style overrides, row overrides, and install target. If unclear and not risky, choose sensible defaults.
2. **Generate a base sprite.** Use the reference image as identity grounding. Create one centered full-body sprite on flat chroma-key background. Preserve core identity: hair, face, outfit, ears/tail/accessories, palette, and personality.
3. **Generate every visual frame with image2.** Do not use scripts, Pillow, canvas, SVG, or local drawing code to create character art. Directly use the image2/image generation tool to generate one frame at a time, grounded by the base sprite and original reference, then assemble those generated frames into animated GIF previews and the final atlas. Row strips are acceptable only as a fallback when the image tool cannot produce individual frames; still reject any locally drawn character pixels.
4. **Inspect before recording.** Reject frames with broken joints, pasted stick legs, disconnected hands, giant props, floating magnifiers, unreadable text, grid lines, shadows, speed lines, detached symbols, or identity drift.
5. **Extract and compose.** Use deterministic scripts only for non-creative post-processing: background removal, cropping, resizing, centering frames into `192x208` cells, composing the 8x9 atlas, creating GIF/contact-sheet QA previews, and validating transparent unused cells.
6. **QA visually.** Create a contact sheet and per-row GIFs. Check that actions are recognizable at pet size and loops are coherent.
7. **Install or package.** Save the package in the workspace and, when appropriate, copy it to `${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/`.

If a dedicated `hatch-pet` or equivalent Codex pet tooling is available, prefer it for prompt scaffolding, frame extraction, atlas composition, validation, and packaging. Use image generation for visual assets and deterministic scripts only for extraction, cleanup, QA, and packaging.

## Generation Prompt Rules

Every row prompt should include:
- "same character as the base sprite"
- the exact single-frame pose or the exact frame index within the action
- flat chroma-key background
- no text, labels, grid, scenery, shadows, speed lines, detached effects
- whole-body sprite centered in each invisible slot
- identity lock: same face, hair, outfit, palette, proportions, outline style
- row-specific motion with natural body mechanics

Prefer one prompt per frame. When generating a row, describe the frame as `frame N of M` and the adjacent motion context so each frame animates coherently after assembly.

For walking/running rows, explicitly require bent knees, alternating feet, arm swing, tail counter-sway, and coherent side-view body motion.

For prop rows, the prop must be held or attached in every frame. Avoid floating props.

## QA Gate

Do not call the pet finished until:
- atlas size is exactly `1536x1872`
- alpha exists
- unused cells are transparent
- each row has the expected frame count
- contact sheet has no broken anatomy or identity drift
- GIF previews show coherent motion
- `failed` has no detached tremble marks or floating debris after cleanup

## Common Failure

Bad shortcut: taking one static front-facing sprite and drawing new legs/arms over it locally. This creates broken knees, disconnected hands, and ugly GIFs. Prefer full-pose row generation, then deterministic extraction and packaging only.

Worse shortcut: using a local script to draw the pet character or synthesize sprite frames. Do not do this. Generate the character images frame by frame with image2/image generation, then use scripts only to package the generated frames.
