"""Git workflow implementation for feature 132.

Handles staging, committing, and pushing the test-fz0c6t.md file following
the conventional commit format and established git workflow patterns.
"""

import subprocess


def stage_file() -> None:
    """Stage test-fz0c6t.md in git using git add.

    Raises:
        RuntimeError: If git add command fails
    """
    result = subprocess.run(
        ["git", "add", "test-fz0c6t.md"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git add failed with exit code {result.returncode}: {result.stderr}"
        )


def create_commit() -> None:
    """Create a git commit with conventional commit message.

    Commit message format: feat(132): Create markdown file test-fz0c6t.md

    Raises:
        RuntimeError: If git commit command fails
    """
    message = "feat(132): Create markdown file test-fz0c6t.md"
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

    Uses -u flag to set upstream tracking on current branch.

    Raises:
        RuntimeError: If git push command fails
    """
    result = subprocess.run(
        ["git", "push", "-u", "origin", "HEAD"],
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


if __name__ == "__main__":
    run_all_git_workflow()
    print("✓ Git workflow completed: file staged, committed, and pushed")
