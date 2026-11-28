import os
import pytest


def test_vgcxus_markdown_file_exists():
    """Test that test-vgcxus.md file exists."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "test-vgcxus.md")
    assert os.path.exists(file_path), "test-vgcxus.md file does not exist"


def test_vgcxus_markdown_file_content():
    """Test that test-vgcxus.md contains expected content."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "test-vgcxus.md")
    with open(file_path, "r") as f:
        content = f.read()

    assert "# The Art of Fermentation" in content
    assert "Fermentation" in content
    assert len(content) > 100


def test_vgcxus_markdown_file_has_title():
    """Test that test-vgcxus.md has a markdown title."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "test-vgcxus.md")
    with open(file_path, "r") as f:
        content = f.read()

    assert content.startswith("#"), "File should start with a markdown heading"
