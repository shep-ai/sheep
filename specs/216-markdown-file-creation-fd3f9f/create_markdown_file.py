"""
Implementation script for feature 216: markdown file creation.

This module provides functions to:
1. Create a markdown file (test-wyvzr1.md) with proper structure and content
2. Validate the file properties (encoding, line endings, size, structure)
3. Execute git operations (add, commit, push) using subprocess

The implementation uses Python standard library only (pathlib, subprocess)
with no external dependencies.
"""

import re
import subprocess
from pathlib import Path

# ============================================================================
# Constants
# ============================================================================

FILENAME = "test-wyvzr1.md"
MIN_SIZE = 300
MAX_SIZE = 600
HEADING_PATTERN = r'^# .+$'  # Regex for H1 heading validation

# Prose about personal development (3 sentences, ~350 bytes total)
PROSE_CONTENT = (
    "Personal development is a lifelong journey of self-discovery and continuous improvement that enables individuals to unlock their full potential. "
    "By investing in learning, reflection, and meaningful growth experiences, we cultivate the resilience, wisdom, and skills necessary to navigate an increasingly complex world. "
    "Embracing personal development transforms not only who we are, but also amplifies our capacity to make a positive impact on those around us."
)


# ============================================================================
# File Creation Function
# ============================================================================

def create_file():
    """
    Create test-wyvzr1.md in the current directory with markdown structure.

    The file contains:
    - H1 heading (# Title)
    - Blank line
    - 3-sentence prose paragraph about personal development
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path: Path object pointing to the created file

    Raises:
        FileExistsError: If test-wyvzr1.md already exists in current directory
    """
    filepath = Path(FILENAME)

    # Prevent overwriting existing files
    if filepath.exists():
        raise FileExistsError(f"File '{FILENAME}' already exists. Remove it to proceed.")

    # Build markdown content with proper structure
    markdown_content = (
        "# Personal Development and Growth\n"
        "\n"
        f"{PROSE_CONTENT}\n"
    )

    # Write file with UTF-8 encoding (no BOM) and Unix line endings
    filepath.write_text(markdown_content, encoding="utf-8", newline="\n")

    return filepath


# ============================================================================
# File Validation Function
# ============================================================================

def validate_file(filepath):
    """
    Validate that a markdown file meets all specification requirements.

    Checks (in order):
    - File exists
    - UTF-8 encoding without BOM
    - Unix LF line endings (no Windows CRLF)
    - Contains exactly one H1 heading (first line starts with "# ")
    - Contains blank line after heading
    - Contains substantive prose content (not just whitespace)
    - File size is within 300-600 byte range
    - File ends with newline
    - Contains at least 2 sentences (periods)

    Args:
        filepath (Path or str): Path to the markdown file to validate

    Returns:
        bool: True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive error message
    """
    filepath = Path(filepath)

    # 1. Check file exists
    assert filepath.exists(), f"File {filepath.name} does not exist"

    # 2. Read file content
    binary_content = filepath.read_bytes()
    file_size = len(binary_content)

    # 3. Check encoding (UTF-8 without BOM)
    assert not binary_content.startswith(b'\xef\xbb\xbf'), (
        "File has UTF-8 BOM (Byte Order Mark). Should use UTF-8 without BOM."
    )

    try:
        content = binary_content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}") from e

    # 4. Check line endings (LF only, no CRLF)
    assert '\r\n' not in content, (
        "File contains Windows CRLF line endings. Should use Unix LF (\\n) only."
    )
    assert '\n' in content, (
        "File does not contain any line endings. Should use Unix LF (\\n)."
    )

    # 5. Check trailing newline
    assert binary_content.endswith(b'\n'), (
        "File should end with a newline character."
    )

    # 6. Check structure: H1 heading + blank line + prose
    lines = content.split('\n')

    # Check H1 heading on first line using regex
    assert re.match(HEADING_PATTERN, lines[0]), (
        f"Missing H1 heading: first line must match regex '{HEADING_PATTERN}' but found: {lines[0][:50]}"
    )

    # Check blank line after heading
    assert len(lines) > 1, "File should contain more than just a heading"
    assert lines[1] == '', (
        f"Missing blank line after heading: second line should be empty but found: {repr(lines[1][:50])}"
    )

    # Check prose content (not just whitespace)
    prose = '\n'.join(lines[2:]).strip()
    assert prose, "File should contain prose content after blank line"

    # 7. Check file size
    assert MIN_SIZE < file_size < MAX_SIZE, (
        f"File size {file_size} bytes outside typical range ({MIN_SIZE}-{MAX_SIZE}). "
        f"Specification requires 300-600 byte range."
    )

    # 8. Check sentence count (2-3 sentences by splitting on periods)
    sentence_list = [s.strip() for s in prose.split('.') if s.strip()]
    sentence_count = len(sentence_list)
    assert 2 <= sentence_count <= 3, (
        f"Prose content should contain 2-3 sentences, but found {sentence_count}."
    )

    return True


# ============================================================================
# Git Operations Constants
# ============================================================================

COMMIT_MESSAGE = "feat(216): Create markdown file test-wyvzr1.md with prose content"


# ============================================================================
# Git Operations Function
# ============================================================================

def git_operations():
    """
    Execute git operations to stage, commit, and push the markdown file.

    Operations:
    1. git add test-wyvzr1.md
    2. git commit -m "feat(216): Create markdown file test-wyvzr1.md with prose content"
    3. git push -u origin HEAD

    Raises:
        subprocess.CalledProcessError: If any git command fails with descriptive error message
    """
    try:
        # Stage the file for commit
        subprocess.run(
            ["git", "add", FILENAME],
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            output=f"git add failed: {e.stderr or 'Unable to stage file'}"
        ) from e

    try:
        # Commit with conventional commit message
        subprocess.run(
            ["git", "commit", "-m", COMMIT_MESSAGE],
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            output=f"git commit failed: {e.stderr or 'Unable to create commit'}"
        ) from e

    try:
        # Push to feature branch
        subprocess.run(
            ["git", "push", "-u", "origin", "HEAD"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            output=f"git push failed: {e.stderr or 'Unable to push to remote'}"
        ) from e


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    # Create the markdown file
    filepath = create_file()
    print(f"Created file: {filepath}")

    # Validate the created file
    try:
        validate_file(filepath)
        print(f"Validation passed: {filepath.name}")
    except AssertionError as e:
        print(f"Validation failed: {e}")
        raise

    # Execute git operations
    try:
        git_operations()
        print("Git operations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Git operations failed: {e}")
        raise

    print("Feature 216 implementation complete!")
