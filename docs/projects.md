# Projects — content spec

**Written:** 16 Aug 2026
**For:** the build session that implements the site
**Status:** two projects complete, two intentionally held as drafts

Architecture context is in `docs/about-me.md` §0 and `ledger.md` #18–#24. This
page is one of the four home-grid tiles.

---

## 1. What this page is

A **deck of flash cards**. Uniform cards in a grid; each one flips on click to
reveal its details and its repository link.

Four projects are planned. **Two ship now** — PokeDesk and Echo. **Two are held
as drafts** — Lookout and Wizlet — and do not render until their content exists.

The register carries over from About: plain, specific, dry. On the back of a
card, **lead with what was hard**, not with what was used. The stack chips
already list the technology; a sentence that repeats them is a wasted sentence.

---

## 2. Card behaviour

**Flip on click.** Not on hover — hover does not exist on touch devices, and
building both interactions doubles the work for no gain.

| Face | Contents |
|---|---|
| **Front** | Project name · hero image on a colour plate · one-line summary |
| **Back** | Stack chips · what was hard (2–3 sentences) · year · collaborators · GitHub link · Devpost link where one exists |

**All cards are uniform.** The old `weight: featured | standard | text-only`
grading is **removed from the schema** — it existed to vary card size on a
scrolling page, and a deck is uniform by nature. Uniform also means the flip
never reflows the grid and no project is visibly ranked beneath another.

### Requirements

Same bar as the business card in `docs/about-me.md` §5 — these are existing
acceptance criteria, not new ones:

- **Keyboard:** each card is focusable, flips on Enter/Space, has a visible
  focus state. The GitHub link on the back is a real `<a>` and reachable by tab
  **only when the card is face-up** — a hidden link that still takes focus is a
  keyboard trap.
- **`prefers-reduced-motion`:** the flip is motion. Under reduced motion, swap
  faces with no rotation.
- **Tap target ≥44px**, and the whole card is the target, not a small corner.
- **No-JS:** a card that cannot flip must still show the repository link. Front
  face carries the link as a fallback, or the back is rendered below the front
  and hidden by CSS the script removes.

---

## 3. Card front images

**Treatment: matte, do not crop.** Every card front is the same size and filled
with a **flat colour plate** from the palette; the screenshot sits inside it at
its own aspect ratio, whole. `object-fit: contain`, not `cover`.

This is not a stylistic preference — it is forced by the source material. Echo's
screenshots are tall phone portraits (~9:19.5); PokeDesk's are ultra-wide dock
strips (one is roughly 1800×250). No single crop ratio serves both. Cropping to
4:3 would cut the `MESH ACTIVE` badge off the best Echo screenshot.

The plate also gives the two draft projects a graceful empty state later: a
plate with no image is still a designed card, where a missing image is a hole.

---

## 4. The projects

### 4.1 PokeDesk — ships now

| Field | Value |
|---|---|
| **Name** | PokeDesk |
| **Year** | 2026 |
| **Repo** | `https://github.com/Mr-Shine09/PokeDesk` |
| **Devpost** | — |
| **Collaborators** | Solo |
| **Draft** | no |

**Summary (front of card), from the README verbatim:**

> A tiny pixel-art mascot that lives at the bottom of your Mac's screen and
> shows, at a glance, what your coding agent is doing.

**Stack chips:** Swift · SwiftUI · AppKit · Python 3 · XcodeGen

**Back of card — what was hard.** Two candidate angles; the second is stronger:

*Option A — the one already written.* The seeded `01-dock-pet.md` in the repo
carries a real writeup, drawn from the project's own atlas contract:

> The hard part was never drawing the character. It was making sixteen separate
> animation states feel like one creature. Every frame is authored against a
> fixed contract: a 96×112 cell, a shared ground baseline at `y=102`, binary
> alpha, and a frozen twelve-colour palette that props and effects are not
> allowed to extend. That contract is enforced, not just documented — the frame
> checks reject any sprite that crosses the four-pixel cell guard or drifts off
> the baseline, which is what keeps the mascot from subtly changing size as it
> walks.

*Option B — the honest fragility.* **Recommended.** The README names a real
weakness: chat detection depends on **a single English UI string** in the Claude
desktop app. Rename that string upstream and detection silently breaks. It is
opt-in and requires Accessibility permission for exactly that reason.

A card that says *"this feature rests on one string I don't control, so I made
it opt-in"* is more convincing than any success story on the page. It shows
judgement, not just execution. **Recommendation: lead with A, close with one
sentence of B.**

**Other facts worth a line, not a paragraph:** no telemetry, no network access,
reads nothing from prompts or code; ~2.2% idle CPU with animation halted when
obscured; separate Claude (orange) and Codex (navy) mascots tracking state
independently; respects macOS Reduce Motion.

> **Naming inconsistency to resolve.** The repo is **PokeDesk**, the app
> installs as **`Dock Pet.app`**, and the existing content file is
> `01-dock-pet.md`. Three names for one project. Pick one for the site — the
> spec assumes **PokeDesk**, per the owner's own list — and rename the content
> file to `01-pokedesk.md` so the slug matches.

**Images:**

| Slot | Screenshot | Use |
|---|---|---|
| `pokedesk-hero` | Two mascots on a purple desktop — one working at a desk, one walking | **Card front.** Most characterful, shows both mascots and the concept in one frame |
| `pokedesk-02` | Single mascot walking above a full dock | Card back |
| `pokedesk-03` | Agent session — "Redesign mascot and cursor assets," mascot idling in the corner | Card back. This is a *process* shot, not a product shot — it shows the thing being made, which is interesting but secondary. Do not use it as the front |

### 4.2 Echo — ships now

| Field | Value |
|---|---|
| **Name** | Echo |
| **Year** | 2026 |
| **Repo** | `https://github.com/aadityad12/Echo` |
| **Devpost** | TODO(owner) — the H4H submission URL, if there is one |
| **Collaborators** | **aadityad12 · shahxsheel · Mr-Shine09** |
| **Built at** | Hack for Humanity 2026 (V3) — SCU |
| **Draft** | no |

**Summary (front of card), from the README verbatim:**

> A Flutter prototype for receiving, storing, and relaying emergency alerts
> between nearby devices over Bluetooth Low Energy when an internet connection
> is unavailable.

**Stack chips:** Flutter · Dart · Kotlin · Swift · SQLite · Python 3

**Back of card — what was hard.** The README states it plainly, and it is a real
distributed-systems problem rather than a tooling complaint:

> Alert identifiers don't appear consistently in BLE advertisements across
> platforms. Without a stable ID visible at advertisement time, a device can't
> tell whether an alert it's hearing is one it has already relayed — which
> breaks background deduplication and makes iOS-to-Android relay coordination
> unreliable.

Supporting facts, one line each: devices act as both BLE client and server, so
alerts propagate mesh-like; a custom indexed-chunk protocol with gzip moves
alerts that don't fit in a single BLE payload; on-device translation into 22
languages with native text-to-speech, so an alert reaches someone who doesn't
read English.

> **Attribution is not optional here.** This is a three-person hackathon project
> in **someone else's repository**. The card must name all three contributors,
> and the link goes to `aadityad12/Echo` — not a fork. Presenting a team build
> as solo work is the one mistake on a portfolio that costs more than having no
> portfolio.

> **No licence file.** Echo currently grants nobody rights to copy, modify or
> redistribute it. That's the team's call and it does not block listing the
> project — but if the repo is ever meant to be reusable, it needs a licence,
> and that conversation belongs to all three of them.

**Images:**

| Slot | Screenshot | Use |
|---|---|---|
| `echo-hero` | Alert list, `MESH ACTIVE` badge lit, severity chips down the feed | **Card front.** Communicates the entire product in one glance: it's an alert app, and the mesh is live |
| `echo-02` | Alert detail — Read Aloud, Echo Path, "Received directly from a Relay node (0 echoes)" | Card back. The Echo Path row is the mesh made visible |
| `echo-03` | Same alert translated to Hindi, mid-readout | Card back. Proof of the 22-language claim, not just an assertion of it |

### 4.3 Lookout — draft, does not render

| Field | Value |
|---|---|
| **Name** | Lookout |
| **Draft** | **yes** — excluded from the built page |

All other fields `TODO(owner)`. The owner is refining this project and will
supply content later.

### 4.4 Wizlet — draft, does not render

| Field | Value |
|---|---|
| **Name** | Wizlet |
| **Draft** | **yes** — excluded from the built page |

All other fields `TODO(owner)`. Same as above.

> **Draft handling.** Both files exist in `src/content/projects/` with
> `draft: true` and are **filtered out at build time**. Nobody ever sees an
> empty or "coming soon" card. Flipping the flag to `false` is the only action
> needed to publish them — no schema change, no template change.
>
> Consequence to accept: **the deck renders as two cards until then.** Two is a
> thin grid. That is the honest state of the work and is better than two hollow
> cards padding it out.

---

## 5. Schema changes

The existing `Project` type in `src/content.config.ts` needs amending:

**Remove:**
- `weight` — and with it the three card variants and their components

**Add:**
- `draft: boolean` — default `false`; `true` filters the entry out of the build
- `collaborators: string[]` — empty means solo; non-empty renders on the card back
- `builtAt?: string` — the hackathon or context, e.g. `"Hack for Humanity 2026"`
- `links.devpost?: string`

**Keep as-is:** `title`, `slug`, `order`, `year`, `stack`, `summary`, `image`,
`imageAlt`, `metric`, `links.github`, and the markdown body.

`imageAlt` stays **required** wherever an image exists. That is an accessibility
requirement already in force, and matte-not-crop does not change it.

Placeholder files to delete once the real content lands:
`02-placeholder-standard.md`, `03-placeholder-text.md`, `04-placeholder-text.md`,
and the two generated stripe images in `src/assets/projects/`.

---

## 6. Home grid tile

The Projects tile uses **`pokedesk-hero`** — the two mascots on the purple
desktop. It is the most visually distinctive image in the whole project set, it
is unmistakably yours, and it ties the grid to the mascot that already runs
across the site.

Per ledger #21, the tile must carry that image, not a label on a coloured
rectangle.

---

## 7. Open items

Blocking:

- [ ] Screenshot files into `src/assets/projects/` — six of them, named per the
      slots above
- [ ] `imageAlt` for all six

Not blocking:

- [ ] Echo's Devpost URL, if the team submitted one
- [ ] Decide the PokeDesk / Dock Pet naming, and rename the content file to match
- [ ] Lookout and Wizlet content, whenever the owner is ready
- [ ] Echo licence — a conversation for the three contributors, not a site task
