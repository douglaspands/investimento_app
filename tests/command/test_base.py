from typer.testing import CliRunner

from app.cli import create_app
from app.config import get_config

runner = CliRunner()


def test_get_version():
    result = runner.invoke(create_app(), ["version"])
    assert result.exit_code == 0
    config = get_config()
    assert config.version in result.stdout
