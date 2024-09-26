"""create floors table

Revision ID: 7e5db20872cd
Revises: 4e5aff9000cc
Create Date: 2024-09-25 16:32:40.688765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e5db20872cd'
down_revision: Union[str, None] = '4e5aff9000cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'floors',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False)
    )

def downgrade():
    op.drop_table('floors')
