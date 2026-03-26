#!/usr/bin/env python3
"""
Feature 223: Create markdown file test-no1878.md with title and prose content.

This module implements file creation with explicit UTF-8 encoding and LF line endings,
following the established pattern of 220+ existing test files in the Sheep project.

Phase 1: File creation and validation
Phase 2: Git integration (add, commit, push)
"""

from pathlib import Path
import sys
import subprocess


def create_file() -> Path:
    """
    Create test-no1878.md markdown file with H1 heading and prose content.

    Uses pathlib.Path.write_text() with explicit UTF-8 encoding to ensure:
    - UTF-8 encoding without BOM (Byte Order Mark)
    - Unix LF line endings (0x0A) via newline='\n' parameter
    - Consistent behavior across all platforms

    Returns:
        Path: The path to the created file

    Raises:
        FileExistsError: If file already exists at target path
    """
    filename = "test-no1878.md"
    title = "The Power of Persistence"
    prose = (
        "Success rarely comes instantly, but through consistent effort and determination. "
        "Every obstacle we face becomes a stepping stone when we choose to learn from it rather than be defeated by it. "
        "By embracing challenges with optimism and resilience, we unlock our potential to achieve extraordinary things."
    )

    # Construct markdown content: heading + blank line + prose + trailing newline
    content = f"# {title}\n\n{prose}\n"

    # Write to file at repository root with explicit UTF-8 encoding and Unix LF
    filepath = Path(filename)

    # Defensive check: prevent accidental overwrite
    if filepath.exists():
        raise FileExistsError(f"File {filename} already exists")

    # Use write_text with encoding and newline parameters for explicit control
    filepath.write_text(content, encoding='utf-8', newline='\n')

    return filepath


def validate_file(filepath: Path = None) -> bool:
    """
    Validate markdown file meets all structural and encoding requirements.

    Validates:
    - File exists at expected path
    - File size is within range (300-500 bytes per NFR-2)
    - File contains exactly one H1 heading (line starting with '# ')
    - File contains blank line after heading (double newline pattern)
    - File contains prose content (2-3 sentences)
    - File is valid UTF-8 without BOM
    - File uses Unix LF line endings only (no CRLF)
    - File ends with newline character

    Args:
        filepath (Path, optional): Path to file to validate. Defaults to test-no1878.md

    Returns:
        True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive error message
    """
    if filepath is None:
        filepath = Path("test-no1878.md")

    # Check 1: File exists
    assert filepath.exists(), f"File {filepath} does not exist"

    # Check 2: Read file as binary for encoding/line ending validation
    file_bytes = filepath.read_bytes()
    file_size = len(file_bytes)

    # Check 3: File size within range (300-500 bytes per NFR-2)
    assert 300 <= file_size <= 500, (
        f"File size {file_size} bytes outside acceptable range [300, 500]. "
        f"Target: 300-500 bytes"
    )

    # Check 4: No UTF-8 BOM (Byte Order Mark)
    assert not file_bytes.startswith(b'\xef\xbb\xbf'), (
        "File contains UTF-8 BOM; must use UTF-8 without BOM"
    )

    # Check 5: Unix LF line endings only (no CRLF)
    assert b'\r\n' not in file_bytes, (
        "File contains CRLF (\\r\\n) line endings; must use LF (\\n) only"
    )
    assert b'\r' not in file_bytes, (
        "File contains CR (\\r) characters; must use LF (\\n) only"
    )

    # Check 6: File ends with newline
    assert file_bytes.endswith(b'\n'), (
        "File must end with newline character (\\n)"
    )

    # Check 7: Valid UTF-8 encoding
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    # Check 8: H1 heading exists in first line
    lines = content.split('\n')
    assert len(lines) > 0 and lines[0].startswith('# '), (
        f"First line must be H1 heading (start with '# '). Got: {lines[0]!r}"
    )

    # Check 9: Blank line after heading (second line should be empty)
    assert len(lines) > 1 and lines[1] == '', (
        f"Second line must be blank (for blank line after heading). Got: {lines[1]!r}"
    )

    # Check 10: Prose content exists (2-3 sentences)
    prose_lines = lines[2:]
    prose_text = '\n'.join(prose_lines).strip()

    # Count sentences by looking for sentence terminators
    import re
    sentences = re.split(r'[.!?]+', prose_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)

    assert 2 <= sentence_count <= 3, (
        f"Prose must contain 2-3 sentences. Found {sentence_count} sentences"
    )

    print(f"✓ File {filepath} validates successfully")
    print(f"  - Size: {file_size} bytes (range: 300-500)")
    print(f"  - Heading: {lines[0]}")
    print(f"  - Sentences: {sentence_count}")
    print(f"  - Encoding: UTF-8 without BOM")
    print(f"  - Line endings: Unix LF")

    return True


def git_operations() -> None:
    """
    Stage, commit, and push the markdown file using git.

    Uses subprocess.run() with list-based arguments to safely execute git commands.
    Commit message follows Conventional Commits specification.

    Raises:
        subprocess.CalledProcessError: If any git command fails (via check=True)
    """
    filename = "test-no1878.md"
    commit_message = "feat(223): Create markdown file test-no1878.md"

    # Stage the file: git add test-no1878.md
    # Using list-based arguments prevents shell injection attacks
    print(f"Staging file with 'git add {filename}'...")
    subprocess.run(["git", "add", filename], check=True)
    print("✓ File staged successfully")

    # Commit the file with conventional commit message
    print(f"Committing with message: {commit_message}")
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print("✓ File committed successfully")

    # Push to remote on feature branch
    print("Pushing to remote with 'git push -u origin HEAD'...")
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
    print("✓ File pushed successfully")


def main() -> int:
    """Execute file creation and validation. Exit with code 0 on success, 1 on failure."""
    try:
        print("Phase 1: File Creation and Validation")
        print("=" * 50)
        filepath = create_file()
        print(f"✓ Created {filepath}")

        validate_file(filepath)
        print("\n✓ Phase 1 complete - file created and validated successfully")
        return 0
    except FileExistsError as e:
        print(f"✗ File creation error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"✗ File I/O error: {e}", file=sys.stderr)
        return 1
    except AssertionError as e:
        print(f"✗ Validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
