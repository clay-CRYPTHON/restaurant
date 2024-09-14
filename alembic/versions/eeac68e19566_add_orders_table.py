"""Add orders table

Revision ID: eeac68e19566
Revises: af8463474a37
Create Date: 2024-09-14 11:39:35.768725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eeac68e19566'
down_revision: Union[str, None] = 'af8463474a37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('menu_id', sa.Integer, sa.ForeignKey('menu.id'), nullable=False),
        sa.Column('table_id', sa.Integer, sa.ForeignKey('tables.id'), nullable=True),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('delivery_time', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('orders')