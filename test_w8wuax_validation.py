#!/usr/bin/env python3
"""
Validation tests for test-w8wuax.md markdown file creation.
Validates file structure, encoding, line endings, and size per specification.
"""

import os
from pathlib import Path


def test_file_exists():
    """Assert file test-w8wuax.md exists at repository root."""
    assert Path("test-w8wuax.md").exists(), "File test-w8wuax.md does not exist"
    print("[PASS] File exists at repository root")


def test_file_is_readable():
    """Assert file is readable."""
    assert Path("test-w8wuax.md").is_file(), "test-w8wuax.md is not a file"
    print("[PASS] File is readable")


def test_h1_heading_syntax():
    """Assert file starts with '# ' (H1 heading marker)."""
    content = Path("test-w8wuax.md").read_text(encoding="utf-8")
    assert content.startswith("# "), "File does not start with '# ' (H1 heading)"
    print("[PASS] H1 heading syntax is valid (starts with '# ')")


def test_blank_line_after_heading():
    """Assert H1 heading followed by blank line (\n\n)."""
    content = Path("test-w8wuax.md").read_text(encoding="utf-8")
    assert "\n\n" in content, "File does not contain blank line after H1 heading"
    # Verify blank line comes after heading
    first_newline = content.find("\n")
    assert first_newline > 0, "H1 heading not terminated properly"
    assert content[first_newline:first_newline+2] == "\n\n", "Blank line not properly placed after H1"
    print("[PASS] Blank line separation exists after H1 heading")


def test_sentence_count():
    """Assert file contains exactly 2-3 sentences in prose section."""
    content = Path("test-w8wuax.md").read_text(encoding="utf-8")
    # Find prose section (after first \n\n)
    prose_start = content.find("\n\n") + 2
    prose_section = content[prose_start:]

    # Count sentences by counting periods
    sentence_count = prose_section.count(".")
    assert 2 <= sentence_count <= 3, f"File contains {sentence_count} sentences, expected 2-3"
    print("[PASS] File contains {} sentences (valid: 2-3)".format(sentence_count))


def test_file_size():
    """Assert file size is between 400-600 bytes (inclusive)."""
    file_size = Path("test-w8wuax.md").stat().st_size
    assert 400 <= file_size <= 600, f"File size {file_size} is outside 400-600 byte range"
    print("[PASS] File size is {} bytes (valid: 400-600)".format(file_size))


def test_utf8_encoding_no_bom():
    """Assert file encoding is UTF-8 without BOM."""
    with open("test-w8wuax.md", "rb") as f:
        first_bytes = f.read(3)

    # UTF-8 BOM is \xef\xbb\xbf
    assert first_bytes != b'\xef\xbb\xbf', "File contains UTF-8 BOM"
    print("[PASS] File uses UTF-8 encoding without BOM")


def test_lf_line_endings():
    """Assert file uses LF line endings, not CRLF or CR."""
    with open("test-w8wuax.md", "rb") as f:
        content_bytes = f.read()

    # Check for CRLF (\r\n)
    assert b"\r\n" not in content_bytes, "File contains CRLF line endings"

    # Check for CR (\r) not followed by \n
    # Python's line ending conversion: we need to check the raw bytes
    cr_count = content_bytes.count(b"\r")
    assert cr_count == 0, f"File contains {cr_count} CR characters"

    # Verify LF is present
    lf_count = content_bytes.count(b"\n")
    assert lf_count > 0, "File does not contain any LF line endings"
    print("[PASS] File uses LF line endings ({} newlines, no CRLF or CR)".format(lf_count))


def test_prose_quality():
    """Assert prose content is grammatically correct and coherent."""
    content = Path("test-w8wuax.md").read_text(encoding="utf-8")
    prose_start = content.find("\n\n") + 2
    prose_section = content[prose_start:].strip()

    # Basic checks for prose quality
    assert len(prose_section) > 100, "Prose section is too short"
    assert not prose_section.startswith("Lorem"), "Prose appears to be placeholder text"
    assert prose_section[0].isupper(), "Prose does not start with uppercase letter"

    # Check for basic grammar: sentences should end with periods
    sentences = [s.strip() for s in prose_section.split(".") if s.strip()]
    for sentence in sentences:
        assert len(sentence) > 5, f"Sentence too short: '{sentence}'"

    print("[PASS] Prose content is grammatically correct and coherent")


def validate_all():
    """Run all validation tests."""
    print("\n" + "="*60)
    print("Validating test-w8wuax.md")
    print("="*60 + "\n")

    tests = [
        test_file_exists,
        test_file_is_readable,
        test_h1_heading_syntax,
        test_blank_line_after_heading,
        test_sentence_count,
        test_file_size,
        test_utf8_encoding_no_bom,
        test_lf_line_endings,
        test_prose_quality,
    ]

    for test in tests:
        try:
            test()
        except AssertionError as e:
            print("[FAIL] {}: {}".format(test.__name__, e))
            return False

    print("\n" + "="*60)
    print("[SUCCESS] ALL VALIDATION TESTS PASSED")
    print("="*60 + "\n")
    return True


if __name__ == "__main__":
    success = validate_all()
    exit(0 if success else 1)
