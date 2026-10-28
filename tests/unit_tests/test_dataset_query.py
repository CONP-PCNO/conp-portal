"""Tests for the dataset search (app/search/dataset_query.py and text_match.py,
as _dataset_elements uses them: over the search index's stored fields)."""
import json

from whoosh.analysis import LowercaseFilter, StopFilter
from whoosh.fields import KEYWORD, STORED, TEXT, Schema
from whoosh.filedb.filestore import RamStorage

from app.JsonTokenizer import JsonTokenizer
from app.search.dataset_query import matches_suggestion, normalize, words
from app.search.text_match import score

TITLE = "Long-term, Phantom Quality Assurance data for functional Magnetic Resonance Imaging from 13 3T research scanners"


def _index():
    keyword = JsonTokenizer(',', True) | LowercaseFilter() | StopFilter()
    title = JsonTokenizer('^', True) | LowercaseFilter() | StopFilter()
    schema = Schema(
        id=STORED,
        title=KEYWORD(stored=True, commas=True, scorable=True, analyzer=title),
        description=TEXT(stored=True),
        keywords=KEYWORD(stored=True, commas=True, scorable=True, analyzer=keyword),
        modalities=KEYWORD(stored=True, commas=True, scorable=True, analyzer=keyword),
    )
    ix = RamStorage().create_index(schema)
    w = ix.writer()
    w.add_document(id='fbirn', title=TITLE, description="fBIRN phantoms scanned monthly",
                   keywords=json.dumps(["Quality Assurance", "MRI"]), modalities=json.dumps(["MRI"]))
    w.add_document(id='head', title="Head motion in children", description="A study of head movement",
                   keywords=json.dumps(["motion"]), modalities=json.dumps(["MRI", "EEG"]))
    w.add_document(id='ad', title="PREVENT-AD open data", description="Pre-symptomatic Alzheimer cohort",
                   keywords=json.dumps(["Alzheimer's disease"]), modalities=json.dumps(["PET"]))
    w.commit()
    return ix


def _ids(ix, text, mapping=None):
    """The ids _dataset_elements keeps for this search: same fields, same rule."""
    fields = [f for f in ix.schema.scorable_names() if f in ix.schema.names()]
    with ix.searcher() as s:
        return {d['id'] for d in s.documents() if score({f: d.get(f) for f in fields}, text, mapping)}


def test_words_and_normalize():
    assert words("Long-term, phantom") == ["long", "term", "phantom"]
    assert words("data for MRI") == ["data", "mri"]          # stop word dropped
    assert words("for") == ["for"]                           # unless nothing else is left
    assert normalize("Long-term,  Phantom!") == "long term phantom"


def test_hyphens_spaces_and_commas_are_the_same():
    ix = _index()
    for text in ("long-term", "long term", "Long Term", "term, phantom", "long-term phantom"):
        assert _ids(ix, text) == {'fbirn'}, text


def test_full_title_from_the_type_ahead_finds_the_dataset():
    ix = _index()
    assert _ids(ix, TITLE.lower()) == {'fbirn'}


def test_comma_separated_words_never_raise():
    ix = _index()
    assert _ids(ix, "mri, eeg") == {'head'}
    assert _ids(ix, "---") == set()
    assert _ids(ix, "") == set()


def test_word_start_not_anywhere():
    ix = _index()
    assert _ids(ix, "ad") == {'ad'}      # PREVENT-AD, not "head"
    assert _ids(ix, "prevent ad") == {'ad'}


def test_synonyms_are_alternatives():
    ix = _index()
    assert _ids(ix, "qa", {"qa": "quality assurance"}) == {'fbirn'}


def test_matches_suggestion():
    assert matches_suggestion("long term", TITLE.lower())
    assert matches_suggestion("Long-Term", TITLE.lower())
    assert not matches_suggestion("", TITLE)
