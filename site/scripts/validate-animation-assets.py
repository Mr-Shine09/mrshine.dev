#!/usr/bin/env python3
"""Validate the canonical runtime animation atlases and contracts."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1] / "public" / "assets" / "animation"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def require_image(path: Path, expected_size: tuple[int, int], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing image: {path.relative_to(ROOT)}")
        return
    with Image.open(path) as image:
        if image.size != expected_size:
            errors.append(
                f"{path.relative_to(ROOT)}: expected {expected_size}, found {image.size}"
            )
        if image.mode not in {"RGBA", "LA", "P"}:
            errors.append(
                f"{path.relative_to(ROOT)}: expected alpha-capable mode, found {image.mode}"
            )


def main() -> None:
    errors: list[str] = []

    scene_contract = read_json(ROOT / "scenes" / "scene-contract.json")
    layout = scene_contract["layout"]
    frame_count = int(layout["frameCount"])
    frame_w, frame_h = (int(value) for value in layout["outputFrameSize"])
    if frame_count != int(layout["columns"]) * int(layout["rows"]):
        errors.append("scene contract frame count does not match its source-board grid")
    if len(scene_contract["scenes"]) != 6:
        errors.append(f"expected 6 approved scenes, found {len(scene_contract['scenes'])}")

    seen_ids: set[str] = set()
    for scene in scene_contract["scenes"]:
        scene_id = str(scene["id"])
        if scene_id in seen_ids:
            errors.append(f"duplicate scene id: {scene_id}")
        seen_ids.add(scene_id)
        if len(scene["durationsMs"]) != frame_count:
            errors.append(
                f"{scene_id}: expected {frame_count} durations, "
                f"found {len(scene['durationsMs'])}"
            )
        require_image(
            ROOT / "scenes" / f"{scene_id}-atlas.png",
            (frame_w * frame_count, frame_h),
            errors,
        )

    hero_contract = read_json(ROOT / "hero" / "oak-welcome-contract.json")
    hero_size = tuple(int(value) for value in hero_contract["atlas"]["pixel_size"])
    hero_cell = tuple(
        int(value) for value in hero_contract["atlas"]["cell_pixel_size"]
    )
    require_image(ROOT / "hero" / hero_contract["asset"], hero_size, errors)
    require_image(ROOT / "hero" / "oak-welcome-static.png", hero_cell, errors)
    if len(hero_contract["sequence"]["frames"]) != len(
        hero_contract["sequence"]["durations_ms"]
    ):
        errors.append("Hero frame and duration counts differ")

    legacy_contract = read_json(ROOT / "legacy" / "mascot-contract.json")
    legacy_size = tuple(
        int(value) for value in legacy_contract["atlas"]["pixel_size"]
    )
    require_image(ROOT / "legacy" / legacy_contract["asset"], legacy_size, errors)

    forbidden = sorted(
        path.relative_to(ROOT)
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".gif", ".webp"}
    )
    if forbidden:
        errors.append(
            "redundant runtime formats found: " + ", ".join(map(str, forbidden))
        )

    if errors:
        raise SystemExit("\n".join(errors))

    print(
        f"OK: {len(scene_contract['scenes'])} scene atlases, Hero V2, "
        "and legacy mascot assets are canonical and valid"
    )


if __name__ == "__main__":
    main()
