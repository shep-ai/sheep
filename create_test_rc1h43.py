#!/usr/bin/env python3
"""
Git integration for markdown file test-rc1h43.md.

This script demonstrates git workflow operations:
1. Staging file with git add
2. Committing with conventional commit message format
3. Pushing to remote feature branch
"""

import subprocess
import sys

# Filename being committed
FILENAME = "test-rc1h43.md"


def stage_file(filename):
    """Stage file with git add."""
    try:
        subprocess.run(["git", "add", filename], check=True)
        print(f"✓ File staged: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Git add failed: {e}", file=sys.stderr)
        raise


def commit_file(filename):
    """Commit file with conventional commit message."""
    message = f"feat(105): markdown file creation {filename}"
    try:
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True
        )
        print(f"✓ File committed with message: {message}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Git commit failed: {e}", file=sys.stderr)
        raise


def push_commit():
    """Push commit to remote origin."""
    try:
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
        print("✓ Commit pushed to remote origin")
    except subprocess.CalledProcessError as e:
        print(f"✗ Git push failed: {e}", file=sys.stderr)
        raise


def git_workflow(filename):
    """Execute complete git workflow: stage, commit, push."""
    try:
        stage_file(filename)
        commit_file(filename)
        push_commit()
        return 0
    except Exception:
        return 1


def main_phase3():
    """Main entry point for phase 3: git integration."""
    try:
        result = git_workflow(FILENAME)
        if result == 0:
            print(f"\n✓ Feature 105 Phase 3 complete: {FILENAME} staged, committed, and pushed")
        return result
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main_phase3())
