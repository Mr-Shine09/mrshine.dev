# Oak Hero V2 — Asset and Claude Code Handoff

This folder is a design handoff only. The portfolio website under `site/` was
not changed.

## Start here

1. Review `assets/previews/oak-welcome-loop.gif` and
   `assets/previews/oak-welcome-contact-sheet.png`.
   For frame-by-frame scale inspection, use
   `assets/previews/oak-welcome-inspection-1s.gif`; every pose holds for one
   second and includes fixed top/baseline guides.
2. Give Claude Code this entire `oak-hero-v2` folder.
3. Ask it to follow `docs/IMPLEMENTATION-GUIDE.md` and treat
   `assets/mascot/oak-welcome-contract.json` as the animation source of truth.
4. Use `docs/CURSOR-ASSET-SPEC.md` for cursor hotspot, theme switching,
   star-grid reveal, ripple timing, and accessibility fallbacks.

## Production-ready assets

- `assets/mascot/oak-welcome-atlas.png` — 13-frame, 2080 × 208 transparent atlas.
- `assets/mascot/oak-welcome-contract.json` — geometry, frame timing, intent,
  bubble visibility, and reduced-motion frame.
- `assets/mascot/oak-welcome-static.png` — friendly open-eyed wave fallback.
- `assets/mascot/welcome-bubble.svg` and `welcome-bubble-dark.svg` — optional
  compact 192 × 96 pixel bubble artwork. For accessibility, render the word
  `WELCOME` as real DOM text even if these shapes are used as visual references.
- `assets/cursor/*.svg` — light/dark arrows, square shockwaves, ring unit, and
  theme-specific seamless star-grid tiles.

Individual PNG frames are included for debugging and alternate renderers.
Chroma sources and the deterministic build tool are retained so the extraction
can be reproduced without regenerating the artwork.

## Art direction

Oak follows reference image 3: friendly clean pixel art, black tousled hair,
rectangular glasses, navy quarter-zip with white side panels, wide gray pants,
black belt, and blue/white sneakers. The dominant hero loop slowly raises the
same waving arm through three extra in-betweens, waves, closes its eyes, gives
a toothy smile, sparkles, reopens its eyes, and settles. The earlier
opposite-arm pose has been removed.

The loop uses non-uniform frame durations. Do not replace them with a flat FPS;
the expressive holds are what keep the motion from feeling robotic.

## Verification status

- Transparent atlas corners verified.
- All 13 frames use a common baseline, the same waving side, and an exact
  192-pixel central hair-to-shoe body height.
- Contact sheet checks both light and dark surfaces.
- Cursor SVGs pass XML validation.
- No generated text is baked into the mascot artwork.
- No files under `site/` were modified.
