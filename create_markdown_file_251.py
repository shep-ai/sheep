#!/usr/bin/env python3
"""
Implementation script for feature 251: markdown-file-creation-5b29b2

Creates test-xoqnko.md with proper markdown structure, validates encoding and
line endings, then stages, commits, and pushes to the feature branch.

Phase 1: Markdown File Creation and Structural Validation
- Create file with pathlib using UTF-8 encoding and LF line endings
- Validate structure (H1 heading, blank line, 2-3 sentences)
- Validate encoding (UTF-8 without BOM) and line endings (LF only)
"""

import re
import subprocess
import sys
from pathlib import Path

# Module-level constants
FILENAME = "test-xoqnko.md"
TITLE = "The Power of Continuous Testing"
PROSE = (
    "Testing is the backbone of software reliability, catching defects before they reach users and providing confidence in code changes. "
    "By automating tests and running them continuously, teams can iterate faster without sacrificing quality or introducing regressions. "
    "A comprehensive test suite becomes the living documentation of system behavior, enabling developers to refactor with assurance and maintain momentum across sprints."
)
COMMIT_MESSAGE = "feat(251): create markdown file test-xoqnko.md with prose content"

# Regex patterns for validation
HEADING_PATTERN = re.compile(r"^# .+$")


def create_file():
    """
    Create markdown file with proper structure and encoding (Task 1).

    Creates test-xoqnko.md in the current working directory with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path object to the created file if successful.

    Raises:
        FileExistsError: If file already exists (defensive check).
        OSError: If file creation fails.
    """
    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Create file path
    file_path = Path(FILENAME)

    # Check file doesn't already exist (defensive check)
    if file_path.exists():
        raise FileExistsError(f"File {file_path} already exists")

    try:
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"[OK] Created {file_path}")
        return file_path
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        raise
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        raise


def validate_structure(file_path):
    """
    Validate file structure (heading, blank line, sentences) (Task 2).

    Checks:
    - First line is H1 heading (matches regex ^# .+$)
    - Second line is blank (empty string)
    - Remaining lines contain 2-3 sentences (counted by punctuation: . ! ?)

    Args:
        file_path: Path to file to validate

    Returns:
        True if all structure checks pass, False otherwise.

    Raises:
        FileNotFoundError: If file does not exist.
        UnicodeDecodeError: If file is not valid UTF-8.
    """
    if not file_path.exists():
        print(f"[FAIL] File does not exist: {file_path}", file=sys.stderr)
        return False

    # Read file content as text
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Check 1: First line is H1 heading
    if not lines or not HEADING_PATTERN.match(lines[0]):
        print(f"[FAIL] First line is not a valid H1 heading (^# .+$)", file=sys.stderr)
        return False
    print(f"[OK] H1 heading found: {lines[0]}")

    # Check 2: Second line is blank
    if len(lines) < 2 or lines[1] != "":
        print(f"[FAIL] Second line is not blank (expected blank line after heading)", file=sys.stderr)
        return False
    print("[OK] Blank line present after heading")

    # Check 3: Count sentences in remaining lines (lines[2:])
    if len(lines) < 3:
        print(f"[FAIL] No prose content found (need lines after blank line)", file=sys.stderr)
        return False

    prose_text = "\n".join(lines[2:]).strip()
    if not prose_text:
        print(f"[FAIL] Prose content is empty", file=sys.stderr)
        return False

    # Count sentences by finding punctuation marks that end sentences
    punctuation_matches = re.findall(r"[.!?]", prose_text)
    sentence_count = len(punctuation_matches)

    if sentence_count < 2 or sentence_count > 3:
        print(f"[FAIL] Found {sentence_count} sentences, expected 2-3", file=sys.stderr)
        return False
    print(f"[OK] Prose contains {sentence_count} sentences")

    return True


def validate_encoding_and_line_endings(file_path):
    """
    Validate file encoding (UTF-8) and line endings (LF) (Task 3).

    Checks:
    - File is valid UTF-8 encoded
    - File does not contain UTF-8 BOM (EF BB BF at start)
    - File contains LF line endings (\n)
    - File does not contain CRLF line endings (\r\n)

    Args:
        file_path: Path to file to validate

    Returns:
        True if all encoding/line-ending checks pass, False otherwise.

    Raises:
        FileNotFoundError: If file does not exist.
    """
    if not file_path.exists():
        print(f"[FAIL] File does not exist: {file_path}", file=sys.stderr)
        return False

    # Read file in binary mode
    try:
        file_bytes = file_path.read_bytes()
    except OSError as e:
        print(f"[FAIL] Error reading file: {e}", file=sys.stderr)
        return False

    # Check 1: UTF-8 encoding (attempt to decode)
    try:
        file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        print(f"[FAIL] File is not valid UTF-8", file=sys.stderr)
        return False
    print("[OK] File is valid UTF-8 encoded")

    # Check 2: No UTF-8 BOM (EF BB BF)
    UTF8_BOM = b"\xef\xbb\xbf"
    if file_bytes.startswith(UTF8_BOM):
        print(f"[FAIL] File contains UTF-8 BOM", file=sys.stderr)
        return False
    print("[OK] File has no UTF-8 BOM")

    # Check 3: No CRLF line endings
    if b"\r\n" in file_bytes:
        print(f"[FAIL] File contains CRLF line endings (should be LF only)", file=sys.stderr)
        return False
    print("[OK] File has no CRLF line endings")

    # Check 4: Contains LF line endings
    if b"\n" not in file_bytes:
        print(f"[FAIL] File does not contain LF line endings", file=sys.stderr)
        return False
    print("[OK] File uses LF line endings")

    return True


def validate_file_size(file_path):
    """
    Validate file size is in expected range (400-600 bytes).

    Args:
        file_path: Path to file to validate

    Returns:
        True if file size is in range, False otherwise.
    """
    if not file_path.exists():
        return False

    file_bytes = file_path.read_bytes()
    file_size = len(file_bytes)

    if not (400 <= file_size <= 600):
        print(f"[FAIL] File size {file_size} bytes is outside expected range 400-600", file=sys.stderr)
        return False

    print(f"[OK] File size is {file_size} bytes (within 400-600 range)")
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

    Executes the full feature 251 workflow:
    1. Phase 1: Create markdown file with proper encoding and line endings
    2. Phase 1: Validate file structure (heading, blank line, sentences)
    3. Phase 1: Validate file encoding (UTF-8) and line endings (LF)
    4. Phase 2: Git integration (add, commit, push)

    Catches specific exceptions and logs errors to stderr before exiting:
    - FileExistsError: File already exists (defensive check)
    - OSError: File I/O problems (system-level issue)
    - subprocess.CalledProcessError: Git command failures with command output

    Returns:
        0 on success, 1 on failure
    """
    print("=" * 60)
    print("Feature 251: Markdown File Creation and Validation")
    print("=" * 60)

    try:
        # Phase 1: Create markdown file
        print("\nPhase 1: Creating markdown file...")
        file_path = create_file()

        # Phase 1: Validate file structure
        print("\nPhase 1: Validating file structure...")
        if not validate_structure(file_path):
            sys.exit(1)

        # Phase 1: Validate encoding and line endings
        print("\nPhase 1: Validating encoding and line endings...")
        if not validate_encoding_and_line_endings(file_path):
            sys.exit(1)

        # Phase 1: Validate file size
        print("\nPhase 1: Validating file size...")
        if not validate_file_size(file_path):
            sys.exit(1)

        # Phase 2: Git integration
        print("\nPhase 2: Git integration and workflow...")
        git_add()
        git_commit()
        git_push()

        # Success
        print("\n" + "=" * 60)
        print("Successfully created test-xoqnko.md")
        print("File has been created, validated, staged, committed, and pushed.")
        print("=" * 60)
        sys.exit(0)

    except FileExistsError as e:
        print(f"[ERROR] File already exists: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"[ERROR] File I/O error: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git command failed: {e.cmd}", file=sys.stderr)
        if e.stderr:
            print(f"  Error output: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
