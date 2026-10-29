"""add retired_dataset table

Datasets removed from conp-dataset keep a record here, so that their ARK and
their old /dataset?id= address explain the removal instead of failing.

Revision ID: b7e2c91d4f30
Revises: ada4a4cd0d09
Create Date: 2026-10-28 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7e2c91d4f30'
down_revision = 'ada4a4cd0d09'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'retired_dataset',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('dataset_id', sa.String(length=256), nullable=True),
        sa.Column('name', sa.String(length=256), nullable=True),
        sa.Column('retired_on', sa.DateTime(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('replaced_by', sa.String(length=256), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_retired_dataset_dataset_id'), 'retired_dataset', ['dataset_id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_retired_dataset_dataset_id'), table_name='retired_dataset')
    op.drop_table('retired_dataset')
