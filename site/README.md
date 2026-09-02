# Oak's portfolio — site

Astro site for oaksoekhant's personal portfolio: a single scrolling page with
About, Highlights, Projects, Reading List, and Contact. The full specification
is `../Plan.md`; read it before changing anything.

## Commands

| Command | Action |
|---|---|
| `npm install` | Install dependencies (Node ≥ 22.12) |
| `npm run dev` | Dev server at `localhost:4321` |
| `npm run build` | Production build to `./dist/` (gitignored) |
| `npm run preview` | Preview the production build |
| `npm run covers` | Fetch Open Library covers for books with an `isbn` |
| `npm run check` | Type-check the Astro project |
| `npm run verify` | Run the Playwright acceptance harness (needs `npm run preview -- --port 4321` running) |

## Where content lives

- `src/data/site.ts` — name, role, socials, résumé and site URL. The contact card and `contact.vcf` both read it.
- `src/content/achievements/` — one markdown file per highlight.
- `src/content/projects/` — one file per project; images in `src/assets/projects/`.
- `src/content/books/` — one file per book; covers in `src/assets/books/`.
- `public/assets/animation/` — the canonical mascot animation tree (see its `ANIMATION_ASSETS.md`).

Update recipes are in `Plan.md` §13.

## Updating books

Adding or updating a book (Plan.md §7.4):

1. Create `src/content/books/<slug>.md` with the frontmatter the schema in
   `src/content.config.ts` requires (Plan.md §8).
2. If it has an `isbn`, run `npm run covers`. The script fetches
   `https://covers.openlibrary.org/b/isbn/<ISBN>-L.jpg` into
   `src/assets/books/<slug>.jpg`, skips files that already exist, and **fails
   loudly on a 404 or a 1×1 placeholder** so a missing cover is noticed rather
   than silently blank. Then add `cover: ../../assets/books/<slug>.jpg`.
3. Commit and push. Cloudflare redeploys.

Finishing a book: change `status` to `finished`, add `ended`, `rating`, and
`review`, remove `progress`, push. It moves from Currently Reading to its
shelf on the next build.

## Deploy

Cloudflare Pages, connected to this repo (Plan.md §14.3). Every push to `main`
rebuilds and redeploys; pull requests get preview URLs.

| Field | Value |
|---|---|
| Production branch | `main` |
| Framework preset | Astro |
| Root directory | `site` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Environment variable | `NODE_VERSION` = `22` |

`NODE_VERSION=22` is not optional: Astro 7 needs Node ≥ 22.12 and the Pages
default may be older.
