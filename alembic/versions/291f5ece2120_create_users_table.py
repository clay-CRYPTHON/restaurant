"""create users table

Revision ID: 291f5ece2120
Revises: 6d31b7bad36e
Create Date: 2024-09-28 14:37:45.914614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '291f5ece2120'
down_revision: Union[str, None] = '6d31b7bad36e'
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