#!/usr/bin/env python3
"""
The Capelli Institute™ — page generator.

This is a convenience for the developer, NOT a build step the site needs: it writes plain
static HTML into the repo, and the committed HTML is the deliverable. Run it after editing
assets/data/catalog.json (the single source of truth for books, editions and lectures) or
after changing the shared header / nav / footer below, and commit the output.

    python3 tools/build-pages.py

It also derives assets/data/catalog.js from catalog.json so the in-page edition selector
and any future checkout read the same data.

Copy rules: every sentence of visible prose comes from Sam Capelli's own art and sheets as
transcribed in catalog.json and DESIGN-SPEC.md, or from facts he already publishes on
thecapelligroup.com. Where copy is missing the page carries a visible .needs-copy block and
an HTML comment beginning "COPY NEEDED:". Nothing is written in his voice.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = json.load(open(os.path.join(ROOT, "assets/data/catalog.json")))
PHONE = "915-799-0614"
PHONE_TEL = "+19157990614"
ADDRESS = "9739 Socorro Rd, El Paso, TX 79927"
SITE = "The Capelli Institute"
TM = '<span class="tm">™</span>'

NAV = [
    ("home", "index.html", "Home"),
    ("books", "books/index.html", "Books"),
    ("philosophy", "philosophy.html", "Philosophy"),
    ("lectures", "lectures/index.html", f"Lectures<br>in Print{TM}"),
    ("ceu", "ceu.html", "CEU's"),
    ("bipp", "programs/bipp.html", "BIPP<br>Education Series"),
    ("anger", "programs/anger-resolution.html", "Anger<br>Resolution Series"),
    ("cognitive", "programs/cognitive-programs.html", "Cognitive<br>Programs"),
    ("workshops", "workshops.html", "Workshops<br>Seminars"),
]

def esc(s): return html.escape(s, quote=True)

def seps(words, sep="·"):
    return f' <span class="sep">{sep}</span> '.join(esc(w) for w in words)

def head(title, desc, root, body_class=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#000C1E">
<link rel="icon" href="{root}assets/img/brand/roundel.png" type="image/png">
<script>document.documentElement.className+=' js';</script>
<link rel="stylesheet" href="{root}assets/css/fonts.css">
<link rel="stylesheet" href="{root}assets/css/institute.css">
</head>
<body{(' class="'+body_class+'"') if body_class else ''}>
<a class="skip" href="#main">Skip to content</a>
"""

def header(root, current):
    items = []
    for key, href, label in NAV:
        cur = ' aria-current="page"' if key == current else ""
        items.append(f'      <li><a href="{root}{href}"{cur}>{label}</a></li>')
    return f"""<header class="band">
  <div class="wrap">
    <a class="crest" href="{root}index.html" aria-label="The Capelli Institute, home">
      <img src="{root}assets/img/brand/crest.png" width="260" height="267" alt="The Capelli crest: a shield quartered with a tree, a flame, a wave and a mountain, under a crown and laurel, with the name Capelli on a banner.">
    </a>
    <a class="wordmark" href="{root}index.html">
      <span class="name">The Capelli Institute{TM}</span>
      <span class="pillars">Education <span class="sep">•</span> Research <span class="sep">•</span> Certification <span class="sep">•</span> Publishing</span>
    </a>
    <div class="motto">
      <img class="roundel" src="{root}assets/img/brand/roundel.png" width="200" height="200" alt="Gold tree-of-life roundel.">
      <p>Know Thyself<br>Master Thy Life<br>Ascend to Higher<br>Frequencies</p>
    </div>
  </div>
</header>

<!-- Primary navigation. Nine sections. There is deliberately NO global "Register" control:
     the BIPP, Anger Resolution and Cognitive pages must never carry a registration affordance. -->
<nav class="nav" aria-label="Primary">
  <div class="wrap">
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="primary-menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      Menu
    </button>
    <ul id="primary-menu">
{chr(10).join(items)}
    </ul>
  </div>
</nav>

<main id="main">
"""

def footer(root):
    return f"""</main>

<footer class="site-foot">
  <div class="wrap">
    <div>
      <div class="brand">The Capelli Institute{TM}</div>
      <p class="small" style="margin:0 0 8px">Education · Research · Certification · Publishing</p>
      <p class="small" style="margin:0">{esc(ADDRESS)}<br><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
      <!-- COPY NEEDED: confirm the Institute's own phone number and address. These are the clinic's published details (thecapelligroup.com). -->
    </div>
    <div>
      <h4>Explore</h4>
      <ul>
        <li><a href="{root}books/index.html">Books</a></li>
        <li><a href="{root}philosophy.html">Philosophy</a></li>
        <li><a href="{root}lectures/index.html">Lectures in Print{TM}</a></li>
        <li><a href="{root}ceu.html">Continuing Education Units</a></li>
        <li><a href="{root}workshops.html">Workshops &amp; Seminars</a></li>
      </ul>
    </div>
    <div>
      <h4>Programs</h4>
      <ul>
        <li><a href="{root}programs/bipp.html">BIPP Education Series</a></li>
        <li><a href="{root}programs/anger-resolution.html">Anger Resolution Series</a></li>
        <li><a href="{root}programs/cognitive-programs.html">Cognitive Programs</a></li>
      </ul>
      <p class="small" style="margin:10px 0 0">Enrollment for these programs is in person. Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
    </div>
    <div class="legal">
      <span>&copy; 2026 The Capelli Institute{TM} · El Paso, Texas · All written works &copy; Samuel Capelli</span>
      <span><a href="{root}legal/privacy.html">Privacy</a> · <a href="{root}legal/terms.html">Terms</a> · <a href="{root}coming-soon.html">Launch notice</a></span>
    </div>
  </div>
</footer>
<script src="{root}assets/data/catalog.js"></script>
<script src="{root}assets/js/institute.js"></script>
</body>
</html>
"""

def page_head(root, crumbs, h1, thesis=None, eyebrow=None, art=None, art_alt=""):
    cl = " ".join(f'<li><a href="{root}{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for t, h in crumbs)
    artimg = f'\n  <img class="art" src="{root}{art}" alt="{esc(art_alt)}">' if art else ""
    return f"""  <div class="page-head{' has-art' if art else ''}">{artimg}
    <div class="wrap">
      <ol class="crumbs" aria-label="Breadcrumb">{cl}</ol>
      {f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ''}
      <h1>{h1}</h1>
      {f'<p class="thesis">{thesis}</p>' if thesis else ''}
    </div>
  </div>
"""

def needs_copy(ask):
    """Visible placeholder + machine-findable comment. `ask` is the exact thing Sam must supply."""
    return f'<!-- COPY NEEDED: {esc(ask)} -->\n<p class="needs-copy">{esc(ask)}</p>'

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f: f.write(content)
    print("wrote", path)

# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------
CARD_ICONS = {
 "books": '<path d="M3 8c5-2 9-2 14 1 5-3 9-3 14-1v19c-5-2-9-2-14 1-5-3-9-3-14-1Z M17 9v20"/>',
 "philosophy": '<circle cx="17" cy="12" r="8"/><circle cx="12" cy="21" r="8"/><circle cx="22" cy="21" r="8"/>',
 "lectures": '<path d="M8 3h13l6 6v22H8Z M21 3v6h6 M12 15h10 M12 20h10 M12 25h6"/>',
 "ceu": '<path d="M3 13 17 7l14 6-14 6Z M9 16v7c0 2 4 4 8 4s8-2 8-4v-7 M31 13v8"/>',
 "bipp": '<circle cx="11" cy="11" r="4"/><circle cx="23" cy="11" r="4"/><path d="M3 27c0-5 4-8 8-8s8 3 8 8 M15 27c0-5 4-8 8-8s8 3 8 8"/>',
 "anger": '<path d="M3 28 13 10l5 9 4-5 9 14Z"/>',
 "cognitive": '<path d="M12 4c-5 0-8 4-7 8-3 2-3 7 0 9 0 4 3 7 7 7h4V4Z M22 4c5 0 8 4 7 8 3 2 3 7 0 9 0 4-3 7-7 7h-4V4Z M17 4v24"/>',
 "workshops": '<rect x="3" y="5" width="28" height="18" rx="1"/><path d="M17 23v6 M10 29h14 M9 17l5-5 4 3 7-6"/>',
}
CARDS = [
 ("books", "books/index.html", "Books", "Explore our publications", "cards/card-1.jpg", "A stack of leather-bound books with an open volume on top."),
 ("philosophy", "philosophy.html", "Philosophy", "Principles for conscious living", "cards/card-2.jpg", "Balanced stones stacked at the water's edge at sunrise."),
 ("lectures", "lectures/index.html", f"Lectures<br>in Print{TM}", "Educational writings &amp; resources", "cards/card-3.jpg", "Handwritten manuscript pages with a fountain pen."),
 ("ceu", "ceu.html", "Continuing Education Units (CEU's)", "Professional development", "cards/card-4.jpg", "Gold laurel and mortarboard emblem on navy."),
 ("bipp", "programs/bipp.html", "BIPP<br>Education Series", "Domestic violence intervention &amp; prevention", "cards/card-5.jpg", "Silhouetted figures joining hands at sunset."),
 ("anger", "programs/anger-resolution.html", "Anger<br>Resolution Series", seps(["Regulation","Responsibility","Lasting change"]), "cards/card-6.jpg", "A mountain peak above cloud at dawn."),
 ("cognitive", "programs/cognitive-programs.html", "Cognitive<br>Programs", seps(["Think","Regulate","Choose","Evolve"]), "cards/card-7.jpg", "An illuminated brain within a neural network on navy."),
 ("workshops", "workshops.html", "Workshops<br>Seminars", seps(["Live training","Practical application","Real-world change"]), "cards/card-8.jpg", "A speaker addressing a seated audience."),
]

def program_cards(root):
    out = []
    for key, href, title, desc, img, alt in CARDS:
        out.append(f"""      <li class="card">
        <img class="art" src="{root}assets/img/{img}" width="480" height="281" alt="{esc(alt)}" loading="lazy">
        <div class="body">
          <svg class="icon" viewBox="0 0 34 34" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">{CARD_ICONS[key]}</svg>
          <h3><a href="{root}{href}">{title}</a></h3>
          <p class="desc">{desc}</p>
          <span class="more" aria-hidden="true">Learn more <span class="arrow">→</span></span>
        </div>
      </li>""")
    return "\n".join(out)

PILLARS = [("education","Education","Expanding Knowledge.","Gold tree of life"),("research","Research","Advancing Understanding.","Gold flame"),("certification","Certification","Developing Competence.","Gold mountain peaks"),("publishing","Publishing","Sharing Tools for Change.","Blue and gold wave")]
def pillar_band(root):
    items = "\n".join(f"""      <div class="pillar">
        <img src="{root}assets/img/brand/pillar-{k}.png" width="64" height="64" alt="" loading="lazy">
        <div><b>{t}</b><i>{s}</i></div>
      </div>""" for k,t,s,_ in PILLARS)
    return f"""  <section class="pillar-band" aria-label="The four pillars">
    <div class="wrap">
{items}
    </div>
  </section>
"""

def in_person_block(root, program):
    """The only call to action on an in-person page. No form element exists here."""
    return f"""        <div class="frame phone-block">
          <div class="seal" aria-hidden="true">Enrollment<b>In Person</b>at the office</div>
          <div class="lbl">Enrollment is in person</div>
          <a class="tel" href="tel:{PHONE_TEL}">{PHONE}</a>
          <p class="addr">Call to arrange enrollment in the {program}.<br>Enrollment is completed at the office, not online.</p>
          <p class="addr small dim">{esc(ADDRESS)}</p>
          <!-- COPY NEEDED: confirm the phone number and address for Institute enrollment (clinic details shown). -->
        </div>
        <p class="callout" style="margin-top:24px">This program does not take online enrollment, by design. There is no form on this page and none will be added. Call the number above.</p>"""

def money(v): return None if v is None else f"${v:,.2f}"

def product_block(root, kind, item, editions, cover_alt_default):
    """Edition selector + SKU panel, rendered server-side from the catalog so it works without JS."""
    first = editions[0]
    opts = []
    for ed in editions:
        checked = " checked" if ed is first else ""
        tag = f'<span class="vt">{esc(ed["tagline"])}</span>' if ed.get("tagline") else ""
        opts.append(f"""              <label class="variant" data-key="{ed['key']}">
                <input type="radio" name="edition" value="{ed['key']}"{checked}>
                <span class="vn">{esc(ed['name'])}</span>
                {tag}
              </label>""")
    price = money(first.get("price"))
    price_html = f'<span class="price">{price}</span>' if price else '<span class="price" data-field="price" data-placeholder="price">$—</span>'
    if price: price_html = price_html.replace('class="price"', 'class="price" data-field="price"')
    isbn = first.get("isbn")
    isbn_html = f'<dd data-field="isbn">{esc(isbn)}</dd>' if isbn else '<dd data-field="isbn" data-placeholder="isbn">To be assigned</dd>'
    buy = first.get("buyUrl")
    buy_html = (f'<a class="btn solid" data-buy href="{esc(buy)}" target="_blank" rel="noopener">Buy this edition <span class="arrow" aria-hidden="true">→</span></a>'
                if buy else '<a class="btn solid" data-buy href="#" aria-disabled="true">Purchase link available at launch</a>')
    tagline = first.get("tagline") or "—"
    return f"""        <div class="variants" data-variants data-kind="{kind}" data-slug="{item['slug']}" data-root="{root}">
          <fieldset>
            <legend>Choose an edition</legend>
            <div class="opts">
{chr(10).join(opts)}
            </div>
          </fieldset>
        </div>

        <div class="sku" data-variant-panel aria-live="polite">
          <dl>
            <dt>Edition</dt><dd data-field="name">{esc(first['name'])}</dd>
            <dt>Binding</dt><dd data-field="binding">{esc(first['binding'])}</dd>
            <dt>Finish</dt><dd data-field="tagline">{esc(tagline)}</dd>
            <dt>ISBN</dt>{isbn_html}
            <dt>Price</dt><dd>{price_html}</dd>
          </dl>
          {buy_html}
          <!-- COMMERCE: outbound purchase link per edition (Amazon or other channel). Set "buyUrl" in
               assets/data/catalog.json. No cart or checkout exists on this site by decision; the SKU
               structure above is what a checkout would bind to later. -->
          <p class="ph-note">Prices, ISBNs and purchase links are published at launch. <!-- COPY NEEDED: price, ISBN and purchase URL for each edition --></p>
          <p class="channels">Also available through Amazon and other booksellers at launch.</p>
        </div>"""

# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
def build_home():
    root = ""
    shelf = "\n".join(f'          <a href="books/{b["slug"]}.html"><img src="{[e for e in b["editions"] if e.get("image")][0]["image"]}" alt="{esc(b["title"])} cover" width="700" loading="lazy"></a>' for b in CAT["books"])
    body = f"""  <section class="hero" aria-labelledby="hero-title">
    <div class="wrap">
      <p class="rail">Knowledge Regulates. Responsibility Transforms. <em>Education</em> Creates a Higher Human Potential.<span class="dia" aria-hidden="true"></span></p>
      <div class="center">
        <h1 id="hero-title">The Capelli Institute{TM}</h1>
        <div class="rule" aria-hidden="true"><span class="dia"></span></div>
        <p class="thesis">Advancing clinical education through research, innovation, and psychological science.</p>
        <p class="pillars">Education <span class="sep">•</span> Research <span class="sep">•</span> Certification <span class="sep">•</span> Publishing</p>
        <a class="btn" href="#programs">Explore our programs <span class="arrow" aria-hidden="true">→</span></a>
      </div>
      <div aria-hidden="true"></div>
    </div>
  </section>

  <section class="programs" id="programs" aria-labelledby="programs-title">
    <h2 id="programs-title" class="vh">Programs</h2>
    <ul class="cards">
{program_cards(root)}
    </ul>
  </section>

  <section class="featured" aria-labelledby="featured-title">
    <div class="wrap">
      <div>
        <p class="eyebrow">Publishing</p>
        <h2 id="featured-title">Five titles. Each in more than one edition.</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <p class="lede">Paperback and hardback for everyday readers. Leather-bound, gold-foil collector's editions for the shelf. Every book is published by The Capelli Institute{TM} and written by its founder.</p>
        <div class="btn-row">
          <a class="btn" href="books/index.html">Browse the books <span class="arrow" aria-hidden="true">→</span></a>
          <a class="btn ghost" href="lectures/index.html">Lectures in Print{TM} <span class="arrow" aria-hidden="true">→</span></a>
        </div>
      </div>
      <div class="shelf" aria-label="The five books">
{shelf}
      </div>
    </div>
  </section>

{pillar_band(root)}"""
    write("index.html", head(f"{SITE}™ | Education · Research · Certification · Publishing",
        "The Capelli Institute, El Paso, Texas. Books, Lectures in Print, philosophy, continuing education units, and clinical programs. Advancing clinical education through research, innovation, and psychological science.", root)
        + header(root, "home") + body + footer(root))

# ---------------------------------------------------------------------------
# BOOKS index + product pages
# ---------------------------------------------------------------------------
def build_books():
    root = "../"
    items = []
    for b in CAT["books"]:
        cover = [e for e in b["editions"] if e.get("image")][0]
        eds = " · ".join(e["name"].replace(" Edition", "").replace("Special — Leather Bound", "Special Edition") for e in b["editions"])
        items.append(f"""      <li class="book">
        <div class="cover"><img src="{root}{cover['image']}" alt="{esc(cover['imageAlt'])}" width="700" loading="lazy"></div>
        <div class="body">
          <h3><a href="{b['slug']}.html">{esc(b['title'])}</a></h3>
          <p class="st">{esc(b['subtitle'])}</p>
          <p class="eds">{esc(eds)}</p>
        </div>
      </li>""")
    body = page_head(root, [("Home","index.html"),("Books",None)], "Books", "Explore our publications", f"Published by The Capelli Institute{TM}") + f"""
  <section aria-label="Catalog">
    <div class="wrap">
      <ul class="shelf-grid">
{chr(10).join(items)}
      </ul>
    </div>
  </section>
  <section class="alt tight" aria-labelledby="lip-cta">
    <div class="wrap two">
      <div>
        <p class="eyebrow">Also from the Institute</p>
        <h2 id="lip-cta">Lectures in Print{TM}</h2>
        <p class="lede">{esc(CAT['lectures']['positioning'])}</p>
        <a class="btn" href="{root}lectures/index.html" style="margin-top:16px">See the lectures <span class="arrow" aria-hidden="true">→</span></a>
      </div>
      <div>
        <p class="eyebrow">About the author</p>
        {needs_copy("author biography for the Books section, in the author's words.")}
      </div>
    </div>
  </section>
"""
    write("books/index.html", head(f"Books | {SITE}™", "The books of The Capelli Institute: A Five Elemental Philosophy, The Capelli Doctrine, The Architecture of Universal Order, The Void in Separation Theory, and ZenPai. Paperback, hardback and leather-bound editions.", root)
          + header(root, "books") + body + footer(root))
    for b in CAT["books"]:
        build_book(b)

def feature_section(root, b):
    f = b.get("feature")
    if not f: return ""
    if f["type"] == "elements":
        els = "\n".join(f"""        <li class="element">
          <div class="sym"><img src="{root}{it['image']}" alt="{esc(it['name'])} symbol" width="110" height="110" loading="lazy"></div>
          <h3>{esc(it['name'])}</h3>
          <p class="mean">{seps(it['traits'],'•')}</p>
          <p class="line">{esc(it['line'])}</p>
        </li>""" for it in f["items"])
        c = f["center"]
        return f"""
  <section id="elements" class="alt" aria-labelledby="elements-title">
    <div class="wrap">
      <p class="eyebrow">{esc(f['kicker'])}</p>
      <h2 id="elements-title">{esc(f['title'])}</h2>
      <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
      <ul class="elements" style="margin-top:40px">
{els}
      </ul>
      <div class="diamond frame">
        <img src="{root}{c['image']}" alt="A glowing golden diamond, the central symbol." width="90" height="150" loading="lazy">
        <div>
          <h3>{esc(c['name'])}</h3>
          <p class="mean">{esc(c['kicker'])}</p>
          <p class="small" style="margin:0">{esc(c['line'])}</p>
        </div>
      </div>
    </div>
  </section>
"""
    if f["type"] == "concepts":
        els = "\n".join(f"""        <li class="element">
          <div class="sym"><img src="{root}{it['image']}" alt="{esc(it['name'])} symbol" width="95" height="95" loading="lazy"></div>
          <h3>{esc(it['name'])}</h3>
          <p class="line">{esc(it['line'])}</p>
        </li>""" for it in f["items"])
        return f"""
  <section class="alt" aria-labelledby="concepts-title">
    <div class="wrap">
      <p class="eyebrow">{esc(f['kicker'])}</p>
      <h2 id="concepts-title">{esc(f['title'])}</h2>
      <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
      <ul class="elements four" style="margin-top:40px">
{els}
      </ul>
    </div>
  </section>
"""
    if f["type"] == "pillars":
        els = "\n".join(f"""        <li class="element">
          <div class="sym"><img src="{root}{it['image']}" alt="{esc(it['name'])}" width="100" height="100" loading="lazy"></div>
          <h3>{esc(it['name'])}</h3>
          <p class="line">{esc(it['line'])}</p>
        </li>""" for it in f["items"])
        pr = "\n".join(f"""        <li class="practice">
          <img src="{root}{p['image']}" alt="" width="480" loading="lazy">
          <b>{esc(p['name'])}</b><i>{esc(p['line'])}</i>
        </li>""" for p in f["practices"])
        return f"""
  <section class="alt" aria-labelledby="pillars-title">
    <div class="wrap">
      <p class="eyebrow">{esc(f['kicker'])}</p>
      <h2 id="pillars-title">{esc(f['title'])}</h2>
      <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
      <ul class="elements" style="margin-top:40px">
{els}
      </ul>
      <h3 style="margin-top:56px;color:var(--parchment)">Practices</h3>
      <ul class="practices">
{pr}
      </ul>
    </div>
  </section>
"""
    return ""

def build_book(b):
    root = "../"
    eds = b["editions"]
    with_img = [e for e in eds if e.get("image")]
    first = eds[0]
    cover = first if first.get("image") else with_img[0]
    thumbs = "".join(f'<button type="button" data-key="{e["key"]}" aria-pressed="{"true" if e is cover else "false"}" aria-label="Show the {esc(e["name"])} cover"><img src="{root}{e["image"]}" alt="" width="58"></button>' for e in with_img) if len(with_img) > 1 else ""
    sub2 = f'<p class="sub2">{esc(b["subtitle2"])}</p>' if b.get("subtitle2") else ""
    if b.get("description"):
        desc = (f'<p class="desc-h">{esc(b["descriptionHeading"])}</p>' if b.get("descriptionHeading") else "") + "".join(f"<p>{esc(p)}</p>" for p in b["description"])
    else:
        desc = needs_copy(f"back-cover synopsis for {b['title']}, in the author's words.")
    quote = f"""
  <section class="tight" aria-label="From the book">
    <div class="wrap narrow"><blockquote class="quote" style="margin:0 auto;text-align:center">{esc(b['pullQuote'])}<cite>{esc(CAT['author']['coverName'])}</cite></blockquote></div>
  </section>""" if b.get("pullQuote") else ""
    series = f"""
  <section class="tight" aria-label="Series line">
    <div class="wrap" style="text-align:center"><p class="eyebrow" style="font-size:14px;letter-spacing:.26em;margin:0">{esc(b['seriesLine']).replace('◆','<span style="color:var(--gold)">◆</span>')}</p></div>
  </section>""" if b.get("seriesLine") else ""
    back = f"""
  <section class="alt" aria-labelledby="back-title">
    <div class="wrap two">
      <div><img class="spread" src="{root}{b['backCoverImage']}" alt="Back cover of {esc(b['title'])}: the synopsis, the five keywords, the Capelli crest, a quotation and the ISBN barcode." width="700" loading="lazy"></div>
      <div>
        <p class="eyebrow">Back cover</p>
        <h2 id="back-title">{esc(b.get('descriptionHeading',''))}</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <p class="kw" style="margin-top:20px">{seps(b['keywords'])}</p>
      </div>
    </div>
  </section>""" if b.get("backCoverImage") else ""
    ed_note = ""
    missing = [e for e in eds if not e.get("image")]
    if missing:
        ed_note = f'<!-- COPY NEEDED: cover art for the {", ".join(e["name"] for e in missing)} of {b["title"]}; and confirmation of its edition list. -->'
    body = page_head(root, [("Home","index.html"),("Books","books/index.html"),(esc(b["title"]),None)], esc(b["title"]), esc(b["subtitle"]), f"Books · Published by The Capelli Institute{TM}") + f"""
  <section aria-label="Product">
    <div class="wrap product">
      <figure class="cover-stage" style="margin:0">
        <img data-cover src="{root}{cover['image']}" alt="{esc(cover['imageAlt'])}" width="700">
        <figcaption>{esc(cover['name'])}</figcaption>
        {f'<div class="thumbs">{thumbs}</div>' if thumbs else ''}
      </figure>
      <div>
        <h2 class="vh">Editions and details</h2>
        {sub2}
        <p class="author">{esc(CAT['author']['coverName'])}</p>
        <p class="kw" style="margin-bottom:24px">{seps(b['keywords'])}</p>
        {desc}
        {ed_note}
{product_block(root, "book", b, eds, cover['imageAlt'])}
      </div>
    </div>
  </section>
{quote}{back}{feature_section(root, b)}{series}
"""
    write(f"books/{b['slug']}.html", head(f"{b['title']} | {CAT['author']['coverName']} | {SITE}™",
        f"{b['title']}: {b['subtitle']}. By {CAT['author']['coverName']}. " + " · ".join(e["name"] for e in eds) + ".", root)
        + header(root, "books") + body + footer(root))

# ---------------------------------------------------------------------------
# PHILOSOPHY
# ---------------------------------------------------------------------------
def build_philosophy():
    root = ""
    fep = CAT["books"][0]; f = fep["feature"]
    els = "\n".join(f"""        <li class="element">
          <div class="sym"><img src="{it['image']}" alt="{esc(it['name'])} symbol" width="110" height="110" loading="lazy"></div>
          <h3>{esc(it['name'])}</h3>
          <p class="mean">{seps(it['traits'],'•')}</p>
          <p class="line">{esc(it['line'])}</p>
        </li>""" for it in f["items"])
    c = f["center"]
    void = CAT["books"][3]; zen = CAT["books"][4]; doc = CAT["books"][1]; auo = CAT["books"][2]
    body = page_head(root, [("Home","index.html"),("Philosophy",None)], "Philosophy", "Principles for conscious living", "Know Thyself · Master Thy Life · Ascend to Higher Frequencies", "assets/img/cards/card-2.jpg", "Balanced stones at the water's edge at sunrise.") + f"""
  <section aria-labelledby="intro-title">
    <div class="wrap two wide-left">
      <div>
        <p class="eyebrow">Foundation</p>
        <h2 id="intro-title">The Elements Within. The Architecture of a Purposeful Life.</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <p class="lede">Awareness <span class="sep">·</span> Regulation <span class="sep">·</span> Adaptability <span class="sep">·</span> Structure <span class="sep">·</span> Purpose</p>
        {needs_copy("an introduction to the philosophy section, in the author's words, drawn from the books.")}
      </div>
      <blockquote class="quote frame" style="margin:0">Knowledge Regulates. Responsibility Transforms. Education Creates a Higher Human Potential.<cite>The Capelli Institute{TM}</cite></blockquote>
    </div>
  </section>

  <section id="elements" class="alt" aria-labelledby="elements-title">
    <div class="wrap">
      <p class="eyebrow">Symbols and Meanings</p>
      <h2 id="elements-title">The Five Elements</h2>
      <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
      <ul class="elements" style="margin-top:40px">
{els}
      </ul>
      <div class="diamond frame">
        <img src="{c['image']}" alt="A glowing golden diamond, the central symbol." width="90" height="150" loading="lazy">
        <div>
          <h3>{esc(c['name'])}</h3>
          <p class="mean">{esc(c['kicker'])}</p>
          <p class="small" style="margin:0">{esc(c['line'])}</p>
        </div>
      </div>
      <p style="margin-top:28px"><a class="btn" href="books/{fep['slug']}.html">The book: {esc(fep['title'])} <span class="arrow" aria-hidden="true">→</span></a></p>
    </div>
  </section>

  <section aria-labelledby="void-title">
    <div class="wrap two">
      <div>
        <p class="eyebrow">Separation Theory</p>
        <h2 id="void-title">The space between stimulus and response</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <ul class="fact-list" style="margin-top:20px">
{chr(10).join(f'''          <li><img src="{it['image']}" alt="" width="28" height="28" style="border-radius:50%;margin-top:2px"><div><b>{esc(it['name'])}</b>{esc(it['line'])}</div></li>''' for it in void['feature']['items'])}
        </ul>
        <p style="margin-top:20px"><a class="btn sm" href="books/{void['slug']}.html">{esc(void['title'])} <span class="arrow" aria-hidden="true">→</span></a></p>
      </div>
      <div>
        <blockquote class="quote" style="margin:0 0 40px">{esc(void['pullQuote'])}<cite>{esc(CAT['author']['coverName'])}</cite></blockquote>
        <p class="eyebrow">Balanced Conscious Movement</p>
        <h2 style="font-size:24px">ZenPai</h2>
        <p class="kw" style="margin:12px 0 10px">{seps([i['name'] for i in zen['feature']['items']])}</p>
        <p class="dim" style="font-style:italic">“{esc(zen['pullQuote'])}”</p>
        <p><a class="btn sm" href="books/{zen['slug']}.html">{esc(zen['title'])} <span class="arrow" aria-hidden="true">→</span></a></p>
      </div>
    </div>
  </section>

  <section class="alt" aria-labelledby="doctrine-title">
    <div class="wrap two">
      <div>
        <p class="eyebrow">The Capelli Doctrine</p>
        <h2 id="doctrine-title">37 Principles to Live By</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <p class="kw" style="margin:16px 0">{seps(doc['keywords'])}</p>
        <p class="lede">{esc(doc['subtitle2'])}</p>
        {needs_copy("the 37 principles, or a selection of them, if the author wants them listed on the site.")}
        <p><a class="btn sm" href="books/{doc['slug']}.html">{esc(doc['title'])} <span class="arrow" aria-hidden="true">→</span></a></p>
      </div>
      <div>
        <p class="eyebrow">Universal Order</p>
        <h2 style="font-size:24px">{esc(auo['descriptionHeading'])}</h2>
        <p style="margin-top:14px">{esc(auo['description'][0])}</p>
        <p class="kw" style="margin:16px 0">{seps(auo['keywords'])}</p>
        <p><a class="btn sm" href="books/{auo['slug']}.html">{esc(auo['title'])} <span class="arrow" aria-hidden="true">→</span></a></p>
      </div>
    </div>
  </section>
"""
    write("philosophy.html", head(f"Philosophy | Principles for Conscious Living | {SITE}™", "The philosophy of The Capelli Institute: the Five Elements (Void, Wind, Fire, Water, Earth) and the Central Diamond; separation theory; balanced conscious movement; the Capelli Doctrine.", root)
          + header(root, "philosophy") + body + footer(root))

# ---------------------------------------------------------------------------
# LECTURES IN PRINT
# ---------------------------------------------------------------------------
VALUE_ICONS = [
 '<path d="M4 8c5-2 9-2 11 1 2-3 6-3 11-1v16c-5-2-9-2-11 1-2-3-6-3-11-1Z M15 9v16"/>',
 '<rect x="11" y="3" width="8" height="14" rx="4"/><path d="M6 14a9 9 0 0 0 18 0 M15 23v4 M10 27h10"/>',
 '<path d="M6 4h12l6 6v16H6Z M18 4v6h6 M10 15h10 M10 20h7"/>',
 '<path d="M15 3a8 8 0 0 0-5 14v3h10v-3a8 8 0 0 0-5-14Z M12 24h6 M13 27h4"/>',
 '<circle cx="10" cy="10" r="3"/><circle cx="20" cy="10" r="3"/><path d="M4 24c0-4 3-7 6-7s6 3 6 7 M14 24c0-4 3-7 6-7s6 3 6 7"/>',
]
def build_lectures():
    L = CAT["lectures"]; root = "../"
    vals = "\n".join(f"""        <li class="value"><div class="ic"><svg viewBox="0 0 30 30" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{VALUE_ICONS[i]}</svg></div><span>{esc(v)}</span></li>""" for i, v in enumerate(L["values"]))
    cards = "\n".join(f"""      <li class="lecture">
        <div class="art"><span class="num">No. {it['number']}</span><img src="{root}{it['image']}" alt="{esc(it['imageAlt'])}" width="400" loading="lazy"></div>
        <div class="body">
          <span class="series">Lectures in Print{TM}</span>
          <h3><a href="{it['slug']}.html">{esc(it['title'])}</a></h3>
          {f'<p class="st">{esc(it["subtitle"])}</p>' if it.get('subtitle') else ''}
          <div class="foot"><span>{esc(CAT['author']['coverName'])}</span><span>Read the synopsis →</span></div>
        </div>
      </li>""" for it in L["items"])
    body = f"""  <div class="page-head">
    <div class="wrap lip-head">
      <img src="{root}assets/img/brand/lectures-in-print-mark.png" alt="Lectures in Print emblem: an open book radiating light beneath a gold arch." width="300">
      <div>
        <ol class="crumbs" aria-label="Breadcrumb"><li><a href="{root}index.html">Home</a></li><li aria-current="page">Lectures in Print{TM}</li></ol>
        <h1>Lectures in Print{TM}</h1>
        <p class="thesis">{esc(L['tagline'])}</p>
        <p class="lede" style="margin-top:18px">{esc(L['positioning'])}</p>
      </div>
    </div>
  </div>

  <section class="tight" aria-label="What the series offers">
    <div class="wrap">
      <ul class="values" style="margin-top:0">
{vals}
      </ul>
    </div>
  </section>

  <section class="alt" aria-labelledby="catalog-title">
    <div class="wrap">
      <p class="eyebrow">The series</p>
      <h2 id="catalog-title">Lectures</h2>
      <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
      <!-- COPY NEEDED: lecture numbering. The author's sheet labels two lectures 005; 006 assigned here (Q19). -->
      <ul class="lectures" style="margin-top:36px">
{cards}
      </ul>
    </div>
  </section>

  <section aria-labelledby="inside-title">
    <div class="wrap two">
      <div><img class="spread" src="{root}assets/img/lectures/spread.jpg" alt="An open Lectures in Print volume: Lecture No. 001, The Architecture of Human Choice, with its introduction on the left page and the lecture text on the right." width="800" loading="lazy"></div>
      <div>
        <p class="eyebrow">Inside</p>
        <h2 id="inside-title">Each lecture stands alone</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <blockquote class="quote" style="margin-top:24px">{esc(L['pullQuote'])}<cite>{esc(CAT['author']['coverName'])}</cite></blockquote>
      </div>
    </div>
  </section>

  <section class="alt tight" aria-labelledby="watch-title">
    <div class="wrap">
      <p class="eyebrow">Watch</p>
      <h2 id="watch-title">The Capelli Institute channel</h2>
      <!-- COPY NEEDED: YouTube channel ID after the "Resident Mind" rename (Q8). Embed by channel ID, not vanity URL. Each lecture will link to its video. -->
      {needs_copy("the YouTube channel link once the channel is renamed from Resident Mind to The Capelli Institute, and a video link for each lecture.")}
    </div>
  </section>
"""
    write("lectures/index.html", head(f"Lectures in Print™ | {L['tagline']} | {SITE}™", L["positioning"], root) + header(root, "lectures") + body + footer(root))
    for it in L["items"]:
        build_lecture(it)

def build_lecture(it):
    root = "../"; L = CAT["lectures"]
    syn = f"<p class=\"lede\">{esc(it['synopsis'])}</p>" if it.get("synopsis") else needs_copy(f"synopsis for Lecture No. {it['number']}, {it['title']}, in the author's words.")
    excerpt = f"""
  <section aria-labelledby="excerpt-title">
    <div class="wrap narrow">
      <div class="excerpt">
        <p class="eyebrow">Lecture No. {it['number']} · The Lecture</p>
        <h3 id="excerpt-title">{esc(it['title'])}</h3>
        <p style="margin-top:14px">“{esc(it['excerpt'])}”</p>
        <cite>{esc(CAT['author']['coverName'])}</cite>
      </div>
    </div>
  </section>""" if it.get("excerpt") else ""
    thumbs = ""
    if it.get("collectorImage"):
        thumbs = f'<div class="thumbs"><button type="button" data-key="print" aria-pressed="true" aria-label="Show the print cover"><img src="{root}{it["image"]}" alt="" width="58"></button><button type="button" data-key="collector" aria-pressed="false" aria-label="Show the leather bound cover"><img src="{root}{it["collectorImage"]}" alt="" width="58"></button></div>'
        for e in it["editions"]:
            e.setdefault("image", it["image"] if e["key"] == "print" else it["collectorImage"])
            e.setdefault("imageAlt", it["imageAlt"] if e["key"] == "print" else it["collectorImageAlt"])
    else:
        for e in it["editions"]:
            e.setdefault("image", it["image"]); e.setdefault("imageAlt", it["imageAlt"])
    body = page_head(root, [("Home","index.html"),(f"Lectures in Print{TM}","lectures/index.html"),(f"No. {it['number']}",None)], esc(it["title"]), esc(it["subtitle"]) if it.get("subtitle") else None, f"Lectures in Print{TM} · Lecture No. {it['number']}") + f"""
  <section aria-label="Product">
    <div class="wrap product">
      <figure class="cover-stage" style="margin:0">
        <img data-cover src="{root}{it['image']}" alt="{esc(it['imageAlt'])}" width="700">
        <figcaption>Lecture No. {it['number']}</figcaption>
        {thumbs}
      </figure>
      <div>
        <p class="eyebrow">{esc(L['tagline'])}</p>
        <h2 class="vh">Editions and details</h2>
        <p class="author">{esc(CAT['author']['coverName'])}</p>
        <h3 style="color:var(--parchment);font-size:14px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:10px">Introduction</h3>
        {syn}
        <!-- VIDEO: each lecture gets a video on the Institute's channel. Set "video" in catalog.json once the channel is renamed (Q8). -->
{product_block(root, "lecture", it, it['editions'], it['imageAlt'])}
      </div>
    </div>
  </section>
{excerpt}
  <section class="alt tight" aria-label="Series">
    <div class="wrap" style="display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:center">
      <p class="eyebrow" style="margin:0">Lectures in Print{TM} · {esc(L['tagline'])}</p>
      <a class="btn sm" href="index.html">All lectures <span class="arrow" aria-hidden="true">→</span></a>
    </div>
  </section>
"""
    write(f"lectures/{it['slug']}.html", head(f"Lecture No. {it['number']}: {it['title']} | Lectures in Print™ | {SITE}™",
        f"Lectures in Print No. {it['number']}, {it['title']}" + (f": {it['subtitle']}" if it.get('subtitle') else "") + f". By {CAT['author']['coverName']}.", root)
        + header(root, "lectures") + body + footer(root))

# ---------------------------------------------------------------------------
# CEU — the ONE program with online registration
# ---------------------------------------------------------------------------
def build_ceu():
    root = ""
    body = page_head(root, [("Home","index.html"),("CEU's",None)], "Continuing Education Units", "Professional development", "CEU's · State of Texas CEU Provider", "assets/img/cards/card-4.jpg", "Gold laurel and mortarboard emblem.") + f"""
  <section aria-labelledby="about-title">
    <div class="wrap two wide-left">
      <div>
        <p class="eyebrow">About</p>
        <h2 id="about-title">Continuing education for clinicians and professionals</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <!-- Fact below is published by the author on thecapelligroup.com: "State of Texas CEU Provider for Continuing Education". -->
        <p class="lede">State of Texas CEU Provider for Continuing Education.</p>
        {needs_copy("what the CEU workshops cover, who they are approved for (license types), how many units each session carries, the fee, and what attendees receive, in the author's words.")}
        <ul class="fact-list" style="margin-top:20px">
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="4" width="18" height="17" rx="1"/><path d="M3 9h18 M8 2v4 M16 2v4"/></svg><div><b>Cadence</b>Workshops are held monthly. <!-- COPY NEEDED: end of month or first of month (Q3). Dates come from the Institute calendar, not hand-edited copy. --></div></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 2 20 6v6c0 5-4 9-8 10-4-1-8-5-8-10V6Z M9 12l2 2 4-4"/></svg><div><b>Provider</b>State of Texas CEU Provider <!-- COPY NEEDED: provider number and approving board(s) to list here. --></div></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-7-5-7-11a7 7 0 0 1 14 0c0 6-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg><div><b>Where</b>{esc(ADDRESS)} <!-- COPY NEEDED: confirm the CEU venue, and whether sessions are also offered online. --></div></li>
        </ul>
      </div>
      <div class="sticky">
        <div class="frame">
          <p class="eyebrow">Upcoming workshops</p>
          <!-- CALENDAR: the agreed design pulls dates from the author's Outlook calendar (SCOPE §2.4, Q12).
               Until that feed exists, sessions are listed here by hand. Each <li class="session"> is one date. -->
          <ul class="sessions">
            <li class="session">
              <div class="date"><b>—</b>Date to be announced</div>
              <div><h3>Monthly CEU Workshop</h3><p class="meta">Topic, units and fee are announced with each date.</p></div>
              <a class="btn sm" href="#register">Register</a>
            </li>
          </ul>
          {needs_copy("the next three workshop dates, topics and CEU hours.")}
        </div>
      </div>
    </div>
  </section>

  <section id="register" class="alt" aria-labelledby="register-title">
    <div class="wrap narrow">
      <p class="eyebrow">Online registration</p>
      <h2 id="register-title">Register for a CEU workshop</h2>
      <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
      <p class="lede" style="margin:20px 0 28px">This is the Institute's one program with online registration. Your registration is sent to the Institute, which confirms your place by email.</p>
      <!-- Netlify Forms: works on the Netlify deploy with no backend code. On WordPress or another host,
           replace with that platform's form handler. No payment is collected here (Q5, Q14 open). -->
      <form class="form" name="ceu-registration" method="POST" action="ceu.html?sent=1" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="ceu-registration">
        <p class="hp"><label>Leave this field empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <div class="row">
          <div><label for="r-name">Full name<span class="req" aria-hidden="true">*</span></label><input id="r-name" name="name" type="text" required autocomplete="name"></div>
          <div><label for="r-email">Email<span class="req" aria-hidden="true">*</span></label><input id="r-email" name="email" type="email" required autocomplete="email"></div>
        </div>
        <div class="row">
          <div><label for="r-phone">Phone</label><input id="r-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div><label for="r-license">License type and number</label><input id="r-license" name="license" type="text" placeholder="e.g. LPC 12345"><p class="help">Needed for the CEU certificate.</p></div>
        </div>
        <div>
          <label for="r-session">Workshop<span class="req" aria-hidden="true">*</span></label>
          <select id="r-session" name="session" required>
            <option value="">Choose a date</option>
            <option value="next">Next scheduled workshop</option>
            <!-- CALENDAR: one <option> per upcoming session. -->
          </select>
        </div>
        <div><label for="r-notes">Notes</label><textarea id="r-notes" name="notes" placeholder="Anything the Institute should know"></textarea></div>
        <div class="actions">
          <button class="btn solid" type="submit">Send registration <span class="arrow" aria-hidden="true">→</span></button>
          <span class="small dim">No payment is taken online. <!-- COPY NEEDED: whether the fee is paid at registration or at the door (Q14). --></span>
        </div>
      </form>
      <div class="form-ok" role="status">Thank you. Your registration has been sent to The Capelli Institute. You will receive a confirmation by email.</div>
    </div>
  </section>
"""
    write("ceu.html", head(f"CEU's | Continuing Education Units | {SITE}™", "Continuing Education Units at The Capelli Institute, El Paso, Texas. State of Texas CEU Provider. Monthly workshops with online registration.", root)
          + header(root, "ceu") + body + footer(root))

# ---------------------------------------------------------------------------
# IN-PERSON PROGRAMS: BIPP · Anger Resolution · Cognitive — info + phone ONLY
# ---------------------------------------------------------------------------
GUARD = """<!--
  ============================================================================
  HARD CONSTRAINT — DO NOT BREAK.
  This page is INFORMATION + A TAPPABLE PHONE NUMBER ONLY.
  No form. No online enrollment control. No calendar sign-up. No payment.
  No shared registration component may be included in this template.
  Client's words (Sam Capelli, Oct 2026 call): "I don't want them registering
  online. They have to register here in person for those two."
  Source: SCOPE.md §3.1, DESIGN-SPEC.md §6.
  ============================================================================
-->
"""
def build_bipp():
    root = "../"
    body = page_head(root, [("Home","index.html"),("BIPP Education Series",None)], "BIPP Education Series", "Domestic violence intervention &amp; prevention", "Programs · In-person enrollment", "assets/img/cards/card-5.jpg", "Silhouetted figures joining hands at sunset.") + f"""
  <section aria-labelledby="about-title">
    <div class="wrap two wide-left">
      <div>
        <p class="eyebrow">About the program</p>
        <h2 id="about-title">Battering Intervention and Prevention Program</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <!-- The facts below are the author's own, as published on thecapelligroup.com. Whether the
             Institute page should carry them, link to the clinic, or carry different copy is open
             question Q2 (one brand or two). COPY NEEDED: confirm or replace. -->
        <p class="lede">An 18-week program that satisfies the 36-hour TDCJ-CJAD and State of Texas requirement. Four phases, in English and in Spanish.</p>
        <p class="callout" style="margin:20px 0">BIPP is not an anger management program. It addresses socio-cultural issues regarding gender and violence, critical thinking, empathy, accountability, and communication.</p>
        {needs_copy("the BIPP Education Series description for the Institute site, in the author's words: what the series is, who it is for, and what a participant receives on completion.")}

        <h3 style="margin:36px 0 12px;color:var(--parchment)">How enrollment works</h3>
        <ol style="padding-left:1.3em;margin:0">
          <li><b style="font-weight:500;color:var(--parchment)">Call.</b> Phone the office to schedule an evaluation and orientation.</li>
          <li><b style="font-weight:500;color:var(--parchment)">Evaluation.</b> A psycho-social evaluation, completed in person.</li>
          <li><b style="font-weight:500;color:var(--parchment)">Orientation.</b> An interactive group session.</li>
          <li><b style="font-weight:500;color:var(--parchment)">Ongoing groups.</b> Groups of 5 to 20 people, per State of Texas BIPP Accreditation Guidelines.</li>
        </ol>
        <p class="small dim" style="margin-top:14px">Completion requires the minimum 36-hour educational group sessions and appropriate participation. Program fees are explained at enrollment.</p>

        <h3 style="margin:36px 0 12px;color:var(--parchment)">Group schedule</h3>
        <!-- COPY NEEDED: confirm these are the Institute's group times (they are the clinic's published schedule). -->
        <table class="schedule">
          <thead><tr><th scope="col">Day</th><th scope="col">Time</th><th scope="col">Group</th></tr></thead>
          <tbody>
            <tr><td>Monday</td><td>6:00 – 8:00 pm</td><td>Men's English Group</td></tr>
            <tr><td>Tuesday</td><td>6:00 – 8:00 pm</td><td>Men's Spanish Group</td></tr>
            <tr><td>Wednesday</td><td>6:00 – 8:00 pm</td><td>Women's English Group</td></tr>
            <tr><td>Saturday</td><td>11:00 am – 1:00 pm</td><td>Men's English Group</td></tr>
          </tbody>
        </table>

        <ul class="fact-list" style="margin-top:28px">
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 2 20 6v6c0 5-4 9-8 10-4-1-8-5-8-10V6Z M9 12l2 2 4-4"/></svg><div><b>Accreditation</b>Battering Intervention and Prevention Provider #071-021, accredited by the Texas Department of Criminal Justice, Community Justice Assistance Division (TDCJ-CJAD). National NCTI Court Approved Programs provider. El Paso County Court Approved Provider.</div></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 20 20 4 M8 4h12v12"/></svg><div><b>Where BIPP is not recommended</b>Affirmative Finding of Family Violence (AFV) counseling is available where the court recommends family violence counseling rather than BIPP.</div></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-7-5-7-11a7 7 0 0 1 14 0c0 6-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg><div><b>Where</b>{esc(ADDRESS)}</div></li>
        </ul>
      </div>
      <div class="sticky">
{in_person_block(root, "BIPP Education Series")}
      </div>
    </div>
  </section>
"""
    write("programs/bipp.html", GUARD + head(f"BIPP Education Series | Domestic Violence Intervention &amp; Prevention | {SITE}™".replace("&amp;","&"), f"BIPP Education Series at The Capelli Institute, El Paso, Texas. An 18-week program satisfying the 36-hour TDCJ-CJAD requirement. Enrollment is in person. Call {PHONE}.", root)
          + header(root, "bipp") + body + footer(root))

def build_anger():
    root = "../"
    body = page_head(root, [("Home","index.html"),("Anger Resolution Series",None)], "Anger Resolution Series", seps(["Regulation","Responsibility","Lasting change"]), "Programs · In-person enrollment", "assets/img/cards/card-6.jpg", "A mountain peak above cloud at dawn.") + f"""
  <section aria-labelledby="about-title">
    <div class="wrap two wide-left">
      <div>
        <p class="eyebrow">About the program</p>
        <h2 id="about-title">Therapeutic anger resolution</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <!-- The facts below are the author's own, as published on thecapelligroup.com (Q2 applies).
             COPY NEEDED: confirm or replace with Institute-specific copy. -->
        <p class="lede">A Texas Court Approved program of 8 to 16 hours, depending on the court order. Court-mandated or self-referred. A certificate of completion is awarded.</p>
        {needs_copy("the Anger Resolution Series description for the Institute site, in the author's words: what the series teaches, who it is for, and how the sessions run.")}
        <ul class="fact-list" style="margin-top:28px">
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="4" width="18" height="17" rx="1"/><path d="M3 9h18 M8 2v4 M16 2v4"/></svg><div><b>Schedule</b>Every Saturday, 9:30 – 10:30 am. <!-- COPY NEEDED: confirm for the Institute. --></div></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 2 20 6v6c0 5-4 9-8 10-4-1-8-5-8-10V6Z M9 12l2 2 4-4"/></svg><div><b>Approach</b>Built on Personalized Theory{TM}, developed by Samuel Capelli. Curriculum designed for probationers and parolees. One-on-one therapy is available.</div></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/></svg><div><b>Certification</b>Certified Anger Resolution Clinical Therapy Provider, License #2524-5741.</div></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-7-5-7-11a7 7 0 0 1 14 0c0 6-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg><div><b>Where</b>{esc(ADDRESS)}</div></li>
        </ul>
      </div>
      <div class="sticky">
{in_person_block(root, "Anger Resolution Series")}
      </div>
    </div>
  </section>
"""
    write("programs/anger-resolution.html", GUARD + head(f"Anger Resolution Series | Regulation · Responsibility · Lasting Change | {SITE}™", f"Anger Resolution Series at The Capelli Institute, El Paso, Texas. Texas Court Approved, 8 to 16 hours. Enrollment is in person. Call {PHONE}.", root)
          + header(root, "anger") + body + footer(root))

def build_cognitive():
    root = "../"
    body = page_head(root, [("Home","index.html"),("Cognitive Programs",None)], "Cognitive Programs", seps(["Think","Regulate","Choose","Evolve"]), "Programs · In-person enrollment", "assets/img/cards/card-7.jpg", "An illuminated brain within a neural network.") + f"""
  <section aria-labelledby="about-title">
    <div class="wrap two wide-left">
      <div>
        <p class="eyebrow">About the programs</p>
        <h2 id="about-title">Think. Regulate. Choose. Evolve.</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <!-- No copy for Cognitive Programs exists on any sheet the author sent. Treated as in-person,
             the same as BIPP and Anger Resolution, until he says otherwise (Q11). -->
        {needs_copy("the Cognitive Programs description: what the programs are, who they serve, how long they run, and what a participant receives on completion, in the author's words.")}
        {needs_copy("the Cognitive Programs schedule.")}
      </div>
      <div class="sticky">
{in_person_block(root, "Cognitive Programs")}
      </div>
    </div>
  </section>
"""
    write("programs/cognitive-programs.html", GUARD + head(f"Cognitive Programs | Think · Regulate · Choose · Evolve | {SITE}™", f"Cognitive Programs at The Capelli Institute, El Paso, Texas. Enrollment is in person. Call {PHONE}.", root)
          + header(root, "cognitive") + body + footer(root))

# ---------------------------------------------------------------------------
# WORKSHOPS / SEMINARS — inquiry form (not a purchase, not a registration)
# ---------------------------------------------------------------------------
def build_workshops():
    root = ""
    body = page_head(root, [("Home","index.html"),("Workshops Seminars",None)], "Workshops &amp; Seminars", seps(["Live training","Practical application","Real-world change"]), "For organizations", "assets/img/cards/card-8.jpg", "A speaker addressing a seated audience.") + f"""
  <section aria-labelledby="about-title">
    <div class="wrap two">
      <div>
        <p class="eyebrow">On site, at your organization</p>
        <h2 id="about-title">Bring the Institute to your place of business</h2>
        <div class="rule left" aria-hidden="true"><span class="dia"></span></div>
        <p class="lede">Organizations can request a workshop or seminar delivered at their own location.</p>
        {needs_copy("the workshop and seminar offering: topics available, typical length, audience, and what an organization receives, in the author's words.")}
        <p class="eyebrow" style="margin-top:28px">Topics drawn from the Institute's published work</p>
        <ul class="fact-list">
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 7c4-2 7-2 8 1 1-3 4-3 8-1v12c-4-2-7-2-8 1-1-3-4-3-8-1Z M12 8v12"/></svg><div><b>Lectures in Print{TM}</b>{"; ".join(esc(i["title"]) for i in CAT["lectures"]["items"])}.</div></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="8" r="5"/><circle cx="8" cy="15" r="5"/><circle cx="16" cy="15" r="5"/></svg><div><b>Philosophy</b>The Five Elements; separation theory; balanced conscious movement; the Capelli Doctrine.</div></li>
        </ul>
      </div>
      <div>
        <p class="eyebrow">Request a workshop</p>
        <h2 style="font-size:24px;margin-bottom:18px">Tell us about your organization</h2>
        <!-- Netlify Forms inquiry. Delivered to the Institute by email. Not a purchase, not a registration. -->
        <form class="form" name="workshop-inquiry" method="POST" action="workshops.html?sent=1" data-netlify="true" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="workshop-inquiry">
          <p class="hp"><label>Leave this field empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
          <div><label for="w-org">Organization<span class="req" aria-hidden="true">*</span></label><input id="w-org" name="organization" type="text" required autocomplete="organization"></div>
          <div class="row">
            <div><label for="w-name">Contact name<span class="req" aria-hidden="true">*</span></label><input id="w-name" name="name" type="text" required autocomplete="name"></div>
            <div><label for="w-email">Email<span class="req" aria-hidden="true">*</span></label><input id="w-email" name="email" type="email" required autocomplete="email"></div>
          </div>
          <div class="row">
            <div><label for="w-phone">Phone</label><input id="w-phone" name="phone" type="tel" autocomplete="tel"></div>
            <div><label for="w-size">Audience size</label><input id="w-size" name="audience" type="text" placeholder="e.g. 25"></div>
          </div>
          <div class="row">
            <div><label for="w-dates">Preferred dates</label><input id="w-dates" name="dates" type="text" placeholder="e.g. March, any Friday"></div>
            <div><label for="w-topic">Topic of interest</label><input id="w-topic" name="topic" type="text"></div>
          </div>
          <div><label for="w-msg">Message</label><textarea id="w-msg" name="message" placeholder="Where, who is attending, and what you hope they take away"></textarea></div>
          <div class="actions"><button class="btn solid" type="submit">Send inquiry <span class="arrow" aria-hidden="true">→</span></button></div>
        </form>
        <div class="form-ok" role="status">Thank you. Your inquiry has been sent to The Capelli Institute. We will reply by email.</div>
      </div>
    </div>
  </section>
"""
    write("workshops.html", head(f"Workshops & Seminars | Live Training · Practical Application · Real-World Change | {SITE}™", "Workshops and seminars from The Capelli Institute, delivered at your organization. Request a workshop.", root)
          + header(root, "workshops") + body + footer(root))

# ---------------------------------------------------------------------------
# COMING SOON (standalone teaser), 404, LEGAL
# ---------------------------------------------------------------------------
def build_coming_soon():
    root = ""
    mini = "\n".join(f'        <li><img src="assets/img/{img}" alt="" width="200" height="200" loading="lazy"><b>{title}</b></li>' for _, _, title, _, img, _ in CARDS)
    content = f"""{head(f"Coming Soon · Early January 2027 | {SITE}™", "The Capelli Institute is coming early January 2027. A comprehensive educational platform for clinicians, professionals, and seekers of knowledge. Join the early access mailing list.", root, "teaser-page")}
<header class="band" style="border-bottom:none">
  <div class="wrap">
    <div class="crest"><img src="assets/img/brand/crest.png" width="260" height="267" alt="The Capelli crest."></div>
    <div class="wordmark">
      <span class="name">The Capelli Institute{TM}</span>
      <span class="pillars">Education <span class="sep">•</span> Research <span class="sep">•</span> Certification <span class="sep">•</span> Publishing</span>
    </div>
    <div class="motto">
      <img class="roundel" src="assets/img/brand/roundel.png" width="200" height="200" alt="Gold tree-of-life roundel.">
      <p>Know Thyself<br>Master Thy Life<br>Ascend to Higher<br>Frequencies</p>
    </div>
  </div>
</header>

<main id="main" class="teaser">
  <div class="inner">
    <p class="thesis">Advancing Clinical Education Through Research, Innovation, and Psychological Science.</p>
    <h1>Coming Soon</h1>
    <p class="when">Early January 2027</p>
    <div class="rule center" aria-hidden="true"><span class="dia"></span></div>
    <p class="platform">A comprehensive educational platform for clinicians, professionals, and seekers of knowledge.</p>

    <ul class="teaser-cards" aria-label="What is coming">
{mini}
    </ul>

    <div class="capture-wrap frame">
      <div class="qr">
        <!-- QR: the code from the author's own teaser art. COPY NEEDED: confirm the URL it encodes points at
             this page on the final domain (Q1) BEFORE anything is printed. Regenerate if not. -->
        <img src="assets/img/brand/qr-from-sam.png" alt="QR code linking to the early access mailing list." width="150" height="150">
        <small>Scan to join</small>
      </div>
      <div>
        <p class="capture-head"><small>Scan to join our</small>Early Access Mailing List</p>
        <p class="capture-sub">Be the first to receive updates, new programs, book releases, workshops and launch information.</p>
        <form class="capture" name="early-access" method="POST" action="coming-soon.html?sent=1" data-netlify="true" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="early-access">
          <p class="hp"><label>Leave this field empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
          <label class="vh" for="t-email">Email address</label>
          <input id="t-email" name="email" type="email" required autocomplete="email" placeholder="Your email address">
          <button class="btn solid" type="submit">Join the list</button>
        </form>
        <p class="capture-ok" role="status">Thank you. You are on the list. We will write when the Institute opens.</p>
        <p class="capture-note">Your address is used only to send launch news from The Capelli Institute{TM}. No tracking, no third parties.</p>
      </div>
    </div>

    <p class="teaser-rail">Knowledge Regulates. Responsibility Transforms. <em>Education</em> Creates a Higher Human Potential.</p>
  </div>
</main>
<footer class="teaser-foot">&copy; 2026 The Capelli Institute{TM} · El Paso, Texas · <a href="index.html" style="color:inherit">Enter the site</a></footer>
<script src="assets/js/institute.js"></script>
</body>
</html>
"""
    write("coming-soon.html", content)

def build_404():
    root = "/"
    # Absolute paths: a 404 is served at any depth.
    body = f"""  <section class="simple" aria-labelledby="nf-title">
    <div class="wrap" style="text-align:center">
      <div class="big-404" aria-hidden="true">404</div>
      <h1 id="nf-title">That page is not here</h1>
      <p class="lede" style="margin:0 auto 28px">The address may be mistyped, or the page may have moved. Everything the Institute publishes is reachable from the menu above.</p>
      <div class="btn-row" style="justify-content:center">
        <a class="btn" href="/index.html">Home <span class="arrow" aria-hidden="true">→</span></a>
        <a class="btn ghost" href="/books/index.html">Books</a>
        <a class="btn ghost" href="/lectures/index.html">Lectures in Print{TM}</a>
      </div>
    </div>
  </section>
"""
    write("404.html", head(f"Page not found | {SITE}™", "The page you asked for is not here.", root) + header(root, None) + body + footer(root))

def build_legal():
    root = "../"
    priv = page_head(root, [("Home","index.html"),("Privacy",None)], "Privacy", None, "Legal") + f"""
  <section class="simple" aria-label="Privacy policy">
    <div class="wrap">
      <div class="notice"><b>Client-supplied document</b>This page is a placeholder. The privacy policy is The Capelli Institute's own legal document and must be supplied or approved by the Institute before launch (SCOPE.md Q9). The list below states what this site actually does, so the policy can be written against it.</div>
      <!-- COPY NEEDED: privacy policy text, supplied or approved by the Institute. -->
      <h2>What this website collects</h2>
      <ul>
        <li>The early access mailing list: an email address, only when you submit it on the launch notice page.</li>
        <li>CEU workshop registration: name, email, phone, license details, chosen session, and any notes you add.</li>
        <li>Workshop inquiries from organizations: organization, contact name, email, phone, and the details of your request.</li>
      </ul>
      <h2>What it does not do</h2>
      <ul>
        <li>No analytics, no advertising pixels, no social media beacons, no third-party scripts. Fonts are served from this site.</li>
        <li>No cookies are set by this site.</li>
        <li>The BIPP Education Series, Anger Resolution Series and Cognitive Programs pages collect nothing. Enrollment for those programs is in person.</li>
        <li>Nothing resembling clinical information is requested anywhere on this site.</li>
      </ul>
      <h2>Purchases</h2>
      <p>Books and lectures are purchased through outside booksellers. This site does not take payment and does not hold payment details.</p>
    </div>
  </section>
"""
    write("legal/privacy.html", head(f"Privacy | {SITE}™", "Privacy notice for The Capelli Institute website.", root) + header(root, None) + priv + footer(root))
    terms = page_head(root, [("Home","index.html"),("Terms",None)], "Terms", None, "Legal") + f"""
  <section class="simple" aria-label="Terms">
    <div class="wrap">
      <div class="notice"><b>Client-supplied document</b>This page is a placeholder. Terms of use, and terms of sale if the Institute ever sells directly, are the Institute's own legal documents and must be supplied or approved before launch (SCOPE.md Q9, Q10).</div>
      <!-- COPY NEEDED: terms of use, supplied or approved by the Institute. -->
      <h2>Trademark</h2>
      <p>The Capelli Institute{TM} and Lectures in Print{TM} are trademarks of The Capelli Institute. Registration is pending.</p>
      <h2>Copyright</h2>
      <p>All written works, book covers and lecture texts shown on this site are &copy; Samuel Capelli. All rights reserved.</p>
      <h2>Continuing education and programs</h2>
      <p>CEU workshop registration is confirmed by the Institute by email. Enrollment in the BIPP Education Series, the Anger Resolution Series and the Cognitive Programs is completed in person at the office.</p>
    </div>
  </section>
"""
    write("legal/terms.html", head(f"Terms | {SITE}™", "Terms for The Capelli Institute website.", root) + header(root, None) + terms + footer(root))

# ---------------------------------------------------------------------------
def build_catalog_js():
    data = json.dumps(CAT, ensure_ascii=False, separators=(",", ":"))
    write("assets/data/catalog.js", "/* DERIVED FILE — generated from assets/data/catalog.json by tools/build-pages.py. Edit the JSON, not this. */\nwindow.CAPELLI_CATALOG=" + data + ";\n")

if __name__ == "__main__":
    build_home(); build_books(); build_philosophy(); build_lectures(); build_ceu()
    build_bipp(); build_anger(); build_cognitive(); build_workshops()
    build_coming_soon(); build_404(); build_legal(); build_catalog_js()
