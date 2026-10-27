# The Capelli Institute™ — website

Static HTML, CSS and vanilla JavaScript. No framework, no npm, no tracking. Opens from `file://` and from
any static host. Deployed on GitHub Pages at https://rfinlay.github.io/capelli-institute-site/.

**How a change goes live.** Every push to `main` runs `.github/workflows/pages.yml`: it regenerates the pages
from `assets/data/catalog.json` and `assets/data/copy.json` with `tools/build-pages.py`, commits the
regenerated HTML back to `main` (so the repository always holds what is live), and publishes the site to
Pages. If the catalog fails validation the build exits non-zero, nothing is published, and the last good
site stays up. The client edits the two data files through **Pages CMS** (`.pages.yml`, app.pagescms.org);
a CMS save is a commit, so it rebuilds and publishes by itself. Guides for him: `SAM-EDITOR-GUIDE.md` and
`STRIPE-SETUP-FOR-SAM.md`.

`BASE_PATH` in `tools/build-pages.py` is the Pages project path; `404.html` is built against it because
Pages serves that page at any depth. Pages cannot set response headers, so the content security policy
ships as a `<meta>` tag in every page.

## Layout

| Path | What |
|---|---|
| `index.html` | Home |
| `books/index.html`, `books/<slug>.html` | Book catalog and one product page per title (5) |
| `philosophy.html` | The Five Elements and the systems from the books |
| `lectures/index.html`, `lectures/<slug>.html` | Lectures in Print™ catalog and one page per lecture (9, numbered 001–009 from the client's master catalog of Oct 26, 2026) |
| `resonant-mind.html` | Resonant Mind™, the Institute's video channel (https://www.youtube.com/@ResonantMindPsych): the client's banner, what the channel carries, Subscribe / Visit buttons, and the channel's latest uploads as click-to-play embeds. The channel address is **one value**, `resonantMind.channelUrl` in `copy.json`; while it is empty no button is rendered. See *Resonant Mind videos* below |
| `assets/data/videos.json`, `assets/img/videos/` | **Machine-written** by `tools/fetch-videos.py`: the channel's latest uploads (id, title, date) and one poster per video. Do not edit by hand |
| `sitemap.xml`, `robots.txt` | Generated with the pages, on the final domain (same URLs as the canonical tags) |
| `ceu.html` | Continuing Education Units. **The only program with online registration.** |
| `programs/bipp.html`, `programs/anger-resolution.html`, `programs/cognitive-programs.html` | **Information + phone number only. No form, by client instruction.** |
| `workshops.html` | Workshops & Seminars, with an organization inquiry form |
| `coming-soon.html` | Standalone launch teaser with QR and email capture |
| `404.html`, `legal/privacy.html`, `legal/terms.html` | Not-found page and client-supplied legal placeholders |
| `assets/data/catalog.json` | **Single source of truth** for books, editions, SKUs, ISBNs, prices, buy links and lectures |
| `assets/data/copy.json` | Editable page copy: contact details, home page lines, CEU / workshops / launch intros, the Resonant Mind channel link and lines |
| `assets/data/catalog.js` | Derived from the JSON for the in-page edition selector. Do not edit by hand. |
| `.pages.yml` | Pages CMS form definitions for the two data files. Every catalog key must be declared here (the CMS drops undeclared keys and empty values on save; the generator restores defaults) |
| `.github/workflows/pages.yml` | Build, commit-back and publish on every push to `main` |
| `assets/img/` | Optimized crops of the client's own art. Originals stay in `../assets-from-sam/` (not in this repo). |
| `tools/build-pages.py` | Regenerates every page from `catalog.json` and the shared header/nav/footer. |

## Editing

- **Add or change a book, edition, price, ISBN or purchase link:** edit `assets/data/catalog.json` (or let
  the client do it in Pages CMS), then run `python3 tools/build-pages.py` and commit. Prices are numbers.
  Per edition, `buyUrl` is the client's **Stripe Payment Link** (gold "Buy this edition" button; the money
  goes to his Stripe account) and `amazonUrl` is an optional secondary "Also on Amazon" link. An edition
  with no `buyUrl` renders "Available soon" with no href at all, never a placeholder link. Both must be
  `https://` or the build refuses.
- **Header, nav, footer:** edit the functions at the top of `tools/build-pages.py`, regenerate, commit.
- **Resonant Mind channel link:** set `resonantMind.channelUrl` in `assets/data/copy.json` (or Pages CMS → Site copy →
  Resonant Mind), regenerate, commit. Must be `https://` or the build refuses. Each lecture's own `video` field in the
  catalog adds a "Watch on Resonant Mind" button to that lecture page.

## Resonant Mind videos

The channel is `UCQLWzFAe-_0OCJhs9v1W44g` (`resonantMind.channelId` in `copy.json`). Two sources feed the page, in this order:

1. **Featured (editor's list).** `resonantMind.featured` in `copy.json` (Pages CMS → Site copy → Resonant Mind → Featured videos):
   rows of `{video, title}` where `video` is any YouTube link or an 11-character id. A row that is not a video fails the build
   with the row number. These always show first.
2. **Latest uploads (automatic).** `tools/fetch-videos.py` reads the channel's public Atom feed
   (`https://www.youtube.com/feeds/videos.xml?channel_id=UC…`, no API key, newest 15), keeps the 12 newest, copies each
   poster to `assets/img/videos/<id>.jpg`, and writes `assets/data/videos.json`. The GitHub Action runs it before every build:
   on every push **and on a daily schedule (06:17 UTC)**, committing the result back when anything changed. A new upload
   therefore appears on the site within a day with no one touching anything. If YouTube cannot be reached the script warns
   and keeps the previous list; it never fails the build. With no public videos the page shows "First videos coming soon"
   and the Subscribe button.

**Embeds.** Each video is rendered as a facade: the site's own poster copy plus a play button, as a plain link to the video
on YouTube. `institute.js` turns a click, Enter or Space into the cookieless player (`https://www.youtube-nocookie.com/embed/<id>`,
autoplay, titled iframe, focus moved into it). Nothing is requested from YouTube or Google until a visitor presses play, which is
why posters are committed rather than hot-linked, and why `img-src` in the CSP stays `'self'`. The Resonant Mind page is the only
page whose CSP carries `frame-src https://www.youtube-nocookie.com`, and only when it has videos to show. Test it locally with a
saved feed: `python3 tools/fetch-videos.py --feed some-feed.xml && python3 tools/build-pages.py`.
- **Lecture cover art** is named by slug in `assets/img/lectures/`. Three lectures (002, 008, 009) use
  `cover-pending.jpg` (the Lectures in Print emblem on navy) until the client sends covers; the covers for 003–007 still
  carry the interim numbers printed on the art, noted per lecture in `_artNote`.
- **™ → ®:** when the registration is granted, replace `™` inside `<span class="tm">` across the site (one find-and-replace).
- **Copy the client still owes:** every spot is marked with an HTML comment starting `COPY NEEDED:` and a visible
  dashed box. `grep -rn "COPY NEEDED" --include=*.html .` lists them all.

## Rules carried from the engagement

- BIPP, Anger Resolution and Cognitive pages never get a form, a "register" control, a calendar sign-up or a payment.
  The nav has no global call-to-action for the same reason.
- No AI-written prose in the client's voice. All visible copy is transcribed from his art and sheets.
- Palette and type are his: navy ground, single gold accent, Cinzel + EB Garamond (self-hosted, OFL).
- Forms: GitHub Pages has no form backend. `FORM_ENDPOINT` in `tools/build-pages.py` is `None` on the preview
  build, so the three forms (CEU registration, workshop inquiry, early-access list) are stopped in the browser
  and the status box says nothing was sent. At launch set `FORM_ENDPOINT` to the chosen form service's URL,
  regenerate, and every form posts there. Nothing is ever silently discarded.
- `assets/data/catalog.js` is linked with a content-hash query string, so a catalog change is never served stale
  from a browser cache.
