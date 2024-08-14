"""empty message

Revision ID: f33ae154400e
Revises: 7d393a6a5b2d
Create Date: 2024-08-14 08:19:57.260435

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f33ae154400e"
down_revision: Union[str, None] = "7d393a6a5b2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "SELECT setval(pg_get_serial_sequence('users', 'id'), coalesce(max(id)+1, 1), false) FROM users;"
        )
    )


def downgrade() -> None:
    pass
