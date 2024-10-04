"""create reservation table

Revision ID: 88378b3fa5fd
Revises: fc9ffcd81da4
Create Date: 2024-09-28 15:11:00.732954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '88378b3fa5fd'
down_revision: Union[str, None] = 'fc9ffcd81da4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('table_id', sa.Integer(), sa.ForeignKey('tables.id')),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True)
    )

def downgrade() -> None:
    sa.drop_table('reservations')