"""One way to match and rank what a visitor types, for datasets, tools and
experiments alike.

Matching (every typed word must start a word somewhere, as since #1021) is
made forgiving in three ways, taken from the CONP-INCF-TOSI Starter Kit's
library search:

- Spellings are folded before comparing: UK/Canadian and US forms
  ("behaviour"/"behavior", "grey"/"gray", "centre"/"center", "-ise"/"-ize",
  "modelling"/"modeling", "paediatric"/"pediatric"), and accents are dropped
  ("Montréal" = "montreal").
- Hyphenated words are also indexed joined: "pre-processing" can be found as
  "preprocessing", "pre-processing" or "pre processing"; and two typed words
  may match one joined word ("neuro imaging" finds "neuroimaging").
- A plural or possessive "s" is dropped from typed words (dataset_query.stem).

Ranking: each typed word scores the weight of the best field it starts a word
in (title above keywords and modalities, above people, above the description),
more for a whole word than for a prefix; the whole search as a phrase in the
title, or the title itself, scores most. Ties keep the list's usual order.
"""
import json
import re
import unicodedata

from whoosh.analysis import STOP_WORDS

_WORD = re.compile(r'[^\W_]+', re.UNICODE)
# Words joined by a hyphen, a slash-free dash or an apostrophe: "pre-processing",
# "Alzheimer's", "test–retest".
_COMPOUND = re.compile(r"[^\W_]+(?:[-‐-―'’][^\W_]+)+", re.UNICODE)

# UK/Canadian -> US spellings, applied to lower-case text without accents.
# Applied to both sides, so a folded form only has to be consistent, not a
# real word ("analysis" -> "analyzis" matches "analyze" and "analysis" alike).
_FOLDS = [(re.compile(p), r) for p, r in (
    (r'(behavi|col|flav|fav|hum|lab|neighb|tum|rum|vap|harb|hon|od|vig|sav|arm|endeav|rig|ard)our', r'\1or'),
    (r'\bgrey', 'gray'),
    (r'centred\b', 'centered'),
    (r'(cent|fib|lit|met|theat|calib|sab)re(s|d)?\b', r'\1er\2'),
    (r'licenc', 'licens'),
    (r'defenc', 'defens'),
    (r'ageing', 'aging'),
    (r'\bpaed', 'ped'), (r'paedi', 'pedi'), (r'\bhaem', 'hem'), (r'aemi', 'emi'), (r'\boed', 'ed'),
    (r'\boestr', 'estr'), (r'anaesth', 'anesth'), (r'\bfoet', 'fet'), (r'orthopaed', 'orthoped'),
    # analyse/analyze/analysis/analyses/analysing -> one root, so any form finds the others.
    (r'(ana|para)ly[sz](?:es|ed|er|ers|ing|is|e)?\b', r'\1lyz'),
    (r'(organ|standard|normal|visual|character|optim|harmon|synchron|random|minim|maxim|general|parameter|'
     r'initial|custom|summar|categor|priorit|recogn|util|real|digit|binar|vector|regular|local|special|'
     r'anonym|pseudonym|token|emphas|catalog|memor|stabil|steril|central|famil|mobil|polar|quantit|'
     r'hospital|immun|capital|individual|personal|contextual|operational|conceptual)is(e|ed|es|ing|ation|ations|er|ers)\b',
     r'\1iz\2'),
    (r'(model|label|signal|travel|cancel|channel|level|fuel|tunnel|total|counsel|tunnel)l(ing|ed|er|ers)\b', r'\1\2'),
    (r'programme', 'program'),
    (r'(catal|dial|anal)ogue', r'\1og'),
    (r'enrolment', 'enrollment'),
)]

# Field weights. Datasets use the search index's field names; tools and
# experiments name theirs in the same terms.
WEIGHTS = {
    'title': 10,
    'keywords': 6, 'modalities': 6, 'family': 6, 'domains': 6, 'functions': 5,
    'isAbout': 5, 'formats': 4, 'software': 4,
    'creators': 4, 'author': 4, 'contacts': 3, 'languages': 3,
    'description': 2,
}
OTHER_WEIGHT = 1
WHOLE_WORD = 1.5      # a typed word that is a whole word, not just its start
PHRASE_IN_TITLE = 15  # all the typed words, in order, inside the title
TITLE_STARTS = 8      # ... at the start of the title
TITLE_IS = 30         # the title is what was typed
SYNONYM = 0.5         # a match found only through dataset-terms-mapping.json


def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))


def fold(text):
    """Lower case, accents dropped, UK/Canadian spellings turned into US ones."""
    t = strip_accents(str(text or '')).lower()
    for pattern, repl in _FOLDS:
        t = pattern.sub(repl, t)
    return t


def stem(word):
    """A plural or possessive "s" dropped ("alzheimers" -> "alzheimer");
    short words and words in "ss", "us", "is" kept as typed."""
    w = str(word or '')
    if len(w) > 4 and w.endswith('s') and not w.endswith(('ss', 'us', 'is')):
        return w[:-1]
    return w


def _joined(compound):
    return re.sub(r'[^\w]|_', '', compound)


def terms(text):
    """The folded words of a text, plus each hyphenated word joined up
    ("pre-processing" -> "preprocessing") and each two neighbouring words
    joined ("neuro imaging" -> "neuroimaging"), so a compound is found
    however it was written."""
    t = fold(text)
    found = _WORD.findall(t)
    pairs = [a + b for a, b in zip(found, found[1:])]
    return found + pairs + [_joined(c) for c in _COMPOUND.findall(t)]


def query_words(text):
    """What to look for: folded words, stop words dropped (unless nothing else
    is left), plural "s" dropped. A typed hyphenated word is one word
    ("pre-processing" = "preprocessing"; "Alzheimer's" = "alzheimer")."""
    t = re.sub(r"['’]s\b", 's', fold(text))
    t = _COMPOUND.sub(lambda m: _joined(m.group()), t)
    found = _WORD.findall(t)
    kept = [w for w in found if w not in STOP_WORDS]
    return [stem(w) for w in (kept or found)]


def text_values(value):
    """The strings inside a field value: a JSON list or object (as the search
    index stores them) is read for its values, recursively."""
    if isinstance(value, str):
        s = value.strip()
        if s[:1] in '[{':
            try:
                return text_values(json.loads(s))
            except ValueError:
                pass
        return [value]
    if isinstance(value, dict):
        return [t for v in value.values() for t in text_values(v)]
    if isinstance(value, (list, tuple, set)):
        return [t for v in value for t in text_values(v)]
    if value is None:
        return []
    return [str(value)]


class Searchable:
    """One record's fields, prepared once for matching and scoring."""

    def __init__(self, fields):
        self.fields = {}
        for name, value in fields.items():
            words = set()
            for s in text_values(value):
                words.update(terms(s))
            if words:
                self.fields[name] = words
        title = ' '.join(text_values(fields.get('title')))
        self.title = ' '.join(_WORD.findall(fold(title)))

    def word_score(self, word):
        best = 0
        for name, words in self.fields.items():
            weight = WEIGHTS.get(name, OTHER_WEIGHT)
            if word in words:
                best = max(best, weight * WHOLE_WORD)
            elif weight * WHOLE_WORD > best and any(w.startswith(word) for w in words):
                best = max(best, weight)
        return best

    def score(self, text):
        """0 when the record doesn't match; otherwise how well it does."""
        words = query_words(text)
        if not words:
            return 0
        memo = {}

        def cover(i):
            # Best score for words[i:], each word alone or joined with the next
            # ("neuro imaging" -> "neuroimaging"); None when they can't all match.
            if i == len(words):
                return 0
            if i not in memo:
                options = []
                for j in (i + 1, i + 2):
                    if j > len(words):
                        break
                    s = self.word_score(''.join(words[i:j]))
                    rest = cover(j) if s else None
                    if rest is not None:
                        options.append(s + rest)
                memo[i] = max(options) if options else None
            return memo[i]

        total = cover(0)
        if total is None:
            return 0
        phrase = ' '.join(_WORD.findall(re.sub(r"['’]s\b", 's', fold(text))))
        if phrase and self.title:
            if self.title == phrase:
                total += TITLE_IS
            elif (self.title + ' ').startswith(phrase + ' '):
                total += TITLE_STARTS + PHRASE_IN_TITLE
            elif (' ' + phrase + ' ') in (' ' + self.title + ' '):
                total += PHRASE_IN_TITLE
        return total


def _norm(text):
    return ' '.join(_WORD.findall(fold(text)))


def score(fields, text, synonyms=None):
    """How well a record (a dict of field name -> value) matches the search,
    0 when it doesn't. Synonyms ({term: alternative}, dataset-terms-mapping.json)
    are tried too, scored lower: when the search is a term, its alternative is
    searched as well ("OBI" also finds "Ontario Brain Institute"). Only the
    whole term counts: before, a search that was any part of a term also
    searched its alternative, so "mri" searched "Functional Magnetic Resonance
    Imaging" (from "fMRI") and "neuroimaging" found every NIfTI dataset (from
    "Neuroimaging Informatics Technology Initiative")."""
    rec = fields if isinstance(fields, Searchable) else Searchable(fields)
    best = rec.score(text)
    norm = _norm(text)
    for key, alternative in (synonyms or {}).items():
        if norm and norm == _norm(key):
            best = max(best, rec.score(alternative) * SYNONYM)
    return best


def rank(items, key='score'):
    """Best match first; ties keep the order the items came in (the list's
    usual order), since Python's sort is stable."""
    return sorted(items, key=lambda c: -(c.get(key) or 0))
