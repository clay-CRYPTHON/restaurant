"""create modules table

Revision ID: 215d36dc3d0e
Revises: 7e5db20872cd
Create Date: 2024-09-25 16:33:18.190294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '215d36dc3d0e'
down_revision: Union[str, None] = '7e5db20872cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'modules',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('floor_id', sa.Integer(), sa.ForeignKey('floors.id')),
        sa.Column('table_id', sa.Integer(), sa.ForeignKey('tables.id'))
    )

def downgrade():
    op.drop_table('modules')