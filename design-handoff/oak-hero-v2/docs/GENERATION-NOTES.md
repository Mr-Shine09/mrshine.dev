# Generation Notes

The raster artwork was created with the built-in image generation path using
the user-provided `Oak's Mascot.png` as the primary style reference and
`ChatGPT Image Aug 15, 2026, 01_10_59 PM.png` as a supporting outfit reference.
The cursor and grid assets are deterministic SVGs rather than generated raster
images.

## Canonical character prompt

> Friendly clean pixel-art full-body hero mascot based on reference image 3.
> Preserve black tousled hair, black rectangular glasses, navy quarter-zip with
> white side panels, gray wide-leg trousers, black belt, and blue/white
> sneakers. Relaxed dominant hero pose, crisp clustered pixels, selective dark
> outline, no crest, briefcase, text, or scenery. Flat solid green chroma
> background with no shadows or gradients.

## Animation storyboard prompt

> Exactly 12 isolated full-body poses in an invisible 4 × 3 layout, consistent
> identity, scale, palette, and baseline. Sequence: relaxed open eyes; arm
> raises; two high-wave arcs; high wave with warm smile; eyes begin closing;
> closed eyes with toothy smile; closed-eye smile with attached pixel sparkle;
> eyes reopen with sparkle; final open-eyed wave; arm lowers; settled open-eyed
> pose. Flat green chroma background, no text, bubble, grid, shadows, scenery,
> slot overlap, or cropping.

The word `WELCOME` was intentionally excluded from generated raster artwork.
It is supplied as a separate vector shape and should be rendered as real DOM
text by the implementation.

## Wave-rise revision prompt

> Exactly three identity-preserving in-between poses, left-to-right, showing
> the existing waving arm on the viewer's right gradually rising from rest:
> just away from the hip, around waist height, then around shoulder height.
> The other arm remains in the trouser pocket. Match the canonical identity,
> outfit, scale, baseline, palette, and pixel clusters. Flat green chroma
> background; no opposite-arm gesture, expression change, sparkle, bubble,
> text, motion lines, overlap, or cropping.

These three frames were inserted after the neutral pose. Both source poses
that raised the opposite arm—including the previously missed sixth displayed
pose—were removed from the production sequence rather than retimed or mirrored.

## Frames 2–3 proportion correction

> Replace exactly the second and third displayed poses. Use the neutral frame
> as the strict identity and proportion reference and the later hand-rise poses
> as motion endpoints. Preserve the same head-to-body ratio, torso width,
> trouser width, leg length, shoes, 192-pixel hair-to-shoe height, center x=80,
> and baseline y=204. Change only the viewer-right waving arm: first just away
> from the hip, then around waist/lower-rib height. No enlargement, head-size
> change, leg-length change, opposite-arm gesture, expression change, or text.

The corrected two-pose source replaces only production frames 2 and 3. Final
deterministic normalization still enforces the shared body height and baseline.

## Frame 4 waist correction

> Replace only displayed frame 4, using displayed frame 3 as the strict body-
> proportion reference. Keep the viewer-left hand in the trouser pocket and
> raise only the viewer-right hand to the next shoulder-level wave position.
> Preserve torso length, belt height, trouser length, head size, center, palette,
> and pixel-art identity. No speech bubble, text, sparkle, opposite-hand raise,
> background, shadow, or crop.

The replacement is normalized with the same deterministic body-height and
baseline pass as every other production pose. Its detected belt center moved
from y=103 to y=114, matching displayed frame 3 and sitting one pixel above
displayed frame 2 (y=115).
