"""Git operations tools for agents."""

import subprocess
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


def _run_git(
    args: list[str],
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a git command and return the result."""
    cmd = ["git"] + args
    _logger.debug("git_command", cmd=" ".join(cmd), cwd=str(cwd))
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


class GitStatusInput(BaseModel):
    """Input for git status."""

    repo_path: str = Field(description="Path to the git repository")


class GitStatusTool(BaseTool):
    """Get the current git status of a repository."""

    name: str = "git_status"
    description: str = "Get the current git status showing modified, staged, and untracked files."
    args_schema: type[BaseModel] = GitStatusInput

    def _run(self, repo_path: str) -> str:
        path = Path(repo_path)
        if not path.exists():
            return f"Error: Repository path does not exist: {repo_path}"

        try:
            result = _run_git(["status", "--porcelain", "-b"], path)
            if not result.stdout.strip():
                return "Working tree is clean, no changes."
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Git error: {e.stderr}"


class GitDiffInput(BaseModel):
    """Input for git diff."""

    repo_path: str = Field(description="Path to the git repository")
    file_path: str | None = Field(default=None, description="Optional specific file to diff")
    staged: bool = Field(default=False, description="Show staged changes only")


class GitDiffTool(BaseTool):
    """Show git diff of changes."""

    name: str = "git_diff"
    description: str = "Show the diff of changes in the repository."
    args_schema: type[BaseModel] = GitDiffInput

    def _run(
        self,
        repo_path: str,
        file_path: str | None = None,
        staged: bool = False,
    ) -> str:
        path = Path(repo_path)
        if not path.exists():
            return f"Error: Repository path does not exist: {repo_path}"

        try:
            args = ["diff"]
            if staged:
                args.append("--staged")
            if file_path:
                args.append("--")
                args.append(file_path)

            result = _run_git(args, path)
            if not result.stdout.strip():
                return "No changes to show."
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Git error: {e.stderr}"


class GitLogInput(BaseModel):
    """Input for git log."""

    repo_path: str = Field(description="Path to the git repository")
    count: int = Field(default=10, description="Number of commits to show")
    oneline: bool = Field(default=True, description="Use oneline format")


class GitLogTool(BaseTool):
    """Show git commit history."""

    name: str = "git_log"
    description: str = "Show recent commit history."
    args_schema: type[BaseModel] = GitLogInput

    def _run(
        self,
        repo_path: str,
        count: int = 10,
        oneline: bool = True,
    ) -> str:
        path = Path(repo_path)
        if not path.exists():
            return f"Error: Repository path does not exist: {repo_path}"

        try:
            args = ["log", f"-{count}"]
            if oneline:
                args.append("--oneline")

            result = _run_git(args, path)
            return result.stdout if result.stdout.strip() else "No commits yet."
        except subprocess.CalledProcessError as e:
            return f"Git error: {e.stderr}"


class GitCreateBranchInput(BaseModel):
    """Input for creating a git branch."""

    repo_path: str = Field(description="Path to the git repository")
    branch_name: str = Field(description="Name of the branch to create")
    base_branch: str | None = Field(
        default=None, description="Base branch to create from (default: current branch)"
    )


class GitCreateBranchTool(BaseTool):
    """Create a new git branch."""

    name: str = "git_create_branch"
    description: str = "Create a new git branch from the current or specified base branch."
    args_schema: type[BaseModel] = GitCreateBranchInput

    def _run(
        self,
        repo_path: str,
        branch_name: str,
        base_branch: str | None = None,
    ) -> str:
        path = Path(repo_path)
        if not path.exists():
            return f"Error: Repository path does not exist: {repo_path}"

        try:
            # Fetch latest if there's a remote
            _run_git(["fetch", "--all"], path, check=False)

            args = ["checkout", "-b", branch_name]
            if base_branch:
                args.append(base_branch)

            _run_git(args, path)
            return f"Created and switched to branch: {branch_name}"
        except subprocess.CalledProcessError as e:
            return f"Git error: {e.stderr}"


class GitCheckoutInput(BaseModel):
    """Input for git checkout."""

    repo_path: str = Field(description="Path to the git repository")
    branch_name: str = Field(description="Name of the branch to checkout")


class GitCheckoutTool(BaseTool):
    """Checkout a git branch."""

    name: str = "git_checkout"
    description: str = "Switch to an existing git branch."
    args_schema: type[BaseModel] = GitCheckoutInput

    def _run(self, repo_path: str, branch_name: str) -> str:
        path = Path(repo_path)
        if not path.exists():
            return f"Error: Repository path does not exist: {repo_path}"

        try:
            _run_git(["checkout", branch_name], path)
            return f"Switched to branch: {branch_name}"
        except subprocess.CalledProcessError as e:
            return f"Git error: {e.stderr}"


class GitCommitInput(BaseModel):
    """Input for git commit."""

    repo_path: str = Field(description="Path to the git repository")
    message: str = Field(description="Commit message")
    add_all: bool = Field(default=True, description="Stage all changes before commit")


class GitCommitTool(BaseTool):
    """Create a git commit."""

    name: str = "git_commit"
    description: str = "Stage changes and create a git commit."
    args_schema: type[BaseModel] = GitCommitInput

    def _run(
        self,
        repo_path: str,
        message: str,
        add_all: bool = True,
    ) -> str:
        path = Path(repo_path)
        if not path.exists():
            return f"Error: Repository path does not exist: {repo_path}"

        try:
            if add_all:
                _run_git(["add", "-A"], path)

            result = _run_git(["commit", "-m", message], path)
            return f"Committed: {message}\n{result.stdout}"
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in e.stderr.lower():
                return "Nothing to commit, working tree clean."
            return f"Git error: {e.stderr}"


class GitPushInput(BaseModel):
    """Input for git push."""

    repo_path: str = Field(description="Path to the git repository")
    remote: str = Field(default="origin", description="Remote name")
    branch: str | None = Field(default=None, description="Branch to push (default: current branch)")
    set_upstream: bool = Field(default=True, description="Set upstream tracking reference")


class GitPushTool(BaseTool):
    """Push changes to remote repository."""

    name: str = "git_push"
    description: str = "Push committed changes to the remote repository."
    args_schema: type[BaseModel] = GitPushInput

    def _run(
        self,
        repo_path: str,
        remote: str = "origin",
        branch: str | None = None,
        set_upstream: bool = True,
    ) -> str:
        path = Path(repo_path)
        if not path.exists():
            return f"Error: Repository path does not exist: {repo_path}"

        try:
            # Get current branch if not specified
            if branch is None:
                result = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], path)
                branch = result.stdout.strip()

            args = ["push"]
            if set_upstream:
                args.extend(["-u", remote, branch])
            else:
                args.extend([remote, branch])

            result = _run_git(args, path)
            return f"Pushed to {remote}/{branch}\n{result.stderr}"
        except subprocess.CalledProcessError as e:
            return f"Git error: {e.stderr}"


class GitWorktreeInput(BaseModel):
    """Input for git worktree operations."""

    repo_path: str = Field(description="Path to the main git repository")
    worktree_path: str = Field(description="Path where worktree should be created")
    branch_name: str = Field(description="Branch name for the worktree")
    base_branch: str = Field(default="main", description="Base branch to create worktree from")


class GitWorktreeTool(BaseTool):
    """Manage git worktrees for isolated development."""

    name: str = "git_worktree"
    description: str = (
        "Create a git worktree for isolated development. "
        "Worktrees allow working on multiple branches simultaneously in separate directories."
    )
    args_schema: type[BaseModel] = GitWorktreeInput

    def _run(
        self,
        repo_path: str,
        worktree_path: str,
        branch_name: str,
        base_branch: str = "main",
    ) -> str:
        path = Path(repo_path)
        worktree = Path(worktree_path)

        if not path.exists():
            return f"Error: Repository path does not exist: {repo_path}"

        if worktree.exists():
            return f"Error: Worktree path already exists: {worktree_path}"

        try:
            # Fetch latest
            _run_git(["fetch", "--all"], path, check=False)

            # Create worktree with new branch
            _run_git(
                ["worktree", "add", "-b", branch_name, str(worktree), base_branch],
                path,
            )
            return f"Created worktree at {worktree_path} with branch {branch_name}"
        except subprocess.CalledProcessError as e:
            return f"Git error: {e.stderr}"
