# W Phrases — content spec

**Written:** 16 Aug 2026
**For:** the build session that implements the site
**Status:** structure locked, four phrases collected

Architecture context is in `docs/about-me.md` §0 and `ledger.md` #18–#32. This
page is one of the four home-grid tiles.

---

## 1. What this page is

A dump of **cool words and phrases found online** — the ones that go hard. A
collection, kept because they're good, not because they prove anything.

**Do not explain the name on the page.** "W" as a win is understood by everyone
who would enjoy this page, and a wall of phrases teaches anyone else in about
four seconds. A subtitle explaining the joke would be the least W thing on the
site.

The page has two jobs, and they pull against each other:

1. **Be readable** — these are phrases; someone has to be able to read one.
2. **Be a type specimen** — each phrase carries its own font, size and colour,
   so the wall is also a showcase.

Every decision below is a resolution of that tension. Motion serves the second
job; pausing, focus states and reduced-motion handling protect the first.

---

## 2. Layout and motion

**Marquee rows.** Two or three horizontal rows of phrases, sliding at different
speeds, adjacent rows in opposite directions.

- **Pause on hover and on keyboard focus.** Not optional — a phrase that can't
  be stopped can't be read, and the whole point is that someone reads one.
- **`prefers-reduced-motion`: no motion at all.** The rows become a static
  wrapped wall. Not "slower" — stopped. Per ledger #24.
- Rows loop seamlessly, so the page works at four phrases or eighty. This is why
  a marquee was chosen over a static wall: **four phrases is a thin page**, and
  a looping row never looks empty the way a four-item collage does.

### Accessibility

The seamless loop is normally built by duplicating the row's contents. That
duplicate is **decorative and must be `aria-hidden="true"`**, or a screen reader
reads the entire collection twice.

- A phrase with a `meaning` or `source` to reveal must be **focusable**, with a
  visible focus state, and revealing must work on focus as well as hover.
- If nothing is revealed, phrases are plain text and stay out of tab order.
  Don't make text focusable for no reason.
- **The static wall under reduced motion is also the no-JS fallback.** Every
  phrase renders and is readable with no script at all; the marquee is the
  enhancement. Same principle as search on the Reading List and the contact page
  behind the business card (#23).

---

## 3. Per-phrase styling

Each phrase carries its own type treatment, authored in the content file. Adding
a phrase is adding an entry; removing one is deleting it. **No admin UI, no
backend, no auth** — the site stays static, and the Keystatic panel planned in
#2 turns this file into a visual editor with dropdowns later.

### `font` — a fixed set of six

The field **validates against a named list** and fails the build on an unknown
value. Free-text font names were rejected: a typo would silently fall back to a
system default with no error anywhere.

Proposed six — the first two are already on the site:

| Token | Family | Why it's in the set |
|---|---|---|
| `display` | Playfair Display | Already loaded (#14). The high-contrast serif |
| `mono` | JetBrains Mono | Already loaded (#14). The engineering voice |
| `grotesque` | Space Grotesk | A neutral modern sans — the internet's default register |
| `condensed` | Archivo Narrow | Fits long phrases without shrinking them |
| `hand` | Caveat | Handwritten. The "scrawled in a notebook" feel these deserve |
| `slab` | Bitter | Heavy and declarative — for a phrase that lands hard |

**Four of the six are new families.** Self-host them through the same Astro
pipeline as #14 — no third-party requests — and load **only the weights actually
used, Latin subset only**. Six unbounded families would undo the performance
work already done on this site. **No pixel font**, per the standing exclusion in
#10.

### `size` — a token scale, not free pixels

`sm` · `md` · `lg` · `xl`. Free pixel values would let one phrase blow out a
marquee row's height and break the row rhythm. Four steps is plenty of contrast
across a wall.

### `color` — **must be a palette token**

> **This is the field most likely to break the site, and it breaks silently.**
>
> A free hex value will be legible in one theme and invisible in the other. A
> phrase set to near-black disappears on the dark background; a pale one
> vanishes in light mode. Nothing errors — the phrase is simply gone.
>
> **The field accepts palette tokens only** (ledger #9's twelve colours), and
> every token used must be **checked for contrast in both themes**. Rust is the
> known trap: #12 already records that it disappears in dark mode and amber
> replaces it as the dark accent.

### Optional style fields

`weight` and `italic`, both optional, both bounded to what the chosen family
actually ships. Requesting a weight a font doesn't have produces faux-bold — a
smeared approximation the browser synthesises — which looks broken next to real
type.

---

## 4. Schema

New content collection, `phrases`:

```ts
type Phrase = {
  slug: string;
  text: string;               // the phrase itself — short. Words, not paragraphs
  source?: string;            // who said it, where it came from
  meaning?: string;           // optional gloss — use rarely, see below
  dateAdded: string;          // ISO date

  style: {
    font: "display" | "mono" | "grotesque" | "condensed" | "hand" | "slab";
    size: "sm" | "md" | "lg" | "xl";
    color: PaletteToken;      // palette tokens only — never a raw hex
    weight?: number;          // must exist in the chosen family
    italic?: boolean;
  };

  bookSlug?: string;          // links to a Reading List entry — see §5
};
```

**`meaning` should mostly be empty.** A gloss on a phrase that lands on its own
kills it. Keep the field for the two or three that genuinely need one.

**`source` is optional and honest.** "Random finds on Instagram" is a better
source than a fabricated one, and better than leaving it blank. Where the source
is genuinely lost, say so rather than inventing attribution.

**`dateAdded` is stored on every phrase but displayed quietly**, if at all. It
costs nothing, it makes the page a real log rather than a static wall, and it
fits the time-capsule frame from About.

---

## 5. Cross-link to the Reading List

One of the four phrases comes from **Zero to One**, which is currently on the
Reading List shelf. When a phrase's `bookSlug` matches a book in the `books`
collection, **the source becomes a link to that book on the shelf**.

This is the only place two content pages in this site touch each other, and it
costs one optional field. A visitor who likes the line can see what you're
reading; a visitor on the shelf can see what came out of it.

Fail the build if `bookSlug` points at a book that doesn't exist — a silently
dead cross-link is worse than none.

---

## 6. The phrases

Four collected so far. Style assignments below are proposals — the whole point
of the schema is that they are one-line changes.

| # | Phrase | Source | Proposed style |
|---|---|---|---|
| 1 | *(the Drake entry — see the note below)* | Drake | `hand` · `lg` |
| 2 | Your name is a guest. Your life is the host. | Random finds on Instagram | `display` · `xl` |
| 3 | Build you up to drag you down (knock you down) | Unknown — `TODO(owner)` | `condensed` · `md` |
| 4 | The future is the set of moments yet to come | *Zero to One* → `bookSlug: zero-to-one` | `slab` · `lg` |

### Notes on the entries

**Phrase 1 — the Drake line.** The text is in the owner's own source note and is
not transcribed here: if it is a song lyric, it is the one category of quotation
this spec won't reproduce. Two practical points, separate from that: lyrics are
the most aggressively enforced kind of quotation on the open web, and the same
question is worth asking of phrase 3. Four words on a personal site is not a
realistic risk — this is a "know where the line is" note, not a blocker.

**Phrase 3 — "I forgot" is not an attribution.** Worth ten minutes of searching
to find the real one. If it stays unknown, `source: "Unknown"` is honest and
reads fine; a fabricated attribution would not.

**Phrase 4 is the cross-link.** It carries `bookSlug: zero-to-one` and its source
renders as a link to the shelf.

**Keep future entries short.** Words and phrases, not paragraphs. A collected
phrase is a phrase; a quoted passage from someone's writing is a different thing
and should be attributed if it ever appears.

---

## 7. Home grid tile

The W Phrases tile shows a **still of the wall** — three or four phrases at
their real sizes and fonts, cropped tight, motionless.

Per #21 the tile must carry real visual weight. Here the typography *is* the
image, which is exactly how the `alectear.com/lettering` reference works: every
tile on that grid is a piece of lettering. This is the tile that most resembles
the reference, and it should be built to look like it belongs there.

The tile must not animate on the home grid. Four tiles, one of them a running
marquee, would drag the eye away from the other three.

---

## 8. Open items

Blocking:

- [ ] The four new font families added to the Astro pipeline, subset and weight-limited
- [ ] Contrast check for every palette token used as a phrase colour, **in both themes**

Not blocking:

- [ ] A real source for phrase 3, or `Unknown`
- [ ] More phrases — the marquee loops, so four works and forty works
- [ ] Confirm the six-font set; swapping any family is a one-line change
