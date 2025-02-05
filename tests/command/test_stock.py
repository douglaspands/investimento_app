from typer.testing import CliRunner

from app.cli import create_app

runner = CliRunner()


def test_get_stoke():
    result = runner.invoke(create_app(), ["stock", "get", "PETR3"])
    assert result.exit_code == 0
    assert "PETR3" in result.stdout


def test_list_stocks():
    result = runner.invoke(create_app(), ["stock", "list", "B3SA3", "AMER3"])
    assert result.exit_code == 0
    assert "B3SA3" in result.stdout
    assert "B3" in result.stdout
    assert "AMER3" in result.stdout
    assert "AMERICANAS" in result.stdout


def test_list_stocks_most_popular():
    result = runner.invoke(create_app(), ["stock", "most_popular"])
    assert result.exit_code == 0
    assert "BBAS3" in result.stdout
    assert "VALE3" in result.stdout
