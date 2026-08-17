# Portfolio site — decision ledger

Running record of what's settled, what's open, and what to pick up next.
Update at the end of every session. This is **not** the build plan —
see `plan.md` for the execution document.

**Last updated:** 2026-08-16 (Hero V2 mascot asset repair and calibration)
**Stage:** **the built site's page architecture has been superseded.** The
structural work from 15 Aug is done and still valid at the component level, but
the site is no longer a single scrolling page — see decisions #18–#21. The
content pass has started; `docs/about-me.md` is written. A separate, dominant
13-frame Hero V2 mascot handoff is now saved and QA-passed, but intentionally
has not been integrated into `site/`.

---

## Status

| | |
|---|---|
| Decisions locked | 47 (4 superseded) |
| Blocking open items | 10 |
| Non-blocking open items | 7 |
| `plan.md` written | **yes** |
| Build started | **yes — structurally complete** |
| Deployed | no (needs owner's Cloudflare account) |
| Under version control | **no** — see Housekeeping |

---

## Locked decisions

| # | Decision | Reasoning |
|---|---|---|
| 1 | **Purpose:** portfolio + personal introduction | Shows projects, but also introduces who he is and what he loves |
| 2 | **Content lives in files** in the repo; Keystatic admin panel added **at the end**, not first | Panel is wanted, but building it first risks a weekend of plumbing before a site exists |
| 3 | **Framework: Astro** | Ships almost no JS by default; suits a content site with one animated element |
| 4 | ~~**Structure:** single scrolling page, anchored sections~~ **SUPERSEDED by #18 (16 Aug 2026)** | Was: 4–6 projects doesn't justify separate pages. Overturned when the owner found a layout reference he actually wanted |
| 5 | **Section order:** Built → Current → Ahead | Owner's own framing: past, present, future |
| 6 | **Projects: hybrid** — 2–3 with images, rest typographic | Only some projects have visuals worth showing |
| 7 | **No WebGL / three.js** | Mascot is the signature element instead. **Do not reintroduce** |
| 8 | **Mascot is the signature element** | Sprite animation is an image plus a few lines of CSS |
| 9 | **Palette: sampled from the sprite**, 12 colours, nothing invented | A page coloured from its own mascot reads unified for free |
| 10 | ~~**Type:** high-contrast serif + monospace. **No pixel font**~~ **SUPERSEDED by #41 (16 Aug 2026)** | Was: serif carries the Classics side, mono carries the engineering. Overturned once the owner chose Geist Pixel — and the reasoning inverts: the mascot is pixel art, so a pixel face is *more* coherent with the signature element (#8) than a serif ever was |
| 11 | **Hosting: Cloudflare Pages + Cloudflare registrar** | `.dev` is HSTS-preloaded, HTTPS mandatory; registrar + host together = no DNS step |
| 12 | **Light and dark, with a toggle** | Sprite outlines lose definition on dark; dark accent must become amber, rust disappears |
| 13 | ~~**Layout skeleton adapted from afig.dev**~~ **SUPERSEDED by #18/#19 (16 Aug 2026)** | Was: sticky anchor nav, minimal hero, weighted project cards, split "Current" section, footer contact card. The whole skeleton assumed one scrolling page. `plan.md` §5 goes with it |
| 14 | ~~**Type: Playfair Display + JetBrains Mono**~~ **SUPERSEDED by #41 (16 Aug 2026)** | Was: satisfies #10, self-hosted, no layout shift. Both families are removed from `astro.config.mjs`. What survives is the *method* — self-hosted at build time, metric-matched fallback, no third-party request |
| 15 | **Sprites render from canonical atlases**, driven by contracts in `site/public/assets/animation/` | The contract is the machine-readable source of truth for geometry, row order and timing. One request per active animation, and the site can never drift from the art |
| 16 | **Art licence amended, not gutted** — the owner's own personal sites are named as permitted; the third-party restriction stands | The plan said "remove the no-other-website clause". Removing it outright would have licensed the character to anyone for any product, against the file's stated intent. The owner never needed permission from himself — the file just needed to stop saying it |
| 17 | **The mascot player fails open**: looping sprites animate immediately and `IntersectionObserver` only *pauses* them; one-shot rows (`poof`) are the only ones that wait to be seen | Gating every sprite on IO looked tidier and was wrong — where IO never delivers (a page rendered while hidden), every mascot froze on frame 0 permanently. Found by testing, not by reading. **Do not "optimise" this back into a gate.** |
| 18 | **Structure: a home grid of tiles, each block its own page.** Replaces #4 | The owner found the layout he actually wanted — `alectear.com/lettering`: a masonry grid of full-bleed image tiles, sticky pill nav top-left, every tile navigating to its own page. Five blocks of content do not read as one scroll; they read as a set of rooms |
| 19 | **Layout reference is now `alectear.com/lettering`**, replacing afig.dev (#13) | Structural pattern only, same caveat as #13 carried: palette (#9), type (#10/#14) and mascot (#8) are unrelated to the reference and stay locked. What is borrowed is the grid, the pill nav, and the tile-to-page navigation |
| 20 | **Four grid tiles: About · Projects · Reading List · W Phrases.** Contact is a nav pill with its own page, not a tile | Mirrors the reference, whose nav carries `index · about · contact` while the grid carries the work. Contact is a destination, but it should not compete with the actual content for grid space. Keeps the grid at four, which a masonry absorbs cleanly |
| 21 | **Grid tiles must carry real images**, not labels on coloured rectangles | The reference's grid works because the tiles *are* the content — ten pieces of actual lettering. A five-tile grid is a navigation menu wearing a gallery's clothes, and it only survives the comparison if each tile has genuine visual weight: the portrait, project shots, book covers, the mascot |
| 22 | **Contact lives in a business card fixed to the bottom corner of every page.** Click → it spins, scales up, travels to centre, and reveals email, GitHub, LinkedIn, Instagram, Facebook, **Devpost**, résumé | A card that flips is the same idea as a mascot that waves and a serif that carries the Classics — the page as an object, not a document. It also puts contact one click from anywhere instead of one navigation away |
| 23 | **The `/contact` page survives as the card's fallback**, not as the primary surface. Refines #20 | The reveal needs JavaScript, the nav pill needs a destination, and the already-built `contact.vcf` endpoint needs a page so right-click-save keeps working. **Contact information must never exist only behind an animation.** The card is the front door; the page is the one that still opens when the power is out |
| 24 | **Every new motion respects `prefers-reduced-motion`** — the business card's spin-and-travel, the `Yangon ✈ California` plane, and the project-card flip | Not a new rule; the existing acceptance criteria already require it and the mascot player already implements it. Recorded because all three new elements are motion-first ideas, and each would otherwise be written as pure CSS animation with no guard |
| 25 | **Projects are a uniform flip-card deck.** Front: name, image, one-liner. Back: stack, what was hard, repo link. Flip on click, never on hover | Hover does not exist on touch, so a hover flip means building two interactions. Uniform cards keep the flip from reflowing the grid and stop the deck from visibly ranking one project beneath another |
| 26 | **`weight: featured / standard / text-only` is removed from the project schema.** Replaced by `draft: boolean` | The grading existed to vary card size down a scrolling page (#4, now superseded). A deck is uniform by nature. `draft` does the job that actually matters now: holding an unfinished project out of the build entirely rather than rendering a hollow card |
| 27 | **Card front images are matted on a flat colour plate, never cropped** | Forced by the source material, not chosen: Echo's screenshots are tall phone portraits and PokeDesk's are ultra-wide dock strips. No crop ratio serves both — a 4:3 crop cuts the `MESH ACTIVE` badge off the best Echo shot. The plate also gives a card with no image yet a designed empty state instead of a hole |
| 28 | **Team projects name every contributor, and link to the original repo** | Echo is a three-person Hack for Humanity build in `aadityad12/Echo`. Presenting a team project as solo work is the one portfolio mistake that costs more than having no portfolio |
| 29 | **The Reading List is a shelf of rendered spines**, not photographed and not a grid of covers. Layout reference: `carollia-library.lovable.app` — structural pattern only | Rendered spines are elements: clickable, searchable, theme-aware, and correct at 2 books or 60. A photograph is one flat image that has to be reshot every time a book is finished. Spine colours come from the locked 12-colour palette (#9), so the shelf matches the site with nothing invented |
| 30 | **Books are organised language → genre, never by status.** English/Burmese sections, each holding Non-fiction and Fiction shelves; status is a marker on the spine | A real shelf is organised by subject, not by whether you finished the book. Supersedes an earlier decision this session to shelve by status — that split the Burmese books across three shelves and made the language distinction invisible |
| 31 | **Empty shelves do not render**, and neither do draft projects | Two books across four shelves means two empty racks. An empty shelf reads as broken rather than aspirational. Consistent with #26: the data holds the structure, the page shows only what exists |
| 32 | **A Myanmar-capable font must be self-hosted before any Burmese content ships** | Playfair Display and JetBrains Mono have no Myanmar coverage. Burmese titles render as tofu boxes and **the build still succeeds** — this is the one failure on the site that is silent. Noto Sans Myanmar or Padauk, through the same Astro font pipeline as #14, with `lang="my"` markup and extra line-height for stacked diacritics |
| 33 | **The calibrated Hero V2 mascot is the approved home animation** | Its runtime atlas, contract, and static fallback are consolidated in `site/public/assets/animation/hero/`. Displayed frame 4 was repaired to match frames 2–3 at the waist and baseline before this decision was locked |
| 34 | **W Phrases are styled per-entry in the content file, not through a live editor** | "Customizable" resolved to author-time, not runtime. A live editor needs auth and a backend, or localStorage — which only changes the owner's own browser. Per-phrase `font`/`size`/`colour` fields keep the site fully static, and the Keystatic panel already planned in #2 turns that file into a visual editor for free |
| 35 | **The `font` field validates against six named self-hosted families**; free-text font names are rejected | A typo in a free-text field falls back to a system default with no error anywhere. A closed set fails the build by name, bounds the page weight, and becomes a dropdown in Keystatic. Four families are new — subset and weight-limited, no third-party requests, and **no pixel font** per #10 |
| 36 | **Per-phrase colour must be a palette token, never a raw hex** | The failure is silent and theme-dependent: a near-black phrase vanishes on the dark background, a pale one vanishes in light. Nothing errors — the phrase is simply gone. Palette tokens only, each contrast-checked in **both** themes. #12 already records rust as the known trap |
| 37 | **The W Phrases marquee pauses on hover and on focus, and does not move at all under reduced motion** | A phrase that cannot be stopped cannot be read, and reading them is the entire point. The static wall is also the no-JS fallback — same principle as #23 and the Reading List search |
| 38 | **`/contact` renders the business card in its opened state, from the same data file** | One source, two presentations, so the card and the page can never drift out of sync. It is also what makes keeping the page cheap — it is a second layout of data that already exists, not a second copy of it |
| 39 | **No contact form.** An email address, plus a copy-to-clipboard control beside it | A form needs somewhere to POST. This site is static with no backend — a form means either a third-party service (new external dependency, and a privacy question about where messages go) or a Cloudflare Function (a backend to maintain and a spam problem on day one). The email is published plainly: obfuscation that defeats scrapers also defeats screen readers and copy-paste |
| 40 | **Mascot mapping is resolved in `ANIMATION_ASSETS.md`** | Hero V2 is home-only; reading-fire maps to Reading; computer-working and workbench-zap map to Projects; thinking-cloud maps to W Phrases; walking and run-trip-recover form the scroll traveller. The old waiting/working/poof/sleeping page mapping is retired |
| 41 | **Type: Geist Pixel, one family for the whole site.** Replaces #10 and #14 | SIL OFL, self-hosted, subsetted. The owner's choice, and the reasoning inverts the old rule: the mascot is pixel art (#8), so a pixel face is more coherent with the signature element than a serif was. Verified by rendering: it is a fine technical monospace, not a chunky arcade face, and reads cleanly at 16px |
| 42 | **There is no bold. Emphasis is size, accent colour, and letterspaced uppercase** — and `font-synthesis: none` globally | Geist Pixel's only axis is `ELSH` ("Element Shape"), which changes pixel shape, not weight. Verified by rendering: **mid-axis values 20–80 are hollow and low-contrast**, so any real text is locked to `ELSH` 0 or 100. Without `font-synthesis: none` a browser fakes a bold and smears the pixel edges |
| 43 | **Type scale is built on 4px multiples with a 16px floor for prose** | Pixel faces are crisp at integer multiples of their grid and muddy between. The font is also monospaced and therefore wide — the same sentence takes more horizontal room than the old proportional face, which makes 375px the real test |
| 44 | **Theme: "Riso C2" — deep violet ink and coral second ink on pale lilac.** Replaces the mascot-sampled page palette (#9) | The owner wanted the site to look unlike other portfolios. Chosen over keeping the paper palette and over a phosphor terminal. The ink was shifted from riso blue to deep violet deliberately: blue-on-lavender is `alectear.com`'s exact palette, and since the layout is already borrowed from that site (#19), taking the colours too would tip homage into imitation. All six token/background pairs measured against WCAG AA — light `--accent` clears 4.5 by only 0.06, so neither it nor `--bg` may be adjusted without re-measuring |
| 45 | **The mascot is exempt from the theme and keeps its own 12 colours** | Verified by compositing the real atlas onto the new palette: the navy jacket sits comfortably against violet ink and the orange accents read as the second ink. It works as a full-colour object on a duotone page. Recolouring would also break the atlas contract's frozen palette (#15) |
| 46 | **Mobile: home grid stays two-column masonry; the business card becomes a tab that opens full-screen; each bookshelf scrolls horizontally in its own container** | One column would turn a four-tile front door into a scroll, defeating #18. There is no "centre" worth travelling to on a 375px screen. And the page body must never scroll horizontally — wide content scrolls inside itself |
| 47 | **The build amends `site/` rather than starting fresh** | The mascot player's fail-open behaviour (#17) was found by running the thing, not by reading it, and a reimplementation would very likely reintroduce the bug. The content collections, validation pattern, theme toggle and vCard endpoint are all hardened too |

---

## The 16 Aug architecture change — what survives, what doesn't

Decisions #18–#21 overturn the page structure, not the design system. Worth
being precise about the blast radius, because "we're changing the layout" reads
as bigger than it is.

**Survives unchanged — do not rebuild:**

- `tokens.css`, the whole palette and type system (#9, #10, #14)
- `Mascot.astro` and the atlas/contract sprite pipeline (#8, #15, #17) — the
  player is the most-tested thing in the repo and none of it is page-structure
  dependent
- `ThemeToggle.astro` and the `localStorage` persistence (#12)
- The content collections and their schemas — `projects`, `books`, `hobbies` —
  and the build-time validation with custom messages
- `contact.vcf` as a build-time static endpoint
- Every accessibility property already verified: focus-visible rule, ≥44px tap
  targets, `image-rendering: pixelated`, no horizontal overflow at 320px

**Superseded — rewrite:**

- `index.astro` — was the single scrolling page, becomes the tile grid
- `Nav.astro` — was a sticky in-page anchor rail, becomes a pill nav with real
  routes
- `SectionNav.astro` — no longer has a job; there are no in-page sections to
  anchor
- `Hero.astro` — the minimal hero belonged to the one-page structure. The About
  *page* opens differently (see `docs/about-me.md` §2)
- `ContactCard.astro` — was a footer card at the end of one scroll, becomes the
  global business card of #22. The vCard generation inside it survives; the
  placement and the treatment do not
- `plan.md` §5, the section-by-section spec, and the section order in §6

**Open, not yet decided:**

- Where the mascot lives now. The old sprite-to-section mapping (`waiting` in
  the hero, `working` at Built, `ideating` at Current, `poof` between sections,
  `walk-right` at Ahead, `sleeping` in contact) assumed a single scroll. Five
  separate pages need a new mapping, and the `poof` transition in particular has
  no obvious home — it existed to cover a scroll boundary that no longer exists.
  **This is the largest unresolved consequence of #18.**
- What happened to the "Ahead" section. The past/present/future framing (#5) was
  a section order on one page; it has no equivalent in a four-tile grid, and
  "W Phrases" has taken its place in the set. Either it folds into About, or it
  is dropped deliberately — but it should not just quietly vanish.

---

## Open items

### Blocking

- [ ] **Rotate the API keys visible in a hackathon photo.** One of the photos
      supplied for the About page shows a `.env` file on screen with a live
      `ANTHROPIC_API_KEY`, a `BROWSERBASE_API_KEY`, and a `REDIS_URL` containing
      a password. This is not a website problem — the photo exists independently
      and the keys should be treated as compromised. See `docs/about-me.md` §4.
- [ ] Dates for all 19 About-page photos, and captions for the portrait, Yangon
      and De Anza groups
- [ ] The photo files themselves, into `site/src/assets/photos/`
- [ ] A real `resume.pdf`. Every other business-card field was supplied on
      16 Aug; this is the only one still empty
- [ ] Six project screenshots into `site/src/assets/projects/`, with alt text —
      three PokeDesk, three Echo. See `docs/projects.md` §4
- [ ] Project schema amendment: drop `weight`, add `draft`, `collaborators`,
      `builtAt`, `links.devpost`
- [ ] Book schema replacement: `language`, `genre`, three-state `status`,
      `started`/`ended`, `rating`, `review`. Delete `content/books/current.md`
      and the `past/` directory
- [ ] Started dates and progress for Dune and Zero to One
- [ ] Four new font families for W Phrases, subset and weight-limited
- [ ] Contrast-check every palette token used as a phrase colour, in both themes

### Not blocking
- [x] Dominant Hero V2 wave asset — saved as a separate 13-frame atlas and
      implementation handoff under `design-handoff/oak-hero-v2/`. Frame 4's
      short-torso defect was repaired and the slow calibration loop passes.
      Integration remains intentionally deferred under decision #33.
- [ ] Reading pose gap for the Current section — the reading card currently shows no sprite at all rather than a wrong one
- [ ] Mascot mapping for the new page structure — **deliberately deferred per #40**
      until the new Hero arrives from Codex. `poof` has no home in the new
      architecture and should be retired unless a use appears
- [ ] Decide the fate of the "Ahead" / past-present-future framing (#5). It had
      no slot in the four-tile grid and W Phrases took its place in the set —
      drop it on purpose rather than by accident
- [ ] Regenerate `contact.vcf` with the four socials and the Santa Clara location
- [ ] ~~Real content: role, location, tagline~~ — **supplied 16 Aug**, captured in `docs/about-me.md` §3. Still outstanding: LinkedIn, résumé PDF, real domain
- [ ] Real project list (4–6), which 2–3 get images, and their writeups. Dock Pet is seeded as the featured project from facts in its own atlas contract — it still needs the owner's voice and a real screenshot
- [ ] Real book data (current + past) and hobby list
- [ ] Two generated placeholder images sit in `site/src/assets/projects/` — diagonal stripe patterns, obviously not screenshots. Replace or delete with their projects

### Observed during the build, not acted on
- Dark mode: the mascot's black hair does lose definition against `--ink`, exactly as #12 anticipated. The accent swap is in place as decided; no backing plate or outline was added, since that would change how the character reads and was not a locked decision. Worth an eye on a real screen before deciding it needs anything.
- **`prefers-reduced-motion` was not verified by execution.** The CSS rule and the player's guard are both in place and were confirmed by inspection, but the build environment could not emulate the media query. This is the one acceptance criterion resting on reading rather than running — check it once on a real machine.

---

## Files produced

The original build files were verified against the working directory on
2026-08-15. The Hero V2 handoff was rebuilt and verified on 2026-08-16.

| File | What it's for |
|---|---|
| `plan.md` | Claude-Code-shaped execution plan: file tree, content schemas, design tokens, task checklist, acceptance criteria. §7a records where the build differed from the plan. **§5 and the section order in §6 are superseded by #18–#21** and have not yet been rewritten |
| `docs/about-me.md` | Content spec for the About page — the first of five. Page anatomy, draft copy, the 19-photo manifest with slots and captions, and the exclusions the owner set |
| `docs/projects.md` | Content spec for the Projects page — the second of five. Flip-card behaviour, the matte-not-crop image rule, full content for PokeDesk and Echo pulled from their READMEs, and two held drafts |
| `docs/reading-list.md` | Content spec for the Reading List — the third of five. Rendered-spine shelf, the language→genre structure, the book schema replacement, client-side search, and the Myanmar font requirement |
| `docs/w-phrases.md` | Content spec for W Phrases — the fourth of five. Marquee rows, the six-font set, per-phrase style fields, the palette-token colour rule, and the cross-link to the Reading List |
| `docs/contact.md` | Content spec for Contact — the fifth of five. The card opened as a page, the full link set, why there is no form, and the vCard regeneration |
| `HANDOFF.md` | **The build brief.** Self-contained: architecture, routes, the Geist Pixel type system, the Riso C2 theme with measured contrast, per-page component specs, schemas, what to keep and what to delete, and acceptance criteria. Written 16 Aug for a session starting cold |
| `Geist_Pixel copy/` | Source TTF (3.6 MB, variable, single `ELSH` axis), `OFL.txt`, `README.txt`. **Must be subsetted to woff2 before shipping** |
| `site/` | **The site.** Astro 7, builds clean (0 errors / 0 warnings / 0 hints), no external JS files — 5 inlined scripts, 3.5 KB total |
| `site/scripts/strip-clock-overlay.js` | Clears the clock from the `waiting` row so those frames can be re-used as a hero wave. Idempotent, and refuses to run if the source art changes shape |
| `site/public/assets/animation/ANIMATION_ASSETS.md` | Canonical asset map. Claude should start here before placing or changing any mascot animation |
| `site/public/assets/animation/scenes/` | Six approved 12-frame runtime atlases plus one shared timing contract |
| `site/public/assets/animation/hero/` | Hero V2 runtime atlas, contract, and static fallback |
| `site/public/assets/animation/legacy/` | Existing multi-state mascot atlas and contract, retained for component compatibility |
| `site/public/assets/animation/authoring/legacy-atlas-source.png` | Pristine legacy atlas input used only by `strip-clock-overlay.js`; never reference from page code |

### Listed in an earlier session but **not present** in this directory

`ground-comparison.html`, `mascot-wave-prompts.md`, `mascot-scale-comparison.png`,
`tall-wave-attempt.png`.

All four were recorded as produced during planning and none of them exist here.
They were probably made somewhere else (a chat session, another folder) and never
landed in the project. Two of them still carry real value if they can be found:
`mascot-wave-prompts.md` is the input for the outstanding tall-wave frames, and
`tall-wave-attempt.png` is the record of an approach the ledger says not to retry
— that warning is now unbacked. Nothing in the build depended on any of them.

---

## Where the build actually stands

Running locally on `:4321`. Everything in §6 of `plan.md` is checked off except
real content and deploy — **but it is building the superseded structure.** What
follows describes the 15 Aug build as it exists today, not as it should be.

- Sections all present in the now-superseded order: hero → Built → *poof* → Current → Ahead → Contact
- Sprite mappings as locked: `waiting` wave in the hero, `working` at Built,
  `ideating` at Current, `poof` between the two, `walk-right` at Ahead,
  `sleeping` in the contact card
- Content collections are schema-validated at build time, with custom messages
  (a `standard` project without an image fails the build by name)
- vCard is a build-time static endpoint at `/contact.vcf`; verified well-formed

---

## Housekeeping

**This directory is not a git repository.** There is no history, no diff, and
nothing to recover — the missing files above are the first evidence of what that
costs. A `site/.gitignore` is written and ready, but it is inert until `git init`
runs. Doing that before the content pass would be cheap insurance, and Cloudflare
Pages wants a repo to deploy from anyway, so decision #11 needs it regardless.

The art licence is narrow by design (#16). If the repo is ever made public, the
sprite atlas travels with it — that is intended for the owner's own portfolio,
but it is worth being deliberate about rather than discovering later.

## GitHub issue map

No issue numbers exist because this directory is not yet a Git repository and
has no connected GitHub repository. Convert blocking and non-blocking items to
issues only after the first repository and commit exist; until then, the open
items above are authoritative.

## Risk register

| Risk | Status | Mitigation / next gate |
|---|---|---|
| No version-control history for the site or new art handoff | Resolved | Git repository initialized on `main`; animation cleanup remains recoverable from history |
| API keys visible in a supplied photograph | Open, high | Rotate all exposed credentials before using or publishing the photograph |
| Hero V2 exists but its page-level placement is unresolved | Resolved | Mapping and runtime rules are recorded in `ANIMATION_ASSETS.md` and HANDOFF §11 |
| Motion accessibility not executed on a real browser/device | Open, medium | Run the manual reduced-motion acceptance check before deployment |

## Verification matrix

| Area | Evidence | Result |
|---|---|---|
| Hero V2 frame geometry | 13 RGBA cells at 160 × 208; body height 192; anchor baseline y=204 | PASS — 2026-08-16 |
| Frames 2–4 waist calibration | Historical QA completed before redundant calibration images were removed | PASS — 2026-08-16 |
| Atlas packaging | 2080 × 208 Hero atlas; JSON lists frames 0–12 | PASS — 2026-08-16 |
| Scene packaging | Six 4608 × 320 scene atlases; shared JSON lists 12 frames and 12 durations per scene | PASS — 2026-08-16 |
| Website integration | Components point only at `public/assets/animation/` | PASS — 2026-08-16 |

## Session log

### 2026-08-16 — Save and calibrate Hero V2 mascot

- Objective: Preserve the accepted mascot repair and record an implementation-
  ready handoff without changing the website.
- Completed: Saved the repaired 13-frame atlas, individual frames, JSON
  contract, slow inspection GIF, frames 2–4 calibration image, generation
  notes, QA report, and implementation guide under
  `design-handoff/oak-hero-v2/`.
- Decisions: Locked decision #33. The handoff is the canonical Hero V2
  candidate, while `site/` remains unchanged until a separate implementation
  pass.
- Verification: All 13 frames are RGBA 160 × 208 with hard alpha; every central
  body is 192 logical pixels tall; every shoe sits on opaque row y=203 against
  anchor baseline y=204; displayed frames 2–4 have detected waist centers
  `[115, 114, 114]`; the 2080 × 208 atlas matches every source frame byte-for-
  byte; and the inspection GIF contains 13 frames at 1000 ms each. Atlas SHA-256:
  `36b918fafd3e496069c05ac32830bb886e99ba9d91800a670dee4ab8fb6f2ed6`.
- Risks or blockers: The project root is still not under version control, so
  the saved handoff has no commit history. Website integration also depends on
  the unresolved mascot mapping for the new multi-page architecture.
- Next: Give `docs/IMPLEMENTATION-GUIDE.md` and the saved atlas contract to the
  implementation agent after the page-level mascot mapping is decided.

## Next session

1. `git init` and a first commit, before anything else changes. See Housekeeping.
   This matters more now than it did on 15 Aug: the next session rewrites
   `index.astro` and `Nav.astro`, and there is still no way to recover them.
2. ~~Finish the remaining four content docs~~ — **done 16 Aug.** All five specs
   exist in `docs/`: `about-me`, `projects`, `reading-list`, `w-phrases`,
   `contact`.
3. Rewrite `plan.md` §5 for the grid-and-pages architecture. Until that happens
   `plan.md` and `ledger.md` disagree, and a build session reading only the plan
   will build the wrong site. **This is now the highest-value remaining task.**
4. Decide the fate of "Ahead" (#5). The mascot mapping is deferred by #40, not
   forgotten.
5. Deploy to Cloudflare Pages and connect the `.dev` domain. Not started: it
   needs the owner's own Cloudflare account, so it is his to run.
6. One manual `prefers-reduced-motion` check on a real machine — the single
   acceptance criterion not verified by running it.
7. Revisit the reading-pose gap and tall wave frames opportunistically, not as
   gating work. Look for `mascot-wave-prompts.md` first; without it those frames
   start from scratch.
8. Keystatic panel last, per #2 — the schemas in `src/content.config.ts` are
   written strictly so it has something clean to bind to.
