#!/usr/bin/env python3
"""Validate dimensions, frame counts, transparency, and chroma cleanup."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1] / "public" / "animations" / "oak-scenes"
CONTRACT = json.loads((ROOT / "scene-contract.json").read_text())


def main() -> None:
    expected_size = tuple(CONTRACT["layout"]["outputFrameSize"])
    expected_count = int(CONTRACT["layout"]["frameCount"])
    results = []
    errors = []

    for scene in CONTRACT["scenes"]:
        scene_id = scene["id"]
        frames = sorted((ROOT / "frames" / scene_id).glob(f"{scene_id}-*.png"))
        if len(frames) != expected_count:
            errors.append(f"{scene_id}: expected {expected_count} frame PNGs, found {len(frames)}")

        transparent_corners = 0
        opaque_pixels = 0
        greenish_pixels = 0
        for path in frames:
            image = Image.open(path).convert("RGBA")
            if image.size != expected_size:
                errors.append(f"{path.name}: expected {expected_size}, found {image.size}")
            alpha = image.getchannel("A")
            corners = [alpha.getpixel((0, 0)), alpha.getpixel((image.width - 1, 0)), alpha.getpixel((0, image.height - 1)), alpha.getpixel((image.width - 1, image.height - 1))]
            transparent_corners += sum(value == 0 for value in corners)
            for red, green, blue, value in image.get_flattened_data():
                if value == 0:
                    continue
                opaque_pixels += 1
                if green > 210 and green > red * 1.7 and green > blue * 1.7:
                    greenish_pixels += 1

        animated = Image.open(ROOT / f"{scene_id}.webp")
        animated_count = getattr(animated, "n_frames", 1)
        if animated_count != expected_count:
            errors.append(f"{scene_id}.webp: expected {expected_count} frames, found {animated_count}")

        atlas = Image.open(ROOT / f"{scene_id}-atlas.png")
        expected_atlas = (expected_size[0] * expected_count, expected_size[1])
        if atlas.size != expected_atlas:
            errors.append(f"{scene_id}-atlas.png: expected {expected_atlas}, found {atlas.size}")

        results.append({
            "id": scene_id,
            "frameCount": len(frames),
            "animatedWebpFrames": animated_count,
            "transparentCornerChecksPassed": transparent_corners,
            "transparentCornerChecksTotal": len(frames) * 4,
            "opaquePixels": opaque_pixels,
            "greenishOpaquePixels": greenish_pixels,
        })

    report = {"ok": not errors, "errors": errors, "scenes": results}
    report_path = ROOT / "previews" / "validation.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(report_path)
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
