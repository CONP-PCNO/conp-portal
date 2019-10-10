"""adding one-to-one relationship for dataset stats

Revision ID: a756c32e9169
Revises: c4780889e90b
Create Date: 2019-10-08 15:05:09.864185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a756c32e9169'
down_revision = 'c4780889e90b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
      "ALTER TABLE dataset_stats "
      "ADD COLUMN fk_dataset_id INTEGER "
      "REFERENCES datasets(id) " 
    )
    op.execute(
      "CREATE UNIQUE INDEX ix_dataset_stats_fk_dataset_id "
      "ON dataset_stats (fk_dataset_id) "
    )
    op.execute(
      "UPDATE dataset_stats "
      "SET fk_dataset_id = ("
        "SELECT id FROM datasets "
          "WHERE datasets.dataset_id = dataset_stats.dataset_id"
      ")"
    )


def downgrade():
    op.execute(
      "CREATE TABLE tmp_dataset_stats AS "
      "SELECT id, dataset_id, size, files, sources, "
        "num_subjects, num_downloads, num_likes, "
        "num_views, date_updated "
      "FROM dataset_stats"
    )
    op.drop_index('ix_dataset_stats_fk_dataset_id', table_name='dataset_stats')
    op.drop_index('ix_dataset_stats_dataset_id', table_name='dataset_stats')
    op.drop_index('ix_dataset_stats_files', table_name='dataset_stats')
    op.drop_index('ix_dataset_stats_num_downloads', table_name='dataset_stats')
    op.drop_index('ix_dataset_stats_num_likes', table_name='dataset_stats')
    op.drop_index('ix_dataset_stats_num_subjects', table_name='dataset_stats')
    op.drop_index('ix_dataset_stats_num_views', table_name='dataset_stats')
    op.drop_index('ix_dataset_stats_size', table_name='dataset_stats')
    op.drop_index('ix_dataset_stats_sources', table_name='dataset_stats')
    op.drop_table('dataset_stats')

    op.execute("ALTER TABLE tmp_dataset_stats RENAME TO dataset_stats")
    op.create_index('ix_dataset_stats_sources', 'dataset_stats', ['sources'], unique=False)
    op.create_index('ix_dataset_stats_size', 'dataset_stats', ['size'], unique=False)
    op.create_index('ix_dataset_stats_num_views', 'dataset_stats', ['num_views'], unique=False)
    op.create_index('ix_dataset_stats_num_subjects', 'dataset_stats', ['num_subjects'], unique=False)
    op.create_index('ix_dataset_stats_num_likes', 'dataset_stats', ['num_likes'], unique=False)
    op.create_index('ix_dataset_stats_num_downloads', 'dataset_stats', ['num_downloads'], unique=False)
    op.create_index('ix_dataset_stats_files', 'dataset_stats', ['files'], unique=False)
    op.create_index('ix_dataset_stats_dataset_id', 'dataset_stats', ['dataset_id'], unique=1)
    
