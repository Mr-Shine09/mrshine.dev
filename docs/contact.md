# Contact — content spec

**Written:** 16 Aug 2026
**For:** the build session that implements the site
**Status:** locked, no outstanding content except `resume.pdf`

Architecture context is in `docs/about-me.md` §0 and `ledger.md` #18–#37.

---

## 1. What this page is

**The business card, already open.**

Contact is not a grid tile (#20). The primary contact surface is the business
card fixed to the bottom corner of every page (#22) — spins, scales, travels to
centre, reveals. This page is what that card looks like when it is simply a
page: same seven links, same vCard, no animation required.

It exists for four reasons, all of them ordinary:

1. **The card's reveal needs JavaScript.** With JS off, the card may not open.
   The page always does.
2. **The nav pill needs a destination.** `index · about · contact` is the
   locked nav (#20); "contact" has to go somewhere.
3. **A URL you can send someone.** An animation is not a link.
4. **`/contact.vcf` needs a home** so right-click-save still works.

> **One data source, two presentations.** The page and the card both read the
> same file. Neither has its own copy of the links, so they cannot drift apart —
> which is the entire reason this page is cheap to keep.

---

## 2. Contents

Exactly what the card carries. Nothing extra, nothing withheld.

| Field | Value |
|---|---|
| Email | `oaksoekhant182209@gmail.com` |
| GitHub | `https://github.com/Mr-Shine09` |
| LinkedIn | `https://www.linkedin.com/in/oak-soe-khant-350252362` |
| Instagram | `https://www.instagram.com/oak_soe_khant909` |
| Facebook | `https://www.facebook.com/johnwick.wick.37625` |
| Devpost | `https://devpost.com/oaksoekhant182209` |
| Résumé | `/resume.pdf` — **TODO(owner)**, still the only empty field |
| vCard | `/contact.vcf` — download |

Plus the identity line already established in `site.ts`: **Oak Soe Khant**,
Second-year Computer Engineering student at De Anza Community College,
**Santa Clara, California**.

**Blank fields drop rather than render empty**, the rule `site.ts` already
applies. Today that means the Résumé row is simply absent until the PDF exists.

**Presentation: a labelled list, not icon soup.** This was the original
intent in `plan.md` §5 and it survives the architecture change. Six unlabelled
glyphs make a visitor guess; six labelled rows do not.

---

## 3. No contact form

There is no form on this page, and there should not be one.

A form needs somewhere to POST. This site is static, hosted on Cloudflare Pages,
with no backend and no database — adding a form means adding a third-party
form service (a new external dependency and a privacy question about where
messages go) or a Cloudflare Function (a backend to maintain, and a spam problem
to solve on day one).

An email address is a contact form that already works everywhere.

**Do include a copy-to-clipboard control** beside the email. It is the one small
convenience that costs nothing and saves a visitor on a phone from a clumsy
long-press. It must sit *beside* the address, never replace it — the address
stays visible and selectable as text.

---

## 4. The vCard

`/contact.vcf` is already built as a build-time static endpoint and was verified
well-formed in the 15 Aug session. It survives the architecture change unchanged
in principle — but **its contents are now out of date.**

It was generated when `site.ts` held only name, GitHub and email. It must be
regenerated to carry the full set: LinkedIn, Instagram, Facebook, Devpost, and
the Santa Clara location.

Keep it a **real file generated at build time**, not a Blob assembled in the
browser. That is what makes right-click-save work and what keeps it functional
with JS off.

---

## 5. Requirements

Nothing new — the same bar as every other page:

- **Keyboard:** every link in tab order with a visible focus state. The
  copy-to-clipboard control is a real `<button>`, reachable and operable by
  keyboard, and it announces success in an `aria-live` region rather than only
  changing its own label colour.
- **No-JS:** every link and the vCard download work with no script at all. Only
  the copy button degrades, and it should be hidden rather than present-and-dead
  if the script hasn't loaded.
- **Tap targets ≥44px** on every row.
- **`rel="me"` on the social links**, and `rel="noopener"` on anything opening
  in a new tab. Prefer same-tab navigation; a personal site has no reason to
  hold the window hostage.

**One thing to accept, not solve:** a plain email address on a public, indexed
page will be scraped by spam harvesters. Obfuscation tricks that defeat scrapers
also defeat screen readers and copy-paste, which costs real visitors more than
the spam costs. Publish it plainly. That is the normal trade and it is the right
one here.

---

## 6. Relationship to the business card

| | Business card (#22) | This page (#23) |
|---|---|---|
| Where | Bottom corner of **every** page | `/contact` |
| Opened by | Click → spin, scale, travel to centre | Navigation |
| Needs JS | Yes, for the reveal | No |
| Data source | **The same file** | **The same file** |
| Role | Front door | The door that still opens when the power is out |

The standing rule from #23: **contact information must never exist only behind
an animation.**

---

## 7. Mascot — deferred

The old build placed the `sleeping` sprite in the contact card, so the page
"went to sleep" at the end of the scroll. That mapping belonged to the
single-page structure and has not been replaced.

**This is deliberately left open.** The owner is producing a new Hero on Codex,
and decision #33 already holds a 13-frame Hero V2 welcome atlas as a saved
implementation candidate outside `site/`. The full mascot mapping across the new
five-surface architecture should be decided **once that asset lands**, not
guessed at now and revised later.

Build this page with no sprite. Adding one afterwards is a component call; it
does not affect anything specced here.

---

## 8. Home grid

**Contact gets no tile** (#20). It is a nav pill — `index · about · contact` —
and the grid stays at four content tiles.

---

## 9. Open items

Blocking:

- [ ] `resume.pdf` at `site/public/resume.pdf` — the last empty field across all
      five docs

Not blocking:

- [ ] Regenerate `contact.vcf` with the four socials and the location
- [ ] Mascot placement, once the new Hero lands (see §7)
- [ ] Real `.dev` domain, which the vCard and canonical URLs both need
