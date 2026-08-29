"""friends table

Revision ID: 0001
Revises:
Create Date: 2026-08-29

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # if_not_exists adopts databases created before migrations existed.
    op.create_table(
        "friends",
        sa.Column("name", sa.Text(), primary_key=True),
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_table("friends", if_exists=True)
