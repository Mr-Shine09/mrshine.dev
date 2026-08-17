# Portfolio site — decision ledger

Running record of what's settled, what's open, and what to pick up next.
Update at the end of every session. This is **not** the build plan —
see `plan.md` for the execution document.

**Last updated:** 2026-08-16 (multi-page build executed; content complete)
**Stage:** **the site described in `HANDOFF.md` is built and content-complete.**
All seven routes exist, every acceptance criterion was verified by running the
site (Playwright, four widths, both themes, reduced motion, no-JS), and every
`TODO(owner)` except the real `.dev` domain and Echo's Devpost URL is resolved.
The owner supplied 12 photos, 6 project screenshots, `resume.pdf`, the Drake
phrase, and both books' dates/progress on the evening of 16 Aug. Remaining work
is deploy, not build.

---

## Status

| | |
|---|---|
| Decisions locked | 51 (4 superseded) |
| Blocking open items | 0 |
| Non-blocking open items | 6 |
| `plan.md` written | **yes — superseded by `HANDOFF.md`; historical** |
| Build started | **yes — built and content-complete** |
| Deployed | no (needs owner's Cloudflare account and the `.dev` domain) |
| Under version control | **yes** — `main`, clean tree at end of 16 Aug session |

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
| 48 | **Phrase colours are the three Riso theme tokens — `ink` / `accent` / `muted` — not the mascot's twelve.** Refines #36 | The docs pointed at the mascot palette, but that predates the Riso C2 theme (#44). The theme tokens are already contrast-measured AA in both modes, so a phrase can never silently vanish in either — which was the entire point of #36. The mascot twelve stay on the book spines, where each pairing was checked individually |
| 49 | **The W Phrases specimen set: Geist Pixel + Space Grotesk (grotesque), Archivo Narrow (condensed), Caveat (hand), Bitter (slab), Playfair Display (serif).** Refines #35 | Playfair returns as a phrase-only face — one weight, Latin subset — not as a site font; #41 stands. All five self-host through the Astro pipeline at build time and their `@font-face` rules are emitted only on pages that render phrases (the wall itself and the home tile) |
| 50 | **The scroll traveller walks on short pages, runs-trips-recovers on long ones (≥2.5 viewports), flips with travel direction, and does not exist on phones or under reduced motion** | The walking gait is scrubbed from distance travelled so the feet stay planted. On a phone a fixed overlay covers content and controls, and §11.2's own rule — never let the mascot cover a control — outranks having the traveller at all there |
| 51 | **The owner's 16 Aug content decisions:** the photo set is 12, not 19 — the `.env`-laptop shot, the Anthropic slide, the Campanile, the schoolyard, the fountain and the autumn hills are dropped by choice; Yangon/De Anza/DA Hacks photos carry no dates; the closing line keeps "Leveraging" | Dates render only where supplied rather than showing "date to come" placeholders — an owner decision overriding the spec's every-photo-dated rule. The dropped `.env` photo also closes the key-exposure risk on the website side; the owner reports the keys themselves were rotated long ago |

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

**Both former open questions are now closed:**

- Where the mascot lives — resolved by #40 and executed 16 Aug: Hero V2 on home,
  reading-fire on Reading, computer-working + one-shot workbench-zap on
  Projects, thinking-cloud on W Phrases, walking/run-trip as the scroll
  traveller (#50). `poof` found no home and is retired with the legacy atlas
  kept for compatibility (#17, #47).
- The "Ahead" / past-present-future framing (#5) is **dropped deliberately**.
  W Phrases took its slot in the four-tile set, and the built site records the
  decision rather than leaving it to vanish quietly.

---

## Open items

### Blocking

None. Everything blocking on 16 Aug morning was closed by the evening build:

- [x] API keys in the hackathon photo — photo dropped from the set (#51); owner
      reports the keys were rotated long ago
- [x] Photos — 12 supplied, renamed to manifest slugs, wired into About and the
      home tile; dates render only where supplied (#51)
- [x] `resume.pdf` — at `site/public/resume.pdf`, Résumé row live
- [x] Project screenshots — 6 supplied; `pokedesk-hero` and `echo-hero` on the
      card fronts and the home Projects tile
- [x] Project schema amendment, book schema replacement — in
      `src/content.config.ts` with named build failures
- [x] Dune (started 1 Aug 2026, 73% — p.302/412) and Zero to One (started
      1 Aug 2026, 43% — ch.6/14)
- [x] The five specimen families, subset and weight-limited (#49)
- [x] Phrase-colour contrast — solved structurally by #48 (theme tokens only)

### Not blocking

- [ ] Real `.dev` domain → `site/src/data/site.ts` `url`, then canonical URLs
      and the vCard are correct. Owner wants to review the site first
- [ ] Push the repo to GitHub and deploy to Cloudflare Pages (root `site/`,
      build `npm run build`, output `dist`) — needs the owner's accounts
- [ ] Echo's Devpost URL, if the team submitted one — the row simply doesn't
      render until it exists
- [ ] Lookout and Wizlet content — both sit as `draft: true`; flipping the flag
      is the only publish step
- [ ] A Myanmar-capable font **before** any Burmese book is entered (#32) — the
      Burmese shelves exist and stay hidden until then
- [ ] Keystatic panel, last, per #2 — the schemas are strict so it has something
      clean to bind to

### Observed during the build, not acted on
- Dark mode: the mascot's black hair does lose definition against the dark
  ground, as #12 anticipated. No backing plate was added — it would change how
  the character reads. Fine on the screens checked; keep an eye on it.
- One real-device pass (an actual phone, an actual OS reduced-motion setting)
  is still worth doing before deploy. Everything was verified in a real browser
  engine (headless Chromium with emulated viewport/motion/no-JS), which is
  running-the-thing, but not the same as holding the thing.

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
| `site/` | **The site.** Astro 7, built to the HANDOFF architecture 16 Aug, builds clean (0 errors / 0 warnings / 0 hints), content-complete, all assets self-hosted |
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

**The HANDOFF architecture is built, content-complete, and verified by
execution** (16 Aug evening session). Running locally on `:4321`; `astro build`
and `astro check` both clean (0 errors / 0 warnings / 0 hints).

- Seven routes: `/` (2-col masonry, four tiles, Hero V2 welcome), `/about`,
  `/projects`, `/reading`, `/w-phrases`, `/contact`, `/contact.vcf`
- Geist Pixel subset 3.6 MB → 26 KB woff2, ELSH axis kept, default instance 0;
  `font-synthesis: none`; 4px-multiple scale; five phrase-only families (#49)
- Riso C2 tokens light/dark (#44); mascot palette preserved as `--px-*` for
  spines only (#45)
- Business card on every page: corner card → spin-and-travel dialog; full-screen
  tab on phones; plain `/contact` link with no JS; Escape closes
- All six scenes wired per #40, including one-shot workbench-zap that holds the
  singed pose, and the two-mode scroll traveller (#50)
- Verified by running: 0 horizontal overflow at 320/375/768/1280 on every
  route; dark theme; reduced motion (wall static, traveller hidden, scenes
  frozen); no-JS (shelves, phrases, card faces, contact all render); keyboard
  flip uses `inert` on the face-down side; no third-party requests — all 7
  font files self-hosted in `dist/_astro/fonts/`
- Content: 2 projects live + 2 drafts, 2 books with real dates/progress,
  4 phrases including the Drake line, 12 photos, live `resume.pdf`

---

## Housekeeping

**Version control: resolved.** The root is a git repository on `main` with the
full 16 Aug history: baseline → animation consolidation → build → photo wiring →
owner facts → this ledger update. Cloudflare Pages (#11) still needs it pushed
to GitHub, which needs the owner's account.

`.qa/` at the root is a gitignored scratch area holding the Playwright
screenshot/verification harness (`shoot.mjs`, `verify.mjs`) — useful for
re-running the acceptance sweep, safe to delete.

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
| API keys visible in a supplied photograph | Resolved | Photo dropped from the published set (#51); owner reports the keys were rotated long ago |
| Hero V2 exists but its page-level placement is unresolved | Resolved | Mapping and runtime rules are recorded in `ANIMATION_ASSETS.md` and HANDOFF §11; executed 16 Aug |
| Motion accessibility not executed on a real browser/device | Mostly resolved | Verified in headless Chromium with `reducedMotion: reduce` emulation (wall static, traveller hidden, scenes frozen). One pass on a physical device before deploy remains prudent |
| `url` still `https://example.dev` | Open, low | Canonical URLs and the vCard carry the placeholder until the owner buys the domain and updates `site.ts` |

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

### 2026-08-16 (evening) — Build the HANDOFF site, end-to-end

- Objective: Execute `HANDOFF.md` inside the existing `site/`, then land the
  owner's real content.
- Completed: All seven routes; Geist Pixel pipeline (26 KB woff2, ELSH kept);
  Riso C2 theme with light/dark; new/updated components (`NavPill`,
  `BusinessCard`, `HeroWelcome`, `ProjectCard` flip deck, `BookSpine` shelf,
  the W Phrases marquee, one-shot support in `AnimatedScene`, two-mode
  `ScrollTripMascot`); schemas rewritten with named failures; `contact.vcf`
  regenerated; owner's 12 photos + 6 screenshots wired; Drake phrase, book
  dates/progress, `resume.pdf` landed. Decisions #48–#51 locked.
- Verification: `astro build` + `astro check` clean; Playwright sweep across
  320/375/768/1280 on every route (0 horizontal overflow); dark theme,
  reduced-motion emulation, no-JS, keyboard-flip `inert`, and the business-card
  dialog all verified by execution; no third-party requests in `dist/`.
- Risks or blockers: none blocking. Domain, GitHub push, and Cloudflare deploy
  are the owner's to run.
- Next: owner reviews the running site and sends refinements.

## Next session

1. **Owner review pass** — the site runs at `:4321` (`npx astro dev
   --background` in `site/`). Collect refinements and apply them.
2. Buy the `.dev` domain, set `url` in `site/src/data/site.ts`.
3. Push to GitHub, deploy to Cloudflare Pages (root `site/`, build
   `npm run build`, output `dist`), connect the domain (#11).
4. One physical-device pass before the domain goes public: a real phone, OS
   reduced-motion on, both themes.
5. Echo's Devpost URL if it exists; Lookout/Wizlet whenever the owner is ready
   (`draft: false` is the only step).
6. `plan.md` is historical — `HANDOFF.md` and this ledger are the record. No
   rewrite needed; leave it labelled superseded.
7. Keystatic panel last, per #2 — the schemas in `src/content.config.ts` are
   written strictly so it has something clean to bind to.
8. A Myanmar-capable font before the first Burmese book (#32).
