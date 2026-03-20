#!/usr/bin/env python3
"""
Test suite for feature 130: Create markdown file test-ppqzc5.md.
Validates file creation, content structure, encoding, and line endings.
"""

import pathlib
import subprocess
import sys


def test_file_exists():
    """Test that test-ppqzc5.md exists in the repository root."""
    test_file = pathlib.Path("test-ppqzc5.md")
    assert test_file.exists(), "File test-ppqzc5.md does not exist"
    print("PASS: File test-ppqzc5.md exists")


def test_file_has_exactly_one_heading():
    """Test that file contains exactly one level-1 markdown heading."""
    test_file = pathlib.Path("test-ppqzc5.md")
    content = test_file.read_text(encoding='utf-8')
    heading_count = content.count('\n# ') + (1 if content.startswith('# ') else 0)
    assert heading_count == 1, f"Expected 1 level-1 heading, found {heading_count}"
    assert content.startswith('# '), "File must start with a level-1 heading"
    print("PASS: File contains exactly one level-1 heading at the start")


def test_heading_followed_by_blank_line():
    """Test that heading is followed by exactly one blank line."""
    test_file = pathlib.Path("test-ppqzc5.md")
    content = test_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    # First line should be heading
    assert lines[0].startswith('# '), "First line must be a heading"

    # Second line should be empty (blank line)
    assert lines[1] == '', "Second line must be blank after heading"

    # Third line should have content (prose)
    assert len(lines) > 2 and lines[2], "Prose content must start on line 3"
    print("PASS: Heading is followed by exactly one blank line")


def test_prose_content():
    """Test that file contains exactly 2-3 complete sentences after blank line."""
    test_file = pathlib.Path("test-ppqzc5.md")
    content = test_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Get prose content (everything after heading and blank line)
    prose = '\n'.join(lines[2:]).strip()

    # Count sentences (basic count by periods, question marks, exclamation marks)
    sentence_count = prose.count('.') + prose.count('?') + prose.count('!')

    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    # Verify prose is not empty and contains words
    words = prose.split()
    assert len(words) >= 20, f"Prose seems too short, only {len(words)} words found"

    print(f"PASS: File contains {sentence_count} complete sentences with {len(words)} words")


def test_utf8_encoding_no_bom():
    """Test that file is UTF-8 encoded without BOM."""
    test_file = pathlib.Path("test-ppqzc5.md")
    with open(test_file, 'rb') as f:
        first_bytes = f.read(3)

    # UTF-8 BOM is bytes EF BB BF
    assert first_bytes != b'\xef\xbb\xbf', "File should not have UTF-8 BOM"

    # Verify file can be read as UTF-8
    try:
        test_file.read_text(encoding='utf-8')
        print("PASS: File is UTF-8 encoded without BOM")
    except UnicodeDecodeError:
        raise AssertionError("File is not valid UTF-8")


def test_lf_line_endings():
    """Test that file uses LF (0x0A) line endings, not CRLF (0x0D 0x0A)."""
    test_file = pathlib.Path("test-ppqzc5.md")
    with open(test_file, 'rb') as f:
        content_bytes = f.read()

    # Check for CRLF (0x0D 0x0A)
    assert b'\r\n' not in content_bytes, "File should use LF line endings, not CRLF"

    # Check that file contains LF endings
    assert b'\n' in content_bytes, "File should contain LF line endings"

    print("PASS: File uses LF (0x0A) line endings, not CRLF")


def test_file_size():
    """Test that file size is between 400-600 bytes."""
    test_file = pathlib.Path("test-ppqzc5.md")
    file_size = test_file.stat().st_size

    assert 400 <= file_size <= 600, f"File size {file_size} is outside 400-600 byte range"
    print(f"PASS: File size is {file_size} bytes (within 400-600 range)")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        ("File exists", test_file_exists),
        ("Exactly one heading", test_file_has_exactly_one_heading),
        ("Heading followed by blank line", test_heading_followed_by_blank_line),
        ("Prose content (2-3 sentences)", test_prose_content),
        ("UTF-8 encoding without BOM", test_utf8_encoding_no_bom),
        ("LF line endings", test_lf_line_endings),
        ("File size 400-600 bytes", test_file_size),
    ]

    print("\n" + "=" * 60)
    print("Testing test-ppqzc5.md file creation")
    print("=" * 60 + "\n")

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"FAIL: {test_name}: Unexpected error: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
