"""create reservations table

Revision ID: 5fb4dc7e62bf
Revises: eb1dd196fdcc
Create Date: 2024-09-25 16:34:43.256781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fb4dc7e62bf'
down_revision: Union[str, None] = 'eb1dd196fdcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('table_id', sa.Integer(), sa.ForeignKey('tables.id')),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True)
    )

def downgrade():
    op.drop_table('reservations')

