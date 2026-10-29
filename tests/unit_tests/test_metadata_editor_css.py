"""metadata-editor.css undoes the Portal styles that broke Material UI fields."""
import os

CSS = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'static',
                   'css', 'metadata-editor.css')


def _css():
    with open(CSS, encoding='utf-8') as f:
        return f.read()


def test_legend_is_not_floated():
    # Bootstrap 5 floats <legend>; Material UI's outlined fields need it in flow
    css = _css()
    assert 'MuiOutlinedInput-notchedOutline > legend' in css
    assert 'float: none' in css


def test_field_focus_has_no_portal_halo():
    css = _css()
    assert '#dats-editor-container .MuiInputBase-input:focus' in css


def test_title_rule_sits_under_the_title():
    css = _css()
    assert '.page-header:has(.page-lede)::after' in css
