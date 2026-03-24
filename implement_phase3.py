#!/usr/bin/env python3
"""
Implementation of Feature 202 Phase 3: Git Integration

This script executes the three Phase 3 tasks:
1. Task 7: Stage file with git add
2. Task 8: Create commit with conventional commit message
3. Task 9: Push commit to feature branch
"""

import subprocess
import sys
from pathlib import Path

from src.create_markdown import (
    stage_and_commit_file,
    push_to_feature_branch,
)


def main():
    """Execute Phase 3 git integration tasks."""

    filename = "test-1u4gfg.md"
    commit_message = "feat(202): Create markdown file test-1u4gfg.md with title and prose content"
    branch_name = "feat/202-markdown-file-creation-05a473"

    print("\n" + "="*70)
    print("Phase 3: Git Integration")
    print("="*70)

    # Verify file exists
    if not Path(filename).exists():
        print(f"✗ Error: {filename} does not exist")
        return 1

    print(f"✓ File exists: {filename}")

    # Task 7: Stage file with git add
    print("\nTask 7: Stage file with git add")
    print("-" * 70)

    try:
        result = subprocess.run(
            ['git', 'add', filename],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✓ Staged file: git add {filename}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to stage file: {e.stderr or e.stdout}")
        return 1

    # Task 8: Create commit with conventional message
    print("\nTask 8: Create commit with conventional message")
    print("-" * 70)

    try:
        result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print(f"✓ Created commit: {commit_message}")
        elif "nothing to commit" in result.stderr or "nothing to commit" in result.stdout:
            print(f"✓ File already committed: {commit_message}")
        else:
            print(f"✗ Failed to create commit: {result.stderr or result.stdout}")
            return 1
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create commit: {e.stderr or e.stdout}")
        return 1

    # Task 9: Push commit to feature branch
    print("\nTask 9: Push commit to feature branch")
    print("-" * 70)

    try:
        # Using the module function with retry logic
        push_result = push_to_feature_branch(branch_name=branch_name)

        if push_result['success']:
            print(f"✓ Pushed to feature branch: {branch_name}")
        else:
            # If push failed, try manual push
            print(f"! Attempting manual push to {branch_name}...")
            result = subprocess.run(
                ['git', 'push', '-u', 'origin', branch_name],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"✓ Pushed to feature branch: {branch_name}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to push to branch: {e.stderr or e.stdout}")
        return 1
    except Exception as e:
        print(f"✗ Unexpected error during push: {e}")
        return 1

    print("\n" + "="*70)
    print("✓ Phase 3: Git Integration - Complete")
    print("="*70 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
