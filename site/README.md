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
| `npm run covers` | Fetch Open Library covers for books with an `isbn` (added in the build session) |

## Where content lives

- `src/data/site.ts` — name, role, socials, résumé and site URL. The contact card and `contact.vcf` both read it.
- `src/content/achievements/` — one markdown file per highlight.
- `src/content/projects/` — one file per project; images in `src/assets/projects/`.
- `src/content/books/` — one file per book; covers in `src/assets/books/`.
- `public/assets/animation/` — the canonical mascot animation tree (see its `ANIMATION_ASSETS.md`).

Update recipes are in `Plan.md` §13.
