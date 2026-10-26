"""One search across the Portal from the home page, and spelling tolerance."""
from app.search.dataset_query import stem, suggest_correction, vocabulary
from tests.unit_tests.test_data_page import _element
from tests.unit_tests.test_tools_list import FS, GENERIC, _el


def test_plural_and_possessive_forms():
    assert stem('alzheimers') == 'alzheimer' and stem('parkinsons') == 'parkinson'
    assert stem('mass') == 'mass' and stem('mri') == 'mri' and stem('tasks') == 'task' and stem('focus') == 'focus'


def test_did_you_mean():
    vocab = vocabulary(["Parkinson's Disease Datasets - Neurocon", 'Alzheimer disease', 'FreeSurfer-Recon-all'])
    assert suggest_correction('parkisnon', vocab) == 'parkinson'
    assert suggest_correction('freesufer recon', vocab) == 'freesurfer recon'
    assert suggest_correction('alzheimer', vocab) is None          # found as typed: nothing to suggest
    assert suggest_correction('qwxzy', vocab) is None              # nothing close


def test_find_lists_all_three_sections(session, test_client, tmp_path, monkeypatch):
    from app.experiments import routes as exp_routes
    from app.pipelines import routes as tool_routes
    from app.search import routes
    datasets = [_element(tmp_path, 'projects/fs{}'.format(i), title='FreeSurfer outputs {}'.format(i)) for i in range(7)]
    monkeypatch.setattr(routes, '_dataset_elements', lambda q, authorized: datasets)
    tools = [_el('zenodo.1', 'FreeSurfer-Recon-all', 10), _el('zenodo.2', 'BET', 5)]
    monkeypatch.setattr(tool_routes, '_tool_elements', lambda: tools)
    monkeypatch.setattr(tool_routes, 'get_tool_icons', lambda: ({'zenodo.1': FS}, GENERIC))
    monkeypatch.setattr(exp_routes, 'experiment_cards', lambda: [])
    html = test_client.get('/find?q=freesurfer').get_data(as_text=True)
    assert '7 datasets' in html and 'See all 7 in Data' in html and 'href="/search?search=freesurfer"' in html
    assert 'FreeSurfer-Recon-all' in html and '1 tool<' in html and 'BET' not in html
    assert 'No experiment matches.' in html
    assert test_client.get('/find').status_code == 302          # empty search: back to the home page


def test_home_search_goes_to_find(test_client):
    html = test_client.get('/').get_data(as_text=True)
    assert 'action="/find"' in html and 'name="q"' in html
