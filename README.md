# Any Codex Pet

`any` is a custom Codex pet based on the provided pink-haired fox-eared anime character, redesigned as a cute JK-uniform desktop companion.

## Files

- `any/pet.json` - Codex pet manifest.
- `any/spritesheet.webp` - final 8x9 Codex pet atlas, 1536x1872.
- `qa/contact-sheet.png` - visual QA sheet for every animation cell.
- `qa/gifs/` - per-state animated previews.
- `qa/validation.json` - atlas dimension and transparent-unused-cell validation.
- `scripts/export_previews.py` - regenerates QA GIFs, contact sheet, and atlas validation from `any/spritesheet.webp`.

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

Copy `any/` into:

```text
~/.codex/pets/any/
```

Then restart or refresh Codex if the pet list is already open.
