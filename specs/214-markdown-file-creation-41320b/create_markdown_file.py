"""
Implementation script for feature 214: markdown file creation.

This module provides functions to:
1. Create a markdown file (test-k8kqxb.md) with proper structure and content
2. Validate the file properties (encoding, line endings, size, structure)
3. Execute git operations (add, commit, push)

The implementation uses Python standard library only (pathlib, subprocess, os)
with no external dependencies.
"""

import subprocess
from pathlib import Path

# ============================================================================
# Constants
# ============================================================================

FILENAME = "test-k8kqxb.md"
MIN_SIZE = 300
MAX_SIZE = 600

# Prose about learning and creativity (3 sentences, ~340 bytes total)
PROSE_CONTENT = (
    "Learning is the foundation of human growth and development, allowing us to acquire new knowledge, skills, and perspectives that transform our understanding of the world. "
    "Through continuous learning and creative exploration, we unlock our potential to innovate, solve complex problems, and contribute meaningfully to society. "
    "The combination of curiosity-driven learning and creative thinking enables us to adapt to change and shape a better future."
)


# ============================================================================
# File Creation Function
# ============================================================================

def create_file():
    """
    Create test-k8kqxb.md in the current directory with markdown structure.

    The file contains:
    - H1 heading (# Title)
    - Blank line
    - 3-sentence prose paragraph about learning and creativity
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path: Path object pointing to the created file

    Raises:
        FileExistsError: If test-k8kqxb.md already exists in current directory
    """
    filepath = Path(FILENAME)

    # Prevent overwriting existing files
    if filepath.exists():
        raise FileExistsError(f"File {FILENAME} already exists in current directory")

    # Build markdown content with proper structure
    markdown_content = (
        "# Learning and Creativity\n"
        "\n"
        f"{PROSE_CONTENT}\n"
    )

    # Write file with UTF-8 encoding (no BOM) and Unix line endings
    filepath.write_text(markdown_content, encoding="utf-8")

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

    # Check H1 heading on first line
    assert lines[0].startswith('# '), (
        f"Missing H1 heading: first line should start with '# ' but found: {lines[0][:50]}"
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

    # 8. Check for at least 2 sentences (periods)
    period_count = prose.count('.')
    assert period_count >= 2, (
        f"Prose content should contain at least 2 sentences, but only found {period_count} period(s)."
    )

    return True


# ============================================================================
# Git Operations Function
# ============================================================================

def git_operations():
    """
    Execute git operations to stage, commit, and push the markdown file.

    Operations:
    1. git add test-k8kqxb.md
    2. git commit -m "feat(214): Create markdown file test-k8kqxb.md with prose content"
    3. git push -u origin HEAD

    Raises:
        subprocess.CalledProcessError: If any git command fails
    """
    # Stage the file
    subprocess.run(
        ["git", "add", FILENAME],
        check=True
    )

    # Commit with conventional commit message
    commit_message = "feat(214): Create markdown file test-k8kqxb.md with prose content"
    subprocess.run(
        ["git", "commit", "-m", commit_message],
        check=True
    )

    # Push to feature branch
    subprocess.run(
        ["git", "push", "-u", "origin", "HEAD"],
        check=True
    )


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

    print("Feature 214 implementation complete!")
