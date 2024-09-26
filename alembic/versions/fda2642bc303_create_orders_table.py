"""create orders table

Revision ID: fda2642bc303
Revises: 5fb4dc7e62bf
Create Date: 2024-09-25 16:35:14.208131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fda2642bc303'
down_revision: Union[str, None] = '5fb4dc7e62bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('menu_id', sa.Integer(), sa.ForeignKey('menu.id')),
        sa.Column('table_id', sa.Integer(), sa.ForeignKey('tables.id')),
        sa.Column('quantity', sa.Integer()),
        sa.Column('status', sa.String()),
        sa.Column('delivery_time', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('orders')
