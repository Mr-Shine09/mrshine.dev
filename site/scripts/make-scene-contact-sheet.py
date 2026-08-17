#!/usr/bin/env python3
"""Create a single dark-backed QA sheet for every authored scene frame."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "public" / "animations" / "oak-scenes"
CONTRACT = json.loads((ROOT / "scene-contract.json").read_text())
FRAME_W, FRAME_H = CONTRACT["layout"]["outputFrameSize"]
COLS = CONTRACT["layout"]["columns"]
ROWS = CONTRACT["layout"]["rows"]
LABEL_H = 30
GAP = 8
SCENE_GAP = 34
BG = (16, 19, 26, 255)
PANEL = (25, 28, 35, 255)
TEXT = (241, 189, 88, 255)


def main() -> None:
    width = COLS * FRAME_W + (COLS - 1) * GAP
    scene_height = LABEL_H + ROWS * FRAME_H + (ROWS - 1) * GAP
    height = len(CONTRACT["scenes"]) * scene_height + (len(CONTRACT["scenes"]) - 1) * SCENE_GAP
    sheet = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for scene_index, scene in enumerate(CONTRACT["scenes"]):
        top = scene_index * (scene_height + SCENE_GAP)
        draw.text((0, top + 7), scene["label"].upper(), fill=TEXT, font=font)
        frames_dir = ROOT / "frames" / scene["id"]
        for frame_index in range(CONTRACT["layout"]["frameCount"]):
            row, col = divmod(frame_index, COLS)
            x = col * (FRAME_W + GAP)
            y = top + LABEL_H + row * (FRAME_H + GAP)
            panel = Image.new("RGBA", (FRAME_W, FRAME_H), PANEL)
            frame = Image.open(frames_dir / f"{scene['id']}-{frame_index:02d}.png").convert("RGBA")
            panel.alpha_composite(frame)
            sheet.alpha_composite(panel, (x, y))
            draw.rectangle((x + 6, y + 6, x + 34, y + 22), fill=BG)
            draw.text((x + 10, y + 8), f"{frame_index:02d}", fill=TEXT, font=font)

    output = ROOT / "previews" / "contact-sheet.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(output, optimize=True)
    print(output)


if __name__ == "__main__":
    main()

