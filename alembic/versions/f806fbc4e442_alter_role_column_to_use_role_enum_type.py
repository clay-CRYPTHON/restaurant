"""Alter role column to use role_enum_type

Revision ID: f806fbc4e442
Revises: 0dd9b288cb83
Create Date: 2024-08-27 12:50:00.206550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f806fbc4e442'
down_revision: Union[str, None] = '0dd9b288cb83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
