from typer.testing import CliRunner

from app.cli import create_app

runner = CliRunner()


def test_get_reit():
    result = runner.invoke(create_app(), ["reit", "get", "BPML11"])
    assert result.exit_code == 0
    assert "BPML11" in result.stdout
    assert "FDO INV IMOB BTG PACTUAL SHOPPINGS" in result.stdout


def test_list_reits():
    result = runner.invoke(create_app(), ["reit", "list", "HTMX11", "PORD11"])
    assert result.exit_code == 0
    assert "HTMX11" in result.stdout
    assert "Hotel" in result.stdout
    assert "PORD11" in result.stdout
    assert "Polo" in result.stdout


def test_list_reits_most_popular():
    result = runner.invoke(create_app(), ["reit", "most_popular"])
    assert result.exit_code == 0
    assert "MXRF11" in result.stdout
    assert "XPML11" in result.stdout
