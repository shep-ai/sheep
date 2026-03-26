#!/usr/bin/env python3
"""
Implementation script for feature 218: markdown-file-creation-e92f29
Creates test-gmvvpm.md with proper markdown structure and validation.
"""

import sys
import subprocess
from pathlib import Path

# Module-level constants
FILENAME = "test-gmvvpm.md"
TITLE = "The Power of Continuous Learning"
PROSE = (
    "Continuous learning is essential in a rapidly evolving world where knowledge and technologies "
    "transform at an unprecedented pace. By cultivating curiosity and dedicating time to expand our "
    "understanding, we equip ourselves with the adaptability and resilience needed to thrive in changing environments. "
    "This commitment to growth not only enhances our professional capabilities but also enriches our personal "
    "development and opens doors to unexpected opportunities."
)
COMMIT_MESSAGE = "feat(218): Create markdown file test-gmvvpm.md"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-gmvvpm.md in the current working directory with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path object to the created file if successful.

    Raises:
        OSError: If file creation fails.
    """
    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Create file path
    file_path = Path(FILENAME)

    # Check file doesn't already exist
    if file_path.exists():
        print(f"Error: File {file_path} already exists", file=sys.stderr)
        return None

    try:
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"✓ Created {file_path}")
        return file_path
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        return None
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        return None


def validate_file(file_path):
    """
    Validate markdown file structure and properties.

    Performs comprehensive validation of the created markdown file:
    - File exists and has non-zero size
    - UTF-8 encoding without BOM
    - Unix LF line endings (no CRLF)
    - H1 heading on first line
    - Blank line on second line
    - 2-3 sentences of prose content
    - File ends with newline
    - File size within 300-600 bytes

    Args:
        file_path: Path object or string path to file to validate.

    Returns:
        True if validation passes.

    Raises:
        ValueError: If any validation check fails, with descriptive message.
    """
    file_path = Path(file_path)

    # Check file exists
    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    # Check file size is non-zero
    file_size = file_path.stat().st_size
    if file_size == 0:
        raise ValueError(f"File is empty: {file_path}")

    # Read file as bytes for encoding and line ending checks
    try:
        binary_content = file_path.read_bytes()
    except OSError as e:
        raise ValueError(f"Cannot read file: {e}")

    # Check for UTF-8 BOM (EF BB BF bytes)
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File contains UTF-8 BOM (should use plain UTF-8)")

    # Check for CRLF line endings
    if b"\r\n" in binary_content:
        raise ValueError("File uses CRLF line endings (should use LF)")

    # Decode content as UTF-8
    try:
        content = binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")

    # Split into lines (preserving empty lines)
    lines = content.split("\n")

    # Check H1 heading on first line
    if not lines or not lines[0].startswith("# "):
        raise ValueError("First line must be H1 heading starting with '# '")

    # Check blank line on second line
    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank")

    # Check prose content has 2-3 sentences
    if len(lines) < 3:
        raise ValueError("File must contain prose content after heading")

    prose_content = "\n".join(lines[2:]).strip()
    if not prose_content:
        raise ValueError("Prose content is empty")

    sentence_count = prose_content.count(".")
    if not (2 <= sentence_count <= 3):
        raise ValueError(
            f"Prose must have 2-3 sentences (found {sentence_count})"
        )

    # Check file ends with newline
    if not content.endswith("\n"):
        raise ValueError("File must end with newline")

    # Check file size is in 300-600 byte range
    if not (300 <= file_size <= 600):
        raise ValueError(
            f"File size {file_size} bytes is outside 300-600 byte range"
        )

    return True


def git_add():
    """
    Stage the markdown file in git.

    Uses 'git add' command to stage the file for commit.

    Raises:
        subprocess.CalledProcessError: If git add command fails.
    """
    try:
        subprocess.run(["git", "add", FILENAME], check=True)
        print(f"✓ Staged {FILENAME} with git add")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e


def git_commit():
    """
    Create a git commit with the markdown file.

    Uses 'git commit' with the conventional commit message format.

    Raises:
        subprocess.CalledProcessError: If git commit command fails.
    """
    try:
        subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
        print(f"✓ Created commit: {COMMIT_MESSAGE}")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e


def git_push():
    """
    Push the commit to the remote feature branch.

    Uses 'git push -u origin HEAD' to push to the current branch.
    The -u flag sets upstream tracking for the branch.

    Raises:
        subprocess.CalledProcessError: If git push command fails.
    """
    try:
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
        print("✓ Pushed to remote origin")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e


def main():
    """
    Main entry point: orchestrate complete workflow.

    Executes the full feature 218 workflow:
    1. Phase 1: Create markdown file with proper encoding and line endings
    2. Phase 2: Validate file structure, encoding, and size
    3. Phase 3: Git integration (add, commit, push)

    Catches specific exceptions and logs errors to stderr before exiting:
    - ValueError: Validation failures (user-facing, actionable)
    - OSError: File I/O problems (system-level issue)
    - subprocess.CalledProcessError: Git command failures with command output

    Returns:
        0 on success, 1 on failure
    """
    print("=" * 60)
    print("Feature 218: Markdown File Creation")
    print("=" * 60)

    try:
        # Phase 1: Create markdown file
        print("\nPhase 1: Creating markdown file...")
        file_path = create_file()
        if not file_path:
            print("Error: File creation failed", file=sys.stderr)
            sys.exit(1)

        # Phase 2: Validate file
        print("Phase 2: Validating file structure and content...")
        validate_file(file_path)
        print("✓ File validation passed")

        # Phase 3: Git integration
        print("\nPhase 3: Git integration and workflow...")
        git_add()
        git_commit()
        git_push()

        # Success
        print("\n" + "=" * 60)
        print("Successfully created test-gmvvpm.md")
        print("File has been created, validated, staged, committed, and pushed.")
        print("=" * 60)
        sys.exit(0)

    except ValueError as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"✗ File I/O error: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"✗ Git command failed: {e.cmd}", file=sys.stderr)
        if e.stderr:
            print(f"  Error output: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
