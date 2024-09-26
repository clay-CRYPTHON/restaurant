"""create menu table

Revision ID: 4e5aff9000cc
Revises: 0728540cc5ba
Create Date: 2024-09-25 16:32:00.493522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e5aff9000cc'
down_revision: Union[str, None] = '0728540cc5ba'
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
