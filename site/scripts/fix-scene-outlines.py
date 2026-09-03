#!/usr/bin/env python3
"""Darken the pale outer rim of the mascot scenes so they sit cleanly on dark
backgrounds (Plan.md §7.7). The hero and reading-fire art already have ink
outlines; trophy-lift, workbench-zap and run had light edge pixels left from
conversion. Only pixels that are fully opaque, touch a transparent pixel, and
have mean RGB > LIGHT are recoloured to the mascot ink. Interior colours and
alpha are untouched.

Usage:
  python3 scripts/fix-scene-outlines.py          # fix in place, archive originals
  python3 scripts/fix-scene-outlines.py --check  # exit 1 if any light rim remains
"""
from __future__ import annotations
import shutil, sys
from pathlib import Path
from PIL import Image, ImageSequence

ROOT = Path(__file__).resolve().parents[1]
SCENES = ROOT / "public/assets/animation/scenes"
ARCHIVE = ROOT / "archive/animation/pre-outline-fix"
INK = (17, 18, 25, 255)
LIGHT = 150
TARGETS = ["trophy-lift", "workbench-zap", "run"]


def rim_pixels(im: Image.Image) -> list[tuple[int, int]]:
    px = im.load(); w, h = im.size; out = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a != 255 or (r + g + b) / 3 <= LIGHT:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
                    out.append((x, y)); break
    return out


def fix(im: Image.Image) -> tuple[Image.Image, int]:
    im = im.convert("RGBA"); rim = rim_pixels(im); px = im.load()
    for x, y in rim: px[x, y] = INK
    return im, len(rim)


def hard_alpha(im: Image.Image) -> bool:
    return all(a in (0, 255) for a in im.getchannel("A").getdata())


def main(check: bool) -> int:
    bad = 0
    for name in TARGETS:
        apng = SCENES / f"{name}-atlas.png"; static = SCENES / f"{name}-static.png"
        src = Image.open(apng)
        frames = [f.convert("RGBA") for f in ImageSequence.Iterator(src)]
        durations = [int(f.info.get("duration", 83)) for f in ImageSequence.Iterator(Image.open(apng))]
        if check:
            n = sum(len(rim_pixels(f)) for f in frames) + len(rim_pixels(Image.open(static).convert("RGBA")))
            print(f"{name}: {n} light rim pixels"); bad += n; continue
        ARCHIVE.mkdir(parents=True, exist_ok=True)
        for p in (apng, static):
            dest = ARCHIVE / p.name
            if not dest.exists(): shutil.copy2(p, dest)
        fixed, counts = [], 0
        for f in frames:
            g, n = fix(f); fixed.append(g); counts += n
        assert all(hard_alpha(g) for g in fixed), f"{name}: alpha is no longer hard"
        # loop=0 → infinite. trophy-lift and workbench-zap were authored loop=1; the
        # owner asked for every scene to run continuously (2 Sep 2026).
        fixed[0].save(apng, save_all=True, append_images=fixed[1:], duration=durations, loop=0, disposal=1, blend=0)
        s, n2 = fix(Image.open(static)); s.save(static)
        print(f"{name}: darkened {counts} rim pixels across {len(fixed)} frames (+{n2} static); loop=0")
    if check:
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
