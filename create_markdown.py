#!/usr/bin/env python3
"""
Feature 213: Create markdown file test-lyi2gl.md following the established pattern.

This script implements Phase 1 (File Creation & Validation):
1. Creates test-lyi2gl.md with hard-coded prose content (H1 heading + 2-3 sentences)
2. Uses pathlib.Path for file I/O (automatic UTF-8, LF handling)
3. Validates file format (UTF-8, LF line endings, structure, size 300-800 bytes)
4. Fail-fast error handling with clear validation before git operations
"""

from pathlib import Path
import sys

# Hard-coded, deterministic prose content: H1 heading + exactly 2-3 sentences
# Topic: Digital Communication and Connection
PROSE_CONTENT = """# The Evolution of Digital Communication

Digital communication has transformed how humans connect across vast distances, enabling instantaneous exchange of ideas and information that would have been impossible just decades ago. The evolution from email to messaging platforms to social media reflects our fundamental desire to share experiences and maintain relationships despite geographical barriers. These technologies continue to shape society, creating both unprecedented opportunities for connection and novel challenges for maintaining meaningful engagement.
"""

# Target filename for feature 213
FILENAME = "test-lyi2gl.md"


def create_markdown_file():
    """
    Create the markdown file using pathlib.Path.write_text().

    Uses default encoding (UTF-8) and line ending handling (LF) from pathlib.
    Per the research and NFR-4: "Rely on pathlib.Path.write_text() defaults
    (UTF-8, no BOM, LF line endings)".
    """
    path = Path(FILENAME)

    # write_text() with newline='' ensures LF line endings on all platforms (Windows, Linux, macOS)
    # Per NFR-2: "File line endings must be LF (line feed, \n) throughout"
    path.write_text(PROSE_CONTENT, newline='')

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

    # Verify file size is in expected range (300-800 bytes per spec)
    file_size = len(binary_content)
    assert 300 <= file_size <= 800, f"File size {file_size} is outside 300-800 byte range"
    print(f"[OK] File size is {file_size} bytes (300-800 byte range)")

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
    """
    Phase 1: File Creation & Validation.

    Implements:
    - Task 1: Create markdown file with hard-coded content
    - Task 2: Validate file encoding, line endings, and properties

    Phase 2 (git integration) will follow after validation succeeds.
    """
    try:
        # Task 1: Create file using pathlib.write_text()
        path = create_markdown_file()

        # Task 2: Validate file properties before git operations
        validate_file(path)

        print("\n[OK] Phase 1 complete: markdown file created and validated")
        print("  Ready for Phase 2: Git integration (add/commit/push)")
        return 0

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
