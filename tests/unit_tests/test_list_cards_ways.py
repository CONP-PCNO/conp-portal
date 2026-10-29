"""The ways to get or run something on list cards are visually separated."""
import os

CSS = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'static', 'css', 'list-page.css')


def test_ways_have_dividers():
    css = open(CSS, encoding='utf-8').read()
    assert '.lp-get > a + a { border-left: 1px solid' in css
    assert '@media (max-width: 600px)' in css
