#!/usr/bin/env python3
"""
Create a markdown file (test-2kb5i9.md) with deterministic prose content.

This script implements feature 174 by orchestrating the markdown file creation workflow:
1. Seed Python's random module with feature number 174 for deterministic content generation
2. Generate markdown content with H1 heading and 2-3 sentences using deterministic approach
3. Write file to repository root with UTF-8 encoding and Unix LF line endings
4. Validate complete file structure, encoding, and format requirements
5. Stage, commit with conventional message (feat(174)), and push to git

The deterministic seeding ensures:
- Same content generated on repeated runs (reproducible testing)
- Consistent git history across builds
- Testable, debuggable implementation

Follows the established pattern from prior markdown file creation features.
"""

import random
import subprocess
import sys
from pathlib import Path


# Feature configuration
FEATURE_NUMBER = 174
FILENAME = "test-2kb5i9.md"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): create markdown file {FILENAME} with prose content"


def generate_deterministic_content(seed: int) -> str:
    """
    Generate deterministic markdown content seeded with feature number.

    Args:
        seed: Feature number to seed randomness (174)

    Returns:
        Markdown content string with H1 heading, blank line, and 2-3 sentences
    """
    # Seed random for deterministic generation
    random.seed(seed)

    # Title options (seed selects one)
    titles = [
        "The Power of Consistency",
        "Building with Intention",
        "The Foundation of Excellence",
        "Creating Meaningful Impact",
        "The Art of Simplicity",
    ]

    # Prose options (seed selects combination) - expanded for 300+ byte range
    prose_parts = [
        "Excellence emerges through deliberate practice and unwavering commitment to quality in all endeavors, both great and small.",
        "Consistency breeds confidence and transforms aspirations into tangible achievements through persistent effort and dedication to purpose.",
        "Mastery requires embracing challenges as opportunities for growth and refinement, learning from both successes and setbacks along the way.",
        "Simplicity achieved through careful design yields elegant and powerful solutions that resonate with clarity and intention.",
        "Intentional effort, combined with clear vision and purposeful action, unlocks extraordinary potential and meaningful possibilities.",
    ]

    # Use seed to deterministically select title and prose
    title_idx = seed % len(titles)
    prose_idx = (seed * 3) % len(prose_parts)

    title = titles[title_idx]
    sentence1 = prose_parts[prose_idx]
    sentence2 = prose_parts[(prose_idx + 1) % len(prose_parts)]
    sentence3 = prose_parts[(prose_idx + 2) % len(prose_parts)]

    # Construct markdown with H1 heading, blank line, and prose
    content = f"# {title}\n\n{sentence1} {sentence2} {sentence3}\n"
    return content


def create_file() -> Path:
    """
    Create the markdown file with proper UTF-8 encoding and LF line endings.

    Returns:
        Path: The pathlib.Path object pointing to the created file

    Raises:
        IOError: If file creation fails
    """
    print(f"Generating deterministic content (seed={FEATURE_NUMBER})...")
    content = generate_deterministic_content(FEATURE_NUMBER)

    # Write the file using pathlib with explicit UTF-8 encoding
    # This ensures: UTF-8 without BOM, Unix LF line endings, platform independence
    filepath = Path(FILENAME)
    filepath.write_bytes(content.encode('utf-8'))

    return filepath


def validate_file(filepath: Path) -> bool:
    """
    Validate the markdown file structure, encoding, and size.

    Args:
        filepath: Path object pointing to the markdown file

    Returns:
        bool: True if all validations pass

    Raises:
        AssertionError: If any validation fails
    """
    # Check file exists
    assert filepath.exists(), f"File {filepath} does not exist"

    # Check file size is in typical range (300-800 bytes)
    file_size = filepath.stat().st_size
    assert 300 < file_size < 800, (
        f"File size {file_size} bytes is outside typical range (300-800 bytes)"
    )

    # Read and validate content
    content = filepath.read_text(encoding='utf-8')

    # Check for H1 heading at start
    assert content.startswith('# '), "File must start with H1 heading (# )"

    # Check for blank line after heading
    assert '\n\n' in content, "File must contain blank line after heading"

    # Check for prose content
    parts = content.split('\n\n', 1)
    assert len(parts) == 2, "File structure should be: heading, blank line, prose"
    prose = parts[1].strip()
    assert len(prose) > 0, "File must contain prose content"

    # Check for trailing newline
    assert content.endswith('\n'), "File must end with trailing newline"

    # Verify UTF-8 encoding (no BOM, valid UTF-8)
    binary_content = filepath.read_bytes()
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File must not have UTF-8 BOM"
    try:
        binary_content.decode('utf-8')
    except UnicodeDecodeError:
        raise AssertionError("File must be valid UTF-8")

    # Check for CRLF line endings (should use LF)
    assert b'\r\n' not in binary_content, "File must use LF line endings, not CRLF"

    return True


def git_operations() -> None:
    """
    Stage, commit, and push the markdown file to git.

    Raises:
        subprocess.CalledProcessError: If any git command fails
    """
    # Stage the file
    print("Staging file with git add...")
    subprocess.run(["git", "add", FILENAME], check=True)
    print("[OK] File staged")

    # Commit the file
    print(f"Committing with message: {COMMIT_MESSAGE}")
    subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
    print("[OK] File committed")

    # Push to remote
    print("Pushing to remote origin...")
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
    print("[OK] Pushed to remote")


def main() -> None:
    """
    Main entry point: orchestrate file creation, validation, and git operations.

    Exits with status code 0 on success, 1 on failure.
    """
    try:
        # Step 1: File creation
        print("Creating markdown file...")
        filepath = create_file()
        print(f"[OK] File created: {filepath}")

        # Step 2: Validation
        print("\nValidating file structure and format...")
        validate_file(filepath)
        print("[OK] File validation passed")
        print("  - H1 heading present")
        print("  - Blank line separator present")
        print("  - Prose content present")
        print("  - UTF-8 encoding (no BOM)")
        print("  - Unix LF line endings")
        print("  - Trailing newline present")
        print(f"  - Size: {filepath.stat().st_size} bytes")

        # Step 3: Git integration
        print("\nPerforming git operations...")
        git_operations()

        print("\n" + "=" * 60)
        print("[OK] WORKFLOW COMPLETE")
        print("=" * 60)
        print(f"File: {FILENAME}")
        print(f"Commit: {COMMIT_MESSAGE}")
        sys.exit(0)

    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Git command failed: {e.cmd}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        sys.exit(1)
    except AssertionError as e:
        print(f"\n[ERROR] Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
