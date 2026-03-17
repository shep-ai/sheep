#!/usr/bin/env python3
"""
Create markdown file test-gwplv4.md following the established pattern.

This script:
1. Creates test-gwplv4.md with hardcoded prose content (H1 heading + 2-3 sentences)
2. Uses pathlib.Path for file I/O (per NFR-5)
3. Validates file format (UTF-8, LF line endings, structure)
4. Phase 1 only: File creation and validation (git operations in phase 2)
"""

from pathlib import Path
import sys

# Hardcoded prose content: H1 heading + exactly 2-3 sentences
# Topic: The Magic of Storytelling
PROSE_CONTENT = """# The Magic of Storytelling

Stories are the fundamental way humans share knowledge, experience, and wisdom across generations throughout history. They transform abstract ideas into vivid experiences that engage our emotions and help us remember lessons far better than facts alone. Through the art of storytelling, we connect with others deeply and make sense of the world around us.
"""

# Filename to create
FILENAME = "test-gwplv4.md"


def create_markdown_file():
    """Create the markdown file using pathlib.Path.write_text()."""
    path = Path(FILENAME)

    # Write file with explicit UTF-8 encoding and newline='' to preserve LF
    # newline='' ensures that \n is written as-is, not converted to \r\n on Windows
    path.write_text(PROSE_CONTENT, encoding='utf-8', newline='')

    print(f"[OK] Created file: {FILENAME}")
    return path


def validate_file(path):
    """Validate file format, encoding, and line endings."""
    # Read file to check encoding and line endings
    binary_content = path.read_bytes()
    text_content = path.read_text(encoding='utf-8')

    # Verify UTF-8 encoding (no BOM)
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have BOM"
    print("[OK] File is UTF-8 encoded without BOM")

    # Verify Unix-style LF line endings (not Windows CRLF)
    assert b'\r\n' not in binary_content, "File should use LF, not CRLF"
    print("[OK] File uses Unix-style LF line endings")

    # Verify file size is in expected range (400-600 bytes typical)
    file_size = len(binary_content)
    assert 350 < file_size < 650, f"File size {file_size} is outside expected range"
    print(f"[OK] File size is {file_size} bytes (expected ~400-600)")

    # Verify content structure
    lines = text_content.strip().split('\n')
    assert lines[0].startswith('# '), "First line should be H1 heading"
    assert lines[1] == '', "Second line should be blank"

    # Count sentences (simple check: count periods)
    prose_section = '\n'.join(lines[2:])
    sentence_count = prose_section.count('.')
    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"
    print(f"[OK] Content has correct structure: H1 heading + {sentence_count} sentences")

    return True


def main():
    """Main entry point: create file and validate (phase 1 only)."""
    try:
        # Task 1: Create file
        path = create_markdown_file()

        # Task 2: Validate
        validate_file(path)

        print("\n[OK] Phase 1 complete: markdown file created and validated")
        return 0

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
