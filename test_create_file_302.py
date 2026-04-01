"""
Test suite for feature 302: markdown file creation.

This module tests the create_file_302.py script which creates test-94uqvv.md
with H1 heading, blank line separator, and 2-3 sentences of prose content.

Test Coverage:
- File creation with correct structure (H1 heading + blank line + prose)
- File exists at repository root
- First line starts with # (H1 markdown heading)
- Second line is empty (blank line separator)
- Prose contains 2-3 sentences
- File encoding is UTF-8 without BOM
- File uses Unix LF line endings (not CRLF)
- File size is in acceptable range (300-800 bytes)
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Add the repository root to the path so we can import the create_file_302 module
script_path = Path(__file__).parent / "create_file_302.py"
sys.path.insert(0, str(Path(__file__).parent))
from create_file_302 import create_file, validate_file


# ============================================================================
# Pytest Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """
    Provide an isolated temporary directory for test file creation.

    Yields a temporary directory path and restores the original working
    directory after the test completes. This fixture ensures tests don't
    interfere with the repository state or each other.

    Yields:
        Path: The temporary directory path
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)


# ============================================================================
# Test Cases: File Creation
# ============================================================================


def test_create_file_creates_file_at_root(temp_dir):
    """
    Test that create_file() creates test-94uqvv.md at repository root.

    This test verifies the basic requirement that the markdown file is
    created with the correct filename at the current directory.
    """
    filepath = create_file()
    assert filepath.exists(), "File test-94uqvv.md should exist"
    assert filepath.name == "test-94uqvv.md", "File should be named test-94uqvv.md"


def test_create_file_returns_path_object(temp_dir):
    """
    Test that create_file() returns a pathlib.Path object.
    """
    filepath = create_file()
    assert isinstance(filepath, Path), "create_file() should return a Path object"


def test_create_file_has_h1_heading(temp_dir):
    """
    Test that created file contains H1 markdown heading on first line.

    This test verifies:
    - First line starts with "# " (H1 markdown syntax)
    - Heading is followed by content
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    assert len(lines) > 0, "File should have content"
    assert lines[0].startswith('# '), "First line should be H1 heading (# )"


def test_create_file_has_blank_line_separator(temp_dir):
    """
    Test that created file has blank line separating heading from prose.

    This test verifies that there is a blank line (double newline) between
    the H1 heading and the prose content.
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    assert '\n\n' in content, "File should contain blank line separator"

    # Verify the blank line is in the correct position
    lines = content.split('\n')
    assert lines[0].startswith('# '), "First line should be H1 heading"
    assert lines[1] == '', "Second line should be empty (blank line)"


def test_create_file_has_prose_content(temp_dir):
    """
    Test that created file contains prose content after blank line.

    This test verifies that there is actual text content in the prose section.
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    parts = content.split('\n\n', 1)
    assert len(parts) == 2, "File should have heading and prose separated by blank line"
    prose = parts[1].strip()
    assert len(prose) > 0, "Prose section should contain text"


def test_create_file_prose_has_sentences(temp_dir):
    """
    Test that prose content contains 2-3 sentences.

    This test counts periods in the prose to estimate sentence count.
    A simple heuristic: count periods in the prose section.
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    parts = content.split('\n\n', 1)
    prose = parts[1].strip()

    # Count sentences by periods
    sentence_count = prose.count('.')
    assert 2 <= sentence_count <= 3, f"Prose should have 2-3 sentences, found {sentence_count}"


def test_create_file_utf8_encoding(temp_dir):
    """
    Test that file is UTF-8 encoded.

    This test verifies that the file can be read with UTF-8 encoding
    without raising an exception.
    """
    filepath = create_file()
    content = filepath.read_text(encoding='utf-8')
    assert isinstance(content, str), "Content should be readable as UTF-8"


def test_create_file_no_bom(temp_dir):
    """
    Test that file does not contain UTF-8 BOM (Byte Order Mark).

    BOM signature for UTF-8 is bytes: 0xEF 0xBB 0xBF
    """
    filepath = create_file()
    file_bytes = filepath.read_bytes()
    bom_signature = b'\xef\xbb\xbf'
    assert not file_bytes.startswith(bom_signature), "File should not have UTF-8 BOM"


def test_create_file_unix_lf_endings(temp_dir):
    """
    Test that file uses Unix LF line endings, not Windows CRLF.

    CRLF signature: 0x0D 0x0A
    LF signature: 0x0A (only)
    """
    filepath = create_file()
    file_bytes = filepath.read_bytes()
    crlf_signature = b'\r\n'
    assert crlf_signature not in file_bytes, "File should use LF endings, not CRLF"


def test_create_file_size_in_range(temp_dir):
    """
    Test that file size is in acceptable range (300-800 bytes).

    This validates that the file has reasonable content length.
    """
    filepath = create_file()
    file_size = filepath.stat().st_size
    assert 300 < file_size < 800, (
        f"File size {file_size} should be between 300-800 bytes"
    )


# ============================================================================
# Test Cases: File Validation
# ============================================================================


def test_validate_file_passes_for_valid_file(temp_dir):
    """
    Test that validate_file() returns True for a valid markdown file.
    """
    filepath = create_file()
    result = validate_file(filepath)
    assert result is True, "validate_file() should return True for valid file"


def test_validate_file_fails_for_nonexistent_file(temp_dir):
    """
    Test that validate_file() raises AssertionError for nonexistent file.
    """
    filepath = Path("nonexistent.md")
    with pytest.raises(AssertionError, match="does not exist"):
        validate_file(filepath)


def test_validate_file_fails_for_file_too_small(temp_dir):
    """
    Test that validate_file() fails if file is too small (<300 bytes).
    """
    # Create a small file
    small_file = Path("small.md")
    small_file.write_text("# Title\n\nSmall content.", encoding='utf-8')

    with pytest.raises(AssertionError, match="outside typical range"):
        validate_file(small_file)


def test_validate_file_fails_for_missing_h1(temp_dir):
    """
    Test that validate_file() fails if H1 heading is missing.
    """
    # Create file without H1 heading
    filepath = Path("test.md")
    filepath.write_text("No heading here\n\nThis is prose content.", encoding='utf-8')

    with pytest.raises(AssertionError, match="H1 heading"):
        validate_file(filepath)


def test_validate_file_fails_for_missing_blank_line(temp_dir):
    """
    Test that validate_file() fails if blank line separator is missing.
    """
    # Create file without blank line separator but with enough content to pass size check
    prose = "This is a longer prose section to make the file bigger. " * 5
    filepath = Path("test.md")
    filepath.write_text(f"# Title\nNo blank line here\n{prose}", encoding='utf-8')

    with pytest.raises(AssertionError, match="blank line"):
        validate_file(filepath)


# ============================================================================
# Integration Tests
# ============================================================================


def test_create_and_validate_integration(temp_dir):
    """
    Integration test: create file and validate it passes all checks.

    This test verifies the complete workflow of creating and validating
    the markdown file.
    """
    filepath = create_file()
    result = validate_file(filepath)

    assert filepath.exists(), "File should exist"
    assert result is True, "Validation should pass"


def test_file_structure_order(temp_dir):
    """
    Test that file structure is in correct order: heading -> blank -> prose.
    """
    filepath = create_file()
    lines = filepath.read_text(encoding='utf-8').split('\n')

    # Verify structure
    assert lines[0].startswith('# '), "Line 1: H1 heading"
    assert lines[1] == '', "Line 2: blank line"
    assert len(lines) > 2, "Should have prose content"
    assert len(lines[2]) > 0, "Line 3+: prose content"
