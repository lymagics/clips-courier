"""friends by telegram id

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-17

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Username rows cannot be turned into ids, so the table starts over.
    op.drop_table("friends", if_exists=True)
    op.create_table(
        "friends",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("name", sa.Text(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("friends", if_exists=True)
    op.create_table(
        "friends",
        sa.Column("name", sa.Text(), primary_key=True),
    )
