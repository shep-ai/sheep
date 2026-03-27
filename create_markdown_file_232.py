#!/usr/bin/env python3
"""
Create markdown file test-qfbu3q.md with title and prose content.

This script creates a markdown file in the repository root following the
established pattern from features 151-231. The file contains an H1 heading,
a blank line, and 2-3 sentences of coherent prose.

File format:
  - Line 1: H1 markdown heading (# Title)
  - Line 2: Blank line
  - Lines 3+: 2-3 sentences of prose content
  - Encoding: UTF-8 without BOM
  - Line endings: Unix LF (\n)
  - Size: 300-600 bytes
"""

from pathlib import Path
import subprocess
import sys


# Markdown file content
TITLE = "The Power of Curiosity"

PROSE = (
    "Curiosity is the driving force behind human discovery and progress, "
    "pushing us to question the world around us and seek deeper understanding. "
    "It fosters innovation and creativity by encouraging us to explore beyond "
    "conventional boundaries and challenge existing assumptions. Through curiosity, "
    "we unlock new possibilities and transform our perspective on life and knowledge."
)

# Target file
TARGET_FILE = "test-qfbu3q.md"
FEATURE_BRANCH = "feat/markdown-content-file-dac83b"


def create_markdown_file():
    """Create markdown file with title and prose content."""
    file_path = Path(TARGET_FILE)

    # Defensive check: prevent overwriting existing files
    if file_path.exists():
        raise FileExistsError(
            f"File '{TARGET_FILE}' already exists. "
            "Delete it first if you want to recreate it."
        )

    # Construct file content: H1 heading + blank line + prose + final newline
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Write file with explicit UTF-8 encoding and Unix line endings
    # newline="\n" ensures LF line endings on all platforms (including Windows)
    file_path.write_text(content, encoding="utf-8", newline="\n")

    print(f"[OK] Created {TARGET_FILE}")
    print(f"  - File size: {len(content)} bytes")
    print(f"  - Encoding: UTF-8")
    print(f"  - Line endings: LF (Unix)")


def git_operations():
    """Stage, commit, and push the file to the feature branch."""
    try:
        # Stage the file
        subprocess.run(
            ["git", "add", TARGET_FILE],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[OK] Staged {TARGET_FILE} with git add")

        # Create conventional commit
        commit_message = f"feat(232): Create markdown file {TARGET_FILE} with prose content"
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[OK] Created commit: {commit_message}")

        # Push to feature branch
        subprocess.run(
            ["git", "push", "-u", "origin", FEATURE_BRANCH],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[OK] Pushed to branch {FEATURE_BRANCH}")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git operation failed: {e}", file=sys.stderr)
        print(f"  stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point: create file and handle git operations."""
    try:
        print("Creating markdown file...")
        create_markdown_file()

        print("\nRunning git operations...")
        git_operations()

        print("\n[OK] Feature 232 implementation complete!")
        return 0

    except FileExistsError as e:
        print(f"[ERROR] Error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"[ERROR] File I/O error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
