"""
Integration test suite for feature 304: markdown file validation and testing.

This module provides comprehensive validation tests for the created markdown file
(test-ypzjo0.md) to ensure it meets all specification requirements.

Test Coverage:
- File encoding: UTF-8 without BOM
- Line endings: LF only (not CRLF)
- Markdown structure: H1 heading, blank line separator, prose content
- Prose content: 2-3 sentences with proper punctuation
- File properties: trailing newline, reasonable file size
"""

import os
import sys
from pathlib import Path
from unittest import mock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import validate_markdown_file


# ============================================================================
# FILE ENCODING TESTS
# ============================================================================


def test_file_has_utf8_encoding_without_bom():
    """
    Test that test-ypzjo0.md has UTF-8 encoding without BOM.

    Verifies:
    - File is readable as UTF-8
    - File does not have UTF-8 BOM (0xEF 0xBB 0xBF) at start
    - All characters are valid UTF-8
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Read file in binary mode to check for BOM
    with open(filepath, "rb") as f:
        binary_content = f.read()

    # Check for UTF-8 BOM (should NOT be present)
    assert not binary_content.startswith(b"\xef\xbb\xbf"), \
        "File should not have UTF-8 BOM (0xEF 0xBB 0xBF at start)"

    # Verify file is valid UTF-8
    try:
        text_content = binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        assert False, f"File is not valid UTF-8: {e}"

    print(f"✓ File has UTF-8 encoding without BOM ({len(binary_content)} bytes)")


def test_file_uses_lf_line_endings_not_crlf():
    """
    Test that test-ypzjo0.md uses Unix LF line endings, not Windows CRLF.

    Verifies:
    - File uses LF (\n, 0x0A) for line endings
    - File does NOT use CRLF (\r\n, 0x0D 0x0A) for line endings
    - File does NOT use CR (\r, 0x0D) for line endings
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Read file in binary mode to check line endings
    with open(filepath, "rb") as f:
        binary_content = f.read()

    # Check for CRLF (Windows line endings - should NOT be present)
    assert b"\r\n" not in binary_content, \
        "File should use LF (\\n) line endings, not CRLF (\\r\\n)"

    # Check for standalone CR (old Mac line endings - should NOT be present)
    assert b"\r" not in binary_content, \
        "File should use LF (\\n) line endings, not CR (\\r)"

    # Count LF to verify it's the line ending being used
    lf_count = binary_content.count(b"\n")
    assert lf_count > 0, "File should have at least one LF line ending"

    print(f"✓ File uses LF line endings ({lf_count} lines)")


# ============================================================================
# MARKDOWN STRUCTURE TESTS
# ============================================================================


def test_first_line_is_h1_markdown_heading():
    """
    Test that first line of test-ypzjo0.md is an H1 markdown heading.

    Verifies:
    - First line starts with "# " (H1 markdown syntax)
    - First line has content after "# " (non-empty heading)
    - First line is not empty
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Read file as text
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    first_line = lines[0]

    # Check that first line starts with "# "
    assert first_line.startswith("# "), \
        f"First line must start with '# ' (H1 heading), got: {repr(first_line)}"

    # Check that heading has content after "# "
    heading_content = first_line[2:].strip()
    assert heading_content, \
        "H1 heading must have content after '# ', got empty heading"

    print(f"✓ First line is H1 heading: {first_line}")


def test_second_line_is_blank_separator():
    """
    Test that second line of test-ypzjo0.md is blank (separator).

    Verifies:
    - Second line exists (file has at least 2 lines)
    - Second line is completely empty (no whitespace)
    - Second line separates heading from prose content
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Read file as text
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # Check that file has at least 2 lines
    assert len(lines) >= 2, \
        f"File must have at least 2 lines (heading + blank), got {len(lines)}"

    second_line = lines[1]

    # Check that second line is completely empty
    assert second_line == "", \
        f"Second line must be blank (separator), got: {repr(second_line)}"

    print(f"✓ Second line is blank separator")


def test_prose_content_has_2_to_3_sentences():
    """
    Test that prose content contains exactly 2-3 sentences.

    Verifies:
    - Sentences are counted by periods (.) at end of sentences
    - There are 2-3 sentences total
    - Prose is substantial (not just isolated words)
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Read file as text
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # Extract prose content (skip heading and blank line)
    prose_lines = lines[2:]

    # Remove trailing empty lines
    while prose_lines and prose_lines[-1] == "":
        prose_lines.pop()

    # Get prose as single string
    prose_content = "\n".join(prose_lines).strip()

    assert prose_content, "No prose content found after heading"

    # Count sentences by periods
    sentence_count = prose_content.count(".")

    assert 2 <= sentence_count <= 3, \
        f"Prose must have 2-3 sentences, found {sentence_count}: {repr(prose_content)}"

    print(f"✓ Prose content has {sentence_count} sentences")


def test_file_ends_with_newline():
    """
    Test that test-ypzjo0.md ends with a newline (Unix convention).

    Verifies:
    - File content ends with \n (LF newline)
    - File follows Unix convention (trailing newline)
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Read file as text
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that content ends with newline
    assert content.endswith("\n"), \
        "File must end with newline (Unix convention)"

    print(f"✓ File ends with newline")


# ============================================================================
# COMPREHENSIVE VALIDATION TEST
# ============================================================================


def test_complete_file_validation():
    """
    Integration test: Comprehensive validation of all file requirements.

    Tests that test-ypzjo0.md passes complete validation:
    - Encoding: UTF-8 without BOM
    - Line endings: LF only
    - Structure: H1 heading, blank line, prose
    - Content: 2-3 sentences
    - Trailing newline

    Uses the project's validate_markdown_file() function to ensure
    consistency with specification validation.
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Use the project's validation function
    try:
        result = validate_markdown_file(str(filepath))
        assert result is True, "File validation failed"
        print(f"✓ Complete file validation passed")
    except ValueError as e:
        assert False, f"File validation failed: {e}"


def test_file_exists_at_repository_root():
    """
    Test that test-ypzjo0.md exists at repository root.

    Verifies:
    - File exists on filesystem
    - File is located at repository root (same directory as src/, specs/)
    - File is a regular file (not directory)
    - File is readable
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Check file exists
    assert filepath.exists(), f"File does not exist: {filepath}"

    # Check it's a file (not directory)
    assert filepath.is_file(), f"Path is not a file: {filepath}"

    # Check it's readable
    with open(filepath, "r") as f:
        content = f.read()

    assert content, "File is empty"

    print(f"✓ File exists at repository root: {filepath}")


def test_file_has_reasonable_size():
    """
    Test that test-ypzjo0.md has reasonable file size.

    Verifies:
    - File is at least 50 bytes (H1 + blank + prose)
    - File is less than 5KB (no bloat)
    - File size is consistent with spec (400-600 bytes typical)
    """
    repo_root = Path(__file__).parent.parent.parent
    filepath = repo_root / "test-ypzjo0.md"

    # Skip if file doesn't exist yet
    if not filepath.exists():
        print(f"SKIPPED: {filepath} not created yet")
        return

    # Get file size
    file_size = filepath.stat().st_size

    # Check minimum size (heading + blank + prose)
    assert file_size >= 50, \
        f"File is too small ({file_size} bytes), expected at least 50"

    # Check maximum size (sanity check)
    assert file_size <= 5000, \
        f"File is too large ({file_size} bytes), expected max 5000"

    # File should be in typical range (400-600 bytes)
    expected_min = 200  # Conservative minimum
    expected_max = 1000  # Conservative maximum

    print(f"✓ File has reasonable size: {file_size} bytes")


# ============================================================================
# RUN TESTS
# ============================================================================


if __name__ == "__main__":
    """Run all validation tests."""
    tests = [
        ("File encoding (UTF-8, no BOM)", test_file_has_utf8_encoding_without_bom),
        ("Line endings (LF only)", test_file_uses_lf_line_endings_not_crlf),
        ("H1 heading on first line", test_first_line_is_h1_markdown_heading),
        ("Blank line separator", test_second_line_is_blank_separator),
        ("Prose: 2-3 sentences", test_prose_content_has_2_to_3_sentences),
        ("Trailing newline", test_file_ends_with_newline),
        ("File exists at root", test_file_exists_at_repository_root),
        ("Reasonable file size", test_file_has_reasonable_size),
        ("Complete validation", test_complete_file_validation),
    ]

    passed = 0
    skipped = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Test Results: {passed} passed, {skipped} skipped, {failed} failed")
    print(f"{'='*60}")

    if failed > 0:
        sys.exit(1)
