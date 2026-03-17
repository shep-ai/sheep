"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env_file():
    """Load .env file for tests if it exists."""
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        load_dotenv(env_file)
