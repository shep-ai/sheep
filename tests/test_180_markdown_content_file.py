"""Tests for feature 180: markdown file content creation."""

from pathlib import Path


def test_180_markdown_file_exists_with_title_and_2_to_3_sentences():
    repo_root = Path(__file__).parent.parent
    test_file = repo_root / "test-6pu9k7.md"

    assert test_file.exists()

    content = test_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    assert lines
    assert lines[0].startswith("# ")
    assert len(lines[0]) > 2

    prose_lines = [line.strip() for line in lines[1:] if line.strip()]
    prose = " ".join(prose_lines)

    sentence_count = prose.count(".")
    assert 2 <= sentence_count <= 3
