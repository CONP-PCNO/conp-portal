"""Page frame accessibility and the analytics keyword list."""
from app.analytics.routes import clean_search_keywords


def test_search_keywords_without_probes_or_identifiers():
    out = clean_search_keywords([
        {'label': 'prevent-ad', 'nb_hits': 358}, {'label': 'PREVENT-AD', 'nb_hits': 256},
        {'label': 'sssiedhsearchxsx', 'nb_hits': 202}, {'label': "fsssiedxa'sssiedx", 'nb_hits': 28},
        {'label': 'treatment"', 'nb_hits': 28}, {'label': '<script>alert(1)</script>', 'nb_hits': 5},
        {'label': 'http://uri.interlex.org/base/ilx_0106458', 'nb_hits': 4}, {'label': 'ilx:0779125', 'nb_hits': 3},
        {'label': 'MRI', 'nb_hits': 182},
    ])
    assert sorted((e['label'], e['nb_hits']) for e in out) == [('MRI', 182), ('prevent-ad', 614)]


def test_frame_has_skip_link_main_and_titled_video(test_client):
    html = test_client.get('/').get_data(as_text=True)
    assert html.lstrip().startswith('<!doctype html>\n<html lang="en">')   # standards mode, page language
    assert html.count('<body>') == 1 and html.rstrip().endswith('</html>')
    assert '<a class="skip-link" href="#main">Skip to content</a>' in html
    assert '<main id="main"' in html and html.count('<main') == 1
    assert 'title="CONP Portal tutorial video"' in html
