/* Tooltips that appear at once (the browser's own, from title="...", wait
   about a second and can't be made faster). Shown for any element with
   data-tip="...", and for elements with a title inside a container marked
   data-quick-tips (their title becomes the tip, so the browser's own no
   longer doubles it). Follows the pointer; also shown on keyboard focus. */
(function () {
  'use strict';
  var tip = null;
  var current = null;

  function box() {
    if (tip) { return tip; }
    var style = document.createElement('style');
    style.textContent =
      '.quick-tip{position:fixed;z-index:2000;max-width:320px;padding:5px 9px;border-radius:5px;' +
      'background:#1d2129;color:#fff;font-size:13px;line-height:1.35;pointer-events:none;' +
      'box-shadow:0 2px 8px rgba(0,0,0,.18);white-space:pre-line}' +
      '.quick-tip[hidden]{display:none}' +
      '[data-tip]{cursor:default}a[data-tip],button[data-tip],[data-tip] a{cursor:pointer}';
    document.head.appendChild(style);
    tip = document.createElement('div');
    tip.className = 'quick-tip';
    tip.setAttribute('role', 'tooltip');
    tip.hidden = true;
    document.body.appendChild(tip);
    return tip;
  }

  function target(el) {
    while (el && el !== document) {
      if (el.nodeType === 1) {
        if (el.hasAttribute('data-tip')) { return el; }
        if (el.hasAttribute('title') && el.closest && el.closest('[data-quick-tips]')) {
          var t = el.getAttribute('title');
          if (t) {
            el.setAttribute('data-tip', t);
            if (!el.hasAttribute('aria-label') && !el.textContent.trim()) { el.setAttribute('aria-label', t); }
          }
          el.removeAttribute('title');
          return t ? el : null;
        }
      }
      el = el.parentNode;
    }
    return null;
  }

  function place(x, y) {
    var t = box();
    var w = t.offsetWidth;
    var h = t.offsetHeight;
    var left = Math.min(x + 14, window.innerWidth - w - 8);
    var top = y + 18;
    if (top + h > window.innerHeight - 8) { top = y - h - 12; }
    t.style.left = Math.max(8, left) + 'px';
    t.style.top = Math.max(8, top) + 'px';
  }

  function show(el, x, y) {
    var t = box();
    current = el;
    t.textContent = el.getAttribute('data-tip');
    t.hidden = false;
    place(x, y);
  }

  function hide() {
    current = null;
    if (tip) { tip.hidden = true; }
  }

  document.addEventListener('mouseover', function (e) {
    var el = target(e.target);
    if (el) { show(el, e.clientX, e.clientY); } else if (current) { hide(); }
  });
  document.addEventListener('mousemove', function (e) {
    if (current) { place(e.clientX, e.clientY); }
  });
  document.addEventListener('mouseout', function (e) {
    if (current && (!e.relatedTarget || target(e.relatedTarget) !== current)) { hide(); }
  });
  document.addEventListener('focusin', function (e) {
    var el = target(e.target);
    if (el) {
      var r = el.getBoundingClientRect();
      show(el, r.left, r.bottom - 10);
    }
  });
  document.addEventListener('focusout', hide);
  document.addEventListener('scroll', hide, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { hide(); } });
}());
