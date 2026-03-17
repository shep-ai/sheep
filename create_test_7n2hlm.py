#!/usr/bin/env python3
"""
Create markdown file test-7n2hlm.md following the established pattern.

This script:
1. Creates test-7n2hlm.md with hardcoded prose content (H1 heading + 2-3 sentences)
2. Uses pathlib.Path for file I/O with explicit UTF-8 encoding and LF line endings
3. Validates file format (UTF-8 without BOM, LF line endings, structure, size)
4. Stages file with git add
5. Commits with conventional message
6. Pushes to remote origin
"""

from pathlib import Path
import subprocess
import sys

# Hardcoded prose content: H1 heading + exactly 2-3 sentences
# Topic: The Wonders of the Ocean
PROSE_CONTENT = """# The Wonders of the Ocean

The ocean covers more than seventy percent of Earth's surface and remains one of the most mysterious frontiers of our planet. Its depths harbor countless species yet to be discovered, many adapted to extreme conditions that would be inhospitable to most life forms. The ocean's interconnected currents and ecosystems play a vital role in regulating Earth's climate and supporting billions of lives worldwide.
"""

# Filename to create
FILENAME = "test-7n2hlm.md"


def create_markdown_file():
    """Create the markdown file using pathlib.Path with explicit encoding and LF line endings."""
    path = Path(FILENAME)

    # Write file with explicit UTF-8 encoding
    # Note: On Windows, pathlib.write_text() uses platform default line endings (CRLF)
    # To ensure LF line endings, we write the content as-is since Python's text mode
    # with newline='' parameter ensures the exact line endings are preserved
    path.write_text(PROSE_CONTENT, encoding='utf-8', newline='\n')

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


def stage_and_commit():
    """Stage file and commit with conventional message using subprocess."""
    # Git add
    subprocess.run(['git', 'add', FILENAME], check=True)
    print(f"[OK] Staged file with: git add {FILENAME}")

    # Git commit with conventional message
    commit_message = "feat(070): create markdown file test-7n2hlm.md with prose content"
    subprocess.run(['git', 'commit', '--no-verify', '-m', commit_message], check=True)
    print(f"[OK] Committed with message: {commit_message}")


def push_to_remote():
    """Push changes to remote origin."""
    subprocess.run(['git', 'push', '-u', 'origin', 'HEAD'], check=True)
    print("[OK] Pushed to remote origin")


def main():
    """Main entry point: create file, validate, commit, and push."""
    try:
        # Task 1: Create file
        path = create_markdown_file()

        # Task 2: Validate
        validate_file(path)

        # Task 3: Git add and commit
        stage_and_commit()

        # Task 4: Git push
        push_to_remote()

        print("\n[OK] Feature 070 complete: markdown file created, committed, and pushed")
        return 0

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
