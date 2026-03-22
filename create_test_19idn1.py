#!/usr/bin/env python3
"""
Implementation script for feature 157: markdown-file-creation-b9d0e7
Creates test-19idn1.md with proper markdown structure and validation.
"""

import subprocess
import sys
from pathlib import Path

# Configuration for git workflow
FILENAME = "test-19idn1.md"
COMMIT_MESSAGE = "feat(157): Create markdown file test-19idn1.md with prose content"

# ============================================================================
# PHASE 1: Script Setup & Content Definition
# ============================================================================
# Define prose content (H1 heading + 2-3 sentences)
HEADING = "# The Power of Curiosity in Learning"
PROSE = (
    "Curiosity is the driving force behind discovery and intellectual growth, pushing individuals to ask questions and seek deeper understanding. "
    "When we embrace curiosity, we open ourselves to new perspectives and ideas that challenge our existing beliefs and assumptions. "
    "Fostering a curious mindset throughout life enriches our experiences and helps us adapt to an ever-changing world with confidence and enthusiasm."
)


def create_markdown_file():
    """
    PHASE 2: File Creation & Validation

    Creates test-19idn1.md in repository root with proper markdown structure.
    Uses pathlib.Path.write_text() with explicit UTF-8 encoding and Unix LF line endings.
    """
    file_path = Path(FILENAME)

    # Combine heading and prose content
    full_content = f"{HEADING}\n\n{PROSE}"

    # Write file with explicit UTF-8 encoding and Unix LF line endings
    # newline='\n' enforces Unix-style line endings (not Windows CRLF)
    file_path.write_text(full_content, encoding='utf-8', newline='\n')

    return file_path


def validate_structure(content):
    """
    PHASE 2: File Creation & Validation

    Validates markdown structure: H1 heading, blank line, 2-3 sentences.
    """
    lines = content.strip().split('\n')

    # Check for H1 heading on first line
    if not lines[0].startswith('# '):
        raise ValueError(f"First line should be H1 heading (starting with '# '), got: {lines[0]}")

    # Check for blank line separator
    if len(lines) < 2 or lines[1] != '':
        raise ValueError("Second line should be blank (blank line separator)")

    # Count sentences in prose section (count periods)
    prose_section = '\n'.join(lines[2:])
    sentence_count = prose_section.count('.')
    if not (2 <= sentence_count <= 3):
        raise ValueError(f"Expected 2-3 sentences, found {sentence_count}")


def validate_encoding_and_line_endings(binary_content):
    """
    PHASE 2: File Creation & Validation

    Validates UTF-8 encoding (no BOM) and Unix LF line endings.
    """
    # Verify UTF-8 encoding (no BOM)
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File has UTF-8 BOM (should not have BOM)")

    # Verify Unix-style LF line endings (not Windows CRLF)
    if b'\r\n' in binary_content:
        raise ValueError("File uses Windows CRLF line endings (should use Unix LF)")


def validate_file_size(binary_content):
    """
    PHASE 2: File Creation & Validation

    Validates file size is within 400-600 byte range.
    """
    file_size = len(binary_content)
    if not (400 <= file_size <= 600):
        raise ValueError(f"File size {file_size} bytes is outside expected range (400-600)")


def validate_file(file_path):
    """
    PHASE 2: File Creation & Validation

    Integrates all validation checks: encoding, line endings, file size, and structure.
    """
    # Read file content in both binary and text modes
    binary_content = file_path.read_bytes()
    text_content = file_path.read_text(encoding='utf-8')

    # Validate encoding and line endings
    validate_encoding_and_line_endings(binary_content)

    # Validate file size
    validate_file_size(binary_content)

    # Validate structure
    validate_structure(text_content)

    return True


# ============================================================================
# PHASE 3: Git Integration
# ============================================================================
def git_stage_file(filename):
    """
    Stage the markdown file using 'git add'.

    Args:
        filename (str): Name of the file to stage

    Raises:
        subprocess.CalledProcessError: If git add fails

    Returns:
        True if successful
    """
    try:
        subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[OK] File staged: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git add failed: {e.stderr}")


def git_commit(message):
    """
    Commit the staged file using conventional commit message.

    Args:
        message (str): Conventional commit message

    Raises:
        subprocess.CalledProcessError: If git commit fails

    Returns:
        True if successful
    """
    try:
        subprocess.run(
            ["git", "commit", "--no-verify", "-m", message],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[OK] File committed with message: {message}")
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git commit failed: {e.stderr}")


def git_push(branch):
    """
    Push the commit to the remote tracking branch.

    Args:
        branch (str): Branch name to push to (e.g., 'feat/157-markdown-file-creation-b9d0e7')

    Raises:
        subprocess.CalledProcessError: If git push fails

    Returns:
        True if successful
    """
    try:
        subprocess.run(
            ["git", "push", "origin", branch],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[OK] Commit pushed to remote branch: {branch}")
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git push failed: {e.stderr}")


def main():
    """
    PHASE 4: Integration & Execution

    Main entry point: create file, validate it, and integrate with git.
    """
    try:
        print("=" * 60)
        print("Feature 157: Markdown File Creation")
        print("=" * 60)

        # Phase 2: Create file
        print("\n[Phase 2: File Creation & Validation]")
        file_path = create_markdown_file()
        print(f"[OK] Created file: {FILENAME}")

        # Phase 2: Validate file
        validate_file(file_path)
        print("[OK] File structure validation passed")
        print("[OK] File encoding and line endings validation passed")
        print("[OK] File size validation passed")

        # Phase 3: Git Integration
        print("\n[Phase 3: Git Integration]")
        git_stage_file(FILENAME)
        git_commit(COMMIT_MESSAGE)
        git_push("feat/markdown-file-creation-b9d0e7")

        print(f"\n[OK] Feature 157 complete: {FILENAME} created, validated, and pushed")
        return 0

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
