from sqlalchemy import engine_from_config, pool
from alembic import context
from app import models
from alembic import op
import sqlalchemy as sa

config = context.config
config.set_main_option('sqlalchemy.url', 'postgresql+psycopg2://postgres:abbossetdarov@localhost/restaurants_db')

target_metadata = models.Base.metadata


def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


def upgrade():
    # 'users' jadvali va 'role' ustuni nomlarini moslashtiring
    op.execute('ALTER TABLE users ALTER COLUMN role TYPE role_enum_type USING role::role_enum_type')



def downgrade():
    op.execute("DROP TYPE role_enum_type")