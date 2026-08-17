import contract from "../../public/assets/animation/legacy/mascot-contract.json";

/**
 * Typed view over the atlas contract.
 *
 * The contract JSON is the machine-readable source of truth shipped with the
 * art (grid geometry, row order, per-frame durations). Nothing here restates
 * those numbers — it only reshapes them for the renderer, so the site can
 * never drift from the art.
 */

const [ATLAS_W, ATLAS_H] = contract.atlas.pixel_size;
const [CELL_W, CELL_H] = contract.atlas.cell_pixel_size;

export const atlas = {
  src: "/assets/animation/legacy/mascot-atlas.png",
  width: ATLAS_W,
  height: ATLAS_H,
  columns: contract.atlas.columns,
  rowCount: contract.atlas.rows,
  cellWidth: CELL_W,
  cellHeight: CELL_H,
} as const;

export type MascotState = (typeof contract.rows)[number]["state"];

/** `hold` means "show until the state changes" — it is not a duration. */
const HOLD = Number.POSITIVE_INFINITY;

export type MascotRow = {
  state: MascotState;
  index: number;
  frames: number;
  playback: "loop" | "once-hold" | "intro-hold";
  /** Per-frame milliseconds; `Infinity` for a held final frame. */
  durations: number[];
};

const rows = new Map<string, MascotRow>(
  contract.rows.map((row) => [
    row.state,
    {
      state: row.state as MascotState,
      index: row.index,
      frames: row.frames,
      playback: row.playback as MascotRow["playback"],
      durations: row.durations_ms.map((d) => (d === "hold" ? HOLD : Number(d))),
    },
  ])
);

export function mascotRow(state: MascotState): MascotRow {
  const row = rows.get(state);
  if (!row) {
    throw new Error(
      `unknown mascot state "${state}" — expected one of ${[...rows.keys()].join(", ")}`
    );
  }
  return row;
}

/**
 * A playable timeline: an explicit frame order plus the duration of each step.
 *
 * `sequence` lets a caller re-time a row without touching the art. The hero
 * uses it to ping-pong the `waiting` row (0→1→2→3→2→1) into a wave, which the
 * desktop app never plays — there the row is a one-shot hand-raise that holds.
 */
export type MascotTimeline = {
  row: number;
  frames: number[];
  durations: number[];
  loop: boolean;
};

export function buildTimeline(
  state: MascotState,
  options: { sequence?: number[]; frameDuration?: number } = {}
): MascotTimeline {
  const row = mascotRow(state);
  const { sequence, frameDuration } = options;

  if (sequence) {
    const outOfRange = sequence.find((f) => f < 0 || f >= row.frames);
    if (outOfRange !== undefined) {
      throw new Error(
        `mascot state "${state}" has ${row.frames} frames — frame ${outOfRange} does not exist`
      );
    }
  }

  const frames = sequence ?? Array.from({ length: row.frames }, (_, i) => i);

  const durations = frames.map((frame, i) => {
    if (frameDuration) return frameDuration;
    const declared = row.durations[frame] ?? row.durations.at(-1) ?? 200;
    // A held frame only truly holds if it is the end of the timeline. Inside a
    // custom sequence it is just another step, so fall back to a real value.
    if (declared === HOLD) {
      return i === frames.length - 1 ? HOLD : 200;
    }
    return declared;
  });

  return {
    row: row.index,
    frames,
    durations,
    // Custom sequences are authored to loop; declared playback decides otherwise.
    loop: sequence ? true : row.playback === "loop",
  };
}
