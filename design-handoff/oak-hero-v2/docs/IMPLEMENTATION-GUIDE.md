# Oak Hero V2 — Claude Code Implementation Guide

> Status: design handoff only. This document does **not** modify the website.
> Every filename, dimension, duration, color, breakpoint, and component name
> labeled **Handoff recommendation** is proposed rather than an existing site
> contract. Claude Code should reconcile these recommendations with the final
> exported asset inventory before implementation.

## 1. Requested result

Replace the small, mechanical four-frame hero wave with a dominant, friendly
full-body mascot based on reference image 3. Preserve Oak's black hair,
rectangular glasses, navy quarter-zip with white side panels, loose gray pants,
and blue-and-white sneakers. The sequence loops in this exact narrative order:

1. the same waving arm slowly rises through three in-between poses;
2. friendly high wave;
3. eyes close;
4. toothy smile and a sparkle appears above the head;
5. eyes reopen while the sparkle lingers;
6. settle back into the open-eyed pose, without an opposite-arm gesture.

A separate speech bubble must contain the exact visible word **WELCOME**. Do
not bake the letters into the sprite sheet: real DOM text stays sharp,
translatable, and accessible while the mascot remains pixel art.

The cursor treatment is site-wide: a pixel arrow follows the active theme; a
mask around the pointer reveals a starry grid; movement emits restrained
pixel-square shockwaves; clicking emits a stronger burst. The effect must be
decorative and must never obstruct links, text selection, focus, or scrolling.

## 2. Compatibility with the existing Astro implementation

The current site uses:

- `site/src/components/Hero.astro` — a two-column hero with the mascot in the
  right auto-sized column;
- `site/src/components/Mascot.astro` — a CSS background-position player using
  `setTimeout`, `IntersectionObserver`, and `prefers-reduced-motion`;
- `site/src/data/mascot.ts` — reads the atlas contract and turns a single row
  into a timeline;
- `site/src/data/atlas-contract.json` — an 8-column × 16-row atlas with 96 ×
  112 px cells and a fixed baseline at y=102;
- `/sprites/atlas.png` — hard-coded in `Mascot.astro` even though `mascot.ts`
  also exposes `atlas.src`;
- `html[data-theme="light"|"dark"]` plus existing palette tokens such as
  `--bg`, `--fg`, `--navy-*`, `--paper`, and `--amber-*`.

The current hero converts the four-frame `waiting` row into
`[0,1,2,3,2,1]` at 190 ms per step. This repetition is the main source of its
robotic feel. In addition, `buildTimeline()` treats every custom sequence as a
loop, and a timeline cannot change atlas rows. It therefore cannot express the
requested wave → face change → sparkle choreography cleanly.

**Handoff recommendation:** do not replace or expand the existing shared atlas.
Keep `Mascot.astro`, `mascot.ts`, and `atlas-contract.json` working for all
non-hero states. Add an isolated hero-v2 asset, contract, and component. This
avoids changing the desktop/status mascot's state semantics and the existing
96 × 112 cell assumptions.

## 3. Recommended deliverable names and sprite contract

The following names and values are **Handoff recommendations**. If the final
asset pack uses different names or geometry, treat its generated JSON as the
source of truth and update imports only—not the values in two places.

```text
site/public/hero-v2/
  oak-welcome-atlas.png
  oak-welcome-static.png
  welcome-bubble.svg
  welcome-bubble-dark.svg
  pixel-arrow-on-light.svg
  pixel-arrow-on-dark.svg
  ripple-ring-unit.svg
  ripple-square-light-theme.svg
  ripple-square-dark-theme.svg
  star-grid-light-theme.svg
  star-grid-dark-theme.svg

site/src/data/
  oak-hero-v2-contract.json
  oak-hero-v2.ts

site/src/components/
  HeroMascotV2.astro
  SpaceCursor.astro
```

**Delivered art geometry:** one horizontal row, 13 frames, logical cell
160 × 208 px, atlas 2080 × 208 px, transparent RGBA, alpha values limited to
0 or 255, shared scale, center x=80, and baseline y=204. The supplied JSON is
the source of truth. Hair and sparkle remain inside the cell.

**Handoff recommendation — contract shape:**

```json
{
  "schema_version": 1,
  "asset": "oak-welcome-atlas.png",
  "atlas": {
    "columns": 13,
    "rows": 1,
    "pixel_size": [2080, 208],
    "cell_pixel_size": [160, 208]
  },
  "anchor": { "x": 80, "baseline_y": 204 },
  "body_height": 192,
  "sequence": {
    "frames": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "durations_ms": [700, 180, 180, 180, 160, 120, 140, 140, 260, 260, 160, 160, 1100],
    "loop": true
  },
  "speech_bubble": { "text": "WELCOME", "visible_frames": [3, 11] },
  "reduced_motion_frame": 11
}
```

**Handoff recommendation — frame intent:**

| Frame | Visual intent |
|---:|---|
| 0 | Open-eyed relaxed hold |
| 1 | Waving arm begins lifting away from the hip |
| 2 | Waving hand reaches waist height |
| 3 | Waving hand reaches shoulder height |
| 4 | Waving hand reaches head height |
| 5–6 | Two distinct same-arm high-wave poses with shoulder motion |
| 7 | Eyelids lowering; smile beginning |
| 8 | Eyes fully closed; clear white toothy smile |
| 9 | Closed-eye toothy smile; first sparkle above the head |
| 10 | Eyes reopening while the sparkle remains |
| 11 | Open-eyed final wave; reduced-motion frame |
| 12 | Settled open-eyed pose and long loop hold |

The 1.1 s final hold plus the 0.7 s opening hold creates a human pause around
the loop boundary. Use the
declared non-uniform durations; do not flatten the sequence into a constant
frame rate. If the delivered art has more frames, retain the story order and
rough timing proportions. Identity should come from silhouette, glasses,
navy/white pullover, wide pants, and sneakers—not tiny fabric detail.

## 4. Hero integration

**Handoff recommendation:** create `HeroMascotV2.astro` rather than adding
hero-only branching to `Mascot.astro`. Read geometry and timings from the v2
JSON, serialize one data payload, and expose CSS custom properties exactly as
the current renderer does. Reuse the current player's useful behavior:

- pause offscreen with `IntersectionObserver`;
- pause while `document.hidden`;
- respond live to `prefers-reduced-motion` changes;
- clean up observers, listeners, timers, and animation handles during Astro
  page transitions if those are introduced later.

The mascot sprite should remain a CSS background or an `<img>` inside a clipped
frame. In either case set:

```css
image-rendering: pixelated;
image-rendering: crisp-edges; /* harmless fallback where supported */
background-repeat: no-repeat;
```

Never apply `filter`, blur, fractional transform scaling, or a CSS transition
to `background-position`. Move between frames as discrete steps.

For a dominant hero, change the hero's visual proportions rather than only
enlarging the current right-hand auto column. **Handoff recommendation:**

```css
.hero__grid {
  grid-template-columns: minmax(0, 0.9fr) minmax(20rem, 1.1fr);
  min-height: min(52rem, calc(100svh - var(--nav-h, 3.5rem)));
}

.hero__mascot-stage {
  position: relative;
  justify-self: center;
  width: min(46vw, 36rem);
  min-height: clamp(28rem, 66svh, 44rem);
}

.hero-v2 {
  --hero-scale: 3; /* 160 × 208 logical cell renders at 480 × 624 */
  position: absolute;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
}
```

Only use integer sprite scale factors. A 160 × 208 logical cell at 3× is
480 × 624 px; at 2× it is 320 × 416 px; at 1× it is 160 × 208 px. Choose the
largest integer that fits both available width and a capped viewport height.
Do not use `transform: scale(2.6)` to force a fit.

**Handoff recommendation — responsive scale:**

- ≥ 64rem wide and ≥ 48rem tall: 3×, two-column, mascot dominant on the right;
- 46–63.99rem or short desktop viewport: 2×, two-column when it fits;
- < 46rem: one column, mascot above the copy at 2×;
- < 22rem or height-constrained landscape: 1× or use the static crop so the
  heading and first action remain visible without horizontal scrolling.

Prefer container queries or a small `ResizeObserver` choosing the discrete
scale 1/2/3 over width-only breakpoints. Confirm the mascot never covers the
hero heading, CTA focus rings, or sticky navigation.

### WELCOME speech bubble

The bubble is a sibling overlay inside `.hero__mascot-stage`, not part of the
atlas. Its source must literally be:

```astro
<p class="hero-welcome" aria-label="Welcome">WELCOME</p>
```

**Handoff recommendation:** position it above-left of the head on desktop and
above/right or centered on narrow screens. Use the existing `--surface-raised`,
`--fg`, `--rule`, and `--shadow` tokens. Build the tail with a square pseudo
element; use a 2 px hard border and no blur. Keep the bubble compact: the
delivered SVG reference is 192 × 96, and the DOM version should use roughly
`0.3rem 0.55rem` padding with `font-size: clamp(0.7rem, 0.8vw, 0.85rem)`.
The word `WELCOME` only needs to remain clearly readable; do not let the bubble
compete with the mascot or hero heading. A two-step `steps(2, end)` entrance
may accompany the first wave, but the word remains visible after entrance.
Under reduced motion, show it immediately with no transform or opacity
animation. Do not type the letters one by one.

## 5. Site-wide pixel cursor and star-grid reveal

Mount one `SpaceCursor.astro` near the end of `Base.astro` so it can span every
page. It should render two decorative fixed layers:

```astro
<div class="space-reveal" data-space-reveal aria-hidden="true"></div>
<canvas class="pixel-ripples" data-pixel-ripples aria-hidden="true"></canvas>
```

Both layers need `position: fixed; inset: 0; pointer-events: none;` and must not
be focusable. Put them above the page background but below interactive content;
establish the site's content stacking context explicitly instead of assigning
an arbitrarily high z-index to the effect.

### Pixel arrow

The delivered light/dark arrows are 32 × 32 SVGs drawn on an integer grid with
hot spot `(3, 3)`. Use the near-black arrow on light surfaces and the
near-white arrow on dark surfaces. Example wiring:

```css
@media (hover: hover) and (pointer: fine) {
  html[data-theme="light"] body {
    cursor: url("/hero-v2/pixel-arrow-on-light.svg") 3 3, default;
  }
  html[data-theme="dark"] body {
    cursor: url("/hero-v2/pixel-arrow-on-dark.svg") 3 3, default;
  }
  a, button, summary, [role="button"] { cursor: pointer; }
}
```

If custom pointer SVGs are supplied, use them on interactive controls; if not,
retain the native `pointer` cursor so affordance is never lost. Test Safari and
Chromium: cursor files must be same-origin and should remain small.

### Star-grid reveal mask

The reveal layer should be transparent outside the pointer region so the
existing `--bg` remains authoritative. Update `--pointer-x` and `--pointer-y`
from the latest pointer event, then reveal a fixed star-grid texture through a
mask centered on those coordinates.

**Handoff recommendation:** 32 px grid, major line every 4 cells, sparse 2 px
square stars, reveal radius 144 px on desktop. Keep the edge relatively hard
and pixel-like (roughly 16 px transition), not a broad glow. CSS may use a
radial mask for the reveal while the grid and stars remain square. For stricter
pixel edges, render the mask to a low-resolution offscreen canvas and upscale
with smoothing disabled.

Theme values are **Handoff recommendations** derived from existing tokens:

```css
:root {
  --space-grid: rgb(13 35 78 / 0.24);       /* navy-2 on paper */
  --space-major: rgb(27 66 139 / 0.36);     /* navy-3 */
  --space-star: rgb(167 82 33 / 0.72);      /* rust */
}
[data-theme="dark"] {
  --space-grid: rgb(246 243 228 / 0.16);    /* paper on ink */
  --space-major: rgb(255 190 75 / 0.30);    /* amber-1 */
  --space-star: rgb(255 190 75 / 0.82);
}
```

On every theme toggle, CSS variables should update automatically. If the
canvas copies computed colors, observe the `data-theme` attribute with a
`MutationObserver` and refresh its cached palette. Verify the effect remains
visible without lowering text contrast; it must sit behind content, never
between text and its background.

### Pixel-square movement shockwave and click burst

Draw ripple particles on the canvas as axis-aligned filled squares—no circles,
blur, or additive bloom. A movement shockwave is a short ring made of squares
moving away from the pointer; a click makes a larger, denser second ring.

**Handoff recommendation:**

- movement: emit only after 12 px of pointer travel or 50 ms, whichever is
  later; 8–12 squares; 280–420 ms life; 2–5 px square size; 20–46 px radius;
- click: 24–32 squares in two staggered rings; 520–700 ms life; 3–7 px square
  size; 70–110 px radius;
- cap the shared live pool at 96 particles and reuse objects rather than
  allocating per frame;
- use theme variables above, preserving at least 3:1 visibility against the
  local page background where practical;
- do not trigger on synthetic keyboard clicks (`event.detail === 0`), because
  keyboard interaction has no meaningful pointer origin.

## 6. Performance requirements

Use pointer events and store only the latest coordinates in the event handler.
Perform DOM variable updates and all drawing inside one `requestAnimationFrame`
loop. Never start one animation loop per particle or per `pointermove` event.

- Start rAF while the pointer is active or particles exist; stop it when idle.
- Size the canvas to its CSS box multiplied by
  `min(devicePixelRatio, 2)` (**Handoff recommendation: DPR cap 2**).
- On resize, resize once through `ResizeObserver` or a debounced window resize;
  preserve CSS-pixel particle coordinates and scale the drawing context.
- Disable `ctx.imageSmoothingEnabled`.
- Reuse a fixed particle pool (recommended maximum 96).
- Avoid layout reads during movement; cache bounds and use `clientX/clientY`
  for a fixed viewport canvas.
- Suspend the loop while `document.hidden` and clear expired particles on
  return.
- Do not register non-passive wheel/touch listeners. `pointermove` can be
  passive because it never calls `preventDefault()`.
- Target a steady 60 fps on an average laptop; the effect should create no
  long tasks over 50 ms and negligible CPU use when the pointer is idle.

## 7. Accessibility and input fallbacks

- The effect layers are decorative: `aria-hidden="true"`, `pointer-events:none`,
  and absent from the tab order.
- Never replace visible focus styles. The existing skip link, navigation,
  buttons, text selection, and native scrolling must continue to work.
- Use one accessible description for the mascot. Recommended: put
  `role="img" aria-label="Pixel-art mascot of Oak waving and smiling"` on the
  mascot frame. Keep the speech bubble as real text with `aria-label="Welcome"`.
  If the hero copy already says the same greeting and testing finds duplicate
  announcements noisy, make the mascot decorative rather than hiding the
  visible word.
- Under `prefers-reduced-motion: reduce`, freeze the mascot on the contract's
  `reduced_motion_frame`, show WELCOME immediately, disable movement and click
  shockwaves, and show either a static low-opacity star grid or no reveal.
- Under `forced-colors: active`, use the native cursor and disable canvas/grid
  decoration. Do not interfere with system colors.
- Under `(hover: none)` or `(pointer: coarse)`, preserve the native cursor,
  disable pointer-following and movement ripples, and avoid a permanently
  empty mask. **Handoff recommendation:** show a very faint static grid in the
  hero only; optionally allow one small burst at a tap location if it does not
  delay scrolling. Never treat touch movement as mouse hover.
- If JavaScript fails, the static mascot frame and WELCOME text must still
  render. The custom cursor and star field are progressive enhancement.

## 8. Suggested implementation order

1. Copy the delivered v2 assets into `site/public/hero-v2/` and validate actual
   dimensions/transparency against the delivered contract.
2. Add typed v2 contract access without changing `site/src/data/mascot.ts`.
3. Implement and visually test `HeroMascotV2.astro` in isolation on light and
   dark backgrounds at 1×, 2×, and 3×.
4. Replace only the hero's `<Mascot state="waiting" ... />` call with the v2
   stage and separate WELCOME bubble.
5. Adjust the hero grid for the dominant composition and all height/width
   constraints.
6. Implement `SpaceCursor.astro`, first the cursor, then reveal, then pooled
   shockwaves. Mount one instance in the base layout.
7. Test reduced motion, forced colors, keyboard-only navigation, touch/coarse
   pointer, theme toggling, page visibility, and resize.

## 9. Acceptance checklist

### Assets and animation

- [ ] Mascot unmistakably follows reference image 3 and preserves glasses,
      black hair, navy/white pullover, gray loose pants, and blue sneakers.
- [ ] Sprite cells share one origin and baseline; no foot sliding or body
      jitter during playback.
- [ ] Transparent pixels are clean; no generated green/magenta background or
      semitransparent halo remains.
- [ ] Pixel edges stay sharp at every supported size; only integer scaling is
      used and `image-rendering` is set.
- [ ] Every frame measures 192 logical pixels from central hair silhouette to
      the shared shoe baseline at y=204; the body does not grow or shrink.
- [ ] Loop reads in order: slow same-arm rise → wave → eyes close → toothy
      smile with sparkle → eyes reopen → settle.
- [ ] No opposite-arm gesture appears during the return to the settled pose.
- [ ] Wave uses distinct arm/shoulder poses, not four repeated frames.
- [ ] Timing has expressive holds and does not use one flat duration.
- [ ] Reduced motion shows a deliberate, friendly static frame.

### Hero and WELCOME bubble

- [ ] Mascot is visually dominant without hiding the heading, CTAs, nav, or
      focus rings.
- [ ] Exact visible bubble text is `WELCOME` in a separate DOM element.
- [ ] Bubble stays visually subordinate to the mascot and uses the compact
      192 × 96 reference proportion.
- [ ] Bubble has enough contrast in both themes and remains legible at 200%
      browser zoom.
- [ ] No horizontal overflow at 320 px viewport width.
- [ ] Heading and first primary action remain discoverable in short landscape
      viewports.

### Cursor, reveal, and shockwaves

- [ ] Pixel arrow has an accurate hot spot and switches with light/dark theme.
- [ ] Native pointer affordance remains on links and buttons if no custom
      pointer variant is available.
- [ ] Starry 32 px grid appears only through the pointer reveal on fine-pointer
      devices and has adequate contrast in both themes.
- [ ] Movement creates restrained square shockwaves; click produces a clearly
      stronger square burst; neither uses blurred circles.
- [ ] Effect layers never intercept clicks, selection, focus, or scroll.
- [ ] One rAF loop, DPR cap, particle pool, visibility pause, and idle stop are
      verified in DevTools.
- [ ] Theme changes update grid and particles without reload.

### Accessibility and fallbacks

- [ ] Keyboard navigation and skip link work with unchanged visible focus.
- [ ] Screen-reader output is useful and not needlessly repetitive.
- [ ] Reduced motion disables frame playback and every shockwave.
- [ ] Coarse pointer/touch uses native cursor and has a deliberate static
      fallback.
- [ ] Forced-colors mode disables nonessential visual effects.
- [ ] Without JavaScript, a static mascot and WELCOME text remain visible.

## 10. Verification evidence to capture

Before merging, save screenshots at 1440 × 900, 1024 × 768, 390 × 844, and a
short 844 × 390 landscape viewport in both themes. Record one normal-motion
loop and one reduced-motion session. In DevTools, verify no horizontal scroll,
no canvas larger than 2× DPR, no active rAF while idle/hidden, no console
errors, and no layout shift when the hero atlas loads. Also inspect the mascot
at its 1× logical size on both `--paper` and `--ink`; if identity depends on
details visible only at 3×, revise the art rather than hiding the problem with
scale.
