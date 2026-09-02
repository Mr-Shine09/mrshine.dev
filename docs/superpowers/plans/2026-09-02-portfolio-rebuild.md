# Portfolio Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `site/src` from scratch as a single scrolling page (About · Highlights · Projects · Personal · Contact) per `Plan.md`, verified by a Playwright acceptance harness, ready to deploy to Cloudflare Pages at `https://mrshine.dev`.

**Architecture:** Astro static site, one route `/`. Content in markdown collections validated by zod with named failures. Plain CSS with Riso C2 tokens; Geist Pixel for headings/labels and Geist Sans for prose, both self-hosted. Native APNG mascot scenes swapped to static frames when offscreen or under reduced motion. Every interactive feature is progressive enhancement over working HTML.

**Tech Stack:** Astro ^7.2.2, Node ≥ 22.12, zod ^4, Playwright 1.62.1 (verification only), `pyftsubset` (fontTools) for font subsetting. No UI framework, no CSS framework, no third-party runtime requests.

**Spec:** `Plan.md` (repo root). Section numbers below (§) refer to it.

## Global Constraints

- **No horizontal body scroll at 320px, ever.** Wide content scrolls inside its own `overflow-x: auto` container. (§2.1)
- **`font-synthesis: none` globally.** Geist Pixel has no weight axis; never fake a bold. (§2.2)
- **Every motion respects `prefers-reduced-motion: reduce`.** Scenes freeze on static frame, runner hidden, plane stops, slider scale effect removed. (§2.3)
- **Nothing essential behind JavaScript.** Every section, link, and contact detail works with scripting off. (§2.4)
- **No WebGL, no three.js.** (§2.5)
- **Mascot player fails open:** loops animate immediately; `IntersectionObserver` only pauses. Never gate on IO. (§2.6)
- **Mascot palette is frozen.** Never recolour scenes. `image-rendering: pixelated`, integer scales only. (§2.7)
- **Every tap target ≥ 44px. Every interactive element has a visible focus state.** (§2.8, §2.9)
- **Geist Pixel:** headings, nav, labels, chips, counts. **Geist Sans:** all prose. Sizes on the 4px scale `12/14/16/20/28/40/56`. **16px floor for prose.** (§4)
- **Riso C2 tokens verbatim** (§5.1). Light `--accent` #C43A18 and light `--bg` #F0ECFA must not change.
- **Copy is verbatim** where §7 quotes it: lead line, tagline, closing line, project summaries.
- **Do not invent** any `TODO(owner)` value (§12). Omit the field; never fill it.
- **Register in commit messages and comments:** plain, specific. Every commit ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- **Working directory for all commands is `site/`** unless a step says otherwise. Run git from the repo root.

---

## File structure

**Kept from the old tree (do not rewrite unless a task says so):**
- `site/astro.config.mjs` — rewritten in Task 1 (two local fonts)
- `site/package.json`, `tsconfig.json`, `node_modules/`, `public/**`, `scripts/*.py`, `scripts/strip-clock-overlay.js`
- `site/src/assets/**` — fonts, `photos/portrait.jpg`, `projects/*`
- `site/src/content/projects/01-pokedesk.md`, `02-echo.md` (renamed in Task 8), `books/dune.md` (edited in Task 9)
- `site/src/data/site.ts` — rewritten in Task 2 (same facts, new fields)
- `site/src/pages/contact.vcf.ts` — kept verbatim
- `site/src/components/ThemeToggle.astro`, `AnimatedScene.astro`, `HeroWelcome.astro` — kept, small edits noted
- `site/src/styles/tokens.css` — kept, edited in Task 1

**Deleted in Task 0:** `src/pages/{index,about,projects,reading,contact}.astro`, `src/components/{BusinessCard,NavPill,BookSpine,ProjectCard,ScrollTripMascot,Mascot}.astro`, `src/data/mascot.ts`, `src/content/books/zero-to-one.md`.

**Created:**

| File | Responsibility |
|---|---|
| `scripts/subset-fonts.sh` | Reproducible `pyftsubset` recipe for both faces |
| `scripts/fetch-covers.mjs` | Download Open Library covers by ISBN into `src/assets/books/` |
| `tests/verify.mjs` | Playwright acceptance harness; one named check per requirement |
| `src/data/nav.ts` | The five sections: id + label, single source for TopBar and `index.astro` |
| `src/styles/global.css` | Reset, fonts, focus, layout primitives (rewritten) |
| `src/layouts/Base.astro` | `<head>`, theme bootstrap, skip link, TopBar, slot, BottomRunner |
| `src/components/TopBar.astro` | Sticky bar: favicon, five anchors, active-section highlight, ThemeToggle |
| `src/components/SectionHead.astro` | Heading + optional label used by every section |
| `src/components/PlaneMotif.astro` | `Yangon ✈ Bay Area, CA` |
| `src/components/Hero.astro` | §7.1 |
| `src/components/Highlights.astro` | §7.2 |
| `src/components/ProjectCard.astro`, `ProjectSlider.astro`, `Projects.astro` | §7.3 |
| `src/components/ProgressRing.astro`, `CurrentlyReading.astro`, `Shelf.astro`, `BookDetail.astro`, `ReadingList.astro` | §7.4 |
| `src/components/ContactCard.astro` | §7.5 |
| `src/components/BottomRunner.astro` | §7.6 |
| `src/pages/index.astro` | Assembles the five sections |
| `src/content.config.ts` | achievements, projects, books collections (rewritten) |
| `src/content/achievements/icpc-pacnw-2025.md` | The one highlight |
| `src/content/projects/02-look-out.md`, `03-visionassist.md`, `04-echo.md` | Project entries |
| `src/content/books/the-infinity-machine.md` | Second current book |
| `src/assets/projects/lookout-eye.png`, `visionassist-hero.jpg` | Card images |
| `src/assets/books/dune.jpg`, `the-infinity-machine.jpg` | Covers |
| `src/assets/fonts/geist-sans.woff2`, `geist-sans-medium.woff2` | Body face |

---

## Verification harness — how every task tests itself

`tests/verify.mjs` runs Playwright against a preview server and executes named checks. Tasks add checks; each task's "failing test" step is running its new check before the implementation exists.

Start the preview once per session and leave it running:

```bash
cd site && npm run build && (npm run preview -- --port 4321 > /tmp/preview.log 2>&1 &) && sleep 2 && curl -s -o /dev/null -w '%{http_code}\n' http://localhost:4321/
```
Expected: `200`. After every build, the preview serves the new `dist/` (Astro preview reads from disk) — rebuild, then re-run checks.

Run checks: `node tests/verify.mjs` (all) or `node tests/verify.mjs sections overflow` (named).

---

### Task 0: Clear the old source tree and add Playwright

**Files:**
- Delete: `site/src/pages/index.astro`, `about.astro`, `projects.astro`, `reading.astro`, `contact.astro`
- Delete: `site/src/components/BusinessCard.astro`, `NavPill.astro`, `BookSpine.astro`, `ProjectCard.astro`, `ScrollTripMascot.astro`, `Mascot.astro`
- Delete: `site/src/data/mascot.ts`, `site/src/content/books/zero-to-one.md`
- Modify: `site/package.json`

**Interfaces:**
- Produces: a tree with no pages, `playwright` as a devDependency, scripts `check`, `verify`, `covers` declared (scripts' targets are created in later tasks).

- [ ] **Step 1: Delete the superseded files**

From the repo root:
```bash
cd "site" && git rm -q src/pages/index.astro src/pages/about.astro src/pages/projects.astro src/pages/reading.astro src/pages/contact.astro \
  src/components/BusinessCard.astro src/components/NavPill.astro src/components/BookSpine.astro src/components/ProjectCard.astro \
  src/components/ScrollTripMascot.astro src/components/Mascot.astro src/data/mascot.ts src/content/books/zero-to-one.md
ls src/pages src/components src/data src/content/books
```
Expected: `src/pages` has only `contact.vcf.ts`; `src/components` has `AnimatedScene.astro HeroWelcome.astro ThemeToggle.astro`; `src/data` has `site.ts`; `books` has `dune.md`.

- [ ] **Step 2: Add Playwright and the scripts**

Replace the `scripts` and `devDependencies` blocks in `site/package.json`:
```json
{
  "name": "site",
  "type": "module",
  "version": "0.0.1",
  "engines": { "node": ">=22.12.0" },
  "scripts": {
    "dev": "astro dev --port ${PORT:-4321}",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro",
    "check": "astro check",
    "covers": "node scripts/fetch-covers.mjs",
    "verify": "node tests/verify.mjs"
  },
  "dependencies": { "astro": "^7.2.2" },
  "devDependencies": {
    "@astrojs/check": "^0.9.10",
    "playwright": "1.62.1",
    "pngjs": "^7.0.0",
    "typescript": "^6.0.3",
    "zod": "^4.4.3"
  }
}
```
Run: `npm install`
Expected: completes; `ls node_modules/playwright/package.json` exists. Browsers are already cached at `~/Library/Caches/ms-playwright/chromium-1234`; if `node -e "require('playwright').chromium.executablePath()"` errors, run `npx playwright install chromium`.

- [ ] **Step 3: Confirm the build currently fails for the right reason**

Run: `npm run build 2>&1 | tail -5`
Expected: build succeeds with **no pages** except `/contact.vcf`, and a `[WARN]` about the phrases collection directory. That warning disappears in Task 2 when `content.config.ts` is rewritten. Do not fix it here.

- [ ] **Step 4: Commit**

```bash
cd .. && git add -A site && git commit -m "rebuild: clear old pages and components; add Playwright + scripts

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 1: Fonts, tokens, config

**Files:**
- Create: `site/scripts/subset-fonts.sh`
- Create: `site/src/assets/fonts/geist-sans.woff2`, `site/src/assets/fonts/geist-sans-medium.woff2`
- Modify: `site/astro.config.mjs` (rewrite)
- Modify: `site/src/styles/tokens.css:52-57` (type comment) — add `--font-*` aliases
- Test: `npm run build` + font file sizes

**Interfaces:**
- Produces: CSS variables `--font-pixel` (Geist Pixel) and `--font-sans` (Geist Sans, weights 400 and 500) emitted by Astro's font pipeline, consumed via `<Font cssVariable="…" />` in Task 2.

- [ ] **Step 1: Write the subset script**

`site/scripts/subset-fonts.sh`:
```bash
#!/usr/bin/env bash
# Subset both site faces to Latin and emit woff2 (Plan.md §4.1).
# Requires fontTools: `brew install fonttools` or `pip install fonttools brotli`.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=src/assets/fonts/source
OUT=src/assets/fonts
UNI="U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-205E,U+2708"   # U+2708 = ✈ for the motif

subset() { # $1 in.ttf  $2 out.woff2
  pyftsubset "$1" --output-file="$2" --flavor=woff2 --layout-features='*' \
    --unicodes="$UNI" --name-IDs='*' --notdef-outline
  printf '%s  %s bytes\n' "$2" "$(stat -f%z "$2")"
}

mkdir -p "$SRC/geist-sans"
for w in Regular Medium; do
  f="$SRC/geist-sans/Geist-$w.ttf"
  [ -f "$f" ] || curl -sSL -o "$f" \
    "https://raw.githubusercontent.com/vercel/geist-font/main/packages/next/dist/fonts/geist-sans/Geist-$w.ttf"
done
[ -f "$SRC/geist-sans/OFL.txt" ] || curl -sSL -o "$SRC/geist-sans/OFL.txt" \
  "https://raw.githubusercontent.com/vercel/geist-font/main/LICENSE.TXT"

subset "$SRC/geist-pixel/GeistPixel-Regular-VariableFont_ELSH.ttf" "$OUT/geist-pixel.woff2"
subset "$SRC/geist-sans/Geist-Regular.ttf" "$OUT/geist-sans.woff2"
subset "$SRC/geist-sans/Geist-Medium.ttf"  "$OUT/geist-sans-medium.woff2"
```

- [ ] **Step 2: Run it and check sizes**

Run: `chmod +x scripts/subset-fonts.sh && ./scripts/subset-fonts.sh`
Expected: three lines, each between 15 000 and 90 000 bytes. If `pyftsubset` says `brotli` missing: `pip3 install brotli`.

- [ ] **Step 3: Rewrite `astro.config.mjs`**

```js
// @ts-check
import { defineConfig, fontProviders } from "astro/config";

// Two self-hosted faces (Plan.md §4): Geist Pixel for headings, nav, labels and
// chips; Geist Sans for prose. Both are subset by scripts/subset-fonts.sh. No
// third-party font requests exist anywhere on the site.
export default defineConfig({
  site: "https://mrshine.dev",
  fonts: [
    {
      provider: fontProviders.local(),
      name: "Geist Pixel",
      cssVariable: "--font-pixel",
      // Single ELSH axis 0–100. Default instance ELSH 0 = solid pixels.
      // 20–80 renders hollow: never for real text.
      options: {
        variants: [{ weight: 400, style: "normal", src: ["./src/assets/fonts/geist-pixel.woff2"] }],
      },
      fallbacks: ["ui-monospace", "Menlo", "monospace"],
    },
    {
      provider: fontProviders.local(),
      name: "Geist Sans",
      cssVariable: "--font-sans",
      options: {
        variants: [
          { weight: 400, style: "normal", src: ["./src/assets/fonts/geist-sans.woff2"] },
          { weight: 500, style: "normal", src: ["./src/assets/fonts/geist-sans-medium.woff2"] },
        ],
      },
      fallbacks: ["system-ui", "-apple-system", "Segoe UI", "Helvetica Neue", "sans-serif"],
    },
  ],
});
```

- [ ] **Step 4: Update the type comment and add the pixel-face size aliases in `tokens.css`**

Replace the block starting `/*\n   * ---- type ----` through `--fs-2xl: 56px;` with:
```css
  /*
   * ---- type ----
   * Two faces from the Astro font pipeline: --font-pixel (Geist Pixel) for
   * headings, nav, labels, chips, counts; --font-sans (Geist Sans) for prose.
   * The pixel face is crisp at integer multiples of its grid: sizes are
   * multiples of 4px, no fractional sizes, no clamp(). 16px is a hard floor
   * for prose; 12–14px are labels/metadata only (Plan.md §4.2).
   */
  --fs-xs: 12px;
  --fs-sm: 14px;
  --fs-base: 16px;
  --fs-md: 20px;
  --fs-lg: 28px;
  --fs-xl: 40px;
  --fs-2xl: 56px;
```
Also delete the `--px-*` block comment sentence "The --px-* set colours book spines on /reading only — never page chrome." and replace with "The --px-* set is kept for any future element that must match the mascot; page chrome never uses it." (Spines are gone; §7.4 uses cover images.)

- [ ] **Step 5: Build**

Run: `npm run build 2>&1 | grep -E "fonts|error|Complete"`
Expected: `[assets] Copying fonts (3 files)...` (or similar count) and `Complete!`. No `error`.

- [ ] **Step 6: Commit**

```bash
cd .. && git add site/scripts/subset-fonts.sh site/src/assets/fonts site/astro.config.mjs site/src/styles/tokens.css && git commit -m "fonts: Geist Sans body face, subset script, two local font providers

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Global CSS, Base layout, TopBar, page skeleton, verify harness

**Files:**
- Create: `site/src/data/nav.ts`
- Modify: `site/src/data/site.ts` (rewrite)
- Modify: `site/src/styles/global.css` (rewrite)
- Create: `site/src/layouts/Base.astro` (rewrite over the old one)
- Create: `site/src/components/TopBar.astro`, `SectionHead.astro`
- Modify: `site/src/components/ThemeToggle.astro` — no change needed; verify it exists
- Create: `site/src/pages/index.astro` (skeleton with five empty sections)
- Modify: `site/src/content.config.ts` (rewrite: projects + books only for now; achievements in Task 6)
- Create: `site/tests/verify.mjs`

**Interfaces:**
- Produces: `sections` array from `nav.ts`: `{ id: "about"|"highlights"|"projects"|"personal"|"contact", label: string }[]`. `site` object from `site.ts` (shape in §8). `Base.astro` props `{ title?: string; description?: string }` with a default slot. `SectionHead.astro` props `{ id: string; title: string; label?: string; emoji?: string }` rendering `<h2 id="{id}-title">`. CSS classes `.wrap`, `.label`, `.btn`, `.chip`, `.sr-only`, `.section`.

- [ ] **Step 1: Write the harness with the first two checks**

`site/tests/verify.mjs`:
```js
// Playwright acceptance harness (Plan.md §10). Usage:
//   node tests/verify.mjs            # all checks
//   node tests/verify.mjs a b        # named checks
// Expects `npm run preview -- --port 4321` running against a fresh build.
import { chromium } from "playwright";

const BASE = process.env.PREVIEW_URL ?? "http://localhost:4321/";
const WIDTHS = [320, 375, 768, 1280];
const SECTIONS = ["about", "highlights", "projects", "personal", "contact"];

const checks = {};
const results = [];
function check(name, fn) { checks[name] = fn; }
function assert(cond, msg) { if (!cond) throw new Error(msg); }

async function page(browser, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, ...opts });
  const p = await ctx.newPage();
  await p.goto(BASE, { waitUntil: "networkidle" });
  return { ctx, p };
}

check("sections", async (browser) => {
  const { ctx, p } = await page(browser);
  for (const id of SECTIONS) {
    assert(await p.locator(`section#${id}`).count() === 1, `missing <section id="${id}">`);
    assert(await p.locator(`nav a[href="#${id}"]`).count() === 1, `nav lacks link to #${id}`);
  }
  const order = await p.$$eval("main > section", (els) => els.map((e) => e.id));
  assert(order.join() === SECTIONS.join(), `section order is ${order.join(" · ")}`);
  await ctx.close();
});

check("overflow", async (browser) => {
  for (const width of WIDTHS) {
    const { ctx, p } = await page(browser, { viewport: { width, height: 800 } });
    const { sw, iw } = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth }));
    assert(sw <= iw, `horizontal overflow at ${width}px: scrollWidth ${sw} > innerWidth ${iw}`);
    await ctx.close();
  }
});

// ---- runner ----
const only = process.argv.slice(2);
const names = only.length ? only : Object.keys(checks);
const browser = await chromium.launch();
for (const name of names) {
  if (!checks[name]) { results.push([name, "UNKNOWN"]); continue; }
  try { await checks[name](browser); results.push([name, "PASS"]); }
  catch (e) { results.push([name, `FAIL — ${e.message}`]); }
}
await browser.close();
for (const [n, r] of results) console.log(`${r.startsWith("PASS") ? "✓" : "✗"} ${n}: ${r}`);
process.exit(results.some(([, r]) => !r.startsWith("PASS")) ? 1 : 0);
```

- [ ] **Step 2: Run the harness to see it fail**

Run: `npm run build && (npm run preview -- --port 4321 > /tmp/preview.log 2>&1 &) && sleep 2 && node tests/verify.mjs sections overflow`
Expected: `✗ sections: FAIL — missing <section id="about">` (there is no index page). `overflow` may PASS or fail on a 404 page; irrelevant yet.

- [ ] **Step 3: Write `nav.ts` and `site.ts`**

`site/src/data/nav.ts`:
```ts
/** The five sections, in page order. TopBar and index.astro both read this. */
export const sections = [
  { id: "about", label: "About" },
  { id: "highlights", label: "Highlights" },
  { id: "projects", label: "Projects" },
  { id: "personal", label: "Personal" },
  { id: "contact", label: "Contact" },
] as const;
export type SectionId = (typeof sections)[number]["id"];
```

`site/src/data/site.ts`:
```ts
/**
 * Site-wide facts (Plan.md §8). The hero, the contact card, and contact.vcf
 * all read this file so they can never drift. Do not invent TODO(owner) values.
 */
export type SiteConfig = {
  name: string;
  role: string;
  shortRole: string;
  location: string;
  origin: string;
  destination: string;
  lead: string;
  tagline: string;
  closing: string;
  socials: {
    email: string;
    github: string;
    linkedin: string;
    instagram: string;
    facebook: string;
    devpost: string;
  };
  resumeUrl: string;
  url: string;
  seo: { description: string };
};

export const site: SiteConfig = {
  name: "Oak Soe Khant",
  role: "Second-year Computer Engineering student, De Anza Community College",
  shortRole: "Computer Engineering @ De Anza",
  location: "Santa Clara, California",
  origin: "Yangon",
  destination: "Bay Area, CA",
  // Verbatim, owner's own words. Three exclamation marks are intentional.
  lead:
    "What's up everyone!!! My name is Oak, a Second-year Computer Engineering student at DeAnza Community College, transferring in 2027.",
  tagline:
    "Building cool products to boost productivity. Hackathon fanatic. Mindful AI user. Reader in progress.",
  closing: "Leveraging artificial intelligence to sharpen actual intelligence.",
  socials: {
    email: "oaksoekhant182209@gmail.com",
    github: "https://github.com/Mr-Shine09",
    linkedin: "https://www.linkedin.com/in/oak-soe-khant-350252362",
    instagram: "https://www.instagram.com/oak_soe_khant909", // vCard only
    facebook: "https://www.facebook.com/johnwick.wick.37625", // vCard only
    devpost: "https://devpost.com/oaksoekhant182209", // vCard only
  },
  resumeUrl: "/resume.pdf",
  // Registered 2 Sep 2026 through Cloudflare Registrar.
  url: "https://mrshine.dev",
  seo: {
    description: "A personal time capsule — who I am and what I love to do. Projects, highlights, and what I'm reading.",
  },
};

/** Rows on the contact card, in order. Blank hrefs drop rather than render empty. */
export const contactRows: { label: string; href: string; text: string; me?: boolean; copy?: boolean }[] = [
  { label: "Website", href: site.url, text: site.url.replace(/^https?:\/\//, "") },
  { label: "Email", href: `mailto:${site.socials.email}`, text: site.socials.email, copy: true },
  { label: "LinkedIn", href: site.socials.linkedin, text: "oak-soe-khant", me: true },
  { label: "GitHub", href: site.socials.github, text: "Mr-Shine09", me: true },
  { label: "Save contact", href: "/contact.vcf", text: "contact.vcf" },
].filter((row) => row.href && row.text);
```

- [ ] **Step 4: Rewrite `global.css`**

```css
@import "./tokens.css";

*, *::before, *::after { box-sizing: border-box; }

html {
  scroll-behavior: smooth;
  scroll-padding-top: 4.5rem; /* sticky top bar height + breathing room */
  -webkit-text-size-adjust: 100%;
  /* Geist Pixel has no weight axis; never let a browser fake one (Plan.md §2.2). */
  font-synthesis: none;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: var(--fs-base);
  line-height: var(--leading-body);
  /* Belt for §2.1: wide things scroll inside their own container, never the body. */
  overflow-x: hidden;
}

::selection { background: var(--selection); }

/* Headings, labels, chips and counts are the pixel face. There is no bold:
   hierarchy is a size step, emphasis is the accent colour, labels are
   uppercase + letterspacing. */
h1, h2, h3, .pixel {
  font-family: var(--font-pixel);
  font-weight: 400;
  line-height: var(--leading-tight);
  margin: 0;
  text-wrap: balance;
}
h1 { font-size: var(--fs-xl); }
h2 { font-size: var(--fs-lg); }
h3 { font-size: var(--fs-md); }

strong, b { font-weight: 500; color: var(--accent); }
em, i { font-style: normal; color: var(--accent); }

p { margin: 0 0 var(--space-s); max-width: var(--measure); text-wrap: pretty; }
p:last-child { margin-bottom: 0; }

a {
  color: inherit;
  text-decoration-color: var(--accent);
  text-decoration-thickness: 1px;
  text-underline-offset: 0.25em;
  transition: color 0.15s ease, text-decoration-color 0.15s ease;
}
a:hover { color: var(--accent); }

img { max-width: 100%; height: auto; display: block; }
ul, ol { margin: 0; padding: 0; list-style: none; }
button { font: inherit; color: inherit; }
[hidden] { display: none !important; }

/* ---- focus: every interactive element, always visible (§2.9) ---- */
:where(a, button, [tabindex], summary, input):focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
  border-radius: 2px;
}

/* ---- primitives ---- */
.wrap { width: min(100% - var(--gutter) * 2, var(--page-max)); margin-inline: auto; }

.section { padding-block: var(--space-2xl); border-top: var(--border); }
.section:first-of-type { border-top: 0; }

.label {
  font-family: var(--font-pixel);
  font-size: var(--fs-xs);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--muted);
  margin: 0;
}

.chip {
  display: inline-block;
  font-family: var(--font-pixel);
  font-size: var(--fs-xs);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.2rem 0.5rem;
  border: var(--border);
  border-radius: var(--radius);
  color: var(--muted);
}

.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2xs);
  min-height: var(--tap-min); min-width: var(--tap-min);
  padding: 0.55rem 1rem;
  border: 1px solid var(--ink); border-radius: var(--radius);
  background: transparent; color: var(--ink);
  font-family: var(--font-pixel); font-size: var(--fs-sm); letter-spacing: 0.06em; text-transform: uppercase;
  text-decoration: none; cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}
.btn:hover { background: var(--ink); color: var(--bg); }
.btn--primary { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }
.btn--primary:hover { background: var(--ink); border-color: var(--ink); color: var(--bg); }

.sr-only {
  position: absolute; width: 1px; height: 1px; overflow: hidden;
  clip-path: inset(50%); white-space: nowrap;
}

.pixelated { image-rendering: pixelated; }

/* Horizontal scrollers: their own overflow, an edge fade, keyboard-focusable (§6). */
.scroller {
  overflow-x: auto; overflow-y: hidden;
  scroll-snap-type: x mandatory;
  scrollbar-width: thin;
  -webkit-overflow-scrolling: touch;
  mask-image: linear-gradient(to right, transparent, #000 2.5rem, #000 calc(100% - 2.5rem), transparent);
}

/* ---- reduced motion (§2.3) ---- */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
  }
}
```

- [ ] **Step 5: Write `SectionHead.astro`**

```astro
---
interface Props {
  id: string;         // section id; heading gets `${id}-title`
  title: string;
  label?: string;     // small letterspaced line under the title (e.g. a count)
  emoji?: string;     // decorative, above the title
}
const { id, title, label, emoji } = Astro.props;
---
<header class="section-head">
  {emoji && <span class="section-head__emoji" aria-hidden="true">{emoji}</span>}
  <h2 id={`${id}-title`} class="section-head__title">{title}</h2>
  {label && <p class="label">{label}</p>}
</header>

<style>
  .section-head { display: grid; gap: var(--space-xs); margin-bottom: var(--space-l); }
  .section-head__emoji { font-size: var(--fs-xl); line-height: 1; }
  .section-head__title { font-size: var(--fs-xl); letter-spacing: 0.04em; text-transform: uppercase; }
  @media (max-width: 40rem) { .section-head__title { font-size: var(--fs-lg); } }
</style>
```

- [ ] **Step 6: Write `TopBar.astro`**

```astro
---
import { sections } from "../data/nav";
import ThemeToggle from "./ThemeToggle.astro";
---
<header class="topbar">
  <div class="wrap topbar__row">
    <a class="topbar__mark" href="#top" aria-label="Back to top">
      <img src="/favicon-32.png" alt="" width="32" height="32" class="pixelated" />
    </a>
    <nav class="topbar__nav" aria-label="Sections" data-topnav>
      {sections.map((s) => <a href={`#${s.id}`} data-nav-link={s.id}>{s.label}</a>)}
    </nav>
    <ThemeToggle />
  </div>
</header>

<style>
  .topbar {
    position: sticky; top: 0; z-index: 50;
    background: color-mix(in srgb, var(--bg) 92%, transparent);
    backdrop-filter: blur(6px);
    border-bottom: var(--border);
  }
  .topbar__row { display: flex; align-items: center; gap: var(--space-s); min-height: 3.5rem; }
  .topbar__mark { display: inline-flex; align-items: center; justify-content: center; min-width: var(--tap-min); min-height: var(--tap-min); flex: none; }
  .topbar__nav { display: flex; gap: 0; margin-left: auto; overflow-x: auto; scrollbar-width: none; }
  .topbar__nav a {
    display: inline-flex; align-items: center;
    min-height: var(--tap-min); padding: 0 0.7rem;
    font-family: var(--font-pixel); font-size: var(--fs-sm); letter-spacing: 0.1em; text-transform: uppercase;
    text-decoration: none; color: var(--muted); white-space: nowrap;
    border-bottom: 2px solid transparent;
  }
  .topbar__nav a:hover, .topbar__nav a[aria-current="true"] { color: var(--ink); border-bottom-color: var(--accent); }
  @media (max-width: 40rem) {
    .topbar__nav a { font-size: var(--fs-xs); padding: 0 0.5rem; }
  }
</style>

<script>
  // Progressive enhancement: mark the section in view. Anchors work without it.
  const links = new Map<string, HTMLAnchorElement>();
  for (const a of document.querySelectorAll<HTMLAnchorElement>("[data-nav-link]")) links.set(a.dataset.navLink!, a);
  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        for (const a of links.values()) a.removeAttribute("aria-current");
        links.get(e.target.id)?.setAttribute("aria-current", "true");
      }
    },
    { rootMargin: "-40% 0px -55% 0px" }
  );
  for (const id of links.keys()) { const s = document.getElementById(id); if (s) io.observe(s); }
</script>
```

- [ ] **Step 7: Write `Base.astro`**

```astro
---
import { Font } from "astro:assets";
import { site } from "../data/site";
import TopBar from "../components/TopBar.astro";
import "../styles/global.css";

interface Props { title?: string; description?: string }
const { title, description = site.seo.description } = Astro.props;
const pageTitle = title ? `${title} — ${site.name}` : `${site.name} — ${site.shortRole}`;
const canonical = new URL(Astro.url.pathname, site.url).href;
---
<!doctype html>
<html lang="en" data-theme="light" id="top">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{pageTitle}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />
    <link rel="icon" href="/favicon.ico" sizes="any" />
    <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32" />
    <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48" />
    <link rel="icon" href="/favicon.png" type="image/png" sizes="512x512" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content={pageTitle} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonical} />
    <meta name="twitter:card" content="summary" />

    <Font cssVariable="--font-pixel" preload />
    <Font cssVariable="--font-sans" preload />

    {/* Theme before first paint (Plan.md §5.3). Inline and blocking on purpose. */}
    <script is:inline>
      (function () {
        try {
          var s = localStorage.getItem("theme");
          if (s === "dark" || s === "light") { document.documentElement.dataset.theme = s; return; }
        } catch (e) {}
        if (window.matchMedia("(prefers-color-scheme: dark)").matches) document.documentElement.dataset.theme = "dark";
      })();
    </script>
    <noscript>
      {/* JS off: follow the OS. The dark tokens are mirrored from tokens.css. */}
      <style>
        @media (prefers-color-scheme: dark) {
          html { color-scheme: dark; --bg: #150E2B; --ink: #E7DEFB; --accent: #FF7A55; --muted: #A99BC9; --line: #2E2450; --plate: #221846; --on-accent: #150E2B; }
        }
      </style>
    </noscript>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <TopBar />
    <main id="main">
      <slot />
    </main>
    <slot name="after" />
  </body>
</html>

<style>
  .skip-link {
    position: absolute; left: var(--space-s); top: var(--space-s); z-index: 100;
    padding: 0.7rem 1.1rem; background: var(--accent); color: var(--on-accent);
    text-decoration: none; border-radius: var(--radius);
    transform: translateY(-200%); transition: transform 0.15s ease;
  }
  .skip-link:focus { transform: translateY(0); }
</style>
```

- [ ] **Step 8: Write the skeleton `index.astro`**

```astro
---
import Base from "../layouts/Base.astro";
import SectionHead from "../components/SectionHead.astro";
import { sections } from "../data/nav";
---
<Base>
  {sections.map((s) => (
    <section id={s.id} class="section" aria-labelledby={`${s.id}-title`}>
      <div class="wrap"><SectionHead id={s.id} title={s.label} /></div>
    </section>
  ))}
</Base>
```

- [ ] **Step 9: Rewrite `content.config.ts` (projects + books; achievements come in Task 6)**

```ts
import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "zod";

/**
 * Content lives in files. Every schema fails the build BY NAME on an invalid
 * state (Plan.md §8) — silent fallbacks are how unfinished books grow ratings.
 */

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string(),
        order: z.number().default(99),
        year: z.string(),
        stack: z.array(z.string()).default([]),
        summary: z.string(),
        image: image().optional(),
        imageAlt: z.string().optional(),
        /** Empty = no line rendered. Never claims "solo". */
        collaborators: z.array(z.string()).default([]),
        builtAt: z.string().optional(),
        links: z.object({ github: z.url().optional(), devpost: z.url().optional(), live: z.url().optional() }).default({}),
        draft: z.boolean().default(false),
      })
      .superRefine((data, ctx) => {
        if (data.image && !data.imageAlt) {
          ctx.addIssue({ code: "custom", path: ["imageAlt"], message: `"${data.title}": an image needs \`imageAlt\` describing what it shows` });
        }
      }),
});

const books = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/books" }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string(),
        author: z.string(),
        /** ISBN-13 digits only. Drives `npm run covers`. */
        isbn: z.string().regex(/^\d{13}$/, "isbn must be 13 digits, no dashes").optional(),
        /** Output of `npm run covers`; Astro fails the build if the file is missing. */
        cover: image().optional(),
        language: z.enum(["en", "my"]),
        genre: z.enum(["nonfiction", "fiction"]),
        status: z.enum(["reading", "finished"]),
        started: z.string().optional(),
        ended: z.string().optional(),
        progress: z.number().min(0).max(100).optional(),
        rating: z.union([z.literal(1), z.literal(2), z.literal(3), z.literal(4), z.literal(5)]).optional(),
        review: z.string().optional(),
        /** A brief note, any status. */
        note: z.string().optional(),
        pageCount: z.number().positive().optional(),
      })
      .superRefine((data, ctx) => {
        const name = `"${data.title}"`;
        const finishedOnly = ["ended", "rating", "review"] as const;
        for (const key of finishedOnly) {
          if (data[key] !== undefined && data.status !== "finished") {
            ctx.addIssue({ code: "custom", path: [key], message: `${name}: \`${key}\` is set but status is "${data.status}" — only finished books have it` });
          }
        }
        if (data.progress !== undefined && data.status !== "reading") {
          ctx.addIssue({ code: "custom", path: ["progress"], message: `${name}: \`progress\` is set but status is "${data.status}" — progress only means something mid-read` });
        }
        if (data.isbn && !data.cover) {
          ctx.addIssue({ code: "custom", path: ["cover"], message: `${name}: has an isbn but no \`cover\` — run \`npm run covers\` and add \`cover: ../../assets/books/<slug>.jpg\`` });
        }
        if (data.language === "my") {
          ctx.addIssue({ code: "custom", path: ["language"], message: `${name}: Burmese needs a Myanmar-capable font registered in astro.config.mjs first (Plan.md §4.3)` });
        }
      }),
});

export const collections = { projects, books };
```
Note: the `language: "my"` issue is unconditional for now because no Myanmar font is registered. When one is added, replace the condition with a check against an exported `MYANMAR_FONT_READY = true` constant.

- [ ] **Step 10: Temporarily park the two project files that the schema still accepts but the page does not yet use**

Nothing to do — `01-pokedesk.md`, `02-echo.md`, `03-lookout.md` all validate against this schema. `03-lookout.md` has `draft: true` and is replaced in Task 8.

- [ ] **Step 11: Build, run the two checks**

Run: `npm run build 2>&1 | grep -E "WARN|error|Complete" ; node tests/verify.mjs sections overflow`
Expected: no `WARN`, `Complete!`, then `✓ sections` and `✓ overflow`.

- [ ] **Step 12: Commit**

```bash
cd .. && git add site && git commit -m "rebuild: base layout, top bar, global styles, page skeleton, verify harness

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3: Scene player and hero welcome (carry forward, resize hooks)

**Files:**
- Modify: `site/src/components/AnimatedScene.astro` — add `scale` prop for integer display sizes
- Modify: `site/src/components/HeroWelcome.astro` — add `scale` prop
- Test: `tests/verify.mjs` checks `pixelated`, `reduced-motion-scenes`

**Interfaces:**
- Produces: `<AnimatedScene scene="trophy-lift" once scale={1|0.5} class="…" />` rendering a `<span class="oak-scene">` sized `384×320 × scale`; `<HeroWelcome scale={1|2} />` sized `160×208 × scale`. Both expose `img[data-oak-scene-image]` / `img[data-welcome-sprite]` whose `src` ends in `-static.png` when paused.

- [ ] **Step 1: Add the checks**

Append to `tests/verify.mjs` before `// ---- runner ----`:
```js
check("pixelated", async (browser) => {
  const { ctx, p } = await page(browser);
  const bad = await p.$$eval(".oak-scene img, .hero-welcome img, .runner img", (imgs) =>
    imgs.filter((i) => getComputedStyle(i).imageRendering !== "pixelated").map((i) => i.getAttribute("src")));
  assert(bad.length === 0, `not pixelated: ${bad.join(", ")}`);
  const count = await p.locator(".oak-scene img, .hero-welcome img").count();
  assert(count >= 4, `expected ≥4 mascot images, found ${count}`);
  await ctx.close();
});

check("reduced-motion-scenes", async (browser) => {
  const { ctx, p } = await page(browser, { reducedMotion: "reduce" });
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(600);
  const srcs = await p.$$eval(".oak-scene img, .hero-welcome img", (imgs) => imgs.map((i) => i.getAttribute("src")));
  const animated = srcs.filter((s) => !s.includes("-static."));
  assert(animated.length === 0, `animated under reduced motion: ${animated.join(", ")}`);
  await ctx.close();
});
```

- [ ] **Step 2: Run them to see them fail**

Run: `node tests/verify.mjs pixelated reduced-motion-scenes`
Expected: `✗ pixelated: FAIL — expected ≥4 mascot images, found 0`. (`reduced-motion-scenes` passes vacuously; it becomes meaningful from Task 4.)

- [ ] **Step 3: Add `scale` to `AnimatedScene.astro`**

In the frontmatter, extend `Props` and destructuring:
```ts
interface Props {
  scene: SceneId;
  class?: string;
  label?: string;
  /** Play once on first reveal and hold the APNG's final frame. */
  once?: boolean;
  /** Integer-friendly display scale: 1 = 384×320, 0.5 = 192×160. */
  scale?: 0.5 | 1;
}
const { scene, class: className, label, once = false, scale = 1 } = Astro.props;
```
Replace the `<span … data-oak-scene={payload}>` opening tag with:
```astro
<span
  class:list={["oak-scene", className]}
  role="img"
  aria-label={label ?? metadata.label}
  data-oak-scene={payload}
  style={`--scene-w:${frameWidth * scale}px;--scene-h:${frameHeight * scale}px`}
>
```
Replace the `<style>` block with:
```css
  .oak-scene { display: block; width: var(--scene-w); height: var(--scene-h); max-width: 100%; }
  .oak-scene__animation { display: block; width: 100%; height: 100%; object-fit: contain; image-rendering: pixelated; }
  /* Phones: half size keeps integer scale (384→192). */
  @media (max-width: 40rem) { .oak-scene { width: calc(var(--scene-w) / 2); height: calc(var(--scene-h) / 2); } }
```
Leave the `<script>` untouched — it is the fail-open player (§2.6).

- [ ] **Step 4: Add `scale` to `HeroWelcome.astro`**

Frontmatter:
```ts
interface Props { scale?: 1 | 2 }
const { scale = 1 } = Astro.props;
```
Add `style={`--w:${spriteWidth * scale}px;--h:${spriteHeight * scale}px`}` to the `.hero-welcome` div, and change the style block's fixed sizes:
```css
  .hero-welcome { position: relative; width: var(--w); flex: none; }
  .hero-welcome__sprite { display: block; width: var(--w); height: var(--h); image-rendering: pixelated; }
  .hero-welcome__bubble { position: absolute; top: -2.2rem; left: 68%; z-index: 1; }
  @media (max-width: 48rem) { .hero-welcome { width: 160px; } .hero-welcome__sprite { width: 160px; height: 208px; } }
```
Leave the script untouched.

- [ ] **Step 5: Build and type-check**

Run: `npm run build 2>&1 | grep -E "error|Complete" && npm run check 2>&1 | tail -3`
Expected: `Complete!`; check reports `0 errors`. (`pixelated` still fails until scenes are placed in Tasks 4–7; that is expected.)

- [ ] **Step 6: Commit**

```bash
cd .. && git add site && git commit -m "scenes: scale prop for AnimatedScene and HeroWelcome; pixelated/reduced-motion checks

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4: Hero (§7.1)

**Files:**
- Create: `site/src/components/PlaneMotif.astro`, `site/src/components/Hero.astro`
- Modify: `site/src/pages/index.astro`
- Test: `tests/verify.mjs` check `hero`

**Interfaces:**
- Consumes: `site` (Task 2), `HeroWelcome` (Task 3), `portrait.jpg` via `astro:assets` `<Image>`.
- Produces: `<section id="about">` containing `h1` = name, the lead, tagline, three links with visible labels, the welcome mascot, the bordered portrait, and the closing line.

- [ ] **Step 1: Add the check**

```js
check("hero", async (browser) => {
  const { ctx, p } = await page(browser);
  const s = p.locator("section#about");
  assert((await s.locator("h1").innerText()).trim() === "OAK SOE KHANT", "h1 must be the name in caps");
  const text = await s.innerText();
  assert(text.includes("What's up everyone!!!"), "lead line missing or altered");
  assert(text.includes("Reader in progress."), "tagline missing");
  assert(text.includes("Leveraging artificial intelligence to sharpen actual intelligence."), "closing line missing");
  assert(text.includes("Yangon") && text.includes("Bay Area, CA"), "plane motif missing");
  for (const [label, href] of [["Résumé", "/resume.pdf"], ["GitHub", "https://github.com/Mr-Shine09"], ["LinkedIn", "https://www.linkedin.com/in/oak-soe-khant-350252362"]]) {
    const a = s.locator(`a[href="${href}"]`);
    assert(await a.count() === 1, `hero link ${label} → ${href} missing`);
    assert((await a.innerText()).includes(label), `hero link ${href} has no visible label "${label}"`);
  }
  assert(await s.locator(".hero-welcome").count() === 1, "welcome mascot missing");
  const border = await s.locator(".hero__portrait").evaluate((el) => getComputedStyle(el).borderWidth);
  assert(border === "2px", `portrait border is ${border}, want 2px`);
  await ctx.close();
});
```
Run: `node tests/verify.mjs hero` → Expected: `✗ hero: FAIL — h1 must be the name in caps` (skeleton has no h1).

- [ ] **Step 2: Write `PlaneMotif.astro`**

```astro
---
import { site } from "../data/site";
---
<p class="plane label" aria-label={`From ${site.origin} to ${site.destination}`}>
  <span>{site.origin}</span>
  <span class="plane__track" aria-hidden="true"><span class="plane__icon">✈</span></span>
  <span>{site.destination}</span>
</p>

<style>
  .plane { display: inline-flex; align-items: center; gap: 0.6rem; color: var(--muted); }
  .plane__track { position: relative; display: inline-block; width: 4.5rem; height: 1px; background: var(--line); }
  .plane__icon {
    position: absolute; top: 50%; left: 0; translate: 0 -55%;
    font-size: var(--fs-base); line-height: 1; color: var(--accent);
    animation: fly 6s ease-in-out infinite alternate;
  }
  @keyframes fly { from { left: 0; } to { left: calc(100% - 1em); } }
  @media (prefers-reduced-motion: reduce) { .plane__icon { animation: none; left: calc(100% - 1em); } }
</style>
```

- [ ] **Step 3: Write `Hero.astro`**

```astro
---
import { Image } from "astro:assets";
import { site } from "../data/site";
import HeroWelcome from "./HeroWelcome.astro";
import PlaneMotif from "./PlaneMotif.astro";
import portrait from "../assets/photos/portrait.jpg";

const links = [
  { label: "Résumé", href: site.resumeUrl, icon: "▤" },
  { label: "GitHub", href: site.socials.github, icon: "◉", me: true },
  { label: "LinkedIn", href: site.socials.linkedin, icon: "in", me: true },
];
---
<section id="about" class="section hero" aria-labelledby="about-title">
  <div class="wrap">
    <div class="hero__grid">
      <div class="hero__text">
        <PlaneMotif />
        <h1 id="about-title" class="hero__name">{site.name.toUpperCase()}</h1>
        <p class="label hero__role">{site.shortRole}</p>
        <p class="hero__lead">{site.lead}</p>
        <p class="hero__tagline">{site.tagline}</p>
        <ul class="hero__links" aria-label="Links">
          {links.map((l) => (
            <li>
              <a class="hero__link" href={l.href} rel={l.me ? "me" : undefined}>
                <span class="hero__icon pixel" aria-hidden="true">{l.icon}</span>
                <span class="hero__linklabel">{l.label}</span>
              </a>
            </li>
          ))}
        </ul>
      </div>
      <div class="hero__mascot"><HeroWelcome scale={1} /></div>
      <figure class="hero__portrait-wrap">
        <Image class="hero__portrait" src={portrait} alt="Oak, in side profile" width={360} densities={[1, 2]} loading="eager" />
      </figure>
    </div>
    <p class="hero__closing pixel">{site.closing}</p>
  </div>
</section>

<style>
  .hero { padding-top: var(--space-xl); }
  .hero__grid {
    display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(180px, 300px);
    gap: var(--space-l); align-items: end;
  }
  .hero__text { display: grid; gap: var(--space-s); align-content: end; min-width: 0; }
  .hero__name { font-size: var(--fs-2xl); letter-spacing: 0.02em; overflow-wrap: anywhere; }
  .hero__role { color: var(--muted); }
  .hero__lead { font-size: var(--fs-md); line-height: 1.5; }
  .hero__tagline { color: var(--muted); }
  .hero__links { display: flex; flex-wrap: wrap; gap: var(--space-s); margin-top: var(--space-xs); }
  .hero__link {
    display: inline-flex; flex-direction: column; align-items: center; gap: 0.3rem;
    min-width: var(--tap-min); min-height: var(--tap-min); padding: 0.4rem 0.6rem;
    text-decoration: none; color: var(--ink);
  }
  .hero__icon {
    display: grid; place-items: center; width: 44px; height: 44px;
    border: 2px solid var(--ink); border-radius: var(--radius); font-size: var(--fs-md);
  }
  .hero__linklabel { font-family: var(--font-pixel); font-size: var(--fs-xs); letter-spacing: 0.1em; text-transform: uppercase; }
  .hero__link:hover .hero__icon { background: var(--ink); color: var(--bg); }
  .hero__mascot { align-self: end; }
  .hero__portrait-wrap { margin: 0; padding: var(--space-xs); background: var(--plate); border: var(--border); }
  .hero__portrait { border: 2px solid var(--line); aspect-ratio: 1; object-fit: cover; width: 100%; }
  .hero__closing { margin-top: var(--space-xl); font-size: var(--fs-lg); text-align: center; text-wrap: balance; }

  @media (max-width: 64rem) {
    .hero__grid { grid-template-columns: minmax(0, 1fr) auto; }
    .hero__portrait-wrap { grid-column: 1 / -1; max-width: 300px; }
  }
  @media (max-width: 40rem) {
    .hero__grid { grid-template-columns: minmax(0, 1fr); }
    .hero__name { font-size: var(--fs-xl); }
    .hero__mascot { justify-self: start; }
    .hero__portrait-wrap { max-width: 60vw; }
    .hero__closing { font-size: var(--fs-md); }
  }
</style>
```

- [ ] **Step 4: Wire it into `index.astro`**

Replace the file with:
```astro
---
import Base from "../layouts/Base.astro";
import SectionHead from "../components/SectionHead.astro";
import Hero from "../components/Hero.astro";
import { sections } from "../data/nav";
const rest = sections.filter((s) => s.id !== "about");
---
<Base>
  <Hero />
  {rest.map((s) => (
    <section id={s.id} class="section" aria-labelledby={`${s.id}-title`}>
      <div class="wrap"><SectionHead id={s.id} title={s.label} /></div>
    </section>
  ))}
</Base>
```

- [ ] **Step 5: Build, verify**

Run: `npm run build 2>&1 | grep -E "error|Complete" && node tests/verify.mjs hero overflow sections`
Expected: all three `✓`. If `overflow` fails at 320, the culprit is almost always `.hero__name` — confirm `overflow-wrap: anywhere` is present, or reduce to `--fs-lg` under 24rem.

- [ ] **Step 6: Commit**

```bash
cd .. && git add site && git commit -m "hero: name, lead, tagline, links, plane motif, welcome mascot, bordered portrait, closing line

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 5: Bottom runner (§7.6)

**Files:**
- Create: `site/src/components/BottomRunner.astro`
- Modify: `site/src/layouts/Base.astro` — render it after `<main>`
- Test: `tests/verify.mjs` checks `runner`, `reduced-motion-runner`

**Interfaces:**
- Produces: `<div class="runner-layer" data-runner>` fixed overlay; `img[data-runner-sprite]` whose `src` is `run-atlas.png?play=N` while scrolling and `run-static.png` when settled. Hidden under reduced motion via CSS.

- [ ] **Step 1: Add the checks**

```js
check("runner", async (browser) => {
  const { ctx, p } = await page(browser);
  const sprite = p.locator("[data-runner-sprite]");
  assert(await sprite.count() === 1, "runner sprite missing");
  const xAt = async () => p.locator("[data-runner]").evaluate((el) => new DOMMatrix(getComputedStyle(el).transform).m41);
  const x0 = await xAt();
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(250);
  assert((await sprite.getAttribute("src")).includes("run-atlas.png"), "runner should animate while scrolling");
  await p.waitForTimeout(1500);
  const x1 = await xAt();
  assert(x1 < x0 - 200, `runner did not travel left (x ${x0} → ${x1})`);
  assert((await sprite.getAttribute("src")).endsWith("run-static.png"), "runner should freeze when idle");
  const scaleX = await p.locator("[data-runner]").evaluate((el) => new DOMMatrix(getComputedStyle(el).transform).a);
  assert(scaleX < 0, "runner should face left (scaleX(-1))");
  await ctx.close();
});

check("reduced-motion-runner", async (browser) => {
  const { ctx, p } = await page(browser, { reducedMotion: "reduce" });
  const display = await p.locator(".runner-layer").evaluate((el) => getComputedStyle(el).display);
  assert(display === "none", `runner layer visible under reduced motion (display ${display})`);
  await ctx.close();
});
```
Run: `node tests/verify.mjs runner reduced-motion-runner` → Expected: both `✗` (no runner yet).

- [ ] **Step 2: Write `BottomRunner.astro`**

```astro
---
// Decorative scroll runner (Plan.md §7.6). Parked off the right edge at scroll
// 0, arrives at the left edge at page bottom. The APNG cannot be paused, so the
// sprite swaps to its static frame when the eased position settles and back to
// the animation on the next scroll. Hidden under reduced motion by CSS alone.
---
<div class="runner-layer" aria-hidden="true">
  <div class="runner" data-runner>
    <img class="runner__sprite" data-runner-sprite src="/assets/animation/scenes/run-static.png" alt="" width="384" height="320" />
  </div>
</div>

<style>
  .runner-layer { position: fixed; inset: 0; z-index: 40; overflow: hidden; pointer-events: none; contain: strict; }
  .runner {
    position: absolute; left: 0; bottom: max(0.65rem, env(safe-area-inset-bottom));
    width: 192px; height: 160px; will-change: transform; transform: translate3d(110vw, 0, 0);
  }
  .runner__sprite { display: block; width: 100%; height: 100%; object-fit: contain; image-rendering: pixelated; }
  @media (max-width: 40rem) { .runner { width: 96px; height: 80px; bottom: max(0.4rem, env(safe-area-inset-bottom)); } }
  @media (prefers-reduced-motion: reduce) { .runner-layer { display: none; } }
</style>

<script>
  const ANIMATED = "/assets/animation/scenes/run-atlas.png";
  const STATIC = "/assets/animation/scenes/run-static.png";
  let token = 0;

  function mount(el: HTMLElement) {
    const sprite = el.querySelector<HTMLImageElement>("[data-runner-sprite]");
    if (!sprite) return;
    let target = 0, rendered = 0, frame = 0, running = false;

    const showAnimated = () => { if (!running) { running = true; sprite.src = `${ANIMATED}?play=${++token}`; } };
    const showStatic = () => { if (running) { running = false; sprite.src = STATIC; } };

    const read = () => {
      const root = document.documentElement;
      const range = Math.max(1, root.scrollHeight - window.innerHeight);
      if (range < window.innerHeight * 0.35) { el.style.display = "none"; return; }
      el.style.display = "";
      target = Math.min(1, Math.max(0, window.scrollY / range));
      if (Math.abs(target - rendered) > 0.0002) showAnimated();
      if (!frame) frame = requestAnimationFrame(render);
    };

    const render = () => {
      frame = 0;
      rendered += (target - rendered) * 0.14;
      const w = el.getBoundingClientRect().width;
      const travel = window.innerWidth + w * 2.4;
      const x = window.innerWidth + w * 0.7 - rendered * travel;
      // The scene is authored running toward the viewer's right; we travel left.
      el.style.transform = `translate3d(${x.toFixed(2)}px, 0, 0) scaleX(-1)`;
      if (Math.abs(target - rendered) > 0.0002) frame = requestAnimationFrame(render);
      else showStatic();
    };

    window.addEventListener("scroll", read, { passive: true });
    window.addEventListener("resize", read, { passive: true });
    read();
  }

  for (const el of document.querySelectorAll<HTMLElement>("[data-runner]")) mount(el);
</script>
```

- [ ] **Step 3: Render it from `Base.astro`**

Add `import BottomRunner from "../components/BottomRunner.astro";` and replace `<slot name="after" />` with `<BottomRunner />`.

- [ ] **Step 4: Build, verify**

Run: `npm run build 2>&1 | grep -E "error|Complete" && node tests/verify.mjs runner reduced-motion-runner overflow`
Expected: all `✓`. If `runner` fails on "did not travel left", the page is too short at this stage (only the hero has content) — the runner hides itself below 0.35 viewports of scroll range. Re-run after Task 7; do not weaken the check.

- [ ] **Step 5: Commit**

```bash
cd .. && git add site && git commit -m "runner: scroll-driven run scene along the bottom, right to left, static when idle

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6: Highlights (§7.2)

**Files:**
- Modify: `site/src/content.config.ts` — add `achievements`
- Create: `site/src/content/achievements/icpc-pacnw-2025.md`
- Create: `site/src/components/Highlights.astro`
- Modify: `site/src/pages/index.astro`
- Test: named-failure test for the schema; `tests/verify.mjs` check `highlights`

**Interfaces:**
- Produces: collection `achievements` with `{ title, org, year, kind, link?, order }`; `<Highlights />` renders `<section id="highlights">` with `trophy-lift` scene (`once`), a `<ul class="achievements">`, and the coming-soon line when fewer than 3 entries.

- [ ] **Step 1: Add the collection**

In `content.config.ts`, before `export const collections`:
```ts
const achievements = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/achievements" }),
  schema: z.object({
    title: z.string(),
    org: z.string(),
    year: z.string().regex(/^\d{4}$/, "year must be four digits"),
    kind: z.enum(["competition", "hackathon", "award", "other"]),
    link: z.url().optional(),
    order: z.number().default(99),
  }),
});
```
and change the export to `export const collections = { projects, books, achievements };`.

- [ ] **Step 2: Prove the schema fails by name**

Create `src/content/achievements/bad.md` with `---\ntitle: x\norg: y\nyear: "25"\nkind: competition\n---` and run `npm run build 2>&1 | grep -E "year|bad" | head -3`.
Expected: an error naming `bad.md` and `year must be four digits`. Then `rm src/content/achievements/bad.md`.

- [ ] **Step 3: Write the real entry**

`src/content/achievements/icpc-pacnw-2025.md`:
```md
---
title: ICPC Pacific Northwest Regional, Division I — Participant
org: ICPC
year: "2025"
kind: competition
order: 1
---
```

- [ ] **Step 4: Add the check**

```js
check("highlights", async (browser) => {
  const { ctx, p } = await page(browser);
  const s = p.locator("section#highlights");
  assert((await s.locator("h2").innerText()).toUpperCase().includes("HIGHLIGHTS"), "heading");
  assert(await s.locator(".achievements li").count() === 1, "expected one achievement row");
  const row = await s.locator(".achievements li").first().innerText();
  assert(row.includes("ICPC") && row.includes("2025"), `row text: ${row}`);
  assert((await s.innerText()).includes("More achievements coming soon."), "coming-soon line missing");
  assert(await s.locator('.oak-scene[aria-label*="trophy"]').count() === 1, "trophy-lift scene missing");
  await ctx.close();
});
```
Run: `node tests/verify.mjs highlights` → `✗` (skeleton).

- [ ] **Step 5: Write `Highlights.astro`**

```astro
---
import { getCollection } from "astro:content";
import AnimatedScene from "./AnimatedScene.astro";
import SectionHead from "./SectionHead.astro";

const COMING_SOON_BELOW = 3;
const items = (await getCollection("achievements")).sort((a, b) => a.data.order - b.data.order);
---
<section id="highlights" class="section" aria-labelledby="highlights-title">
  <div class="wrap highlights">
    <AnimatedScene scene="trophy-lift" once class="highlights__scene" />
    <div class="highlights__body">
      <SectionHead id="highlights" title="Highlights" emoji="🏆" />
      <ul class="achievements">
        {items.map(({ data }) => (
          <li class="achievement">
            <span class="achievement__glyph" aria-hidden="true">🏆</span>
            <span class="achievement__text">
              {data.link ? <a href={data.link} rel="noopener">{data.title}</a> : data.title}
              <span class="achievement__meta pixel">{data.org} · {data.year}</span>
            </span>
          </li>
        ))}
      </ul>
      {items.length < COMING_SOON_BELOW && <p class="highlights__soon">More achievements coming soon.</p>}
    </div>
  </div>
</section>

<style>
  .highlights { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: var(--space-l); align-items: start; }
  .highlights__scene { align-self: end; }
  .achievements { display: grid; gap: var(--space-s); }
  .achievement { display: flex; gap: var(--space-s); align-items: flex-start; min-height: var(--tap-min); padding: var(--space-xs) 0; border-bottom: var(--border); }
  .achievement__glyph { font-size: var(--fs-md); line-height: 1.4; }
  .achievement__text { display: grid; gap: 0.2rem; }
  .achievement__meta { font-size: var(--fs-xs); letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }
  .highlights__soon { margin-top: var(--space-m); color: var(--muted); }
  @media (max-width: 48rem) { .highlights { grid-template-columns: 1fr; } }
</style>
```

- [ ] **Step 6: Wire into `index.astro`**

Add `import Highlights from "../components/Highlights.astro";`, change `rest` to exclude `"about"` and `"highlights"`, and render `<Hero />` then `<Highlights />` before the remaining skeleton sections.

- [ ] **Step 7: Build, verify, commit**

Run: `npm run build 2>&1 | grep -E "error|Complete" && node tests/verify.mjs highlights sections overflow`
Expected: all `✓`.
```bash
cd .. && git add site && git commit -m "highlights: achievements collection, ICPC PacNW 2025, trophy-lift scene

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: Projects slider (§7.3)

**Files:**
- Create: `site/src/components/ProjectCard.astro`, `ProjectSlider.astro`, `Projects.astro`
- Create: `site/src/assets/projects/lookout-eye.png`, `visionassist-hero.jpg` (download)
- Create: `site/src/content/projects/02-look-out.md`, `03-visionassist.md`; rename `02-echo.md` → `04-echo.md`; delete `03-lookout.md`
- Modify: `site/src/pages/index.astro`
- Test: `tests/verify.mjs` checks `projects`, `nojs`

**Interfaces:**
- Consumes: `projects` collection (Task 2), `AnimatedScene` (Task 3).
- Produces: `<section id="projects">` with `.slider__track` (scroll-snap) holding `.card` articles in order PokeDesk, Look-Out, VisionAssist, Echo; `button[data-slider-prev]`, `button[data-slider-next]`.

- [ ] **Step 1: Content files and images**

```bash
curl -sSL -o src/assets/projects/lookout-eye.png "https://raw.githubusercontent.com/Mr-Shine09/Look-Out/HEAD/public/lookout-eye-1024.png"
curl -sSL -o src/assets/projects/visionassist-hero.jpg "https://raw.githubusercontent.com/Mr-Shine09/VisionAssist/HEAD/docs/images/hero.jpg"
git mv src/content/projects/02-echo.md src/content/projects/04-echo.md
git rm -q src/content/projects/03-lookout.md
```
Edit `04-echo.md`: change `order: 2` to `order: 4`. Keep everything else.

`src/content/projects/02-look-out.md`:
```md
---
title: Look-Out
order: 2
year: "2026"
stack: ["Python 3.11", "FastAPI", "Redis Stack", "Vite", "Ollama / Claude", "Browserbase"]
summary: The first alert tool built to notify you less — semantic dedup in Redis vector search plus an LLM relevance judge, so only genuinely new and relevant items surface.
collaborators: []
builtAt: "UC Berkeley AI Hackathon 2026"
links:
  github: https://github.com/Mr-Shine09/Look-Out
image: ../../assets/projects/lookout-eye.png
imageAlt: The Lookout logo — a single watchful eye.
draft: false
---

Every alert tool is built to notify you more. Lookout is a suppression engine:
for each change it detects, it asks whether it has effectively shown you this
already (a semantic-duplicate check against alert history in Redis vector
search) and whether it actually matters (an LLM judge against a spec compiled
from your plain-English ask). It only surfaces an alert when both clear the bar.
```
Note `collaborators: []` — the team names are `TODO(owner)`; an empty list renders no line and never claims solo.

`src/content/projects/03-visionassist.md`:
```md
---
title: VisionAssist
order: 3
year: "2026"
stack: ["Python", "YOLOv8n", "Raspberry Pi 5", "Arducam IMX708", "Piper TTS", "Flask"]
summary: Wearable obstacle detection and spoken navigation for the visually impaired. Runs fully offline on a Raspberry Pi 5.
collaborators: []
builtAt: "De Anza College, Infineon-sponsored capstone"
links:
  github: https://github.com/Mr-Shine09/VisionAssist
image: ../../assets/projects/visionassist-hero.jpg
imageAlt: The 3D-printed head-mounted enclosure holding a Raspberry Pi 5 with an Arducam camera on the lid.
draft: false
---

There is no depth sensor. Distance comes from the pinhole relation between a
known object height, the focal length, and the bounding-box height YOLO
reports — and it overestimates at close range, because a partially visible
chair produces a short box. The zones were widened to compensate; the honest
fix, edge-clip detection, is on the roadmap.
```

- [ ] **Step 2: Add the checks**

```js
check("projects", async (browser) => {
  const { ctx, p } = await page(browser);
  const titles = await p.$$eval("section#projects .card h3", (els) => els.map((e) => e.textContent.trim()));
  assert(titles.join("|") === "PokeDesk|Look-Out|VisionAssist|Echo", `card order: ${titles.join(" · ")}`);
  const echo = p.locator("section#projects .card", { hasText: "Echo" });
  const echoText = await echo.innerText();
  for (const n of ["aadityad12", "shahxsheel", "Mr-Shine09"]) assert(echoText.includes(n), `Echo must credit ${n}`);
  assert(await echo.locator('a[href="https://github.com/aadityad12/Echo"]').count() === 1, "Echo repo link");
  const fit = await p.locator("section#projects .card img").first().evaluate((i) => getComputedStyle(i).objectFit);
  assert(fit === "contain", `card images must be object-fit: contain, got ${fit}`);
  const track = p.locator("section#projects .slider__track");
  const before = await track.evaluate((t) => t.scrollLeft);
  await p.locator("[data-slider-next]").click();
  await p.waitForTimeout(600);
  assert((await track.evaluate((t) => t.scrollLeft)) > before, "next button did not scroll the track");
  assert(await p.locator('section#projects .oak-scene[aria-label*="workbench"]').count() === 1, "workbench-zap scene missing");
  await ctx.close();
});

check("nojs", async (browser) => {
  const { ctx, p } = await page(browser, { javaScriptEnabled: false });
  for (const id of SECTIONS) assert(await p.locator(`section#${id}`).count() === 1, `no-JS: section ${id} missing`);
  assert(await p.locator("section#projects .card").count() === 4, "no-JS: cards missing");
  assert(await p.locator('section#projects a[href="https://github.com/Mr-Shine09/PokeDesk"]').count() === 1, "no-JS: repo link");
  await ctx.close();
});
```
Run: `node tests/verify.mjs projects nojs` → both `✗`.

- [ ] **Step 3: Write `ProjectCard.astro`**

```astro
---
import { Image } from "astro:assets";
import type { CollectionEntry } from "astro:content";
interface Props { project: CollectionEntry<"projects">; index: number }
const { project, index } = Astro.props;
const { data } = project;
const meta = [data.year, data.builtAt].filter(Boolean).join(" · ");
---
<article class="card" tabindex="0" aria-roledescription="slide" aria-label={`${index + 1} of 4: ${data.title}`}>
  <div class="card__plate">
    {data.image && <Image class="card__image" src={data.image} alt={data.imageAlt ?? ""} width={640} densities={[1, 2]} loading={index === 0 ? "eager" : "lazy"} />}
  </div>
  <div class="card__body">
    <h3 class="card__title">{data.title}</h3>
    <p class="card__summary">{data.summary}</p>
    <ul class="card__stack" aria-label="Stack">{data.stack.map((s) => <li class="chip">{s}</li>)}</ul>
    {meta && <p class="card__meta pixel">{meta}</p>}
    {data.collaborators.length > 0 && <p class="card__team">With {data.collaborators.join(" · ")}</p>}
    <p class="card__links">
      {data.links.github && <a class="btn" href={data.links.github} rel="noopener">GitHub</a>}
      {data.links.devpost && <a class="btn" href={data.links.devpost} rel="noopener">Devpost</a>}
      {data.links.live && <a class="btn btn--primary" href={data.links.live} rel="noopener">Live</a>}
    </p>
  </div>
</article>

<style>
  .card {
    scroll-snap-align: center; flex: 0 0 min(85vw, 34rem);
    display: grid; grid-template-rows: auto 1fr;
    border: var(--border); border-radius: var(--radius); background: var(--bg);
    transform-origin: center;
  }
  .card__plate { aspect-ratio: 16 / 10; background: var(--plate); display: grid; place-items: center; padding: var(--space-s); border-bottom: var(--border); }
  .card__image { width: 100%; height: 100%; object-fit: contain; }
  .card__body { display: grid; gap: var(--space-s); padding: var(--space-m); align-content: start; }
  .card__summary { color: var(--ink); }
  .card__stack { display: flex; flex-wrap: wrap; gap: 0.4rem; }
  .card__meta, .card__team { font-size: var(--fs-sm); color: var(--muted); }
  .card__meta { font-size: var(--fs-xs); letter-spacing: 0.1em; text-transform: uppercase; }
  .card__links { display: flex; flex-wrap: wrap; gap: var(--space-xs); }

  /* Coverflow: the centred card is full size; neighbours recede. Scroll-driven,
     no JS; browsers without support get a flat, fully usable snap carousel. */
  @supports (animation-timeline: view()) {
    .card { animation: card-focus linear both; animation-timeline: view(inline); animation-range: cover 0% cover 100%; }
    @keyframes card-focus { 0%, 100% { transform: scale(0.82); opacity: 0.6; } 50% { transform: scale(1); opacity: 1; } }
  }
  @media (prefers-reduced-motion: reduce) { .card { animation: none; } }
</style>
```

- [ ] **Step 4: Write `ProjectSlider.astro`**

```astro
---
import type { CollectionEntry } from "astro:content";
import ProjectCard from "./ProjectCard.astro";
interface Props { projects: CollectionEntry<"projects">[] }
const { projects } = Astro.props;
---
<div class="slider" data-slider>
  <div class="slider__track scroller" tabindex="0" aria-label="Projects, scroll horizontally">
    {projects.map((p, i) => <ProjectCard project={p} index={i} />)}
  </div>
  <div class="slider__controls">
    <button type="button" class="btn" data-slider-prev aria-label="Previous project">←</button>
    <button type="button" class="btn" data-slider-next aria-label="Next project">→</button>
  </div>
</div>

<style>
  .slider { display: grid; gap: var(--space-s); }
  .slider__track {
    display: flex; gap: var(--space-m);
    padding: var(--space-s) calc(50% - min(85vw, 34rem) / 2);  /* lets first/last card centre */
    scroll-snap-type: x mandatory;
  }
  .slider__controls { display: flex; gap: var(--space-xs); justify-content: center; }
  /* Buttons need JS; hide them without it so nothing dead is on the page. */
  .slider__controls { display: none; }
  :global(html.js) .slider__controls { display: flex; }
</style>

<script>
  document.documentElement.classList.add("js");
  for (const root of document.querySelectorAll<HTMLElement>("[data-slider]")) {
    const track = root.querySelector<HTMLElement>(".slider__track")!;
    const step = () => (track.querySelector<HTMLElement>(".card")?.getBoundingClientRect().width ?? 320) + 24;
    root.querySelector("[data-slider-prev]")?.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));
    root.querySelector("[data-slider-next]")?.addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
    track.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") { e.preventDefault(); track.scrollBy({ left: step(), behavior: "smooth" }); }
      if (e.key === "ArrowLeft") { e.preventDefault(); track.scrollBy({ left: -step(), behavior: "smooth" }); }
    });
  }
</script>
```
- [ ] **Step 5: Write `Projects.astro`**

```astro
---
import { getCollection } from "astro:content";
import AnimatedScene from "./AnimatedScene.astro";
import SectionHead from "./SectionHead.astro";
import ProjectSlider from "./ProjectSlider.astro";
const projects = (await getCollection("projects", ({ data }) => !data.draft)).sort((a, b) => a.data.order - b.data.order);
---
<section id="projects" class="section" aria-labelledby="projects-title">
  <div class="wrap projects__head">
    <SectionHead id="projects" title="Projects" label={`${projects.length} projects`} />
    <AnimatedScene scene="workbench-zap" once class="projects__scene" />
  </div>
  <ProjectSlider projects={projects} />
</section>

<style>
  .projects__head { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: var(--space-l); align-items: end; }
  @media (max-width: 48rem) { .projects__head { grid-template-columns: 1fr; } .projects__scene { justify-self: start; } }
</style>
```

- [ ] **Step 6: Wire, build, verify**

In `index.astro` import `Projects` and render after `<Highlights />`; exclude `"projects"` from `rest`.
Run: `npm run check 2>&1 | tail -2 && npm run build 2>&1 | grep -E "error|Complete" && node tests/verify.mjs projects nojs overflow runner pixelated`
Expected: `0 errors`; all checks `✓`. The page is now long enough for `runner` to pass.

- [ ] **Step 7: Commit**

```bash
cd .. && git add -A site && git commit -m "projects: coverflow slider with PokeDesk, Look-Out, VisionAssist, Echo; workbench-zap scene

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 8: Covers script and book content (§7.4 data)

**Files:**
- Create: `site/scripts/fetch-covers.mjs`
- Modify: `site/src/content/books/dune.md`
- Create: `site/src/content/books/the-infinity-machine.md`
- Create: `site/src/assets/books/dune.jpg`, `the-infinity-machine.jpg` (script output)

**Interfaces:**
- Produces: `npm run covers` — for each `src/content/books/*.md` with `isbn:`, writes `src/assets/books/<slug>.jpg` if absent; exits non-zero on 404 or tiny placeholder. Book files reference `cover: ../../assets/books/<slug>.jpg`.

- [ ] **Step 1: Write the script**

```js
// Download Open Library covers by ISBN into src/assets/books/<slug>.jpg (Plan.md §7.4).
// Skips existing files. Fails loudly on 404 or the 1×1 placeholder so a missing
// cover is noticed, never silently blank.
import { readdir, readFile, writeFile, mkdir, stat } from "node:fs/promises";
import path from "node:path";

const BOOKS = "src/content/books";
const OUT = "src/assets/books";
await mkdir(OUT, { recursive: true });

let failures = 0;
for (const file of (await readdir(BOOKS)).filter((f) => f.endsWith(".md"))) {
  const slug = file.replace(/\.md$/, "");
  const fm = (await readFile(path.join(BOOKS, file), "utf8")).match(/^---\n([\s\S]*?)\n---/)?.[1] ?? "";
  const isbn = fm.match(/^isbn:\s*"?(\d{13})"?\s*$/m)?.[1];
  if (!isbn) { console.log(`· ${slug}: no isbn, skipped`); continue; }
  const dest = path.join(OUT, `${slug}.jpg`);
  if (await stat(dest).then(() => true, () => false)) { console.log(`· ${slug}: cover exists`); continue; }
  const res = await fetch(`https://covers.openlibrary.org/b/isbn/${isbn}-L.jpg?default=false`);
  const bytes = res.ok ? Buffer.from(await res.arrayBuffer()) : null;
  if (!bytes || bytes.length < 2000) {
    console.error(`✗ ${slug}: no cover for ISBN ${isbn} (HTTP ${res.status}, ${bytes?.length ?? 0} bytes). Try another edition's ISBN.`);
    failures++; continue;
  }
  await writeFile(dest, bytes);
  console.log(`✓ ${slug}: ${bytes.length} bytes → ${dest}`);
}
process.exit(failures ? 1 : 0);
```

- [ ] **Step 2: Prove the failure path**

Create `src/content/books/_probe.md` with `---\ntitle: probe\nauthor: x\nisbn: "9798217336661"\nlanguage: en\ngenre: fiction\nstatus: reading\n---`. Run `npm run covers; echo exit=$?`.
Expected: `✗ _probe: no cover for ISBN 9798217336661 (HTTP 404 …)` and `exit=1`. Then `rm src/content/books/_probe.md`.

- [ ] **Step 3: Write the book files**

`src/content/books/dune.md`:
```md
---
title: Dune
author: Frank Herbert
isbn: "9780441013593"
cover: ../../assets/books/dune.jpg
language: en
genre: fiction
status: reading
started: "2026-08-01"
# Owner is on page 302 of 412.
progress: 73
pageCount: 412
---
```

`src/content/books/the-infinity-machine.md`:
```md
---
title: "The Infinity Machine: Demis Hassabis, DeepMind and the Quest for Superintelligence"
author: Sebastian Mallaby
# Hardcover ISBN — Open Library has this cover. The owner's copy is the US
# digital edition, ISBN 9798217336661, which has no cover there.
isbn: "9780593831847"
cover: ../../assets/books/the-infinity-machine.jpg
language: en
genre: nonfiction
status: reading
# TODO(owner): started date and progress. Omitted, not invented.
---
```

- [ ] **Step 4: Fetch, build**

Run: `npm run covers && ls -la src/assets/books && npm run build 2>&1 | grep -E "error|Complete"`
Expected: two `✓` lines, two jpg files (≈28 KB and ≈34 KB), `Complete!`.

- [ ] **Step 5: Prove the cover-missing failure is named**

Temporarily comment out the `cover:` line in `dune.md`, run `npm run build 2>&1 | grep -i "npm run covers" | head -1`.
Expected: `"Dune": has an isbn but no \`cover\` — run \`npm run covers\`…`. Restore the line.

- [ ] **Step 6: Commit**

```bash
cd .. && git add site && git commit -m "books: covers script, Dune ISBN + cover, The Infinity Machine replaces Zero to One

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 9: Reading List section (§7.4 UI)

**Files:**
- Create: `site/src/components/ProgressRing.astro`, `CurrentlyReading.astro`, `Shelf.astro`, `BookDetail.astro`, `ReadingList.astro`
- Modify: `site/src/pages/index.astro`
- Test: `tests/verify.mjs` check `reading`

**Interfaces:**
- Consumes: `books` collection.
- Produces: `<section id="personal">` with `.current` cards (one per `status: reading`, second slot reserved), `.shelf` per language→genre with `.shelf__track` of cover buttons (`<a href="#book-<slug>">`) or `.shelf__empty`, and `<article id="book-<slug>" class="book-detail">` panels shown via `:target`. `<ProgressRing value={n} />` renders `role="progressbar"`.

- [ ] **Step 1: Add the check**

```js
check("reading", async (browser) => {
  const { ctx, p } = await page(browser);
  const s = p.locator("section#personal");
  assert((await s.locator("h2").innerText()).toUpperCase().includes("READING LIST"), "heading");
  assert((await s.locator(".label").first().innerText()).match(/2 VOLUMES/i), "count must derive from data (2 volumes)");
  assert(await s.locator(".current__card").count() === 2, "expected two currently-reading cards");
  const ring = s.locator('[role="progressbar"]').first();
  assert(await ring.getAttribute("aria-valuenow") === "73", "Dune ring should be 73");
  assert(await s.locator(".current__card img").count() === 2, "current cards should show covers");
  assert(await s.locator(".shelf").count() === 2, "expected Fiction and Non-Fiction shelves");
  assert(await s.locator(".shelf__empty").count() === 2, "both shelves should render the empty state");
  assert((await s.innerText()).includes("Nothing finished yet"), "empty state copy");
  assert(await s.locator('.oak-scene[aria-label*="stove"], .oak-scene[aria-label*="reading"]').count() === 1, "reading-fire scene missing");
  await ctx.close();
});
```
Run: `node tests/verify.mjs reading` → `✗`.

- [ ] **Step 2: Write `ProgressRing.astro`**

```astro
---
interface Props { value: number; label: string; size?: number }
const { value, label, size = 64 } = Astro.props;
const r = (size - 8) / 2, c = 2 * Math.PI * r;
const pct = Math.max(0, Math.min(100, Math.round(value)));
---
<span class="ring" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow={pct} aria-label={label} style={`--size:${size}px`}>
  <svg viewBox={`0 0 ${size} ${size}`} width={size} height={size} aria-hidden="true">
    <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--line)" stroke-width="6" />
    <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--accent)" stroke-width="6" stroke-linecap="butt"
      stroke-dasharray={`${(c * pct) / 100} ${c}`} transform={`rotate(-90 ${size / 2} ${size / 2})`} />
  </svg>
  <span class="ring__text pixel">{pct}%</span>
</span>

<style>
  .ring { position: relative; display: inline-grid; place-items: center; width: var(--size); height: var(--size); flex: none; }
  .ring svg { position: absolute; inset: 0; }
  .ring__text { font-size: var(--fs-xs); letter-spacing: 0.05em; }
</style>
```

- [ ] **Step 3: Write `CurrentlyReading.astro`**

```astro
---
import { Image } from "astro:assets";
import type { CollectionEntry } from "astro:content";
import ProgressRing from "./ProgressRing.astro";
interface Props { books: CollectionEntry<"books">[] }
const { books } = Astro.props;
const fmt = (iso?: string) => iso ? new Date(iso + "T00:00:00").toLocaleDateString("en-US", { month: "short", year: "numeric" }) : undefined;
---
<div class="current">
  <p class="label">Currently reading</p>
  <ul class="current__grid">
    {books.map(({ data }) => (
      <li class="current__card">
        <div class="current__cover">
          {data.cover ? <Image src={data.cover} alt={`Cover of ${data.title}`} width={160} densities={[1, 2]} /> : <span class="current__nocover pixel">{data.title}</span>}
        </div>
        <div class="current__body">
          <h3 class="current__title">{data.title}</h3>
          <p class="current__author">{data.author}</p>
          {data.started && <p class="current__meta pixel">Started {fmt(data.started)}</p>}
          {data.note && <p class="current__note">{data.note}</p>}
        </div>
        {data.progress !== undefined && <ProgressRing value={data.progress} label={`${data.title}: ${data.progress}% read`} />}
      </li>
    ))}
    {books.length < 2 && <li class="current__card current__card--empty" aria-hidden="true"><span class="label">Second book</span></li>}
  </ul>
</div>

<style>
  .current { display: grid; gap: var(--space-s); }
  .current__grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-m); }
  .current__card {
    display: grid; grid-template-columns: 96px minmax(0, 1fr) auto; gap: var(--space-s); align-items: center;
    padding: var(--space-s); border: var(--border); border-radius: var(--radius); background: var(--plate);
  }
  .current__card--empty { border-style: dashed; background: transparent; place-items: center; min-height: 9rem; }
  .current__cover { aspect-ratio: 2 / 3; display: grid; place-items: center; background: var(--bg); border: var(--border); overflow: hidden; }
  .current__cover img { width: 100%; height: 100%; object-fit: cover; }
  .current__nocover { font-size: var(--fs-xs); padding: 0.4rem; text-align: center; }
  .current__body { display: grid; gap: 0.25rem; min-width: 0; }
  .current__title { font-size: var(--fs-base); text-wrap: pretty; }
  .current__author, .current__note { font-size: var(--fs-sm); color: var(--muted); }
  .current__meta { font-size: var(--fs-xs); letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }
  @media (max-width: 48rem) { .current__grid { grid-template-columns: 1fr; } .current__card--empty { display: none; } }
  @media (max-width: 24rem) { .current__card { grid-template-columns: 72px minmax(0, 1fr); } .current__card .ring { grid-column: 2; justify-self: start; } }
</style>
```

- [ ] **Step 4: Write `Shelf.astro` and `BookDetail.astro`**

`Shelf.astro`:
```astro
---
import { Image } from "astro:assets";
import type { CollectionEntry } from "astro:content";
interface Props { id: string; title: string; books: CollectionEntry<"books">[]; emptyHint?: string }
const { id, title, books, emptyHint } = Astro.props;
---
<div class="shelf" id={id}>
  <div class="shelf__head">
    <h3 class="shelf__title">{title}</h3>
    <p class="label">{books.length} {books.length === 1 ? "volume" : "volumes"}</p>
  </div>
  {books.length === 0 ? (
    <p class="shelf__empty">Nothing finished yet.{emptyHint && ` ${emptyHint}`}</p>
  ) : (
    <ul class="shelf__track scroller" tabindex="0" aria-label={`${title} shelf, scroll horizontally`}>
      {books.map(({ id: slug, data }) => (
        <li>
          <a class="shelf__book" href={`#book-${slug}`} aria-label={`${data.title} by ${data.author}, finished${data.rating ? `, rated ${data.rating} out of 5` : ""}`}>
            {data.cover ? <Image src={data.cover} alt="" width={140} densities={[1, 2]} /> : <span class="shelf__nocover pixel">{data.title}</span>}
          </a>
        </li>
      ))}
    </ul>
  )}
</div>

<style>
  .shelf { display: grid; gap: var(--space-s); padding-bottom: var(--space-m); border-bottom: 2px solid var(--ink); }
  .shelf__head { display: flex; align-items: baseline; gap: var(--space-s); }
  .shelf__title { text-transform: uppercase; letter-spacing: 0.08em; font-size: var(--fs-md); }
  .shelf__empty { color: var(--muted); padding: var(--space-m) 0; }
  .shelf__track { display: flex; gap: var(--space-s); padding: var(--space-xs) 0.25rem; }
  .shelf__book { display: block; width: 104px; aspect-ratio: 2 / 3; min-height: var(--tap-min); scroll-snap-align: start; border: var(--border); background: var(--plate); overflow: hidden; }
  .shelf__book img { width: 100%; height: 100%; object-fit: cover; }
  .shelf__book:hover { border-color: var(--accent); }
  .shelf__nocover { display: grid; place-items: center; height: 100%; padding: 0.4rem; font-size: var(--fs-xs); text-align: center; }
</style>
```

`BookDetail.astro`:
```astro
---
import { Image } from "astro:assets";
import type { CollectionEntry } from "astro:content";
interface Props { book: CollectionEntry<"books">; backHref: string }
const { book, backHref } = Astro.props;
const { data } = book;
const fmt = (iso?: string) => iso ? new Date(iso + "T00:00:00").toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" }) : undefined;
---
<article id={`book-${book.id}`} class="book-detail" aria-labelledby={`book-${book.id}-title`}>
  <div class="book-detail__cover">
    {data.cover && <Image src={data.cover} alt={`Cover of ${data.title}`} width={200} densities={[1, 2]} />}
  </div>
  <div class="book-detail__body">
    <h3 id={`book-${book.id}-title`}>{data.title}</h3>
    <p class="book-detail__author">{data.author}</p>
    <dl class="book-detail__facts">
      <dt>Status</dt><dd>{data.status === "reading" ? "Reading" : "Finished"}</dd>
      {data.started && <><dt>Started</dt><dd>{fmt(data.started)}</dd></>}
      {data.ended && <><dt>Finished</dt><dd>{fmt(data.ended)}</dd></>}
      {data.rating && <><dt>Rating</dt><dd><span aria-hidden="true">{"★".repeat(data.rating)}{"☆".repeat(5 - data.rating)}</span><span class="sr-only">Rated {data.rating} out of 5</span></dd></>}
    </dl>
    {(data.review ?? data.note) && <p class="book-detail__note">{data.review ?? data.note}</p>}
    <a class="btn" href={backHref}>Close</a>
  </div>
</article>

<style>
  /* Shown only when targeted by the URL hash — works with JS off, no focus trap. */
  .book-detail { display: none; }
  .book-detail:target { display: grid; grid-template-columns: 140px minmax(0, 1fr); gap: var(--space-m); padding: var(--space-m); margin-top: var(--space-m); border: var(--border); background: var(--plate); scroll-margin-top: 5rem; }
  .book-detail__cover img { width: 100%; border: var(--border); }
  .book-detail__body { display: grid; gap: var(--space-xs); align-content: start; }
  .book-detail__author { color: var(--muted); }
  .book-detail__facts { display: grid; grid-template-columns: max-content 1fr; gap: 0.3rem var(--space-s); margin: 0; }
  .book-detail__facts dt { font-family: var(--font-pixel); font-size: var(--fs-xs); letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }
  .book-detail__facts dd { margin: 0; }
  @media (max-width: 40rem) { .book-detail:target { grid-template-columns: 1fr; } .book-detail__cover { max-width: 140px; } }
</style>
```

- [ ] **Step 5: Write `ReadingList.astro`**

```astro
---
import { getCollection } from "astro:content";
import AnimatedScene from "./AnimatedScene.astro";
import SectionHead from "./SectionHead.astro";
import CurrentlyReading from "./CurrentlyReading.astro";
import Shelf from "./Shelf.astro";
import BookDetail from "./BookDetail.astro";

const books = await getCollection("books");
const reading = books.filter((b) => b.data.status === "reading").sort((a, b) => (b.data.progress ?? 0) - (a.data.progress ?? 0));
const finished = books.filter((b) => b.data.status === "finished").sort((a, b) => (b.data.ended ?? "").localeCompare(a.data.ended ?? ""));
const count = `${books.length} ${books.length === 1 ? "volume" : "volumes"} · ${finished.length} finished`;
const lead = reading[0];
const hint = lead?.data.progress !== undefined ? `${lead.data.title} is at ${lead.data.progress}%.` : undefined;

// Language → genre; Burmese shelves appear only when data exists (§7.4).
const shelves = [
  { id: "shelf-fiction", title: "Fiction", books: finished.filter((b) => b.data.language === "en" && b.data.genre === "fiction") },
  { id: "shelf-nonfiction", title: "Non-Fiction", books: finished.filter((b) => b.data.language === "en" && b.data.genre === "nonfiction") },
];
---
<section id="personal" class="section" aria-labelledby="personal-title">
  <div class="wrap reading">
    <AnimatedScene scene="reading-fire" class="reading__scene" />
    <div class="reading__body">
      <SectionHead id="personal" title="Reading List" label={count} />
      <CurrentlyReading books={reading} />
      <div class="reading__shelves">
        {shelves.map((s) => <Shelf id={s.id} title={s.title} books={s.books} emptyHint={hint} />)}
      </div>
      {finished.map((b) => <BookDetail book={b} backHref={`#${b.data.genre === "fiction" ? "shelf-fiction" : "shelf-nonfiction"}`} />)}
    </div>
  </div>
</section>

<style>
  .reading { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: var(--space-l); align-items: start; }
  .reading__body { display: grid; gap: var(--space-l); min-width: 0; }
  .reading__shelves { display: grid; gap: var(--space-l); }
  @media (max-width: 48rem) { .reading { grid-template-columns: 1fr; } }
</style>
```

- [ ] **Step 6: Wire, build, verify**

In `index.astro` import `ReadingList`, render after `<Projects />`, exclude `"personal"` from `rest`.
Run: `npm run check 2>&1 | tail -2 && npm run build 2>&1 | grep -E "error|Complete" && node tests/verify.mjs reading overflow nojs`
Expected: `0 errors`, all `✓`. If `overflow` fails at 320, the long Infinity Machine title in `.current__title` needs `overflow-wrap: anywhere`.

- [ ] **Step 7: Commit**

```bash
cd .. && git add site && git commit -m "reading: currently-reading cards with progress rings, cover shelves with empty state, :target detail panels, reading-fire scene

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 10: Contact card (§7.5)

**Files:**
- Create: `site/src/components/ContactCard.astro`
- Modify: `site/src/pages/index.astro` (final assembly, remove skeleton loop)
- Test: `tests/verify.mjs` checks `contact`, `contact-nojs`

**Interfaces:**
- Consumes: `site`, `contactRows` (Task 2); `/contact.vcf` endpoint (kept).
- Produces: `<section id="contact">` with `.bizcard`, rows as `<a>`; `button[data-copy]` beside the email; `[data-copy-status]` `aria-live` region.

- [ ] **Step 1: Add the checks**

```js
check("contact", async (browser) => {
  const { ctx, p } = await page(browser);
  const s = p.locator("section#contact");
  for (const href of ["https://mrshine.dev", "mailto:oaksoekhant182209@gmail.com", "https://www.linkedin.com/in/oak-soe-khant-350252362", "https://github.com/Mr-Shine09", "/contact.vcf"]) {
    assert(await s.locator(`a[href="${href}"]`).count() === 1, `contact row ${href} missing`);
  }
  assert((await s.innerText()).includes("oaksoekhant182209@gmail.com"), "email must be visible text");
  await ctx.grantPermissions(["clipboard-read", "clipboard-write"]);
  await s.locator("[data-copy]").click();
  await p.waitForTimeout(200);
  assert((await s.locator("[data-copy-status]").innerText()).toLowerCase().includes("copied"), "copy button must announce success");
  assert(await s.locator("form").count() === 0, "no contact form");
  assert(await s.locator(".oak-scene").count() === 0, "no mascot in contact");
  const me = await s.locator('a[href="https://github.com/Mr-Shine09"]').getAttribute("rel");
  assert(me && me.includes("me"), 'social links need rel="me"');
  await ctx.close();
});

check("contact-nojs", async (browser) => {
  const { ctx, p } = await page(browser, { javaScriptEnabled: false });
  assert(await p.locator("section#contact a[href^='mailto:']").count() === 1, "no-JS: email link");
  assert(!(await p.locator("section#contact [data-copy]").isVisible()), "no-JS: copy button must be hidden");
  await ctx.close();
});
```
Run: `node tests/verify.mjs contact contact-nojs` → `✗`.

- [ ] **Step 2: Write `ContactCard.astro`**

```astro
---
import { site, contactRows } from "../data/site";
import SectionHead from "./SectionHead.astro";
const icons: Record<string, string> = { Website: "⌂", Email: "✉", LinkedIn: "in", GitHub: "◉", "Save contact": "▤" };
---
<section id="contact" class="section" aria-labelledby="contact-title">
  <div class="wrap">
    <SectionHead id="contact" title="Contact" />
    <div class="bizcard">
      <header class="bizcard__head">
        <div>
          <p class="bizcard__name pixel">{site.name.toUpperCase()}</p>
          <p class="label">{site.shortRole}</p>
        </div>
        <img class="bizcard__mark pixelated" src="/favicon-48.png" alt="" width="48" height="48" />
      </header>
      <ul class="bizcard__rows">
        {contactRows.map((row) => (
          <li class="bizcard__row">
            <span class="bizcard__icon pixel" aria-hidden="true">{icons[row.label] ?? "·"}</span>
            <span class="bizcard__label label">{row.label}</span>
            <a class="bizcard__value" href={row.href} rel={row.me ? "me" : row.href.startsWith("http") ? "noopener" : undefined}>{row.text}</a>
            {row.copy && (
              <button type="button" class="bizcard__copy btn" data-copy={row.text} aria-label="Copy email address" hidden>Copy</button>
            )}
          </li>
        ))}
      </ul>
      <p class="bizcard__status label" data-copy-status aria-live="polite"></p>
    </div>
  </div>
</section>

<style>
  .bizcard { max-width: 36rem; margin-inline: auto; padding: var(--space-m); border: 2px solid var(--ink); border-radius: var(--radius); background: var(--plate); box-shadow: 6px 6px 0 var(--shadow); }
  .bizcard__head { display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-s); padding-bottom: var(--space-s); border-bottom: 2px solid var(--ink); }
  .bizcard__name { font-size: var(--fs-md); letter-spacing: 0.04em; margin: 0 0 0.2rem; }
  .bizcard__rows { display: grid; gap: 0.25rem; margin-top: var(--space-s); }
  .bizcard__row { display: grid; grid-template-columns: 2rem 7rem minmax(0, 1fr) auto; align-items: center; gap: var(--space-xs); min-height: var(--tap-min); }
  .bizcard__icon { color: var(--accent); font-size: var(--fs-base); }
  .bizcard__value { overflow-wrap: anywhere; min-height: var(--tap-min); display: inline-flex; align-items: center; }
  .bizcard__copy { padding: 0.3rem 0.6rem; font-size: var(--fs-xs); }
  .bizcard__status { min-height: 1.2em; margin-top: var(--space-xs); }
  @media (max-width: 40rem) {
    .bizcard__row { grid-template-columns: 2rem minmax(0, 1fr) auto; }
    .bizcard__label { grid-column: 2; }
    .bizcard__value { grid-column: 2; }
    .bizcard__copy { grid-column: 3; grid-row: 1 / span 2; }
  }
</style>

<script>
  const status = document.querySelector<HTMLElement>("[data-copy-status]");
  for (const btn of document.querySelectorAll<HTMLButtonElement>("[data-copy]")) {
    btn.hidden = false; // JS is here; the button can earn its place.
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.copy ?? "");
        if (status) status.textContent = "Copied to clipboard.";
      } catch {
        if (status) status.textContent = "Copy failed — select the address instead.";
      }
      setTimeout(() => { if (status) status.textContent = ""; }, 3000);
    });
  }
</script>
```

- [ ] **Step 3: Final `index.astro`**

```astro
---
import Base from "../layouts/Base.astro";
import Hero from "../components/Hero.astro";
import Highlights from "../components/Highlights.astro";
import Projects from "../components/Projects.astro";
import ReadingList from "../components/ReadingList.astro";
import ContactCard from "../components/ContactCard.astro";
---
<Base>
  <Hero />
  <Highlights />
  <Projects />
  <ReadingList />
  <ContactCard />
</Base>
```
`SectionHead` and `sections` from `nav.ts` are still used by the components and TopBar respectively — `nav.ts` remains the single source of the anchor list; confirm each component's `id` matches it (the `sections` check enforces this).

- [ ] **Step 4: Build, run everything**

Run: `npm run check 2>&1 | tail -2 && npm run build 2>&1 | grep -E "WARN|error|Complete" && node tests/verify.mjs`
Expected: `0 errors`, no `WARN`, every check `✓`.

- [ ] **Step 5: Commit**

```bash
cd .. && git add site && git commit -m "contact: business-card block with website, email + copy, LinkedIn, GitHub, vCard; final page assembly

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 11: Remaining acceptance checks — focus, tap targets, theme, fonts, third-party

**Files:**
- Modify: `site/tests/verify.mjs`
- Modify: whichever component fails (expected: none, or small CSS fixes)

**Interfaces:** none new.

- [ ] **Step 1: Add the checks**

```js
check("focus", async (browser) => {
  const { ctx, p } = await page(browser);
  const total = await p.locator("a, button, [tabindex='0'], summary").count();
  const missing = [];
  await p.keyboard.press("Tab"); // skip link
  for (let i = 0; i < total; i++) {
    const info = await p.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body) return null;
      const cs = getComputedStyle(el);
      return { tag: el.tagName + (el.getAttribute("href") ? `[${el.getAttribute("href")}]` : ""), outline: cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0 };
    });
    if (info && !info.outline) missing.push(info.tag);
    await p.keyboard.press("Tab");
  }
  assert(missing.length === 0, `no visible focus on: ${[...new Set(missing)].join(", ")}`);
  await ctx.close();
});

check("tap-targets", async (browser) => {
  const { ctx, p } = await page(browser, { viewport: { width: 375, height: 700 } });
  await p.evaluate(() => document.documentElement.classList.add("js"));
  const small = await p.$$eval("a, button, summary", (els) =>
    els.filter((e) => { const r = e.getBoundingClientRect(); const vis = r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== "hidden"; return vis && (r.width < 44 || r.height < 44); })
       .map((e) => `${e.tagName}${e.className ? "." + e.className.split(" ")[0] : ""} ${Math.round(e.getBoundingClientRect().width)}×${Math.round(e.getBoundingClientRect().height)}`));
  assert(small.length === 0, `tap targets under 44px: ${small.join(", ")}`);
  await ctx.close();
});

check("theme", async (browser) => {
  const { ctx, p } = await page(browser);
  await p.locator("[data-theme-toggle]").click();
  assert((await p.getAttribute("html", "data-theme")) === "dark", "toggle should switch to dark");
  await p.reload({ waitUntil: "networkidle" });
  assert((await p.getAttribute("html", "data-theme")) === "dark", "theme should persist across reload");
  const bg = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
  assert(bg === "rgb(21, 14, 43)", `dark --bg should be #150E2B, got ${bg}`);
  await ctx.close();
});

check("fonts", async (browser) => {
  const { ctx, p } = await page(browser);
  const loaded = await p.evaluate(async () => { await document.fonts.ready; return [...document.fonts].filter((f) => f.status === "loaded").map((f) => f.family.replace(/"/g, "")); });
  assert(loaded.some((f) => /Geist Pixel/.test(f)), `Geist Pixel not loaded: ${loaded.join(", ")}`);
  assert(loaded.some((f) => /Geist Sans/.test(f)), `Geist Sans not loaded: ${loaded.join(", ")}`);
  const synth = await p.evaluate(() => getComputedStyle(document.documentElement).fontSynthesis);
  assert(synth === "none", `font-synthesis is ${synth}`);
  const heavy = await p.$$eval("body *", (els) => els.filter((e) => parseInt(getComputedStyle(e).fontWeight) >= 600 && e.textContent.trim()).length);
  assert(heavy === 0, `${heavy} elements render at weight ≥600 (faux bold risk)`);
  await ctx.close();
});

check("third-party", async (browser) => {
  const ctx = await browser.newContext();
  const p = await ctx.newPage();
  const foreign = [];
  p.on("request", (r) => { const u = new URL(r.url()); if (u.origin !== new URL(BASE).origin) foreign.push(r.url()); });
  await p.goto(BASE, { waitUntil: "networkidle" });
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(800);
  assert(foreign.length === 0, `third-party requests: ${foreign.slice(0, 5).join(", ")}`);
  await ctx.close();
});
```

- [ ] **Step 2: Run everything**

Run: `node tests/verify.mjs`
Expected: all `✓`. Likely fixes if not:
- `tap-targets` flags `.topbar__nav a` on 375: add `min-width: 44px; justify-content: center` to those links.
- `tap-targets` flags `.shelf__book`: none exist at launch (empty shelves); fine.
- `focus` flags `.card`: cards have `tabindex="0"` and inherit the global rule; if the outline is clipped by the scroller's `mask-image`, add `padding-block: 6px` to `.slider__track`.
- `fonts` flags weight ≥600: search components for `font-weight` and remove.

- [ ] **Step 3: Commit**

```bash
cd .. && git add site && git commit -m "verify: focus, tap-target, theme, fonts, third-party checks; fixes

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 12: Screenshots, README update, cleanup of stale comments

**Files:**
- Create: `site/tests/screenshots.mjs`
- Modify: `site/README.md` (covers script line), `site/src/components/ThemeToggle.astro:1-4` (comment), `site/src/pages/contact.vcf.ts` (no change), `Plan.md` §11 (tick the checklist)

- [ ] **Step 1: Screenshot script for a human look**

`site/tests/screenshots.mjs`:
```js
import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
const BASE = process.env.PREVIEW_URL ?? "http://localhost:4321/";
await mkdir("tests/shots", { recursive: true });
const browser = await chromium.launch();
for (const theme of ["light", "dark"]) for (const width of [375, 1280]) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: theme });
  const p = await ctx.newPage();
  await p.goto(BASE, { waitUntil: "networkidle" });
  await p.screenshot({ path: `tests/shots/${theme}-${width}.png`, fullPage: true });
  await ctx.close();
}
await browser.close();
console.log("wrote tests/shots/*.png");
```
Run: `node tests/screenshots.mjs` and open the four PNGs. Look for: hero fits above the fold at 375; slider centre card is largest at 1280; empty shelves read as intentional; card is legible in dark. Fix anything wrong, re-run `node tests/verify.mjs`.

Add `tests/shots/` to `site/.gitignore`.

- [ ] **Step 2: Repo docs**

In `site/README.md`, remove "(added in the build session)" from the `npm run covers` row and add rows for `npm run check`, `npm run verify` (needs `npm run preview` running). In `Plan.md` §11, change each `N.` item to `- [x]`. In `ThemeToggle.astro` the header comment already matches Base.astro's bootstrap; leave it.

- [ ] **Step 3: Grep for stale references**

Run from repo root: `grep -rn "HANDOFF\|w-phrases\|BusinessCard\|NavPill\|spine" site/src site/astro.config.mjs | grep -v node_modules`
Expected: no output. Fix any hit (comments included).

- [ ] **Step 4: Final full run and commit**

```bash
cd site && npm run check 2>&1 | tail -2 && npm run build 2>&1 | grep -E "WARN|error|hint|Complete" && node tests/verify.mjs && cd .. && git add -A && git commit -m "rebuild complete: screenshots script, docs, stale-reference sweep

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```
Expected: `0 errors, 0 warnings, 0 hints`; build `Complete!` with no `WARN`; every check `✓`.

---

### Task 13: Publish — GitHub repo and Cloudflare Pages

**Files:** none in the tree. Requires the owner's Cloudflare login (interactive).

- [ ] **Step 1: Create the public GitHub repo and push** (owner approved public, 2 Sep 2026)

From the repo root:
```bash
gh repo create Mr-Shine09/mrshine.dev --public --source=. --remote=origin --description "Oak Soe Khant's portfolio — mrshine.dev" --push
git remote -v && gh repo view --web >/dev/null 2>&1 || true
```
Expected: `origin` set; `main` pushed.

- [ ] **Step 2: Cloudflare login (owner runs this)**

The owner types in the prompt: `! cd site && npx wrangler login` — a browser opens, they approve. Then: `npx wrangler whoami` shows the account.

- [ ] **Step 3: Create the Pages project and do a first direct deploy**

```bash
cd site && npm run build && npx wrangler pages project create mrshine-dev --production-branch main && npx wrangler pages deploy dist --project-name mrshine-dev --branch main
```
Expected: a `https://mrshine-dev.pages.dev` URL. Open it; run `PREVIEW_URL=https://mrshine-dev.pages.dev/ node tests/verify.mjs sections overflow third-party`.

- [ ] **Step 4: Attach the domain**

```bash
ACCOUNT=$(npx wrangler whoami 2>/dev/null | grep -oE '[0-9a-f]{32}' | head -1)
for host in mrshine.dev www.mrshine.dev; do
  npx wrangler pages project list >/dev/null  # ensures auth
  curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT/pages/projects/mrshine-dev/domains" \
    -H "Authorization: Bearer $(cat ~/.wrangler/config/default.toml 2>/dev/null | grep -oE 'oauth_token = "[^"]+"' | cut -d'"' -f2)" \
    -H "Content-Type: application/json" --data "{\"name\":\"$host\"}"
done
```
If the token extraction fails, do this step in the dashboard: Workers & Pages → mrshine-dev → Custom domains → add `mrshine.dev`, then `www.mrshine.dev` (Plan.md §14.4). Then add the "Redirect from WWW to Root" rule template under the zone's Rules.

- [ ] **Step 5: Connect Git for automatic deploys (dashboard only)**

Workers & Pages → mrshine-dev → Settings → Builds & deployments → Connect to Git → `Mr-Shine09/mrshine.dev`, root directory `site`, build `npm run build`, output `dist`, env `NODE_VERSION=22`. Push an empty commit to confirm it deploys: `git commit --allow-empty -m "ci: trigger Pages build" && git push`.

- [ ] **Step 6: Verify the live site**

```bash
curl -sI https://mrshine.dev | head -3; curl -sI http://www.mrshine.dev | grep -i location
PREVIEW_URL=https://mrshine.dev/ node site/tests/verify.mjs
```
Expected: `HTTP/2 200`, `location: https://mrshine.dev/`, all checks `✓`.

---

## Self-review against `Plan.md`

| Spec | Task |
|---|---|
| §2 non-negotiables | global.css (2, 3), AnimatedScene untouched player (3), runner CSS hide (5), no-JS checks (7, 10), focus/tap (11) |
| §3 stack, fonts local only | 1, 11 `third-party` |
| §4 type, 4px scale, 16px floor | 1, 2 |
| §4.3 Burmese named failure | 2 (`language: my` issue) |
| §5 tokens, toggle, no-JS system theme | 2 (`<noscript>` mirror), 11 `theme` |
| §6 responsive rules | overflow check every task; phone rules in each component |
| §7.0 top bar | 2 |
| §7.1 hero incl. lead + closing, bordered portrait, borderless mascot | 4 |
| §7.2 highlights, trophy once, coming-soon threshold | 6 |
| §7.3 slider, order, contain, Echo credits, no-JS repo link | 7 |
| §7.4 current cards, rings, cover shelves, empty state, `:target` detail, covers script | 8, 9 |
| §7.5 card rows, copy button, rel=me, vCard | 10 |
| §7.6 runner | 5 |
| §7.7 scene player | 3 |
| §8 schemas + named failures | 2, 6, 8 |
| §10 acceptance | harness across 2–11; Lighthouse is manual (open DevTools → Lighthouse on the live site, Task 13) |
| §11 checklist | tasks map 1:1; Plan.md ticked in 12 |
| §14 deploy | 13 |

Placeholder scan: the only `TODO(owner)` strings are inside content files where the spec requires omission, not invention. Type consistency: `sections`/`SectionId` (Task 2) used by TopBar and index; `scale` props match between Tasks 3–7; `contactRows` fields `copy`/`me` match Task 10's template; check names in the harness are unique.
