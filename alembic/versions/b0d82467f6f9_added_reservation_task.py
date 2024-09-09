"""Added reservation task

Revision ID: b0d82467f6f9
Revises: 31b6695b3469
Create Date: 2024-09-05 15:04:33.849517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0d82467f6f9'
down_revision: Union[str, None] = '31b6695b3469'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Enum turini yaratish
    op.execute("CREATE TYPE roleenum AS ENUM ('NAZORATCHI', 'AFISSANT', 'HODIM', 'USER')")

    # Ustunning turini enumga o'zgartirish
    op.alter_column('users', 'role', type_=sa.Enum('NAZORATCHI', 'AFISSANT', 'HODIM', 'USER', name='roleenum'),
                    nullable=False)


def downgrade():
    # Enum turini o'chirish uchun rollback
    op.execute('DROP TYPE roleenum')
    op.alter_column('users', 'role', type_=sa.String(), nullable=False)
