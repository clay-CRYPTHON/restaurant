"""Add tables table

Revision ID: af8463474a37
Revises: 6919928ab951
Create Date: 2024-09-14 11:35:18.730413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af8463474a37'
down_revision: Union[str, None] = '6919928ab951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tables',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('table_number', sa.Integer, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('capacity', sa.Integer, nullable=False),
        sa.Column('status', sa.String, nullable=False)
    )

def downgrade():
    op.drop_table('tables')