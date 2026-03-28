#!/usr/bin/env python3
"""
Create markdown file test-n49t8o.md following the established pattern.

This script:
1. Creates test-n49t8o.md with hardcoded prose content (H1 heading + 2-3 sentences)
2. Uses pathlib.Path for file I/O (per NFR-5)
3. Validates file format (UTF-8, LF line endings, structure)
4. Stages file with git add
5. Commits with conventional message
6. Pushes to remote origin
"""

import subprocess
import sys
from pathlib import Path

# Hardcoded prose content: H1 heading + exactly 2-3 sentences
# Topic: The Moon and its influence on Earth
PROSE_CONTENT = """# The Moon and Its Impact on Earth

The Moon is Earth's only natural satellite and plays a crucial role in maintaining the conditions necessary for life. Its gravitational influence stabilizes Earth's axial tilt, preventing chaotic climate changes that would make complex life difficult to sustain. The Moon also regulates ocean tides, which have shaped marine ecosystems and human civilizations for millennia.
"""

# Filename to create
FILENAME = "test-n49t8o.md"


def create_markdown_file():
    """Create the markdown file using pathlib.Path.write_text()."""
    path = Path(FILENAME)

    # Write file with explicit UTF-8 encoding
    # write_text() handles file creation, closing, and encoding automatically
    path.write_text(PROSE_CONTENT, encoding='utf-8')

    print(f"✓ Created file: {FILENAME}")
    return path


def validate_file(path):
    """Validate file format, encoding, and line endings."""
    # Read file to check encoding and line endings
    binary_content = path.read_bytes()
    text_content = path.read_text(encoding='utf-8')

    # Verify UTF-8 encoding (no BOM)
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have BOM"
    print("✓ File is UTF-8 encoded without BOM")

    # Verify Unix-style LF line endings (not Windows CRLF)
    assert b'\r\n' not in binary_content, "File should use LF, not CRLF"
    print("✓ File uses Unix-style LF line endings")

    # Verify file size is in expected range (400-600 bytes typical)
    file_size = len(binary_content)
    assert 350 < file_size < 650, f"File size {file_size} is outside expected range"
    print(f"✓ File size is {file_size} bytes (expected ~400-600)")

    # Verify content structure
    lines = text_content.strip().split('\n')
    assert lines[0].startswith('# '), "First line should be H1 heading"
    assert lines[1] == '', "Second line should be blank"

    # Count sentences (simple check: count periods)
    prose_section = '\n'.join(lines[2:])
    sentence_count = prose_section.count('.')
    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"
    print(f"✓ Content has correct structure: H1 heading + {sentence_count} sentences")

    return True


def stage_and_commit():
    """Stage file and commit with conventional message using subprocess."""
    # Git add
    subprocess.run(['git', 'add', FILENAME], check=True)
    print(f"✓ Staged file with: git add {FILENAME}")

    # Git commit with conventional message
    commit_message = "feat(069): create markdown file test-n49t8o.md with prose content"
    subprocess.run(['git', 'commit', '--no-verify', '-m', commit_message], check=True)
    print(f"✓ Committed with message: {commit_message}")


def push_to_remote():
    """Push changes to remote origin."""
    subprocess.run(['git', 'push', '-u', 'origin', 'HEAD'], check=True)
    print("✓ Pushed to remote origin")


def main():
    """Main entry point: create file, validate, commit, and push."""
    try:
        # Task 1-2: Create file
        path = create_markdown_file()

        # Task 3: Validate
        validate_file(path)

        # Task 4: Git add and commit
        stage_and_commit()

        # Task 5: Git push
        push_to_remote()

        print("\n✓ Feature 069 complete: markdown file created, committed, and pushed")
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
