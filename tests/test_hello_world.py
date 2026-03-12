"""Tests for hello-world command."""

from typer.testing import CliRunner

from sheep.cli import app


def test_hello_world_prints_hello_world():
    """Test that the hello-world command prints Hello World."""
    runner = CliRunner()
    result = runner.invoke(app, ["hello-world"])
    assert result.exit_code == 0
    assert "Hello World" in result.output
