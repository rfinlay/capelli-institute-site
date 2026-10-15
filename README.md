# The Capelli Institute™ — website

Static HTML, CSS and vanilla JavaScript. No framework, no build step, no npm, no tracking.
Opens from `file://` and from any static host. Deployed as a Netlify preview.

## Layout

| Path | What |
|---|---|
| `index.html` | Home |
| `books/index.html`, `books/<slug>.html` | Book catalog and one product page per title (5) |
| `philosophy.html` | The Five Elements and the systems from the books |
| `lectures/index.html`, `lectures/<slug>.html` | Lectures in Print™ catalog and one page per lecture (6) |
| `ceu.html` | Continuing Education Units. **The only program with online registration.** |
| `programs/bipp.html`, `programs/anger-resolution.html`, `programs/cognitive-programs.html` | **Information + phone number only. No form, by client instruction.** |
| `workshops.html` | Workshops & Seminars, with an organization inquiry form |
| `coming-soon.html` | Standalone launch teaser with QR and email capture |
| `404.html`, `legal/privacy.html`, `legal/terms.html` | Not-found page and client-supplied legal placeholders |
| `assets/data/catalog.json` | **Single source of truth** for books, editions, SKUs, ISBNs, prices, buy links and lectures |
| `assets/data/catalog.js` | Derived from the JSON for the in-page edition selector. Do not edit by hand. |
| `assets/img/` | Optimized crops of the client's own art. Originals stay in `../assets-from-sam/` (not in this repo). |
| `tools/build-pages.py` | Regenerates every page from `catalog.json` and the shared header/nav/footer. |

## Editing

- **Add or change a book, edition, price, ISBN or purchase link:** edit `assets/data/catalog.json`, then run
  `python3 tools/build-pages.py` and commit. Prices are numbers; `buyUrl` is the outbound (Amazon or other) link.
- **Header, nav, footer:** edit the functions at the top of `tools/build-pages.py`, regenerate, commit.
- **™ → ®:** when the registration is granted, replace `™` inside `<span class="tm">` across the site (one find-and-replace).
- **Copy the client still owes:** every spot is marked with an HTML comment starting `COPY NEEDED:` and a visible
  dashed box. `grep -rn "COPY NEEDED" --include=*.html .` lists them all.

## Rules carried from the engagement

- BIPP, Anger Resolution and Cognitive pages never get a form, a "register" control, a calendar sign-up or a payment.
  The nav has no global call-to-action for the same reason.
- No AI-written prose in the client's voice. All visible copy is transcribed from his art and sheets.
- Palette and type are his: navy ground, single gold accent, Cinzel + EB Garamond (self-hosted, OFL).
- Forms post to Netlify Forms on the Netlify deploy. On another host, swap the form handler.
