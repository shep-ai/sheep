\"""Sheep CLI - Command line interface for the agentic platform."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from sheep import __version__
from sheep.config.settings import get_settings
from sheep.observability import init_observability, setup_logging
from sheep.hello import say_hello # New import

app = typer.Typer(
    name="sheep