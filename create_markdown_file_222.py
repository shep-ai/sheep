#!/usr/bin/env python3
"""
Implementation script for feature 222: markdown-file-creation-3cd3fb
Creates test-tmmd9v.md with proper markdown structure.
No validation layer per spec requirement.
"""

import subprocess
import sys
from pathlib import Path

# Set UTF-8 encoding for stdout to handle special characters on Windows
if sys.platform == "win32":
    import io
    if sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="")

# Module-level constants
FILENAME = "test-tmmd9v.md"
TITLE = "The Art of Effective Problem Solving"
PROSE = (
    "Effective problem solving requires a combination of critical thinking, creativity, and persistence. "
    "By breaking complex challenges into manageable steps and approaching them with curiosity, we can discover "
    "innovative solutions that lead to meaningful progress and personal growth."
)
COMMIT_MESSAGE = "feat(222): Create markdown file test-tmmd9v.md"


def create_file() -> Path:
    """
    Create markdown file with proper structure and encoding.

    Creates test-tmmd9v.md in the current working directory with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path object to the created or existing file if successful.

    Raises:
        OSError: If file creation fails.
    """
    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Create file path
    file_path = Path(FILENAME)

    # If file already exists, just return it (skip creation)
    if file_path.exists():
        print(f"✓ File {file_path} already exists, skipping creation")
        return file_path

    try:
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"✓ Created {file_path}")
        return file_path
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        raise
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        raise


def git_add() -> None:
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


def git_commit() -> None:
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


def git_push() -> None:
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


def main() -> None:
    """
    Main entry point: orchestrate complete workflow.

    Executes the full feature 222 workflow:
    1. Phase 1: Create markdown file with proper encoding and line endings
    2. Phase 2: Git integration (add, commit, push)

    No validation layer per spec requirement "No validation, create only".

    Catches specific exceptions and logs errors to stderr before exiting:
    - OSError: File I/O problems (system-level issue)
    - subprocess.CalledProcessError: Git command failures with command output

    Returns:
        0 on success, 1 on failure
    """
    print("=" * 60)
    print("Feature 222: Markdown File Creation")
    print("=" * 60)

    try:
        # Phase 1: Create markdown file
        print("\nPhase 1: Creating markdown file...")
        create_file()

        # Phase 2: Git integration
        print("\nPhase 2: Git integration and workflow...")
        git_add()
        git_commit()
        git_push()

        # Success
        print("\n" + "=" * 60)
        print("Successfully created test-tmmd9v.md")
        print("File has been created, staged, committed, and pushed.")
        print("=" * 60)
        sys.exit(0)

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
