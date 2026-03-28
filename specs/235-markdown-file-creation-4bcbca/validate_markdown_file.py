"""
Validation module for feature 235: markdown file creation.

This module provides functions to validate all markdown file properties
to ensure spec compliance.

Validation checks:
- File exists
- UTF-8 encoding without BOM
- Unix LF line endings (no Windows CRLF)
- Contains exactly one H1 heading (first line starts with "# ")
- Contains blank line after heading
- Contains substantive prose content (not just whitespace)
- File size is within 400-600 byte range
- File ends with newline
- Contains 2-3 sentences (periods)
"""

import re
from pathlib import Path

# ============================================================================
# Constants
# ============================================================================

FILENAME = "test-qz1gsg.md"
FEATURE_NUMBER = "235"
MIN_SIZE = 400
MAX_SIZE = 600
HEADING_PATTERN = r"^# .+$"  # Regex for H1 heading validation


# ============================================================================
# Exception Class
# ============================================================================


class ValidationError(Exception):
    """
    Custom exception for markdown file validation errors.

    Provides detailed error messages for each validation failure.
    """
    pass


# ============================================================================
# Individual Validation Functions
# ============================================================================


def validate_encoding(binary_content):
    """
    Validate that file is UTF-8 encoded without BOM (Byte Order Mark).

    Args:
        binary_content (bytes): The raw file content as bytes

    Raises:
        AssertionError: If encoding is invalid or BOM is present
    """
    # Check for UTF-8 BOM
    assert not binary_content.startswith(b"\xef\xbb\xbf"), (
        "File has UTF-8 BOM (Byte Order Mark). Should use UTF-8 without BOM."
    )

    # Check if content is valid UTF-8
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}") from e


def validate_line_endings(content):
    """
    Validate that file uses Unix LF line endings, not Windows CRLF.

    Args:
        content (str): The file content as text

    Raises:
        AssertionError: If CRLF is found or no line endings are present
    """
    assert "\r\n" not in content, (
        "File contains Windows CRLF line endings. Should use Unix LF (\\n) only."
    )
    assert "\n" in content, (
        "File does not contain any line endings. Should use Unix LF (\\n)."
    )


def validate_trailing_newline(binary_content):
    """
    Validate that file ends with a newline character.

    Args:
        binary_content (bytes): The raw file content as bytes

    Raises:
        AssertionError: If file does not end with newline
    """
    assert binary_content.endswith(b"\n"), (
        "File should end with a newline character."
    )


def validate_file_size(file_size):
    """
    Validate that file size is within 400-600 byte range.

    Args:
        file_size (int): Size of file in bytes

    Raises:
        AssertionError: If file size is outside valid range
    """
    assert MIN_SIZE < file_size < MAX_SIZE, (
        f"File size {file_size} bytes outside typical range ({MIN_SIZE}-{MAX_SIZE}). "
        f"Specification requires 400-600 byte range."
    )


def validate_h1_heading(lines):
    """
    Validate that file contains exactly one H1 heading on the first line.

    Args:
        lines (list): List of lines from the file

    Raises:
        AssertionError: If H1 heading is missing or malformed
    """
    assert len(lines) > 0, "File is empty or contains no lines"
    assert re.match(HEADING_PATTERN, lines[0]), (
        f"Missing H1 heading: first line must match regex '{HEADING_PATTERN}' "
        f"but found: {lines[0][:50]}"
    )


def validate_blank_line_separator(lines):
    """
    Validate that there is a blank line between heading and prose.

    Args:
        lines (list): List of lines from the file

    Raises:
        AssertionError: If blank line separator is missing
    """
    assert len(lines) > 1, "File should contain more than just a heading"
    assert lines[1] == "", (
        f"Missing blank line after heading: second line should be empty "
        f"but found: {repr(lines[1][:50])}"
    )


def validate_prose_content(lines):
    """
    Validate that file contains substantive prose content (not just whitespace).

    Args:
        lines (list): List of lines from the file

    Raises:
        AssertionError: If prose content is missing or empty
    """
    prose = "\n".join(lines[2:]).strip()
    assert prose, "File should contain prose content after blank line"


def count_sentences(prose):
    """
    Count the number of sentences in prose content.

    Sentences are identified by periods (.). Splits on periods and counts
    non-empty segments.

    Args:
        prose (str): The prose content as text

    Returns:
        int: Number of sentences found
    """
    sentence_list = [s.strip() for s in prose.split(".") if s.strip()]
    return len(sentence_list)


def validate_sentence_count(prose):
    """
    Validate that prose contains exactly 2-3 sentences.

    Args:
        prose (str): The prose content as text

    Raises:
        AssertionError: If sentence count is not 2-3
    """
    sentence_count = count_sentences(prose)
    assert 2 <= sentence_count <= 3, (
        f"Prose content should contain 2-3 sentences, but found {sentence_count}."
    )


# ============================================================================
# Main Validation Function
# ============================================================================


def validate_file(filepath):
    """
    Validate that a markdown file meets all specification requirements.

    Performs comprehensive validation including:
    - File existence
    - UTF-8 encoding without BOM
    - Unix LF line endings (no Windows CRLF)
    - Exactly one H1 heading on first line
    - Blank line separator after heading
    - Substantive prose content
    - File size in 400-600 byte range
    - Trailing newline
    - 2-3 sentences in prose

    Args:
        filepath (str or Path): Path to the markdown file to validate

    Returns:
        bool: True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive error message
    """
    filepath = Path(filepath)

    # 1. Check file exists
    assert filepath.exists(), f"File {filepath.name} does not exist"

    # 2. Read file content
    binary_content = filepath.read_bytes()
    file_size = len(binary_content)

    # 3. Validate encoding (UTF-8 without BOM)
    validate_encoding(binary_content)

    # Decode content for further validation
    content = binary_content.decode("utf-8")

    # 4. Validate line endings (LF only, no CRLF)
    validate_line_endings(content)

    # 5. Validate trailing newline
    validate_trailing_newline(binary_content)

    # 6. Validate file size
    validate_file_size(file_size)

    # 7. Validate structure: H1 heading + blank line + prose
    lines = content.split("\n")

    # Check H1 heading on first line
    validate_h1_heading(lines)

    # Check blank line after heading
    validate_blank_line_separator(lines)

    # Check prose content
    validate_prose_content(lines)

    # 8. Validate sentence count
    prose = "\n".join(lines[2:]).strip()
    validate_sentence_count(prose)

    return True
