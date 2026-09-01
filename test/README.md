
# **./test Directory**

**Purpose:** Test data and utilities

## **Files:**

- `__init__.py` - Creates app instance for testing
- `insert_test_data_localhost.py` - Utility class for populating test database with sample data
- CSV files (users.csv, datasets.csv, datasets_stats.csv, pipelines.csv) - Test data source files
- Image files (loris.png, medics.png, etc.) - Sample dataset images
- `test_dataset/` - Directory with sample dataset files

**Function:** Provides reusable test data and fixtures for manual database population during testing

## Python Packages Imported

Standard Library:
- sys
- os
- csv
- datetime (datetime, timedelta)

Project Modules:
- app (create_app, db)
- app.models (User, Dataset, Pipeline)

