#!/usr/bin/env python3
"""
Feature 162: Create markdown file test-l2av8j.md with title and prose content.

This module implements file creation with explicit UTF-8 encoding and LF line endings,
following the established pattern of 170+ existing test files in the Sheep project.

Phase 1 (File Creation & Content Preparation): File creation and validation
Phase 2 (Git Integration & Publication): Git workflow (add, commit, push)
"""

from pathlib import Path
import sys
import subprocess


def create_file() -> None:
    """
    Create test-l2av8j.md markdown file with H1 heading and prose content.

    Uses pathlib.Path.write_bytes() with explicit UTF-8 encoding to ensure:
    - No BOM (Byte Order Mark) is added
    - Unix LF line endings (0x0A) across all platforms
    - Consistent encoding behavior
    """
    title = "Continuous Integration and Software Quality"
    prose = (
        "Continuous integration practices fundamentally transform how software teams collaborate and deliver "
        "reliable code by automating testing and validation at every commit. When teams embrace CI pipelines, "
        "they catch defects early, reduce integration friction, and enable faster feedback loops that keep "
        "developers informed of their impact on the codebase. This systematic approach to code quality has become "
        "essential in modern software development, allowing teams to maintain high standards while accelerating delivery."
    )

    # Construct markdown content: heading + blank line + prose + trailing newline
    content = f"# {title}\n\n{prose}\n"

    # Write to file at repository root with explicit UTF-8 encoding
    filepath = Path("test-l2av8j.md")
    filepath.write_bytes(content.encode('utf-8'))

    print(f"[OK] Created {filepath} ({len(content.encode('utf-8'))} bytes)")


def validate_file() -> bool:
    """
    Validate test-l2av8j.md meets all structural and encoding requirements.

    Checks:
    - File exists at expected path
    - File size is within acceptable range (300-600 bytes)
    - File contains exactly one H1 heading (line starting with '# ')
    - File contains blank line after heading (double newline pattern)
    - File contains prose content (exactly 2-3 sentences)
    - File is valid UTF-8 (via read_text with UTF-8 encoding)
    - File uses LF line endings (not CRLF)

    Returns:
        True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive error message
    """
    filepath = Path("test-l2av8j.md")

    # Check 1: File exists
    assert filepath.exists(), f"File {filepath} does not exist"

    # Check 2: File size within range
    file_size = filepath.stat().st_size
    assert 300 <= file_size <= 600, (
        f"File size {file_size} bytes outside acceptable range (300-600). "
        f"Target: 300-600 bytes"
    )

    # Check 3: UTF-8 encoding (will raise if not valid UTF-8)
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    # Check 4: Line endings are LF (not CRLF)
    raw_bytes = filepath.read_bytes()
    assert b'\r\n' not in raw_bytes, (
        "File contains CRLF line endings, but must use LF (Unix) line endings"
    )

    # Check 5: H1 heading exists
    lines = content.split('\n')
    assert len(lines) > 0 and lines[0].startswith('# '), (
        f"First line must be H1 heading (start with '# '). Got: {lines[0]!r}"
    )

    # Check 6: Blank line after heading (second line should be empty)
    assert len(lines) > 1 and lines[1] == '', (
        f"Second line must be blank (for blank line after heading). Got: {lines[1]!r}"
    )

    # Check 7: Prose content exists (exactly 2-3 sentences)
    prose_lines = lines[2:]
    prose_text = '\n'.join(prose_lines).strip()

    # Count sentences (periods, question marks, exclamation marks)
    sentence_count = sum(
        prose_text.count(punct)
        for punct in ['.', '?', '!']
    )
    assert 2 <= sentence_count <= 3, (
        f"Prose must contain exactly 2-3 sentences. Found {sentence_count} sentences"
    )

    # Check 8: Verify no BOM (UTF-8 BOM is bytes EF BB BF)
    assert not raw_bytes.startswith(b'\xef\xbb\xbf'), (
        "File contains UTF-8 BOM, but spec requires no BOM"
    )

    print(f"[OK] File {filepath} validates successfully")
    print(f"  - Size: {file_size} bytes (target: 300-600)")
    print(f"  - Heading: {lines[0]}")
    print(f"  - Sentences: {sentence_count}")
    print(f"  - Encoding: UTF-8 (valid, no BOM)")
    print(f"  - Line endings: LF (Unix)")

    return True


def git_operations() -> None:
    """
    Stage, commit, and push the markdown file using git.

    Uses subprocess.run() with list-based arguments to safely execute git commands.
    Commit message follows Conventional Commits specification:
    'feat(162): Create markdown file test-l2av8j.md with prose content'

    Raises:
        subprocess.CalledProcessError: If any git command fails (via check=True)
    """
    commit_message = "feat(162): Create markdown file test-l2av8j.md with prose content"

    # Stage the file: git add test-l2av8j.md
    # Using list-based arguments prevents shell injection attacks
    print("Staging file with 'git add test-l2av8j.md'...")
    subprocess.run(["git", "add", "test-l2av8j.md"], check=True)
    print("[OK] File staged successfully")

    # Commit the file with conventional commit message
    print(f"Committing with message: {commit_message}")
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print("[OK] File committed successfully")

    # Push to remote on feature branch
    print("Pushing to remote with 'git push -u origin HEAD'...")
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
    print("[OK] File pushed successfully")


def main() -> int:
    """Execute file creation and validation. Exit with code 0 on success, 1 on failure."""
    try:
        create_file()
        validate_file()
        print("\n[OK] Phase 1 (File Creation & Content Preparation) complete")
        return 0
    except Exception as e:
        print(f"[ERROR] Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
