"""Progress output for the data update CLI commands."""

import app.cli as cli


def test_update_experiments_reports_progress(app, runner, monkeypatch):
    monkeypatch.setattr(cli, "_update_experiments", lambda _app: None)
    cli.register(app)

    result = runner.invoke(args=["update_experiments"])

    assert result.exit_code == 0
    assert result.output.splitlines() == [
        "Refreshing experiment metadata from conp-experiments...",
        "Experiment metadata update complete.",
    ]


def test_update_datasets_reports_progress(app, runner, monkeypatch):
    monkeypatch.setattr(cli, "_update_datasets", lambda _app: None)
    monkeypatch.setattr(cli, "_update_index", lambda *_args: None)
    cli.register(app)

    result = runner.invoke(args=["update_datasets"])

    assert result.exit_code == 0
    assert result.output.splitlines() == [
        "Refreshing dataset metadata from conp-datasets...",
        "Rebuilding the dataset search index...",
        "Dataset metadata and search index update complete.",
    ]


def test_update_pipeline_data_reports_progress(app, runner, monkeypatch):
    monkeypatch.setattr(cli, "_update_pipeline_data", lambda _app: None)
    cli.register(app)

    result = runner.invoke(args=["update_pipeline_data"])

    assert result.exit_code == 0
    assert result.output.splitlines() == [
        "Refreshing available pipelines from Zenodo...",
        "Pipeline data update complete.",
    ]
