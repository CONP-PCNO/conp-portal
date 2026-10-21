"""Dataset search: turn what a visitor types into a Whoosh query.

The visitor's text is split into words on anything that is not a letter or a
digit, so "long-term", "long term" and "Long-term," are the same two words.
A dataset matches when every word is found in at least one searchable field
(title, description, keywords, creators, modalities, formats, ...).

Fields analysed word by word (TEXT) are matched on word prefixes. Fields that
keep whole values (the title, keywords, modalities: KEYWORD fields whose
tokens are complete phrases such as "quality assurance") are matched on a
word inside the value that starts with the typed word. Synonyms from dataset-terms-mapping.json are
added as alternatives, as before.

Building the query never raises: a field that cannot take a query is skipped,
so no search returns a server error.
"""
import re

from whoosh import query as Q
from whoosh.analysis import STOP_WORDS
from whoosh.fields import TEXT

_WORD = re.compile(r'[^\W_]+', re.UNICODE)


def normalize(text):
    """Lower case, with every run of punctuation or spaces as one space."""
    return ' '.join(_WORD.findall(str(text or '').lower()))


def words(text):
    """The words to look for: stop words ("of", "for", "the") are dropped, as
    the index drops them, unless nothing else is left."""
    found = _WORD.findall(str(text or '').lower())
    kept = [w for w in found if w not in STOP_WORDS]
    return kept or found


def _field_word_query(schema, field, word):
    """One word in one field, or None when the field can't match it."""
    ftype = schema[field]
    if isinstance(ftype, TEXT):
        # Run the word through the field's analyzer (lower case, stop words).
        try:
            tokens = [t.text for t in ftype.analyzer(word)]
        except Exception:
            tokens = [word]
        if not tokens:
            return None
        return Q.Prefix(field, tokens[0])
    # Whole-value fields: the word must start a word inside the value, the same
    # prefix rule as for analysed fields ("ad" finds "ad" and "adhd", not "head").
    return Q.Regex(field, r'(?:.*[^a-z0-9])?' + re.escape(word) + r'.*')


def _phrase_query(schema, fields, text):
    """All the words of `text`, each in at least one field."""
    parts = []
    for word in words(text):
        alternatives = [q for q in (_field_word_query(schema, f, word) for f in fields) if q is not None]
        if not alternatives:
            return None
        parts.append(Q.Or(alternatives))
    if not parts:
        return None
    return parts[0] if len(parts) == 1 else Q.And(parts)


def build_dataset_query(schema, search_term, terms_mapping=None):
    """Whoosh query for the visitor's search text, or None for an empty search."""
    fields = [f for f in schema.scorable_names() if f in schema.names()]
    main = _phrase_query(schema, fields, search_term)
    if main is None:
        return None
    alternatives = [main]
    norm = normalize(search_term)
    for key, mapped in (terms_mapping or {}).items():
        if norm and norm in normalize(key):
            q = _phrase_query(schema, fields, mapped)
            if q is not None:
                alternatives.append(q)
    return alternatives[0] if len(alternatives) == 1 else Q.Or(alternatives)


def matches_suggestion(search_term, value):
    """Type-ahead: does the stored value contain what was typed, ignoring
    punctuation and spacing ("long term" finds "long-term, phantom ...")."""
    norm = normalize(search_term)
    return bool(norm) and norm in normalize(value)
