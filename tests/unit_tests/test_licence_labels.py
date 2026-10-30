"""One licence badge for Data cards and dataset pages: the record's own name
when it is a short title, a standard short name otherwise, and a link to the
licence's address (the DATS licence `identifier`, or a name that is an address)."""
from flask import render_template_string

from app.search import dataset_list as dl
from app.search.dataset_page import licence_badges, licence_entries
from tests.unit_tests.test_data_page import _element

OPEN = [{'name': 'Open PREVENT-AD Terms of Use',
         'identifier': {'identifier': 'https://openpreventad.loris.ca/images/Open_PREVENT-AD_Terms_of_Use.png'}}]
REGISTERED = [{'name': 'https://registeredpreventad.loris.ca/images/PREVENT-AD_Terms_of_Use.png'}]


def test_entries_carry_the_address():
    assert licence_entries(OPEN) == [{'name': 'Open PREVENT-AD Terms of Use',
                                      'url': 'https://openpreventad.loris.ca/images/Open_PREVENT-AD_Terms_of_Use.png'}]
    assert licence_entries(REGISTERED)[0]['url'] == REGISTERED[0]['name']
    assert licence_entries(['CC0']) == [{'name': 'CC0', 'url': None}]
    assert licence_entries(None) == []


def test_badges_name_and_link():
    b = licence_badges(licence_entries(OPEN))[0]
    assert (b['label'], b['url']) == ('Open PREVENT-AD Terms of Use', OPEN[0]['identifier']['identifier'])
    b = licence_badges(licence_entries(REGISTERED))[0]
    assert (b['label'], b['url']) == ('PREVENT-AD Terms of Use', REGISTERED[0]['name'])
    assert licence_badges(['https://creativecommons.org/licenses/by-sa/4.0/'])[0]['label'] == 'CC BY-SA 4.0'


def test_card_and_page_show_the_same_badge(tmp_path):
    e = _element(tmp_path, 'projects/preventad-open-bids', licenses=['Open PREVENT-AD Terms of Use'],
                 licenceLinks=licence_entries(OPEN))
    card = dl.dataset_card(e)
    assert card['licences'] == licence_badges(licence_entries(OPEN))
    html = render_template_string("{% from 'macros/cards.html' import dataset_card %}{{ dataset_card(c) }}", c=card)
    assert 'href="https://openpreventad.loris.ca/images/Open_PREVENT-AD_Terms_of_Use.png"' in html
    assert 'Open PREVENT-AD Terms of Use' in html


def test_card_from_an_older_index_without_addresses(tmp_path):
    e = _element(tmp_path, 'projects/preventad-registered', licenses=[REGISTERED[0]['name']])
    card = dl.dataset_card(e)
    assert card['licence'] == 'PREVENT-AD Terms of Use'
    assert 'loris.ca' not in card['licence']


def test_dataset_page_chip_and_metadata_row_link_to_the_terms(app):
    from tests.unit_tests.test_research_use_pages import _render
    html = _render(app, None, licences=licence_badges(licence_entries(OPEN)))
    url = OPEN[0]['identifier']['identifier']
    assert html.count(f'href="{url}"') == 2        # chip and the Licence row
    assert 'Data use terms' not in html


def test_licence_pill_icon_and_label_are_spaced_like_other_facts(tmp_path):
    # The pill (a flex <li> with a gap) must hold the icon directly; a wrapper
    # around icon and text made them touch (30 Oct).
    for links in (licence_entries(OPEN), [{'name': 'Open PREVENT-AD Terms of Use', 'url': None}]):
        e = _element(tmp_path, 'projects/p' + str(bool(links[0]['url'])), licenses=['x'], licenceLinks=links)
        html = render_template_string("{% from 'macros/cards.html' import dataset_card %}{{ dataset_card(c) }}",
                                      c=dl.dataset_card(e))
        li = html[html.index('<li title="Licence:'):]
        li = li[li.index('>') + 1:li.index('</li>')]      # the pill's content, after its title attribute
        assert li.startswith('<svg') and li.index('</svg>') < li.index('Open PREVENT-AD Terms of Use')
        assert '<span title' not in li and ('<a class="lp-licence"' in li) == bool(links[0]['url'])
        if links[0]['url']:
            assert li.index('</svg>') < li.index('<a class="lp-licence"')
