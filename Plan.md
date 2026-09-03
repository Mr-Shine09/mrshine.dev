# Plan.md — Oak's portfolio site

**Written:** 2 September 2026
**Supersedes:** `HANDOFF.md`, `plan.md`, `ledger.md`, and `docs/{about-me,contact,projects,reading-list,w-phrases}.md`. All of those are deleted; their still-valid decisions, verbatim copy, and reasoning live here. Git history has the originals.
**Design source:** `docs/Website-Plan.pdf` — four hand-drawn pages by the owner (2 Sep 2026). Where this document and the sketch disagree, the sketch wins unless a decision below says otherwise.
**For:** a build session starting cold. Read all of it. No other document is required.
**Day-to-day edits** (books, highlights, projects, copy): see `instruction.md` at the repo root.

---

## 0. Decisions at a glance

| Topic | Decision |
|---|---|
| Structure | **One scrolling page** at `/`. Nav anchors in order: About · Highlights · Projects · Personal · Contact. "Personal" is the Reading List. |
| Stack | Astro (existing `^7.2.2` shell in `site/`), plain CSS with custom properties, no CSS framework, no UI framework, minimal JS. |
| Hosting | Cloudflare Pages connected to the GitHub repo; every push to `main` redeploys. Domain **`mrshine.dev`**, bought through Cloudflare Registrar on 2 Sep 2026. |
| Type | **Geist Pixel** as a display accent (hero name, section titles, watermark, band, closing). **Geist Sans** for everything else, including nav, labels, chips and buttons. Both self-hosted woff2. |
| Theme | **Riso C2**, light and dark, toggle persisted in `localStorage`, `prefers-color-scheme` honoured on first visit. |
| Mascot | Native APNG scenes from `site/public/assets/animation/`. Used: `oak-welcome`, `trophy-lift`, `workbench-zap`, `reading-fire`, `run`. Unused but kept: `computer-working`, `thinking-cloud`, `walking`. **Every scene loops continuously** (owner, 2 Sep 2026); scenes render at 0.75 so the figure matches the hero. |
| Projects | Coverflow slider, four uniform single-face cards: **PokeDesk, Look-Out, VisionAssist, Echo**. |
| Reading | Currently-reading cards with progress rings (Dune; The Infinity Machine); shelves of **cover images** for **finished** books only; empty state at launch. |
| Contact | One business-card block at the end: Website, Email (+ copy), LinkedIn, GitHub. No floating card. No form. |
| Dropped | W Phrases, About photo galleries, floating business card, masonry home grid, hobbies, "Ahead" section, flip cards, rendered spines, Wizlet, the six-font specimen set. |
| Rejected tools | Framer (GUI-only, paid domain, pixel rendering needs overrides, site stops being a portfolio artefact). WebGL / three.js (standing exclusion). |

---

## 1. Purpose, audience, voice

The owner's own framing, which governs every judgement call:

> **"A personal time capsule, describing who I am and what I love to do."**

Written for everyone — friends, recruiters, whoever finds it. Not a résumé, not a transfer application. Legible to a non-technical reader; it should never smell like a personal statement. Recruiters get Résumé, GitHub, and LinkedIn in the first screen; everyone gets the person below.

**Register:** first person, plain, specific, a little dry. No "passionate about leveraging technology." No inspirational-immigrant-narrative voice — the origin is stated as a fact and left there, deliberately.

**Deliberately excluded — do not add:** the date he moved, his age at the time, why he moved, or any account of the move itself. This was an explicit decision.

**Owner identity facts** (confirmed, not to be invented around): Oak Soe Khant. Second-year Computer Engineering student at De Anza Community College, transferring 2027. From Yangon, Myanmar. Lives in Santa Clara, California.

---

## 2. Non-negotiables

1. **Works on a phone and a laptop with no issues.** The owner's top priority. **No horizontal body scroll at 320px, ever.** Wide content scrolls inside its own `overflow-x: auto` container.
2. **Never fake a bold.** `font-synthesis: none` globally. Geist Pixel has no weight axis.
3. **Every motion respects `prefers-reduced-motion: reduce`.** Scenes freeze on their static frame, the runner is hidden, the plane stops, the slider's scale effect is removed.
4. **Nothing essential lives behind JavaScript.** Every section, link, and piece of contact information works with scripting off.
5. **No WebGL, no three.js.**
6. **The mascot player fails open.** Looping scenes animate immediately; `IntersectionObserver` only *pauses* them offscreen. Only one-shot scenes wait to be seen. Gating everything on IO froze every mascot on frame 0 where IO never fired. **Do not "optimise" this into a gate.**
7. **The mascot keeps its own frozen 12-colour palette.** Never recolour it to the page theme. It reads as a full-colour object on a duotone page; verified by compositing.
8. **Every tap target ≥ 44px**, including book covers and slider controls.
9. **Every interactive element has a visible keyboard focus state.**

---

## 3. Stack and hosting

| | |
|---|---|
| Framework | Astro `^7.2.2` (`site/package.json`), Node ≥ 22.12. Zero integrations. `astro.config.mjs` holds only the `fonts` array. |
| Content | Local files: markdown + frontmatter in `site/src/content/`, validated by zod content collections **with named build failures**. Keystatic or any admin UI is a later option, not now. |
| Styling | Plain CSS. Tokens in `src/styles/tokens.css`, resets and utilities in `src/styles/global.css`, component styles scoped in `.astro` files. |
| JS | Astro ships none by default. Scripts allowed: theme toggle, active-nav highlighting, scene player (APNG/static swap), slider prev/next, email copy button, bottom runner. Each is progressive enhancement over working HTML. |
| Fonts | `fontProviders.local()` for both faces. **No `fontProviders.google()` entries** — the five that existed served W Phrases and were the site's only third-party requests. |
| Hosting | Cloudflare Pages. Build command `npm run build`, output `dist`, root `site`. Free tier, automatic HTTPS. |
| Domain | **`https://mrshine.dev`** — registered 2 Sep 2026 through Cloudflare Registrar, DNS zone on Cloudflare. `.dev` is HSTS-preloaded, so HTTPS is mandatory and automatic. `site.url` is set to it; the Pages custom-domain step (§14.4) is still to do. |
| Updating content | Edit or add a markdown file, commit, push. Cloudflare redeploys. This is what "books must be updatable" means in practice; see §7.4. |

### Why these (carried reasoning)
- Astro: near-zero JS suits a content site with a handful of animated images (ledger #3).
- Content in files, admin last: keeps the site owner-editable in git without a service (ledger #2).
- Cloudflare host + registrar together avoids a DNS hand-off step (ledger #11).
- Amend the `site/` shell rather than re-scaffold: the config, font pipeline, vCard endpoint, and validation pattern are hardened by runtime failures already found (ledger #47). The **source tree** (`site/src` pages, components, styles) is rebuilt from scratch in the build session; `site/src/assets` is kept.

---

## 4. Type system

### 4.1 Two families
| Face | File | Use | Licence |
|---|---|---|---|
| **Geist Pixel** | `site/src/assets/fonts/geist-pixel.woff2` (subsetted from the 3.6 MB TTF in `fonts/source/geist-pixel/`) | Display accent only (owner, 3 Sep 2026): hero name, `h2` section titles, shelf titles, watermark words, band, closing line, contact-card name | SIL OFL 1.1 — ship `OFL.txt` |
| **Geist Sans** | `site/src/assets/fonts/geist-sans.woff2` — download from the Vercel `geist-font` GitHub release, subset to Latin (same `pyftsubset` recipe below), weights 400 and 500 only | Everything else: prose, `h3` item titles, nav, labels, chips, buttons, counts, dates, ring percentage — small type as letterspaced small caps at weight 500 | SIL OFL 1.1 — ship `OFL.txt` |

Subset recipe (both faces):
```bash
pyftsubset "<source>.ttf" --output-file="<name>.woff2" --flavor=woff2 \
  --layout-features='*' --unicodes="U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-205E" \
  --name-IDs='*' --notdef-outline
```
Target ≈ 30–80 KB each. Register both with `fontProviders.local()` and emit metric-matched fallbacks so the swap does not shift layout.

### 4.2 Geist Pixel rules
- Single variable axis **`ELSH` (Element Shape), 0–100**. It is not weight. **Values 20–80 render hollow and low-contrast** (verified). Any real text uses **0 or 100**. Mid-axis is decorative only.
- **There is no bold.** Emphasis devices, in order: size step (hierarchy), accent colour (inside running text), uppercase + letterspacing (labels, chips, nav, shelf titles, counts).
- Pixel faces are crisp at integer multiples of their grid. Scale on **multiples of 4px**, never fractional:
  ```
  --fs-xs 12px  labels, captions     --fs-md 20px
  --fs-sm 14px  secondary            --fs-lg 28px
  --fs-base 16px  prose floor        --fs-xl 40px    --fs-2xl 56px  hero name
  ```
- **16px is the floor for prose.** 14px for labels and metadata only. 12px for captions only.
- The face is monospaced and wide. Check every heading and the tagline at **375px** — the most likely overflow source.

### 4.3 Burmese
Neither face has Myanmar glyphs (Geist Pixel: 421 glyphs, 0 in U+1000–109F). A Burmese book title would render as tofu **and the build would still succeed** — the one silent failure on the site. Before any `language: my` book ships: self-host **Noto Sans Myanmar** or **Padauk**, mark the text `lang="my"`, give it extra line-height for stacked diacritics. **Add a named build failure:** `language: my` present while no Myanmar font is configured.

---

## 5. Theme — "Riso C2"

Two flat inks on a pale ground, print-shop register. The mascot is exempt (§2.7).

### 5.1 Tokens (`src/styles/tokens.css`)
```css
:root {
  --bg:      #F0ECFA;   /* pale lilac ground */
  --ink:     #3B1E7A;   /* deep violet — primary text */
  --accent:  #C43A18;   /* coral/rust — second ink */
  --muted:   #695A87;   /* secondary text */
  --line:    #D9D0EC;   /* rules, borders, plate edges */
  --plate:   #E4DDF4;   /* card-front colour plate */
}
[data-theme="dark"] {
  --bg:      #150E2B;
  --ink:     #E7DEFB;
  --accent:  #FF7A55;
  --muted:   #A99BC9;
  --line:    #2E2450;
  --plate:   #221846;
}
```

### 5.2 Contrast — measured, all pass WCAG AA for body text
| Mode | Token | Ratio vs `--bg` | Ratio vs `--plate` |
|---|---|---|---|
| Light | `--ink` | 10.94 | 9.65 |
| Light | `--accent` | **4.56 — no headroom** | 4.02 (glyphs/strokes only, 3:1 applies) |
| Light | `--muted` | 5.30 | 4.67 |
| Dark | `--ink` | 14.38 | 12.62 |
| Dark | `--accent` | 7.23 | 6.35 |
| Dark | `--muted` | 7.28 | 6.39 |

`--muted` is used as text on `--plate` (contact card, currently-reading cards, book detail), so it must clear 4.5:1 on both surfaces.

> Light `--accent` clears 4.5 by 0.06. **Do not lighten it, and do not darken `--bg`.** If either changes, re-measure before committing.

### 5.3 Toggle
`data-theme` on `<html>`, persisted in `localStorage`, `prefers-color-scheme` respected on first visit. An inline `<script>` in `<head>` applies the stored theme before first paint to avoid a flash. With JS off the site renders in the system-preferred mode via `@media (prefers-color-scheme: dark)` mirroring the dark tokens.

---

## 6. Responsive

Mobile-first. Test at **320, 375, 768, 1280**.

| Component | Phone behaviour |
|---|---|
| Top bar | Compact single row; nav labels shrink to `--fs-xs` uppercase; still plain anchor links. No hamburger. Theme toggle stays. |
| Hero | Stacks: text → mascot → portrait. Portrait max 60vw. |
| Projects slider | Cards ~85vw wide, one centred; neighbours peek at the edges. Scroll-snap. |
| Shelves | Each shelf scrolls horizontally in its own container with a visible edge fade. Keyboard scrollable. |
| Contact card | Full width, single column of rows. |
| Runner | Half size (96×80), bottom above `env(safe-area-inset-bottom)`, never over a control. If it collides with the sticky bar or a button at 320px, hide it below 40rem instead. |

**Absolute rule: no horizontal page scroll at any width.**

---

## 7. Page spec — one route, five sections

Section order: About → Highlights → Projects → Personal (Reading List) → Contact. Each `<section>` has an `id` matching its nav anchor and a heading in Geist Pixel.

### 7.0 Sticky top bar
- Left: favicon mark (`public/favicon.png`, 32px), links to `#top`.
- Right: `About | Highlights | Projects | Personal | Contact` as anchor links. Active section gets `aria-current="true"` via `IntersectionObserver` (enhancement only). Theme toggle at the far right.
- Background `--bg` with a `--line` bottom rule. Collapses in height on scroll if simple; not required.

### 7.1 About / hero — `#about`
Three columns on desktop (text · mascot · portrait), stacked on phone.

**Left column**
- `Yangon ✈ Bay Area, CA` motif: two place names, an arrow, a small plane on the arrow. Muted colour, no heading, no border. Small — a corner element, not a band. This is the only place the origin-to-here fact is stated visually, and it works because it says nothing more. If the plane animates along the arrow, slow and subtle, frozen at one end under reduced motion.
- **OAK SOE KHANT** at `--fs-2xl` (`--fs-xl` on phones).
- `Computer Engineering @ De Anza` in Geist Pixel, uppercase, letterspaced.
- Tagline, Geist Sans, one line where it fits:
  > Building cool products to boost productivity. Hackathon fanatic. Mindful AI user. Reader in progress.

  "Hackathon fanatic" is singular. "Reader in progress" is deliberate and honest — do not upgrade it to "avid reader". Acceptable shorter alternative if needed: "Becoming a reader."
- Three icon links **with visible text labels**, each ≥ 44px: **Résumé** (`/resume.pdf`), **GitHub**, **LinkedIn**. Working links — no placeholders.

**Middle column** — `oak-welcome` hero animation (`hero/oak-welcome-atlas.png`, 160×208, contract `hero/oak-welcome-contract.json`). **No border, no box.** Integer scale (×1 on phone, ×2 from 768px). Static companion under reduced motion and while offscreen.

**Right column** — `portrait.jpg`, **with a visible border**: 2px `--line` on a `--plate` field, square-ish crop. It is a side profile by choice — never substitute a face-forward shot.

**Two more lines, both in, both verbatim (owner opted in, 2 Sep 2026):**
- **Lead**, above the tagline, Geist Sans `--fs-md`: *"What's up everyone!!! My name is Oak, a Second-year Computer Engineering student at DeAnza Community College, transferring in 2027."* Three exclamation marks intentional. No second paragraph — the "I like building things that make a day run better…" line was cut and must not return.
- **Closing line**, set large in Geist Pixel (`--fs-lg`, `--fs-md` on phones) as the last element of the hero, full width under the three columns: *"Leveraging artificial intelligence to sharpen actual intelligence."* One line, no gloss, no supporting prose. The wordplay does not survive being explained.

Check the lead at 375px: with Geist Sans it wraps to three lines, which is fine; it must not push the icon links below the fold on a 667px-tall phone. If it does, tighten vertical spacing before touching the copy.

### 7.2 Highlights — `#highlights`
- Trophy emoji 🏆 centred above the heading **HIGHLIGHTS**.
- `trophy-lift` scene to the left of the columns, **looping** (the owner asked for every animation to run continuously; the play-once-and-hold rule is retired). Static companion under reduced motion.
- **Two columns** (afig.dev pattern, 2 Sep 2026): **Awards & contests** (every `kind` except `hackathon`) and **Hackathons** (`kind: hackathon`), each headed by an accent-underlined label. Rows: Tabler glyph (trophy / code) · title · `org · year`. `year` is optional so an event with no supplied date renders without one. Rows ≥ 44px.
- When the awards column has fewer than three entries, render *"More achievements coming soon."* under it. The threshold lives in one constant.

**Launch content:** Awards — **ICPC Pacific Northwest Regional, Division I — Participant**, ICPC, **2025**. Hackathons — **DA Hacks 3.5** and **DA Hacks 4.0** (De Anza College, 2025), **Hack for Humanity 2026 — built Echo** (Santa Clara University), **UC Berkeley AI Hackathon 2026 — built Look-Out** (UC Berkeley).

### 7.3 Projects — `#projects`
- Centred heading **PROJECTS**; the `workbench-zap` scene sits in the right margin on wide screens (absolutely positioned inside the head, never pushing the title off-centre) and centred below the heading otherwise. It **loops** (owner decision, 2 Sep 2026; the play-once rule is retired).
- **Coverflow slider.** A horizontal `overflow-x: auto` track with `scroll-snap-type: x mandatory` and centre alignment. The centred card is scale 1.0, full opacity; neighbours scale ≈ 0.82 at ≈ 0.6 opacity. The scale/opacity comes from **CSS scroll-driven animations** (`animation-timeline: view(inline)`), so it needs no JS; browsers without support get a flat snap carousel, still fully usable. Under reduced motion the scale effect is removed.
- **Controls:** prev/next buttons (JS, `scrollBy` one card), native touch/wheel scroll, and keyboard — each card is focusable and Left/Right arrows move focus and scroll it into view. Edge fade on both sides signals more content. The track never widens the body.
- **Card (single face, uniform size):**
  - Image matted on a `--plate` field with `object-fit: contain`, never cropped. Forced by the material: Echo's screenshots are ~9:19.5 phone portraits, PokeDesk's are ~1800×250 dock strips; no single crop serves both, and a 4:3 crop cuts Echo's `MESH ACTIVE` badge. `imageAlt` required.
  - Title (Geist Pixel `--fs-md`), one-line summary (Geist Sans), stack chips (Geist Pixel `--fs-xs` uppercase), year and `builtAt` if present, collaborators if any, then links: **GitHub** (always, a plain `<a>` so it works with JS off), **Devpost** when present.
- **Four cards, this order.** Facts below are from the repos; do not embellish.

| # | Project | Year / where | Stack chips | Summary (verbatim where quoted) | Image | Links | Collaborators |
|---|---|---|---|---|---|---|---|
| 1 | **PokeDesk** | 2026, solo | Swift · SwiftUI · AppKit · Python 3 · XcodeGen | *"A tiny pixel-art mascot that lives at the bottom of your Mac's screen and shows, at a glance, what your coding agent is doing."* | `src/assets/projects/pokedesk-hero.png` — alt: *Two pixel mascots on a purple desktop above the macOS dock — one working at a desk, one walking.* | `https://github.com/Mr-Shine09/PokeDesk` | — |
| 2 | **Look-Out** | UC Berkeley AI Hackathon 2026 | Python 3.11 · FastAPI · Redis Stack · Vite · Ollama / Claude · Browserbase | The first alert tool built to notify you *less*: semantic dedup in Redis vector search plus an LLM relevance judge, so only genuinely new and relevant items surface. | Repo `public/lookout-eye-1024.png` (logo, matted) → save as `src/assets/projects/lookout-eye.png`. `TODO(owner)`: a dashboard screenshot when available. | `https://github.com/Mr-Shine09/Look-Out` | `TODO(owner)` — the README has a Team section |
| 3 | **VisionAssist** | 2026, De Anza, Infineon-sponsored capstone | Python · YOLOv8n · Raspberry Pi 5 · Arducam IMX708 · Piper TTS · Flask | Wearable obstacle detection and spoken navigation for the visually impaired. Runs fully offline on a Raspberry Pi 5. | Repo `docs/images/hero.jpg` (device photo) → `src/assets/projects/visionassist-hero.jpg` | `https://github.com/Mr-Shine09/VisionAssist` | Five-person team — names `TODO(owner)` |
| 4 | **Echo** | Hack for Humanity 2026 (V3) — SCU | Flutter · Dart · Kotlin · Swift · SQLite · Python 3 | *"A Flutter prototype for receiving, storing, and relaying emergency alerts between nearby devices over Bluetooth Low Energy when an internet connection is unavailable."* | `src/assets/projects/echo-hero.webp` — alt: *Echo's alert list with the MESH ACTIVE badge lit and severity chips down the feed.* | `https://github.com/aadityad12/Echo` (the **original repo, not a fork**); Devpost `TODO(owner)` | **aadityad12 · shahxsheel · Mr-Shine09** — name all three. Presenting a team build as solo is the one mistake that costs more than having no portfolio. |

- The existing "what was hard" bodies for PokeDesk and Echo (`src/content/projects/01-pokedesk.md`, `02-echo.md`) stay in the files. The single-face card shows the summary only; the body is available for a future detail view. Keep the PokeDesk angle: lead with the sixteen-states / frozen-contract writeup, close with one sentence on chat detection resting on a single English UI string, hence opt-in.
- Wizlet is removed. Zephyr (pinned on GitHub) is not included unless the owner adds a file.

### 7.4 Personal / Reading List — `#personal`
- `reading-fire` scene at left (ambient loop: breathing, blink, fire flicker, page turn; pauses offscreen). Heading **READING LIST**. Under it a letterspaced count **derived from data**, never hardcoded: e.g. `2 VOLUMES · 0 FINISHED`.
- **Currently Reading.** One card per `status: reading` book. Card: cover (from `src/assets/books/<slug>.jpg` when present, else a plain `--plate` rectangle with the title), title, author, started date, **progress ring** — an SVG circle with `stroke-dasharray`, `role="progressbar"`, `aria-valuenow`, and the percentage as visible text — and the brief `note` if present. The layout reserves two slots side by side (the sketch's "save some space for second book"); with one book the second slot is an empty plate.
- **Shelves.** Grouped **language → genre**: `English → Fiction`, `English → Non-Fiction`, then `Burmese → …` only when data exists. Status is never a shelf. Each shelf: title in Geist Pixel uppercase, a count, then a horizontal scroll container of **cover images** (Carol's Library reference) — each cover a `<button>`/summary ≥ 44px tall, natural cover aspect, edge fade, keyboard scrollable. **Only `status: finished` books appear on shelves.**
- **Empty state.** Both shelves are empty at launch, so **an empty shelf renders an intentional message** rather than disappearing: *"Nothing finished yet."* followed by the current book with the highest progress, e.g. *"Dune is at 73%."* Derived from data.
- **Detail panel.** Clicking a cover opens its details **below the shelf** using a native disclosure (`<details>`/`<summary>` or a JS-enhanced equivalent with the same no-JS behaviour). No modal, no focus trap. Contents: cover, title, author, status, started, ended, rating (stars decorative; accessible text *"Rated 4 out of 5"*), note/review. **Rating, ended, and review are absent until a book is finished**, and the panel must look complete without them — a book being read shows started date and progress, and that is enough.
- **Search** is deferred until the shelves hold ten or more books. Not in launch scope. When added: client-side, filters title and author, `aria-live` result count, hidden with JS off, matches raw strings — never normalise in a way that assumes Latin.
- **Tone** from the time & space reference: uppercase letterspaced labels, plain or bracketed counts, calm spacing. Headings and counts only.

**Adding or updating a book — the recipe to document in the site README:**
1. Create `site/src/content/books/<slug>.md` with the frontmatter in §8.
2. If it has an `isbn`, run `npm run covers`. The script fetches `https://covers.openlibrary.org/b/isbn/<ISBN>-L.jpg` into `src/assets/books/<slug>.jpg`, skips files that already exist, and **fails loudly on a 404 or a 1×1 placeholder** so a missing cover is noticed, not silently blank.
3. Commit and push. Cloudflare redeploys.
Finishing a book = change `status` to `finished`, add `ended`, `rating`, `review`, remove `progress`, push.

**Launch content (two books reading, none finished):**
- **Dune** — Frank Herbert, `en`, `fiction`, `reading`, started 2026-08-01, progress 73 (p. 302 of 412), pageCount 412, **isbn `9780441013593`** (Open Library has the cover; verified 2 Sep 2026).
- **The Infinity Machine: Demis Hassabis, DeepMind and the Quest for Superintelligence** — Sebastian Mallaby, `en`, `nonfiction`, `reading`, started `TODO(owner)`, progress `TODO(owner)`, **isbn `9780593831847`** (hardcover — Open Library has this cover). The owner's copy is the US digital edition, ISBN 979-8217336661, which has **no cover on Open Library**; keep the hardcover ISBN in the file so `npm run covers` succeeds, and note the digital ISBN in a comment if wanted.
- **Zero to One** (Peter Thiel) is **removed** — replaced by The Infinity Machine at the owner's request. Delete `src/content/books/zero-to-one.md`.

### 7.5 Contact — `#contact`
A single block styled as a business card, centred, max-width ≈ 36rem.
- Top: **OAK SOE KHANT** (Geist Pixel), `Computer Engineering @ De Anza`, the favicon mark in the top-right corner, a `--line` rule.
- Then a **labelled list, not icon soup** — icon · label · value, each row ≥ 44px:
  1. **Website** — `https://mrshine.dev`, shown as `mrshine.dev`.
  2. **Email** — `oaksoekhant182209@gmail.com`, visible and selectable, as a `mailto:` link, with a **copy-to-clipboard button beside it** (never replacing it). Success announced in an `aria-live` region. With JS off the button is hidden.
  3. **LinkedIn** — `https://www.linkedin.com/in/oak-soe-khant-350252362`
  4. **GitHub** — `https://github.com/Mr-Shine09`
  5. **Save contact** — `/contact.vcf` (quiet fifth row; owner may drop it).
- `rel="me"` on social links; `rel="noopener"` on anything opening a new tab; prefer same-tab. Blank fields drop rather than render empty.
- **No contact form.** Static host, no backend; a form means a third-party service and a spam problem. An email address is a form that already works.
- **No decorative mascot here.**
- `contact.vcf` is a **real file generated at build time** (`src/pages/contact.vcf.ts`) from `src/data/site.ts`, so right-click-save and no-JS work. It carries name, email, URL, GitHub, LinkedIn, Instagram, Facebook, Devpost, and the Santa Clara location. Instagram, Facebook, and Devpost live in `site.ts` for the vCard but do not render on the card.

### 7.5b Visual devices (2 Sep 2026, afig.dev-inspired, kept inside Riso C2)

- **Highlighter marks**: `<mark>` = a 22% coral wash behind key phrases (lead: "Computer Engineering", "transferring in 2027"; tagline: "Hackathon fanatic", "Reader in progress"). Copy stays verbatim; `Marked.astro` only wraps. Text contrast on the wash is asserted ≥ 4.5 in both themes (`mark-contrast`).
- **Name block**: the first name sits on a `--plate` block inside the single `h1`.
- **Buttons**: primary = solid ink with an accent icon square (Résumé); outline = quiet border with a ↗ corner arrow for links that leave the page (GitHub, LinkedIn, project repos).
- **Icons**: inline SVG via `Icon.astro` — **Devicon** for brands and stack chips (GitHub, LinkedIn plain variant, Swift, Python, Flutter, Dart, Kotlin, SQLite, FastAPI, Redis, Vite, Flask, Raspberry Pi, PyTorch, Apple, Xcode), **Tabler** for generic glyphs (mail, world, file-text, address-book, arrow-up-right, trophy, code). No icon request leaves the page. `mono` recolours brand fills to `currentColor` for links; stack chips keep brand colours.
- **Section heads**: centred pixel-face title, hairline rule, and a ghosted watermark of the section name at ~5% ink behind it; sections use `overflow-x: clip` so the word never widens the body.
- **Divider band** before Reading: full-bleed ink ground with paper text — "Reader *in progress*." — and a ghosted READING behind it.
- **Ruled paper** for Reading: `--plate` tint with a `--line` hairline every 28px; the currently-reading cards sit on `--bg` so they lift off the paper. The reading-fire scene is sticky beside the list on wide screens.
- **Contact card**: 2px ink border with an 8px hard ink offset shadow, Devicon/Tabler row icons, a soft accent wash on row hover.
- **Motion**: `[data-reveal]` elements fade and rise 18px on first sight (one shared IntersectionObserver in `Base.astro`; `html.js` gates the hidden state so nothing is hidden with JS off); project cards lift on hover; the progress ring draws from 0 to its value on reveal. All disabled under reduced motion; asserted by `reveal`.

### 7.6 Bottom runner (site-wide, decorative)
The `run` scene travels along the bottom of the viewport as the visitor scrolls: **parked just off the right edge at scroll 0, arriving at the left edge at the bottom of the page.**
- Chassis: a fixed `inset: 0` layer, `pointer-events: none`, `contain: strict`, `z-index` below the top bar; the sprite `position: absolute; left: 0; bottom: max(0.65rem, env(safe-area-inset-bottom))`, **192×160** on laptops and **96×80** on phones, `image-rendering: pixelated`.
- Progress = `scrollY / (scrollHeight − innerHeight)`, clamped 0–1, from a passive scroll listener, rAF-batched, eased with a lerp (`rendered += (target − rendered) × 0.14`, loop exits below 0.0002 delta).
- Position: `travel = innerWidth + w × 2.4`; `x = innerWidth + w × 0.7 − progress × travel`. The scene is authored running **toward the viewer's right**, so apply `scaleX(−1)` for this leftward travel.
- **Stride only while scrolling.** APNGs cannot be paused from JS, so: when the lerp settles, swap `src` to `run-static.png`; on the next scroll, swap back to `run-atlas.png` with a `?play=N` cache-buster (restarts the 12-frame, 12 fps loop — acceptable).
- Hidden entirely under `prefers-reduced-motion: reduce` (CSS, no JS branch). On phones: half size, kept clear of the top bar and any button; hide below 40rem if it ever overlaps a control at 320px.
- Never creates layout width or body scroll.

### 7.7 Scene player rules (all stationary scenes)
- One component (`AnimatedScene.astro`) reads `public/assets/animation/scenes/scene-contract.json`; an unknown scene id **throws at build time**. Frame size 384×320, hero 160×208. **Scene art is stored at 2× its native pixels** (every pixel run is even), so the default display scale is **0.75 → 288×240**. The trophy uses that default; the **workbench and reading scenes render at 0.5 (192×160)** because their frames include furniture and read far larger than the lone trophy figure at the same scale (owner, 3 Sep 2026). The runner is smaller than the stationary scenes — 192×160 on laptops, 96×80 on phones — so it never dominates the viewport (owner, 3 Sep 2026).
- **Outline pass (2 Sep 2026):** `trophy-lift`, `workbench-zap` and `run` had a pale rim of edge pixels that haloed on dark backgrounds. `scripts/fix-scene-outlines.py` recolours only fully opaque edge pixels with mean RGB > 150 to the mascot ink (#111219) on every frame; interior colours and alpha are untouched. Originals are in `site/archive/animation/pre-outline-fix/`. `--check` fails if a light rim reappears (harness check `scene-outlines`).
- Astro does not propagate a parent's style scope to a child component's root, so parents position scenes through a wrapper `<div>` they own, never through a class passed to `AnimatedScene`.
- Each scene = APNG `*-atlas.png` (animation with embedded timing — never treat as a sprite sheet) + `*-static.png` first-frame companion.
- Play = set `img.src` to the APNG with a `?play=N` cache-buster (restarts from frame 0). Pause = set `src` to the static PNG.
- `IntersectionObserver` (`rootMargin: 160px`) toggles visibility; `apply()` also runs immediately after observing so nothing waits on IO (§2.6).
- `once` mode plays on first reveal and never reverts to static.
- `matchMedia("(prefers-reduced-motion: reduce)")` short-circuits to static and re-applies on `change`.
- Keep `image-rendering: pixelated`, integer scale, the frozen palette, and the authored three-quarter facial angles. Do not put words or icons inside the thinking cloud (unused today, rule stands).

---

## 8. Content data and validation

```ts
// src/data/site.ts
type SiteConfig = {
  name: "Oak Soe Khant";
  role: "Second-year Computer Engineering student, De Anza Community College";
  shortRole: "Computer Engineering @ De Anza";
  location: "Santa Clara, California";
  origin: "Yangon";                       // for the ✈ motif only
  tagline: string;                        // §7.1, verbatim
  socials: {
    email:     "oaksoekhant182209@gmail.com";
    github:    "https://github.com/Mr-Shine09";
    linkedin:  "https://www.linkedin.com/in/oak-soe-khant-350252362";
    instagram: "https://www.instagram.com/oak_soe_khant909";   // vCard only
    facebook:  "https://www.facebook.com/johnwick.wick.37625"; // vCard only
    devpost:   "https://devpost.com/oaksoekhant182209";        // vCard only
  };
  resumeUrl: "/resume.pdf";               // file exists at site/public/resume.pdf
  url: "https://mrshine.dev";             // registered 2 Sep 2026
  seo: { description: string };
};

// src/content/achievements/<slug>.md
type Achievement = {
  title: string; org: string; year: string;
  kind: "competition" | "hackathon" | "award" | "other";
  link?: string;                          // z.url()
  order: number;
};

// src/content/projects/<nn>-<slug>.md   (body = what was hard)
type Project = {
  title: string; order: number; year: string;
  stack: string[]; summary: string;
  image?: string; imageAlt?: string;      // imageAlt REQUIRED when image exists
  collaborators: string[];                // default [] = solo
  builtAt?: string;                       // e.g. "Hack for Humanity 2026 (V3) — SCU"
  links: { github?: string; devpost?: string; live?: string };  // z.url()
  draft: boolean;                         // default false; true = filtered out
};

// src/content/books/<slug>.md
type Book = {
  title: string; author: string;
  isbn?: string;                          // drives `npm run covers`
  language: "en" | "my";
  genre: "fiction" | "nonfiction";
  status: "reading" | "finished";
  started?: string; ended?: string;       // ISO dates
  progress?: number;                      // 0–100, only when status = reading
  rating?: 1 | 2 | 3 | 4 | 5;             // only when status = finished
  review?: string;                        // only when status = finished
  note?: string;                          // brief note, any status
  pageCount?: number;
};
```

**Named build failures** (zod `superRefine`, message names the file and field):
- `image` without `imageAlt`.
- `ended`, `rating`, or `review` set while `status !== "finished"`.
- `progress` set while `status !== "reading"`.
- `isbn` present but `src/assets/books/<slug>.jpg` missing (run `npm run covers`).
- `language: "my"` present while no Myanmar font is registered in `astro.config.mjs`.
- Unknown scene id passed to `AnimatedScene`.

Draft projects and books with unknown status never render; the build says why.

---

## 9. Assets — where things live

| Asset | Path | Notes |
|---|---|---|
| Animation tree (canonical) | `site/public/assets/animation/` | `ANIMATION_ASSETS.md` inside it is the asset manual. Keep the whole tree: `hero/`, `scenes/`, `legacy/`, `authoring/`, `reference/`, `effects/`, `LICENSE.md`. |
| Retired animation | `site/archive/animation/run-trip-recover-atlas.png` | Authoring reference only, never shipped. |
| Portrait | `site/src/assets/photos/portrait.jpg` | The only photo. |
| Project images | `site/src/assets/projects/` | `pokedesk-hero.png`, `pokedesk-02/03.png`, `echo-hero.webp`, `echo-02/03.webp`; add `lookout-eye.png`, `visionassist-hero.jpg`. |
| Book covers | `site/src/assets/books/<slug>.jpg` | Committed output of `npm run covers`. |
| Fonts | `site/src/assets/fonts/` | `geist-pixel.woff2`, `geist-sans.woff2`, `OFL.txt`; sources in `fonts/source/`. |
| Favicons | `site/public/favicon.{ico,png}`, `favicon-32.png`, `favicon-48.png`, `apple-touch-icon.png` | Built by `site/scripts/build-favicon.py`. |
| Résumé | `site/public/resume.pdf` | Exists. |
| Asset tooling | `site/scripts/*.py`, `strip-clock-overlay.js` | Idempotent; keep. `validate-animation-assets.py` checks the tree. |
| Design source | `docs/Website-Plan.pdf` | The sketch. |

`site/dist/` is build output and is gitignored. It is never a source of anything.

**Art licence:** the mascot art permits the owner's own personal sites and restricts third parties. If this repo goes public, the atlas travels with it. That is intended — be deliberate.

**Security note (historical):** a hackathon photo once showed a `.env` with live API keys. The keys were rotated and the photo dropped. All gallery photos are now removed from the repo; if photos return, check every screen in them first.

---

## 10. Acceptance criteria — verify by running, not by reading CSS

- [ ] No horizontal page scroll at **320, 375, 768, 1280**.
- [ ] Every interactive element has a **visible keyboard focus state**; tab order is sensible; skip link first.
- [ ] Every tap target **≥ 44px**, including covers, chips that are links, slider buttons.
- [ ] `prefers-reduced-motion: reduce` stops: the runner (hidden), the plane, every scene (static frame), the slider scale effect. **Emulate it in Playwright** — the previous session could not and left it unverified.
- [ ] `font-synthesis: none` set; no faked bold anywhere; Geist Pixel only at ELSH 0 or 100.
- [ ] All scenes render `image-rendering: pixelated` at integer scale.
- [ ] Light **and** dark checked on every section; measured contrast holds.
- [ ] **JS disabled:** all five sections render, nav anchors work, slider scrolls, book details open, every contact row is a working link, theme follows system.
- [ ] Both fonts ship as subsetted woff2; **no third-party font, script, or style requests** (check the network panel).
- [ ] Build passes with **0 errors, 0 warnings, 0 hints**.
- [ ] No layout shift on the hero when fonts swap.
- [ ] Runner never covers the top bar or a control at 320/375; never widens the body.
- [ ] Lighthouse: no layout-shift or unoptimised-image flags on the hero.

---

## 11. Build-session checklist

- [x] 0. Delete `site/src/` **except** `src/assets/`. Keep `package.json`, `astro.config.mjs`, `tsconfig.json`, `public/`, `scripts/`, `node_modules/`.
- [x] 1. `tokens.css`, `global.css` (reset, `font-synthesis: none`, focus-visible rule, skip link), `Base.astro` (head, theme bootstrap script, fonts, top bar slot). Register Geist Pixel + Geist Sans locally; remove all Google providers.
- [x] 2. `TopBar.astro` + `ThemeToggle.astro`.
- [x] 3. `AnimatedScene.astro` and `HeroWelcome.astro` per §7.7 (port the fail-open logic).
- [x] 4. `Hero.astro` (§7.1) incl. the ✈ motif.
- [x] 5. `content.config.ts` with all four collections and every named failure in §8. `achievements/icpc.md`.
- [x] 6. `Highlights.astro` (§7.2).
- [x] 7. `ProjectCard.astro` + `ProjectSlider.astro` (§7.3). Rewrite `03-lookout.md` → `02-look-out.md`, add `03-visionassist.md`, renumber Echo to `04`, delete `04-wizlet.md`. Save the two repo images into `src/assets/projects/`.
- [x] 8. `scripts/fetch-covers.mjs` + `npm run covers`; delete `books/zero-to-one.md`, add `books/the-infinity-machine.md`, add `isbn` to `books/dune.md`; `CurrentlyReading.astro`, `Shelf.astro`, `BookDetail.astro`, `ReadingList.astro` (§7.4).
- [x] 9. `ContactCard.astro` (§7.5) + regenerate `contact.vcf.ts`.
- [x] 10. `BottomRunner.astro` (§7.6).
- [x] 11. `index.astro` assembling the five sections in order.
- [x] 12. Accessibility, reduced-motion, no-JS, four-width passes with Playwright (§10). Fix, re-run.
- [ ] 13. Push; connect Cloudflare Pages (root `site`, build `npm run build`, output `dist`); confirm HTTPS.

---

## 12. Open `TODO(owner)` — do not invent values

| Item | Blocks |
|---|---|
| Look-Out dashboard screenshot | The owner decided the eye logo stays (3 Sep 2026); no action |
| VisionAssist team names | Collaborator line |
| Any finished books | Shelves show the empty state until one exists |

Resolved 3 Sep 2026: Infinity Machine progress 30% (chapter 6 of 20); DA Hacks years (3.5 and 4.0, both 2025); Infinity Machine start date (20 Aug 2026); Echo Devpost (`https://devpost.com/software/re3-x6kj0r`, submitted as Re3); Pages connected to GitHub with `site/.node-version` = 22.
Resolved 2 Sep 2026: domain (`mrshine.dev`, bought — §14.4 attach step pending); ICPC year (2025); Echo's link (`https://github.com/aadityad12/Echo`, the original repo — confirmed); Dune ISBN; Infinity Machine ISBN; lead and closing lines both in.

---

## 13. How to update the site after launch

| Want to… | Do |
|---|---|
| Add an achievement | New file in `src/content/achievements/`, push. |
| Add a project | New file in `src/content/projects/` + image in `src/assets/projects/` with `imageAlt`, push. |
| Add a book you are reading | New file in `src/content/books/` with `status: reading`, `started`, `progress`; add `isbn` and run `npm run covers`; push. |
| Update reading progress | Edit `progress`, push. |
| Finish a book | `status: finished`, add `ended`, `rating`, `review`; remove `progress`; push. It moves from Currently Reading to its shelf. |
| Change a contact link | Edit `src/data/site.ts`; the card and the vCard both update. |
| Switch the theme colours | Edit `tokens.css`; re-measure contrast (§5.2) before committing. |

---

## 14. Buying the `.dev` domain and connecting it — step by step

**Status:** 14.1–14.2 done — `mrshine.dev` was registered on 2 Sep 2026. `site.url` is already set. Remaining: 14.3 (Pages project), 14.4 (attach the domain), 14.5 step 3 (verify). Everything happens inside one Cloudflare account, which is the point: registrar, DNS, hosting, and certificates in one place, no DNS hand-off.

### 14.1 Before you start
- A Cloudflare account (free) with **two-factor authentication turned on** — a domain is an identity asset.
- A payment card or PayPal. `.dev` at Cloudflare Registrar is sold **at cost** (registry wholesale plus the ICANN fee), roughly **US$12–13 per year**. Cloudflare adds no markup; the price shown at checkout is the renewal price.

### 14.2 Register the domain (about 5 minutes)
1. Log in at `dash.cloudflare.com`. In the left sidebar open **Domain Registration → Register Domains**.
2. Type the name (e.g. `oaksoekhant`) and search. Pick the `.dev` result; the price shown is per year.
3. Choose **1 year** (you can extend later) and leave **auto-renew on**. Letting a personal domain lapse is how someone else ends up owning your name.
4. Fill the registrant contact details — your real name, email, and address are required by ICANN. **WHOIS redaction is free and on by default**, so none of it is published.
5. Pay. The domain appears under **Domain Registration → Manage Domains** and, because Cloudflare is also the DNS host, a DNS zone is created automatically. Nothing to point anywhere.
6. Two facts about `.dev` to know: it is run by Google Registry, and the whole TLD is **HSTS-preloaded** — browsers refuse plain `http://` for every `.dev` site. Cloudflare issues the certificate automatically, so this costs you nothing, but it means the site can never be served over HTTP by mistake.

### 14.3 Put the site on Cloudflare Pages (first deploy, about 10 minutes)
1. Push the repo to GitHub (it is already `Mr-Shine09/…`; make sure `main` is current).
2. In the Cloudflare sidebar open **Workers & Pages → Create → Pages → Connect to Git**. Authorise the Cloudflare GitHub app for the portfolio repo only.
3. Build settings:

   | Field | Value |
   |---|---|
   | Production branch | `main` |
   | Framework preset | Astro |
   | Root directory | `site` |
   | Build command | `npm run build` |
   | Build output directory | `dist` |
   | Environment variable | `NODE_VERSION` = `22` (Astro 7 needs Node ≥ 22.12; the Pages default may be older) |

4. **Save and Deploy.** The first build takes a minute or two. You get a URL like `oak-portfolio.pages.dev`. Open it on your phone and laptop.
5. Every later `git push` to `main` rebuilds and redeploys. Pull requests get preview URLs.

### 14.4 Attach the domain (about 2 minutes, then a short wait)
1. In the Pages project open **Custom domains → Set up a custom domain**.
2. Enter `mrshine.dev` (your name). Because the zone is already on Cloudflare, it **adds the DNS record for you** — confirm and activate. Repeat for `www.mrshine.dev`.
3. Wait for the status to read **Active** (usually under 10 minutes). Cloudflare provisions the certificate in the same step.
4. Make `www` redirect to the bare domain: in the domain's zone, **Rules → Redirect Rules → Create rule**: when hostname equals `www.mrshine.dev`, redirect 301 to `https://mrshine.dev${uri}`… (the dashboard offers a "Redirect from WWW to Root" template — use it).
5. In the zone's **SSL/TLS** settings confirm mode **Full (strict)** and that **Always Use HTTPS** is on. Both should already be the defaults.

### 14.5 Tell the site its own address (build-session task)
1. `url` in `site/src/data/site.ts` is already `https://mrshine.dev` (set 2 Sep 2026); the rebuilt `site.ts` must keep it.
2. Push. The canonical `<link>`, Open Graph URL, the Website row on the contact card, and `contact.vcf` all update from that one field.
3. Verify: `https://mrshine.dev` loads with a padlock; `http://` is upgraded; `www` redirects; the vCard downloads and opens.

### 14.6 Afterwards
- Set a calendar reminder a month before renewal even with auto-renew on, in case the card expires.
- Keep the domain's **registrar lock** (transfer lock) on — it is on by default.
- Never publish the registrant email anywhere on the site; the contact email is a separate choice.
