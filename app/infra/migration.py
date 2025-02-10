from alembic import command
from alembic.config import Config


def migration_upgrade_head():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
