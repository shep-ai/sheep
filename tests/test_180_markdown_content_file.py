"""Tests for feature 180: markdown content file creation."""

from pathlib import Path


def test_markdown_file_exists_with_title_and_sentences():
    """Ensure test-7hid38.md has an H1 and 2-3 sentences."""
    repo_root = Path(__file__).parent.parent
    file_path = repo_root / "test-7hid38.md"

    assert file_path.exists()

    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    assert lines
    assert lines[0].startswith("# ")
    assert len(lines[0]) > 2
    assert len(lines) > 2
    assert lines[1] == ""

    prose = "\n".join(line for line in lines[2:] if line.strip())
    sentence_count = prose.count(".")
    assert 2 <= sentence_count <= 3
