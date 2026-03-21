#!/usr/bin/env python3
"""Orchestration script for feature 142: Create and push markdown file test-hqbiuy.md.

This script implements the complete workflow:
1. Verify markdown file exists and is valid
2. Validate file encoding, line endings, and structure
3. Stage file with git add
4. Commit with conventional message
5. Push to remote feature branch

The script coordinates file validation and git operations to ensure
the markdown file is properly created and committed to the repository.
"""

from pathlib import Path
import subprocess
import sys
import re


# Configuration constants
FILENAME = "test-hqbiuy.md"
COMMIT_MESSAGE = "feat(142): Create markdown file test-hqbiuy.md with specification"
FEATURE_BRANCH = "feat/markdown-file-creation-b65b0e"


def validate_file(file_path: str) -> bool:
    """Validate markdown file meets all structural and encoding requirements.

    Checks:
    - File exists and has non-zero size
    - Content is valid UTF-8
    - File contains H1 heading on first line
    - File contains blank line after heading
    - File contains 2-3 sentences of prose content
    - File has no BOM bytes (UTF-8 without BOM)
    - File uses LF line endings, not CRLF
    - File ends with newline character

    Args:
        file_path: Path to file to validate

    Returns:
        True if all validations pass, False otherwise
    """
    file_path = Path(file_path)

    # Check file exists and has content
    if not file_path.exists():
        print(f"[FAIL] File does not exist: {file_path}")
        return False

    size_bytes = file_path.stat().st_size
    if size_bytes == 0:
        print(f"[FAIL] File is empty: {file_path}")
        return False

    print(f"[OK] File exists with size: {size_bytes} bytes")

    # Read file as binary to check BOM and CRLF
    with open(file_path, "rb") as f:
        binary_content = f.read()

    # Check for UTF-8 BOM (EF BB BF)
    if binary_content.startswith(b"\xef\xbb\xbf"):
        print("[FAIL] File contains UTF-8 BOM; expected UTF-8 without BOM")
        return False

    print("[OK] No UTF-8 BOM detected")

    # Check for CRLF (Windows line endings)
    if b"\r\n" in binary_content:
        print("[FAIL] File contains CRLF line endings; expected Unix LF")
        return False

    print("[OK] Unix LF line endings confirmed (no CRLF)")

    # Decode and validate text structure
    try:
        text_content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        print(f"[FAIL] File is not valid UTF-8: {e}")
        return False

    print("[OK] Valid UTF-8 encoding")

    # Check file ends with newline
    if not text_content.endswith("\n"):
        print("[FAIL] File does not end with newline character")
        return False

    print("[OK] File ends with newline")

    # Split into lines and validate structure
    lines = text_content.rstrip("\n").split("\n")

    if not lines:
        print("[FAIL] File is empty (no lines)")
        return False

    # Check first line is H1 heading
    if not lines[0].startswith("# "):
        print(f"[FAIL] First line is not H1 heading; got: {lines[0][:30]}")
        return False

    print(f"[OK] H1 heading found: {lines[0]}")

    # Check second line is blank
    if len(lines) < 2:
        print("[FAIL] File too short; needs heading, blank line, and prose")
        return False

    if lines[1] != "":
        print(f"[FAIL] Second line should be blank; got: {lines[1][:30]}")
        return False

    print("[OK] Blank line after heading confirmed")

    # Check prose content exists (sentences ending with periods)
    if len(lines) < 3:
        print("[FAIL] File too short; needs heading, blank line, and prose")
        return False

    prose_text = "\n".join(lines[2:])
    sentence_count = prose_text.count(".")

    if sentence_count < 2 or sentence_count > 3:
        print(
            f"[FAIL] Prose should contain 2-3 sentences; found {sentence_count}"
        )
        return False

    print(f"[OK] Prose content found: {sentence_count} sentences")

    return True


def stage_file(filename: str) -> bool:
    """Stage file in git using git add.

    Args:
        filename: Name of the file to stage

    Returns:
        True if successful, False otherwise
    """
    result = subprocess.run(
        ["git", "add", filename],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"[OK] Staged file in git: {filename}")
        return True

    print(f"[FAIL] git add failed: {result.stderr}")
    return False


def create_commit(message: str) -> bool:
    """Create a git commit with conventional commit message.

    Args:
        message: Commit message

    Returns:
        True if successful, False otherwise. Returns True if nothing to commit
        (file already committed), as this is not an error condition.
    """
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"[OK] Committed with message: {message}")
        return True

    # Check if error is "nothing to commit" (file already committed)
    combined_output = (result.stdout + result.stderr).lower()
    if "nothing to commit" in combined_output or "nothing added to commit" in combined_output:
        print("[OK] File already committed (nothing new to commit)")
        return True

    print(f"[FAIL] git commit failed: {result.stderr}")
    return False


def push_to_remote(branch_name: str) -> bool:
    """Push the commit to the remote feature branch.

    Args:
        branch_name: Feature branch name to push to

    Returns:
        True if successful, False otherwise
    """
    result = subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"[OK] Pushed to remote branch: {branch_name}")
        return True

    print(f"[FAIL] git push failed: {result.stderr}")
    return False


def main() -> int:
    """Main orchestration workflow.

    Returns:
        0 if successful, 1 if any step fails
    """
    print("=" * 60)
    print("Feature 142: Git Integration Workflow")
    print("=" * 60)

    # Step 1: Validate file
    print("\nStep 1: Validating file...")
    if not validate_file(FILENAME):
        print("\n[FAIL] File validation failed")
        return 1

    print("\n[OK] File validation passed")

    # Step 2: Stage file
    print("\nStep 2: Staging file...")
    if not stage_file(FILENAME):
        print("\n[FAIL] Git stage operation failed")
        return 1

    # Step 3: Commit
    print("\nStep 3: Creating commit...")
    if not create_commit(COMMIT_MESSAGE):
        print("\n[FAIL] Git commit operation failed")
        return 1

    # Step 4: Push
    print("\nStep 4: Pushing to remote...")
    if not push_to_remote(FEATURE_BRANCH):
        print("\n[FAIL] Git push operation failed")
        return 1

    print("\n" + "=" * 60)
    print("[OK] All operations completed successfully!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
