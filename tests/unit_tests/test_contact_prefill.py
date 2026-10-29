"""The contact form can be opened with its topic and message pre-filled."""
from urllib.parse import parse_qs, urlparse

from app.main.routes import contact_form_src


def _q(src):
    return parse_qs(urlparse(src).query)


def test_plain_form():
    q = _q(contact_form_src())
    assert q == {'embedded': ['true']}


def test_topic_and_message():
    q = _q(contact_form_src('other', 'A paper that used "Calgary" is missing.'))
    assert q['entry.1130948154'] == ['Other topic or general feedback']
    assert q['entry.470057101'] == ['A paper that used "Calgary" is missing.']


def test_unknown_topic_is_ignored_and_message_is_capped():
    assert _q(contact_form_src('nope', 'x')) == {'embedded': ['true']}
    q = _q(contact_form_src('bug', 'y' * 900))
    assert len(q['entry.1130875829'][0]) == 500


def test_page_uses_it(test_client):
    html = test_client.get('/contact_us?topic=other&message=Hello').get_data(as_text=True)
    assert 'entry.470057101=Hello' in html
    assert 'entry.1130948154=Other+topic+or+general+feedback' in html
