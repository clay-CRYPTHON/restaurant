"""Add menu table

Revision ID: 6919928ab951
Revises: 21f2ec4aff16
Create Date: 2024-09-14 11:33:52.371789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6919928ab951'
down_revision: Union[str, None] = '21f2ec4aff16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'menu',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('price', sa.Numeric, nullable=False),
        sa.Column('description', sa.Text)
    )

def downgrade():
    op.drop_table('menu')
