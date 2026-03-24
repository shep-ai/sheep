#!/usr/bin/env python3
"""
Validation module for test-l5g799.md markdown file.

Provides comprehensive validation functions to check:
- Markdown syntax (H1 heading on first line)
- Sentence count (exactly 2-3 sentences)
- Encoding (UTF-8 without BOM)
- Line endings (LF only, no CRLF)
- File size (250-600 bytes)
- File structure and CommonMark compliance

Usage:
    from validate_l5g799 import ValidationError, validate_markdown_file

    try:
        validate_markdown_file(Path('test-l5g799.md'))
        print("✓ All validations passed")
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
        exit(1)
"""

import re
from pathlib import Path
from typing import Tuple


class ValidationError(Exception):
    """Raised when file validation fails."""
    pass


def validate_file_exists(filepath: Path) -> None:
    """
    Validate that the file exists.

    Args:
        filepath: Path to the file to validate

    Raises:
        ValidationError: If file does not exist
    """
    if not filepath.exists():
        raise ValidationError(f"File does not exist: {filepath}")


def validate_utf8_encoding(filepath: Path) -> None:
    """
    Validate that file is valid UTF-8 encoded.

    Args:
        filepath: Path to the file to validate

    Raises:
        ValidationError: If file is not valid UTF-8
    """
    try:
        filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValidationError(f"File is not valid UTF-8: {e}")


def validate_no_bom(filepath: Path) -> None:
    """
    Validate that file does not contain UTF-8 BOM (byte order mark).

    Args:
        filepath: Path to the file to validate

    Raises:
        ValidationError: If file contains UTF-8 BOM
    """
    file_bytes = filepath.read_bytes()
    if file_bytes.startswith(b'\xef\xbb\xbf'):
        raise ValidationError("File contains UTF-8 BOM (0xEFBBBF) - should have no BOM")


def validate_line_endings(filepath: Path) -> None:
    """
    Validate that file uses Unix LF line endings (not CRLF).

    Args:
        filepath: Path to the file to validate

    Raises:
        ValidationError: If file contains CRLF or CR characters
    """
    file_bytes = filepath.read_bytes()

    # Check for CRLF (Windows line endings)
    if b'\r\n' in file_bytes:
        raise ValidationError("File contains CRLF line endings - should use LF only")

    # Check for any CR characters
    if b'\r' in file_bytes:
        raise ValidationError("File contains CR characters - should use LF only")


def validate_h1_heading(content: str) -> None:
    """
    Validate that first line is a valid H1 markdown heading.

    Args:
        content: File content as string

    Raises:
        ValidationError: If H1 heading is invalid
    """
    lines = content.split('\n')
    if not lines:
        raise ValidationError("File is empty")

    first_line = lines[0]

    # Check basic format: starts with "# "
    if not first_line.startswith('# '):
        raise ValidationError(
            f"First line should start with '# ' (H1 heading), got: {first_line!r}"
        )

    # Check proper H1 format: # followed by space and at least one word character
    heading_pattern = r'^#\s+\w+'
    if not re.match(heading_pattern, first_line):
        raise ValidationError(
            f"H1 heading does not match pattern '^#\\s+\\w+': {first_line!r}"
        )


def validate_blank_line_after_heading(content: str) -> None:
    """
    Validate that second line is blank (after H1 heading).

    Args:
        content: File content as string

    Raises:
        ValidationError: If blank line is missing or invalid
    """
    lines = content.split('\n')

    if len(lines) < 3:
        raise ValidationError(
            f"File should have at least 3 lines (heading + blank + prose), got {len(lines)}"
        )

    second_line = lines[1]
    if second_line != '':
        raise ValidationError(
            f"Second line should be blank, got: {second_line!r}"
        )


def validate_prose_content(content: str) -> Tuple[str, int]:
    """
    Validate that prose content exists and return it with minimum length check.

    Args:
        content: File content as string

    Returns:
        Tuple of (prose_content, prose_length)

    Raises:
        ValidationError: If prose content is invalid or too short
    """
    parts = content.split('\n\n', 1)
    if len(parts) != 2:
        raise ValidationError(
            "File should be split into heading and prose by blank line"
        )

    prose = parts[1].strip()
    if not prose:
        raise ValidationError("Prose content should not be empty")

    # Minimum length check (at least 100 characters for substantive content)
    if len(prose) < 100:
        raise ValidationError(
            f"Prose content is too short ({len(prose)} chars), expected at least 100"
        )

    return prose, len(prose)


def validate_sentence_count(prose: str) -> int:
    """
    Validate that prose contains exactly 2-3 sentences.

    Counts sentences by terminal punctuation (. ! ?).

    Args:
        prose: Prose content as string

    Returns:
        Number of sentences found

    Raises:
        ValidationError: If sentence count is not 2-3
    """
    # Count sentences using regex: terminal punctuation (. ! ?)
    sentence_pattern = r'[.!?]'
    sentence_count = len(re.findall(sentence_pattern, prose))

    if sentence_count < 2:
        raise ValidationError(
            f"Prose must contain at least 2 sentences, found {sentence_count}"
        )

    if sentence_count > 3:
        raise ValidationError(
            f"Prose must contain at most 3 sentences, found {sentence_count}"
        )

    return sentence_count


def validate_file_size(filepath: Path, min_bytes: int = 250, max_bytes: int = 600) -> int:
    """
    Validate that file size is within specified range.

    Args:
        filepath: Path to the file to validate
        min_bytes: Minimum file size in bytes (default 250)
        max_bytes: Maximum file size in bytes (default 600)

    Returns:
        Actual file size in bytes

    Raises:
        ValidationError: If file size is outside range
    """
    file_bytes = filepath.read_bytes()
    file_size = len(file_bytes)

    if file_size < min_bytes:
        raise ValidationError(
            f"File size {file_size} bytes is below minimum {min_bytes} bytes"
        )

    if file_size > max_bytes:
        raise ValidationError(
            f"File size {file_size} bytes exceeds maximum {max_bytes} bytes"
        )

    return file_size


def validate_commonmark_structure(content: str) -> None:
    """
    Validate that file structure is CommonMark compliant.

    Args:
        content: File content as string

    Raises:
        ValidationError: If structure is not CommonMark compliant
    """
    # Should start with H1 heading
    if not content.startswith('# '):
        raise ValidationError("File must start with H1 heading (# )")

    # Should have blank line after heading
    if '\n\n' not in content:
        raise ValidationError("File must have blank line after heading")

    # Should not have multiple consecutive blank lines
    if '\n\n\n' in content:
        raise ValidationError("File should not have multiple consecutive blank lines")


def validate_no_trailing_whitespace(content: str) -> None:
    """
    Validate that lines do not have trailing whitespace.

    Args:
        content: File content as string

    Raises:
        ValidationError: If any line has trailing whitespace
    """
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Allow empty lines, but not trailing spaces on non-empty lines
        if line and not line.isspace():
            if line != line.rstrip():
                raise ValidationError(
                    f"Line {i + 1} has trailing whitespace: {line!r}"
                )


def validate_markdown_file(filepath: Path) -> dict:
    """
    Comprehensive validation of markdown file.

    Validates:
    - File existence
    - UTF-8 encoding (no BOM)
    - Unix LF line endings
    - H1 heading on first line
    - Blank line after heading
    - Prose content (100+ characters)
    - Exactly 2-3 sentences
    - File size (250-600 bytes)
    - CommonMark structure compliance
    - No trailing whitespace

    Args:
        filepath: Path to the file to validate

    Returns:
        Dictionary with validation results:
        {
            'file_exists': True,
            'encoding_valid': True,
            'no_bom': True,
            'line_endings_lf': True,
            'file_size_bytes': 466,
            'sentence_count': 3,
            'prose_length': 420,
            'all_valid': True
        }

    Raises:
        ValidationError: If any validation fails (with descriptive error message)
    """
    results = {
        'file_exists': False,
        'encoding_valid': False,
        'no_bom': False,
        'line_endings_lf': False,
        'file_size_bytes': 0,
        'sentence_count': 0,
        'prose_length': 0,
        'all_valid': False
    }

    # Check file existence
    validate_file_exists(filepath)
    results['file_exists'] = True

    # Check UTF-8 encoding
    validate_utf8_encoding(filepath)
    results['encoding_valid'] = True

    # Check for BOM
    validate_no_bom(filepath)
    results['no_bom'] = True

    # Check line endings
    validate_line_endings(filepath)
    results['line_endings_lf'] = True

    # Read content for further validation
    content = filepath.read_text(encoding='utf-8')

    # Check file size
    file_size = validate_file_size(filepath)
    results['file_size_bytes'] = file_size

    # Check H1 heading
    validate_h1_heading(content)

    # Check blank line after heading
    validate_blank_line_after_heading(content)

    # Check prose content
    prose, prose_length = validate_prose_content(content)
    results['prose_length'] = prose_length

    # Check sentence count
    sentence_count = validate_sentence_count(prose)
    results['sentence_count'] = sentence_count

    # Check CommonMark structure
    validate_commonmark_structure(content)

    # Check for trailing whitespace
    validate_no_trailing_whitespace(content)

    results['all_valid'] = True
    return results


def print_validation_report(filepath: Path, results: dict) -> None:
    """
    Print a formatted validation report.

    Args:
        filepath: Path to the validated file
        results: Dictionary from validate_markdown_file()
    """
    print("\n" + "=" * 70)
    print(f"VALIDATION REPORT: {filepath.name}")
    print("=" * 70)

    checks = [
        ("File Exists", results.get('file_exists', False)),
        ("UTF-8 Encoding", results.get('encoding_valid', False)),
        ("No BOM", results.get('no_bom', False)),
        ("LF Line Endings", results.get('line_endings_lf', False)),
        ("File Size Valid (250-600 bytes)", True),  # Check separately below
        ("H1 Heading Present", True),
        ("Blank Line After Heading", True),
        ("Prose Content Valid", results.get('prose_length', 0) >= 100),
        ("Sentence Count (2-3)", True),  # Check separately below
        ("CommonMark Compliant", True),
        ("No Trailing Whitespace", True),
    ]

    for check_name, passed in checks:
        status = "[OK]" if passed else "[FAIL]"
        print(f"{status} {check_name}")

    print("\n" + "-" * 70)
    print(f"File Size: {results.get('file_size_bytes', 0)} bytes (range: 250-600)")
    print(f"Sentence Count: {results.get('sentence_count', 0)} (required: 2-3)")
    print(f"Prose Length: {results.get('prose_length', 0)} characters")
    print("-" * 70)

    if results.get('all_valid', False):
        print("\n[OK] ALL VALIDATIONS PASSED")
        print(f"[OK] File {filepath.name} is ready for git commit")
    else:
        print("\n[FAIL] VALIDATION FAILED")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Example usage
    filepath = Path("test-l5g799.md")

    try:
        results = validate_markdown_file(filepath)
        print_validation_report(filepath, results)
        exit(0)
    except ValidationError as e:
        print(f"\n✗ VALIDATION FAILED: {e}\n")
        exit(1)
