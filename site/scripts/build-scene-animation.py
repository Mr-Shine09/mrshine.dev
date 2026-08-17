#!/usr/bin/env python3
"""Build web-ready frame PNGs, atlas PNG, animated WebP, and GIF preview.

The generated source is an invisible 4x3 board. Grid cuts are proportional so
the script remains deterministic even when the source dimensions are not
evenly divisible by three. Each complete cell is letterboxed onto a shared
canvas instead of content-cropped, which preserves the authored camera and
prevents animation jitter.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    return parser.parse_args()


def fit_cell(cell: Image.Image, size: tuple[int, int]) -> Image.Image:
    cell = cell.convert("RGBA")
    target_w, target_h = size
    scale = min(target_w / cell.width, target_h / cell.height)
    fitted = cell.resize(
        (max(1, round(cell.width * scale)), max(1, round(cell.height * scale))),
        Image.Resampling.NEAREST,
    )
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (target_w - fitted.width) // 2
    y = target_h - fitted.height
    canvas.alpha_composite(fitted, (x, y))
    return canvas


def main() -> None:
    args = parse_args()
    contract = json.loads(args.contract.read_text())
    scene = next((item for item in contract["scenes"] if item["id"] == args.scene_id), None)
    if scene is None:
        raise SystemExit(f"Unknown scene id: {args.scene_id}")

    layout = contract["layout"]
    cols = int(layout["columns"])
    rows = int(layout["rows"])
    frame_count = int(layout["frameCount"])
    frame_size = tuple(int(value) for value in layout["outputFrameSize"])
    if cols * rows != frame_count:
        raise SystemExit("Contract grid does not match frameCount")

    source = Image.open(args.source).convert("RGBA")
    frames_dir = args.output_root / "frames" / args.scene_id
    previews_dir = args.output_root / "previews"
    frames_dir.mkdir(parents=True, exist_ok=True)
    previews_dir.mkdir(parents=True, exist_ok=True)

    frames: list[Image.Image] = []
    for row in range(rows):
        for col in range(cols):
            left = round(col * source.width / cols)
            right = round((col + 1) * source.width / cols)
            top = round(row * source.height / rows)
            bottom = round((row + 1) * source.height / rows)
            frame = fit_cell(source.crop((left, top, right, bottom)), frame_size)
            index = row * cols + col
            frame.save(frames_dir / f"{args.scene_id}-{index:02d}.png", optimize=True)
            frames.append(frame)

    atlas = Image.new("RGBA", (frame_size[0] * frame_count, frame_size[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (index * frame_size[0], 0))
    atlas_path = args.output_root / f"{args.scene_id}-atlas.png"
    atlas.save(atlas_path, optimize=True)

    durations = [int(value) for value in scene["durationsMs"]]
    if len(durations) != frame_count:
        raise SystemExit(f"{args.scene_id} has {len(durations)} durations, expected {frame_count}")

    webp_path = args.output_root / f"{args.scene_id}.webp"
    frames[0].save(
        webp_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        lossless=True,
        method=6,
    )

    preview_frames: list[Image.Image] = []
    backing = Image.new("RGBA", frame_size, (16, 19, 26, 255))
    for frame in frames:
        preview = backing.copy()
        preview.alpha_composite(frame)
        preview_frames.append(preview.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    preview_frames[0].save(
        previews_dir / f"{args.scene_id}.gif",
        save_all=True,
        append_images=preview_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )

    manifest = {
        "id": args.scene_id,
        "label": scene["label"],
        "frameSize": list(frame_size),
        "frameCount": frame_count,
        "durationsMs": durations,
        "atlas": f"{args.scene_id}-atlas.png",
        "animatedWebp": f"{args.scene_id}.webp",
        "frames": [f"frames/{args.scene_id}/{args.scene_id}-{i:02d}.png" for i in range(frame_count)],
    }
    (args.output_root / f"{args.scene_id}.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
