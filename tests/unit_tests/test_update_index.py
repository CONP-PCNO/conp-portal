"""`flask update_index` must rebuild the search index, never add to it.

Running it after `flask update_datasets` (which already rebuilds the index)
used to list every dataset twice on the Data page, the dataset counts and the
"Cumulative Number of Datasets" chart.
"""
import json
from types import SimpleNamespace

from whoosh import index

import app.cli as cli
import app.search.models as search_models


class _FakeDATS:
    def __init__(self, fspath, dataset_id=None):
        self.name = dataset_id
        self.DatsFilepath = fspath + "/DATS.json"
        self.LogoFilepath = None

    def __getattr__(self, name):
        return None


class _FakeQuery:
    def __init__(self, rows):
        self._rows = rows

    def order_by(self, *args):
        return self

    def all(self):
        return self._rows


def test_update_index_twice_does_not_duplicate(tmp_path, monkeypatch, app):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "app/static/datasets").mkdir(parents=True)
    (tmp_path / "app/static/datasets/dataset-cbrain-ids.json").write_text(json.dumps({}))

    rows = [
        SimpleNamespace(id=1, dataset_id="projects/a", name="Dataset A", fspath="/data/a"),
        SimpleNamespace(id=2, dataset_id="projects/b", name="Dataset B", fspath="/data/b"),
    ]
    fake_model = SimpleNamespace(id=None, query=_FakeQuery(rows))
    monkeypatch.setattr(cli, "DBDataset", fake_model)
    monkeypatch.setattr(search_models, "DATSDataset", _FakeDATS)

    cli._update_index(app, fake_model, True)   # as `flask update_datasets` does
    cli._update_index(app, fake_model, False)  # then `flask update_index`
    cli._update_index(app, fake_model, False)

    ix = index.open_dir("index")
    with ix.searcher() as searcher:
        ids = sorted(d["id"] for d in searcher.documents())
    assert ids == ["projects/a", "projects/b"]
