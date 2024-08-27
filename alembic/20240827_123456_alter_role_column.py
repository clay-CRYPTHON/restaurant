from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE users ALTER COLUMN role TYPE role_enum_type USING role::role_enum_type')
