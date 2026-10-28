"""Search across datasets, tools and experiments (app/search/text_match.py):
spelling folds, hyphenated words joined up, and the "Best match" order."""
from werkzeug.datastructures import MultiDict

from app.search.text_match import fold, query_words, rank, score, terms


def test_uk_and_us_spellings_are_the_same():
    for uk, us in (('behaviour', 'behavior'), ('behavioural', 'behavioral'), ('grey matter', 'gray matter'),
                   ('Centre', 'center'), ('licence', 'license'), ('paediatric', 'pediatric'),
                   ('normalisation', 'normalization'), ('harmonised', 'harmonized'), ('modelling', 'modeling'),
                   ('labelled', 'labeled'), ('tumour', 'tumor'), ('ageing', 'aging'), ('fibre', 'fiber'),
                   ('anonymised', 'anonymized'), ('programme', 'program'), ('haemodynamic', 'hemodynamic')):
        assert fold(uk) == fold(us), (uk, us)
    # Applied the same way to both sides, so "analyse" finds "analysis".
    assert score({'description': 'Statistical analysis of EEG'}, 'analyse')
    # Words that only look alike are left alone.
    assert fold('four hours') == 'four hours' and fold('your') == 'your'


def test_accents_dropped():
    assert score({'description': 'Recruited in Montréal and Québec'}, 'montreal quebec')


def test_hyphenated_words_also_joined():
    assert 'preprocessing' in terms('Pre-processing pipeline')
    rec = {'title': 'fMRIPrep pre-processing outputs'}
    for text in ('preprocessing', 'pre-processing', 'pre processing'):
        assert score(rec, text), text
    # Two typed words can make one joined word: "neuro imaging" finds "neuroimaging".
    assert score({'title': 'NiMARE: Neuroimaging Meta-Analysis'}, 'neuro imaging')
    assert score({'title': 'Alzheimer’s disease cohort'}, "alzheimer's")
    assert query_words("Alzheimer's") == ['alzheimer']


def test_every_word_must_start_a_word():
    rec = {'title': 'Head motion in children'}
    assert not score(rec, 'ad')                 # not inside "head"
    assert not score(rec, 'motion adults')      # every word must match
    assert score(rec, 'mot child')


def test_title_matches_rank_first():
    in_title = {'title': 'Tau PET in young adults', 'description': 'MK6240'}
    in_keywords = {'title': 'Ageing cohort', 'keywords': ['tau', 'PET']}
    in_description = {'title': 'Brain atlas', 'description': 'Includes a tau PET subset'}
    s = [score(r, 'tau pet') for r in (in_title, in_keywords, in_description)]
    assert s[0] > s[1] > s[2] > 0
    # The title itself beats a title that only contains the words.
    assert score({'title': 'BigBrain'}, 'bigbrain') > score({'title': 'BigBrain 2015 release'}, 'bigbrain')
    # A whole word beats the start of a longer one.
    assert score({'title': 'MRI phantom'}, 'mri') > score({'title': 'MRIQC reports'}, 'mri')


def test_synonyms_score_lower():
    mapping = {'qa': 'quality assurance'}
    direct = score({'title': 'QA reports'}, 'qa', mapping)
    via = score({'title': 'Quality assurance of scanners'}, 'qa', mapping)
    assert direct > via > 0


def test_rank_keeps_the_usual_order_for_ties():
    items = [{'id': 'a', 'score': 5}, {'id': 'b', 'score': 9}, {'id': 'c', 'score': 5}]
    assert [i['id'] for i in rank(items)] == ['b', 'a', 'c']


def test_sort_defaults_and_menu():
    from app.search import dataset_list as dl
    assert dl.chosen_sort(MultiDict(), 'eeg') == 'relevance'
    assert dl.chosen_sort(MultiDict(), '') == 'added'
    assert dl.chosen_sort(MultiDict({'sort': 'relevance'}), '') == 'added'   # no search: no best match
    assert dl.chosen_sort(MultiDict({'sort': 'name'}), 'eeg') == 'name'
    menu = dl.sort_options(dl.SORTS, 'eeg', 'added')
    assert menu[0] == ('', 'Best match') and ('added', 'Recently added') in menu
    menu = dl.sort_options(dl.SORTS, '', 'added')
    assert menu[0] == ('', 'Recently added') and all(label != 'Best match' for _v, label in menu)


def test_data_page_cards_in_best_match_order(tmp_path):
    from app.search import dataset_list as dl
    from tests.unit_tests.test_data_page import _element
    old = dict(_element(tmp_path, 'projects/a', title='Old', dateAdded='2020-01-01'), _score=20)
    new = dict(_element(tmp_path, 'projects/b', title='New', dateAdded='2026-01-01'), _score=5)
    tie = dict(_element(tmp_path, 'projects/c', title='Tie', dateAdded='2025-01-01'), _score=5)
    cards = [dl.dataset_card(e) for e in (new, old, tie)]
    shown, _ = dl.filter_cards(cards, {}, 'relevance')
    assert [c['title'] for c in shown] == ['Old', 'New', 'Tie']


def _exp(title, description, added):
    return {'title': title, 'description': description, 'creators': [], 'keywords': [], 'functions': [],
            'modalities': [], 'software': [], 'software_label': '', 'languages': [], 'added': added, 'views': 0}


def test_tools_and_experiments_rank_too():
    from app.experiments.experiment_page import filter_cards as exp_filter
    from app.pipelines.tool_list import filter_cards as tool_filter
    from tests.unit_tests.test_tools_list import GENERIC, _el
    from app.pipelines.tool_list import tool_card
    tools = [tool_card(_el('zenodo.1', 'Tool with behaviour in its description', 100), None, set(), set(), GENERIC),
             tool_card(_el('zenodo.2', 'Behavior', 1), None, set(), set(), GENERIC)]
    shown, _ = tool_filter(tools, 'behaviour', {}, 'relevance')
    assert [c['title'] for c in shown][0] == 'Behavior'          # the title match first, despite fewer downloads
    cards = [_exp('Visual search', '', '2020-01-01'), _exp('Memory task', 'a visual search variant', '2026-01-01')]
    shown, _ = exp_filter(cards, 'visual search', {}, 'relevance')
    assert [c['title'] for c in shown] == ['Visual search', 'Memory task']
    shown, _ = exp_filter(cards, 'isual', {}, 'relevance')     # word starts only (was "anywhere")
    assert shown == []


def test_sort_menus_render(session, test_client, tmp_path, monkeypatch):
    from app.pipelines import routes as tool_routes
    from app.search import routes
    from tests.unit_tests.test_data_page import _element
    from tests.unit_tests.test_tools_list import GENERIC, _el
    elements = [dict(_element(tmp_path, 'projects/a', title='EEG rest'), _score=30)]
    monkeypatch.setattr(routes, '_dataset_elements', lambda q, authorized: elements)
    html = test_client.get('/search?search=eeg').get_data(as_text=True)
    assert '<option value="" selected>Best match</option>' in html and '<option value="added">' in html
    html = test_client.get('/search').get_data(as_text=True)
    assert '<option value="" selected>Recently added</option>' in html and 'Best match' not in html
    html = test_client.get('/search?search=eeg&sort=name').get_data(as_text=True)
    assert '<option value="name" selected>' in html
    assert "s.disabled = true" in html                      # the empty default is left out of the address
    monkeypatch.setattr(tool_routes, '_tool_elements', lambda: [_el('zenodo.1', 'BET', 5)])
    monkeypatch.setattr(tool_routes, 'get_tool_icons', lambda: ({}, GENERIC))
    html = test_client.get('/pipelines?search=bet').get_data(as_text=True)
    assert '<option value="" selected>Best match</option>' in html
    html = test_client.get('/pipelines').get_data(as_text=True)
    assert '<option value="" selected>Most downloaded</option>' in html
    html = test_client.get('/experiments/?q=memory').get_data(as_text=True)
    assert '<option value="" selected>Best match</option>' in html
