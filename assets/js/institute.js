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
      var buy = panel.querySelector('[data-buy]');
      if (buy) {
        if (ed.buyUrl) {
          buy.setAttribute('href', ed.buyUrl);
          buy.removeAttribute('aria-disabled');
          buy.setAttribute('rel', 'noopener');
          buy.setAttribute('target', '_blank');
        } else {
          buy.setAttribute('href', '#');
          buy.setAttribute('aria-disabled', 'true');
          buy.removeAttribute('target');
        }
      }
      panel.setAttribute('data-current', key);
      if (ed.image) setCover(ed.image.replace(/^assets\//, variants.getAttribute('data-root') + 'assets/'), ed.imageAlt);
      /* Book captions name the edition shown; lecture captions carry the lecture number and stay put. */
      if (caption && kind === 'book') caption.textContent = ed.name;
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
  /* A live endpoint that redirects back with ?sent=1 lands here and shows the real confirmation. */
  if (/[?&]sent=1/.test(location.search)) {
    var sentForm = document.querySelector('form[data-form="live"]');
    if (sentForm) { sentForm.classList.add('sent'); }
  }
})();
