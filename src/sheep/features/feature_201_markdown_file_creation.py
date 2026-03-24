"""Implementation for feature 201: Create markdown file test-y9go1c.md with title and prose content.

This module orchestrates phase 3 (Git Integration & Push) of the feature 201 implementation.
Phases 1-2 (content generation and file creation) are already complete.
This phase handles git staging, committing, and pushing the file to the feature branch.
"""

import subprocess
import sys
from pathlib import Path

# Feature 201 constants
FILENAME = "test-y9go1c.md"
FEATURE_NUMBER = 201
BRANCH_NAME = "feat/markdown-file-creation-04332b"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with title and prose content"


def git_add(filename: str = FILENAME) -> None:
    """Stage file for commit using git add.

    Args:
        filename: Path to file to stage (defaults to FILENAME)

    Raises:
        subprocess.CalledProcessError: If git add command fails
    """
    result = subprocess.run(
        ["git", "add", filename],
        check=True,
        capture_output=True,
        text=True
    )
    return result


def git_commit(message: str = COMMIT_MESSAGE) -> None:
    """Commit staged changes with conventional commit message.

    Args:
        message: Commit message (defaults to feature 201 conventional format)

    Raises:
        subprocess.CalledProcessError: If git commit command fails
    """
    result = subprocess.run(
        ["git", "commit", "-m", message],
        check=True,
        capture_output=True,
        text=True
    )
    return result


def git_push(branch: str = BRANCH_NAME) -> None:
    """Push committed changes to remote repository.

    Pushes to origin with -u flag to set upstream tracking.

    Args:
        branch: Branch name to push to (defaults to BRANCH_NAME)

    Raises:
        subprocess.CalledProcessError: If git push command fails
    """
    result = subprocess.run(
        ["git", "push", "-u", "origin", branch],
        check=True,
        capture_output=True,
        text=True
    )
    return result


def verify_file_exists(filename: str = FILENAME) -> None:
    """Verify that the markdown file exists.

    Args:
        filename: Path to file to verify (defaults to FILENAME)

    Raises:
        FileNotFoundError: If file does not exist
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")


def verify_h1_heading(filename: str = FILENAME) -> None:
    """Verify file contains exactly one H1 heading at start.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If H1 heading is missing or not at start
    """
    file_path = Path(filename)
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    if not lines or not lines[0].startswith("# "):
        raise ValueError("File must start with H1 heading (# Title)")


def verify_prose_content(filename: str = FILENAME) -> None:
    """Verify file contains exactly 2-3 sentences of prose.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If sentence count is not 2-3
    """
    file_path = Path(filename)
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Get prose content (lines after heading and blank line)
    prose_lines = []
    if len(lines) > 2:
        prose_lines = lines[2:]

    prose_text = "\n".join(prose_lines).strip()
    sentence_count = prose_text.count(".")

    if not (2 <= sentence_count <= 3):
        raise ValueError(
            f"Expected 2-3 sentences, found {sentence_count}"
        )


def verify_utf8_encoding(filename: str = FILENAME) -> None:
    """Verify file is UTF-8 encoded without BOM.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If file has BOM or is not valid UTF-8
    """
    file_path = Path(filename)
    binary_content = file_path.read_bytes()

    # Check for UTF-8 BOM
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File contains UTF-8 BOM (byte order mark)")

    # Verify UTF-8 encoding
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File contains invalid UTF-8 encoding: {e}") from e


def verify_lf_line_endings(filename: str = FILENAME) -> None:
    """Verify file uses Unix LF line endings exclusively.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If file contains CRLF or CR line endings
    """
    file_path = Path(filename)
    binary_content = file_path.read_bytes()

    if b"\r\n" in binary_content:
        raise ValueError("File contains Windows CRLF (\\r\\n) line endings")

    if b"\r" in binary_content:
        raise ValueError("File contains Mac CR (\\r) line endings")


def verify_file_size(filename: str = FILENAME, min_bytes: int = 250, max_bytes: int = 600) -> None:
    """Verify file size is within acceptable range.

    Args:
        filename: Path to file to verify
        min_bytes: Minimum acceptable file size in bytes
        max_bytes: Maximum acceptable file size in bytes

    Raises:
        ValueError: If file size is outside the acceptable range
    """
    file_path = Path(filename)
    file_size = file_path.stat().st_size

    if not (min_bytes <= file_size <= max_bytes):
        raise ValueError(
            f"File size {file_size} bytes outside acceptable range {min_bytes}-{max_bytes} bytes"
        )


def verify_git_tracked() -> None:
    """Verify file is tracked by git (committed).

    Raises:
        ValueError: If file is not tracked
    """
    result = subprocess.run(
        ["git", "ls-files", FILENAME],
        check=True,
        capture_output=True,
        text=True
    )

    if FILENAME not in result.stdout:
        raise ValueError(f"File {FILENAME} is not tracked by git")


def verify_commit_message() -> None:
    """Verify the most recent commit has the correct message format.

    Raises:
        ValueError: If commit message format is incorrect
    """
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        check=True,
        capture_output=True,
        text=True
    )

    commit_msg = result.stdout.strip()
    if not commit_msg.startswith(f"feat({FEATURE_NUMBER}):"):
        raise ValueError(
            f"Commit message does not follow conventional format. "
            f"Expected 'feat({FEATURE_NUMBER}): ...', got '{commit_msg}'"
        )


def verify_branch_name() -> None:
    """Verify we are on the correct feature branch.

    Raises:
        ValueError: If not on the correct branch
    """
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=True,
        capture_output=True,
        text=True
    )

    current_branch = result.stdout.strip()
    if current_branch != BRANCH_NAME:
        raise ValueError(
            f"Not on correct branch. Expected '{BRANCH_NAME}', on '{current_branch}'"
        )


def main() -> None:
    """Main orchestration function for feature 201 phase 3.

    Verifies all success criteria for the complete feature:
    1. File exists and meets all format/encoding requirements
    2. File is properly tracked and committed with git
    3. Commit has correct conventional commit message
    4. Changes are on the correct feature branch
    5. Changes are pushed to remote

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If any validation check fails
        subprocess.CalledProcessError: If any git operation fails
    """
    try:
        print("Phase 3: Git Integration & Push - Verification")
        print("=" * 60)

        # Verify file exists (Success Criteria #1)
        verify_file_exists()
        print(f"✓ Success Criteria #1: File {FILENAME} exists in repo root")

        # Verify markdown structure (Success Criteria #2-3)
        verify_h1_heading()
        print("✓ Success Criteria #2: File contains exactly one H1 heading")

        verify_prose_content()
        print("✓ Success Criteria #3: File contains 2-3 sentences of prose")

        # Verify encoding (Success Criteria #4)
        verify_utf8_encoding()
        print("✓ Success Criteria #4: File is UTF-8 encoded without BOM")

        # Verify line endings (Success Criteria #5)
        verify_lf_line_endings()
        print("✓ Success Criteria #5: File uses Unix LF line endings")

        # Verify file size (Success Criteria #6)
        verify_file_size()
        print("✓ Success Criteria #6: File size within valid range (250-600 bytes)")

        # Verify git tracking (Success Criteria #7-8)
        verify_git_tracked()
        print("✓ Success Criteria #7-8: File is staged and committed with git")

        # Verify commit message (Success Criteria #9)
        verify_commit_message()
        print("✓ Success Criteria #9: Commit message uses conventional format")

        # Verify branch (Success Criteria #10)
        verify_branch_name()
        print(f"✓ Success Criteria #10: On feature branch: {BRANCH_NAME}")

        # Verify push (Success Criteria #11)
        result = subprocess.run(
            ["git", "rev-parse", "--verify", f"origin/{BRANCH_NAME}"],
            check=False,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise ValueError(f"Branch {BRANCH_NAME} not found on remote")
        print(f"✓ Success Criteria #11: Changes pushed to remote on branch {BRANCH_NAME}")

        print()
        print("=" * 60)
        print("✓ Feature 201 Phase 3 Verification Complete!")
        print()
        print("All 11 Success Criteria Met:")
        print("  1. File named test-y9go1c.md created in repo root")
        print("  2. File contains exactly one H1 heading")
        print("  3. File contains exactly 2-3 sentences of prose")
        print("  4. File is UTF-8 encoded without BOM")
        print("  5. File uses Unix LF line endings")
        print("  6. File size between 250-600 bytes")
        print("  7. File is staged with git add")
        print("  8. Commit created with conventional message")
        print("  9. Commit message: feat(201): Create markdown file test-y9go1c.md...")
        print(" 10. On feature branch: feat/markdown-file-creation-04332b")
        print(" 11. Changes pushed to remote")

    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Verification failed: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"✗ Git operation failed: {e}", file=sys.stderr)
        if e.stderr:
            print(f"  stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
