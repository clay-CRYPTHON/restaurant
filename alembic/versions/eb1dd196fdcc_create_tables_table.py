"""create tables table

Revision ID: eb1dd196fdcc
Revises: 215d36dc3d0e
Create Date: 2024-09-25 16:34:00.532947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb1dd196fdcc'
down_revision: Union[str, None] = '215d36dc3d0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tables',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('table_number', sa.Integer(), unique=True, index=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('capacity', sa.Integer()),
        sa.Column('module_id', sa.Integer(), sa.ForeignKey('modules.id')),
        sa.Column('status', sa.Enum('AVAILABLE', 'RESERVED', name='tablestatus'), default='AVAILABLE')
    )

def downgrade():
    op.drop_table('tables')