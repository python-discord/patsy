import asyncio
import logging

from alembic import context
from sqlalchemy.engine import Connection

from patsy.models.orm.base import Base
from patsy.settings import Connections, ConnectionURLs

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Configure logging
logger = logging.root
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt="%(levelname)-5.5s [%(name)s] %(message)s", datefmt="%H:%M:%S"))
logger.addHandler(handler)

# Configure metadata for auto generation
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=ConnectionURLs.DATABASE_URL.get_secret_value(),
        compare_type=True,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:  # noqa: D103
    context.configure(connection=connection, compare_type=True, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = Connections.DB_ENGINE
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
