from typer.testing import CliRunner

from sheep.hello import say_hello
from sheep.cli import app

runner = CliRunner()

def test_say_hello_default():
    assert say_hello() == "Hello, Sheep!"

def test_say_hello_name():
    assert say_hello("World