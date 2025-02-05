from typer.testing import CliRunner

from app.cli import create_app

runner = CliRunner()


def test_get_stoke():
    result = runner.invoke(create_app(), ["stock", "get", "ITSA3"])
    assert result.exit_code == 0
    assert "ITSA3" in result.stdout
    assert "ITAUSA" in result.stdout


def test_list_stocks():
    result = runner.invoke(create_app(), ["stock", "list", "ITSA3", "BBDC3"])
    assert result.exit_code == 0
    assert "ITSA3" in result.stdout
    assert "ITAUSA" in result.stdout
    assert "BBDC3" in result.stdout
    assert "BRADESCO" in result.stdout
