#!/usr/bin/env python3
"""Test script for markdown file creation feature 257."""

import sys
import re
from pathlib import Path


def test_file_exists():
    """Test that test-z5u8bz.md exists at repository root."""
    file_path = Path("test-z5u8bz.md")
    assert file_path.exists(), f"File {file_path} does not exist"
    print("✓ File exists at repository root")


def test_markdown_heading():
    """Test that file contains a markdown heading (# followed by space and text)."""
    file_path = Path("test-z5u8bz.md")
    content = file_path.read_text(encoding="utf-8")

    # Check for H1 heading syntax (# followed by space)
    assert re.match(r"^# .+", content), "File does not start with markdown heading (# )"
    print("✓ File contains markdown heading syntax")


def test_blank_line_after_heading():
    """Test that file has blank line separating heading from prose."""
    file_path = Path("test-z5u8bz.md")
    content = file_path.read_text(encoding="utf-8")

    lines = content.split("\n")
    assert len(lines) >= 3, "File does not have enough lines"
    assert lines[0].startswith("# "), "First line is not a heading"
    assert lines[1] == "", "Second line is not blank"
    assert lines[2].strip() != "", "Third line is blank (should contain prose)"
    print("✓ File has blank line after heading")


def test_prose_content():
    """Test that file contains 2-3 sentences of coherent prose."""
    file_path = Path("test-z5u8bz.md")
    content = file_path.read_text(encoding="utf-8")

    lines = content.split("\n")
    prose = "\n".join(lines[2:]).strip()

    # Count sentences (simple: periods, exclamation marks, question marks)
    sentence_count = len(re.findall(r"[.!?]", prose))
    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"
    print(f"✓ File contains {sentence_count} sentences")


def test_utf8_encoding_without_bom():
    """Test that file is UTF-8 encoded without byte order mark."""
    file_path = Path("test-z5u8bz.md")

    # Read file as binary to check for BOM
    with open(file_path, "rb") as f:
        content = f.read()

    # UTF-8 BOM is b'\xef\xbb\xbf'
    assert not content.startswith(b"\xef\xbb\xbf"), "File has UTF-8 BOM"

    # Verify content is valid UTF-8
    try:
        content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    print("✓ File is UTF-8 encoded without BOM")


def test_lf_line_endings():
    """Test that file uses LF (Unix-style) line endings, not CRLF."""
    file_path = Path("test-z5u8bz.md")

    # Read file as binary
    with open(file_path, "rb") as f:
        content = f.read()

    # Check for CRLF (\r\n)
    assert b"\r\n" not in content, "File contains CRLF line endings"
    assert b"\r" not in content, "File contains CR line endings"

    # Verify file contains LF
    assert b"\n" in content, "File does not contain any line endings"
    print("✓ File uses LF line endings")


def test_file_size():
    """Test that file size is approximately 400-600 bytes."""
    file_path = Path("test-z5u8bz.md")
    size = file_path.stat().st_size

    assert 400 <= size <= 600, f"File size {size} is not in range 400-600 bytes"
    print(f"✓ File size is {size} bytes (in range 400-600)")


def test_commonmark_validity():
    """Test that markdown syntax is valid (simple check for common issues)."""
    file_path = Path("test-z5u8bz.md")
    content = file_path.read_text(encoding="utf-8")

    lines = content.split("\n")

    # Check heading format
    assert lines[0].startswith("# "), "Heading does not follow # syntax"
    assert len(lines[0]) > 2, "Heading text is empty"

    # Check blank line
    assert lines[1] == "", "Missing blank line after heading"

    # Check prose is present and not empty
    prose_lines = [line for line in lines[2:] if line.strip()]
    assert len(prose_lines) > 0, "No prose content found"

    print("✓ Markdown syntax is valid")


if __name__ == "__main__":
    tests = [
        test_file_exists,
        test_markdown_heading,
        test_blank_line_after_heading,
        test_prose_content,
        test_utf8_encoding_without_bom,
        test_lf_line_endings,
        test_file_size,
        test_commonmark_validity,
    ]

    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed.append(test.__name__)

    if failed:
        print(f"\n{len(failed)} test(s) failed")
        sys.exit(1)
    else:
        print(f"\nAll {len(tests)} tests passed ✓")
        sys.exit(0)
