"""Tests for the DataLad-only metadata refresh workflow."""

import datalad.api as datalad_api
import pytest

import app.cli as cli


@pytest.mark.parametrize(
    ("object_type", "repo_name"),
    [
        ("dataset", "conp-dataset"),
        ("experiment", "conp-experiments"),
    ],
)
def test_existing_repository_uses_bounded_datalad_updates(
    tmp_path, monkeypatch, app, object_type, repo_name
):
    """Do not fall back to GitPython's recursive submodule updater."""
    calls = []

    class FakeDataset:
        def __init__(self, path):
            self.path = path

        def is_installed(self):
            return True

        def update(self, **kwargs):
            calls.append(("update", kwargs))

        def install(self, **kwargs):
            calls.append(("install", kwargs))

        def subdatasets(self):
            return []

    def clone(*args, **kwargs):
        raise AssertionError("an installed dataset must not be cloned")

    monkeypatch.setitem(app.config, "DATA_PATH", str(tmp_path))
    monkeypatch.setattr(datalad_api, "Dataset", FakeDataset)
    monkeypatch.setattr(datalad_api, "clone", clone)

    cli._update_datalad_objects(app, object_type, repo_name, object)

    assert calls == [
        ("update", {
            "how": "ff-only",
            "how_subds": "reset",
            "follow": "parentds-lazy",
            "recursive": True,
            "recursion_limit": 1,
        }),
        ("install", {"path": "", "recursive": True, "recursion_limit": 1}),
    ]
