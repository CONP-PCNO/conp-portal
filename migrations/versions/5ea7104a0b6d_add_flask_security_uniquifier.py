"""Add Flask-Security user identity key.

Revision ID: 5ea7104a0b6d
Revises: b7e2c91d4f30
Create Date: 2026-11-04
"""
import uuid

import sqlalchemy as sa
from alembic import op


revision = "5ea7104a0b6d"
down_revision = "b7e2c91d4f30"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "roles",
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("fs_uniquifier", sa.String(length=64), nullable=True),
    )

    users = sa.table("users", sa.column("id", sa.Integer),
                     sa.column("fs_uniquifier", sa.String(length=64)))
    connection = op.get_bind()
    for (user_id,) in connection.execute(sa.select(users.c.id)):
        connection.execute(
            users.update()
            .where(users.c.id == user_id)
            .values(fs_uniquifier=uuid.uuid4().hex)
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "fs_uniquifier",
            existing_type=sa.String(length=64),
            nullable=False,
        )
        batch_op.create_unique_constraint(
            "uq_users_fs_uniquifier",
            ["fs_uniquifier"],
        )


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_users_fs_uniquifier", type_="unique")
        batch_op.drop_column("fs_uniquifier")
    op.drop_column("roles", "description")
