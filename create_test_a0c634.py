#!/usr/bin/env python3
"""
Implementation script for feature 270: markdown-file-creation-9d9707
Creates test-a0c634.md with proper markdown structure and basic validation.
"""

import subprocess
import sys
from pathlib import Path

# Module-level constants
FILENAME = "test-a0c634.md"
TITLE = "Test A0C634"
PROSE = (
    "This is a test file created to demonstrate markdown file creation with proper structure and encoding. "
    "It serves as an example of how to generate markdown files programmatically while maintaining consistency. "
    "The file uses UTF-8 encoding and Unix-style line endings for cross-platform compatibility."
)
COMMIT_MESSAGE = "feat(270): create markdown file test-a0c634.md with prose content"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-a0c634.md in the current working directory with:
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

    try:
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"[OK] Created {file_path}")
        return file_path
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        return None
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        return None


def validate_file(file_path):
    """
    Validate that the markdown file exists and is readable.

    Performs basic validation of the created markdown file:
    - File exists
    - File is readable

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

    # Check file is a regular file
    if not file_path.is_file():
        raise ValueError(f"Path is not a regular file: {file_path}")

    # Check file is readable
    try:
        file_path.read_text(encoding="utf-8")
    except OSError as e:
        raise ValueError(f"Cannot read file: {e}")

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
        print(f"[OK] Staged {FILENAME} with git add")
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
        print(f"[OK] Created commit: {COMMIT_MESSAGE}")
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
        print("[OK] Pushed to remote origin")
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

    Executes the full feature 270 workflow:
    1. Phase 1: Create markdown file with proper encoding and line endings
    2. Phase 1: Validate file exists and is readable
    3. Phase 2: Stage file with git add
    4. Phase 2: Create commit with conventional message
    5. Phase 2: Push to remote origin

    Catches specific exceptions and logs errors to stderr before exiting:
    - ValueError: Validation failures (user-facing, actionable)
    - OSError: File I/O problems (system-level issue)
    - subprocess.CalledProcessError: Git command failures with command output

    Returns:
        0 on success, 1 on failure
    """
    print("=" * 60)
    print("Feature 270: Markdown File Creation")
    print("=" * 60)

    try:
        # Phase 1: Create markdown file
        print("\nPhase 1: Creating markdown file...")
        file_path = create_file()
        if not file_path:
            print("Error: File creation failed", file=sys.stderr)
            sys.exit(1)

        # Phase 1: Validate file exists and is readable
        print("Phase 1: Validating file exists and is readable...")
        validate_file(file_path)
        print("[OK] File validation passed")

        # Phase 2: Git Integration
        print("\nPhase 2: Git Integration & Validation")

        print("Phase 2: Staging file with git add...")
        git_add()

        print("Phase 2: Creating commit with conventional message...")
        git_commit()

        print("Phase 2: Pushing to remote origin...")
        git_push()

        # Success
        print("\n" + "=" * 60)
        print("Successfully created test-a0c634.md")
        print("File has been created, validated, and pushed to remote.")
        print("=" * 60)
        sys.exit(0)

    except ValueError as e:
        print(f"[FAIL] Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"[FAIL] File I/O error: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Git command failed: {e.cmd}", file=sys.stderr)
        if e.stderr:
            print(f"  Error output: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
