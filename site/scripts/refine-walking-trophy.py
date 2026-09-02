#!/usr/bin/env python3
"""Repair walking-frame anchors and package the Achievement trophy APNG.

The walking repair intentionally operates on the original tracked strip so a
previous APNG alignment pass cannot compound its offsets. The trophy builder
accepts one generated 4x3 board and applies the same hard-alpha, palette, and
anchor rules as the production scene assets.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


FRAME_SIZE = (384, 320)
FRAME_COUNT = 12
BASELINE = 304


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--walking-source", type=Path, required=True)
    parser.add_argument("--walking-current", type=Path, required=True)
    parser.add_argument("--trophy-board", type=Path)
    parser.add_argument("--scene-dir", type=Path, required=True)
    parser.add_argument("--preview-dir", type=Path, required=True)
    parser.add_argument("--inspect-only", action="store_true")
    return parser.parse_args()


def strip_frames(path: Path) -> list[Image.Image]:
    with Image.open(path) as image:
        source = image.convert("RGBA")
    expected = (FRAME_SIZE[0] * FRAME_COUNT, FRAME_SIZE[1])
    if source.size != expected:
        raise ValueError(f"{path}: expected {expected}, found {source.size}")
    return [
        source.crop((index * FRAME_SIZE[0], 0, (index + 1) * FRAME_SIZE[0], FRAME_SIZE[1]))
        for index in range(FRAME_COUNT)
    ]


def apng_frames(path: Path) -> tuple[list[Image.Image], list[int], int]:
    frames: list[Image.Image] = []
    durations: list[int] = []
    with Image.open(path) as image:
        loop = int(image.info.get("loop", 0))
        for index in range(getattr(image, "n_frames", 1)):
            image.seek(index)
            frames.append(image.convert("RGBA"))
            durations.append(round(float(image.info.get("duration", 0))))
    return frames, durations, loop


def alpha_components(frame: Image.Image) -> list[tuple[int, tuple[int, int, int, int]]]:
    mask = np.asarray(frame.getchannel("A")) > 0
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    components: list[tuple[int, tuple[int, int, int, int]]] = []
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or seen[y, x]:
                continue
            queue: deque[tuple[int, int]] = deque([(y, x)])
            seen[y, x] = True
            count = 0
            left = right = x
            top = bottom = y
            while queue:
                yy, xx = queue.popleft()
                count += 1
                left = min(left, xx)
                right = max(right, xx)
                top = min(top, yy)
                bottom = max(bottom, yy)
                for ny, nx in ((yy - 1, xx), (yy + 1, xx), (yy, xx - 1), (yy, xx + 1)):
                    if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        queue.append((ny, nx))
            components.append((count, (left, top, right + 1, bottom + 1)))
    return sorted(components, reverse=True)


def largest_component(frame: Image.Image) -> Image.Image:
    """Keep the connected character and discard detached strip-conversion debris."""

    source = np.asarray(frame.convert("RGBA"))
    mask = source[:, :, 3] > 0
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    best: list[tuple[int, int]] = []
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or seen[y, x]:
                continue
            queue: deque[tuple[int, int]] = deque([(y, x)])
            seen[y, x] = True
            pixels: list[tuple[int, int]] = []
            while queue:
                yy, xx = queue.popleft()
                pixels.append((yy, xx))
                for ny, nx in ((yy - 1, xx), (yy + 1, xx), (yy, xx - 1), (yy, xx + 1)):
                    if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        queue.append((ny, nx))
            if len(pixels) > len(best):
                best = pixels
    if not best:
        raise ValueError("blank frame")
    keep = np.zeros_like(mask)
    ys, xs = zip(*best, strict=True)
    keep[np.asarray(ys), np.asarray(xs)] = True
    result = source.copy()
    result[~keep] = 0
    return Image.fromarray(result, "RGBA")


def main_component_bbox(frame: Image.Image) -> tuple[int, int, int, int]:
    components = alpha_components(frame)
    if not components:
        raise ValueError("blank frame")
    largest = components[0]
    included = [largest]
    ll, lt, lr, lb = largest[1]
    for component in components[1:]:
        count, (left, top, right, bottom) = component
        near = not (right < ll - 14 or left > lr + 14 or bottom < lt - 14 or top > lb + 14)
        if count >= 8 and near:
            included.append(component)
    return (
        min(item[1][0] for item in included),
        min(item[1][1] for item in included),
        max(item[1][2] for item in included),
        max(item[1][3] for item in included),
    )


def translate(frame: Image.Image, dx: int, dy: int) -> Image.Image:
    canvas = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    canvas.alpha_composite(frame, (dx, dy))
    return canvas


def palette_for(frames: list[Image.Image], colors: int = 64) -> Image.Image:
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


def clean_with_palette(frame: Image.Image, palette: Image.Image) -> Image.Image:
    small = frame.resize((frame.width // 2, frame.height // 2), Image.Resampling.NEAREST)
    alpha = small.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
    indexed = small.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
    rgba = indexed.convert("RGBA")
    rgba.putalpha(alpha)
    rgba = rgba.resize(frame.size, Image.Resampling.NEAREST)
    pixels = np.asarray(rgba).copy()
    pixels[pixels[:, :, 3] == 0, :3] = 0
    return Image.fromarray(pixels, "RGBA")


def remove_checkerboard(image: Image.Image) -> Image.Image:
    """Remove a baked neutral checkerboard with a border-connected flood fill."""

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
            if 0 <= yy < height and 0 <= xx < width and candidate[yy, xx] and not background[yy, xx]:
                background[yy, xx] = True
                queue.append((yy, xx))
    rgba = np.dstack(
        [rgb.clip(0, 255).astype(np.uint8), np.where(background, 0, 255).astype(np.uint8)]
    )
    return Image.fromarray(rgba, "RGBA")


def trophy_board_frames(path: Path) -> list[Image.Image]:
    with Image.open(path) as image:
        clean = remove_checkerboard(image)
    cells: list[Image.Image] = []
    for row in range(3):
        y0 = round(row * clean.height / 3)
        y1 = round((row + 1) * clean.height / 3)
        for column in range(4):
            x0 = round(column * clean.width / 4)
            x1 = round((column + 1) * clean.width / 4)
            cells.append(clean.crop((x0, y0, x1, y1)))

    opening_heights = []
    for cell in cells[:5]:
        bbox = main_component_bbox(cell)
        opening_heights.append(bbox[3] - bbox[1])
    scale = 248 / float(np.median(opening_heights))
    frames: list[Image.Image] = []
    for cell in cells:
        scaled = cell.resize(
            (round(cell.width * scale), round(cell.height * scale)),
            Image.Resampling.NEAREST,
        )
        bbox = main_component_bbox(scaled)
        center_x = (bbox[0] + bbox[2]) / 2
        canvas = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
        canvas.alpha_composite(
            scaled,
            (round(FRAME_SIZE[0] / 2 - center_x), BASELINE - bbox[3]),
        )
        frames.append(canvas)
    return frames


def save_apng(path: Path, frames: list[Image.Image], durations: list[int], loop: int) -> None:
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


def frame_at_time(frames: list[Image.Image], durations: list[int], elapsed: int) -> Image.Image:
    cursor = elapsed % sum(durations)
    for frame, duration in zip(frames, durations, strict=True):
        if cursor < duration:
            return frame
        cursor -= duration
    return frames[-1]


def motion_preview(
    path: Path,
    walking: list[Image.Image],
    walking_durations: list[int],
    trophy: list[Image.Image],
    trophy_durations: list[int],
) -> None:
    preview: list[Image.Image] = []
    font = ImageFont.load_default()
    for tick in range(42):
        elapsed = tick * 83
        canvas = Image.new("RGBA", (768, 346), (27, 29, 33, 255))
        draw = ImageDraw.Draw(canvas)
        draw.text((8, 8), "Walking — repaired frames 5–8", fill="white", font=font)
        draw.text((392, 8), "Achievement — trophy lift", fill="white", font=font)
        walk_tile = Image.new("RGBA", FRAME_SIZE, (245, 242, 236, 255))
        walk_tile.alpha_composite(frame_at_time(walking, walking_durations, elapsed))
        trophy_tile = Image.new("RGBA", FRAME_SIZE, (245, 242, 236, 255))
        trophy_frame = trophy[-1] if elapsed >= sum(trophy_durations) else frame_at_time(trophy, trophy_durations, elapsed)
        trophy_tile.alpha_composite(trophy_frame)
        canvas.alpha_composite(walk_tile, (0, 26))
        canvas.alpha_composite(trophy_tile, (384, 26))
        preview.append(canvas)
    save_apng(path, preview, [83] * len(preview), 0)


def repair_walking(
    original: list[Image.Image],
    current: list[Image.Image],
    durations: list[int],
    loop: int,
    output: Path,
) -> list[Image.Image]:
    repaired = list(current)
    palette = palette_for(current)
    column_dx = (-9, 26, 44, 70)
    for index in range(4, 8):
        character = largest_component(original[index])
        _left, _top, _right, bottom = main_component_bbox(character)
        aligned = translate(character, column_dx[index % 4], BASELINE - bottom)
        repaired[index] = clean_with_palette(aligned, palette)
    save_apng(output, repaired, durations, loop)
    return repaired


def contact_sheet(path: Path, frames: list[Image.Image], title: str) -> None:
    tile_w, tile_h = 192, 160
    header = 26
    sheet = Image.new("RGBA", (tile_w * 4, header + tile_h * 3), (27, 29, 33, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((8, 8), title, fill=(255, 255, 255, 255), font=font)
    for index, frame in enumerate(frames):
        tile = Image.new("RGBA", (tile_w, tile_h), (245, 242, 236, 255))
        tile.alpha_composite(frame.resize((tile_w, tile_h), Image.Resampling.NEAREST))
        tile_draw = ImageDraw.Draw(tile)
        for y, color in ((56, (55, 190, 220, 190)), (108, (68, 120, 225, 190)), (174, (220, 72, 180, 190)), (BASELINE, (240, 145, 32, 220))):
            yy = round(y * tile_h / FRAME_SIZE[1])
            tile_draw.line((0, yy, tile_w - 1, yy), fill=color, width=1)
        tile_draw.line((tile_w // 2, 0, tile_w // 2, tile_h - 1), fill=(70, 180, 125, 160), width=1)
        tile_draw.text((5, 5), str(index + 1), fill=(215, 35, 35, 255), font=font)
        sheet.alpha_composite(tile, ((index % 4) * tile_w, header + (index // 4) * tile_h))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def main() -> None:
    args = parse_args()
    original = strip_frames(args.walking_source)
    current, _durations, _loop = apng_frames(args.walking_current)
    for label, frames in (("original", original), ("current", current)):
        print(label)
        for index, frame in enumerate(frames):
            components = alpha_components(frame)
            print(
                index + 1,
                "main=", main_component_bbox(frame),
                "components=", components[:6],
            )
    contact_sheet(args.preview_dir / "walking-alignment-before.png", current, "Walking alignment before repair")
    if args.inspect_only:
        return
    walking_output = args.scene_dir / "walking-atlas.png"
    repaired = repair_walking(original, current, _durations, _loop, walking_output)
    contact_sheet(args.preview_dir / "walking-alignment-after.png", repaired, "Walking alignment after repair")
    if args.trophy_board is None:
        return
    trophy_source = trophy_board_frames(args.trophy_board)
    palette = palette_for([*repaired, *trophy_source])
    trophy = [clean_with_palette(frame, palette) for frame in trophy_source]
    trophy_durations = [260, 170, 140, 130, 120, 120, 130, 150, 190, 240, 320, 700]
    save_apng(args.scene_dir / "trophy-lift-atlas.png", trophy, trophy_durations, 1)
    trophy[-1].save(args.scene_dir / "trophy-lift-static.png", optimize=True)
    contact_sheet(args.preview_dir / "trophy-lift-alignment.png", trophy, "Achievement trophy-lift alignment")
    motion_preview(
        args.preview_dir / "walking-trophy-motion-preview.png",
        repaired,
        _durations,
        trophy,
        trophy_durations,
    )


if __name__ == "__main__":
    main()
