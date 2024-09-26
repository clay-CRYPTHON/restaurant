"""create users table

Revision ID: 0728540cc5ba
Revises: da6c28763411
Create Date: 2024-09-25 16:29:28.297120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0728540cc5ba'
down_revision: Union[str, None] = 'da6c28763411'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('username', sa.String(), unique=True, index=True),
        sa.Column('first_name', sa.String()),
        sa.Column('last_name', sa.String()),
        sa.Column('phone_number', sa.String()),
        sa.Column('hashed_password', sa.String()),
        sa.Column('role', sa.Enum('NAZORATCHI', 'AFISSANT', 'HODIM', 'USER', name='roleenum'), index=True)
    )

def downgrade():
    op.drop_table('users')