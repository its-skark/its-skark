# GitHub profile — design & deployment

A dark, modern profile built as a single repo that serves **two** surfaces:

| Surface | File | What it is |
|---|---|---|
| `github.com/its-skark` | `README.md` | The dashboard visitors see without leaving GitHub |
| `its-skark.github.io/its-skark/` | `index.html` | The full interactive HTML/CSS profile |

Both share one design system (palette, type scale, voice) so they feel like one
product rather than two unrelated pages.

---

## 1. Publish it

```bash
cd github-profile
git init -b main
git remote add origin https://github.com/its-skark/its-skark.git
git add .
git commit -m "feat: dark-mode GitHub profile (README + interactive site)"
git push -u origin main
```

The repo **must** be named exactly `its-skark` (your username) and be public for
GitHub to render `README.md` on your profile page.

### Turn on the interactive site

Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
The `pages.yml` workflow then publishes on every push.

> If the profile README does not appear: repo must be public, named `its-skark`,
> and `README.md` non-empty. For accounts created before July 2020, use
> **Share to profile** on the repo page.

### Turn on the snake animation

Repo → **Settings → Actions → General → Workflow permissions → Read and write**,
then run `.github/workflows/snake.yml` once from the Actions tab. It commits
`assets/snake.svg` and cache-busts the `?v=` query in the README.

---

## 2. Why everything visual is a self-hosted SVG

GitHub's README sanitizer keeps a small allowlist of HTML tags
(`h1`–`h6`, `p`, `div`, `span`, `a`, `img`, `table`, `details`, `kbd`, …) and
**removes** everything else: `iframe`, `style`, `script`, `class`, inline
`style=`, `target=`, `svg`, and all `data:` URIs.

So a README has exactly two visual tools:

1. **Layout** — `<table>` for columns, `<div align="center">` to centre,
   `<details>` to collapse.
2. **Artwork** — `<img src="assets/x.svg">`. SVG loaded through `<img>` keeps its
   CSS `@keyframes`, SMIL `<animate>`, gradients and `<filter>` blurs, because
   nothing is fetched from outside the file.

That second property is what makes this design possible: the hero banner,
typewriter, stack grid and status card are real vector artwork with real
animation, hosted in your own repo.

### Table cells are pure HTML on purpose

GFM markdown parsing inside a `<td>` is inconsistent. Verified against
`api.github.com/markdown`:

| Input inside a `<td>` | Result |
|---|---|
| `**bold**` on its own line, blank line after the tag | renders as `<strong>` |
| `<td>**bold**</td>` all on one line | literal asterisks |
| a markdown pipe table, then an indented `</td>` | closing tag escaped as visible `</td>` text |

That last case bit this README during development: the About/Stack cells ended
with an indented `</td>` after markdown content, and GitHub rendered a stray
`</td>` in a code block. Rather than chase the exact interaction, every cell is
now plain HTML (`<h3>`, `<p>`, `<ul>`, `<li>`, `<b>`) with balanced tags. Markdown
is used freely *outside* tables. That is deterministic on every renderer.

`./verify.sh` fails the build if any closing tag escapes into visible text.

### Third-party services were deliberately avoided

Measured live while building this:

| Service | State | Consequence |
|---|---|---|
| `github-profile-trophy.vercel.app` | **HTTP 402** deployment disabled | trophies removed |
| `github-readme-activity-graph.vercel.app` | **HTTP 402** deployment disabled | replaced by self-hosted snake via Actions |
| `readme-typing-svg.demolab.com` | returns the demo HTML page, not an SVG | typewriter generated locally |
| `metrics.lecoq.io` (activity-graph successor) | 500 without per-user OAuth | not used |
| `github-readme-stats.vercel.app` | working | used for stats only |
| `streak-stats.demolab.com` | working | used for streak only |
| shields.io `github/repos`, `/contributors`, `/last-commit` | "badge not found" **for every user** | replaced with verified static values |

`raw.githack.com` and jsDelivr cannot rescue this: iframes are stripped by the
sanitizer, githack serves an anti-phishing interstitial for HTML, and jsDelivr
serves `.html` as `text/plain`.

Result: every visual above and below the stats cards is self-hosted and cannot
break. Only two cards depend on a third party, and the page still looks
complete if both fail.

---

## 3. Regenerating the artwork

```bash
python3 tools/gen_cards.py assets       # assets/stack.svg
python3 tools/gen_typing_svg.py assets  # assets/typing.svg
```

`assets/hero.svg`, `status.svg`, `divider.svg` and `favicon.svg` are
hand-authored and edited directly.

### Bugs worth remembering

All found by rendering the SVGs locally and measuring, not by reading the code:

1. **`keyTimes` must be fractions in `[0,1]`, not percentages.** Writing `3.365`
   instead of `0.03365` makes the whole `<animate>` invalid; browsers ignore it
   silently and the element keeps its base value forever. The typewriter banner
   simply never appeared.
2. **Never put an entrance animation on text with `animation-fill-mode: both`.**
   That starts the element at `opacity: 0`, so any renderer that captures a
   frame before animations start — a static rasteriser, a PDF export, reduced
   motion — shows no text at all. Artwork that must always be legible should
   only animate non-essential decoration.
3. **Never measure glyphs by estimating the advance.** The typewriter caret used
   to rest at `X + width − PAD + 2`, where `width` came from an assumed `0.6em`
   monospace advance. That guess drifts — most on lines containing `·`, which is
   wider in most system mono fonts. The fix is `textLength` +
   `lengthAdjust="spacing"` on every line, which forces the renderer to use
   exactly the computed width no matter which font resolves. The caret is then
   exactly flush (`−1px`) on every line.
4. **Baseline + descender must be inside the viewBox.** `status.svg` had row 3's
   sub-line baseline at `y=193`; descenders reached ~`198` in a 196-tall card, so
   the border cut the text mid-glyph. It looked like stray/garbled characters.
5. **XML comments cannot contain `--`.** Two separate edits were rejected by the
   parser for writing `---------- section ----------` and `line -- keep it`
   inside comments. Browsers parse SVG strictly, so that is a hard parse error.
6. **A static caret plus an animated caret = two cursors.** The typewriter had a
   permanent caret next to `$` *and* per-line carets. Only one should exist.
7. **Unequal bar widths imply data that does not exist.** The three "progress"
   bars were 300/248/176px — that reads as 100/83/59% progress for no reason.
   They are now uniform animated accents over a faint track.

---

## 4. Quality tooling

```bash
./verify.sh              # everything (needs network)
./verify.sh --local      # offline checks only
```

Or individually:

```bash
python3 tools/lint_readme.py     # GitHub rendering mistakes
python3 tools/check_images.py    # every image URL actually resolves
python3 tools/preview_readme.py  # render via GitHub's own markup API
```

`verify.sh` checks: every SVG parses as strict XML, every SMIL animation has
valid `keyTimes`, no text depends on an animation to become visible, every
`assets/` reference exists, the typewriter caret sits flush on each line with a
single cursor, the status banner's rows clear its border, the README passes the
rendering lint, all 56 remote images return real SVG, and GitHub's own renderer
produces zero tag leaks.

Two of those checks exist only because a bug slipped through once:

- `tools/check_caret_alignment.py` asserts `caret_rest_x == X + textLength - 1`
  for every line, and that no static prompt caret remains.
- `tools/check_status_layout.py` asserts every sub-line's descender is inside
  the card, bars are centred on their rows, and bar widths are uniform.

Both were tested by reintroducing the original bug to confirm they fail.

**`preview_readme.py` is the important one.** It POSTs `README.md` to
`api.github.com/markdown` — the same pipeline that serves github.com — and
previews the sanitized result. That is the only way to catch GitHub's
counter-intuitive behaviour, which I verified directly against that API:

| Input | Result |
|---|---|
| `**bold**` on its own line inside a `<td>` | renders as `<strong>` |
| `<td>**bold**</td>` on one line | renders as literal asterisks |
| `### Heading` inside a blank-line-separated `<td>` | renders as `<h3>` |
| `<td><b>x</b><br /><sub>y</sub></td>` (all inline HTML) | fine |
| `style=`, `class=`, `target=` | stripped |
| `align`, `width`, `valign`, `open` | kept |
| `<iframe>`, `<script>`, `<style>`, `<svg>` | removed |

When the API is rate-limited (60 req/hr unauthenticated) the tool warns loudly
and falls back to an approximation — a fallback render is never silently
presented as faithful.

---

## 5. Design system

```css
--bg:        #07090D    /* page */
--bg-card:   #0E1219    /* surfaces */
--text:      #E9EDF6    /* primary ink */
--text-dim:  #A3ADC2    /* secondary */
--text-faint:#6C7689    /* tertiary / mono labels */

--violet:    #8B5CF6    /* primary accent   */
--cyan:      #22D3EE    /* secondary        */
--emerald:   #34D399    /* success / "live" */
--amber:     #FBBF24    /* warning / links  */
```

**Type.** Space Grotesk for display, Inter for body, JetBrains Mono for labels
and code. Space Grotesk reads "developer tool / modern startup" without the
2020 monospace-everything cliché; Inter stays legible at the 11–13px sizes used
inside SVG artwork; JetBrains Mono has the best O/0/l confusion resistance, which
matters at small sizes.

Inside SVGs the fonts must come from the **system stack** — SVG in `<img>` mode
cannot load a webfont, and external resources are blocked. `styles.css` (used by
the Pages site only) does load Google Fonts.

**Voice.** First person, concrete numbers, no filler. "Architected multi-tenant
POS platforms" beats "passionate developer". The one place the README shows its
working is the honesty note under the stats: the top-languages card understates
TypeScript because most professional work is in private repos.

---

## 6. Files

```
README.md                    the profile README
DESIGN.md                    this document
index.html                   full interactive profile (Pages)
verify.sh                    all quality gates in one command
assets/
  styles.css                 design system for the Pages site
  app.js                     typing, counters, reveal, cursor spotlight
  hero.svg                   hero banner
  typing.svg                 animated typewriter      (generated)
  stack.svg                  technology grid          (generated)
  status.svg                 "currently" panel
  divider.svg                section rule
  snake.svg, snake-dark.svg  contribution graph       (generated by Actions)
  favicon.svg                RP monogram
tools/
  gen_cards.py               generates stack.svg
  gen_typing_svg.py          generates typing.svg
  lint_readme.py             catches GitHub rendering mistakes
  check_images.py            verifies every image URL
  check_caret_alignment.py   caret sits flush, single cursor
  check_status_layout.py     no clipped text, bars centred
  preview_readme.py          renders via GitHub's markup API
.github/workflows/
  pages.yml                  deploy the interactive site
  snake.yml                  regenerate the contribution snake
preview.html                 local preview of all SVG assets
preview-readme.html          generated by tools/preview_readme.py
```

`preview-readme.html` and `preview.html` are development aids — they are not
referenced by the README and are excluded from the Pages artifact.

---

## 7. Facts the copy depends on

Recorded here so a future edit does not reintroduce a stale claim:

| Fact | Where it appears |
|---|---|
| B.Tech IT, GBPUAT, 2022 → 2026, **graduated June 2026** | README Education, `index.html` awards card |
| SCPPS: university society, member **2022 → 2024**, Technical Committee Lead, Pantnagar | README Experience, `index.html` timeline |
| Location is **Pantnagar, India** (GBPUAT campus), not Lucknow — corrected directly by the owner | badge, `status.svg`, `index.html` |
| Bilwg Services: Software Developer, May 2026 → present, remote | both |
| Delosch: intern, Jun 2025 → Aug 2025, hybrid | both |
| GitHub handle is `its-skark` (renamed from `Rachit-Pandey-2004`) | everywhere |
| 19 public repos, 18 followers | badge + stack link |

Note the SCPPS dates are **2022 → 2024**, not the 2024 → 2026 in the original
resume draft — the society membership ran through the first half of the degree.
The copy also avoids "final-year", "graduating" and "open to 2026 roles" because
the degree is finished; availability is now stated as "open to opportunities".

---

## 8. Content that is intentionally absent

Stated plainly so future edits don't reintroduce them:

- **No fake stars, no fake badges.** The kernel repo really has 1 star; the
  followers badge is a live query.
- **No trophy or activity-graph cards** — both services are down.
- **No invented metrics.** There is no "projects shipped" counter anywhere; the
  stack and project sections do that work through specificity instead.
- **No claims about the private POS/e-commerce work** beyond role and tech —
  those repos are someone else's, and the README says they are private.