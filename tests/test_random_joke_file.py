"""Tests for random joke file functionality."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sheep.utils import get_random_joke

REPO_ROOT = Path(__file__).parent.parent
RANDOM_JOKE_FILE = REPO_ROOT / "RANDOM_JOKE.md"


def test_file_exists():
    """Test that the RANDOM_JOKE.md file exists."""
    assert RANDOM_JOKE_FILE.exists(), f"{RANDOM_JOKE_FILE} does not exist"


def test_file_is_not_empty():
    """Test that the file contains content."""
    content = RANDOM_JOKE_FILE.read_text(encoding="utf-8")
    assert len(content) > 0, "File is empty"


def test_file_contains_markdown_heading():
    """Test that the file contains a markdown heading."""
    content = RANDOM_JOKE_FILE.read_text(encoding="utf-8")
    assert "# Joke" in content or "#" in content, "File does not contain a markdown heading"


def test_get_random_joke_returns_string():
    """Test that get_random_joke returns a string."""
    joke = get_random_joke(REPO_ROOT)
    assert isinstance(joke, str), "get_random_joke should return a string"


def test_get_random_joke_returns_content():
    """Test that get_random_joke returns non-empty content."""
    joke = get_random_joke(REPO_ROOT)
    assert len(joke) > 0, "get_random_joke should return non-empty content"
