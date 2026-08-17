# Reading List — content spec

**Written:** 16 Aug 2026
**For:** the build session that implements the site
**Status:** structure locked, two books supplied, dates outstanding

Architecture context is in `docs/about-me.md` §0 and `ledger.md` #18–#28. This
page is one of the four home-grid tiles.

---

## 1. What this page is

A **bookshelf**, not a list. Books stand as rendered spines at varying heights
and widths, the way they do on a real shelf. Clicking a spine opens its detail.

**Layout reference: `carollia-library.lovable.app`** — structural pattern only.
What is borrowed: the serif shelf title with a letterspaced mono count beneath
it, and the row of three-dimensional spines. What is **not** borrowed: her
palette, her genre pills, and her scale (97 books to your 2).

The About page calls the owner a **"Reader in progress."** This page has to be
consistent with that. It is a shelf that is visibly starting, not a trophy case,
and it should be built so that being small is not a defect.

---

## 2. Structure

Three levels of nesting, in this order:

```
Reading List
├── English
│   ├── Non-fiction   ← shelf
│   └── Fiction       ← shelf
└── Burmese
    ├── Non-fiction   ← shelf
    └── Fiction       ← shelf
```

**Status is not a shelf.** A real shelf is organised by subject, not by whether
you've finished the book. Status (`reading` · `finished` · `want`) is shown as a
marker on the individual spine and in its detail panel.

> This supersedes the earlier decision in this session to use
> *Reading now · Finished · Want to read* as the three shelves. Language and
> genre became the organising axes once Burmese books entered the picture.

**Empty shelves do not render.** With two books, both English, the two Burmese
shelves have nothing on them — and an empty rack looks broken, not aspirational.
A shelf appears the moment it holds a book. Same pattern as `draft: true` on the
projects (ledger #26), and it means the page grows without a template change.

**Page header:** serif title, letterspaced mono count beneath — `2 VOLUMES`
today. The count is derived from the data, never hardcoded.

**No genre filter pills.** The four shelves plus the search box are already two
controls; pills would be a redundant third. The reference site has them because
she has 97 books across seven genres.

---

## 3. The spines

Each book renders as an **upright spine**: its own width, height, colour, and
rotated title.

- **Colours come from the locked 12-colour mascot palette** (ledger #9). Assign
  so no two adjacent spines share a colour. The shelf then matches the rest of
  the site with nothing invented — which is the same argument that produced the
  palette in the first place.
- **Width and height vary per book.** Derive width from page count where known,
  otherwise a default with slight per-book variation. Uniform spines read as a
  bar chart, not a shelf.
- **Status marker on the spine** for anything currently being read — a small
  band or dot, not a text label. Text on a spine is already tight.
- Slight rotation on one or two spines is what makes the reference shelf look
  real. Keep it to a couple, and never let a leaning spine overlap its
  neighbour's tap target.

### Accessibility requirements

These are not optional and they are the easiest part of this page to get wrong:

- **The rotated title must not be the accessible name.** Each spine is a link or
  button whose accessible name reads normally: *"Dune by Frank Herbert,
  currently reading."* Rotate the visual text with a CSS transform; do not use
  a technique that breaks text selection or screen-reader order.
- **Contrast:** the title on each spine must meet contrast against that spine's
  colour. Some palette colours will need light text and some dark — decide per
  colour, do not use one text colour for all twelve.
- **Tap target ≥44px.** A narrow spine is narrower than 44px. Give each spine a
  transparent hit area that meets the minimum even when the visible spine
  doesn't.
- **Keyboard:** spines are in tab order left to right, visible focus state,
  Enter opens the detail.

---

## 4. Book detail

Opens on clicking a spine. Contents, in order:

| Field | Notes |
|---|---|
| Title · Author | Always present |
| Status | Reading now · Finished · Want to read |
| Started | Date |
| Ended | Date — **absent while a book is unfinished** |
| Progress | 0–100, shown only while status is `reading` |
| Rating | 5 stars — **absent until finished** |
| Review | Short, a few sentences — **absent until finished** |

**Rating, ended date, and review are optional by design.** Both current books
are in progress, so neither has any of the three. The detail panel must look
complete without them, not like a form with blank rows. A book being read shows
started date and progress; that is the whole panel and it is enough.

**Star rating accessibility:** stars are decorative. The accessible text is
`"Rated 4 out of 5"`, not five star glyphs read aloud one at a time.

---

## 5. Search

A single search box filtering **title and author** across all shelves at once.

- **Client-side.** The whole book list is already in the page; no index, no
  fetch, no dependency.
- **Filter, don't navigate.** Non-matching spines hide; shelves that lose all
  their books hide too, and reappear when the query clears.
- **Announce the result count** in an `aria-live` region — *"3 books match"* —
  or a keyboard user gets silence.
- **No-JS fallback:** every shelf renders in full and the search box is hidden.
  Search is an enhancement; it is never the only way to see the books. Same
  principle as the contact page behind the business card (ledger #23).

Searching Burmese titles must work in Burmese. Match on the raw string —
**do not lowercase or normalise in a way that assumes Latin script.**

---

## 6. Burmese support — read this before building

**Playfair Display and JetBrains Mono have no Myanmar coverage.** Burmese titles
in the current type system render as tofu boxes. This is the one thing on this
page that fails silently: the build succeeds, the page loads, and the text is
squares.

Required:

- **Self-host a Myanmar-capable font** — Noto Sans Myanmar or Padauk — through
  the same Astro font pipeline already used for the other two families (ledger
  #14). No third-party request, consistent with every other font on the site.
- **Mark up the language:** `lang="my"` on Burmese titles and authors, so
  browsers and screen readers select the right font and voice.
- **Give Burmese more vertical room.** Myanmar stacks diacritics above and below
  the baseline; a line-height tuned for Latin will clip them.
- **Burmese on a rotated spine is the hard case.** Myanmar is a complex-shaping
  script, and rotated at spine width it gets small fast. Give Burmese spines
  extra width, or set their titles a size larger. Check this on a real device
  before calling it done.

None of this is optional if there is going to be a Burmese shelf at all.

---

## 7. Content

### Currently on the shelf

Two books. Both English, both in progress.

| | **Dune** | **Zero to One** |
|---|---|---|
| Author | Frank Herbert | Peter Thiel with Blake Masters |
| Section | English | English |
| Shelf | **Fiction** | **Non-fiction** |
| Status | Reading now | Reading now |
| Started | `TODO(owner)` | `TODO(owner)` |
| Progress | `TODO(owner)` | `TODO(owner)` |
| Ended | — | — |
| Rating | — | — |
| Review | — | — |

That is the entire shelf: **one section, two shelves, two books.** The Burmese
section does not render at all until a Burmese book exists.

### Not on this page

The windowsill photo from the About session — the stack showing Cobalt Red, Chip
War, Optimism Over Despair, The Crusades, Isaacson's *Einstein* and others — is
**not** the owner's reading and does not belong here. That open item from
`docs/about-me.md` is closed: the photo stays where it is or is dropped, but it
does not become a Reading List image and those titles are not entered as books.

---

## 8. Schema

Replaces the existing `Book` type in `src/content.config.ts`. The old
`status: current | past` with `progress` and `whyReading` is superseded.

```ts
type Book = {
  slug: string;
  title: string;
  author: string;
  language: "en" | "my";
  genre: "nonfiction" | "fiction";
  status: "reading" | "finished" | "want";

  started?: string;        // ISO date
  ended?: string;          // ISO date — omit while unfinished
  progress?: number;       // 0–100, meaningful only when status is "reading"
  rating?: 1 | 2 | 3 | 4 | 5;   // omit until finished
  review?: string;         // short, omit until finished

  pageCount?: number;      // drives spine width when present
  spineColor?: string;     // optional override; otherwise assigned from palette
};
```

Validation worth enforcing at build time, in the spirit of the existing
schema's named failures:

- `ended` set while `status` is not `finished` → fail by name
- `rating` or `review` set while `status` is not `finished` → fail by name
- `progress` set while `status` is not `reading` → fail by name

Delete `content/books/current.md` and `content/books/past/` — the whole
`current` / `past` directory split goes with the old schema.

---

## 9. Home grid tile

The Reading List tile should show **rendered spines**, cropped tight — a slice
of the shelf. Per ledger #21 the tile must carry a real image; a shelf of spines
is one, and it is generated rather than photographed, so it never goes stale.

**Do not use the windowsill book-stack photo for this tile** — see §7.

---

## 10. Open items

Blocking:

- [ ] Started dates and progress for Dune and Zero to One
- [ ] A Myanmar-capable font added to the Astro font pipeline **before** any
      Burmese book is entered

Not blocking:

- [ ] Burmese books — the section is built and stays hidden until one exists
- [ ] Page-count values, if spine widths should vary by real thickness
- [ ] Reviews and ratings, which arrive when the books are finished
