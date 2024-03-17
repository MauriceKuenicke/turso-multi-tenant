import sys
import os
current_dir = os.getcwd()
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from sqlalchemy import engine_from_config
from sqlalchemy import pool, MetaData
from alembic import context
from sqlalchemy.sql import text
from app.domains.base import Base
from dotenv import load_dotenv

load_dotenv()
tables = Base.metadata.tables.values()
#############################################
#                INIT MODELS                #
#############################################
# Models need to be imported at one point to be discovered
from app.domains.organizations.model import *  # NOQA
from app.domains.user.model import *  # NOQA

#############################################

config = context.config

target_metadata = Base.metadata


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    token = os.getenv("TURSO_TOKEN")
    db_url = os.getenv("TURSO_ORG_DB")
    configuration["sqlalchemy.url"] = f"sqlite+{db_url}/?authToken={token}&secure=true"

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Get all tenant databases
    with connectable.connect() as connection:
        rows = connection.execute(text("SELECT db_url FROM organization;"))
        tenant_dbs = [x[0] for x in rows]

    tenant_metadata = MetaData()

    for table in Base.metadata.tables.values():
        if table.info["db"] == "tenant":
            table.tometadata(tenant_metadata)

    for tenant in tenant_dbs:
        db_url = tenant
        configuration["sqlalchemy.url"] = f"sqlite+{db_url}/?authToken={token}&secure=true"

        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=tenant_metadata, compare_type=True, include_schemas=False
            )

            with context.begin_transaction():
                context.run_migrations()
        print("Done.")


run_migrations_online()
