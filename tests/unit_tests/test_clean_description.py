"""
Tests for clean_description: tool descriptions that arrive as HTML (sometimes
entity-escaped) are shown as plain text on the Tools page and tool pages.
"""
from app.pipelines.pipelines import clean_description


def test_escaped_html_is_decoded_and_stripped():
    raw = ('&lt;h1&gt;Description&lt;/h1&gt; MicroVIP is part of PROCHIP, see '
           '&lt;a href=&quot;https://example.org/m&quot;&gt;https://example.org/m&lt;/a&gt;. '
           '&lt;h2&gt;Parameters&lt;/h2&gt; It&amp;apos;s simple.')
    assert clean_description(raw) == (
        'Description\nMicroVIP is part of PROCHIP, see https://example.org/m.\n'
        "Parameters\nIt's simple.")


def test_raw_html_links_keep_their_address():
    raw = 'Documentation is <a href="http://example.org/doc">here</a>.<br />'
    assert clean_description(raw) == 'Documentation is here (http://example.org/doc).'


def test_plain_text_is_kept():
    raw = 'Concatenate fields.\n\nFor instance if you have\n- a warp  field'
    assert clean_description(raw) == 'Concatenate fields.\nFor instance if you have\n- a warp field'
    assert clean_description(None) is None
