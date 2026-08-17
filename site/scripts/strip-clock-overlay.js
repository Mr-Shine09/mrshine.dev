/**
 * One-time (idempotent) sprite pre-process.
 *
 * The `waiting` row of the atlas carries a compact clock in the effect area
 * above the head. On the desktop app that clock is the point of the state; on
 * this site the same frames are re-used as a hero wave, where a ticking clock
 * reads as noise. This clears the effect area of that row only.
 *
 * Safe by construction: in every `waiting` frame the clock occupies y=4..23,
 * y=24 is empty, and the first body pixel (hair) is at y=25. Clearing y=0..24
 * therefore removes the clock and nothing else. The script re-verifies that
 * invariant before writing and refuses to run if the source ever changes.
 *
 *   node scripts/strip-clock-overlay.js
 *
 * Reads  public/assets/animation/authoring/legacy-atlas-source.png
 * Writes public/assets/animation/legacy/mascot-atlas.png
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { PNG } from "pngjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(HERE, "..");

const contract = JSON.parse(
  fs.readFileSync(
    path.join(ROOT, "public", "assets", "animation", "legacy", "mascot-contract.json"),
    "utf8"
  )
);

const SOURCE = path.join(
  ROOT,
  "public",
  "assets",
  "animation",
  "authoring",
  "legacy-atlas-source.png"
);
const OUTPUT = path.join(
  ROOT,
  "public",
  "assets",
  "animation",
  "legacy",
  "mascot-atlas.png"
);

const [CELL_W, CELL_H] = contract.atlas.cell_pixel_size;
const BODY_TOP = contract.bounds.normal_body_inclusive[1]; // y=25
const CLEAR_THROUGH = BODY_TOP - 1; // y=24, the empty separator row

const waitingRow = contract.rows.find((row) => row.state === "waiting");
if (!waitingRow) throw new Error("no `waiting` row in atlas-contract.json");

const png = PNG.sync.read(fs.readFileSync(SOURCE));
const at = (x, y) => (y * png.width + x) * 4;

let cleared = 0;

for (let frame = 0; frame < waitingRow.frames; frame++) {
  const originX = frame * CELL_W;
  const originY = waitingRow.index * CELL_H;

  // Guard: the separator row must be empty, so the clock above it is provably
  // disconnected from the body below it. (The hair top itself floats between
  // y=25 and y=26 as the head bobs, so only the separator is a fixed landmark.)
  let separatorOpaque = 0;
  for (let x = 0; x < CELL_W; x++) {
    if (png.data[at(originX + x, originY + CLEAR_THROUGH) + 3] > 0) separatorOpaque++;
  }
  if (separatorOpaque > 0) {
    throw new Error(
      `waiting frame ${frame}: separator row y=${CLEAR_THROUGH} is not empty ` +
        `(${separatorOpaque} opaque px) — the clock is no longer provably ` +
        `disconnected from the body. Re-derive the clear region.`
    );
  }

  // Guard: the body must still be there below the clear region.
  let bodyOpaque = 0;
  for (let y = BODY_TOP; y < CELL_H; y++) {
    for (let x = 0; x < CELL_W; x++) {
      if (png.data[at(originX + x, originY + y) + 3] > 0) bodyOpaque++;
    }
  }
  if (bodyOpaque === 0) {
    throw new Error(
      `waiting frame ${frame}: no body pixels below y=${BODY_TOP}. ` +
        `Source art changed — re-derive the clear region.`
    );
  }

  for (let y = 0; y <= CLEAR_THROUGH; y++) {
    for (let x = 0; x < CELL_W; x++) {
      const i = at(originX + x, originY + y);
      if (png.data[i + 3] !== 0) cleared++;
      // Contract: transparent pixels are RGB (0,0,0) with alpha 0.
      png.data[i] = 0;
      png.data[i + 1] = 0;
      png.data[i + 2] = 0;
      png.data[i + 3] = 0;
    }
  }
}

fs.writeFileSync(OUTPUT, PNG.sync.write(png));

console.log(
  cleared === 0
    ? `already clean — ${path.relative(ROOT, OUTPUT)} rewritten unchanged`
    : `cleared ${cleared} clock px from ${waitingRow.frames} waiting frames → ${path.relative(ROOT, OUTPUT)}`
);
