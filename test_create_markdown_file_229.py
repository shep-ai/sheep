#!/usr/bin/env python3
"""
Tests for feature 229: markdown-file-creation-530bb9
Tests the create_and_validate_markdown() function for file creation and validation.
"""

import subprocess
import sys
from pathlib import Path

# Import the implementation module
sys.path.insert(0, str(Path(__file__).parent))
from create_markdown_file_229 import (
    create_and_validate_markdown,
    FILENAME,
    TITLE,
    PROSE,
)


def cleanup():
    """Remove test file if it exists."""
    if Path(FILENAME).exists():
        Path(FILENAME).unlink()


def test_markdown_file_exists():
    """Test that the markdown file exists after creation."""
    cleanup()

    create_and_validate_markdown()

    assert Path(FILENAME).exists(), f"{FILENAME} should exist after creation"

    cleanup()


def test_markdown_file_has_h1_heading():
    """Test that the markdown file starts with H1 heading."""
    cleanup()

    create_and_validate_markdown()

    content = Path(FILENAME).read_text(encoding="utf-8")
    assert content.startswith("# "), "File should start with H1 heading (# )"
    assert f"# {TITLE}" in content, f"File should contain H1 heading with title: {TITLE}"

    cleanup()


def test_markdown_file_has_prose_content():
    """Test that the markdown file contains expected prose content."""
    cleanup()

    create_and_validate_markdown()

    content = Path(FILENAME).read_text(encoding="utf-8")
    assert PROSE in content, "File should contain the prose content"

    cleanup()


def test_markdown_file_blank_line_separation():
    """Test that there is a blank line between heading and prose."""
    cleanup()

    create_and_validate_markdown()

    content = Path(FILENAME).read_text(encoding="utf-8")
    lines = content.split("\n")

    assert len(lines) >= 3, "File should have at least 3 lines (heading, blank, prose)"
    assert lines[0] == f"# {TITLE}", f"First line should be heading: # {TITLE}"
    assert lines[1] == "", "Second line should be blank"

    cleanup()


def test_markdown_file_utf8_encoding():
    """Test that the file is UTF-8 encoded."""
    cleanup()

    create_and_validate_markdown()

    with open(FILENAME, "rb") as f:
        raw_bytes = f.read()

    try:
        raw_bytes.decode("utf-8")
        is_utf8 = True
    except UnicodeDecodeError:
        is_utf8 = False

    assert is_utf8, "File should be UTF-8 encoded"

    cleanup()


def test_markdown_file_no_utf8_bom():
    """Test that the file does not have UTF-8 BOM."""
    cleanup()

    create_and_validate_markdown()

    with open(FILENAME, "rb") as f:
        first_bytes = f.read(3)

    assert first_bytes != b"\xef\xbb\xbf", "File should not have UTF-8 BOM"

    cleanup()


def test_markdown_file_lf_line_endings():
    """Test that the file uses LF line endings, not CRLF."""
    cleanup()

    create_and_validate_markdown()

    with open(FILENAME, "rb") as f:
        raw_bytes = f.read()

    has_crlf = b"\r\n" in raw_bytes
    assert not has_crlf, "File should use LF line endings, not CRLF"

    has_lf = b"\n" in raw_bytes
    assert has_lf, "File should contain LF line endings"

    cleanup()


def test_markdown_file_sentence_count():
    """Test that the file contains 2-3 sentences."""
    cleanup()

    create_and_validate_markdown()

    content = Path(FILENAME).read_text(encoding="utf-8")

    # Count sentences by counting . ! ? characters
    sentence_count = sum(1 for char in content if char in ".!?")
    assert 2 <= sentence_count <= 3, f"File should contain 2-3 sentences, found {sentence_count}"

    cleanup()


def test_markdown_file_size():
    """Test that the file size is in expected range (400-600 bytes)."""
    cleanup()

    create_and_validate_markdown()

    file_size = Path(FILENAME).stat().st_size
    assert 400 <= file_size <= 600, f"File size {file_size} should be between 400-600 bytes"

    cleanup()


def test_create_and_validate_returns_path():
    """Test that create_and_validate_markdown() returns a Path object."""
    cleanup()

    result = create_and_validate_markdown()

    assert isinstance(result, Path), "create_and_validate_markdown() should return a Path object"
    assert result.name == FILENAME, f"Returned path should have filename {FILENAME}"

    cleanup()


if __name__ == "__main__":
    # Run tests manually if desired
    test_markdown_file_exists()
    print("✓ test_markdown_file_exists passed")

    test_markdown_file_has_h1_heading()
    print("✓ test_markdown_file_has_h1_heading passed")

    test_markdown_file_has_prose_content()
    print("✓ test_markdown_file_has_prose_content passed")

    test_markdown_file_blank_line_separation()
    print("✓ test_markdown_file_blank_line_separation passed")

    test_markdown_file_utf8_encoding()
    print("✓ test_markdown_file_utf8_encoding passed")

    test_markdown_file_no_utf8_bom()
    print("✓ test_markdown_file_no_utf8_bom passed")

    test_markdown_file_lf_line_endings()
    print("✓ test_markdown_file_lf_line_endings passed")

    test_markdown_file_sentence_count()
    print("✓ test_markdown_file_sentence_count passed")

    test_markdown_file_size()
    print("✓ test_markdown_file_size passed")

    test_create_and_validate_returns_path()
    print("✓ test_create_and_validate_returns_path passed")

    print("\nAll tests passed!")
