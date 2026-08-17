# Oak scene animations

Six 12-keyframe pixel-art loops for the portfolio:

- `reading-fire`: Oak reads on a large couch beside a small cast-iron stove. The loop uses breathing, blinking, fire flicker, and one page turn.
- `run-trip-recover`: Oak runs toward the viewer's left in a three-quarter view, catches a toe, stutter-steps without falling, regains balance, and returns to the run cadence. The live site maps both travel and frame progression to smoothed document scroll.
- `workbench-zap`: Oak works seated at a circuit bench with his tongue out in concentration, flashes into a full-body blue skeleton zap, then stays visibly singed and dishevelled through the recovery. The live site places it beside the Projects introduction.
- `computer-working`: Oak sits at a compact desk, types in a relaxed alternating rhythm, pauses to read, uses the trackpad, and returns to typing without moving the desk or computer.
- `thinking-cloud`: Oak sits in a chin-in-hand thinking pose as a connected blank thought cloud grows, gently changes shape, and recedes. The cloud deliberately contains no symbols so the asset stays reusable.
- `walking`: Oak walks toward the viewer's right in a three-quarter view through two continuous gait cycles, with a stable ground line and subtle body bob.

The source boards are authored as invisible 4 x 3 grids on a flat `#00ff00` chroma background. Production frames are extracted to transparent PNGs and normalized to a shared canvas. The web previews use the frame manifests in this folder so timing stays separate from art.

Open `/animations/oak-scenes/index.html` on the local site to review all six loops together. `src/components/AnimatedScene.astro` plays scene atlases without transparent-frame ghosting and freezes on frame 00 when the visitor prefers reduced motion. `src/components/ScrollTripMascot.astro` owns the page-wide scroll choreography.

Character lock: black tousled hair, black rectangular glasses, navy quarter-zip with white side panels, gray wide-leg trousers, black belt, and blue/white sneakers. Keep the existing hard-edged pixel clusters and warm amber accent.
