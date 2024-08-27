"""Alter role column to use role_enum_type

Revision ID: 0dd9b288cb83
Revises: c752892fccdc
Create Date: 2024-08-27 11:55:19.846115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dd9b288cb83'
down_revision: Union[str, None] = 'c752892fccdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
