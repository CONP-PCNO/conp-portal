/*
 * Dataset landing page (dataset.html): tabs, the description's "more" link,
 * copy buttons, the download confirmation and the CBRAIN pipeline chooser.
 * Plain JavaScript; Bootstrap 5 (loaded by base_main.html) is used for the
 * two modals when it is present, with simple fallbacks otherwise.
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

  // ---------- CBRAIN links ----------
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

  // ---------- tabs ----------
  function initTabs() {
    var tabs = [].slice.call(document.querySelectorAll('.dp-tabs [role="tab"]'));
    if (!tabs.length) { return; }

    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) { tab.focus(); }
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () {
        select(tab, false);
        history.replaceState(null, '', '#' + tab.getAttribute('aria-controls'));
      });
      tab.addEventListener('keydown', function (e) {
        // Cmd/Alt/Ctrl + arrow are the browser's back/forward and other
        // shortcuts: leave them to the browser.
        if (e.metaKey || e.altKey || e.ctrlKey) { return; }
        var next = null;
        if (e.key === 'ArrowRight') { next = tabs[(i + 1) % tabs.length]; }
        if (e.key === 'ArrowLeft') { next = tabs[(i - 1 + tabs.length) % tabs.length]; }
        if (e.key === 'Home') { next = tabs[0]; }
        if (e.key === 'End') { next = tabs[tabs.length - 1]; }
        if (next) { e.preventDefault(); select(next, true); }
      });
    });

    // Deep links: #about, #metadata, #cite; anything inside a panel
    // (for example the old #dataladInstructions anchor) opens that panel.
    function open(hash, scroll) {
      var target = hash && document.getElementById(hash);
      // A way to get the data this dataset doesn't offer (links from the
      // Data page use #route-browser, #route-request, #route-source,
      // #route-cbrain, #dataladInstructions): open Get the data.
      if (!target && hash && (hash.indexOf('route-') === 0 || hash === 'dataladInstructions')) {
        target = document.getElementById('get');
      }
      var panel = target && (target.getAttribute('role') === 'tabpanel' ? target : target.closest('[role="tabpanel"]'));
      if (!panel) { return false; }
      var tab = document.querySelector('[aria-controls="' + panel.id + '"]');
      if (tab) { select(tab, false); }
      if (target === panel && tab && scroll !== false) {
        // A link to a tab (#research from a Data card, #cite, ...): show the
        // tab bar with the chosen tab, just below the sticky navigation bar
        // (scroll-margin-top), rather than the panel's first line under it.
        tab.closest('.dp-tabs').scrollIntoView({ block: 'start' });
      }
      if (target !== panel) {
        target.scrollIntoView({ block: 'center' });
        target.classList.add('is-flash');
        setTimeout(function () { target.classList.remove('is-flash'); }, 2400);
      }
      return true;
    }
    open(decodeURIComponent(location.hash.slice(1)));
    // In-page links such as the licence chip (#dp-licence) open their tab.
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) { return; }
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      if (open(id)) { e.preventDefault(); history.replaceState(null, '', '#' + id); }
    });
  }

  // ---------- description: five lines, then "more" ----------
  function initMore() {
    var desc = document.getElementById('dp-desc');
    var btn = document.querySelector('.dp-more');
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

  // ---------- copy buttons ----------
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

  // What a copy button copies: the text without the dimmed "# ..." notes
  // (zsh, the macOS default shell, does not treat # as a comment when
  // commands are pasted at the prompt).
  function commandText(src) {
    var node = src.cloneNode(true);
    [].forEach.call(node.querySelectorAll('.dp-comment'), function (c) { c.parentNode.removeChild(c); });
    return node.textContent.split('\n').map(function (l) { return l.replace(/\s+$/, ''); }).join('\n').trim();
  }

  function initCopy() {
    document.querySelectorAll('.dp-copy').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var src = btn.dataset.copyTarget ? document.getElementById(btn.dataset.copyTarget)
          : btn.parentNode.querySelector('code');
        if (!src) { return; }
        copyText(commandText(src), function () {
          btn.classList.add('is-copied');
          btn.title = 'Copied';
          setTimeout(function () { btn.classList.remove('is-copied'); btn.title = 'Copy'; }, 1500);
        });
      });
    });
  }

  // ---------- citation formats ----------
  // One Text / BibTeX / RIS switch for every reference on the tab (the
  // dataset, then each publication). It shows that format in each group,
  // points each group's copy button at it, and builds the download (all
  // shown references in one file) in the browser, so no extra route is needed.
  function initCiteFormats() {
    var buttons = document.querySelectorAll('[data-cite-format]');
    var groups = document.querySelectorAll('#cite [data-cite-group]');
    var download = document.getElementById('dp-cite-download');
    if (!buttons.length || !groups.length) { return; }
    var objectUrl = null;
    function show(format) {
      var shownAll = [];
      var ext = 'txt';
      groups.forEach(function (group) {
        var shown = null;
        group.querySelectorAll('[data-cite-block]').forEach(function (block) {
          var on = block.dataset.citeBlock === format;
          block.hidden = !on;
          if (on) { shown = block; }
        });
        var copy = group.querySelector('.dp-copy');
        if (shown) {
          shownAll.push(shown.textContent.trim());
          ext = shown.dataset.ext || ext;
          if (copy) { copy.dataset.copyTarget = shown.id; }
        }
      });
      if (!shownAll.length) { return; }
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.citeFormat === format)); });
      if (download) {
        if (objectUrl) { URL.revokeObjectURL(objectUrl); }
        var type = ext === 'bib' ? 'application/x-bibtex' : (ext === 'ris' ? 'application/x-research-info-systems' : 'text/plain');
        objectUrl = URL.createObjectURL(new Blob([shownAll.join('\n\n') + '\n'], { type: type }));
        download.href = objectUrl;
        download.setAttribute('download', download.getAttribute('download').replace(/\.[a-z]+$/, '') + '.' + ext);
        download.querySelector('span').textContent = '.' + ext;
      }
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function () { show(b.dataset.citeFormat); });
    });
    show('text');
  }

  function showModal(id) {
    var el = document.getElementById(id);
    if (el && window.bootstrap && bootstrap.Modal) {
      bootstrap.Modal.getOrCreateInstance(el).show();
      return true;
    }
    return false;
  }

  // ---------- direct download: confirm the size first ----------
  function initDownload() {
    var links = document.querySelectorAll('[data-dp-download]');
    var doc = document.getElementById('downloadModalDocument');
    Array.prototype.forEach.call(links, function (link) {
      link.addEventListener('click', function (e) {
        var size = link.dataset.size || '';
        if (doc && window.bootstrap) {
          e.preventDefault();
          doc.innerHTML =
            '<div class="modal-content">' +
            '<div class="modal-body"><h4 class="modal-title text-center">You are about to download a ' + escapeHtml(size) + ' file.</h4></div>' +
            '<div class="modal-footer"><button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>' +
            '<a class="btn btn-success" id="confirmDownload" href="' + escapeHtml(link.getAttribute('href')) + '">Download</a></div></div>';
          doc.querySelector('#confirmDownload').addEventListener('click', function () {
            bootstrap.Modal.getOrCreateInstance(document.getElementById('downloadModal')).hide();
          });
          showModal('downloadModal');
        } else if (!window.confirm('You are about to download a ' + size + ' file. Continue?')) {
          e.preventDefault();
        }
      });
    });
  }

  // ---------- CBRAIN: choose a pipeline (or none) ----------
  function initCbrain() {
    var btn = document.querySelector('[data-dp-cbrain]');
    var body = document.getElementById('cbrainModalBody');
    if (!btn) { return; }
    var card = document.querySelector('.dp-card');
    var title = card ? card.dataset.datasetTitle : '';
    var cbrainUrl = btn.dataset.cbrainUrl;
    var param = cbrainGroupId(cbrainUrl);

    btn.addEventListener('click', function () {
      if (!body || !window.bootstrap) { window.open(cbrainUrl, '_blank', 'noopener'); return; }
      body.innerHTML =
        '<p>You\'re about to load <strong>' + escapeHtml(title) + '</strong> on CBRAIN. Please select a pipeline to process this dataset (or "None" to load only the dataset).</p>' +
        '<p>Not all pipelines are compatible with all datasets. Please make sure you are <a href="https://portal.cbrain.mcgill.ca" target="_blank" rel="noreferrer">logged into CBRAIN</a> first.</p>' +
        '<div class="list-group" id="dpCbrainList"><a class="list-group-item list-group-item-action" target="_blank" rel="noreferrer" href="' + escapeHtml(cbrainUrl) + '">None</a></div>';
      showModal('cbrainModal');
      var list = document.getElementById('dpCbrainList');
      list.addEventListener('click', function (e) {
        if (e.target.closest('a')) { bootstrap.Modal.getOrCreateInstance(document.getElementById('cbrainModal')).hide(); }
      });
      fetch(btn.dataset.pipelinesUrl + '?max_per_page=All&cbrain=true&sortKey=title')
        .then(function (r) { return r.ok ? r.json() : { elements: [] }; })
        .then(function (json) {
          (json.elements || []).forEach(function (el) {
            var url = el.platforms && el.platforms[0] ? el.platforms[0].uri : el.cbrain_id;
            if (!url) { return; }
            var a = document.createElement('a');
            a.className = 'list-group-item list-group-item-action';
            a.target = '_blank';
            a.rel = 'noreferrer';
            a.href = withSwitchGroup(url, param);
            a.textContent = el.title;
            list.appendChild(a);
          });
        })
        .catch(function (err) { console.error(err); });
    });
  }

  ready(function () {
    initTabs();
    initMore();
    initCopy();
    initCiteFormats();
    initDownload();
    initCbrain();
  });
})();
