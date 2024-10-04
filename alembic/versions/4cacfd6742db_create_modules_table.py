"""create modules table

Revision ID: 4cacfd6742db
Revises: 4d25377c30e7
Create Date: 2024-09-28 15:05:45.244102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4cacfd6742db'
down_revision: Union[str, None] = '4d25377c30e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'modules',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('floor_id', sa.Integer(), sa.ForeignKey('floors.id')),
    )


def downgrade() -> None:
    op.drop_table('modules')