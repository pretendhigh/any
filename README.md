# Any Codex Pet

`any` is a custom Codex pet based on the provided pink-haired fox-eared anime character, redesigned as a cute JK-uniform desktop companion.

## Files

- `any/pet.json` - Codex pet manifest.
- `any/spritesheet.webp` - final 8x9 Codex pet atlas, 1536x1872.
- `qa/contact-sheet.png` - visual QA sheet for every animation cell.
- `qa/gifs/` - per-state animated previews.
- `qa/validation.json` - atlas dimension and transparent-unused-cell validation.
- `scripts/export_previews.py` - regenerates QA GIFs, contact sheet, and atlas validation from `any/spritesheet.webp`.
- `prompt.md` - standalone prompt for generating a similar Codex pet from a new character image.
- `skill/codex-pet-from-character/SKILL.md` - reusable Codex skill version of the workflow.

## Creation Process

1. Started from the user-provided pink-haired fox-eared anime reference and generated a clean Any base sprite with JK uniform, fluffy tail, chibi proportions, thick outline, and a flat chroma-key background.
2. Used the Codex pet contract as the target format: one transparent `1536x1872` atlas, 8 columns x 9 rows, with `192x208` cells and transparent unused cells.
3. Generated each animation row as a full pose strip instead of hand-patching limbs onto a static sprite. This keeps the body, knees, arms, hair, ears, and tail anatomically coherent frame to frame.
4. Reworked the key states after visual review:
   - `idle`: sleepy nodding loop.
   - `running-right` / `running-left`: side-view walk/run cycles with alternating knees and feet.
   - `waiting`: hopeful big-eyed blink with clasped hands.
   - `running`: frantic coding at a laptop.
   - `review`: searching with a handheld magnifying glass.
   - `failed`: Any hiding inside a trash bin.
5. Extracted the generated row strips into Codex-sized cells, composed the final WebP atlas, and removed small detached failed-row artifacts.
6. Exported QA assets from the final atlas: `qa/contact-sheet.png`, per-state GIFs in `qa/gifs/`, and `qa/validation.json`.
7. Installed the final package to `~/.codex/pets/any/` for local Codex use.

## Animation Rows

1. `idle` - sleepy, drowsy idle.
2. `running-right` - rightward walk/run loop with alternating knees.
3. `running-left` - leftward walk/run loop with alternating knees.
4. `waving`
5. `jumping`
6. `failed` - Any hides inside a trash bin.
7. `waiting` - expectant big-eyed blink.
8. `running` - frantic coding at a keyboard.
9. `review` - searching with a magnifying glass.

## Install

Method 1: install with `codex-pets`:

```bash
npx codex-pets add any
```

Method 2: install manually by copying the package folder:

```bash
mkdir -p ~/.codex/pets/any
cp any/pet.json any/spritesheet.webp ~/.codex/pets/any/
```

Then restart or refresh Codex if the pet list is already open.

## Reuse This Workflow

- Paste [prompt.md](prompt.md) into a new Codex task and attach a character image.
- Or copy `skill/codex-pet-from-character/` into your Codex skills directory and ask Codex to use it when creating a pet from a character image.
