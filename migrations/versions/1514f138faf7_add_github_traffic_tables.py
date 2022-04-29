"""add GitHub traffic tables

Revision ID: 1514f138faf7
Revises: 3d982110f18c
Create Date: 2022-03-09 11:50:50.470004

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1514f138faf7'
down_revision = '3d982110f18c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('github_daily_clones_count',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('repo', sa.String(length=256), nullable=True),
    sa.Column('date', sa.String(length=12), nullable=True),
    sa.Column('timestamp', sa.String(length=30), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('unique_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('github_daily_views_count',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('repo', sa.String(length=256), nullable=True),
    sa.Column('date', sa.String(length=12), nullable=True),
    sa.Column('timestamp', sa.String(length=30), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('unique_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('datasets', schema=None) as batch_op:
        batch_op.alter_column('is_private',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)

    with op.batch_alter_table('pipelines', schema=None) as batch_op:
        batch_op.alter_column('is_private',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('active',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False,
               existing_server_default=sa.text('0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('active',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False,
               existing_server_default=sa.text('0'))

    with op.batch_alter_table('pipelines', schema=None) as batch_op:
        batch_op.alter_column('is_private',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)

    with op.batch_alter_table('datasets', schema=None) as batch_op:
        batch_op.alter_column('is_private',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)

    op.drop_table('github_daily_views_count')
    op.drop_table('github_daily_clones_count')
    # ### end Alembic commands ###