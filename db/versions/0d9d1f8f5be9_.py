"""empty message

Revision ID: 0d9d1f8f5be9
Revises: 207a1528e5c7
Create Date: 2024-02-02 19:29:55.654764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d9d1f8f5be9'
down_revision: Union[str, None] = '207a1528e5c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
