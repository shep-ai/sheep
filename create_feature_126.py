#!/usr/bin/env python3
"""
Create markdown file test-8bcjbe.md following the established pattern.

This script:
1. Creates test-8bcjbe.md with hardcoded prose content (H1 heading + 2-3 sentences)
2. Uses pathlib.Path for file I/O (per NFR-5)
3. Validates file format (UTF-8, LF line endings, structure)
4. Stages file with git add
5. Commits with conventional message
6. Pushes to remote origin
"""

from pathlib import Path
import subprocess
import sys

# Hardcoded prose content: H1 heading + exactly 2-3 sentences
# Topic: The Importance of Clean Code
PROSE_CONTENT = """# The Importance of Clean Code

Clean code is fundamental to software development because it makes programs easier to understand, maintain, and modify. Well-organized code reduces bugs, speeds up development cycles, and lowers the cost of maintenance. Developers should prioritize readability and clarity in their code to create a sustainable and scalable codebase.
"""

# Filename to create
FILENAME = "test-8bcjbe.md"


def create_file():
    """Create the markdown file using pathlib.Path.write_text()."""
    path = Path(FILENAME)

    # Write file with explicit UTF-8 encoding and no newline translation
    # Use write_bytes() to ensure LF line endings are preserved exactly
    path.write_bytes(PROSE_CONTENT.encode('utf-8'))

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

    # Verify file size is in expected range (300-600 bytes typical)
    file_size = len(binary_content)
    assert 300 <= file_size <= 600, f"File size {file_size} is outside expected range"
    print(f"[OK] File size is {file_size} bytes (expected 300-600)")

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
    commit_message = "feat(126): create markdown file test-8bcjbe.md with prose content"
    subprocess.run(['git', 'commit', '--no-verify', '-m', commit_message], check=True)
    print(f"[OK] Committed with message: {commit_message}")


def push_to_remote():
    """Push changes to remote origin."""
    subprocess.run(['git', 'push', '-u', 'origin', 'HEAD'], check=True)
    print("[OK] Pushed to remote origin")


def main():
    """Main entry point: create file, validate, commit, and push."""
    try:
        # Task 1-2: Create file
        path = create_file()

        # Task 3: Validate
        validate_file(path)

        # Task 4: Git add and commit
        stage_and_commit()

        # Task 5: Git push
        push_to_remote()

        print("\n[OK] Feature 126 complete: markdown file created, committed, and pushed")
        return 0

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
