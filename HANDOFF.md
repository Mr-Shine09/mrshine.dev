# HANDOFF — Oak's portfolio site

**Written:** 16 August 2026
**For:** a build session starting cold
**Read this first, and read all of it.** This document is self-contained. You do
not need `plan.md`, `ledger.md`, or the five `docs/*.md` specs to start — they
exist for depth, and §12 says which to open when.

> ⚠️ **`plan.md` is out of date.** Its §5 describes a single scrolling page that
> no longer exists. If you read it, ignore §5 and the section order in §6.
> This document supersedes it.

---

## 1. What you are building

A personal portfolio for **Oak Soe Khant** — second-year Computer Engineering
student at De Anza Community College, transferring 2027, originally from Yangon,
now in Santa Clara, California.

The owner's own framing, which governs every judgement call:

> **"A personal time capsule, describing who I am and what I love to do."**

Written for everyone — friends, recruiters, anyone. **It is not a résumé** and
must not read like one. Register: plain, specific, dry, first person.

### Non-negotiables

1. **It must work on a phone and a laptop with no issues.** This is the owner's
   stated top priority. No horizontal page scroll at 320px. Ever.
2. **Never fake a bold.** The site font has no weight axis. Set
   `font-synthesis: none` globally.
3. **Every motion respects `prefers-reduced-motion`.**
4. **Nothing essential lives behind JavaScript.** Every page, every link, and
   every piece of contact information works with scripting off.
5. **No WebGL, no three.js.** Standing exclusion.

---

## 2. Basis — amend, do not rebuild

Work inside the existing **`site/`** Astro project.

### Keep — these are hardened, some by failures found only at runtime

| Keep | Why |
|---|---|
| The Astro project, config, and build pipeline | Builds clean today |
| `Mascot.astro` + the atlas/`atlas-contract.json` sprite system | **Especially this.** The player "fails open": looping sprites animate immediately and `IntersectionObserver` only *pauses* them; only one-shot rows wait to be seen. Gating everything on IO looked tidier and froze every mascot on frame 0 where IO never fires. **Do not "optimise" this into a gate.** |
| `ThemeToggle.astro` + `localStorage` persistence | Works; only its colour values change |
| Content collections + build-time schema validation with named failures | The pattern is good — extend it |
| `contact.vcf` as a build-time static endpoint | A real file, so right-click-save works with no JS |
| `scripts/strip-clock-overlay.js`, `scripts/atlas-source.png` | Idempotent asset tooling |

### Delete

- `src/pages/index.astro` as a single scrolling page
- `Nav.astro` (in-page anchor rail), `SectionNav.astro`, `Hero.astro`
- The three project card weight variants
- `src/content/projects/02-placeholder-standard.md`, `03-placeholder-text.md`,
  `04-placeholder-text.md`
- `src/content/books/current.md` and the entire `books/past/` directory
- `src/content/hobbies/` — hobbies are not in the new architecture
- Both generated stripe placeholder images in `src/assets/projects/`
- Playfair Display and JetBrains Mono from `astro.config.mjs` (see §4)

### Before you touch anything

**This directory is not a git repository.** Run `git init` and commit the
current state first. Files recorded as produced in earlier sessions have already
gone missing once.

---

## 3. Architecture

**Astro. Local content files. Plain CSS with custom properties, no framework.
Minimal JS. Cloudflare Pages, `.dev` domain.**

### Routes

```
/                 Home — masonry grid of four tiles
/about            About
/projects         Projects
/reading          Reading List
/w-phrases        W Phrases
/contact          Contact (fallback for the business card)
/contact.vcf      vCard, build-time endpoint
```

### Home grid

A **masonry grid of four full-bleed image tiles**, each navigating to its page.
Layout reference: `alectear.com/lettering` — **structural pattern only**.

- Tiles: **About · Projects · Reading List · W Phrases**
- **Contact is not a tile.** It is a nav pill.
- Sticky **pill nav**, top-left: `index · about · contact`
- **Every tile carries a real image**, never a label on a coloured rectangle.
  The reference's grid works because its tiles *are* the content. Tile images:

| Tile | Image |
|---|---|
| About | The side-profile portrait, square-cropped |
| Projects | `pokedesk-hero` — two mascots on the purple desktop |
| Reading List | Rendered spines, cropped tight |
| W Phrases | A still of the phrase wall — no motion on the home grid |

### The business card — on every page

A card fixed to the **bottom corner of every page**. Click → **spins, scales up,
travels to centre**, revealing contact details. See §7.6.

---

## 4. Type system

### One family: Geist Pixel

**Source:** `Geist_Pixel copy/GeistPixel-Regular-VariableFont_ELSH.ttf`
**Licence:** SIL OFL 1.1 — self-hosting and web embedding permitted. Ship
`OFL.txt` alongside it.

> This **overturns the previous "no pixel font" rule**, deliberately. The mascot
> is pixel art; a pixel face is more coherent with the signature element than a
> serif ever was.

**Geist Pixel is used for all site text.** The only exception is W Phrases,
which is explicitly the room where type varies (§7.4).

### Critical: the file is 3.6 MB and must not ship as-is

Subset and convert to woff2. Target ≈30–80 KB.

```bash
pyftsubset "GeistPixel-Regular-VariableFont_ELSH.ttf" \
  --output-file="geist-pixel.woff2" --flavor=woff2 \
  --layout-features='*' --unicodes="U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-205E" \
  --name-IDs='*' --notdef-outline
```

Self-host through Astro's font pipeline, exactly as the previous two families
were. **No third-party font requests.** Emit a metric-matched fallback so the
webfont swap does not shift layout.

### There is no bold

The font has **one variable axis, `ELSH` ("Element Shape"), range 0–100**. It is
not a weight axis — it changes the shape of the pixel elements.

> **`ELSH` values between roughly 20 and 80 render hollow and low-contrast.**
> Verified by rendering the font. **Any real text must use `ELSH` 0 or 100.**
> Mid-axis values are decorative only, never for body copy, labels, or links.

### Emphasis — three devices only

| Device | Use |
|---|---|
| **Size step** | Hierarchy — headings, titles |
| **Accent colour** | Emphasis inside running text |
| **Uppercase + letterspacing** | Labels, chips, nav, shelf titles, metadata |

`font-synthesis: none` globally, or browsers will fake a bold and smear the
pixel edges.

### Scale and pixel-grid alignment

Pixel faces look crisp at **integer multiples of their design grid** and muddy
between. Build the scale on **multiples of 4px** and do not use fractional
sizes.

```
--fs-xs   12px    labels, captions, metadata
--fs-sm   14px    secondary text
--fs-base 16px    body — the floor, never smaller for prose
--fs-md   20px
--fs-lg   28px
--fs-xl   40px
--fs-2xl  56px    hero
```

**16px is a hard floor for prose.** Verified legible in rendering; 14px is
acceptable for labels and metadata only.

**The font is monospaced and therefore wide.** The same sentence occupies
noticeably more horizontal space than a proportional face. Check every line
length at 375px — this is the single most likely source of overflow.

### Burmese

Geist Pixel has **zero Myanmar coverage** (verified: 421 glyphs, 0 in
U+1000–109F). Burmese titles on the Reading List will render as tofu boxes and
**the build will still succeed** — this is the one silent failure on the site.

Before any Burmese content ships: self-host **Noto Sans Myanmar** or **Padauk**,
mark Burmese text `lang="my"`, and give it extra line-height for stacked
diacritics.

---

## 5. Theme — "Riso C2"

Two flat inks on a pale ground, print-shop register. Replaces the old
mascot-sampled palette **for the page**; the mascot keeps its own colours (§5.3).

### 5.1 Tokens

```css
:root {
  --bg:      #F0ECFA;   /* pale lilac ground */
  --ink:     #3B1E7A;   /* deep violet — primary text */
  --accent:  #C43A18;   /* coral/rust — second ink */
  --muted:   #6E5F8C;   /* secondary text */
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

| Mode | Token | Ratio vs `--bg` | Result |
|---|---|---|---|
| Light | `--ink` | **10.94** | AA ✅ |
| Light | `--accent` | **4.56** | AA ✅ — *no headroom* |
| Light | `--muted` | **4.92** | AA ✅ |
| Dark | `--ink` | **14.38** | AA ✅ |
| Dark | `--accent` | **7.23** | AA ✅ |
| Dark | `--muted` | **7.28** | AA ✅ |

> **Light `--accent` clears 4.5 by 0.06.** Do not lighten it, and do not darken
> `--bg`. If either changes, re-measure before committing.

### 5.3 The mascot is exempt

The mascot keeps its **own frozen 12-colour palette**. Verified by compositing:
its navy jacket sits comfortably against the violet ink, and its orange accents
read as the second ink. It works as a full-colour object on a duotone page.

**Do not recolour the sprite.** Its atlas is authored against a contract with a
frozen palette, and recolouring breaks that contract.

### 5.4 Toggle

Light and dark with a toggle, `data-theme` on `<html>`, persisted in
`localStorage`. Respect `prefers-color-scheme` on first visit.

---

## 6. Responsive

Mobile-first. Test at **320, 375, 768, 1280**.

**Absolute rule: no horizontal page scroll at any width.** Wide content
(shelves, marquees, code, tables) scrolls inside its own
`overflow-x: auto` container — never the body.

| Component | Phone behaviour |
|---|---|
| **Home grid** | **Two columns, uneven heights** — masonry survives. Not one column: four full-width tiles is a scroll, and seeing the set at once is the point |
| **Business card** | **Compact tab in the corner (≥44px), opens full-screen.** No spin-and-travel — there is no "centre" worth travelling to on a 375px screen |
| **Bookshelf** | **Each shelf scrolls horizontally in its own container.** Needs a visible edge fade so people know there is more, and must be keyboard-scrollable |
| **Project cards** | Single column. Card back must not overflow — if content is too tall, the card grows rather than clipping |
| **W Phrases marquee** | Rows overflow inside their container, never the body |

**Every tap target ≥44px.** Book spines are narrower than that — give each a
transparent hit area that meets the minimum.

---

## 7. Pages

### 7.1 `/about`

Five parts in order, photos interleaved.

1. **Lead** — **use verbatim:**
   > What's up everyone!!! My name is Oak, a Second-year Computer Engineering
   > student at DeAnza Community College, transferring in 2027.

   The three exclamation marks are intentional. **No second paragraph.**

2. **Tagline**, under the lead:
   > Building cool products to boost productivity. Hackathon fanatic. Mindful AI
   > user. Reader in progress.

3. **`Yangon ✈ California` motif** — small corner element, not a section. Place
   names with an arrow, a plane on the arrow. Muted colour, no heading, no
   border. If the plane animates, it freezes under reduced motion.

4. **Four dated galleries** — every photo needs a caption and a date:
   **Yangon** (3) · **De Anza** (5) · **Hackathons** (9, grouped DA Hacks → SCU
   Hack for Humanity → UC Berkeley AI Hackathon, event name + date only, **no
   case studies**) · plus the portrait in the lead.

5. **Closing block — one line, verbatim, set large, no supporting prose:**
   > Leveraging artificial intelligence to sharpen actual intelligence.

**Do not add** the date he moved, his age, or any account of the move. Explicit
decision. The portrait is a **side profile by choice** — do not substitute a
face-forward shot.

> 🔴 **One hackathon photo shows a `.env` file with a live `ANTHROPIC_API_KEY`,
> a `BROWSERBASE_API_KEY`, and a `REDIS_URL` with a password.** Do not publish
> it until it is cropped or dropped. Flag it to the owner if it appears.

### 7.2 `/projects`

**Uniform flip-card deck.** Front: name, image on a colour plate, one-line
summary. Back: stack chips, what was hard, year, collaborators, GitHub, Devpost.

- **Flip on click, never on hover** — hover does not exist on touch
- **No card size grading.** All cards uniform
- **Card front images are matted on a `--plate` field, never cropped**
  (`object-fit: contain`). Forced by the source material: Echo's screenshots are
  tall phone portraits, PokeDesk's are ultra-wide dock strips
- Under reduced motion, swap faces with no rotation
- The back's links are reachable by tab **only when the card is face-up**, or
  you have built a keyboard trap
- **No-JS: the repo link must still be reachable** on the front face

**Ships now:** **PokeDesk** (solo, Swift/SwiftUI/AppKit/Python 3/XcodeGen,
`github.com/Mr-Shine09/PokeDesk`) and **Echo** (Flutter/Dart/Kotlin/Swift/SQLite/
Python 3, `github.com/aadityad12/Echo`).

> **Echo is a three-person Hack for Humanity 2026 project** by **aadityad12,
> shahxsheel, and Mr-Shine09**, in someone else's repository. **Name all three**
> and link to the original repo, not a fork.

**Held as drafts:** Lookout and Wizlet — `draft: true`, filtered out at build
time. **The deck renders as two cards.** That is intended.

### 7.3 `/reading`

A **shelf of rendered spines** — elements, not a photograph.

**Structure:** `English → {Non-fiction, Fiction}` and `Burmese → {Non-fiction,
Fiction}`. **Status is never a shelf** — it is a marker on the spine.
**Empty shelves do not render**, so Burmese is absent today.

Header: shelf title in serifless display size, letterspaced mono-style count
beneath (`2 VOLUMES`), derived from data.

**Spines:** own width, height and colour; colours from the mascot's 12-colour
palette, no two adjacent alike; width from page count where known. A couple of
leaning spines — never overlapping a neighbour's tap target.

**Accessibility:** the rotated title must **not** be the accessible name. Each
spine's accessible name reads normally — *"Dune by Frank Herbert, currently
reading."* Check text contrast against each spine colour individually; some need
light text, some dark.

**Detail panel:** title, author, status, started, ended, progress, rating,
review. **Rating, ended, and review are omitted until a book is finished** — the
panel must look complete without them. Star ratings announce as *"Rated 4 out of
5"*, not five glyphs.

**Search:** client-side, filters title and author across all shelves, announces
its result count in an `aria-live` region. **No-JS: all shelves render, search
box hidden.** Match raw strings — do not normalise in a way that assumes Latin.

**Content:** **Dune** (Frank Herbert, English → Fiction, reading) and **Zero to
One** (Peter Thiel with Blake Masters, English → Non-fiction, reading). Started
dates and progress are `TODO(owner)`.

### 7.4 `/w-phrases`

A dump of collected words and phrases. **Do not explain the name on the page.**

**Marquee rows** — two or three, different speeds, adjacent rows in opposite
directions.

- **Pause on hover and on keyboard focus.** A phrase that cannot be stopped
  cannot be read
- **Reduced motion: no movement at all** — the rows become a static wrapped wall
- The duplicated content that makes the loop seamless must be
  `aria-hidden="true"`, or a screen reader reads the collection twice
- **The static wall is also the no-JS fallback**

**This page is the one exception to the single-font rule.** Type variety is its
subject. Six self-hosted families, validated as a closed set — free-text font
names are rejected so a typo fails the build instead of silently falling back.

> **Revisit the six-font list.** It was chosen when Playfair and JetBrains Mono
> were the site fonts; both are being removed. The set should now be
> **Geist Pixel plus five contrasting families** — a grotesque, a condensed, a
> script, a slab, and one more. Subset and weight-limit every one. **No pixel
> font other than Geist Pixel.**

**Per-phrase style fields** live in the content file — `font`, `size`, `color`,
optional `weight` and `italic`. `size` is a token scale (`sm`/`md`/`lg`/`xl`),
never free pixels.

> 🔴 **`color` accepts palette tokens only, never a raw hex.** This failure is
> silent and theme-dependent: a dark phrase vanishes on the dark background, a
> pale one vanishes in light. Nothing errors — the phrase is simply gone.

**Content:** four phrases (§9 of `docs/w-phrases.md`). One — *"The future is the
set of moments yet to come"* — comes from **Zero to One**, which is on the
Reading List shelf. It carries `bookSlug: zero-to-one` and its source renders as
a **link to that book**. Fail the build if a `bookSlug` matches no book.

### 7.5 `/contact`

**The business card, rendered already open**, reading the **same data file** as
the card so the two can never drift.

Contents: Email, GitHub, LinkedIn, Instagram, Facebook, Devpost, Résumé, vCard.
Presented as a **labelled list, not icon soup**. Blank fields drop rather than
render empty.

**No contact form.** The site is static with no backend; a form means a
third-party service or a function to maintain and a spam problem. Include a
**copy-to-clipboard button beside the email**, never replacing it — the address
stays visible and selectable, and the button announces success via `aria-live`.

**Regenerate `contact.vcf`** — it was built when only name, GitHub and email
existed. It needs the four socials and the Santa Clara location.

`rel="me"` on socials; `rel="noopener"` on anything opening a new tab.

### 7.6 The business card component

| | |
|---|---|
| Placement | Fixed, bottom corner, **every page** |
| Rest state | Closed card. ≥44px |
| Open | Click → spin, scale up, travel to centre |
| Phone | Compact tab → opens **full-screen**, no travel |
| Keyboard | Focusable; Enter/Space opens; Escape closes; visible focus; every revealed link a real `<a>` in tab order |
| Reduced motion | Appears open. No spin, no scale, no flight |
| No-JS | Degrades to a link to `/contact` |

**Contact information must never exist only behind an animation.**

---

## 8. Content data

```ts
type SiteConfig = {
  name: "Oak Soe Khant";
  role: "Second-year Computer Engineering student, De Anza Community College";
  location: "Santa Clara, California";
  socials: {
    email:     "oaksoekhant182209@gmail.com";
    github:    "https://github.com/Mr-Shine09";
    linkedin:  "https://www.linkedin.com/in/oak-soe-khant-350252362";
    instagram: "https://www.instagram.com/oak_soe_khant909";
    facebook:  "https://www.facebook.com/johnwick.wick.37625";
    devpost:   "https://devpost.com/oaksoekhant182209";
  };
  resumeUrl: string;   // TODO(owner) — /resume.pdf does not exist yet
  url: string;         // TODO(owner) — real .dev domain
};

type Project = {
  slug: string; title: string; order: number; year: string;
  stack: string[]; summary: string;
  image?: string; imageAlt?: string;    // imageAlt REQUIRED when image exists
  metric?: string;
  collaborators: string[];              // empty = solo
  builtAt?: string;                     // e.g. "Hack for Humanity 2026"
  links: { github?: string; devpost?: string; live?: string };
  draft: boolean;                       // true = filtered out of the build
};

type Book = {
  slug: string; title: string; author: string;
  language: "en" | "my";
  genre: "nonfiction" | "fiction";
  status: "reading" | "finished" | "want";
  started?: string; ended?: string;
  progress?: number;                    // 0–100, only when status="reading"
  rating?: 1|2|3|4|5;                   // only when status="finished"
  review?: string;                      // only when status="finished"
  pageCount?: number; spineColor?: string;
};

type Phrase = {
  slug: string; text: string;
  source?: string; meaning?: string; dateAdded: string;
  style: {
    font: "geist" | "grotesque" | "condensed" | "hand" | "slab" | "serif";
    size: "sm" | "md" | "lg" | "xl";
    color: PaletteToken;                // tokens only, never raw hex
    weight?: number; italic?: boolean;
  };
  bookSlug?: string;                    // cross-link to a Book
};
```

**Keep the existing pattern of build-time validation with named failures.** Fail
the build, by name, when: `ended`/`rating`/`review` are set on an unfinished
book; `progress` is set on one that is not being read; a `bookSlug` matches no
book; a `font` or `color` value is outside its allowed set; an `image` exists
without `imageAlt`.

---

## 9. Acceptance criteria

- [ ] **No horizontal page scroll at 320px or 375px** on every route
- [ ] Every interactive element has a **visible keyboard focus state**
- [ ] Every tap target **≥44px**, including book spines
- [ ] `prefers-reduced-motion: reduce` stops: the card spin, the project flip,
      the marquee, the plane, and every mascot animation
- [ ] **`font-synthesis: none`** is set and no faked bold appears anywhere
- [ ] All sprite frames render `image-rendering: pixelated` at integer scale
- [ ] Light **and** dark checked on every route; measured contrast holds
- [ ] **JS disabled:** every page renders, every link works, contact details are
      reachable, all shelves and phrases are visible
- [ ] Geist Pixel ships **subsetted as woff2**, not as the 3.6 MB TTF
- [ ] No third-party font, script, or style requests
- [ ] Build passes with 0 errors, 0 warnings, 0 hints
- [ ] No layout shift on the home grid when fonts swap

**Verify these by running them, not by reading the CSS.** The previous session
could not emulate `prefers-reduced-motion` in its environment and had to leave
it unverified — do it properly this time.

---

## 10. Open `TODO(owner)` — do not invent values

| Item | Blocks |
|---|---|
| `resume.pdf` | The Résumé row (drops silently until it exists) |
| Dates + captions for the 19 About photos | The About galleries |
| Started dates and progress for Dune and Zero to One | Book detail panels |
| Real `.dev` domain | Canonical URLs, vCard |
| Lookout and Wizlet content | Nothing — they stay `draft: true` |
| The new Hero mascot (in progress on Codex) | See §11 |

---

## 11. Mascot animation contract — resolved 16 August 2026

The owner has approved six scene animations plus the separate 13-frame Hero V2
welcome animation. The six production scenes are committed under
`site/public/animations/oak-scenes/`; their shared layout, durations, labels,
and frame size live in `scene-contract.json`.

### 11.1 Page mapping

| Animation | Website use |
|---|---|
| Hero V2 `oak-welcome` | Home only. It welcomes the visitor around the masonry grid but never replaces any tile's required real image. The canonical candidate remains in `design-handoff/oak-hero-v2/`. |
| `reading-fire` | `/reading`, beside the shelf introduction. Ambient loop: breathing, blink, fire flicker, and page turn. It pauses when offscreen. |
| `computer-working` | `/projects`, beside the page introduction. This is the calm looping state while the project deck is being browsed. |
| `workbench-zap` | `/projects`, beside the project-folder/deck area. Play once on first reveal: concentrated work → full-body blue skeleton zap → singed recovery. Hold the final singed pose; do not repeatedly zap when the user nudges the scroll position. |
| `thinking-cloud` | `/w-phrases`, beside the introduction to the collected phrases. The blank connected cloud grows, holds, and recedes; do not insert icons or words inside it. |
| `walking` | The low-speed phase of the site-wide scroll traveller. Scrub its gait from scroll progress so feet remain planted. Horizontally flip it when the traveller is moving right-to-left. |
| `run-trip-recover` | The intricate beat in the same site-wide scroll traveller on sufficiently long pages. The mascot runs from the right edge to the left edge, catches a toe, stutter-recovers without falling or becoming dizzy, then runs again. Both travel and frames are driven by smoothed document scroll. |

`/about` receives the scroll traveller beside its dated gallery sequence, but no
additional stationary scene. `/contact` receives no decorative mascot; the
business card is already the page's motion focus.

The previous scrolling-page mapping (`waiting` in the hero, `working` at Built,
`poof` between sections, and `sleeping` at contact) is retired. `poof` still has
no home in the multi-page architecture. Remove those calls when the new routes
are built, but **keep `Mascot.astro`, the legacy atlas, and
`atlas-contract.json`** as required in §2.

### 11.2 Playback rules

- Production pages consume each scene's `*-atlas.png` and JSON timing manifest
  through `AnimatedScene.astro`. The animated WebP and GIF are review/fallback
  artifacts, not the scroll-scrubbing source.
- Loops may begin immediately and `IntersectionObserver` may pause them when
  offscreen. One-shot scenes wait until visible. Preserve the fail-open behavior
  described in §2.
- The global traveller is decorative and uses a fixed overlay plus transforms;
  it must never create layout width or horizontal body scroll. On short pages,
  use only the walking cycle or omit the traveller.
- On phones, prefer an inline/clipped traveller treatment instead of letting a
  fixed mascot cover content or controls. Verify at 320px and 375px.
- Under `prefers-reduced-motion: reduce`, freeze stationary scenes on a clear
  representative frame and hide the site-wide traveller. No essential content
  or navigation may depend on any animation.
- Keep `image-rendering: pixelated`, integer display scales, the mascot's frozen
  palette, and the authored three-quarter facial angles. Do not recolour the
  scenes to the page theme.
- Source boards, frame PNGs, prompts, contact sheets, and GIFs are retained for
  authoring and QA. A production optimization pass may move those files outside
  `public/`; page code should request only atlases and manifests.

Also open: whether the old "Ahead" / past-present-future section is dropped. It
has no slot in a four-tile grid and W Phrases took its place.

---

## 12. Where to go deeper

| Question | File |
|---|---|
| Why a decision is the way it is | `ledger.md` — 40 numbered decisions with reasoning |
| Full About copy, photo manifest, exclusions | `docs/about-me.md` |
| Project card details, both writeups | `docs/projects.md` |
| Shelf mechanics, Burmese requirements | `docs/reading-list.md` |
| Phrase styling, the six-font set | `docs/w-phrases.md` |
| Contact page and card | `docs/contact.md` |
| **Anything about page structure** | **Not `plan.md` §5 — it is superseded** |

---

## 13. Housekeeping

- `.fonttest/` was a scratch directory from the type and theme exploration. It
  is no longer present.
- `Geist_Pixel copy/` holds the source TTF, `OFL.txt`, and `README.txt`. Move
  the licence into the site with the font.
- Cleanup completed 16 August 2026: `art copy.zip`, `art-extract/`, the two
  loose root mascot reference PNGs, and both generated project stripe
  placeholders were removed from the project. They were moved to
  `~/.Trash/oak-portfolio-old-assets-2026-08-16/` and remain recoverable until
  Trash is emptied. Canonical animation art now lives in
  `site/public/animations/oak-scenes/` and `design-handoff/oak-hero-v2/`.
- The art licence permits the owner's own personal sites and restricts third
  parties. If this repo goes public, the sprite atlas travels with it. That is
  intended — but be deliberate about it.
