"""Git workflow implementation for feature 277.

Handles staging, committing, and pushing the test-yziemx.md file following
the conventional commit format and established git workflow patterns.
"""

import subprocess


def stage_file() -> None:
    """Stage test-yziemx.md in git using git add.

    Raises:
        RuntimeError: If git add command fails
    """
    result = subprocess.run(
        ["git", "add", "test-yziemx.md"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git add failed with exit code {result.returncode}: {result.stderr}"
        )


def create_commit() -> None:
    """Create a git commit with conventional commit message.

    Commit message format: feat(277): create markdown file test-yziemx.md with title and prose content

    Raises:
        RuntimeError: If git commit command fails
    """
    message = "feat(277): create markdown file test-yziemx.md with title and prose content"
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git commit failed with exit code {result.returncode}: {result.stderr}"
        )


def push_to_branch() -> None:
    """Push the commit to the feature branch on remote.

    Uses the explicit feature branch name: feat/277-markdown-file-creation-760875

    Raises:
        RuntimeError: If git push command fails
    """
    result = subprocess.run(
        ["git", "push", "-u", "origin", "feat/277-markdown-file-creation-760875"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git push failed with exit code {result.returncode}: {result.stderr}"
        )


def run_all_git_workflow() -> None:
    """Execute the complete git workflow: stage, commit, and push.

    This is a convenience function that runs all three steps in sequence.

    Raises:
        RuntimeError: If any step fails
    """
    stage_file()
    create_commit()
    push_to_branch()


def verify_file_tracked() -> None:
    """Verify that test-yziemx.md is tracked in git.

    Raises:
        AssertionError: If file is not tracked in git
    """
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
    )
    if "test-yziemx.md" not in result.stdout:
        raise AssertionError("test-yziemx.md is not tracked in git (git ls-files)")


def verify_commit_exists() -> None:
    """Verify that the commit with correct message exists in git log.

    Raises:
        AssertionError: If commit message not found in git log
    """
    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        capture_output=True,
        text=True,
    )
    expected_msg = "feat(277): create markdown file test-yziemx.md with title and prose content"
    if expected_msg not in result.stdout:
        raise AssertionError(
            f"Commit message not found in git log. "
            f"Expected: {expected_msg}\n"
            f"Got: {result.stdout}"
        )


def verify_working_tree_clean() -> None:
    """Verify that the working tree is clean (no uncommitted changes).

    Raises:
        AssertionError: If working tree has uncommitted changes
    """
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        raise AssertionError(
            f"Working tree is not clean. Uncommitted changes:\n{result.stdout}"
        )


def verify_all_git_state() -> None:
    """Execute all git state verification checks.

    Raises:
        AssertionError: If any verification fails
    """
    verify_file_tracked()
    verify_commit_exists()
    verify_working_tree_clean()


if __name__ == "__main__":
    run_all_git_workflow()
    print("✓ Git workflow completed: file staged, committed, and pushed")
    verify_all_git_state()
    print("✓ Git state verification passed")
