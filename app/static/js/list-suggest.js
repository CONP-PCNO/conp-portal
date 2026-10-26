/*
 * Type-ahead for the list pages' search boxes (Data, Tools & Pipelines,
 * Experiments), the same behaviour as the home page's search box: after two
 * characters the browser's suggestion list offers matching titles and
 * keywords; picking one runs the search straight away.
 *
 *   <input data-suggest-url="/dataset-search-suggestions" list="…">
 *       asks the server ({"datasets": [...], "suggestions": [...]});
 *   <input data-suggest-terms="lp-terms" list="…">
 *       filters the terms in <script type="application/json" id="lp-terms">.
 */
(function () {
  'use strict';

  function norm(s) {
    return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }

  function init(input) {
    var list = document.getElementById(input.getAttribute('list'));
    if (!list) { return; }
    var url = input.getAttribute('data-suggest-url');
    var termsId = input.getAttribute('data-suggest-terms');
    var terms = [];
    if (termsId) {
      try { terms = JSON.parse(document.getElementById(termsId).textContent) || []; } catch (e) { terms = []; }
    }
    var shown = [];
    var timer = null;
    var last = '';

    function render(items) {
      list.innerHTML = '';
      items.slice(0, 15).forEach(function (value) {
        var option = document.createElement('option');
        option.value = value;
        list.appendChild(option);
      });
      shown = items;
    }

    function local(query) {
      var q = norm(query);
      var starts = [], contains = [];
      terms.forEach(function (t) {
        var n = norm(t);
        if (n.indexOf(q) === 0) { starts.push(t); } else if (n.indexOf(q) !== -1) { contains.push(t); }
      });
      return starts.concat(contains);
    }

    input.addEventListener('input', function (e) {
      // A suggestion picked from the list arrives without an inputType
      // (Firefox) or as insertReplacementText (Chrome, Safari).
      var picked = !e.inputType || e.inputType === 'insertReplacementText';
      if (picked && shown.indexOf(input.value) !== -1) {
        input.form.submit();
        return;
      }
      var query = input.value.trim();
      clearTimeout(timer);
      if (query.length < 2) { render([]); last = ''; return; }
      if (!url) { render(local(query)); return; }
      if (!window.fetch) { return; }
      timer = setTimeout(function () {
        if (query === last) { return; }
        last = query;
        fetch(url + '?search=' + encodeURIComponent(query))
          .then(function (response) { return response.json(); })
          .then(function (json) {
            if (input.value.trim() !== query) { return; }
            render((json.datasets || []).concat(json.suggestions || []));
          })
          .catch(function () {});
      }, 150);
    });
  }

  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); } else { document.addEventListener('DOMContentLoaded', fn); }
  }
  ready(function () {
    [].forEach.call(document.querySelectorAll('input[data-suggest-url], input[data-suggest-terms]'), init);
  });
})();
