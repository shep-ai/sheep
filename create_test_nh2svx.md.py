#!/usr/bin/env python3
"""
Create markdown file test-nh2svx.md with H1 heading and prose content.
Implements feature 098: markdown-file-creation-7312a8

This script:
1. Composes prose content (H1 heading + blank line + 2-3 sentences)
2. Creates file at repository root using pathlib.Path.write_text()
3. Validates file meets all success criteria (encoding, line endings, size, format)
4. Stages, commits, and pushes file using git
"""

import subprocess
from pathlib import Path


def compose_content() -> tuple[str, str]:
    """Compose markdown heading and prose content.

    Returns:
        Tuple of (heading, prose) where prose is 2-3 sentences
    """
    heading = "# The Art of Asking Good Questions"
    prose = (
        "The ability to ask thoughtful questions is a fundamental skill that drives "
        "learning and innovation across all domains of human knowledge. "
        "Good questions open new pathways of inquiry, challenge assumptions, and reveal "
        "hidden complexities that might otherwise remain unexamined. "
        "By cultivating the practice of asking better questions, individuals and "
        "organizations unlock deeper understanding and discover solutions that transform "
        "how we approach problems."
    )
    return heading, prose


def create_markdown_file(filename: str, heading: str, prose: str) -> None:
    """Create markdown file at repository root.

    Args:
        filename: Name of file to create (e.g., "test-nh2svx.md")
        heading: H1 markdown heading (e.g., "# Title")
        prose: 2-3 sentences of prose content

    Writes file with structure: heading + blank line + prose + final newline
    Ensures UTF-8 encoding without BOM and LF line endings.
    """
    # Compose full content: heading + blank line + prose + final newline
    content = f"{heading}\n\n{prose}\n"

    # Create file using pathlib, writing as bytes to ensure LF line endings on all platforms
    # (text mode on Windows would convert \n to \r\n)
    file_path = Path(filename)
    file_path.write_bytes(content.encode("utf-8"))
    print(f"[OK] Created file: {file_path.absolute()}")


def validate_file(filename: str) -> bool:
    """Validate markdown file meets all success criteria.

    Checks:
    - File exists and is readable
    - H1 heading on line 1 (starts with "# ")
    - Blank line on line 2
    - 2-3 sentences of prose (counted by periods)
    - File size is 320-600 bytes (hard constraint)
    - UTF-8 encoding without BOM (no \xef\xbb\xbf prefix)
    - LF line endings only (no \r\n)
    - Markdown syntax is valid

    Args:
        filename: Path to file to validate

    Returns:
        True if all validation checks pass, False otherwise
    """
    file_path = Path(filename)

    # Check 1: File exists
    if not file_path.exists():
        print(f"[FAIL] File does not exist: {filename}")
        return False
    print(f"[OK] File exists")

    # Check 2: File is readable
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[FAIL] File is not readable: {e}")
        return False
    print(f"[OK] File is readable (UTF-8 encoding)")

    # Check 3: H1 heading on line 1
    lines = content.split("\n")
    if not lines[0].startswith("# "):
        print(f"[FAIL] Line 1 is not H1 heading (starts with '# ')")
        return False
    print(f"[OK] H1 heading present: {lines[0]}")

    # Check 4: Blank line on line 2
    if lines[1] != "":
        print(f"[FAIL] Line 2 is not blank (separator)")
        return False
    print(f"[OK] Blank line separator present")

    # Check 5: Prose content (lines 3+)
    prose_lines = lines[2:]
    # Remove trailing empty lines
    while prose_lines and prose_lines[-1] == "":
        prose_lines.pop()
    prose_text = "\n".join(prose_lines)

    # Count sentences by periods
    period_count = prose_text.count(".")
    if period_count < 2 or period_count > 3:
        print(f"[FAIL] Prose has {period_count} sentences; expected 2-3")
        return False
    print(f"[OK] Prose has {period_count} sentences")

    # Check 6: File size is 320-600 bytes (hard constraint)
    file_size = file_path.stat().st_size
    if file_size < 320 or file_size > 600:
        print(f"[FAIL] File size is {file_size} bytes; expected 320-600")
        return False
    print(f"[OK] File size is {file_size} bytes (within 320-600 range)")

    # Check 7: UTF-8 encoding without BOM
    raw_bytes = file_path.read_bytes()
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        print(f"[FAIL] File has UTF-8 BOM; expected UTF-8 without BOM")
        return False
    print(f"[OK] UTF-8 encoding without BOM")

    # Check 8: LF line endings only (no CRLF)
    if b'\r\n' in raw_bytes:
        print(f"[FAIL] File has CRLF line endings; expected LF only")
        return False
    print(f"[OK] LF line endings (Unix-style)")

    # Check 9: Markdown syntax is valid (basic check)
    # For this simple structure, ensure heading is properly formatted
    if not lines[0].startswith("# ") or len(lines[0]) < 3:
        print(f"[FAIL] H1 heading format is invalid")
        return False
    print(f"[OK] Markdown syntax is valid")

    return True


def git_add(filename: str) -> None:
    """Stage file with git add.

    Args:
        filename: File to stage

    Raises:
        subprocess.CalledProcessError: If git add fails
    """
    subprocess.run(["git", "add", filename], check=True)
    print(f"[OK] Staged file with git add")


def git_commit(message: str) -> None:
    """Commit staged changes with conventional message.

    Args:
        message: Commit message

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    subprocess.run(["git", "commit", "-m", message], check=True)
    print(f"[OK] Committed: {message}")


def git_push() -> None:
    """Push commit to feature branch.

    Raises:
        subprocess.CalledProcessError: If git push fails
    """
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
    print(f"[OK] Pushed to feature branch")


def main() -> None:
    """Main implementation: create file, validate, commit, push."""
    print("\n=== Feature 098: Markdown File Creation ===\n")

    filename = "test-nh2svx.md"
    print(f"Creating: {filename}\n")

    # Phase 1: Prose Composition & File Creation
    print("Phase 1: Prose Composition & File Creation")
    print("-" * 40)
    heading, prose = compose_content()
    print(f"Heading: {heading}")
    print(f"Prose: {prose[:80]}...\n")

    create_markdown_file(filename, heading, prose)
    print()

    # Phase 2: Validation & Verification
    print("Phase 2: Validation & Verification")
    print("-" * 40)
    if not validate_file(filename):
        print("\n[FAIL] Validation failed. File not staged for commit.")
        return
    print()

    # Phase 3: Git Integration & Push
    print("Phase 3: Git Integration & Push")
    print("-" * 40)
    try:
        git_add(filename)
        git_commit("feat(098): create markdown file test-nh2svx.md with prose content")
        git_push()
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Git operation failed: {e}")
        return

    print("\n=== Feature 098 Complete ===\n")
    print(f"[OK] Successfully created {filename}")
    print(f"[OK] All validation checks passed")
    print(f"[OK] Committed and pushed to feature branch\n")


if __name__ == "__main__":
    main()
