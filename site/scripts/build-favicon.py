#!/usr/bin/env python3
"""Build crisp multi-size Oak favicon assets from an ImageGen headshot."""

from __future__ import annotations

import argparse
import io
import struct
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


BACKGROUND = (240, 236, 250, 255)
DARK_PREVIEW = (25, 18, 43, 255)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--public-dir", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    return parser.parse_args()


def remove_checkerboard(image: Image.Image) -> Image.Image:
    rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
    neutral = rgb.max(axis=2) - rgb.min(axis=2) <= 12
    bright = rgb.mean(axis=2) >= 214
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


def head_crop(source: Image.Image) -> Image.Image:
    bbox = source.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("generated favicon source is blank")
    left, top, right, bottom = bbox
    subject_height = bottom - top
    side = round(subject_height * 0.91)
    center_x = (left + right) // 2
    x0 = center_x - side // 2
    y0 = max(0, top - round(side * 0.015))
    if x0 < 0:
        x0 = 0
    if x0 + side > source.width:
        x0 = source.width - side
    if y0 + side > source.height:
        y0 = source.height - side
    return source.crop((x0, y0, x0 + side, y0 + side))


def icon_at(crop: Image.Image, size: int) -> Image.Image:
    background = Image.new("RGBA", crop.size, BACKGROUND)
    background.alpha_composite(crop)
    reduced = background.convert("RGB").resize((size, size), Image.Resampling.BOX)
    indexed = reduced.quantize(
        colors=16,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    return indexed.convert("RGBA")


def icon_16() -> Image.Image:
    """Hand-reduce the identity anchors that disappear in automatic sampling."""

    image = Image.new("RGBA", (16, 16), BACKGROUND)
    draw = ImageDraw.Draw(image)
    hair = (21, 20, 27, 255)
    hair_light = (49, 48, 56, 255)
    skin = (242, 158, 61, 255)
    skin_light = (255, 188, 82, 255)
    skin_shadow = (204, 107, 30, 255)
    lens = (246, 243, 228, 255)
    navy = (18, 47, 104, 255)
    navy_light = (30, 70, 139, 255)

    # Hair silhouette and readable asymmetric spikes.
    draw.rectangle((5, 0, 10, 0), fill=hair)
    draw.rectangle((3, 1, 12, 2), fill=hair)
    draw.rectangle((2, 2, 13, 4), fill=hair)
    draw.rectangle((1, 3, 14, 5), fill=hair)
    draw.rectangle((2, 5, 13, 6), fill=hair)
    draw.point((2, 1), fill=hair)
    draw.point((13, 2), fill=hair)
    draw.rectangle((4, 1, 6, 2), fill=hair_light)
    draw.point((11, 3), fill=hair_light)

    # Face, ears, and hair fringe.
    draw.rectangle((3, 5, 12, 12), fill=skin)
    draw.rectangle((4, 6, 11, 10), fill=skin_light)
    draw.rectangle((2, 7, 2, 9), fill=skin)
    draw.rectangle((13, 7, 13, 9), fill=skin)
    draw.rectangle((3, 5, 5, 6), fill=hair)
    draw.rectangle((10, 5, 12, 6), fill=hair)
    draw.point((7, 5), fill=hair)
    draw.point((8, 6), fill=hair)

    # Two unmistakable rectangular glasses lenses and bridge.
    draw.rectangle((3, 7, 6, 9), fill=hair)
    draw.rectangle((9, 7, 12, 9), fill=hair)
    draw.rectangle((6, 7, 9, 7), fill=hair)
    draw.rectangle((4, 8, 5, 8), fill=lens)
    draw.rectangle((10, 8, 11, 8), fill=lens)
    draw.point((5, 8), fill=(48, 31, 21, 255))
    draw.point((10, 8), fill=(48, 31, 21, 255))
    draw.point((7, 9), fill=skin_shadow)
    draw.point((8, 11), fill=skin_shadow)
    draw.point((7, 11), fill=skin_shadow)

    # Navy hoodie collar and short white zipper.
    draw.rectangle((3, 13, 12, 15), fill=navy)
    draw.rectangle((2, 15, 13, 15), fill=navy)
    draw.rectangle((4, 13, 6, 14), fill=navy_light)
    draw.rectangle((9, 13, 11, 14), fill=navy_light)
    draw.rectangle((7, 13, 8, 15), fill=lens)
    return image


def write_ico(path: Path, icons: list[Image.Image]) -> None:
    encoded: list[bytes] = []
    for icon in icons:
        stream = io.BytesIO()
        icon.save(stream, format="PNG", optimize=True)
        encoded.append(stream.getvalue())
    header_size = 6 + 16 * len(icons)
    offset = header_size
    entries: list[bytes] = []
    for icon, payload in zip(icons, encoded, strict=True):
        width, height = icon.size
        entries.append(
            struct.pack(
                "<BBBBHHII",
                width if width < 256 else 0,
                height if height < 256 else 0,
                0,
                0,
                1,
                32,
                len(payload),
                offset,
            )
        )
        offset += len(payload)
    path.write_bytes(struct.pack("<HHH", 0, 1, len(icons)) + b"".join(entries) + b"".join(encoded))


def make_preview(path: Path, icons: dict[int, Image.Image]) -> None:
    width, height = 920, 520
    sheet = Image.new("RGBA", (width, height), (240, 236, 250, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((24, 20), "Oak favicon — actual-size and nearest-neighbor QA", fill=(35, 22, 70), font=font)
    panels = [((24, 54, 448, 308), (255, 255, 255, 255), "Light tab"), ((472, 54, 896, 308), DARK_PREVIEW, "Dark tab")]
    for (left, top, right, bottom), color, label in panels:
        draw.rounded_rectangle((left, top, right, bottom), radius=18, fill=color)
        draw.text((left + 16, top + 14), label, fill=(45, 35, 70) if color[0] > 100 else (240, 236, 250), font=font)
        x = left + 25
        for size in (16, 32, 48):
            icon = icons[size]
            sheet.alpha_composite(icon, (x, top + 54))
            draw.text((x, top + 110), f"{size}px", fill=(45, 35, 70) if color[0] > 100 else (240, 236, 250), font=font)
            zoom = icon.resize((size * 3, size * 3), Image.Resampling.NEAREST)
            sheet.alpha_composite(zoom, (x, top + 136))
            x += max(112, size * 3 + 24)

    draw.text((24, 340), "Silhouette check", fill=(35, 22, 70), font=font)
    x = 24
    for size in (16, 32, 48):
        icon = icons[size]
        pixels = np.asarray(icon).copy()
        bg = np.all(pixels[:, :, :3] == np.asarray(BACKGROUND[:3]), axis=2)
        pixels[~bg, :3] = (30, 22, 42)
        pixels[bg, :3] = BACKGROUND[:3]
        silhouette = Image.fromarray(pixels, "RGBA").resize((size * 3, size * 3), Image.Resampling.NEAREST)
        sheet.alpha_composite(silhouette, (x, 372))
        draw.text((x, 492), f"{size}px", fill=(35, 22, 70), font=font)
        x += max(112, size * 3 + 28)
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def main() -> None:
    args = parse_args()
    with Image.open(args.source) as generated:
        crop = head_crop(remove_checkerboard(generated))
    icons = {size: icon_at(crop, size) for size in (32, 48, 60, 64)}
    icons[16] = icon_16()
    args.public_dir.mkdir(parents=True, exist_ok=True)
    icons[32].save(args.public_dir / "favicon-32.png", optimize=True)
    icons[48].save(args.public_dir / "favicon-48.png", optimize=True)
    icons[64].resize((512, 512), Image.Resampling.NEAREST).save(
        args.public_dir / "favicon.png", optimize=True
    )
    icons[60].resize((180, 180), Image.Resampling.NEAREST).save(
        args.public_dir / "apple-touch-icon.png", optimize=True
    )
    write_ico(args.public_dir / "favicon.ico", [icons[16], icons[32], icons[48]])
    make_preview(args.preview, icons)


if __name__ == "__main__":
    main()
