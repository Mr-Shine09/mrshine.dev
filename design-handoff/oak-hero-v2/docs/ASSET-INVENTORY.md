# Asset Inventory

> Historical record only. Runtime assets moved to
> `site/public/assets/animation/`; start with `ANIMATION_ASSETS.md`. Paths below
> may describe removed authoring/QA files and must not be used by page code.

## Mascot

| File | Format / size | Role |
| --- | --- | --- |
| `assets/mascot/oak-welcome-atlas.png` | RGBA PNG, 2080 × 208 | Production atlas: 13 cells at 160 × 208 |
| `assets/mascot/oak-welcome-contract.json` | JSON | Canonical geometry, timing, frame intent, bubble window, reduced-motion frame |
| `assets/mascot/oak-welcome-static.png` | RGBA PNG, 160 × 208 | No-JS/reduced-motion static fallback |
| `assets/mascot/oak-base-transparent.png` | RGBA PNG, 1254 × 1254 | High-resolution canonical character reference |
| `assets/mascot/frames/*.png` | 13 RGBA PNGs, 160 × 208 | Debugging or `<img>`-swap renderer |
| `assets/mascot/welcome-bubble.svg` | SVG, 192 × 96 | Compact light bubble visual reference |
| `assets/mascot/welcome-bubble-dark.svg` | SVG, 192 × 96 | Compact dark bubble visual reference |

The atlas and frames have hard alpha values only. Use the atlas for the website
unless the implementation deliberately chooses `<img>` frame swapping.

## Cursor and reveal

| File | Native size | Role |
| --- | ---: | --- |
| `assets/cursor/pixel-arrow-on-light.svg` | 32 × 32 | Arrow over light surfaces; hotspot `3 3` |
| `assets/cursor/pixel-arrow-on-dark.svg` | 32 × 32 | Arrow over dark surfaces; hotspot `3 3` |
| `assets/cursor/ripple-square-light-theme.svg` | 128 × 128 | Light-theme composite shockwave |
| `assets/cursor/ripple-square-dark-theme.svg` | 128 × 128 | Dark-theme composite shockwave |
| `assets/cursor/ripple-ring-unit.svg` | 64 × 64 | Reusable independent square ring |
| `assets/cursor/star-grid-light-theme.svg` | 128 × 128 | Seamless space-grid tile for light pages |
| `assets/cursor/star-grid-dark-theme.svg` | 128 × 128 | Seamless space-grid tile for dark pages |

## QA and source material

- `assets/previews/oak-welcome-loop.gif` — timed 2× animation preview.
- `assets/previews/oak-welcome-inspection-1s.gif` — diagnostic preview with a
  one-second hold, frame number, hair-height, waist, and baseline guides.
- `assets/previews/oak-welcome-contact-sheet.png` — alternating light/dark QA.
- `assets/previews/oak-welcome-1x-contact-sheet.png` — native-size light/dark QA.
- `assets/previews/oak-welcome-silhouettes.png` — native-size motion silhouette QA.
- `assets/previews/oak-welcome-frames-02-04-calibration.png` — 3× waist and
  baseline comparison for the repaired early transition.
- `assets/mascot/source/*-chroma.png` — retained generation sources; do not ship.
- `assets/mascot/source/*-transparent.png` — cleaned full-sheet source; do not ship.
- `tools/build_mascot_assets.py` — deterministic crop, baseline, atlas, contract,
  contact-sheet, and GIF builder.

Recommended production copy: atlas, contract, static image, bubble shapes, and
the seven cursor SVGs. Keep the rest with the design handoff rather than the
public website bundle.
