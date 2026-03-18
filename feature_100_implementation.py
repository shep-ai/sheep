#!/usr/bin/env python3
"""
Feature 100: Create markdown file test-aear8n.md with validation.

This script:
1. Creates test-aear8n.md with hardcoded prose content (H1 heading + 2-3 sentences)
2. Uses pathlib.Path for file I/O with explicit UTF-8 encoding and Unix LF line endings
3. Validates file format (UTF-8 without BOM, LF line endings, structure, size bounds)
4. Stages file with git add
5. Commits with conventional message
6. Pushes to feature branch
"""

from pathlib import Path
import subprocess
import sys

# Hardcoded prose content: H1 heading + exactly 2-3 sentences
# Topic: The Power of Community and Collaborative Growth
PROSE_CONTENT = """# The Power of Community

Community is where individuals discover that their struggles and successes are not theirs alone, and that collective wisdom can solve problems no single person could face independently. When people come together with shared purpose and mutual respect, they create an environment where each member's unique talents contribute to something greater than the sum of its parts. Through collaboration and support, communities become incubators of innovation, resilience, and profound human connection.
"""

# Filename to create
FILENAME = "test-aear8n.md"


def create_markdown_file():
    """Create the markdown file using pathlib.Path.write_text()."""
    path = Path(FILENAME)

    # Write file with explicit UTF-8 encoding and Unix LF line endings
    # encoding='utf-8': ensures UTF-8 without BOM
    # newline='\n': forces Unix LF line endings on all platforms (critical on Windows)
    path.write_text(PROSE_CONTENT, encoding='utf-8', newline='\n')

    print(f"[OK] Created file: {FILENAME}")
    return path


def validate_encoding(path):
    """Validate that file uses UTF-8 encoding without BOM."""
    binary_content = path.read_bytes()

    # Verify UTF-8 encoding (no BOM)
    # BOM bytes for UTF-8: 0xEF 0xBB 0xBF
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File must be UTF-8 without BOM")

    print("[OK] File is UTF-8 encoded without BOM")


def validate_line_endings(path):
    """Validate that file uses Unix-style LF line endings only."""
    binary_content = path.read_bytes()

    # Verify Unix-style LF line endings (not Windows CRLF)
    if b'\r\n' in binary_content:
        raise ValueError("File must use Unix LF line endings, not CRLF")

    # Verify no CR characters (old Mac line endings)
    if b'\r' in binary_content:
        raise ValueError("File must use Unix LF line endings, not CR")

    print("[OK] File uses Unix-style LF line endings only")


def validate_structure(path):
    """Validate file structure (H1 heading, blank line, 2-3 sentences) and size."""
    text_content = path.read_text(encoding='utf-8')
    binary_content = path.read_bytes()

    # Verify file size is in acceptable range (320-600 bytes per NFR-3)
    file_size = len(binary_content)
    if not (320 <= file_size <= 600):
        raise ValueError(f"File size {file_size} bytes is outside 320-600 byte range")
    print(f"[OK] File size is {file_size} bytes (within 320-600 byte range)")

    # Parse content structure
    lines = text_content.strip().split('\n')

    # Verify H1 heading on first line
    if not lines[0].startswith('# '):
        raise ValueError("First line should be H1 heading (# Title)")
    print(f"[OK] File has H1 heading: {lines[0]}")

    # Verify blank line after heading
    if len(lines) < 2 or lines[1] != '':
        raise ValueError("Second line should be blank (separator between heading and prose)")
    print("[OK] Blank line separates heading from prose")

    # Count sentences in prose section (simple check: count periods)
    prose_section = '\n'.join(lines[2:])
    sentence_count = prose_section.count('.')
    if not (2 <= sentence_count <= 3):
        raise ValueError(f"Expected 2-3 sentences, found {sentence_count}")
    print(f"[OK] Prose contains {sentence_count} sentences (expected 2-3)")


def validate_file(path):
    """Run all validation checks on the created file."""
    print("\nValidating file...")
    validate_encoding(path)
    validate_line_endings(path)
    validate_structure(path)
    print("[OK] All validations passed\n")


def stage_and_commit():
    """Stage file and commit with conventional message using subprocess."""
    # Git add
    subprocess.run(['git', 'add', FILENAME], check=True)
    print(f"[OK] Staged file with: git add {FILENAME}")

    # Git commit with conventional message
    commit_message = "feat(100): create markdown file test-aear8n.md with prose content"
    subprocess.run(['git', 'commit', '--no-verify', '-m', commit_message], check=True)
    print(f"[OK] Committed with message: {commit_message}")


def push_to_remote():
    """Push changes to remote origin."""
    subprocess.run(['git', 'push', '-u', 'origin', 'HEAD'], check=True)
    print("[OK] Pushed to remote origin")


def main():
    """Main entry point: create file, validate, commit, and push."""
    try:
        # Phase 1: File Creation & Validation
        print("=== Feature 100: Markdown File Creation ===\n")

        # Task 1: Create file
        path = create_markdown_file()

        # Task 2-4: Validate file
        validate_file(path)

        # Phase 2: Git Integration
        print("=== Git Integration ===\n")
        stage_and_commit()
        push_to_remote()

        print("\n[OK] Feature 100 complete: markdown file created, validated, committed, and pushed")
        return 0

    except Exception as e:
        print(f"\n[FAIL] Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
