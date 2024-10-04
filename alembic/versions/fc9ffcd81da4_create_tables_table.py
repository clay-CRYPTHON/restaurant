"""create tables table

Revision ID: fc9ffcd81da4
Revises: 4cacfd6742db
Create Date: 2024-09-28 15:08:25.628086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fc9ffcd81da4'
down_revision: Union[str, None] = '4cacfd6742db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tables',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('table_number', sa.Integer(), unique=True, index=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('capacity', sa.Integer()),
        sa.Column('module_id', sa.Integer(), sa.ForeignKey('modules.id')),
        sa.Column('status', sa.Enum('AVAILABLE', 'RESERVED', name='tablestatus'), default='AVAILABLE')
    )


def downgrade() -> None:
    op.drop_table('tables')