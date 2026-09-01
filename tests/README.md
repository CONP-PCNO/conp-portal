# **./tests Directory**

**Purpose:** Main comprehensive test suite using pytest

## **Structure**

- **`conftest.py`** - Pytest configuration with session fixtures
- **`unit_tests/`** - Model unit tests
	- `test_user_model.py` - Tests User model creation and DB operations
	- `test_dataset_model.py` - Tests Dataset model creation and DB operations
	- `test_datsdataset_schema_org.py` - Tests DATS schema conversion for Google Dataset Search
	- `test_affiliation_types.py` - Tests AffiliationType model
- **`database_tests/`** - Database integration tests
    - `test_migrations.py` - Tests Alembic migrations and DB seeding CLI commands
- **`blueprint_specific_tests/`** - Flask blueprint endpoint tests
    - `auth_bp_tests/` - Authentication endpoints (login, OAuth)
    - `admin_bp_tests/` - Admin routes
    - `main_bp_tests/` - Main/index routes
    - `search_bp_tests/` - Search functionality endpoints
    - `forums_bp_tests/` - Forums/discussion routes
    - `profile_bp_tests/` - User profile endpoints
    - `pipelines_bp_tests/` - Pipelines endpoints and search

## Python Packages Imported

Standard Library:
- os
- datetime (datetime, timedelta)
- urllib.parse (urlparse)

Third-Party:
- pytest
- sqlalchemy (event)
- sqlalchemy.orm (sessionmaker)
- alembic.command (upgrade)
- alembic.config (Config)
- flask (url_for)
- flask_login (current_user, login_user, logout_user)
- flask_dance.consumer.storage (MemoryStorage)

Project Modules:
- app (create_app, db)
- app.models (Dataset, Pipeline, User, AffiliationType, OAuth, Role, UsersRoles)
- app.search.models (DATSDataset)
- app.cli
- config (TestingConfig)
