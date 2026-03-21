"""Git workflow implementation for feature 142.

Handles staging, committing, and pushing the test-hqbiuy.md file following
the conventional commit format and established git workflow patterns.
"""

import subprocess


def stage_file(filename: str) -> None:
    """Stage file in git using git add.

    Args:
        filename: Name of the file to stage (e.g., "test-hqbiuy.md")

    Raises:
        RuntimeError: If git add command fails
    """
    result = subprocess.run(
        ["git", "add", filename],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git add failed with exit code {result.returncode}: {result.stderr}"
        )


def create_commit(message: str) -> None:
    """Create a git commit with conventional commit message.

    Args:
        message: Commit message following conventional commits format
                (e.g., "feat(142): Create markdown file test-hqbiuy.md with specification")

    Raises:
        RuntimeError: If git commit command fails
    """
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git commit failed with exit code {result.returncode}: {result.stderr}"
        )


def push_to_remote(branch_name: str) -> None:
    """Push the commit to the feature branch on remote.

    Args:
        branch_name: Feature branch name to push to (e.g., "feat/markdown-file-creation-b65b0e")

    Raises:
        RuntimeError: If git push command fails
    """
    result = subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git push failed with exit code {result.returncode}: {result.stderr}"
        )


def run_all_git_workflow(
    filename: str, message: str, branch_name: str
) -> None:
    """Execute the complete git workflow: stage, commit, and push.

    Args:
        filename: File to stage
        message: Commit message
        branch_name: Remote branch to push to

    Raises:
        RuntimeError: If any step fails
    """
    stage_file(filename)
    create_commit(message)
    push_to_remote(branch_name)


if __name__ == "__main__":
    run_all_git_workflow(
        "test-hqbiuy.md",
        "feat(142): Create markdown file test-hqbiuy.md with specification",
        "feat/markdown-file-creation-b65b0e",
    )
    print("✓ Git workflow completed: file staged, committed, and pushed")
