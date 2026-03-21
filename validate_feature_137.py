#!/usr/bin/env python3
"""Validation module for feature 137: markdown file test-narzc3.md.

Validates that the created markdown file meets all specification requirements:
- UTF-8 encoding without BOM
- Unix LF line endings (no CRLF)
- Proper markdown structure (H1 heading, blank line, prose)
- 2-3 sentences of prose content
- File size within acceptable range (320-600 bytes)
"""

from pathlib import Path


class ValidationError(Exception):
    """Raised when file validation fails."""

    pass


def validate_encoding(file_path: Path) -> None:
    """Validate file is UTF-8 encoded without BOM.

    Args:
        file_path: Path to the file to validate.

    Raises:
        ValidationError: If file is not valid UTF-8 or contains BOM.
    """
    try:
        file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise ValidationError(f"File is not valid UTF-8: {e}") from e

    binary_content = file_path.read_bytes()
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValidationError("File contains UTF-8 BOM (Byte Order Mark)")


def validate_line_endings(file_path: Path) -> None:
    """Validate file uses Unix LF line endings, not Windows CRLF.

    Args:
        file_path: Path to the file to validate.

    Raises:
        ValidationError: If file contains CRLF line endings.
    """
    binary_content = file_path.read_bytes()
    if b"\r\n" in binary_content:
        raise ValidationError(
            "File contains Windows-style CRLF line endings; must use Unix LF"
        )


def validate_structure(file_path: Path) -> None:
    """Validate markdown structure: heading + blank line + prose.

    Args:
        file_path: Path to the file to validate.

    Raises:
        ValidationError: If structure is incorrect.
    """
    text_content = file_path.read_text(encoding="utf-8")

    # Check for H1 heading on first line
    lines = text_content.split("\n")
    if not lines[0].startswith("# "):
        msg = f"First line must start with '# ' (H1 heading), got: {lines[0]!r}"
        raise ValidationError(msg)

    # Check for blank line after heading
    if len(lines) < 3 or lines[1].strip() != "":
        raise ValidationError("Line after heading must be blank")

    # Check for prose content after blank line
    prose_content = text_content.split("\n\n", 1)
    if len(prose_content) < 2:
        raise ValidationError("No prose content found after blank line")

    prose = prose_content[1].strip()
    if not prose:
        raise ValidationError("Prose content is empty")


def validate_prose_sentences(file_path: Path) -> None:
    """Validate prose contains 2-3 sentences.

    Args:
        file_path: Path to the file to validate.

    Raises:
        ValidationError: If prose sentence count is not 2-3.
    """
    text_content = file_path.read_text(encoding="utf-8")
    prose_content = text_content.split("\n\n", 1)[1].strip()

    # Count sentences (simple heuristic: count periods, question marks, exclamation marks)
    sentence_count = (
        prose_content.count(".") + prose_content.count("?") + prose_content.count("!")
    )

    if sentence_count < 2 or sentence_count > 3:
        msg = f"Prose must contain 2-3 sentences, found {sentence_count}"
        raise ValidationError(msg)


def validate_file_size(
    file_path: Path, min_bytes: int = 320, max_bytes: int = 600
) -> None:
    """Validate file size is within expected range.

    Args:
        file_path: Path to the file to validate.
        min_bytes: Minimum file size in bytes (default: 320).
        max_bytes: Maximum file size in bytes (default: 600).

    Raises:
        ValidationError: If file size is outside the acceptable range.
    """
    binary_content = file_path.read_bytes()
    file_size = len(binary_content)

    if file_size < min_bytes or file_size > max_bytes:
        msg = f"File size {file_size} bytes is outside acceptable range ({min_bytes}-{max_bytes} bytes)"
        raise ValidationError(msg)


def validate_file(file_path: Path) -> None:
    """Run all validation checks on the markdown file.

    Performs comprehensive validation including:
    - File existence
    - UTF-8 encoding without BOM
    - Unix LF line endings
    - Markdown structure (H1 heading, blank line, prose)
    - 2-3 sentences in prose
    - File size 320-600 bytes

    Args:
        file_path: Path to the file to validate.

    Raises:
        ValidationError: If any validation check fails.
    """
    if not file_path.exists():
        raise ValidationError(f"File does not exist: {file_path}")

    validate_encoding(file_path)
    validate_line_endings(file_path)
    validate_structure(file_path)
    validate_prose_sentences(file_path)
    validate_file_size(file_path)


if __name__ == "__main__":
    try:
        validate_file(Path("test-narzc3.md"))
        print(f"test-narzc3.md passed all validation checks")
    except ValidationError as e:
        print(f"Validation failed: {e}")
        exit(1)
