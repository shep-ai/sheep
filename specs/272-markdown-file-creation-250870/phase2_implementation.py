#!/usr/bin/env python3
"""
Phase 2 Implementation: Git Integration & Push (Feature 272).

This script implements the two tasks of phase 2:
1. Stage and commit file with conventional commit message (task-4)
2. Push commit to feature branch with upstream tracking (task-5)

The script uses existing utilities from sheep.content_generators:
- commit_markdown_file() - Stage and commit with conventional message
- push_markdown_file() - Push to remote with upstream tracking

Phase 1 (content generation and file creation) must be complete before this phase.
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Change working directory to repository root
import os
os.chdir(Path(__file__).parent.parent.parent)

from sheep.content_generators import (
    commit_markdown_file,
    push_markdown_file,
    validate_markdown_file,
)
from sheep.observability.logging import get_logger

logger = get_logger(__name__)

FEATURE_FILENAME = "test-6fioxo.md"
FEATURE_NUMBER = 272
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): create markdown file {FEATURE_FILENAME} with title and prose content"


def task4_commit_file():
    """
    Task 4: Stage and commit file with conventional commit message.

    Uses GitCommitTool to stage the markdown file via git add,
    then commits with conventional commit message following the pattern:
    "feat(272): create markdown file test-6fioxo.md with title and prose content"

    Returns:
        str: Commit result message from GitCommitTool

    Raises:
        ValueError: If file doesn't exist or content is invalid
        Exception: If git commit fails
    """
    print("=" * 70)
    print("TASK 4: Stage and commit file with conventional commit message")
    print("=" * 70)
    print()
    print(f"Staging and committing file: {FEATURE_FILENAME}")
    print(f"- Branch: feat/{FEATURE_NUMBER}-markdown-file-creation-250870")
    print(f"- Commit message: {COMMIT_MESSAGE}")
    print()

    try:
        # Verify file exists
        repo_root = Path.cwd()
        filepath = repo_root / FEATURE_FILENAME

        if not filepath.exists():
            raise FileNotFoundError(f"File {filepath} does not exist")

        print(f"Verifying file exists: {filepath}")
        assert filepath.exists(), f"File {filepath} should exist"
        assert filepath.is_file(), f"Path {filepath} should be a file"
        print("[OK] File verification passed")
        print()

        # Validate file before commit
        print("Validating file before commit...")
        validate_markdown_file(str(filepath))
        print("[OK] File validation passed")
        print()

        # Read content for commit
        content = filepath.read_text(encoding="utf-8")

        # Call commit_markdown_file with custom message
        print("Calling commit_markdown_file() with custom message...")
        result = commit_markdown_file(
            filepath=str(filepath),
            content=content,
            repo_path=str(repo_root),
            custom_message=COMMIT_MESSAGE,
        )

        print(f"[PASS] Task 4 PASSED: File committed successfully")
        print(f"  - Commit message: {COMMIT_MESSAGE}")
        print(f"  - Result: {result}")
        print()

        return result

    except Exception as e:
        print(f"[FAIL] Task 4 FAILED: {e}")
        raise


def task5_push_file():
    """
    Task 5: Push commit to feature branch with upstream tracking.

    Uses GitPushTool to push the committed file to the remote feature branch
    with upstream tracking (-u flag) to set the local branch tracking.

    Returns:
        str: Push result message from GitPushTool

    Raises:
        Exception: If git push fails
    """
    print("=" * 70)
    print("TASK 5: Push commit to feature branch with upstream tracking")
    print("=" * 70)
    print()
    print("Pushing commit to remote feature branch")
    print("- Remote: origin")
    print("- Upstream tracking: enabled (-u flag)")
    print()

    try:
        repo_root = Path.cwd()

        # Call push_markdown_file
        print("Calling push_markdown_file() to push with upstream tracking...")
        result = push_markdown_file(repo_path=str(repo_root), remote="origin")

        print(f"[OK] Task 5 PASSED: Commit pushed successfully")
        print(f"  - Result: {result}")
        print()

        return result

    except Exception as e:
        print(f"[FAIL] Task 5 FAILED: {e}")
        raise


def main():
    """
    Main entry point: orchestrate phase 2 tasks.

    Executes both tasks of phase 2 in sequence:
    1. Stage and commit markdown file with conventional message
    2. Push to remote feature branch with upstream tracking

    Phase 2 completes the feature implementation.

    Exits with status code 0 on success, 1 on failure.
    """
    print()
    print("=" * 70)
    print("Feature 272: Markdown File Creation - Phase 2 Implementation".center(70))
    print("Git Integration & Push".center(70))
    print("=" * 70)
    print()

    try:
        # Task 4: Commit file
        commit_result = task4_commit_file()

        # Task 5: Push file
        push_result = task5_push_file()

        # All tasks passed
        print("=" * 70)
        print("[OK] PHASE 2 COMPLETE: All tasks passed successfully")
        print("=" * 70)
        print()
        print("Summary:")
        print(f"  - Staged markdown file: {FEATURE_FILENAME}")
        print(f"  - Commit message: {COMMIT_MESSAGE}")
        print(f"  - Pushed to remote feature branch: feat/{FEATURE_NUMBER}-markdown-file-creation-250870")
        print(f"  - Upstream tracking: enabled")
        print()
        print("Next steps:")
        print("  - Feature 272 implementation complete")
        print("  - File is committed and pushed to remote")
        print()

        return 0

    except Exception as e:
        print()
        print("=" * 70)
        print("[FAIL] PHASE 2 FAILED: Implementation could not complete")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
