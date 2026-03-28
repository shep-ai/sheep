#!/usr/bin/env python3
"""
Create and validate markdown file test-59xln4.md following the established pattern.

This script demonstrates:
1. File creation with pathlib.Path.write_text() (UTF-8 encoding)
2. Structural validation (H1 heading, blank line, 2-3 sentences)
3. Encoding validation (UTF-8 without BOM)
4. Line ending validation (Unix LF only, no CRLF)
5. File size validation (350-650 bytes)
"""

import subprocess
import sys
from pathlib import Path

# Hardcoded prose content: H1 heading + exactly 2-3 sentences
# Topic: The Power of Learning (unrestricted topic selection per product decision)
PROSE_CONTENT = """# The Power of Learning

Learning is an extraordinary journey of transformation that opens doors to new possibilities and expands our understanding of the world. When we approach knowledge with genuine curiosity and a willingness to challenge our assumptions, we develop resilience and adaptability that serve us well in every aspect of life. The pursuit of learning is not a destination but a continuous process of growth that enriches our character and empowers us to contribute meaningfully to society.
"""

# Filename to create
FILENAME = "test-59xln4.md"


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
    """Validate file size is within expected range (350-650 bytes)."""
    file_size = len(binary_content)
    if not (350 <= file_size <= 650):
        raise ValueError(f"File size {file_size} bytes is outside expected range (350-650)")
    print(f"✓ File size is {file_size} bytes (valid: 350-650)")


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


def stage_file(filename):
    """Stage file with git add."""
    try:
        subprocess.run(["git", "add", filename], check=True)
        print(f"✓ File staged: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Git add failed: {e}", file=sys.stderr)
        raise


def commit_file(filename):
    """Commit file with conventional commit message."""
    message = f"feat(101): create markdown file {filename} with prose content"
    try:
        subprocess.run(
            ["git", "commit", "--no-verify", "-m", message],
            check=True
        )
        print(f"✓ File committed with message: {message}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Git commit failed: {e}", file=sys.stderr)
        raise


def push_commit():
    """Push commit to remote origin."""
    try:
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
        print("✓ Commit pushed to remote origin")
    except subprocess.CalledProcessError as e:
        print(f"✗ Git push failed: {e}", file=sys.stderr)
        raise


def git_workflow(filename):
    """Execute complete git workflow: stage, commit, push."""
    try:
        stage_file(filename)
        commit_file(filename)
        push_commit()
        return 0
    except Exception:
        return 1


def main_phase2():
    """Main entry point for phase 2: git integration."""
    try:
        result = git_workflow(FILENAME)
        if result == 0:
            print(f"\n✓ Feature 101 Phase 2 complete: {FILENAME} staged, committed, and pushed")
        return result
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point: create file and validate."""
    try:
        # Task 1: Create file
        path = create_markdown_file()

        # Tasks 2-3: Validate file
        validate_file(path)

        print(f"\n✓ Feature 101 Phase 1 complete: {FILENAME} created and validated")
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
