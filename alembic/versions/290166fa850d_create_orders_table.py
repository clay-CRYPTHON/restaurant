"""create orders table

Revision ID: 290166fa850d
Revises: 88378b3fa5fd
Create Date: 2024-09-28 15:12:31.731755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '290166fa850d'
down_revision: Union[str, None] = '88378b3fa5fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('menu_id', sa.Integer(), sa.ForeignKey('menu.id')),
        sa.Column('table_id', sa.Integer(), sa.ForeignKey('tables.id')),
        sa.Column('quantity', sa.Integer()),
        sa.Column('status', sa.String()),
        sa.Column('delivery_time', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('orders')