"""Tests for feature 178: sample markdown file creation."""

from pathlib import Path


def test_sample_markdown_file_exists_with_title_and_prose():
    """Validate the requested markdown file has a title and 2-3 sentences."""
    repo_root = Path(__file__).resolve().parents[1]
    markdown_file = repo_root / "test-d90nu8.md"

    assert markdown_file.exists()

    content = markdown_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    assert lines
    assert lines[0].startswith("# ")

    prose = " ".join(lines[2:]).strip()
    sentence_count = prose.count(".")
    assert 2 <= sentence_count <= 3
