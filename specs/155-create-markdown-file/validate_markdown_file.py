"""Validation functions for markdown file creation."""

from pathlib import Path
from typing import Union


# Constants for validation
MIN_FILE_SIZE = 300  # bytes (lower tolerance bound)
MAX_FILE_SIZE = 800  # bytes (upper tolerance bound)
IDEAL_MIN_SIZE = 400  # bytes (ideal range lower bound)
IDEAL_MAX_SIZE = 600  # bytes (ideal range upper bound)
MIN_SENTENCES = 2
MAX_SENTENCES = 3


def validate_file_exists(filepath: Union[str, Path]) -> bool:
    """
    Validate that the file exists.

    Args:
        filepath: Path to the file to validate

    Returns:
        True if file exists

    Raises:
        AssertionError: If file does not exist
    """
    filepath = Path(filepath)
    assert filepath.exists(), f"File {filepath} does not exist"
    return True


def validate_file_size(filepath: Union[str, Path]) -> bool:
    """
    Validate that file size is within acceptable range (300-800 bytes).

    Args:
        filepath: Path to the file to validate

    Returns:
        True if file size is valid

    Raises:
        AssertionError: If file size is outside typical range
    """
    filepath = Path(filepath)
    file_size = filepath.stat().st_size

    assert (
        MIN_FILE_SIZE < file_size < MAX_FILE_SIZE
    ), (
        f"File size {file_size} bytes is outside typical range "
        f"({IDEAL_MIN_SIZE}-{IDEAL_MAX_SIZE}). Acceptable range: {MIN_FILE_SIZE}-{MAX_FILE_SIZE} bytes."
    )
    return True


def validate_encoding(filepath: Union[str, Path]) -> bool:
    """
    Validate that file is UTF-8 encoded without BOM (Byte Order Mark).

    Args:
        filepath: Path to the file to validate

    Returns:
        True if encoding is valid UTF-8 without BOM

    Raises:
        AssertionError: If encoding is invalid or BOM is present
    """
    filepath = Path(filepath)
    binary_content = filepath.read_bytes()

    # Check for UTF-8 BOM
    utf8_bom = b'\xef\xbb\xbf'
    assert not binary_content.startswith(
        utf8_bom
    ), "File should not have UTF-8 BOM (Byte Order Mark)"

    # Verify content can be decoded as UTF-8
    try:
        binary_content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    return True


def validate_line_endings(filepath: Union[str, Path]) -> bool:
    """
    Validate that file uses Unix LF line endings, not Windows CRLF.

    Args:
        filepath: Path to the file to validate

    Returns:
        True if line endings are LF only

    Raises:
        AssertionError: If CRLF line endings are found
    """
    filepath = Path(filepath)
    binary_content = filepath.read_bytes()

    # Check for CRLF (\r\n)
    assert (
        b'\r\n' not in binary_content
    ), "File should use Unix LF line endings (\\n), not Windows CRLF (\\r\\n)"

    # Verify file contains at least one LF line ending
    assert (
        b'\n' in binary_content
    ), "File should contain LF line endings (\\n)"

    return True


def validate_markdown_structure(filepath: Union[str, Path]) -> bool:
    """
    Validate that file has proper markdown structure with H1 heading and blank line.

    Args:
        filepath: Path to the file to validate

    Returns:
        True if markdown structure is valid

    Raises:
        AssertionError: If structure is invalid
    """
    filepath = Path(filepath)
    content = filepath.read_text(encoding='utf-8')

    # Split by double newline to separate heading from prose
    parts = content.split('\n\n', 1)

    assert len(parts) >= 2, (
        "File should have blank line separating heading from prose. "
        "Expected structure: '# Heading\\n\\n<prose>'"
    )

    heading_section = parts[0].strip()

    # Verify heading starts with exactly one # (H1, not H2/H3/etc)
    # H1: "# Title"
    # H2+: "## Title" or "### Title" etc
    if heading_section.startswith('##'):
        raise AssertionError(
            f"First section should be H1 heading (starting with '# '), "
            f"got: {heading_section[:50]}"
        )

    if not heading_section.startswith('#'):
        raise AssertionError(
            f"First section should be H1 heading (starting with '#'), "
            f"got: {heading_section[:50]}"
        )

    # Verify heading is not just "# " with no content
    # Remove the '#' and any following spaces, check if content remains
    heading_content = heading_section[1:].strip()  # Skip the '#' and leading spaces
    assert len(heading_content) > 0, "Heading should have meaningful content"

    return True


def validate_prose_content(filepath: Union[str, Path]) -> bool:
    """
    Validate that file contains 2-3 sentences of prose content.

    Args:
        filepath: Path to the file to validate

    Returns:
        True if prose content is valid

    Raises:
        AssertionError: If prose is missing or incorrect
    """
    filepath = Path(filepath)
    content = filepath.read_text(encoding='utf-8')

    # Split heading and prose by double newline
    parts = content.split('\n\n', 1)

    assert len(parts) >= 2, "File should have prose content after heading"

    prose = parts[1].strip()

    # Verify prose is not empty
    assert len(prose) > 0, "Prose section should not be empty"

    # Count sentences (periods that end sentences)
    # This is a heuristic: count periods but allow for some flexibility
    # (abbreviations, ellipsis, etc.)
    sentence_count = prose.count('.')

    # Should have at least 2 periods (2-3 sentences)
    assert sentence_count >= MIN_SENTENCES, (
        f"File should contain at least {MIN_SENTENCES} sentences, "
        f"found {sentence_count} period(s)"
    )

    # Allow up to 4 periods (3 sentences + possible abbreviation or trailing punctuation)
    # We use 4 as max because we want to be lenient but still validate structure
    assert sentence_count <= (MAX_SENTENCES + 1), (
        f"File should contain at most {MAX_SENTENCES} sentences, "
        f"found {sentence_count} period(s)"
    )

    return True


def validate_file(filepath: Union[str, Path]) -> bool:
    """
    Comprehensive validation of markdown file.

    Checks:
    - File exists
    - File size is in acceptable range (300-800 bytes)
    - File is UTF-8 encoded without BOM
    - File uses LF line endings only
    - File has proper markdown structure (H1 heading + blank line + prose)
    - File contains 2-3 sentences of prose

    Args:
        filepath: Path to the file to validate

    Returns:
        True if all validations pass

    Raises:
        AssertionError: If any validation fails (with descriptive message)
    """
    filepath = Path(filepath)

    # Run all validations in order
    validate_file_exists(filepath)
    validate_file_size(filepath)
    validate_encoding(filepath)
    validate_line_endings(filepath)
    validate_markdown_structure(filepath)
    validate_prose_content(filepath)

    return True
