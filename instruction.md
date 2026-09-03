# How to change things on mrshine.dev

Everything on the site is a file in this repo. You edit a file, commit, push to
`main`, and Cloudflare Pages rebuilds and publishes it in about a minute. No
dashboard needed.

```
cd "~/Oak's Portfolio Website"
git add -A
git commit -m "books: finished Dune"
git push
```

To preview locally before pushing:

```
cd site
npm run dev            # http://localhost:4321, live-reloads as you edit
```

If a build fails, the error names the file and field. Fix it and push again.

---

## Books

Files live in `site/src/content/books/`, one markdown file per book. The
filename is the book's id (`dune.md`, `the-infinity-machine.md`).

### Update reading progress

Open the book's file and change `progress` (0–100). Example, `dune.md`:

```yaml
progress: 80
```

### Finish a book

Change `status`, add `ended`, `rating` (1–5) and a short `review`, and remove
`progress`. The book moves from **Currently Reading** to its shelf.

```yaml
status: finished
ended: "2026-10-01"
rating: 5
review: A slow start, then it does not let go.
```

Do not leave `progress` on a finished book, or `rating`/`review` on an
unfinished one — the build refuses and tells you which file.

### Add a book

1. Create `site/src/content/books/<slug>.md`. Copy this and fill it in:

```yaml
---
title: Book Title
author: Author Name
isbn: "9780000000000"          # ISBN-13, digits only. Find it on the copyright page or Amazon.
cover: ../../assets/books/<slug>.jpg
language: en
genre: fiction                  # or nonfiction
status: reading                 # or finished
started: "2026-09-10"
progress: 5
note: One line on why you picked it up.   # optional
pageCount: 320                  # optional
---
```

2. Fetch the cover (uses the ISBN, saves to `site/src/assets/books/<slug>.jpg`):

```
cd site && npm run covers
```

If it prints `✗ no cover for ISBN`, try the ISBN of another edition (hardcover
often has one when the e-book does not). The `cover:` line must point at the
downloaded file.

3. Commit and push.

### Remove a book

Delete its file in `site/src/content/books/` and its cover in
`site/src/assets/books/`. Commit and push.

### Where the two shelves come from

Fiction and Non-Fiction shelves show **finished** books only, grouped by
`genre`. Books with `status: reading` appear in Currently Reading. Counts
("2 volumes · 0 finished") are computed; do not edit them.

---

## Highlights (awards and hackathons)

Files live in `site/src/content/achievements/`, one per entry.

### Add an award or contest result

```yaml
---
title: 2nd — Some Hackathon 2027
org: Who ran it
year: "2027"
kind: competition        # competition | award | hackathon | other
order: 1                 # lower shows first
---
```

`kind: hackathon` goes in the **Hackathons** column; everything else goes in
**Awards & contests**. `year` is optional. `link` (a URL) is optional.

The line "More achievements coming soon." disappears on its own once the awards
column has three entries. To change that threshold, edit `COMING_SOON_BELOW`
in `site/src/components/Highlights.astro`.

### Remove or reorder

Delete the file, or change `order`.

---

## Projects

Files live in `site/src/content/projects/`, one per card. Images live in
`site/src/assets/projects/`.

### Add a project

```yaml
---
title: Project Name
order: 5
year: "2027"
stack: ["Python", "Flask"]
summary: One sentence that fits on a card.
collaborators: []                       # names or handles; leave [] if solo
builtAt: "Some Hackathon 2027"          # optional
links:
  github: https://github.com/Mr-Shine09/project
  devpost: https://devpost.com/software/...    # optional
image: ../../assets/projects/project-hero.png
imageAlt: What the picture shows, in one sentence.
draft: false
---

Optional longer text about what was hard. Not shown on the card today.
```

Every `image` needs an `imageAlt`, or the build fails.

### Stack chips with icons

Chips get a Devicon logo when the label matches the map in
`site/src/components/ProjectCard.astro` (look for `const devicon`). To add one:
download the SVG from https://devicon.dev into `site/src/icons/devicon/<name>.svg`
and add `"Label": "<name>"` to that map.

### Hide a project without deleting it

Set `draft: true`.

### Change the order

Edit `order`. Lower numbers appear first in the slider.

---

## Text on the site

Most words live in one file: `site/src/data/site.ts`.

| What | Field |
|---|---|
| Name | `name` |
| Role line under the name | `shortRole` |
| "What's up everyone!!!" lead | `lead` |
| Tagline | `tagline` |
| Closing line ("Leveraging artificial intelligence…") | `closing` |
| Email, GitHub, LinkedIn, Instagram, Facebook, Devpost | `socials` |
| Résumé link | `resumeUrl` (file at `site/public/resume.pdf`) |
| Site URL | `url` |
| Search-engine description | `seo.description` |

Which contact rows show, and their order, is `contactRows` at the bottom of
the same file. Instagram, Facebook and Devpost are in the downloadable vCard
but not on the card by default.

### Highlighted phrases

The coral highlights in the hero are listed in `site/src/components/Hero.astro`
as `leadMarks` and `taglineMarks`. Add or remove exact phrases there; the text
itself does not change.

### Section names in the nav

`site/src/data/nav.ts`. The `id` values are used as anchors and by the tests,
so change only the `label`.

### The band before the Reading List

The "Reader in progress." line is in `site/src/pages/index.astro` inside
`<Band>`.

---

## Replace the résumé

Overwrite `site/public/resume.pdf`. Same filename, so nothing else changes.

## Replace the portrait

Overwrite `site/src/assets/photos/portrait.jpg`. Keep it roughly square.

---

## Colours and fonts

- Colours: `site/src/styles/tokens.css`. Light values under `:root`, dark
  under `[data-theme="dark"]`. If you change `--accent`, `--muted` or `--bg`,
  re-check contrast (the text must stay ≥ 4.5:1 on `--bg` and on `--plate`).
- Fonts: Geist Pixel is only for big display text; Geist Sans is everything
  else. To swap a font, put the woff2 in `site/src/assets/fonts/` and edit
  `site/astro.config.mjs`.

---

## Mascot animations

The animation files live in `site/public/assets/animation/`. Which scene shows
where, and its size, is set in the component that renders it:

| Scene | Component | Size prop |
|---|---|---|
| Waving hero | `site/src/components/Hero.astro` → `<HeroWelcome scale={1.5} />` | `1`, `1.5`, `2` |
| Trophy | `site/src/components/Highlights.astro` | default `0.75` |
| Workbench | `site/src/components/Projects.astro` → `scale={0.5}` | `0.5`, `0.75`, `1` |
| Reading by the fire | `site/src/components/ReadingList.astro` → `scale={0.5}` | `0.5`, `0.75`, `1` |
| Runner along the bottom | `site/src/components/BottomRunner.astro` (CSS `width`/`height`) | |

Never recolour the scene images. If you add a new scene, run
`python3 site/scripts/fix-scene-outlines.py` afterwards so it sits cleanly on
dark backgrounds.

---

## Check everything before pushing (optional)

```
cd site
npm run check                      # type check
npm run build                      # production build
npm run preview -- --port 4321     # in another terminal
npm run verify                     # 24 automated checks against the preview
```

`npm run verify` needs the preview running. It checks layout at four widths,
keyboard focus, tap sizes, dark mode, no-JS, reduced motion, fonts, and that
no request leaves the site.

---

## Where the full design decisions live

`Plan.md` at the repo root is the specification: why each thing is the way it
is, the acceptance criteria, and the deploy setup. Read it before changing the
structure of the site.
