"""
Implementation script for feature 215: markdown file creation.

This module provides functions to:
1. Create a markdown file (test-7100re.md) with proper structure and content
2. Validate the file properties (encoding, line endings, size, structure)
3. Execute git operations (add, commit, push) using GitPython

The implementation uses Python standard library (pathlib) and GitPython >= 3.1.0
for git operations, and markdown library for CommonMark validation.
"""

from pathlib import Path
import markdown


# ============================================================================
# Constants
# ============================================================================

FILENAME = "test-7100re.md"
MIN_SIZE = 300
MAX_SIZE = 600

# Prose about innovation and technology (3 sentences, ~350 bytes total)
PROSE_CONTENT = (
    "Innovation drives technological progress and shapes how we solve complex problems in the modern world. "
    "Emerging technologies like artificial intelligence and cloud computing are revolutionizing industries and enabling organizations to scale their operations with unprecedented efficiency. "
    "By embracing innovation and continuous improvement, we can build better solutions that create lasting value."
)


# ============================================================================
# File Creation Function
# ============================================================================

def create_file():
    """
    Create test-7100re.md in the current directory with markdown structure.

    The file contains:
    - H1 heading (# Title)
    - Blank line
    - 3-sentence prose paragraph about innovation and technology
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path: Path object pointing to the created file

    Raises:
        FileExistsError: If test-7100re.md already exists in current directory
    """
    filepath = Path(FILENAME)

    # Prevent overwriting existing files
    if filepath.exists():
        raise FileExistsError(f"File {FILENAME} already exists in current directory. Remove it to proceed.")

    # Build markdown content with proper structure
    markdown_content = (
        "# Innovation and Progress\n"
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
    - Markdown structure is valid according to CommonMark specification

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

    # 9. Validate CommonMark markdown structure
    try:
        md = markdown.Markdown(extensions=[])
        html_output = md.convert(content)
        # Verify output contains h1 tag (indicates heading was parsed)
        assert '<h1>' in html_output.lower(), (
            "CommonMark validation failed: H1 heading not properly parsed"
        )
        # Verify output contains paragraph tags (indicates prose was parsed)
        assert '<p>' in html_output.lower(), (
            "CommonMark validation failed: Prose content not properly parsed"
        )
    except Exception as e:
        raise AssertionError(f"CommonMark markdown validation failed: {e}") from e

    return True


# ============================================================================
# Git Operations Function
# ============================================================================

def git_operations():
    """
    Execute git operations to stage, commit, and push the markdown file.

    Uses GitPython (>= 3.1.0) for git operations.

    Operations:
    1. git add test-7100re.md
    2. git commit -m "feat(215): Create markdown file test-7100re.md with prose content"
    3. git push to origin/HEAD

    Raises:
        ImportError: If GitPython is not installed
        Exception: If any git operation fails
    """
    try:
        from git import Repo
    except ImportError:
        raise ImportError("GitPython >= 3.1.0 is required but not installed")

    # Open the current repository
    repo = Repo(".")

    # Stage the file
    repo.index.add([FILENAME])

    # Create commit with conventional commit message
    commit_message = "feat(215): Create markdown file test-7100re.md with prose content"
    repo.index.commit(commit_message)

    # Push to origin (current branch)
    repo.remotes.origin.push()


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
        print(f"Git operations completed successfully")
    except Exception as e:
        print(f"Git operations failed: {e}")
        raise

    print("Feature 215 implementation complete!")
