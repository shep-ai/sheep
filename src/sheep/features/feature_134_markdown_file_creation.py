"""Implementation for feature 134: Create markdown file test-an35bo.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 133 preceding features (001-133). The file is created with:
- Exact filename: test-an35bo.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 400-600 bytes
- Git staging, commit, and push operations
"""

from pathlib import Path
import subprocess

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 134
FEATURE_NAME = "markdown-file-creation-1d839a"
MARKDOWN_FILENAME = "test-an35bo.md"

# Deterministic markdown content for feature 134
# This follows the established pattern: H1 heading + 2-3 sentences of prose
MARKDOWN_CONTENT = """# Automated Implementation and Testing

Feature 134 demonstrates automated markdown file creation capabilities within the Sheep platform test suite. This implementation validates the complete workflow including file creation, git staging, conventional commit formatting, and remote repository push operations. The feature follows established patterns from 133 preceding markdown file creation features.
"""

def _run_git(args: list[str], cwd: str) -> subprocess.CompletedProcess:
    """Run a git command and return the result."""
    cmd = ["git"] + args
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def _validate_markdown_content(content: str) -> None:
    """Validate markdown content meets basic format requirements."""
    if not content or not content.strip():
        raise ValueError("Content is empty")

    lines = content.split("\n")
    if not lines[0].startswith("# "):
        raise ValueError("Content must start with H1 heading (# )")

    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank (separator after heading)")

    # Count sentences (periods)
    prose = "\n".join(lines[2:]).strip()
    sentence_count = prose.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(f"Content must have 2-3 sentences, found {sentence_count}")

    _logger.info("Markdown content validation passed")


def _write_markdown_file(content: str, filename: str, repo_path: str) -> str:
    """Write markdown content to file with UTF-8 encoding and LF line endings."""
    repo_root = Path(repo_path)
    file_path = repo_root / filename

    _logger.info(f"Writing markdown file to {file_path}")

    # Write with explicit UTF-8 encoding and LF line endings
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    if not file_path.exists():
        raise OSError(f"File was not created: {file_path}")

    file_size = file_path.stat().st_size
    if file_size == 0:
        raise OSError(f"File is empty: {file_path}")

    if not (400 <= file_size <= 600):
        raise ValueError(f"File size {file_size} not in range [400, 600]")

    _logger.info(f"Successfully wrote markdown file: {file_path} ({file_size} bytes)")
    return str(file_path)


def create_feature_134_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 134.

    Orchestrates the complete workflow:
    1. Validate deterministic markdown content (H1 heading + 2-3 sentences)
    2. Write file to repository root with UTF-8 encoding and LF line endings
    3. Stage and commit with conventional message
    4. Push to remote feature branch

    Args:
        repo_path: Path to git repository (defaults to current directory).

    Returns:
        Dictionary containing:
        - filepath: Full path to created file
        - content: Markdown content
        - commit_message: Git commit message used
        - push_result: Result from git push

    Raises:
        ValueError: If content or file is invalid
        IOError: If file operations fail
        Exception: If git operations fail
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    _logger.info(
        f"Creating feature {FEATURE_NUMBER} markdown file: {MARKDOWN_FILENAME}"
    )

    try:
        # Phase 1, Task 1: Validate markdown content
        _logger.info("Phase 1, Task 1: Validating markdown content")
        _validate_markdown_content(MARKDOWN_CONTENT)
        _logger.debug(f"Content is {len(MARKDOWN_CONTENT)} bytes")

        # Phase 1, Task 2: Write file to disk with proper encoding
        _logger.info("Phase 1, Task 2: Writing markdown file to disk")
        filepath = _write_markdown_file(MARKDOWN_CONTENT, MARKDOWN_FILENAME, repo_path)
        _logger.debug(f"File written to: {filepath}")

        # Phase 2, Task 4: Stage and commit file with exact conventional message
        _logger.info("Phase 2, Task 4: Staging and committing file")
        commit_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
        _logger.debug(f"Using commit message: {commit_message}")

        # Stage file
        result = _run_git(["add", MARKDOWN_FILENAME], repo_path)
        if result.returncode != 0:
            raise Exception(f"git add failed: {result.stderr}")
        _logger.info(f"Staged {MARKDOWN_FILENAME}")

        # Commit file
        result = _run_git(["commit", "-m", commit_message], repo_path)
        if result.returncode != 0:
            raise Exception(f"git commit failed: {result.stderr}")
        _logger.info(f"Committed: {commit_message}")
        commit_result = result.stdout.strip()

        # Phase 2, Task 5: Push to remote repository
        _logger.info("Phase 2, Task 5: Pushing to remote repository")
        result = _run_git(["push", "-u", "origin", "HEAD"], repo_path)
        if result.returncode != 0:
            raise Exception(f"git push failed: {result.stderr}")
        _logger.info(f"Pushed to remote")
        push_result = result.stderr.strip()  # git push outputs to stderr

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            "filepath": filepath,
            "content": MARKDOWN_CONTENT,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


if __name__ == "__main__":
    """Execute feature 134 when run as a script."""
    result = create_feature_134_markdown_file()
    print("Feature 134 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
