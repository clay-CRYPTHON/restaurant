"""Add menu table

Revision ID: 21f2ec4aff16
Revises: 697f0c542c57
Create Date: 2024-09-14 10:14:04.934246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21f2ec4aff16'
down_revision: Union[str, None] = '697f0c542c57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('phone_number', sa.String),
        sa.Column('hashed_password', sa.String),
        sa.Column('role', sa.String),
    )

def downgrade():
    op.drop_table('users')