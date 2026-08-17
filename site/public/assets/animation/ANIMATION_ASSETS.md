# Animation assets — start here

This is the **only canonical animation asset folder** for the website. Do not
search old preview, frame, source-board, or design-handoff directories; those
duplicates were intentionally removed.

## Runtime files and placement

| Asset | Runtime files | Website placement | Playback |
|---|---|---|---|
| Hero welcome | `hero/oak-welcome-atlas.png` + `hero/oak-welcome-contract.json` | Home page only, around the masonry grid; never replaces a tile's real image | Timed loop; use `oak-welcome-static.png` for no-JS and reduced motion |
| Reading by the fire | `scenes/reading-fire-atlas.png` | `/reading`, beside the shelf introduction | Ambient loop while visible |
| Computer working | `scenes/computer-working-atlas.png` | `/projects`, beside the page introduction | Calm loop while visible |
| Workbench zap | `scenes/workbench-zap-atlas.png` | `/projects`, beside the project-folder/deck area | Play once on first reveal, then hold the singed final pose |
| Thinking cloud | `scenes/thinking-cloud-atlas.png` | `/w-phrases`, beside the introduction | Loop while visible; cloud stays blank |
| Walking | `scenes/walking-atlas.png` | Low-speed phase of the site-wide scroll traveller | Scrub from scroll progress; flip horizontally for leftward travel |
| Run, trip, recover | `scenes/run-trip-recover-atlas.png` | Intricate phase of the site-wide scroll traveller on long pages | Smoothed scroll-scrub from right to left; no fall or dizzy state |
| Legacy mascot states | `legacy/mascot-atlas.png` + `legacy/mascot-contract.json` | Existing `Mascot.astro` calls only while the multi-page rebuild is in progress | Keep for compatibility; do not use it to invent new page placements |

All six scene timings, labels, dimensions, and IDs come from the single shared
`scenes/scene-contract.json`. There are intentionally no per-scene manifests.

## Folder meanings

- `scenes/` — approved 12-frame website scene atlases and their one contract.
- `hero/` — approved 13-frame home welcome atlas, contract, and static fallback.
- `legacy/` — the old multi-state mascot atlas required by existing components.
- `effects/` — Hero welcome bubble and cursor/ripple overlays only.
- `reference/` — the single identity reference for generating future Oak art;
  never render this file on the website.
- `authoring/` — pristine legacy atlas input for `strip-clock-overlay.js`; never
  reference it from page code.

## Code rules for Claude

1. Use `AnimatedScene.astro` for the six files in `scenes/`.
2. Use atlas PNGs plus their contracts. Do not recreate GIF, WebP, individual
   frame PNG, chroma-board, transparent-board, or contact-sheet variants.
3. Use `image-rendering: pixelated` and integer display scales.
4. Pause loops offscreen. One-shots wait until visible.
5. Under `prefers-reduced-motion: reduce`, freeze stationary scenes on a clear
   frame and hide the global scroll traveller.
6. Decorative animation must never create horizontal body scroll or cover a
   control on mobile.
7. Do not recolour the mascot or put words/icons inside the thinking cloud.

## Files intentionally removed

The old `public/animations/oak-scenes/`, `public/sprites/`, and
`design-handoff/oak-hero-v2/` image trees are retired. Their raw chroma boards,
transparent boards, extracted frame PNGs, GIFs, WebPs, contact sheets, duplicate
JSON manifests, and calibration/source images were removed because they were
not runtime inputs and made the asset choice ambiguous. Git history remains the
recovery path if an authoring artifact is ever needed again.
