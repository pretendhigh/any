from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "any" / "spritesheet.webp"
QA = ROOT / "qa"

CELL_W = 192
CELL_H = 208
COLS = 8
ROWS = [
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
]

DURATIONS = {
    "idle": [320, 180, 180, 220, 220, 360],
    "running-right": [105, 105, 105, 105, 105, 105, 105, 130],
    "running-left": [105, 105, 105, 105, 105, 105, 105, 130],
    "waving": [140, 140, 140, 260],
    "jumping": [130, 130, 150, 140, 260],
    "failed": [150, 150, 150, 180, 180, 160, 150, 220],
    "waiting": [160, 150, 150, 170, 170, 260],
    "running": [90, 90, 90, 90, 90, 120],
    "review": [150, 150, 150, 150, 150, 230],
}


def validate(atlas: Image.Image) -> dict[str, object]:
    unused_ok = True
    for row, (_, used) in enumerate(ROWS):
        for col in range(used, COLS):
            box = (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
            if atlas.crop(box).getchannel("A").getbbox() is not None:
                unused_ok = False
    return {
        "dimensions": list(atlas.size),
        "cell": [CELL_W, CELL_H],
        "grid": [COLS, len(ROWS)],
        "unused_cells_transparent": unused_ok,
        "rows": [{"state": state, "used_columns": used} for state, used in ROWS],
    }


def write_contact_sheet(atlas: Image.Image) -> None:
    sheet = Image.new("RGBA", atlas.size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    tile = 16
    for y in range(0, sheet.height, tile):
        for x in range(0, sheet.width, tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(225, 225, 225, 255))
    sheet.alpha_composite(atlas)
    draw = ImageDraw.Draw(sheet)
    for x in range(0, sheet.width + 1, CELL_W):
        draw.line((x, 0, x, sheet.height), fill=(0, 0, 0, 90), width=1)
    for y in range(0, sheet.height + 1, CELL_H):
        draw.line((0, y, sheet.width, y), fill=(0, 0, 0, 90), width=1)
    sheet.save(QA / "contact-sheet.png")


def write_gifs(atlas: Image.Image) -> None:
    gif_dir = QA / "gifs"
    gif_dir.mkdir(parents=True, exist_ok=True)
    for row, (state, used) in enumerate(ROWS):
        frames: list[Image.Image] = []
        for col in range(used):
            frame = atlas.crop((col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H))
            bg = Image.new("RGBA", frame.size, (24, 25, 30, 255))
            bg.alpha_composite(frame)
            frames.append(bg.resize((CELL_W * 2, CELL_H * 2), Image.Resampling.NEAREST).convert("P", palette=Image.Palette.ADAPTIVE))
        frames[0].save(
            gif_dir / f"{state}.gif",
            save_all=True,
            append_images=frames[1:],
            duration=DURATIONS[state],
            loop=0,
            disposal=2,
        )


def main() -> None:
    if not ATLAS.exists():
        raise SystemExit(f"Missing atlas: {ATLAS}")
    QA.mkdir(parents=True, exist_ok=True)
    atlas = Image.open(ATLAS).convert("RGBA")
    write_contact_sheet(atlas)
    write_gifs(atlas)
    (QA / "validation.json").write_text(json.dumps(validate(atlas), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "qa": str(QA)}, indent=2))


if __name__ == "__main__":
    main()
