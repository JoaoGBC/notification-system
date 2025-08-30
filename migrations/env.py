import asyncio
import os
from logging.config import fileConfig
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
import sqlalchemy as sa

from alembic import context

sys.path.append(os.getcwd())
from dotenv import load_dotenv
load_dotenv()
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
db_name = config.config_ini_section
config.set_main_option(
    "sqlalchemy.url",
    os.environ[f"SQLALCHEMY_DATABASE_URI_{db_name.upper()}"]
)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = {}

from notification_system.templates_api.db_registry import metadata as template_api_metadata
import notification_system.templates_api.models
target_metadata['template_api_db'] = template_api_metadata



from notification_system.notification_workers.db_registry import metadata as notification_workers_metadata
import notification_system.notification_workers.models
target_metadata["notification_workers"] = notification_workers_metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_object(object, name, type_, reflected, compare_to):
    if type_ == 'table' and object.schema and object.schema.startswith("_timescaledb"):
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata.get(db_name),
        literal_binds=True,
        include_object=include_object,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()




def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata.get(db_name),
        include_schemas=True,
        include_object=include_object,
        version_table_schema = target_metadata.get(db_name).schema
    )
    connection.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{target_metadata.get(db_name).schema}"'))
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Usa create_async_engine para criar um engine assíncrono
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    # Conecta-se de forma assíncrona
    async with connectable.connect() as connection:
        # Executa as operações síncronas do Alembic dentro do loop de eventos
        await connection.run_sync(do_run_migrations)

    # Descarta o engine
    await connectable.dispose()



if context.is_offline_mode():
    run_migrations_offline()
else:
    # Executa a função assíncrona usando asyncio.run()
    asyncio.run(run_migrations_online())