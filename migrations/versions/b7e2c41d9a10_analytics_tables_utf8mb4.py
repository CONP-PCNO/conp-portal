"""analytics tables to utf8mb4

The analytics tables kept the database's old character set when ada4a4cd0d09
converted the datasets table, so text from Matomo with a character outside it
(a site search for "CC359 → Reconstructed", 1 Nov 2026) stopped
update_analytics with MariaDB error 1366. Their only unique keys are short
(date, String(12)), so the conversion fits any InnoDB index limit.

Revision ID: b7e2c41d9a10
Revises: 5ea7104a0b6d
Create Date: 2026-11-05 22:45:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b7e2c41d9a10'
down_revision = '5ea7104a0b6d'
branch_labels = None
depends_on = None

TABLES = (
    'matomo_daily_visits_summary',
    'matomo_daily_get_page_urls_summary',
    'matomo_daily_dataset_page_views_summary',
    'matomo_daily_portal_download_summary',
    'matomo_daily_site_keyword_searches_summary',
    'github_daily_clones_count',
    'github_daily_views_count',
)


def upgrade():
    if op.get_bind().dialect.name in ('mysql', 'mariadb'):
        for table in TABLES:
            op.execute(f"ALTER TABLE {table} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    # SQLite stores UTF-8 natively: nothing to do.


def downgrade():
    # Converting back could fail or mangle rows that now hold characters the
    # old set cannot store, so the downgrade leaves the tables as they are.
    pass
