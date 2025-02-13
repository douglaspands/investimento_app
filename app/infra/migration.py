from alembic import command
from alembic.config import Config

from app.config import get_config


def upgrade_head():
    config = get_config()
    alembic_cfg = Config(f"{config.alembic_ini!s}")
    alembic_cfg.set_main_option("script_location", str(config.alembic_migration_folder))
    command.upgrade(alembic_cfg, "head")
