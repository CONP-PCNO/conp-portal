"""Dataset search helpers: the words of a search, "Did you mean", and the
type-ahead's matching.

Which datasets match, and in what order, is decided by app/search/text_match
(the same rules as for tools and experiments): every typed word must start a
word in some searchable field, with spellings folded and hyphenated words
also joined up; synonyms from dataset-terms-mapping.json are tried too.
"""
import re

from whoosh.analysis import STOP_WORDS

from app.search.text_match import fold, stem  # noqa: F401  (stem: used by the lists)

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


def search_words(text):
    """The words to look for, stemmed (see stem)."""
    return [stem(w) for w in words(text)]


def suggest_correction(text, vocabulary, cutoff=0.8):
    """A "Did you mean" for a search that found nothing: each typed word not
    found in the vocabulary is replaced by the closest word that is, when one
    is close enough ("parkisnon" -> "parkinson"). None when nothing changes."""
    import difflib
    vocab = sorted({v for v in vocabulary if v and len(v) > 2})
    if not vocab:
        return None
    vocab_set = set(vocab)
    out, changed = [], False
    for w in _WORD.findall(str(text or '').lower()):
        if w in vocab_set or any(v.startswith(stem(w)) for v in vocab if v[:2] == w[:2]):
            out.append(w)
            continue
        close = difflib.get_close_matches(w, vocab, n=1, cutoff=cutoff)
        if close:
            out.append(close[0])
            changed = True
        else:
            out.append(w)
    return ' '.join(out) if changed else None


def vocabulary(texts):
    """Lower-case words of the given strings, for suggest_correction."""
    found = set()
    for t in texts:
        found.update(_WORD.findall(str(t or '').lower()))
    return found


def matches_suggestion(search_term, value):
    """Type-ahead: does the stored value contain what was typed, ignoring
    punctuation and spacing ("long term" finds "long-term, phantom ...")."""
    norm = normalize(fold(search_term))
    return bool(norm) and norm in normalize(fold(value))
