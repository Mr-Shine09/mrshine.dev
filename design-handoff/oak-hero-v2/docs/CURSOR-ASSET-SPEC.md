# Cursor and Star-Grid Asset Specification

> Historical record only. Runtime assets moved to
> `site/public/assets/animation/`; start with `ANIMATION_ASSETS.md`. Paths below
> may describe removed authoring/QA files and must not be used by page code.

This package is a visual handoff only. It does not modify or prescribe changes to the live portfolio.

## Asset inventory

| Asset | Native size | Intended use |
| --- | ---: | --- |
| `pixel-arrow-on-light.svg` | 32 × 32 px | Custom pointer on light surfaces |
| `pixel-arrow-on-dark.svg` | 32 × 32 px | Custom pointer on dark surfaces |
| `ripple-square-light-theme.svg` | 128 × 128 px | Complete pixel shockwave on light-theme pages |
| `ripple-square-dark-theme.svg` | 128 × 128 px | Complete pixel shockwave on dark-theme pages |
| `ripple-ring-unit.svg` | 64 × 64 px | Theme-neutral cyan ring for independently timed ripple instances |
| `star-grid-light-theme.svg` | 128 × 128 px | Seamless dark-space reveal tile with enough contrast for a light page |
| `star-grid-dark-theme.svg` | 128 × 128 px | Brighter indigo-space reveal tile that separates from a dark page |

All assets use integer coordinates and `shape-rendering="crispEdges"`. Do not run them through an optimizer that converts their paths to fractional coordinates.

## Pixel arrow

- CSS cursor hotspot: **3 3** (x y, measured from the SVG's top-left corner).
- Preferred rendered size: **32 × 32 CSS px** at 1× and 2× device pixel ratios. Browsers rasterize the SVG at the correct output scale.
- The on-light variant has a near-black shell, white inset, and cyan interaction accent.
- The on-dark variant has a near-white shell, near-black border, and the same cyan accent.
- Keep the browser cursor fallback last in the declaration. The equivalent consumer-side syntax is `url("…/pixel-arrow-on-light.svg") 3 3, auto`.
- Use the native system pointer over text inputs, editable content, resize handles, drag regions, and any control whose cursor communicates a distinct behavior. Do not replace those affordances with the decorative arrow.

## Reveal mask and layer order

The intended result is a circular window into a star-grid layer, centered under the pointer. The mask itself should be made in CSS or Canvas; there is intentionally no pre-baked circle in the tile.

Recommended visual stack, from back to front:

1. Existing page background.
2. Theme-specific star-grid tile, clipped to a circular mask approximately **220–300 CSS px** in diameter.
3. Pixel-square shockwaves, centered at the pointer's position at the moment they are emitted.
4. Page content and interactive controls.
5. Custom pixel arrow.

The visual reveal and ripples must not create a hit-testing layer. Any implementation wrapper should be excluded from the accessibility tree and ignore pointer events.

The star-grid assets are repeatable 128 px tiles. Keep `background-size: 128px 128px` or an exact integer multiple to preserve sharp pixels. Anchor the grid to the viewport rather than the cursor so the mask appears to reveal a stable space behind the page instead of carrying the stars around.

## Pixel-square shockwave motion

`ripple-square-*-theme.svg` contains separately named SVG groups: `ring-inner`, `ring-middle`, `ring-outer`, and `origin`. This supports either a one-piece image animation or inline-SVG sequencing. `ripple-ring-unit.svg` is useful when the implementation prefers to emit multiple independent elements.

Suggested motion recipe:

- Emit no more than one movement ripple every **70–100 ms** and use distance gating of roughly **18–24 px** to prevent a dense trail.
- Start at 0.35–0.5 scale and expand to 1.25–1.5 scale over **420–560 ms**.
- Hold opacity briefly, then fade to zero during the final 60% of the animation.
- Use stepped easing (`steps(6, end)` or `steps(8, end)`) to retain the pixel-square character.
- A click may create one larger, brighter shockwave lasting **550–700 ms**.
- Cap the live ripple pool (for example, 8–12 instances) and reuse nodes/canvas objects rather than allowing unbounded creation.

The SVG rings already encode decreasing opacity from the center outward. Avoid blur, drop-shadow, and continuous filter animation; these soften the pixel language and increase paint cost.

## Theme and contrast behavior

- On a light page, select `pixel-arrow-on-light.svg`, `ripple-square-light-theme.svg`, and `star-grid-light-theme.svg`.
- On a dark page, select `pixel-arrow-on-dark.svg`, `ripple-square-dark-theme.svg`, and `star-grid-dark-theme.svg`.
- The two star-grid tiles intentionally differ in surface value: the light-theme tile is dark enough to read as a reveal; the dark-theme tile is brighter and more saturated so the reveal remains visible against an already dark page.
- Re-evaluate the automatic selection when the site's theme changes. If a section overrides the page theme, base cursor selection on the actual surface beneath the pointer where practical.

Palette tokens:

| Role | Hex |
| --- | --- |
| Deep space | `#10172B` |
| Lifted dark-space surface | `#182247` |
| Cursor near-black | `#0B1020` |
| White | `#F8FAFC` / `#FFFFFF` |
| Electric cyan | `#38E8FF` |
| Light-theme ripple blue | `#2563EB` |
| Violet star/ripple accent | `#A78BFA` / `#C4B5FD` |

## Accessibility and input fallbacks

- The effect is decorative. It must not convey information, selection state, or focus by itself.
- Preserve the visible keyboard focus style on every interactive element.
- Honor `prefers-reduced-motion: reduce`: disable movement-emitted ripples, remove stepped expansion, and either show a static reveal disk or disable the reveal. A single short click response is acceptable only if it does not scale or flash aggressively.
- Honor `forced-colors: active`: disable the decorative cursor and reveal, returning to the system cursor.
- Do not apply a custom cursor for coarse or hoverless pointers. Treat `(pointer: coarse)`, `(hover: none)`, touch events, and pen-first devices as system-cursor/static-background experiences.
- If JavaScript is unavailable, the normal browser cursor and original page background must remain fully functional.
- Avoid rapid high-contrast flashes. The ripple should change spatially and fade; it should not alternate between bright and dark states.

## Handoff acceptance checks

- Cursor arrow tip lands on the target with hotspot `3 3` at 100%, 125%, and 200% browser zoom.
- The arrow remains visible over the brightest and darkest sections of each theme.
- The star grid stays fixed while the circular mask moves.
- Ripple emission does not obscure text or block clicks.
- Motion stops when the page is hidden and resumes without releasing a burst of queued ripples.
- Reduced-motion, forced-colors, keyboard-only, touch, and pen behavior all retain native usability.
