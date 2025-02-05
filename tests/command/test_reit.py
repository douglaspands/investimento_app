from typer.testing import CliRunner

from app.cli import create_app

runner = CliRunner()


def test_get_reit():
    result = runner.invoke(create_app(), ["reit", "get", "MXRF11"])
    assert result.exit_code == 0
    assert "MXRF11" in result.stdout
    assert "Maxi Renda" in result.stdout


def test_list_reits():
    result = runner.invoke(create_app(), ["reit", "list", "MXRF11", "XPML11"])
    assert result.exit_code == 0
    assert "MXRF11" in result.stdout
    assert "Maxi Renda" in result.stdout
    assert "XPML11" in result.stdout
    assert "XP Malls" in result.stdout
