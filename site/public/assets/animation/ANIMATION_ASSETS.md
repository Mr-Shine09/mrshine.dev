# Animation assets — start here

This is the only canonical runtime animation asset folder for the website.
The `*-atlas.png` names are retained as stable public URLs, but the files are
now native APNG animations rather than horizontal sprite strips.

## Runtime files and placement

| Asset | Runtime files | Website placement | Playback |
|---|---|---|---|
| Hero welcome | `hero/oak-welcome-atlas.png` + `hero/oak-welcome-static.png` | Home page beside the masonry grid | Native APNG loop; static under reduced motion and while offscreen |
| Reading by the fire | `scenes/reading-fire-atlas.png` + static companion | `/reading`, beside the shelf introduction | Ambient APNG loop while visible |
| Computer working | `scenes/computer-working-atlas.png` + static companion | `/projects`, beside the page introduction | Calm APNG loop while visible |
| Workbench zap | `scenes/workbench-zap-atlas.png` + static companion | `/projects`, beside the project deck | Play once on first reveal and hold its final pose |
| Thinking cloud | `scenes/thinking-cloud-atlas.png` + static companion | `/w-phrases`, beside the introduction | APNG loop while visible; cloud stays blank |
| Walking | `scenes/walking-atlas.png` + static companion | Short-page scroll traveller | Native APNG loop; flip horizontally for leftward travel |
| Running | `scenes/run-atlas.png` + static companion | Long-page scroll traveller | Native 12 fps APNG loop; flip horizontally for leftward travel |
| Trophy lift | `scenes/trophy-lift-atlas.png` + static companion | Achievement section | Play once on reveal, then hold the closed-eye smiling trophy pose |

The scene timings, labels, dimensions, public filenames, and IDs come from
`scenes/scene-contract.json`. The hero uses `hero/oak-welcome-contract.json`.

## Authoring and QA

- Production APNGs are 384×320 (hero: 160×208), RGBA, and contain only hard
  alpha values so edges stay crisp.
- Every scene is aligned against shared column and row anchors before export.
  Alignment guides are QA-only and never appear in production pixels.
- `scripts/refine-animation-assets.py` performs deterministic origin repair,
  palette stabilization, APNG packaging, and preview generation.
- `scripts/refine-walking-trophy.py` removes detached conversion debris from
  walking frames 5–8, restores their common baseline, and packages the
  Achievement trophy board with the production palette and alpha rules.
- The retired `run-trip-recover-atlas.png` is preserved outside the public
  runtime at `site/archive/animation/run-trip-recover-atlas.png`.

## Code rules

1. Use `AnimatedScene.astro` for the stationary APNG scenes.
2. Do not translate the APNG files as sprite sheets; each file is already an
   animation with embedded timing.
3. Keep `image-rendering: pixelated` and integer display sizes.
4. Swap looping APNGs to their static companions while offscreen.
5. Under `prefers-reduced-motion: reduce`, show static companions and hide the
   global scroll traveller.
6. Decorative animation must never create horizontal body scroll or cover a
   control on mobile.
7. Do not recolor Oak or put words/icons inside the thinking cloud.
