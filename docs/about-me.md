# About Me — content spec

**Written:** 16 Aug 2026
**For:** the build session that implements the site
**Status:** content locked except the dates marked `TODO(owner)` and the photo files themselves

---

## 0. Read this first — architecture change

This document assumes a **different site architecture** from `plan.md` and `ledger.md`.
Those two files describe a single scrolling page with anchored sections
(locked decisions **#4** and **#13**). That is superseded.

**The new architecture:**

- The **home page is a masonry grid of tiles**, patterned on `alectear.com/lettering`
  — full-bleed image tiles, sticky pill nav top-left, each tile navigating to
  its own page.
- **Four grid tiles:** About · Projects · Reading List · W Phrases
- **Contact is a nav pill with its own page**, not a grid tile. Nav reads
  something like `index · about · contact`.
- Each block is now **a page**, not a section.

Everything else stays locked: Astro, local content files, plain CSS with custom
properties, the palette sampled from the mascot, Playfair Display + JetBrains
Mono, light/dark with amber (never rust) as the dark accent, no pixel font, no
WebGL. The mascot sprite system built in the first session should be reused, not
rebuilt.

`ledger.md` needs decisions #4 and #13 amended to record this. Until that
happens, the two documents contradict each other.

---

## 1. What this page is

The governing frame, in the owner's own words: **"a personal time capsule,
describing who I am and what I love to do."**

Written for everyone — friends, recruiters, whoever finds it. Not a résumé, not
a transfer application. It should be legible to a non-technical reader and
should never smell like a personal statement.

**Register:** first person, plain, a little dry. No "passionate about leveraging
technology." No inspirational-immigrant-narrative voice — the origin is stated
as a fact and left there, deliberately. The serif/mono type pairing already
signals the bookish-engineer thing; the prose should not repeat what the
typography is doing.

**The page is photo-led.** Nineteen photos carry it; the prose sits between the
galleries so it never becomes a wall of text.

---

## 2. Page anatomy

Five parts, in this order:

| # | Part | Content | Photos |
|---|---|---|---|
| 1 | **Lead** | Portrait + two-sentence opening + tagline | 1 |
| — | *`Yangon ✈ California` motif* | Small corner element, not a section — see §3.4 | 0 |
| 2 | **Yangon** | Where he's from | 3 |
| 3 | **De Anza** | Where he studies | 5 |
| 4 | **Hackathons** | Where he's been — a list, not case studies | 9 |
| 5 | **Actual Intelligence** | **One line.** The closing statement, set large | 0 |
| — | *Business card* | Fixed bottom corner, all contact details — see §5 | 0 |

Galleries are **chronological within each group**. Every photo carries a
**caption (under ~10 words) and a date** — the dates are what make it a time
capsule rather than a camera roll. A gallery with no dates is a failure of this
spec.

---

## 3. The copy

### 3.1 Lead

**Use this copy verbatim. It is the owner's own, not a draft to be improved:**

> What's up everyone!!! My name is Oak, a Second-year Computer Engineering
> student at DeAnza Community College, transferring in 2027.

That is the entire lead. Two things about it:

- **The three exclamation marks are intentional.** Do not tidy them to one, and
  do not soften the opening into "Hi, I'm Oak." The greeting sets the register
  for the whole site.
- **There is no second paragraph.** An earlier draft carried a line beginning
  "I like building things that make a day run better…" — that line has been
  **cut and must not be reinstated.** The tagline (§3.2) does that job.

**Confirmed facts** (these replace the `TODO(owner)` markers in
`site/src/data/site.ts`):

- Name: Oak Soe Khant — goes by **Oak**
- Role: Second-year Computer Engineering student, De Anza Community College
- Transferring: 2027
- Origin: Yangon, Myanmar
- Location: **Santa Clara, California**, United States

**Contact details do not appear in the lead.** Email, GitHub, LinkedIn, socials
and résumé all live in the business card (§5) and nowhere else on this page.

**Deliberately excluded — do not add:** the date he moved, his age at the time,
why he moved, or any account of the move itself. This was an explicit decision.

### 3.2 Tagline

Sits directly under the lead. The owner's own line, lightly cleaned:

> Building cool products to boost productivity. Hackathon fanatic. Mindful AI
> user. **Reader in progress.**

Two notes:

- It is *"Hackathon fanatic"* — singular. The original had "Fanatics."
- **"Reader in progress"** replaces the original "Loves books," which the owner
  flagged as generic. The replacement is deliberately aspirational rather than
  boastful — in his words, *"I am not a book fanatic yet, but trying to be
  one."* Keep that honesty; do not upgrade it to "avid reader." An acceptable
  alternative if a shorter line is needed: **"Becoming a reader."**

**Delete the existing placeholder in `site.ts`** — *"I build small, careful
things — and read old books about why people build at all."* It was
Claude-written. It is not his voice and it does not go on the site.

### 3.3 Actual Intelligence (closing block)

**One line. Verbatim. Nothing else.**

> Leveraging artificial intelligence to sharpen actual intelligence.

**No paragraphs, no explanation, no supporting prose.** An earlier draft
expanded this into two paragraphs; that draft is cut. The line is the whole
block — the wordplay does not survive being explained, and the position it
carries (**AI-native, not AI-dependent**) is legible without a gloss.

**Treatment:** full-width, display serif, set large. It is the last thing on the
page and should read as a closing statement, not a caption. No photo.

*One flag, owner's call:* "Leveraging" is the only corporate-register word
anywhere on this page, and the rest of the copy is deliberately plain. "**Using**
artificial intelligence to sharpen actual intelligence" keeps the parallelism
and loses the boardroom. Written as given unless he says otherwise.

### 3.4 The `Yangon ✈ California` motif

A small, minimal corner element — **not a section, not a gallery, not a map.**

- The two place names with an arrow between them, and a plane sitting on the
  arrow: `Yangon ✈ California`
- **Small.** It occupies a corner, not a band. Mono type, muted colour
  (`--grey-2` in light, its dark-mode counterpart), no heading, no border
- Placement: tucked against the lead — beside or beneath the portrait
- This is the *only* place the origin-to-here fact is stated visually. It is
  what remains of the "move story" the owner chose not to write, and it works
  precisely because it says nothing

**If the plane animates** along the arrow, keep it slow and subtle, and it
**must respect `prefers-reduced-motion`** — freeze the plane at one end, exactly
as the mascot wave already does. This is an existing acceptance criterion, not a
new one.

---

## 4. Photo manifest

Nineteen photos. Drop into `site/src/assets/photos/`. Kebab-case filenames.

All images need **alt text** — this is an accessibility requirement carried over
from the existing acceptance criteria, not a nice-to-have.

### Group 1 — Lead (1 photo)

| Slot | Photo | Caption | Date |
|---|---|---|---|
| `portrait` | Side profile, standing on a hill above San Francisco at dusk | TODO(owner) | TODO(owner) |

**Note:** this is a **side profile by choice** — the owner is not comfortable
with a straight-on portrait. Do not ask for or substitute a face-forward shot.
It must survive a **square crop**, because it doubles as the About tile on the
home grid.

### Group 2 — Yangon (3 photos)

| Slot | Photo | Caption | Date |
|---|---|---|---|
| `yangon-01` | River at sunset, boats moored along the far bank | TODO(owner) | TODO(owner) |
| `yangon-02` | Sun low over the water, city in silhouette | TODO(owner) | TODO(owner) |
| `yangon-03` | Row of trees over a dry schoolyard | TODO(owner) | TODO(owner) |

### Group 3 — De Anza (5 photos)

| Slot | Photo | Caption | Date |
|---|---|---|---|
| `deanza-01` | Administration building, flagpole at dusk | TODO(owner) | TODO(owner) |
| `deanza-02` | A. Robert DeHart Library, low sun on the facade | TODO(owner) | TODO(owner) |
| `deanza-03` | The main fountain, clear blue sky | TODO(owner) | TODO(owner) |
| `deanza-04` | Parking lot and the hills at sunset | TODO(owner) | TODO(owner) |
| `deanza-05` | The hills in autumn colour above the lot | TODO(owner) | TODO(owner) |

### Group 4 — Hackathons (9 photos)

**Treatment: a list of events attended, in order. Not case studies.** No project
writeups, no outcomes, no placements — those belong on the Projects page. Each
photo gets the event name and a date, and nothing more is required.

Sub-grouped by event, chronological:

| Slot | Photo | Event | Date |
|---|---|---|---|
| `hack-da-01` | "TRACKS" screen — Social Impact / Entertainment / Cyber Security | **De Anza Hackathon 4.0 (DA Hacks)** | TODO(owner) |
| `hack-scu-01` | Hack for Humanity can and a red Lego crab on a picnic table | **SCU Hack for Humanity** | 2026 — TODO(owner) month |
| `hack-scu-02` | Red Bull can pyramid with four Lego sea creatures below | **SCU Hack for Humanity** | 2026 — TODO(owner) month |
| `hack-berk-01` | Hack@Berk prizes slide, two organisers on stage | **UC Berkeley AI Hackathon** | June 2026 — TODO(owner) confirm |
| `hack-berk-02` | "Anthropic @ AI Hackathon" slide, speaker on stage | **UC Berkeley AI Hackathon** | June 2026 — TODO(owner) confirm |
| `hack-berk-03` | Two laptops on a crowded hall table | **UC Berkeley AI Hackathon** | 20 June 2026 |
| `hack-berk-04` | Sproul Hall in late sun | **UC Berkeley campus** | TODO(owner) |
| `hack-berk-05` | The Campanile against a clear sky | **UC Berkeley campus** | TODO(owner) |
| `hack-berk-06` | Berkeley and the Bay from the hills at sunset | **UC Berkeley campus** | TODO(owner) |

> ### ⚠️ `hack-berk-03` — DO NOT PUBLISH AS-IS
>
> The left-hand laptop in this photo has a `.env` file open with **live
> credentials readable on screen**: an `ANTHROPIC_API_KEY` (`sk-ant-api03-…`),
> what appears to be a `BROWSERBASE_API_KEY`, and a `REDIS_URL` with an embedded
> password.
>
> **Two separate actions, both required:**
> 1. **Rotate those keys.** They are compromised independently of this website —
>    the photo exists outside it.
> 2. **Crop the left laptop out** before the photo is used, or drop the photo.
>
> Do not publish this image until both are done.

**Also:** photos `hack-da-01` and `hack-berk-03` contain other attendees'
faces. Get their okay, or crop, before a public indexed page carries them.

### Group 5 — Setup (unplaced)

| Slot | Photo | Note |
|---|---|---|
| `books-window` | Stack of books on a windowsill, iPad playing something | Filed by the owner as "my setup." **Resolved 16 Aug: it does not move to the Reading List.** Those books are not his reading — he has not read them — so using the photo as a reading-shelf image would misrepresent it. Keep it here as a setup shot, or drop it. |

---

## 5. The business card

A **fixed element in the bottom corner of every page**, site-wide — not an
About-page flourish. It is the primary way visitors reach Oak.

**Behaviour:** at rest it reads as a closed business card, small, in the corner.
On click it **spins, scales up, and travels to the centre of the viewport**,
revealing its contents.

**Contents — all six, and nothing else:**

| Field | Value | Label on card |
|---|---|---|
| Email | `oaksoekhant182209@gmail.com` | Email |
| GitHub | `https://github.com/Mr-Shine09` | GitHub |
| LinkedIn | `https://www.linkedin.com/in/oak-soe-khant-350252362` | LinkedIn |
| Instagram | `https://www.instagram.com/oak_soe_khant909` | Instagram |
| Facebook | `https://www.facebook.com/johnwick.wick.37625` | Facebook |
| Devpost | `https://devpost.com/oaksoekhant182209` | Devpost |
| Résumé | `/resume.pdf` — **TODO(owner)**, file does not exist yet | Résumé |

Any field left blank is **dropped from the card, not rendered empty** — the same
rule `site.ts` already applies to socials. Résumé is currently the only blank.

**Devpost is a seventh field, added 16 Aug 2026.** It was not in the original
six. It belongs here more than most: the Hackathons gallery lists three events
without describing what was built, and Devpost is exactly where that record
lives. It turns the gallery from a photo set into something a curious visitor
can follow.

**Strip the tracking parameters from the Devpost URL.** As supplied it carried
`?ref_content=user-portfolio&ref_feature=portfolio&ref_medium=global-nav` —
Devpost's own analytics, meaningless on your site and noise in a `href`. The
clean URL above is what goes on the card.

**Also confirmed: location is Santa Clara, California** — this replaces the
`"TODO: your city"` placeholder in `site.ts`.

*One note, not an objection:* Instagram and Facebook are personal accounts, and
this card sits on every page of a public, search-indexed site — the same click
serves a friend and a recruiter. That's consistent with the "for everyone" frame
already locked, so it is written as given. Worth having decided rather than
having defaulted into.

**Relationship to the Contact page:** the card is the primary surface; `/contact`
remains a real page as the fallback. This is a locked decision — the card's
reveal needs JavaScript, the nav pill needs a destination, and the
already-built `contact.vcf` endpoint needs a page to live on so right-click-save
keeps working. **The site must never have contact information that exists only
behind an animation.**

**Requirements, carried over from the existing acceptance criteria:**

- **Keyboard:** the card must be focusable and openable with Enter/Space, with a
  visible focus state, and dismissible with Escape. Every revealed link is a
  real `<a>` in tab order.
- **`prefers-reduced-motion`:** the spin and the travel are motion. Under reduced
  motion the card should simply appear open — no spin, no scale, no flight.
- **Tap target ≥44px** in its closed state.
- It must not cover content it sits on top of at small widths, and it must not
  trap focus behind it.

**Design note:** a real business card is the one contact metaphor that suits
this site — the mascot, the serif/mono pairing, and a card that flips are all
the same idea, which is that the page is an object rather than a document. Worth
building properly rather than as a CSS trick.

---

## 6. Home grid tile

The About tile on the home page uses the **portrait** photo, square-cropped,
labelled `About`. It must read as a person, not a label on a coloured rectangle
— the grid is a gallery, and a tile with no image is a dead cell in it.

---

## 7. Open items

Blocking the build:

- [ ] Dates for all 19 photos (month + year is enough)
- [ ] Captions for groups 1–3 (hackathon captions are just event + date, already specced)
- [ ] Photo files dropped into `site/src/assets/photos/`
- [ ] `hack-berk-03`: keys rotated, photo cropped or dropped
- [ ] `resume.pdf` — the last empty field on the business card

Not blocking:

- [ ] Real `.dev` domain
- [ ] "Leveraging" vs "Using" in the closing line (§3.3)
- [x] `books-window` does **not** move to the Reading List — resolved 16 Aug, see §4 Group 5

Done:

- [x] `ledger.md` amended — #4 and #13 superseded, #18–#21 added (16 Aug 2026)
