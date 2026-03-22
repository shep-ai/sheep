#!/usr/bin/env python3
"""
Feature 155: Create markdown file test-1k8ri0.md with title and prose content.

This module implements file creation with explicit UTF-8 encoding and LF line endings,
following the established pattern of 150+ existing test files in the Sheep project.

Phase 1 (Core Implementation): File creation and validation
Phase 2 (Git Integration & Delivery): Git workflow (add, commit, push)
"""

from pathlib import Path
import sys
import subprocess


def create_file() -> None:
    """
    Create test-1k8ri0.md markdown file with H1 heading and prose content.

    Uses pathlib.Path.write_bytes() with explicit UTF-8 encoding to ensure:
    - No BOM (Byte Order Mark) is added
    - Unix LF line endings (0x0A) across all platforms
    - Consistent encoding behavior
    """
    title = "The Art of Deliberate Practice"
    prose = (
        "Deliberate practice is the cornerstone of mastery in any domain, "
        "requiring focused effort on improving specific weaknesses rather than simply repeating "
        "familiar tasks. When practitioners engage in intentional, structured improvement with immediate "
        "feedback and course correction, they accelerate their development far beyond casual engagement. "
        "This principle has been validated across music, sports, mathematics, and professional fields, "
        "demonstrating that excellence emerges from systematic, goal-oriented effort rather than innate talent alone."
    )

    # Construct markdown content: heading + blank line + prose + trailing newline
    content = f"# {title}\n\n{prose}\n"

    # Write to file at repository root with explicit UTF-8 encoding
    filepath = Path("test-1k8ri0.md")
    filepath.write_bytes(content.encode('utf-8'))

    print(f"✓ Created {filepath} ({len(content.encode('utf-8'))} bytes)")


def validate_file() -> bool:
    """
    Validate test-1k8ri0.md meets all structural and encoding requirements.

    Checks:
    - File exists at expected path
    - File size is within acceptable range (300-800 bytes, targeting 400-600)
    - File contains exactly one H1 heading (line starting with '# ')
    - File contains blank line after heading (double newline pattern)
    - File contains prose content (at least 2 sentences)
    - File is valid UTF-8 (via read_text with UTF-8 encoding)

    Returns:
        True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive error message
    """
    filepath = Path("test-1k8ri0.md")

    # Check 1: File exists
    assert filepath.exists(), f"File {filepath} does not exist"

    # Check 2: File size within range
    file_size = filepath.stat().st_size
    assert 300 <= file_size <= 800, (
        f"File size {file_size} bytes outside acceptable range (300-800). "
        f"Target: 400-600 bytes"
    )

    # Check 3: UTF-8 encoding (will raise if not valid UTF-8)
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    # Check 4: H1 heading exists
    lines = content.split('\n')
    assert len(lines) > 0 and lines[0].startswith('# '), (
        f"First line must be H1 heading (start with '# '). Got: {lines[0]!r}"
    )

    # Check 5: Blank line after heading (second line should be empty)
    assert len(lines) > 1 and lines[1] == '', (
        f"Second line must be blank (for blank line after heading). Got: {lines[1]!r}"
    )

    # Check 6: Prose content exists (at least 2 sentences)
    prose_lines = lines[2:]
    prose_text = '\n'.join(prose_lines).strip()

    # Count sentences (periods, question marks, exclamation marks)
    sentence_count = sum(
        prose_text.count(punct)
        for punct in ['.', '?', '!']
    )
    assert sentence_count >= 2, (
        f"Prose must contain at least 2 sentences. Found {sentence_count} sentences"
    )

    print(f"✓ File {filepath} validates successfully")
    print(f"  - Size: {file_size} bytes (target: 400-600)")
    print(f"  - Heading: {lines[0]}")
    print(f"  - Sentences: {sentence_count}")
    print(f"  - Encoding: UTF-8 (valid)")

    return True


def git_operations() -> None:
    """
    Stage, commit, and push the markdown file using git.

    Uses subprocess.run() with list-based arguments to safely execute git commands.
    Commit message follows Conventional Commits specification:
    'feat(155): create markdown file test-1k8ri0.md with prose content'

    Raises:
        subprocess.CalledProcessError: If any git command fails (via check=True)
    """
    commit_message = "feat(155): create markdown file test-1k8ri0.md with prose content"

    # Stage the file: git add test-1k8ri0.md
    # Using list-based arguments prevents shell injection attacks
    print("Staging file with 'git add test-1k8ri0.md'...")
    subprocess.run(["git", "add", "test-1k8ri0.md"], check=True)
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
    """Execute file creation, validation, and git integration. Exit with code 0 on success, 1 on failure."""
    try:
        create_file()
        validate_file()
        print("\n✓ Phase 1 (Core Implementation) complete")

        print("\nPhase 2 (Git Integration & Delivery)...")
        git_operations()

        print("\n✓ All phases complete - feature 155 delivered successfully")
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
