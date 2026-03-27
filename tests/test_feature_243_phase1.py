"""Tests for feature 243: Phase 1 - Content Generation and Validation.

Tests verify that the markdown file was created with proper structure, encoding,
and content validation according to specification requirements.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_file_test_31irev_exists():
    """Test that test-31irev.md file exists in repository root."""
    # Repository root is two levels up from this test file
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    assert markdown_file.exists(), f"File {markdown_file} does not exist"
    assert markdown_file.is_file(), f"{markdown_file} is not a regular file"


def test_file_utf8_encoding_without_bom():
    """Test that file uses UTF-8 encoding without BOM."""
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    with open(markdown_file, "rb") as f:
        binary_content = f.read()

    # Check for UTF-8 BOM (should not be present)
    assert not binary_content.startswith(b"\xef\xbb\xbf"), \
        "File has UTF-8 BOM (should not be present)"

    # Verify file is valid UTF-8
    try:
        text_content = binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")


def test_file_uses_lf_line_endings():
    """Test that file uses Unix LF line endings (not CRLF)."""
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    with open(markdown_file, "rb") as f:
        binary_content = f.read()

    # Check for CRLF line endings (should not be present)
    assert b"\r\n" not in binary_content, \
        "File uses CRLF line endings (should use LF)"


def test_file_has_h1_heading():
    """Test that file starts with H1 markdown heading."""
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    with open(markdown_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    lines = text_content.split("\n")
    assert lines[0].startswith("# "), "First line must be H1 heading (# )"


def test_file_has_blank_line_separator():
    """Test that file has blank line separator after heading."""
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    with open(markdown_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    lines = text_content.split("\n")
    assert len(lines) >= 2, "File must have at least 2 lines"
    assert lines[1] == "", "Second line must be blank (separator after heading)"


def test_file_has_prose_content():
    """Test that file contains prose content after heading."""
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    with open(markdown_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    lines = text_content.split("\n")
    # Extract prose (skip heading and blank line)
    prose = "\n".join(lines[2:]).strip()

    assert len(prose) > 0, "File must have prose content"
    assert len(prose) >= 50, "Prose content is too short"


def test_file_has_2_to_3_sentences():
    """Test that file has exactly 2-3 sentences (count periods)."""
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    with open(markdown_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    # Count sentences by counting periods
    period_count = text_content.count(".")
    assert 2 <= period_count <= 3, \
        f"Content must have 2-3 sentences, found {period_count}"


def test_file_size_in_expected_range():
    """Test that file size is in expected range (400-600 bytes)."""
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    file_size = markdown_file.stat().st_size
    # Allow some flexibility for different prose lengths
    assert 300 <= file_size <= 800, \
        f"File size {file_size} is outside expected range (300-800 bytes)"


def test_file_ends_with_newline():
    """Test that file ends with trailing newline (Unix convention)."""
    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    with open(markdown_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    assert text_content.endswith("\n"), \
        "File must end with trailing newline"


def test_markdown_file_validation():
    """Test that file passes full markdown validation."""
    import os

    repo_root = Path(__file__).parent.parent
    markdown_file = repo_root / "test-31irev.md"

    # Import the validation function
    from sheep.content_generators import validate_markdown_file

    # Change to repo root to ensure relative path resolution works
    original_cwd = os.getcwd()
    try:
        os.chdir(repo_root)
        # This should not raise any exceptions
        result = validate_markdown_file(str(markdown_file))
        assert result is True, "Validation should return True"
    finally:
        os.chdir(original_cwd)


def test_feature_module_exists():
    """Test that feature 243 module can be imported."""
    from sheep.features.feature_243_markdown_file_creation import (
        create_feature_243_markdown_file,
        FEATURE_NUMBER,
        MARKDOWN_FILENAME,
    )

    assert FEATURE_NUMBER == 243
    assert MARKDOWN_FILENAME == "test-31irev.md"
    assert create_feature_243_markdown_file is not None


if __name__ == "__main__":
    # Run tests manually if executed directly
    import traceback

    tests = [
        test_file_test_31irev_exists,
        test_file_utf8_encoding_without_bom,
        test_file_uses_lf_line_endings,
        test_file_has_h1_heading,
        test_file_has_blank_line_separator,
        test_file_has_prose_content,
        test_file_has_2_to_3_sentences,
        test_file_size_in_expected_range,
        test_file_ends_with_newline,
        test_markdown_file_validation,
        test_feature_module_exists,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
