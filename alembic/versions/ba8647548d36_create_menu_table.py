"""create menu table

Revision ID: ba8647548d36
Revises: 291f5ece2120
Create Date: 2024-09-28 14:42:08.228376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ba8647548d36'
down_revision: Union[str, None] = '291f5ece2120'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'menu',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String()),
        sa.Column('price', sa.Integer()),
        sa.Column('description', sa.String())
    )

def downgrade():
    op.drop_table('menu')