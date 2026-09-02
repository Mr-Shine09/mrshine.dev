#!/usr/bin/env python3
"""Validate the canonical APNG animation assets and their static fallbacks."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1] / "public" / "assets" / "animation"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def require_static(path: Path, expected_size: tuple[int, int], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing image: {path.relative_to(ROOT)}")
        return
    with Image.open(path) as image:
        if image.size != expected_size:
            errors.append(
                f"{path.relative_to(ROOT)}: expected {expected_size}, found {image.size}"
            )
        if getattr(image, "n_frames", 1) != 1:
            errors.append(f"{path.relative_to(ROOT)}: static fallback is animated")
        if "A" not in image.convert("RGBA").getbands():
            errors.append(f"{path.relative_to(ROOT)}: static fallback lacks alpha")


def require_apng(
    path: Path,
    expected_size: tuple[int, int],
    expected_frames: int,
    expected_durations: list[int],
    errors: list[str],
) -> None:
    if not path.exists():
        errors.append(f"missing image: {path.relative_to(ROOT)}")
        return
    with Image.open(path) as image:
        label = path.relative_to(ROOT)
        if image.size != expected_size:
            errors.append(f"{label}: expected {expected_size}, found {image.size}")
        frame_count = getattr(image, "n_frames", 1)
        if frame_count != expected_frames:
            errors.append(f"{label}: expected {expected_frames} APNG frames, found {frame_count}")
            return

        signatures: list[bytes] = []
        for index in range(frame_count):
            image.seek(index)
            frame = image.convert("RGBA")
            alpha_values = {value for _count, value in (frame.getchannel("A").getcolors(256) or [])}
            if not alpha_values.issubset({0, 255}):
                errors.append(f"{label}: frame {index} contains semitransparent pixels")
            if frame.getcolors(66) is None:
                errors.append(f"{label}: frame {index} exceeds the 64-color production palette")
            transparent_colors = {
                color
                for _count, color in (frame.getcolors(frame.width * frame.height) or [])
                if color[3] == 0
            }
            if transparent_colors - {(0, 0, 0, 0)}:
                errors.append(f"{label}: frame {index} retains RGB data under transparency")
            duration = float(image.info.get("duration", 0))
            if abs(duration - expected_durations[index]) > 1.1:
                errors.append(
                    f"{label}: frame {index} expected {expected_durations[index]}ms, found {duration}ms"
                )
            signatures.append(frame.tobytes())
        if len(set(signatures)) != frame_count:
            errors.append(f"{label}: one or more animation frames are exact duplicates")


def main() -> None:
    errors: list[str] = []

    scene_contract = read_json(ROOT / "scenes" / "scene-contract.json")
    layout = scene_contract["layout"]
    frame_count = int(layout["frameCount"])
    frame_size = tuple(int(value) for value in layout["outputFrameSize"])
    if layout.get("format") != "apng":
        errors.append("scene contract must declare APNG format")
    if len(scene_contract["scenes"]) != 7:
        errors.append(f"expected 7 active scenes, found {len(scene_contract['scenes'])}")

    seen_ids: set[str] = set()
    for scene in scene_contract["scenes"]:
        scene_id = str(scene["id"])
        if scene_id in seen_ids:
            errors.append(f"duplicate scene id: {scene_id}")
        seen_ids.add(scene_id)
        durations = [int(value) for value in scene["durationsMs"]]
        if len(durations) != frame_count:
            errors.append(
                f"{scene_id}: expected {frame_count} durations, found {len(durations)}"
            )
            continue
        require_apng(
            ROOT / "scenes" / scene["asset"],
            frame_size,
            frame_count,
            durations,
            errors,
        )
        require_static(ROOT / "scenes" / scene["staticAsset"], frame_size, errors)

    retired = ROOT / "scenes" / "run-trip-recover-atlas.png"
    if retired.exists():
        errors.append("retired run-trip-recover atlas is still present in the public runtime")
    if "run" not in seen_ids or "run-trip-recover" in seen_ids:
        errors.append("scene contract must use run and exclude run-trip-recover")
    if "trophy-lift" not in seen_ids:
        errors.append("scene contract must include the Achievement trophy-lift scene")

    hero_contract = read_json(ROOT / "hero" / "oak-welcome-contract.json")
    hero_size = tuple(int(value) for value in hero_contract["animation"]["pixel_size"])
    hero_count = int(hero_contract["animation"]["frame_count"])
    hero_durations = [int(value) for value in hero_contract["sequence"]["durations_ms"]]
    require_apng(
        ROOT / "hero" / hero_contract["asset"],
        hero_size,
        hero_count,
        hero_durations,
        errors,
    )
    require_static(ROOT / "hero" / hero_contract["static_asset"], hero_size, errors)

    legacy_contract = read_json(ROOT / "legacy" / "mascot-contract.json")
    legacy_size = tuple(int(value) for value in legacy_contract["atlas"]["pixel_size"])
    require_static(ROOT / "legacy" / legacy_contract["asset"], legacy_size, errors)

    forbidden = sorted(
        path.relative_to(ROOT)
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".gif", ".webp"}
    )
    if forbidden:
        errors.append("redundant runtime formats found: " + ", ".join(map(str, forbidden)))

    if errors:
        raise SystemExit("\n".join(errors))

    print(
        f"OK: {len(scene_contract['scenes'])} APNG scenes, Hero welcome, "
        "hard alpha, unique frames, static fallbacks, and legacy compatibility"
    )


if __name__ == "__main__":
    main()
