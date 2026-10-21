/*
 * Tool page (pipeline.html): the description's "more" link, copy buttons,
 * the optional-inputs toggle and the CBRAIN dataset chooser.
 * Plain JavaScript; Bootstrap 5 (loaded by base_main.html) is used for the
 * CBRAIN modal when it is present, with a direct link otherwise.
 */
(function () {
  'use strict';

  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); } else { document.addEventListener('DOMContentLoaded', fn); }
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function initMore() {
    var desc = document.getElementById('tp-desc');
    var btn = document.querySelector('.tp-more');
    if (!desc || !btn) { return; }
    function check() {
      if (desc.classList.contains('is-open')) { btn.hidden = false; return; }
      btn.hidden = desc.scrollHeight <= desc.clientHeight + 2;
    }
    btn.addEventListener('click', function () {
      var open = desc.classList.toggle('is-open');
      btn.textContent = open ? 'less' : 'more';
      btn.setAttribute('aria-expanded', String(open));
    });
    check();
    window.addEventListener('resize', check);
  }

  function copyText(text, done) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () {});
      return;
    }
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'absolute';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) { /* ignore */ }
    document.body.removeChild(ta);
  }

  function initCopy() {
    document.querySelectorAll('.tp-copy').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var code = btn.parentNode.querySelector('code');
        if (!code) { return; }
        copyText(code.textContent.trim(), function () {
          btn.classList.add('is-copied');
          btn.title = 'Copied';
          setTimeout(function () { btn.classList.remove('is-copied'); btn.title = 'Copy'; }, 1500);
        });
      });
    });
  }

  function initOptionalInputs() {
    var btn = document.querySelector('.tp-toggle');
    var body = document.getElementById('tp-optional');
    if (!btn || !body) { return; }
    btn.addEventListener('click', function () {
      var show = body.hidden;
      body.hidden = !show;
      btn.textContent = show ? btn.dataset.hide : btn.dataset.show;
      btn.setAttribute('aria-expanded', String(show));
    });
  }

  // Group (dataset) ids come as ".../groups/switch?id=123", "...?id%3D123" or,
  // through /cbrainredirect, "...switch?id%3D123". Tool links are either plain
  // CBRAIN URLs or /cbrainredirect?cbrainurl=<URL with an encoded query>.
  function cbrainGroupId(url) {
    var m = /[?&]id(?:=|%3D)(\d+)/i.exec(url || '') || /(?:%3F|%26)id%3D(\d+)/i.exec(url || '');
    return m ? m[1] : '';
  }
  function withSwitchGroup(url, id) {
    if (!id) { return url; }
    var encoded = url.indexOf('cbrainredirect') >= 0;
    var sep = encoded ? '%26' : (url.indexOf('?') >= 0 ? '&' : '?');
    return url + sep + 'switch_group_id' + (encoded ? '%3D' : '=') + id;
  }

  // CBRAIN: choose a dataset to process (or none), as on the Tools page.
  function initCbrain() {
    var btn = document.querySelector('[data-tp-cbrain]');
    var body = document.getElementById('cbrainModalBody');
    if (!btn) { return; }
    var card = document.querySelector('.tp-card');
    var title = card ? card.dataset.toolTitle : '';
    var launch = btn.dataset.launchUrl;

    btn.addEventListener('click', function () {
      if (!body || !window.bootstrap) { window.open(launch, '_blank', 'noopener'); return; }
      body.innerHTML =
        '<p>You\'re about to launch <strong>' + escapeHtml(title) + '</strong> on CBRAIN. Please select a dataset to process with this tool (or "None" to load only the tool).</p>' +
        '<p>Not all tools are compatible with all datasets. Please make sure you are <a href="https://portal.cbrain.mcgill.ca" target="_blank" rel="noreferrer">logged into CBRAIN</a> first.</p>' +
        '<div class="list-group" id="tpCbrainList"><a class="list-group-item list-group-item-action" target="_blank" rel="noreferrer" href="' + escapeHtml(launch) + '">None</a></div>';
      var modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('cbrainModal'));
      modal.show();
      var list = document.getElementById('tpCbrainList');
      list.addEventListener('click', function (e) { if (e.target.closest('a')) { modal.hide(); } });
      fetch(btn.dataset.datasetsUrl + '?max_per_page=All&cbrain=true&sortKey=title')
        .then(function (r) { return r.ok ? r.json() : { elements: [] }; })
        .then(function (json) {
          (json.elements || []).forEach(function (el) {
            var id = cbrainGroupId(el.cbrain_id);
            if (!id) { return; }
            var a = document.createElement('a');
            a.className = 'list-group-item list-group-item-action';
            a.target = '_blank';
            a.rel = 'noreferrer';
            a.href = withSwitchGroup(launch, id);
            a.textContent = el.title;
            list.appendChild(a);
          });
        })
        .catch(function (err) { console.error(err); });
    });
  }

  ready(function () {
    initMore();
    initCopy();
    initOptionalInputs();
    initCbrain();
  });
})();
