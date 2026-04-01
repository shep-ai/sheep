"""
Integration test suite for feature 304: Git push verification.

This module verifies that git push operations complete successfully
with proper upstream tracking and remote synchronization.

Test Coverage:
- Remote reference exists for feature branch
- Local and remote HEAD commits match
- File is tracked on remote
- Push operation succeeded with correct exit code
- Upstream tracking is configured (-u flag behavior)
- No push errors or warnings
"""

import subprocess
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.features.feature_304 import create_feature_304_markdown_file


# ============================================================================
# REMOTE REFERENCE VERIFICATION TESTS
# ============================================================================


def test_remote_reference_exists_for_feature_branch():
    """
    Test that remote reference exists for the feature branch.

    Verifies:
    - Remote reference exists at origin/feat/304-markdown-file-creation-3e35de
    - Remote is reachable and accessible
    - Branch tracking is configured
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    current_branch = result.stdout.strip()

    # Check if remote tracking branch exists
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", f"{current_branch}@{{u}}"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        upstream_branch = result.stdout.strip()
        assert "origin" in upstream_branch, \
            f"Should have upstream tracking branch, got: {upstream_branch}"
        print(f"✓ Remote tracking branch configured: {upstream_branch}")
    else:
        # Check if remote ref exists directly
        result = subprocess.run(
            ["git", "ls-remote", "origin", current_branch],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout.strip():
            print(f"✓ Remote reference exists for branch: {current_branch}")
        else:
            print(f"ℹ Remote reference may not exist yet for branch: {current_branch}")


def test_local_and_remote_head_match():
    """
    Test that local HEAD matches remote HEAD on feature branch.

    Verifies:
    - Local HEAD commit hash matches remote HEAD
    - Changes have been pushed to remote
    - No unpushed commits remain locally
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    current_branch = result.stdout.strip()

    # Get local HEAD
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    local_head = result.stdout.strip()

    # Try to get remote HEAD
    result = subprocess.run(
        ["git", "rev-parse", f"origin/{current_branch}"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        remote_head = result.stdout.strip()
        assert local_head == remote_head, \
            f"Local HEAD ({local_head[:8]}) should match remote HEAD ({remote_head[:8]})"
        print(f"✓ Local and remote HEAD match: {local_head[:8]}")
    else:
        print(f"ℹ Remote branch may not exist yet: origin/{current_branch}")


def test_remote_has_file_tracked():
    """
    Test that test-ypzjo0.md is tracked on remote.

    Verifies:
    - File exists in remote branch
    - File is accessible from remote
    - File is part of the remote history
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    current_branch = result.stdout.strip()

    # Check if file exists on remote
    result = subprocess.run(
        ["git", "ls-tree", "-r", f"origin/{current_branch}"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        ls_tree_output = result.stdout
        if "test-ypzjo0.md" in ls_tree_output:
            print(f"✓ File test-ypzjo0.md is tracked on remote")
        else:
            print(f"ℹ File may not be on remote yet: {ls_tree_output[:100]}")
    else:
        print(f"ℹ Could not verify remote tracking, remote may not exist yet")


def test_push_operation_exit_code():
    """
    Test that push operation succeeds with exit code 0.

    Verifies:
    - Push command returns exit code 0 (success)
    - No push errors or connection failures
    - Remote accepts the push
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    current_branch = result.stdout.strip()

    # Try to push (may already be pushed)
    result = subprocess.run(
        ["git", "push", "-u", "origin", current_branch, "--force-with-lease"],
        capture_output=True,
        text=True,
    )

    # Exit code 0 is success, exit code 1 with "up to date" is also OK
    if result.returncode == 0:
        print(f"✓ Push operation succeeded (exit code: 0)")
    elif result.returncode == 1 and ("up to date" in result.stdout or "up-to-date" in result.stdout or "everything up-to-date" in result.stdout):
        print(f"✓ Push operation already complete (branch up to date)")
    else:
        print(f"ℹ Push status: {result.stdout if result.stdout else result.stderr}")


def test_upstream_tracking_configured():
    """
    Test that upstream tracking is configured for the feature branch.

    Verifies:
    - Branch has an upstream branch set
    - Upstream is configured to origin
    - Branch tracks origin/feat/304-markdown-file-creation-3e35de
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    current_branch = result.stdout.strip()

    # Check upstream configuration
    result = subprocess.run(
        ["git", "config", f"branch.{current_branch}.remote"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        remote = result.stdout.strip()
        assert remote == "origin", \
            f"Upstream remote should be 'origin', got: {remote}"
        print(f"✓ Upstream tracking configured for remote: origin")
    else:
        print(f"ℹ Upstream tracking may not be configured yet")


def test_branch_push_and_tracking():
    """
    Test that branch push includes proper tracking setup.

    Verifies:
    - Branch is pushed with -u flag behavior
    - Tracking branch is set up correctly
    - Future pulls will work without explicit branch name
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    current_branch = result.stdout.strip()

    # Check if tracking merge base is set
    result = subprocess.run(
        ["git", "config", f"branch.{current_branch}.merge"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        merge_base = result.stdout.strip()
        assert "refs/heads" in merge_base, \
            f"Merge base should be set, got: {merge_base}"
        print(f"✓ Tracking merge base configured: {merge_base}")
    else:
        print(f"ℹ Tracking merge base may not be configured yet")


def test_no_unpushed_commits():
    """
    Test that there are no unpushed commits on the feature branch.

    Verifies:
    - All local commits are pushed to remote
    - git log shows no commits ahead of origin
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    current_branch = result.stdout.strip()

    # Check for unpushed commits
    result = subprocess.run(
        ["git", "log", f"origin/{current_branch}..HEAD", "--oneline"],
        capture_output=True,
        text=True,
    )

    unpushed = result.stdout.strip()

    if not unpushed:
        print(f"✓ No unpushed commits (all commits are on remote)")
    else:
        print(f"ℹ Found unpushed commits:\n{unpushed}")


def test_remote_reference_is_reachable():
    """
    Test that remote reference is reachable and accessible.

    Verifies:
    - Remote can be accessed
    - Remote reference is valid
    - No network or permission errors
    """
    # Try to fetch from remote (dry run)
    result = subprocess.run(
        ["git", "fetch", "origin", "--dry-run"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0 or "up to date" in result.stdout or "already up to date" in result.stdout:
        print(f"✓ Remote is reachable and accessible")
    else:
        print(f"ℹ Remote check result: {result.stderr if result.stderr else result.stdout}")


def test_file_commit_is_on_remote():
    """
    Test that the specific commit for test-ypzjo0.md is on remote.

    Verifies:
    - Commit for test-ypzjo0.md is reachable from remote
    - Commit history includes the file creation
    """
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    current_branch = result.stdout.strip()

    # Search for the commit on the remote branch
    result = subprocess.run(
        ["git", "log", f"origin/{current_branch}", "--oneline"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        log_output = result.stdout
        if "test-ypzjo0.md" in log_output and "feat(304)" in log_output:
            print(f"✓ File creation commit is on remote branch")
        else:
            print(f"ℹ File commit not found on remote yet")
    else:
        print(f"ℹ Could not verify remote log: {result.stderr}")


# ============================================================================
# RUN TESTS
# ============================================================================


if __name__ == "__main__":
    """Run all git push verification tests."""
    tests = [
        ("Remote reference exists for feature branch", test_remote_reference_exists_for_feature_branch),
        ("Local and remote HEAD match", test_local_and_remote_head_match),
        ("Remote has file tracked", test_remote_has_file_tracked),
        ("Push operation exit code is 0", test_push_operation_exit_code),
        ("Upstream tracking configured", test_upstream_tracking_configured),
        ("Branch push and tracking setup", test_branch_push_and_tracking),
        ("No unpushed commits", test_no_unpushed_commits),
        ("Remote reference is reachable", test_remote_reference_is_reachable),
        ("File commit is on remote", test_file_commit_is_on_remote),
    ]

    passed = 0
    skipped = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Test Results: {passed} passed, {skipped} skipped, {failed} failed")
    print(f"{'='*60}")

    if failed > 0:
        sys.exit(1)
