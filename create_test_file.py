#!/usr/bin/env python3
"""
Feature 165: Create markdown file test-ewmber.md with title and prose content.

This module implements file creation with explicit UTF-8 encoding and LF line endings,
following the established pattern of 170+ existing test files in the Sheep project.

Phase 1 (Core Implementation): File creation and validation
Phase 2 (Git Integration & Delivery): Git workflow (add, commit, push)
"""

from pathlib import Path
import sys
import subprocess


def create_file() -> None:
    """
    Create test-ewmber.md markdown file with H1 heading and prose content.

    Uses pathlib.Path.write_bytes() with explicit UTF-8 encoding to ensure:
    - No BOM (Byte Order Mark) is added
    - Unix LF line endings (0x0A) across all platforms
    - Consistent encoding behavior
    """
    title = "Adaptive Learning"
    prose = (
        "Adaptive learning systems adjust their approach based on individual learner needs and progress, "
        "creating personalized educational experiences that respond dynamically to feedback and performance. "
        "These systems recognize that each learner has unique strengths, weaknesses, and preferred learning styles, "
        "and they tailor content difficulty and presentation to optimize comprehension and retention. "
        "By continuously analyzing learner interactions and outcomes, adaptive systems enhance educational effectiveness "
        "and make learning more efficient and engaging for students of all levels."
    )

    # Construct markdown content: heading + blank line + prose + trailing newline
    content = f"# {title}\n\n{prose}\n"

    # Write to file at repository root with explicit UTF-8 encoding
    filepath = Path("test-ewmber.md")
    filepath.write_bytes(content.encode('utf-8'))

    print(f"✓ Created {filepath} ({len(content.encode('utf-8'))} bytes)")


def validate_file() -> bool:
    """
    Validate test-ewmber.md meets all structural and encoding requirements.

    Checks:
    - File exists at expected path
    - File size is within acceptable range (300-600 bytes)
    - File contains exactly one H1 heading (line starting with '# ')
    - File contains blank line after heading (double newline pattern)
    - File contains prose content (at least 2 sentences)
    - File is valid UTF-8 (via read_text with UTF-8 encoding)

    Returns:
        True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive error message
    """
    filepath = Path("test-ewmber.md")

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
    print(f"  - Size: {file_size} bytes (range: 300-600)")
    print(f"  - Heading: {lines[0]}")
    print(f"  - Sentences: {sentence_count}")
    print(f"  - Encoding: UTF-8 (valid)")

    return True


def git_operations() -> None:
    """
    Stage, commit, and push the markdown file using git.

    Uses subprocess.run() with list-based arguments to safely execute git commands.
    Commit message follows Conventional Commits specification:
    'feat(165): Create markdown file test-ewmber.md with prose content'

    Raises:
        subprocess.CalledProcessError: If any git command fails (via check=True)
    """
    commit_message = "feat(165): Create markdown file test-ewmber.md with prose content"

    # Stage the file: git add test-ewmber.md
    # Using list-based arguments prevents shell injection attacks
    print("Staging file with 'git add test-ewmber.md'...")
    subprocess.run(["git", "add", "test-ewmber.md"], check=True)
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

        print("\n✓ All phases complete - feature 165 delivered successfully")
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
