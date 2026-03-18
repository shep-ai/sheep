#!/usr/bin/env python3
"""
Create and validate markdown file test-mprgt7.md following the established pattern.

This script demonstrates:
1. Prose validation before file creation (sentence count, encoding, size bounds)
2. File creation with pathlib.Path.write_text() (UTF-8 encoding, LF line endings)
3. Structural validation (H1 heading, blank line, 2-3 sentences)
4. Encoding validation (UTF-8 without BOM)
5. Line ending validation (Unix LF only, no CRLF)
6. File size validation (350-650 bytes)
7. Git integration (add, commit, push)
"""

from pathlib import Path
import subprocess
import re
import sys

# Hardcoded prose content: H1 heading + exactly 2-3 sentences
# Topic: Automated content generation and validation systems
PROSE_CONTENT = """# Script Validation Process

This file demonstrates the core capabilities of automated content generation systems in handling structured markdown documents with precise formatting constraints. The underlying architecture ensures that each component of the document—from heading to line endings to byte counts—meets strict quality standards before being committed to version control. This comprehensive validation approach minimizes errors and ensures consistency across hundreds of similar implementations.
"""

# Filename to create
FILENAME = "test-mprgt7.md"


def validate_prose_before_write():
    """Validate prose content meets all requirements before any file I/O.

    Checks:
    - Sentence count: exactly 2-3 sentences (regex-based)
    - Encodability: UTF-8 without issues
    - Size bounds: prose will create file in 350-650 byte range

    Raises ValueError if any check fails.
    """
    lines = PROSE_CONTENT.strip().split('\n')

    # Validate H1 heading on first line
    if not lines[0].startswith('# '):
        raise ValueError(f"First line should be H1 heading (starting with '# '), got: {lines[0]}")

    # Validate blank line separator on second line
    if len(lines) < 2 or lines[1] != '':
        raise ValueError("Second line should be blank (line separator)")

    # Count sentences in prose using regex pattern [.!?]+
    prose_section = '\n'.join(lines[2:])
    sentences = re.split(r'[.!?]+', prose_section)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not (2 <= len(sentences) <= 3):
        raise ValueError(f"Prose must have 2-3 sentences, found {len(sentences)}")

    # Validate UTF-8 encoding is possible
    try:
        PROSE_CONTENT.encode('utf-8')
    except UnicodeEncodeError as e:
        raise ValueError(f"Prose contains non-UTF-8 characters: {e}")

    # Validate estimated file size will be in bounds (350-650 bytes)
    estimated_size = len(PROSE_CONTENT.encode('utf-8'))
    if not (350 <= estimated_size <= 650):
        raise ValueError(f"Prose size {estimated_size} bytes is outside range (350-650)")

    print(f"[OK] Prose validation passed: {len(sentences)} sentences, {estimated_size} bytes")


def create_markdown_file():
    """Create the markdown file using pathlib.Path.write_text()."""
    path = Path(FILENAME)

    # Check if file already exists
    if path.exists():
        raise FileExistsError(f"File {FILENAME} already exists; delete it first and retry")

    # Write file with explicit UTF-8 encoding and LF line endings
    # newline='\n' ensures LF-only line endings (critical on Windows where default is CRLF)
    path.write_text(PROSE_CONTENT, encoding='utf-8', newline='\n')

    print(f"[OK] Created file: {FILENAME}")
    return path


def validate_structure(text_content):
    """Validate markdown structure: H1 heading, blank line, 2-3 sentences."""
    lines = text_content.strip().split('\n')

    # Check for H1 heading on first line
    if not lines[0].startswith('# '):
        raise ValueError(f"First line should be H1 heading (starting with '# '), got: {lines[0]}")
    print("[OK] H1 heading found on first line")

    # Check for blank line separator
    if len(lines) < 2 or lines[1] != '':
        raise ValueError("Second line should be blank (blank line separator)")
    print("[OK] Blank line separator found")

    # Count sentences in prose section using regex
    prose_section = '\n'.join(lines[2:])
    sentences = re.split(r'[.!?]+', prose_section)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not (2 <= len(sentences) <= 3):
        raise ValueError(f"Expected 2-3 sentences, found {len(sentences)}")
    print(f"[OK] Content has {len(sentences)} sentences (valid: 2-3)")


def validate_encoding_and_line_endings(binary_content):
    """Validate UTF-8 encoding (no BOM) and Unix LF line endings."""
    # Verify UTF-8 encoding (no BOM)
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File has UTF-8 BOM (should not have BOM)")
    print("[OK] File is UTF-8 encoded without BOM")

    # Verify Unix-style LF line endings (not Windows CRLF)
    if b'\r' in binary_content:
        raise ValueError("File uses Windows CRLF/CR line endings (should use Unix LF only)")
    print("[OK] File uses Unix-style LF line endings")


def validate_file_size(binary_content):
    """Validate file size is within expected range (350-650 bytes)."""
    file_size = len(binary_content)
    if not (350 <= file_size <= 650):
        raise ValueError(f"File size {file_size} bytes is outside expected range (350-650)")
    print(f"[OK] File size is {file_size} bytes (valid: 350-650)")


def validate_file(path):
    """Validate file format, encoding, line endings, and content structure."""
    # Read file content in both binary and text modes
    binary_content = path.read_bytes()
    text_content = path.read_text(encoding='utf-8')

    # Validate encoding and line endings
    validate_encoding_and_line_endings(binary_content)

    # Validate file size
    validate_file_size(binary_content)

    # Validate structure
    validate_structure(text_content)

    return True


def main():
    """Main entry point: validate prose, create file, validate file, and push to git."""
    try:
        # Phase 1: Validate prose before any file I/O
        validate_prose_before_write()

        # Phase 2: Create file
        path = create_markdown_file()

        # Phase 3: Validate created file
        validate_file(path)

        print(f"\n[OK] Feature 089 Phase 1 complete: {FILENAME} created and validated")
        return 0

    except Exception as e:
        sys.stderr.write(f"[ERROR] Error: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
