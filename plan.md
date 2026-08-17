# Portfolio site — build plan

**Written:** 15 Aug 2026
**Status:** ready for Claude Code. Sections marked `TODO(owner)` need real
content before that step can finish — everything else is buildable as-is.
**Layout reference:** afig.dev — structural pattern only (sticky nav, hero
minimalism, weighted project cards, split "personal" section, footer contact
card). Palette, type, and mascot are unrelated to that reference and stay as
locked below.

---

## 1. Stack

| | |
|---|---|
| Framework | Astro |
| Content | Local files (`.md` / `.json`) — Keystatic added later, not now |
| Styling | Plain CSS with custom properties, no framework |
| Hosting | Cloudflare Pages |
| Domain | Cloudflare registrar, `.dev` (HSTS-preloaded → HTTPS mandatory) |
| JS | Minimal — Astro ships none by default; only the mascot frame-cycler and the theme toggle need real script |

---

## 2. File tree

```
site/
├── astro.config.mjs
├── package.json
├── public/
│   ├── favicon.svg
│   ├── sprites/
│   │   ├── atlas.png                  # existing mascot sprite atlas
│   │   ├── manifest.json              # existing frame manifest
│   │   └── LICENSE.md                 # update: remove "no other website" clause
│   └── resume.pdf                     # TODO(owner)
├── src/
│   ├── content/
│   │   ├── config.ts                  # content collection schemas (section 3)
│   │   ├── projects/
│   │   │   ├── 01-<slug>.md           # TODO(owner): real projects, 4–6 entries
│   │   │   └── ...
│   │   ├── books/
│   │   │   ├── current.md             # TODO(owner)
│   │   │   └── past/
│   │   │       └── <slug>.md          # TODO(owner)
│   │   └── hobbies/
│   │       └── <slug>.md              # TODO(owner)
│   ├── data/
│   │   └── site.ts                    # name, tagline, location, socials — TODO(owner)
│   ├── components/
│   │   ├── Nav.astro
│   │   ├── Hero.astro
│   │   ├── Mascot.astro               # frame-cycler, respects prefers-reduced-motion
│   │   ├── ThemeToggle.astro
│   │   ├── ProjectCard.astro          # weighted variant: featured | standard | text-only
│   │   ├── BookCard.astro
│   │   ├── HobbyCard.astro
│   │   ├── SectionNav.astro           # in-page anchor rail, sticky
│   │   └── ContactCard.astro          # footer: vCard download, copy-link, socials list
│   ├── layouts/
│   │   └── Base.astro                 # theme class on <html>, meta tags, font loading
│   ├── pages/
│   │   └── index.astro                # the single scrolling page
│   └── styles/
│       ├── tokens.css                 # palette + type + spacing custom properties
│       └── global.css
└── scripts/
    └── strip-clock-overlay.js         # one-time: pre-process `waiting` frames if not already clean
```

---

## 3. Content schemas

```ts
// src/content/config.ts

type Project = {
  slug: string;
  title: string;
  weight: "featured" | "standard" | "text-only"; // controls card size/treatment
  stack: string[];              // e.g. ["TypeScript", "Astro"]
  summary: string;              // 1 sentence, appears on the card
  body: string;                 // markdown, longer writeup — leads with what was hard, not what was used
  image?: string;                // required if weight !== "text-only"
  links: { github?: string; live?: string };
  metric?: string;              // optional standout stat, e.g. "2nd place, hackathon 2026"
};

type Book = {
  slug: string;
  title: string;
  author: string;
  status: "current" | "past";
  progress: number;             // 0–100
  oneLiner: string;             // what it's about, one line
  whyReading?: string;          // the "why now" line — locked decision from grill-me session
  cover?: string;
};

type Hobby = {
  slug: string;
  title: string;
  blurb: string;
  spriteState: "walk-right" | "hand-sign" | string; // maps to manifest.json state key
};

type SiteConfig = {
  name: string;                 // TODO(owner)
  role: string;                 // e.g. "Computer Engineering @ [school]" — TODO(owner)
  location: string;             // TODO(owner)
  tagline: string;               // one line, personal register — TODO(owner)
  socials: { github?: string; linkedin?: string; email?: string }; // TODO(owner)
  resumeUrl: string;             // TODO(owner): /resume.pdf once uploaded
};
```

---

## 4. Design tokens

```css
/* src/styles/tokens.css */
:root {
  /* light (default) */
  --ink: #111219;
  --paper: #F6F3E4;
  --grey-1: #B5B6B8; --grey-2: #7E8085; --grey-3: #3E3D43; --grey-4: #25252B;
  --navy-1: #122F68; --navy-2: #0D234E; --navy-3: #1B428B;
  --amber-1: #FFBE4B; --amber-2: #E18B30; --rust: #A75221;
  --accent: var(--rust);
  --bg: var(--paper);
  --fg: var(--ink);
}

[data-theme="dark"] {
  --bg: var(--ink);
  --fg: var(--paper);
  --accent: var(--amber-1); /* rust disappears on dark — do not use rust as dark accent */
}

/* type */
--font-display: /* high-contrast serif, TBD family */;
--font-body: /* monospace, TBD family */;
/* no pixel font, anywhere — locked decision #10 */
```

Sprite frames render with `image-rendering: pixelated;` — acceptance criterion, not optional.

---

## 5. Section-by-section spec

### Nav (sticky)
Anchors: About · Built · Current · Ahead · Contact. Mirrors section order exactly, afig.dev pattern. Collapses to a compact bar on scroll.

### Hero — `#about`
- Name, role, location chip, one-line tagline (minimal, not a paragraph)
- Buttons: GitHub, Resume, Get in touch
- Mascot `waiting` state beside/below text, wave loop `0→1→2→3→2→1` @ 190ms, clock overlay stripped
- `prefers-reduced-motion`: freeze on frame 0

### Built — `#built` (Projects)
- Weighted cards per schema: 1 `featured` (big image, writeup with a real number in it), 1–2 `standard` (smaller image, shorter copy), rest `text-only`
- Mascot `working` state as a small recurring motif at section top, not per-card
- `poof` transition (8-frame) between this section and the next — locked mapping

### Current — `#current` (Reading + hobbies)
- Split internal layout, afig.dev pattern: currently-reading gets a featured card (cover, progress, "why now" line); past reads as a smaller grid
- Reading pose gap: use existing pose as placeholder until new frame/prop is ready — do not block the section on this
- Hobbies as a lighter strip below, `walk-right` / `hand-sign` states

### Ahead — `#ahead`
- Aspirations framing (owner's own "three episodes of time" language) — shortest section, no card grid needed, prose + maybe one sprite gesture

### Footer / Contact — `#contact`
- ContactCard: vCard download, copy-link, socials list (not icon soup)
- `sleeping`/`offline` sprite state — page "goes to sleep" here, locked mapping

---

## 6. Task checklist

- [x] Scaffold Astro project, install, confirm dev server runs
- [x] Add `tokens.css`, confirm light/dark toggle switches `data-theme` and persists via `localStorage` (fine here — this is a real deployed site, not a claude.ai artifact)
- [x] Build `Mascot.astro`: frame-cycler component, accepts `state` prop, reads `atlas-contract.json`, respects `prefers-reduced-motion`
- [x] Strip clock overlay from `waiting` frames if not already clean (`scripts/strip-clock-overlay.js`)
- [x] Build `Nav.astro` + sticky anchor behavior
- [x] Build `Hero.astro`
- [x] Build `ProjectCard.astro` with three weight variants; wire to `content/projects/`
- [x] Build `BookCard.astro` (current vs past variants); wire to `content/books/`
- [x] Build `HobbyCard.astro`; wire to `content/hobbies/`
- [x] Build `ContactCard.astro` incl. vCard generation
- [x] Assemble `index.astro` with all sections in Built → Current → Ahead order
- [x] Verify sprite `image-rendering: pixelated` on all mascot instances
- [x] Mobile pass: single-column, tap targets ≥44px, nav collapses sensibly
- [x] Keyboard pass: visible focus states on every interactive element
- [x] `prefers-reduced-motion` pass: wave and any transition freeze correctly
- [x] Update `art/LICENSE.md` — remove the "not for another website" clause
- [ ] Fill real content: `site.ts`, projects, books, hobbies, `resume.pdf` — `TODO(owner)` items above
- [ ] Deploy to Cloudflare Pages, connect `.dev` domain via Cloudflare registrar
- [ ] Confirm HTTPS (should be automatic — `.dev` is HSTS-preloaded)

---

## 7. Acceptance criteria (quality floor)

- Responsive down to a small phone width, no horizontal scroll
- Every interactive element has a visible keyboard focus state
- `prefers-reduced-motion: reduce` stops the wave and any sprite transition
- All sprite frames render with `image-rendering: pixelated`
- Light/dark toggle: dark mode uses `--amber-1` as accent, never rust
- No pixel font anywhere, no WebGL/three.js anywhere — both are locked exclusions
- Lighthouse: no obvious layout-shift or unoptimized-image flags on the hero

---

## 7a. Build notes — where the build differs from this plan

Recorded 15 Aug 2026, at the end of the first build session.

| Planned | Built | Why |
|---|---|---|
| Mascot reads `manifest.json` | Reads `atlas-contract.json` | `manifest.json` is only a SHA-256 map of frame files. The contract JSON is the actual machine-readable source of truth: grid geometry, row order, per-frame durations, playback mode. |
| Sprite frames as individual PNGs | Single atlas via `background-position` | One 111 KB request instead of ~88. Cell maths comes straight from the contract. |
| Type families "TBD" | Playfair Display (display) + JetBrains Mono (body) | Both self-hosted at build time through Astro's font pipeline — no third-party request, and metric-matched fallbacks are emitted so the webfont swap does not shift layout. Swapping either family is a one-line change in `astro.config.mjs`. |
| One `projects` grid | Three bands: featured, then a 2-col grid of `standard`, then a full-width `text-only` index | Mixing a tall image card and a two-line text card in one grid row stranded the short card in white space. |
| — | `contact.vcf` is a build-time static endpoint | A real file, so the download link survives no-JS and right-click-save. Generating a Blob in the browser would not. |

Verified in-browser, not just by build success: 8 sprite instances all
`image-rendering: pixelated` and all at integer scale; no horizontal overflow at
320 px or 375 px; all 17 interactive elements matched by the focus-visible rule
with the skip link first in tab order; every tap target ≥ 44 px; the hero wave
observed cycling `0→1→2→3→2→1`. Reduced motion was verified by inspection of the
CSS rule and the player's guard — this environment could not emulate the media
query, so it is worth one manual check on a real machine.

Output: no external JS files at all — 5 inlined scripts totalling 3.5 KB.

---

## 8. Still needed before full content pass

- Name, school/role line, location, tagline, socials, resume PDF
- Final project list (4–6) with which 2–3 get images
- Real book data (current + past) and the "why reading this" lines
- Hobby list and which sprite state fits each
