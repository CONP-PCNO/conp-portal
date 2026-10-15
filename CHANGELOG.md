# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed
### Changed
### Added
### Fixed

## [1.1.0] - 2026-10-07

This release prepares CONP Portal for a modern Python and deployment toolchain. It upgrades the project’s supported runtime and framework stack, adds reproducible dependency management and GitHub Actions CI, replaces legacy deployment/CI configuration, modernizes Docker setup and tests, fixes compatibility issues, and refreshes project documentation.

### Runtime, dependencies, and developer tooling

- Bumps the application version to 1.1.
- Pins the Python version to 3.12.3.
- Reworks Python requirements files:
  - archives the former requirements files under v1.0.1-specific names;
  - makes the corrected requirements file the active `requirements.txt`; and
  - updates Dependabot to ignore the archived v1.0 requirements files.
- Aligns and pins Python dependencies with the production environment, records incompatibilities and end-of-life notes, notes Flask-Dance considerations, and adds `requirements-dev.txt`.
- Adopts `uv` dependency management, adding `pyproject.toml` and a committed `uv.lock`.
- Defines a Python 3.12+ baseline and separates application from development dependencies.
- Adds development tools: Ruff, prek/pre-commit hooks, deptry, and pytest.
- Adds deptry checks for dependency issues.
- Upgrades Flake8 to v7.3 and adds exclusion configuration.
- Adds an `.ackrc` configuration file.
- Adds GitHub Linguist overrides.
- Adds Dependabot configuration for GitHub Actions, pip, and npm, and aligns its labels with the project-management workflow.

### Python, Flask, SQLAlchemy, and migration compatibility

- Updates application configuration for Flask 3.x and SQLAlchemy 2.x:
  - adds `SERVER_NAME` and `PREFERRED_URL_SCHEME` to the testing configuration for `url_for()` outside a request context; and
  - documents the Flask 3.x and type-checking rationale.
- Prevents a `TypeError` when `DATASET_CACHE_PATH` receives `None`.
- Fixes Alembic 1.13+ migration configuration by filtering `render_as_batch` before passing migration configuration onward.
- Makes the experiment-table drop conditional in the relevant migration and converts the redundant experiment-ID migration into a no-op to avoid a duplicate-column failure.
- Adds a null check before accessing a dataset ARK ID in search results.
- Removes an invalid `super()` call from the standalone login base template so it renders correctly with modern Flask/Jinja.

### Search and data initialization

- Adds on-demand Whoosh index initialization: the index is created and populated when it is missing or empty, supporting fresh deployments and test environments.
- Updates the test-dataset seed path so it also updates the search index.
- Sets sensible defaults for `DATA_PATH` and `DATASET_CACHE_PATH`.

### Tests and continuous integration

- Modernizes test fixtures for Python 3.10–3.14:
  - keeps a Flask application context active during tests;
  - uses SQLAlchemy 2.x-compatible scoped-session creation; and
  - replaces deprecated `datetime.utcnow()` calls with `datetime.now()`.
- Adds GitHub Actions CI for Python 3.12, 3.13, and 3.14.
- Configures CI to install dependencies, git-annex, and Flake8; run linting and pytest; and avoid rebase behavior during Git pulls.
- Removes the legacy Travis CI configuration.

### Containers and deployment

- Modernizes the Dockerfile into a multi-stage build.
- Makes the Docker Python version configurable through `PYTHON_VERSION`.
- Updates `.dockerignore`.
- Adds base, development, and production Docker Compose files.
- Adds a Docker CONP entrypoint-install file.
- Removes Heroku configuration (`app.json` and the previously removed `Procfile`).

### Front-end fixes

- Fixes React CodeSnippet warnings by adding unique list keys and replacing invalid `class` attributes with `className`.

### Repository cleanup and configuration

- Removes unused repository files, including the root `package-lock.json`, the Procfile, and legacy deployment/CI artifacts.
- Cleans up formatting and whitespace.
- Revises `.gitignore` to cover Python environment files, `.env`, generated static data, and the Whoosh index, while no longer ignoring `.python_version`.
- Updates `flaskenv.template` so options and ordering match production, with formatting and `SECRET_KEY` comment/grouping improvements.
- Updates copyright notices to 2026.

### Documentation

- Refreshes the main README:
  - expands requirements and installation instructions;
  - documents Python support and flexible virtual-environment naming;
  - clarifies one-time bootstrap commands;
  - updates deployment guidance, Docker information, and Flask command help; and
  - moves the experimental AWS Cloud9 material to a separate document.
- Adds `humans.md`.
- Updates deployment documentation for current file locations, content accuracy, and formatting.
- Adds generated base README files for tests.
- Adds inline code documentation, deprecation/end-of-life notes, TODO notes, and a CLI description for `seed_test_experiments`.
- Moves conp-react contribution guidance into its README.

### v1.1.0 Changes

* Hotfix: conp-react/v1.0.1 by @hatzopoulos in https://github.com/CONP-PCNO/conp-portal/pull/864
* Hotfix cbrain ids url encoding by @hatzopoulos in https://github.com/CONP-PCNO/conp-portal/pull/866
* Hotfix conp react urlencode by @hatzopoulos in https://github.com/CONP-PCNO/conp-portal/pull/867
* Release/v1.1 by @hatzopoulos in https://github.com/CONP-PCNO/conp-portal/pull/943

## [1.0.1]

### v1.0.0 to v1.0.1 Changes

* Updated canned queries for new nexus context by @surchs in https://github.com/CONP-PCNO/conp-portal/pull/512
* Update cbrain-conp-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/514
* Update DATS GUI - fix import of ORCID from DATS to GUI + additional REB options by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/516
* Update cbrain-conp-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/519
* Can load terms of use and privacy policy modal windows with URL by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/520
* Escape apostrophies in the title of datasets by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/525
* Update cbrain-conp-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/526
* Query GitHub analytics for number of clones by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/527
* Remove space between "sponsors" and comma on main page by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/529
* ARK implementation by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/523
* Dataset card slight redesign by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/531
* Adding more CONP datasets to dataset-cbrain-ids.json with CBRAIN IDs by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/528
* Fix labels of dataset views chart to be dataset titles instead of dataset GitHub repo name by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/532
* Add links to CBRAIN for Neurocon and Taowu datasets by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/533
* Escape apostrophes in dataset titles by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/534
* Run CONP pipelines on CONP datasets using CBRAIN by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/524
* Do not display current month in "Number of Unique Visitors" analytics graph by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/539
* New dataset and pipeline card layout by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/540
* Fix visit analytics graph by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/541
* Update cbrain-conp-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/543
* Patch 8 by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/544
* Use date when the dataset was merged to conp-dataset instead of repo date creation as date added by @cmadjar in https://github.com/CONP-PCNO/conp-portal/pull/546
* Sort list of pipelines/datasets for CBRAIN modal by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/551
* Update cbrain-conp-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/553
* Update cbrain-conp-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/554
* CBRAIN redirect URL by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/556
* Update cbrain-conp-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/567
* Update block-list-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/566
* Update cbrain-conp-pipeline.json by @natacha-beck in https://github.com/CONP-PCNO/conp-portal/pull/577
* Remove "dark mode" changes from analytics by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/579
* Make dataset search a little smarter by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/582
* Remove type hints that may be causing problems by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/583
* Revert breaks by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/584
* Force light background on front-page charts by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/585
* Search datasets by title in the DB by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/590
* Remove CSS rule to not render first list marker by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/593
* Manually triggered search by @tkkuehn in https://github.com/CONP-PCNO/conp-portal/pull/594
* Third party account by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/620
* Add privacy policy link on the top menu by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/623
* Download page by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/625
* Filter logic changes and Study Spotlight by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/612
* March 2024 fixes by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/630
* DATS downloaded file name fix by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/631
* Primary Publication fix by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/640
* Add space after comma on field lists by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/641
* Offsite download by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/644
* Merge experiments to master by @carona898 in https://github.com/CONP-PCNO/conp-portal/pull/645
* Merge experiements to master - bugfix by @carona898 in https://github.com/CONP-PCNO/conp-portal/pull/653
* Merge experiements to master - bootstrap issue by @carona898 in https://github.com/CONP-PCNO/conp-portal/pull/654
* refactor: put back new dats editor by @carona898 in https://github.com/CONP-PCNO/conp-portal/pull/658
* bugfix: no authors in primary publication cause the request to crash by @carona898 in https://github.com/CONP-PCNO/conp-portal/pull/659
* [Pipelines] Tag filter by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/660
* Reduce menu height by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/668
* Sort pipeline per publication date by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/667
* Missing pipelines fix by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/665
* Sept 2024 UI updates by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/679
* Whoosh search by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/672
* Code copy to clipboard by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/681
* Update dataset-terms-mapping.json by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/682
* Update dataset-terms-mapping.json by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/683
* Update dataset-cbrain-ids.json by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/686
* Update dataset-terms-mapping.json by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/685
* Fix pipeline cbrain processing by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/687
* Fix datasets cBrain filter by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/689
* Remove search limit by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/691
* [Search] Dataset as single entity by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/684
* Datasets README styles by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/692
* [Whoosh] Change indexer separator for title by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/697
* Dataset header card style by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/698
* Search and submodule updates fixes by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/699
* Automatically reindex search terms when importing new datasets by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/700
* Fix indexation logic issue by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/701
* refactor: updated primary publication and version in DATS editor by @carona898 in https://github.com/CONP-PCNO/conp-portal/pull/702
* Desactivate suggestions for pipelines by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/705
* Search field autofocus by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/706
* Fix search key shortcuts by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/707
* Update dataset.html by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/708
* Ghpbz patch 4 by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/709
* Change Field Labels by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/711
* Origin new format by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/713
* Unset search limit by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/717
* feature: update experiment page by @carona898 in https://github.com/CONP-PCNO/conp-portal/pull/723
* New DATS subjects default value by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/724
* Study spotlight fix by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/726
* Fix for quoted dataset names breaking search by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/731
* Bootstrap 5 updates by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/732
* Update dataset-terms-mapping.json by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/743
* Ubuntu 24 and python 3.12 upgrade changes by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/722
* Terms of use fix by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/748
* Post Ubuntu upgrade fixes by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/749
* Fix doi link by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/753
* Add page meta title by @laemtl in https://github.com/CONP-PCNO/conp-portal/pull/755
* update study spotlight  by @kongtiaowang in https://github.com/CONP-PCNO/conp-portal/pull/808
* fix cancelDownload button now working by @kongtiaowang in https://github.com/CONP-PCNO/conp-portal/pull/809
* 2026 06 09 fix search by @kongtiaowang in https://github.com/CONP-PCNO/conp-portal/pull/810
* IA cleanup: link Tutorial in nav, fix mobile nav gap, make Download download-specific by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/819
* Add Data Governance page (route, template, nav link) by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/820
* Style rendered-markdown tables on documentation pages by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/822
* Add descriptive page titles and social link-preview (Open Graph) metadata by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/824
* Add a self-contained maintenance page + nginx activation guide by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/825
* Refactor page-title accent into a CSS class (cosmetic polish) by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/826
* Replace the six "?" help modals with context-aware Tutorial deep links by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/827
* [Search] Link datasets to their NeuroLibre/Evidence publication (strip on dataset card + sort option) by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/845
* [Search] Make the Evidence publication strip tier-accurate, show it on dataset pages, and rebuild the bundle by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/846
* Evidence strip: more breathing room below the card by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/852
* Evidence strip: drop the DOI, align to the title column, larger logo; sort-label reword by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/853
* Fix broken links: homepage acknowledgements, DATS fields guide, McGill IT policy by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/888
* Add a CONP theme layer: design tokens, Bootstrap overrides, and mobile overflow fixes by @GHPBZ in https://github.com/CONP-PCNO/conp-portal/pull/887

**Full Changelog**: https://github.com/CONP-PCNO/conp-portal/compare/v1.0.0...v1.1.0
