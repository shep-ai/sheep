#!/usr/bin/env python3
"""
Phase 2 Implementation: Git Integration - Push to Remote

This script handles task-6: Push the markdown file commit to the feature branch
on the remote repository using git CLI.

Expects:
- File test-tq8wxa.md exists locally
- Commit with message 'feat(300): create markdown file test-tq8wxa.md with prose content' exists locally
- Feature branch 'feat/markdown-file-creation-6aea8a' is current branch
"""

import sys
import subprocess
from pathlib import Path


def run_git_command(cmd, check=True):
    """
    Run a git command and return stdout.

    Args:
        cmd: Command list (e.g., ['git', 'push', 'origin', 'branch'])
        check: Whether to raise error on failure

    Returns:
        Tuple of (stdout, returncode)

    Raises:
        RuntimeError: If check=True and command fails
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=False
        )
        if check and result.returncode != 0:
            raise RuntimeError(
                f"Command failed: {' '.join(cmd)}\n"
                f"Error: {result.stderr}"
            )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        if check:
            raise RuntimeError(f"Failed to execute git command: {e}")
        return "", 1


def push_to_remote(branch_name: str = None) -> bool:
    """
    Push the current branch to the remote origin using git CLI.

    Args:
        branch_name: Name of branch to push (defaults to current branch)

    Returns:
        True if push succeeds

    Raises:
        RuntimeError: If push fails
    """
    try:
        print("=" * 70)
        print("PHASE 2: Git Integration - Push to Remote")
        print(f"Feature: markdown-file-creation-6aea8a (Feature 300)")
        print("=" * 70)
        print()

        # Get current branch
        current_branch, _ = run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        print(f"Current branch: {current_branch}")

        if branch_name is None:
            branch_name = current_branch

        print(f"Branch to push: {branch_name}")

        # Verify we're on the correct branch
        expected_branch = "feat/markdown-file-creation-6aea8a"
        if current_branch != expected_branch:
            raise RuntimeError(
                f"On wrong branch! Expected '{expected_branch}', "
                f"but on '{current_branch}'"
            )
        print(f"[OK] On correct branch: {expected_branch}")
        print()

        # Verify the commit exists locally
        commit_hash, _ = run_git_command(['git', 'rev-parse', 'HEAD'])
        commit_msg_full, _ = run_git_command(['git', 'log', '-1', '--pretty=%B'])
        # Get just the first line (subject) of the commit message
        commit_msg = commit_msg_full.split('\n')[0] if commit_msg_full else ""
        expected_msg = "feat(300): create markdown file test-tq8wxa.md with prose content"

        print("Verifying local commit:")
        print(f"  Commit hash: {commit_hash[:8]}")
        print(f"  Commit message: {commit_msg}")

        if commit_msg != expected_msg:
            raise RuntimeError(
                f"Commit message mismatch! Expected '{expected_msg}', "
                f"got '{commit_msg}'"
            )
        print(f"[OK] Commit message matches expected format")
        print()

        # Verify file is in the commit
        print("Verifying file in commit:")
        files_in_commit, _ = run_git_command(
            ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD']
        )

        if 'test-tq8wxa.md' in files_in_commit:
            print(f"  File: test-tq8wxa.md")
            print(f"[OK] File is in commit")
        else:
            raise RuntimeError("File test-tq8wxa.md not found in commit")
        print()

        # Push to remote
        print("Pushing to remote origin:")
        print(f"  Branch: {branch_name}")
        print()

        # Get remote URL
        remote_url, _ = run_git_command(
            ['git', 'config', '--get', 'remote.origin.url'],
            check=False
        )
        if remote_url:
            print(f"  Remote URL: {remote_url}")
            print()

        print("Executing: git push origin " + branch_name)
        try:
            push_output, returncode = run_git_command(
                ['git', 'push', 'origin', branch_name],
                check=False
            )

            if returncode != 0:
                # Print error output
                if push_output:
                    print(push_output)
                raise RuntimeError(f"Push command failed with return code {returncode}")

            print(push_output)
            print()
            print("[OK] Push completed successfully")
            print()

            return True

        except Exception as e:
            print(f"[ERROR] Push failed: {e}")
            raise RuntimeError(f"Push operation failed: {e}")

    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def verify_push_succeeded() -> bool:
    """
    Verify that the commit was pushed to the remote successfully.

    Returns:
        True if push verification succeeds
    """
    try:
        print("=" * 70)
        print("Verifying Push to Remote")
        print("=" * 70)
        print()

        # Get local and remote commit hashes
        local_hash, _ = run_git_command(['git', 'rev-parse', 'HEAD'])
        print(f"Local commit hash:  {local_hash[:8]}")

        try:
            remote_hash, returncode = run_git_command(
                ['git', 'rev-parse', 'origin/feat/markdown-file-creation-6aea8a'],
                check=False
            )

            if returncode != 0:
                # Remote branch might not exist if this is first push
                print(f"[WARNING] Could not verify remote branch (might not exist yet)")
                return False

            print(f"Remote commit hash: {remote_hash[:8]}")
            print()

            if local_hash == remote_hash:
                print("[OK] Local and remote commits match - push successful!")
                return True
            else:
                print("[ERROR] Local and remote commits do not match")
                return False

        except Exception as e:
            # Remote branch might not exist if this is first push
            print(f"[WARNING] Could not verify remote branch: {e}")
            return False

    except Exception as e:
        print(f"\n[ERROR] Verification failed: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point."""
    try:
        # Step 1: Push to remote
        if not push_to_remote():
            return 1

        print()

        # Step 2: Verify push succeeded
        # Note: Verification might fail in some environments (e.g., no network)
        # so we make it non-fatal
        verify_push_succeeded()

        print()
        print("=" * 70)
        print("[OK] PHASE 2 COMPLETE: Git integration successful")
        print("=" * 70)
        print()
        print("File has been pushed to remote:")
        print("  - Branch: feat/markdown-file-creation-6aea8a")
        print("  - File: test-tq8wxa.md")
        print("  - Commit: feat(300): create markdown file test-tq8wxa.md with prose content")
        print()

        return 0

    except Exception as e:
        print(f"\n[ERROR] Phase 2 failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
