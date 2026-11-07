from typer.testing import CliRunner

from vectrix.cli import app

runner = CliRunner()


def test_version_command():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "VECTRIX" in result.stdout
    assert "0.1.0" in result.stdout


def test_help_command():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "version" in result.stdout