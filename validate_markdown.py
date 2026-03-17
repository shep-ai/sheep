#!/usr/bin/env python3
"""Validation script for markdown file format compliance."""

from pathlib import Path


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_encoding(file_path: Path) -> None:
    """Validate file is UTF-8 encoded without BOM."""
    try:
        file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValidationError(f"File is not valid UTF-8: {e}") from e

    binary_content = file_path.read_bytes()
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValidationError("File contains UTF-8 BOM (Byte Order Mark)")


def validate_line_endings(file_path: Path) -> None:
    """Validate file uses Unix LF line endings, not Windows CRLF."""
    binary_content = file_path.read_bytes()
    if b'\r\n' in binary_content:
        msg = "File contains Windows-style CRLF line endings; must use Unix LF"
        raise ValidationError(msg)


def validate_structure(file_path: Path) -> None:
    """Validate markdown structure: heading + blank line + prose."""
    text_content = file_path.read_text(encoding='utf-8')

    # Check for H1 heading on first line
    lines = text_content.split('\n')
    if not lines[0].startswith('# '):
        msg = f"First line must start with '# ' (H1 heading), got: {lines[0]!r}"
        raise ValidationError(msg)

    # Check for blank line after heading
    if len(lines) < 3 or lines[1].strip() != '':
        raise ValidationError("Line after heading must be blank")

    # Check for prose content after blank line
    prose_content = text_content.split('\n\n', 1)
    if len(prose_content) < 2:
        raise ValidationError("No prose content found after blank line")

    prose = prose_content[1].strip()
    if not prose:
        raise ValidationError("Prose content is empty")


def validate_prose_sentences(file_path: Path) -> None:
    """Validate prose contains 2-3 sentences."""
    text_content = file_path.read_text(encoding='utf-8')
    prose_content = text_content.split('\n\n', 1)[1].strip()

    # Count sentences (simple heuristic: count periods, question marks, exclamation marks)
    sentence_count = prose_content.count('.') + prose_content.count('?') + prose_content.count('!')

    if sentence_count < 2 or sentence_count > 3:
        msg = f"Prose must contain 2-3 sentences, found {sentence_count}"
        raise ValidationError(msg)


def validate_file_size(file_path: Path, min_bytes: int = 350, max_bytes: int = 650) -> None:
    """Validate file size is within expected range."""
    binary_content = file_path.read_bytes()
    file_size = len(binary_content)

    if file_size < min_bytes or file_size > max_bytes:
        msg = f"File size {file_size} bytes is outside acceptable range ({min_bytes}-{max_bytes} bytes)"
        raise ValidationError(msg)


def validate_file(file_path: Path) -> None:
    """Run all validation checks on the markdown file."""
    if not file_path.exists():
        raise ValidationError(f"File does not exist: {file_path}")

    try:
        validate_encoding(file_path)
        validate_line_endings(file_path)
        validate_structure(file_path)
        validate_prose_sentences(file_path)
        validate_file_size(file_path)
        print(f"✓ {file_path.name} passed all validation checks")
    except ValidationError as e:
        print(f"✗ {file_path.name} validation failed: {e}")
        raise


if __name__ == '__main__':
    validate_file(Path('test-3nslmx.md'))
