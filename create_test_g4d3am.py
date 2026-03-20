#!/usr/bin/env python3
"""
Create and validate markdown file test-g4d3am.md following the established pattern.

This script demonstrates:
1. File creation with pathlib.Path.write_text() (UTF-8 encoding)
2. Structural validation (H1 heading, blank line, 2-3 sentences)
3. Encoding validation (UTF-8 without BOM)
4. Line ending validation (Unix LF only, no CRLF)
5. File size validation (400-600 bytes)
"""

from pathlib import Path
import sys

# Hardcoded prose content: H1 heading + exactly 2-3 sentences
# Topic: The Nature of Curiosity (unrestricted topic selection per product decision)
PROSE_CONTENT = """# The Nature of Curiosity

Curiosity is the driving force behind human discovery and progress, pushing us to ask questions and seek answers about the world around us. This innate desire to understand propels innovation in science, technology, and culture, as individuals relentlessly pursue knowledge in their chosen fields. The most successful people throughout history share a common trait: an unwavering commitment to exploring ideas, experimenting boldly, and learning from both their triumphs and failures.
"""

# Filename to create
FILENAME = "test-g4d3am.md"


def create_markdown_file():
    """Create the markdown file using pathlib.Path.write_text()."""
    path = Path(FILENAME)

    # Write file with explicit UTF-8 encoding
    # write_text() handles file creation, closing, and encoding automatically
    path.write_text(PROSE_CONTENT, encoding='utf-8')

    print(f"✓ Created file: {FILENAME}")
    return path


def validate_structure(text_content):
    """Validate markdown structure: H1 heading, blank line, 2-3 sentences."""
    lines = text_content.strip().split('\n')

    # Check for H1 heading on first line
    if not lines[0].startswith('# '):
        raise ValueError(f"First line should be H1 heading (starting with '# '), got: {lines[0]}")
    print("✓ H1 heading found on first line")

    # Check for blank line separator
    if len(lines) < 2 or lines[1] != '':
        raise ValueError("Second line should be blank (blank line separator)")
    print("✓ Blank line separator found")

    # Count sentences in prose section (count periods)
    prose_section = '\n'.join(lines[2:])
    sentence_count = prose_section.count('.')
    if not (2 <= sentence_count <= 3):
        raise ValueError(f"Expected 2-3 sentences, found {sentence_count}")
    print(f"✓ Content has {sentence_count} sentences (valid: 2-3)")


def validate_encoding_and_line_endings(binary_content):
    """Validate UTF-8 encoding (no BOM) and Unix LF line endings."""
    # Verify UTF-8 encoding (no BOM)
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File has UTF-8 BOM (should not have BOM)")
    print("✓ File is UTF-8 encoded without BOM")

    # Verify Unix-style LF line endings (not Windows CRLF)
    if b'\r\n' in binary_content:
        raise ValueError("File uses Windows CRLF line endings (should use Unix LF)")
    print("✓ File uses Unix-style LF line endings")


def validate_file_size(binary_content):
    """Validate file size is within expected range (400-600 bytes)."""
    file_size = len(binary_content)
    if not (400 <= file_size <= 600):
        raise ValueError(f"File size {file_size} bytes is outside expected range (400-600)")
    print(f"✓ File size is {file_size} bytes (valid: 400-600)")


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
    """Main entry point: create file and validate."""
    try:
        # Task 1: Create file
        path = create_markdown_file()

        # Tasks 2-4: Validate file
        validate_file(path)

        print(f"\n✓ Feature 125 Phase 1 complete: {FILENAME} created and validated")
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
