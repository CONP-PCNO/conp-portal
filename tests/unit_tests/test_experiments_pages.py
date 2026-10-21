"""Experiments redesign: the list (search, filters, sort) and the page."""
import os
import shutil

from app.experiments import experiment_page as ep
from app.experiments.experiment_page import filter_cards, software_name, software_short
from app.models import Experiment

FIXTURE = os.path.join(os.path.dirname(__file__), 'fixtures', 'experiment_BADE')
PNG = b'\x89PNG\r\n\x1a\n' + b'\x00' * 16


def _add(session, tmp_path, monkeypatch):
    from app.services import github
    monkeypatch.setattr(github, 'render_content', lambda raw: '<h1>BADE Evidence Integration</h1><p>Procedure.</p>')
    folder = tmp_path / 'BADE-evidence-integration'
    shutil.copytree(FIXTURE, folder)
    (folder / 'README.md').write_text('# BADE Evidence Integration\n\nProcedure.')
    (folder / 'logo.png').write_bytes(PNG)
    (tmp_path / 'BADE-evidence-integration.zip').write_bytes(b'PK')
    Experiment.query.filter_by(experiment_id='projects/BADE-evidence-integration').delete()
    exp = Experiment(experiment_id='projects/BADE-evidence-integration', name='BADE Evidence Integration',
                     fspath=str(folder), version='1.0', is_private=False, views=7,
                     remoteUrl='https://github.com/emmetaobrien/BADE-evidence-integration')
    session.add(exp)
    session.flush()
    return exp


def test_software_names():
    assert software_name('NBS Presentation version 17') == 'NBS Presentation'
    assert software_name('PsychoPy version 2023.1.3') == 'PsychoPy'
    assert software_short('NBS Presentation version 17') == 'NBS Presentation 17'


def test_filter_cards():
    cards = [
        {'title': 'B task', 'description': 'memory', 'creators': [], 'keywords': [], 'functions': ['Cognitive'],
         'modalities': ['fMRI', 'EEG'], 'software': ['PsychoPy'], 'software_label': 'PsychoPy 2023',
         'languages': ['English'], 'added': '2024-08-21', 'views': 5},
        {'title': 'A task', 'description': 'reasoning', 'creators': [], 'keywords': [], 'functions': ['Cognitive'],
         'modalities': ['fMRI'], 'software': ['NBS Presentation'], 'software_label': 'NBS Presentation 17',
         'languages': ['English', 'French'], 'added': '2024-08-26', 'views': 9},
    ]
    shown, facets = filter_cards(cards, '', {}, 'added')
    assert [c['title'] for c in shown] == ['A task', 'B task']
    assert {f['key'] for f in facets} == {'function', 'modality', 'software', 'language'}
    shown, facets = filter_cards(cards, '', {'modality': ['EEG']}, 'name')
    assert [c['title'] for c in shown] == ['B task']
    shown, _ = filter_cards(cards, 'reason', {}, 'name')
    assert [c['title'] for c in shown] == ['A task']
    shown, _ = filter_cards(cards, '', {'language': ['French', 'English']}, 'views')
    assert [c['title'] for c in shown] == ['A task', 'B task']


def test_experiment_page_renders(session, test_client, tmp_path, monkeypatch):
    _add(session, tmp_path, monkeypatch)
    res = test_client.get('/experiments/view/BADE-evidence-integration')
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'Get the task' in html and 'What you need to run the experiment' in html
    assert 'NBS Presentation 17' in html and 'Colour-blindness, Hearing impairment' in html
    assert 'Download from this browser' in html and '/experiments/download/' in html
    assert 'datalad install BADE-evidence-integration' in html and 'datalad get .<span class="dp-comment">' in html
    assert '/static/img/doi/osf.png' in html                          # DOI with its source icon
    assert '(software).' in html and 'https://doi.org/10.17605/OSF.IO/EKDU5' in html
    assert '<p>Procedure.</p>' in html and '<h1>BADE Evidence Integration</h1>' not in html   # title heading dropped
    assert 'Schizophrenia Bulletin' in html and 'Construct validity' in html


def test_experiments_list(session, test_client, tmp_path, monkeypatch):
    _add(session, tmp_path, monkeypatch)
    html = test_client.get('/experiments/').get_data(as_text=True)
    assert 'BADE Evidence Integration' in html and 'href="/experiments/view/BADE-evidence-integration"' in html
    assert 'name="modality" value="fMRI"' in html
    html = test_client.get('/experiments/', query_string={'modality': 'fMRI', 'q': 'disconfirmatory'}).get_data(as_text=True)
    assert 'BADE Evidence Integration' in html and 'checked' in html
    html = test_client.get('/experiments/search', query_string={'q': 'no-such-word'}).get_data(as_text=True)
    assert 'No experiment matches' in html


def test_default_logo_when_none(session, tmp_path, monkeypatch, app):
    exp = _add(session, tmp_path, monkeypatch)
    os.remove(os.path.join(exp.fspath, 'logo.png'))
    with app.test_request_context('/'):
        assert ep.experiment_card(exp)['logo'].endswith('img/experiments/default.svg')
