"""Tool cards: "Run it on" CBRAIN | Your computer | Alliance HPC."""
import os

from werkzeug.datastructures import MultiDict

from app.pipelines import tool_list as tl

CARDS = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'templates', 'macros', 'cards.html')


def test_card_wording():
    html = open(CARDS, encoding='utf-8').read()
    assert '<span class="lp-get-label">Run it on</span>' in html
    assert 'Alliance HPC</a>' in html and 'Alliance cluster</a>' not in html
    assert '#cbrain">On <img' not in html


def test_old_cluster_filter_links_still_work():
    sel = tl.selected_filters(MultiDict([('runs', 'Alliance cluster (container)')]))
    assert sel['runs'] == [tl.RUN_CLUSTER] == ['Alliance HPC (container)']
