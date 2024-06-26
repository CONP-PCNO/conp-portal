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
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ark_id', schema=None) as batch_op:
        batch_op.add_column(sa.Column('experiment_id', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ark_id', schema=None) as batch_op:
        batch_op.drop_column('experiment_id')

    # ### end Alembic commands ###
