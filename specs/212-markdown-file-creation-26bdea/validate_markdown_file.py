#!/usr/bin/env python3
"""
Validation script for markdown file test-e6mp6y.md.

This script validates that test-e6mp6y.md meets all feature 212 requirements:
- File exists and is readable
- File size is 300-800 bytes (typical 400-600)
- File is UTF-8 encoded without BOM
- File has Unix LF line endings (not Windows CRLF)
- File contains H1 markdown heading
- File has blank line after heading
- File contains 2-3 sentences of substantive prose
"""

import sys
from pathlib import Path


def validate_file(filepath):
    """
    Validate a markdown file against feature 212 requirements.

    Args:
        filepath (Path or str): Path to the markdown file to validate

    Returns:
        tuple: (success: bool, message: str)
    """
    filepath = Path(filepath)
    errors = []

    # Check file exists and is readable
    if not filepath.exists():
        return False, f"File {filepath} does not exist"

    if not filepath.is_file():
        return False, f"Path {filepath} is not a file"

    # Try to read file
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        return False, f"File is not valid UTF-8: {e}"
    except Exception as e:
        return False, f"Cannot read file {filepath}: {e}"

    # Check file size
    file_size = filepath.stat().st_size
    if not (300 <= file_size <= 800):
        errors.append(
            f"File size {file_size} bytes outside typical range (300-800). "
            f"Expected 400-600 as soft guideline."
        )

    # Check binary properties
    try:
        binary_content = filepath.read_bytes()
    except Exception as e:
        return False, f"Cannot read file as binary: {e}"

    # Check no UTF-8 BOM
    if binary_content.startswith(b'\xef\xbb\xbf'):
        errors.append("File has UTF-8 BOM (Byte Order Mark) - should not have it")

    # Check no CRLF line endings
    if b'\r\n' in binary_content:
        errors.append("File uses Windows CRLF line endings - should use Unix LF")

    # Check has LF line endings
    if b'\n' not in binary_content:
        errors.append("File does not contain LF line endings")

    # Check file ends with newline
    if not binary_content.endswith(b'\n'):
        errors.append("File does not end with a newline character")

    # Check H1 heading
    if not content.startswith('# '):
        errors.append("File should start with H1 markdown heading (# Title)")

    # Check blank line after heading
    if '\n\n' not in content:
        errors.append("File should have blank line separating heading from prose")

    # Split heading and prose
    parts = content.split('\n\n', 1)
    heading = parts[0].strip()
    prose = parts[1].strip() if len(parts) > 1 else ""

    # Check heading is not empty
    if len(heading) <= 2:
        errors.append("Heading should contain meaningful content")

    # Check prose is substantive
    if len(prose) <= 50:
        errors.append("Prose content should be substantive (more than 50 characters)")

    # Check sentence count (rough estimate by counting periods)
    period_count = prose.count('.')
    if period_count < 2:
        errors.append(
            f"File should contain at least 2 sentences, found {period_count} periods"
        )
    if period_count > 4:
        errors.append(
            f"File should contain at most 3 sentences, found {period_count} periods"
        )

    # Return results
    if errors:
        return False, "\n".join(f"  ✗ {error}" for error in errors)

    return True, "All validations passed"


def print_file_info(filepath):
    """Print information about the file."""
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"File {filepath} does not exist")
        return

    print(f"\n📄 File Information for {filepath}")
    print("=" * 70)

    # Basic info
    file_size = filepath.stat().st_size
    print(f"  Size: {file_size} bytes")

    # Content info
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    print(f"  Lines: {len(lines)}")

    # Heading info
    heading = lines[0] if lines else ""
    print(f"  Heading: {heading}")

    # Prose info
    if len(lines) > 2:
        prose = '\n'.join(lines[2:]).strip()
        period_count = prose.count('.')
        print(f"  Prose length: {len(prose)} characters")
        print(f"  Estimated sentences: {period_count}")

    # Encoding info
    binary_content = filepath.read_bytes()
    has_bom = binary_content.startswith(b'\xef\xbb\xbf')
    has_crlf = b'\r\n' in binary_content
    ends_with_newline = binary_content.endswith(b'\n')

    print(f"  UTF-8 BOM: {'Yes (WRONG)' if has_bom else 'No (correct)'}")
    print(f"  CRLF line endings: {'Yes (WRONG)' if has_crlf else 'No (correct)'}")
    print(f"  Ends with newline: {'Yes (correct)' if ends_with_newline else 'No (WRONG)'}")

    print("=" * 70 + "\n")


def main():
    """Main validation function."""
    filepath = Path("test-e6mp6y.md")

    # Print file information
    print_file_info(filepath)

    # Run validation
    success, message = validate_file(filepath)

    if success:
        print("✅ Validation Result: PASSED")
        print(f"   {message}\n")
        return 0
    else:
        print("❌ Validation Result: FAILED")
        print("Errors found:")
        print(message + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
