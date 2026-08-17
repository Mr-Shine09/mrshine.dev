#!/usr/bin/env python3
"""Build the deterministic Oak Hero V2 frame, atlas, preview, and QA assets."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/mascot/source/oak-welcome-12-source-transparent.png"
RISE_SOURCE = ROOT / "assets/mascot/source/oak-wave-rise-3-source-transparent.png"
RISE_REPLACEMENT_SOURCE = ROOT / "assets/mascot/source/oak-wave-rise-frames-02-03-v2-transparent.png"
FRAME_04_REPLACEMENT_SOURCE = ROOT / "assets/mascot/source/oak-frame-04-replacement-transparent.png"
FRAMES = ROOT / "assets/mascot/frames"
ATLAS = ROOT / "assets/mascot/oak-welcome-atlas.png"
STATIC = ROOT / "assets/mascot/oak-welcome-static.png"
CONTACT = ROOT / "assets/previews/oak-welcome-contact-sheet.png"
CONTACT_1X = ROOT / "assets/previews/oak-welcome-1x-contact-sheet.png"
SILHOUETTES = ROOT / "assets/previews/oak-welcome-silhouettes.png"
PREVIEW = ROOT / "assets/previews/oak-welcome-loop.gif"
INSPECTION_PREVIEW = ROOT / "assets/previews/oak-welcome-inspection-1s.gif"
CONTRACT = ROOT / "assets/mascot/oak-welcome-contract.json"

SOURCE_COLS, SOURCE_ROWS = 4, 3
CONTACT_COLS = 4
CELL_W, CELL_H = 160, 208
ANCHOR_X, BASELINE_Y = 80, 204
TARGET_BODY_HEIGHT = 192
REFERENCE_WAIST_Y = 118
DURATIONS = [700, 180, 180, 180, 160, 120, 140, 140, 260, 260, 160, 160, 1100]
# The generated storyboard uses a visually even grid, but the tallest first-row
# poses extend below the mathematical one-third boundary. These measured gaps
# fall in the actual chroma-only space between pose rows.
ROW_BOUNDARY_RATIOS = [0.0, 450 / 1254, 860 / 1254, 1.0]
# The storyboard's third row was generated at a slightly smaller body scale.
# Correct that source variation before pinning all poses to the shared baseline.
SCALE_CORRECTIONS = [1.0] * 8 + [1.12] * 4


def harden_alpha(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    alpha = image.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
    image.putalpha(alpha)
    return image


def extract_storyboard_frames(source: Image.Image) -> list[Image.Image]:
    isolated: list[Image.Image] = []
    for row in range(SOURCE_ROWS):
        top = round(ROW_BOUNDARY_RATIOS[row] * source.height)
        bottom = round(ROW_BOUNDARY_RATIOS[row + 1] * source.height)
        for col in range(SOURCE_COLS):
            left = round(col * source.width / SOURCE_COLS)
            right = round((col + 1) * source.width / SOURCE_COLS)
            slot = harden_alpha(source.crop((left, top, right, bottom)))
            bbox = slot.getchannel("A").getbbox()
            if bbox is None:
                raise RuntimeError(f"empty storyboard slot at row={row}, col={col}")
            isolated.append(slot.crop(bbox))

    max_w = max(image.width for image in isolated)
    max_h = max(image.height for image in isolated)
    shared_scale = min((CELL_W - 8) / max_w, (CELL_H - 8) / max_h)

    frames: list[Image.Image] = []
    for index, pose in enumerate(isolated):
        corrected_scale = shared_scale * SCALE_CORRECTIONS[index]
        width = max(1, round(pose.width * corrected_scale))
        height = max(1, round(pose.height * corrected_scale))
        pose = pose.resize((width, height), Image.Resampling.NEAREST)
        frame = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
        x = (CELL_W - width) // 2
        y = CELL_H - 4 - height
        frame.alpha_composite(pose, (x, y))
        frames.append(frame)
    return frames


def extract_horizontal_frames(
    source: Image.Image, frame_count: int, target_height: int
) -> list[Image.Image]:
    isolated: list[Image.Image] = []
    for col in range(frame_count):
        left = round(col * source.width / frame_count)
        right = round((col + 1) * source.width / frame_count)
        slot = harden_alpha(source.crop((left, 0, right, source.height)))
        bbox = slot.getchannel("A").getbbox()
        if bbox is None:
            raise RuntimeError(f"empty horizontal source slot at col={col}")
        isolated.append(slot.crop(bbox))

    shared_scale = target_height / isolated[0].height
    frames: list[Image.Image] = []
    for pose in isolated:
        width = max(1, round(pose.width * shared_scale))
        height = max(1, round(pose.height * shared_scale))
        if width > CELL_W - 8 or height > CELL_H - 8:
            fit = min((CELL_W - 8) / width, (CELL_H - 8) / height)
            width = max(1, round(width * fit))
            height = max(1, round(height * fit))
        pose = pose.resize((width, height), Image.Resampling.NEAREST)
        frame = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
        frame.alpha_composite(pose, ((CELL_W - width) // 2, CELL_H - 4 - height))
        frames.append(frame)
    return frames


def body_height(frame: Image.Image) -> int:
    """Measure hair-to-shoe height without treating tiny sparkles as the top."""
    alpha = frame.getchannel("A")
    full_bbox = alpha.getbbox()
    if full_bbox is None:
        raise RuntimeError("cannot measure an empty frame")
    central_row_counts = [
        sum(1 for x in range(60, 100) if alpha.getpixel((x, y)) >= 128)
        for y in range(CELL_H)
    ]
    body_top = next((y for y, count in enumerate(central_row_counts) if count >= 8), None)
    if body_top is None:
        raise RuntimeError("could not locate central body silhouette")
    return full_bbox[3] - body_top


def normalize_body_scale(frame: Image.Image) -> Image.Image:
    """Uniformly scale a pose about the shared center/baseline body anchor."""
    frame = harden_alpha(frame)
    bbox = frame.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("cannot normalize an empty frame")
    scale = TARGET_BODY_HEIGHT / body_height(frame)
    pose = frame.crop(bbox)
    width = max(1, round(pose.width * scale))
    height = max(1, round(pose.height * scale))
    pose = pose.resize((width, height), Image.Resampling.NEAREST)
    normalized = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    x = round(ANCHOR_X + (bbox[0] - ANCHOR_X) * scale)
    y = BASELINE_Y - height
    normalized.alpha_composite(pose, (x, y))
    return harden_alpha(normalized)


def make_atlas(frames: list[Image.Image]) -> Image.Image:
    atlas = Image.new("RGBA", (CELL_W * len(frames), CELL_H), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        atlas.alpha_composite(frame, (index * CELL_W, 0))
    return atlas


def font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSansMono-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def compose_preview_stage(frame: Image.Image, index: int, background: str | None) -> Image.Image:
    scale = 2
    stage = Image.new("RGBA", (480, CELL_H * scale), background or (0, 0, 0, 0))
    stage.alpha_composite(frame.resize((CELL_W * scale, CELL_H * scale), Image.Resampling.NEAREST), (160, 0))
    if 3 <= index <= 11:
        light_surface = background == "#f8fafc"
        fill = "#111827" if light_surface else "#f8fafc"
        ink = "#f8fafc" if light_surface else "#111827"
        draw = ImageDraw.Draw(stage)
        draw.rectangle((18, 30, 178, 88), fill=fill)
        draw.rectangle((26, 24, 170, 96), fill=fill)
        draw.polygon([(146, 88), (184, 88), (174, 116)], fill=fill)
        draw.text((98, 60), "WELCOME", anchor="mm", fill=ink, font=font(18))
    return stage


def compose_inspection_stage(frame: Image.Image, index: int, frame_count: int) -> Image.Image:
    """Render a labeled fixed-background frame with top/baseline QA guides."""
    scale = 2
    y_offset = 48
    stage = Image.new("RGBA", (480, 480), "#e2e8f0")
    draw = ImageDraw.Draw(stage)
    top_guide = y_offset + (BASELINE_Y - TARGET_BODY_HEIGHT) * scale
    waist_guide = y_offset + REFERENCE_WAIST_Y * scale
    baseline_guide = y_offset + BASELINE_Y * scale
    draw.line((0, top_guide, 479, top_guide), fill="#0891b2", width=1)
    draw.line((0, waist_guide, 479, waist_guide), fill="#d97706", width=1)
    draw.line((0, baseline_guide, 479, baseline_guide), fill="#e11d48", width=1)
    stage.alpha_composite(
        frame.resize((CELL_W * scale, CELL_H * scale), Image.Resampling.NEAREST),
        (80, y_offset),
    )
    draw.rectangle((8, 8, 238, 36), fill="#111827")
    draw.text(
        (16, 14),
        f"FRAME {index + 1:02d}/{frame_count:02d}  1000 ms",
        fill="#f8fafc",
        font=font(16),
    )
    draw.text(
        (258, 16),
        "CYAN top  GOLD waist  RED base",
        fill="#111827",
        font=font(10),
    )
    return stage


def make_contact_sheet(frames: list[Image.Image]) -> Image.Image:
    scale = 2
    gap = 12
    label_h = 30
    panel_w = 480
    panel_h = CELL_H * scale
    contact_rows = math.ceil(len(frames) / CONTACT_COLS)
    sheet = Image.new(
        "RGB",
        (
            gap + CONTACT_COLS * (panel_w + gap),
            gap + contact_rows * (panel_h + label_h + gap),
        ),
        "#0f172a",
    )
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        col, row = index % CONTACT_COLS, index // CONTACT_COLS
        x = gap + col * (panel_w + gap)
        y = gap + row * (panel_h + label_h + gap)
        bg = "#f8fafc" if index % 2 == 0 else "#111827"
        panel = compose_preview_stage(frame, index, bg)
        sheet.paste(panel.convert("RGB"), (x, y))
        draw.text(
            (x + 6, y + panel_h + 5),
            f"FRAME {index:02d}  {DURATIONS[index]} ms",
            fill="#f8fafc",
            font=font(16),
        )
    return sheet


def make_qa_strip(frames: list[Image.Image], silhouettes: bool) -> Image.Image:
    cols = 7
    rows = math.ceil(len(frames) / cols)
    gap = 4
    sheet = Image.new(
        "RGB",
        (gap + cols * (CELL_W + gap), gap + rows * (CELL_H + gap)),
        "#64748b",
    )
    for index, frame in enumerate(frames):
        x = gap + (index % cols) * (CELL_W + gap)
        y = gap + (index // cols) * (CELL_H + gap)
        background = "#f8fafc" if index % 2 == 0 else "#111827"
        panel = Image.new("RGBA", (CELL_W, CELL_H), background)
        if silhouettes:
            ink = (15, 23, 42, 0) if index % 2 == 0 else (248, 250, 252, 0)
            silhouette = Image.new("RGBA", frame.size, ink)
            silhouette.putalpha(frame.getchannel("A"))
            panel.alpha_composite(silhouette)
        else:
            panel.alpha_composite(frame)
        sheet.paste(panel.convert("RGB"), (x, y))
    return sheet


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    original_frames = extract_storyboard_frames(source)
    neutral_height = original_frames[0].getchannel("A").getbbox()[3] - original_frames[0].getchannel("A").getbbox()[1]
    rise_source = Image.open(RISE_SOURCE).convert("RGBA")
    rise_frames = extract_horizontal_frames(rise_source, 3, neutral_height)
    replacement_source = Image.open(RISE_REPLACEMENT_SOURCE).convert("RGBA")
    replacement_frames = extract_horizontal_frames(replacement_source, 2, neutral_height)
    rise_frames[:2] = replacement_frames
    frame_04_source = Image.open(FRAME_04_REPLACEMENT_SOURCE).convert("RGBA")
    frame_04_replacement = extract_horizontal_frames(frame_04_source, 1, neutral_height)
    rise_frames[2] = frame_04_replacement[0]

    # Keep the original neutral, add three gradual viewer-right arm rises,
    # Keep original frame 1 because it continues the same viewer-right arm.
    # Remove original frame 2 (the missed opposite-arm high pose), retain
    # original frames 3–9, remove original frame 10 (the other opposite-arm
    # gesture), and finish on original settled frame 11.
    frames = [
        original_frames[0],
        *rise_frames,
        original_frames[1],
        *original_frames[3:10],
        original_frames[11],
    ]
    frames = [normalize_body_scale(frame) for frame in frames]

    for old_frame in FRAMES.glob("oak-welcome-*.png"):
        old_frame.unlink()

    for index, frame in enumerate(frames):
        frame.save(FRAMES / f"oak-welcome-{index:02d}.png", optimize=True)

    atlas = make_atlas(frames)
    atlas.save(ATLAS, optimize=True)
    frames[11].save(STATIC, optimize=True)
    make_contact_sheet(frames).save(CONTACT, optimize=True)
    make_qa_strip(frames, silhouettes=False).save(CONTACT_1X, optimize=True)
    make_qa_strip(frames, silhouettes=True).save(SILHOUETTES, optimize=True)

    gif_frames = [compose_preview_stage(frame, index, None) for index, frame in enumerate(frames)]
    gif_frames[0].save(
        PREVIEW,
        save_all=True,
        append_images=gif_frames[1:],
        duration=DURATIONS,
        loop=0,
        disposal=2,
        transparency=0,
    )

    inspection_frames = [
        compose_inspection_stage(frame, index, len(frames))
        for index, frame in enumerate(frames)
    ]
    inspection_frames[0].save(
        INSPECTION_PREVIEW,
        save_all=True,
        append_images=inspection_frames[1:],
        duration=[1000] * len(inspection_frames),
        loop=0,
        disposal=2,
    )

    contract = {
        "schema_version": 1,
        "asset": "oak-welcome-atlas.png",
        "atlas": {
            "columns": 13,
            "rows": 1,
            "pixel_size": [CELL_W * 13, CELL_H],
            "cell_pixel_size": [CELL_W, CELL_H],
        },
        "anchor": {"x": ANCHOR_X, "baseline_y": BASELINE_Y},
        "body_height": TARGET_BODY_HEIGHT,
        "sequence": {"frames": list(range(13)), "durations_ms": DURATIONS, "loop": True},
        "speech_bubble": {"text": "WELCOME", "visible_frames": [3, 11]},
        "reduced_motion_frame": 11,
        "frame_intents": [
            "open-eyed relaxed pose",
            "waving arm begins lifting away from the hip",
            "waving hand reaches waist height",
            "waving hand reaches shoulder height",
            "waving hand reaches head height",
            "high wave outward arc",
            "high wave with warm smile",
            "eyes closing and smile broadening",
            "eyes closed with toothy smile",
            "closed-eye toothy smile with sparkle",
            "eyes reopening with sparkle",
            "open-eyed final wave",
            "open-eyed settled pose",
        ],
    }
    CONTRACT.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
