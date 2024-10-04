"""create floors table

Revision ID: 4d25377c30e7
Revises: ba8647548d36
Create Date: 2024-09-28 15:01:25.712415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4d25377c30e7'
down_revision: Union[str, None] = 'ba8647548d36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'floors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('floors')