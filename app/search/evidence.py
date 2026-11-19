"""NeuroLibre/Evidence publications: first-page thumbnails and titles for the
dataset page's Evidence banner.

``flask update_evidence_thumbnails`` reads each publication's landing page
(https://doi.org/<doi>) for its title (``citation_title``) and PDF address
(``citation_pdf_url``), renders page 1 of the PDF to a small PNG with
poppler's ``pdftoppm``, and records both in
``DATA_PATH/evidence-publications/index.json``. The dataset page only reads
that index: it never fetches anything, and a publication with no entry, or
no thumbnail, keeps the banner without the page.

Rendering needs poppler (``apt install poppler-utils``); without it the
command still records the titles.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from html import unescape

THUMB_WIDTH = 240  # px; shown at 88 px wide, so sharp on 2x screens
_cache = {'path': None, 'mtime': None, 'index': {}}


def store_dir(data_path):
    return os.path.join(data_path, 'evidence-publications')


def doi_slug(doi):
    """A file-safe name for a DOI: 10.55458/neurolibre.00050 -> 10-55458-neurolibre-00050."""
    return re.sub(r'[^a-z0-9]+', '-', str(doi or '').strip().lower()).strip('-')


def load_index(data_path):
    path = os.path.join(store_dir(data_path), 'index.json')
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return {}
    if _cache['path'] != path or _cache['mtime'] != mtime:
        try:
            with open(path, encoding='utf-8') as f:
                index = json.load(f)
        except (OSError, ValueError):
            index = {}
        _cache.update(path=path, mtime=mtime, index=index if isinstance(index, dict) else {})
    return _cache['index']


def publication_info(data_path, doi):
    """{'title', 'thumbnail'} for the dataset page; 'thumbnail' is the file
    name to serve, or None. Empty values when nothing is recorded."""
    entry = load_index(data_path).get(str(doi or '').strip().lower()) or {}
    thumb = entry.get('thumbnail')
    if thumb and not os.path.exists(os.path.join(store_dir(data_path), thumb)):
        thumb = None
    return {'title': entry.get('title') or None, 'thumbnail': thumb}


def parse_landing(html):
    """(title, pdf_url) from the citation_* meta tags of a landing page."""
    def meta(name):
        for tag in re.findall(r'<meta\b[^>]*>', html or '', re.I):
            if re.search(rf'name\s*=\s*["\']{re.escape(name)}["\']', tag, re.I):
                m = re.search(r'content\s*=\s*["\']([^"\']*)["\']', tag, re.I)
                if m:
                    return unescape(m.group(1)).strip() or None
        return None
    return meta('citation_title'), meta('citation_pdf_url')


def render_first_page(pdf_bytes, out_png, width=THUMB_WIDTH):
    """Page 1 of a PDF as a PNG, ``width`` px wide. False when poppler is
    missing or the PDF cannot be read."""
    exe = shutil.which('pdftoppm')
    if not exe:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        pdf = os.path.join(tmp, 'in.pdf')
        with open(pdf, 'wb') as f:
            f.write(pdf_bytes)
        stem = os.path.join(tmp, 'page')
        try:
            subprocess.run([exe, '-f', '1', '-l', '1', '-png', '-singlefile', '-scale-to-x', str(width),
                            '-scale-to-y', '-1', pdf, stem], check=True, capture_output=True, timeout=120)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False
        if not os.path.exists(stem + '.png'):
            return False
        shutil.move(stem + '.png', out_png)
    return True


def update(data_path, dois, get, force=False, renderer=None, log=print):
    """Fetch title and thumbnail for each DOI not yet done (all with force).
    ``get(url)`` returns an object with ``status_code``, ``text`` and
    ``content`` (requests.get with a timeout). Returns the index."""
    renderer = renderer or render_first_page
    folder = store_dir(data_path)
    os.makedirs(folder, exist_ok=True)
    index = dict(load_index(data_path))
    for doi in sorted({str(d).strip().lower() for d in dois if d}):
        entry = index.get(doi) or {}
        have = entry.get('thumbnail') and os.path.exists(os.path.join(folder, entry['thumbnail']))
        if have and entry.get('title') and not force:
            continue
        try:
            page = get('https://doi.org/' + doi)
            title, pdf_url = parse_landing(page.text) if page.status_code == 200 else (None, None)
        except Exception as exc:  # one publication must not stop the rest
            log(f'{doi}: landing page failed ({exc})')
            continue
        entry.update(title=title or entry.get('title'), pdf=pdf_url or entry.get('pdf'))
        if pdf_url and (force or not have):
            png = doi_slug(doi) + '.png'
            try:
                pdf = get(pdf_url)
                ok = pdf.status_code == 200 and pdf.content[:5] == b'%PDF-' and renderer(
                    pdf.content, os.path.join(folder, png))
            except Exception as exc:
                log(f'{doi}: PDF failed ({exc})')
                ok = False
            if ok:
                entry['thumbnail'] = png
            elif not have:
                entry.pop('thumbnail', None)
            log('{}: {}{}'.format(doi, 'thumbnail made' if ok else 'no thumbnail',
                                  '' if shutil.which('pdftoppm') or ok else ' (pdftoppm not found: apt install poppler-utils)'))
        entry['updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        index[doi] = entry
    tmp = os.path.join(folder, 'index.json.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=1, sort_keys=True)
    os.replace(tmp, os.path.join(folder, 'index.json'))
    return index
