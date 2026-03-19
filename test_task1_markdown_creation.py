"""Test for markdown file creation task (task-1)."""

import re
from pathlib import Path


def test_file_exists():
    """Assert file exists in repository root."""
    file_path = Path("test-oyjp7x.md")
    assert file_path.exists(), f"File {file_path} does not exist"
    assert file_path.is_file(), f"{file_path} is not a file"


def test_file_contains_single_h1_heading():
    """Assert file contains exactly one H1 heading."""
    content = Path("test-oyjp7x.md").read_text(encoding='utf-8')
    h1_count = content.count('\n# ') + (1 if content.startswith('# ') else 0)
    assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"


def test_blank_line_separates_heading_from_prose():
    """Assert file has blank line separating heading from prose."""
    content = Path("test-oyjp7x.md").read_text(encoding='utf-8')
    lines = content.split('\n')
    assert len(lines) >= 3, f"File should have at least 3 lines, found {len(lines)}"
    assert lines[0].startswith('# '), f"First line should be H1 heading, got: {lines[0]}"
    assert lines[1] == '', f"Second line should be blank, got: {repr(lines[1])}"


def test_prose_content_is_valid():
    """Assert prose content is 2-3 sentences."""
    content = Path("test-oyjp7x.md").read_text(encoding='utf-8')
    lines = content.split('\n')

    # Get prose (everything after the blank line)
    prose = '\n'.join(lines[2:]).strip()
    assert prose, "Prose content is empty"

    # Count sentences (roughly: period, exclamation, or question mark followed by space or end)
    sentences = re.split(r'[.!?]+\s+', prose)
    # Remove empty strings and count
    sentences = [s.strip() for s in sentences if s.strip()]

    # Account for final sentence (may not have space after punctuation)
    sentence_count = len([s for s in sentences if s])
    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"


def test_file_size_in_guideline():
    """Assert file size is between 400-600 bytes."""
    file_path = Path("test-oyjp7x.md")
    file_size = len(file_path.read_bytes())
    assert 400 <= file_size <= 600, f"File size {file_size} not in 400-600 byte range"


if __name__ == "__main__":
    # Run tests
    test_file_exists()
    print("[PASS] File exists")

    test_file_contains_single_h1_heading()
    print("[PASS] Contains exactly one H1 heading")

    test_blank_line_separates_heading_from_prose()
    print("[PASS] Blank line separates heading from prose")

    test_prose_content_is_valid()
    print("[PASS] Prose content is 2-3 sentences")

    test_file_size_in_guideline()
    print("[PASS] File size is within 400-600 bytes")

    print("\nAll tests passed!")
