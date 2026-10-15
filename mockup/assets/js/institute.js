/* The Capelli Institute — mockup behaviours. No dependencies, no network. */
(function () {
  'use strict';

  /* Mobile nav toggle */
  var btn = document.querySelector('.menu-btn');
  var list = document.querySelector('.nav ul');
  if (btn && list) {
    btn.addEventListener('click', function () {
      var open = list.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* Edition variant selector (product pages).
     Each radio carries data-* for the fields it drives; the panel elements carry
     data-field="<name>". Placeholders: a value of "" leaves the slot marked TBD. */
  var variants = document.querySelector('[data-variants]');
  if (variants) {
    var panel = document.querySelector('[data-variant-panel]');
    var cover = document.querySelector('[data-cover]');
    var apply = function (radio) {
      if (!radio) return;
      var d = radio.dataset;
      panel.querySelectorAll('[data-field]').forEach(function (el) {
        var key = el.getAttribute('data-field');
        var val = d[key];
        if (key === 'price') {
          if (val) { el.textContent = val; el.removeAttribute('data-placeholder'); }
          else { el.textContent = '$—'; el.setAttribute('data-placeholder', 'price'); }
        } else if (key === 'isbn') {
          el.textContent = val || 'ISBN to be assigned';
          if (val) el.removeAttribute('data-placeholder'); else el.setAttribute('data-placeholder', 'isbn');
        } else {
          el.textContent = val || '';
        }
      });
      if (cover) cover.setAttribute('data-edition', d.edition || '');
      panel.setAttribute('data-current', d.edition || '');
    };
    variants.addEventListener('change', function (e) {
      if (e.target && e.target.matches('input[type=radio]')) apply(e.target);
    });
    apply(variants.querySelector('input[type=radio]:checked'));
  }

  /* Coming-soon capture: no backend in the mockup. Prevent the submit, show the note. */
  var capture = document.querySelector('form.capture');
  if (capture) {
    capture.addEventListener('submit', function (e) {
      e.preventDefault();
      capture.classList.add('sent');
    });
  }
})();
