"""convert datasets table to utf8mb4

Revision ID: ada4a4cd0d09
Revises: 2569d0eba19d
Create Date: 2026-10-28 13:18:50.517200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ada4a4cd0d09'
down_revision = '2569d0eba19d'
branch_labels = None
depends_on = None


def upgrade():
    # Get the current database dialect name (e.g., 'sqlite', 'mysql', etc.)
    bind = op.get_bind()
    dialect_name = bind.dialect.name
    if dialect_name == 'mysql':
        # Convert database, table, and column character set to utf8mb4
        op.execute("ALTER DATABASE CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        op.execute("ALTER TABLE datasets CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    else:
        # SQLite doesn't need (or support) charset conversion statements.
        # SQLite handles UTF-8 natively by default.
        pass


def downgrade():
    bind = op.get_bind()
    dialect_name = bind.dialect.name
    if dialect_name == 'mysql':
        # Reverting back to utf8/latin1 if needed (optional, often left empty or set to utf8)
        op.execute("ALTER TABLE datasets CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;")

