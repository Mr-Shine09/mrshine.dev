# QA Report

> Historical record only. Runtime assets moved to
> `site/public/assets/animation/`; start with `ANIMATION_ASSETS.md`. Paths below
> may describe removed authoring/QA files and must not be used by page code.

Date: 2026-08-16

## Automated checks

- 13 frame PNGs found; each is RGBA and 160 × 208 px.
- Production atlas is RGBA and 2080 × 208 px.
- Frame and atlas alpha values are hard `0` or `255` only.
- Atlas corner pixels are fully transparent.
- Animation GIF contains 13 frames.
- Mascot JSON parses successfully.
- All nine SVG assets pass XML validation.

## Visual checks

- Identity, glasses, hair, navy/white pullover, gray pants, belt, and sneakers
  remain consistent.
- Third-row source poses were normalized by 1.12× to correct a generated scale
  drift; all production frames now share baseline y=204.
- Final normalization measures the central hair-to-shoe body independently of
  raised hands and sparkles. Every frame is exactly 192 logical pixels tall
  against the shared y=204 baseline.
- Displayed frames 2 and 3 were regenerated against the neutral and adjacent
  production frames to correct their separate-source head/body proportions.
  Their body silhouettes now use the production identity lock before the same
  deterministic height/baseline normalization.
- Displayed frame 4 was regenerated against frame 3 to repair its short-torso,
  long-leg proportion. Its detected belt center is now y=114 instead of y=103.
- Three new in-betweens show the same viewer-right waving arm moving from the
  hip through waist and shoulder height before the high wave.
- Both opposite-arm source poses are excluded from the production sequence,
  including the previously missed sixth displayed pose.
- No clipped feet, leaked row fragments, green background, or guide marks.
- Light/dark 1× contact sheets and silhouette sheets retain readable poses.
- Motion reads as slow arm rise → wave → closed-eye toothy smile → sparkle →
  eyes reopen → settle.
- WELCOME appears as a separate high-contrast bubble during preview frames
  3–11. Its preview footprint and supplied SVGs were reduced to a compact
  192 × 96 proportion while keeping the word readable.
- `oak-welcome-inspection-1s.gif` contains all 13 frames at exactly 1000 ms
  each, with fixed cyan hair-height, gold waist (reference y=118), and red
  shoe-baseline guides for diagnosing residual proportion changes.
- The post-repair waist test reports detected belt centers of
  `[118, 115, 114, 114, 116, 116, 116, 116, 118, 116, 121, 121, 122]`.
  Frames 2–4 are therefore within one pixel of one another, and every pose is
  within four pixels of the y=118 reference despite expression/pose changes.
- `oak-welcome-frames-02-04-calibration.png` is a dedicated 3× comparison of
  displayed frames 2, 3, and 4 against a common waist line and shoe baseline.

Final independent visual QA after the frame-4 replacement: **PASS**.

> The production atlas intentionally excludes the speech bubble and text. The
> implementation should render `WELCOME` as a separate DOM element, using the
> supplied SVG bubble shapes only as optional visual references.
