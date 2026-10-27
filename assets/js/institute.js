/* The Capelli Institute™ — site behaviours. No dependencies, no network, no tracking.
   Works from file:// and from a web server. Every page is complete without this file;
   it only enhances. */
(function () {
  'use strict';

  /* ---- Mobile nav toggle ---- */
  var btn = document.querySelector('.menu-btn');
  var list = document.querySelector('.nav ul');
  if (btn && list) {
    btn.addEventListener('click', function () {
      var open = list.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && list.classList.contains('open')) {
        list.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  }

  /* ---- Edition selector (product pages) ----
     The page is rendered from assets/data/catalog.json. The radios carry the edition key;
     the catalog is read from window.CAPELLI_CATALOG (assets/data/catalog.js, derived from the
     same JSON) so a future checkout can read the same structure. */
  var variants = document.querySelector('[data-variants]');
  var catalog = window.CAPELLI_CATALOG;
  if (variants && catalog) {
    var kind = variants.getAttribute('data-kind');        // "book" | "lecture"
    var slug = variants.getAttribute('data-slug');
    var pool = kind === 'lecture' ? catalog.lectures.items : catalog.books;
    var item = null;
    for (var i = 0; i < pool.length; i++) { if (pool[i].slug === slug) { item = pool[i]; break; } }
    var panel = document.querySelector('[data-variant-panel]');
    var cover = document.querySelector('[data-cover]');
    var caption = document.querySelector('.cover-stage figcaption');
    var thumbs = document.querySelectorAll('.thumbs button');

    var money = function (n) {
      if (n === null || n === undefined || n === '') return null;
      return '$' + Number(n).toFixed(2);
    };

    var setCover = function (src, alt) {
      if (!cover || !src) return;
      if (cover.getAttribute('src') === src) return;
      cover.classList.add('swap');
      var img = new Image();
      img.onload = function () { cover.src = src; cover.alt = alt || ''; cover.classList.remove('swap'); };
      img.src = src;
    };

    var apply = function (key) {
      if (!item || !panel) return;
      var ed = null;
      for (var j = 0; j < item.editions.length; j++) { if (item.editions[j].key === key) { ed = item.editions[j]; break; } }
      if (!ed) return;
      var set = function (field, value, placeholder) {
        var el = panel.querySelector('[data-field="' + field + '"]');
        if (!el) return;
        if (value) { el.textContent = value; el.removeAttribute('data-placeholder'); }
        else { el.textContent = placeholder; el.setAttribute('data-placeholder', field); }
      };
      set('name', ed.name, '');
      set('binding', ed.binding, '');
      set('tagline', ed.tagline, '—');
      set('isbn', ed.isbn, 'To be assigned');
      set('sku', ed.sku, '');
      set('price', money(ed.price), '$—');
      /* Purchase controls. Only an https address becomes a link; anything else is the honest
         "Available soon" state with no href at all. The Amazon link is hidden when the edition
         has none. The two notes follow the same facts. */
      var safeUrl = function (u) { return typeof u === 'string' && /^https:\/\/\S+$/.test(u) ? u : null; };
      var arrow = function () {
        var s = document.createElement('span');
        s.className = 'arrow'; s.setAttribute('aria-hidden', 'true'); s.textContent = '→';
        return s;
      };
      var buyUrl = safeUrl(ed.buyUrl), amazonUrl = safeUrl(ed.amazonUrl);
      var buy = panel.querySelector('[data-buy]');
      if (buy) {
        if (buyUrl) {
          buy.setAttribute('href', buyUrl);
          buy.removeAttribute('aria-disabled');
          buy.setAttribute('rel', 'noopener');
          buy.setAttribute('target', '_blank');
          buy.textContent = 'Buy this edition ';
          buy.appendChild(arrow());
        } else {
          buy.removeAttribute('href');
          buy.removeAttribute('rel');
          buy.removeAttribute('target');
          buy.setAttribute('aria-disabled', 'true');
          buy.textContent = 'Available soon';
        }
      }
      var amz = panel.querySelector('[data-amazon]');
      if (amz) {
        if (amazonUrl) {
          amz.setAttribute('href', amazonUrl);
          amz.setAttribute('rel', 'noopener');
          amz.setAttribute('target', '_blank');
          amz.hidden = false;
        } else {
          amz.removeAttribute('href');
          amz.removeAttribute('rel');
          amz.removeAttribute('target');
          amz.hidden = true;
        }
      }
      var payNote = panel.querySelector('[data-pay-note]');
      if (payNote) payNote.hidden = !buyUrl;
      var phNote = panel.querySelector('[data-ph-note]');
      if (phNote) phNote.hidden = !!(buyUrl && ed.price !== null && ed.price !== undefined && ed.price !== '');
      panel.setAttribute('data-current', key);
      /* Book captions name the cover actually shown, so they only change when the edition has its own
         cover art; an edition without art leaves the previous cover and its caption in place.
         Lecture captions carry the lecture number and stay put. */
      if (ed.image) {
        setCover(ed.image.replace(/^assets\//, variants.getAttribute('data-root') + 'assets/'), ed.imageAlt);
        if (caption && kind === 'book') caption.textContent = ed.name;
      }
      thumbs.forEach(function (t) { t.setAttribute('aria-pressed', t.getAttribute('data-key') === key ? 'true' : 'false'); });
    };

    variants.addEventListener('change', function (e) {
      if (e.target && e.target.matches('input[type=radio]')) apply(e.target.value);
    });
    panel && panel.addEventListener('click', function (e) {
      var a = e.target.closest('[data-buy]');
      if (a && a.getAttribute('aria-disabled') === 'true') e.preventDefault();
    });
    thumbs.forEach(function (t) {
      t.addEventListener('click', function () {
        var r = variants.querySelector('input[value="' + t.getAttribute('data-key') + '"]');
        if (r) { r.checked = true; apply(r.value); }
      });
    });
    var checked = variants.querySelector('input[type=radio]:checked');
    if (checked) apply(checked.value);
  }

  /* ---- Forms (CEU registration, workshop inquiry, coming-soon capture) ----
     The generator stamps each form with data-form="preview" or data-form="live" (FORM_ENDPOINT in
     tools/build-pages.py). Live forms post to their endpoint untouched. Preview forms are stopped
     here and the status box says plainly that nothing was sent, so no submission is ever lost
     silently. The in-person program pages contain no form at all. */
  var forms = document.querySelectorAll('form[data-form="preview"]');
  forms.forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      f.classList.add('sent');
      var ok = f.nextElementSibling;
      if (ok) {
        var note = ok.getAttribute('data-preview');
        if (note) ok.textContent = note;
        ok.setAttribute('tabindex', '-1'); ok.focus();
      }
    });
  });
  /* ---- Resonant Mind video facades ----
     Each video is a link to YouTube carrying data-yt="<video id>". On activation (click, Enter, Space) the link is
     replaced by the cookieless player (youtube-nocookie.com) with autoplay, so YouTube is contacted only once the
     visitor has asked for that video. Without this script the link simply opens the video on YouTube. */
  var facades = document.querySelectorAll('a.yt[data-yt]');
  Array.prototype.forEach.call(facades, function (a) {
    var id = a.getAttribute('data-yt') || '';
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) { return; }
    a.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button === 1) { return; } // let "open in new tab" through
      e.preventDefault();
      var title = a.getAttribute('data-title') || 'Resonant Mind video';
      var box = document.createElement('div');
      box.className = 'yt-frame';
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
      f.title = title;
      f.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
      f.setAttribute('allowfullscreen', '');
      f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
      f.setAttribute('loading', 'eager');
      box.appendChild(f);
      a.parentNode.replaceChild(box, a);
      f.focus();
    });
  });

  /* A live endpoint that redirects back with ?sent=1 lands here and shows the real confirmation. */
  if (/[?&]sent=1/.test(location.search)) {
    var sentForm = document.querySelector('form[data-form="live"]');
    if (sentForm) { sentForm.classList.add('sent'); }
  }
})();
