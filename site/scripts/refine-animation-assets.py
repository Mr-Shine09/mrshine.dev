#!/usr/bin/env python3
"""Build aligned, palette-stable APNG animation assets and QA previews.

The old scene art was authored on 4x3 boards and flattened into horizontal
strips with a systematic row/column origin drift.  This tool preserves the
drawings, compensates for that drift with shared column and row anchors,
normalizes the pixel grid, and packages the result as native APNG.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


SCENE_SIZE = (384, 320)
SCENE_COUNT = 12
SCENE_BASELINE = 304
HERO_SIZE = (160, 208)
HERO_COUNT = 13


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--generated-dir", type=Path, required=True)
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--preview-dir", type=Path, required=True)
    return parser.parse_args()


def alpha_bbox(frame: Image.Image) -> tuple[int, int, int, int]:
    bbox = frame.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("blank animation frame")
    return bbox


def translate(frame: Image.Image, dx: int, dy: int) -> Image.Image:
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    result.alpha_composite(frame, (dx, dy))
    return result


def strip_frames(path: Path, count: int, size: tuple[int, int]) -> list[Image.Image]:
    with Image.open(path) as image:
        image = image.convert("RGBA")
        frame_w, frame_h = size
        expected = (frame_w * count, frame_h)
        if image.size != expected:
            raise ValueError(f"{path.name}: expected {expected}, found {image.size}")
        return [
            image.crop((index * frame_w, 0, (index + 1) * frame_w, frame_h))
            for index in range(count)
        ]


def remove_checkerboard(image: Image.Image) -> Image.Image:
    """Remove the generated preview checkerboard via border-connected flood fill."""

    rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
    neutral = rgb.max(axis=2) - rgb.min(axis=2) <= 12
    bright = rgb.mean(axis=2) >= 215
    candidate = neutral & bright
    height, width = candidate.shape
    background = np.zeros((height, width), dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        for y in (0, height - 1):
            if candidate[y, x] and not background[y, x]:
                background[y, x] = True
                queue.append((y, x))
    for y in range(height):
        for x in (0, width - 1):
            if candidate[y, x] and not background[y, x]:
                background[y, x] = True
                queue.append((y, x))

    while queue:
        y, x = queue.popleft()
        for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if (
                0 <= yy < height
                and 0 <= xx < width
                and candidate[yy, xx]
                and not background[yy, xx]
            ):
                background[yy, xx] = True
                queue.append((yy, xx))

    rgba = np.dstack(
        [rgb.clip(0, 255).astype(np.uint8), np.where(background, 0, 255).astype(np.uint8)]
    )
    return Image.fromarray(rgba, "RGBA")


def board_frames(
    path: Path,
    *,
    output_size: tuple[int, int],
    scale: float = 1.0,
) -> list[Image.Image]:
    with Image.open(path) as source:
        clean = remove_checkerboard(source)
    frames: list[Image.Image] = []
    for row in range(3):
        y0 = round(row * clean.height / 3)
        y1 = round((row + 1) * clean.height / 3)
        for column in range(4):
            x0 = round(column * clean.width / 4)
            x1 = round((column + 1) * clean.width / 4)
            cell = clean.crop((x0, y0, x1, y1))
            if scale == 1.0:
                cell = cell.resize(output_size, Image.Resampling.NEAREST)
                frames.append(cell)
                continue
            scaled = cell.resize(
                (round(cell.width * scale), round(cell.height * scale)),
                Image.Resampling.NEAREST,
            )
            canvas = Image.new("RGBA", output_size, (0, 0, 0, 0))
            canvas.alpha_composite(
                scaled,
                ((output_size[0] - scaled.width) // 2, (output_size[1] - scaled.height) // 2),
            )
            frames.append(canvas)
    return frames


def top_anchor_x(frame: Image.Image) -> float:
    left, top, right, bottom = alpha_bbox(frame)
    band_bottom = min(bottom, top + max(56, round((bottom - top) * 0.38)))
    band = frame.getchannel("A").crop((0, top, frame.width, band_bottom)).getbbox()
    if band is None:
        return (left + right) / 2
    return (band[0] + band[2]) / 2


def global_anchor_x(frame: Image.Image) -> float:
    left, _top, right, _bottom = alpha_bbox(frame)
    return (left + right) / 2


def align_board(
    frames: list[Image.Image],
    *,
    x_mode: str,
    target_x: int = 192,
    target_baseline: int = SCENE_BASELINE,
) -> tuple[list[Image.Image], dict[str, list[int]]]:
    if len(frames) != 12:
        raise ValueError("alignment expects a 4x3, 12-frame board")
    anchor = top_anchor_x if x_mode == "top" else global_anchor_x
    column_centers = [
        statistics.median(anchor(frames[row * 4 + column]) for row in range(3))
        for column in range(4)
    ]
    row_bottoms = [
        statistics.median(alpha_bbox(frames[row * 4 + column])[3] for column in range(4))
        for row in range(3)
    ]
    column_dx = [round(target_x - value) for value in column_centers]
    row_dy = [round(target_baseline - value) for value in row_bottoms]
    aligned = [
        translate(frame, column_dx[index % 4], row_dy[index // 4])
        for index, frame in enumerate(frames)
    ]
    return aligned, {"columnDx": column_dx, "rowDy": row_dy}


def palette_for(frames: list[Image.Image], colors: int) -> Image.Image:
    samples: list[np.ndarray] = []
    for frame in frames:
        rgba = np.asarray(frame.convert("RGBA"))
        opaque = rgba[rgba[:, :, 3] >= 128, :3]
        if opaque.size:
            samples.append(opaque)
    pixels = np.concatenate(samples, axis=0)
    if len(pixels) > 500_000:
        pixels = pixels[:: math.ceil(len(pixels) / 500_000)]
    swatch = Image.fromarray(pixels.reshape(1, len(pixels), 3), "RGB")
    return swatch.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)


def pixel_cleanup(
    frames: list[Image.Image],
    *,
    colors: int = 64,
    logical_scale: int = 2,
) -> list[Image.Image]:
    reduced: list[Image.Image] = []
    for frame in frames:
        rgba = frame.convert("RGBA")
        if logical_scale > 1:
            small = rgba.resize(
                (rgba.width // logical_scale, rgba.height // logical_scale),
                Image.Resampling.NEAREST,
            )
        else:
            small = rgba
        alpha = small.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
        rgb = small.convert("RGB")
        clean = rgb.convert("RGBA")
        clean.putalpha(alpha)
        reduced.append(clean)

    palette = palette_for(reduced, colors)
    cleaned: list[Image.Image] = []
    for frame in reduced:
        alpha = frame.getchannel("A")
        indexed = frame.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
        rgba = indexed.convert("RGBA")
        rgba.putalpha(alpha)
        if logical_scale > 1:
            rgba = rgba.resize(frames[0].size, Image.Resampling.NEAREST)
        pixels = np.asarray(rgba).copy()
        pixels[pixels[:, :, 3] == 0, :3] = 0
        cleaned.append(Image.fromarray(pixels, "RGBA"))
    return cleaned


def save_apng(
    path: Path,
    frames: list[Image.Image],
    durations: list[int],
    *,
    loop: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=loop,
        disposal=[2] * len(frames),
        blend=[0] * len(frames),
        optimize=False,
    )


def save_static(path: Path, frame: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.save(path, optimize=True)


def draw_alignment_cell(
    frame: Image.Image,
    *,
    guides: tuple[int, int, int, int],
    size: tuple[int, int] = (192, 160),
) -> Image.Image:
    tile = Image.new("RGBA", size, (247, 244, 238, 255))
    preview = frame.copy()
    preview.thumbnail(size, Image.Resampling.NEAREST)
    tile.alpha_composite(preview, ((size[0] - preview.width) // 2, size[1] - preview.height))
    draw = ImageDraw.Draw(tile)
    sx = size[0] / frame.width
    sy = size[1] / frame.height
    colors = ((36, 184, 210, 180), (55, 112, 220, 180), (211, 70, 190, 180), (235, 145, 32, 220))
    for y, color in zip(guides, colors, strict=True):
        yy = round(y * sy)
        draw.line((0, yy, size[0] - 1, yy), fill=color, width=1)
    cx = round(frame.width / 2 * sx)
    draw.line((cx, 0, cx, size[1] - 1), fill=(60, 170, 120, 150), width=1)
    return tile


def make_alignment_sheet(
    output: Path,
    animations: dict[str, list[Image.Image]],
    guide_map: dict[str, tuple[int, int, int, int]],
) -> None:
    font = ImageFont.load_default()
    sections: list[Image.Image] = []
    for name, frames in animations.items():
        tile_w, tile_h = (192, 160)
        label_h = 24
        section = Image.new("RGBA", (tile_w * 4, label_h + tile_h * 3), (24, 25, 28, 255))
        draw = ImageDraw.Draw(section)
        draw.text((8, 7), name, fill=(255, 255, 255, 255), font=font)
        for index, frame in enumerate(frames[:12]):
            tile = draw_alignment_cell(frame, guides=guide_map[name])
            section.alpha_composite(tile, ((index % 4) * tile_w, label_h + (index // 4) * tile_h))
        sections.append(section)
    sheet = Image.new(
        "RGBA",
        (max(section.width for section in sections), sum(section.height for section in sections)),
        (16, 17, 19, 255),
    )
    y = 0
    for section in sections:
        sheet.alpha_composite(section, (0, y))
        y += section.height
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, optimize=True)


def frame_at_time(frames: list[Image.Image], durations: list[int], elapsed: int) -> Image.Image:
    total = sum(durations)
    cursor = elapsed % total
    for frame, duration in zip(frames, durations, strict=True):
        if cursor < duration:
            return frame
        cursor -= duration
    return frames[-1]


def make_motion_preview(
    output: Path,
    animations: dict[str, tuple[list[Image.Image], list[int], bool]],
) -> None:
    font = ImageFont.load_default()
    names = list(animations)
    tile_w, tile_h, label_h = 192, 160, 20
    columns = 3
    rows = math.ceil(len(names) / columns)
    preview_frames: list[Image.Image] = []
    for tick in range(36):
        elapsed = tick * 83
        board = Image.new("RGBA", (columns * tile_w, rows * (tile_h + label_h)), (24, 25, 28, 255))
        draw = ImageDraw.Draw(board)
        for index, name in enumerate(names):
            frames, durations, once = animations[name]
            if once and elapsed >= sum(durations):
                frame = frames[-1]
            else:
                frame = frame_at_time(frames, durations, elapsed)
            tile = Image.new("RGBA", (tile_w, tile_h), (247, 244, 238, 255))
            scaled = frame.copy()
            scaled.thumbnail((tile_w, tile_h), Image.Resampling.NEAREST)
            tile.alpha_composite(scaled, ((tile_w - scaled.width) // 2, tile_h - scaled.height))
            x = (index % columns) * tile_w
            y = (index // columns) * (tile_h + label_h)
            board.alpha_composite(tile, (x, y + label_h))
            draw.text((x + 6, y + 6), name, fill=(255, 255, 255, 255), font=font)
        preview_frames.append(board)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_apng(output, preview_frames, [83] * len(preview_frames), loop=0)


def main() -> None:
    args = parse_args()
    public = args.site_root / "public" / "assets" / "animation"
    with (public / "scenes" / "scene-contract.json").open() as handle:
        contract = json.load(handle)
    durations = {scene["id"]: scene["durationsMs"] for scene in contract["scenes"]}

    hero = strip_frames(args.source_dir / "oak-welcome-atlas.png", HERO_COUNT, HERO_SIZE)
    hero = pixel_cleanup(hero, colors=64, logical_scale=1)

    scene_sources = {
        "computer-working": strip_frames(args.source_dir / "computer-working-atlas.png", 12, SCENE_SIZE),
        "reading-fire": strip_frames(args.source_dir / "reading-fire-atlas.png", 12, SCENE_SIZE),
        "thinking-cloud": strip_frames(args.source_dir / "thinking-cloud-atlas.png", 12, SCENE_SIZE),
        "walking": strip_frames(args.source_dir / "walking-atlas.png", 12, SCENE_SIZE),
        "workbench-zap": board_frames(
            args.generated_dir / "workbench-board.png", output_size=SCENE_SIZE
        ),
        "run": board_frames(args.generated_dir / "run-board.png", output_size=SCENE_SIZE, scale=0.78),
    }

    align_modes = {
        "computer-working": "global",
        "reading-fire": "global",
        "thinking-cloud": "global",
        "walking": "top",
        "workbench-zap": "global",
        "run": "top",
    }
    scenes: dict[str, list[Image.Image]] = {}
    alignment_report: dict[str, dict[str, list[int]]] = {}
    for name, source_frames in scene_sources.items():
        aligned, report = align_board(source_frames, x_mode=align_modes[name])
        scenes[name] = pixel_cleanup(aligned, colors=64, logical_scale=2)
        alignment_report[name] = report

    hero_durations = [700, 180, 180, 180, 160, 120, 140, 140, 260, 260, 160, 160, 1100]
    save_apng(public / "hero" / "oak-welcome-atlas.png", hero, hero_durations, loop=0)
    save_static(public / "hero" / "oak-welcome-static.png", hero[11])

    scene_durations = dict(durations)
    scene_durations["run"] = [83] * 12
    for name, frames in scenes.items():
        loop = 1 if name == "workbench-zap" else 0
        save_apng(public / "scenes" / f"{name}-atlas.png", frames, scene_durations[name], loop=loop)
        save_static(public / "scenes" / f"{name}-static.png", frames[0])

    guide_map = {
        "oak-welcome": (45, 90, 145, 204),
        "computer-working": (64, 108, 194, 304),
        "reading-fire": (72, 122, 202, 304),
        "thinking-cloud": (122, 168, 226, 304),
        "walking": (58, 108, 174, 304),
        "run": (62, 112, 178, 304),
        "workbench-zap": (92, 142, 224, 304),
    }
    preview_animations = {"oak-welcome": hero, **scenes}
    make_alignment_sheet(
        args.preview_dir / "oak-animation-alignment-guides.png",
        preview_animations,
        guide_map,
    )
    motion = {
        "oak-welcome": (hero, hero_durations, False),
        "computer-working": (scenes["computer-working"], scene_durations["computer-working"], False),
        "reading-fire": (scenes["reading-fire"], scene_durations["reading-fire"], False),
        "thinking-cloud": (scenes["thinking-cloud"], scene_durations["thinking-cloud"], False),
        "walking": (scenes["walking"], scene_durations["walking"], False),
        "run": (scenes["run"], scene_durations["run"], False),
        "workbench-zap": (scenes["workbench-zap"], scene_durations["workbench-zap"], True),
    }
    make_motion_preview(args.preview_dir / "oak-animation-motion-preview.png", motion)
    (args.preview_dir / "alignment-report.json").write_text(
        json.dumps(alignment_report, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
