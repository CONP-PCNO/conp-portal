"""empty message

Revision ID: 2569d0eba19d
Revises: bc891b53bf4f
Create Date: 2023-10-05 11:31:20.311979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2569d0eba19d'
down_revision = 'bc891b53bf4f'
branch_labels = None
depends_on = None


def upgrade():
    # This revision is intentionally a no-op. The `experiment_id` column was
    # added in the preceding migration and is already present in the current
    # schema. Keeping this migration as a no-op avoids duplicate-column errors
    # when Alembic upgrades a fresh database.
    pass


def downgrade():
    # No-op, because the revision itself did not create a schema change.
    pass
