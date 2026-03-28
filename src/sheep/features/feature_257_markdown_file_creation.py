"""Implementation for feature 257: Create markdown file test-oxy715.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 256 preceding features (001-256). The file is created with:
- Exact filename: test-oxy715.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 250-600 bytes
- Git staging, commit, and push operations

Error Handling:
- Implements fail-fast principle with cleanup of partial artifacts on any failure
- On file creation failure: error is immediately propagated
- On commit failure: created file is deleted before error is propagated
- On push failure: created file is deleted and commit is undone (git reset HEAD~1)
- All exceptions are logged at ERROR level before re-raising
"""

import json
import subprocess
import sys
from pathlib import Path

from sheep.content_generators import (
    commit_markdown_file,
    generate_markdown_content,
    push_markdown_file,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 257
FEATURE_NAME = "markdown-file-creation-62bad4"
MARKDOWN_FILENAME = "test-oxy715.md"


def _cleanup_file(filepath: str) -> None:
    """
    Clean up a created markdown file on failure.

    Args:
        filepath: Path to the file to delete.
    """
    if filepath and Path(filepath).exists():
        try:
            Path(filepath).unlink()
            _logger.debug(f"Cleaned up file: {filepath}")
        except Exception as e:
            _logger.warning(f"Failed to clean up file {filepath}: {e}")


def _undo_commit(repo_path: str) -> None:
    """
    Undo the most recent commit when an operation fails after committing.

    Args:
        repo_path: Path to the git repository.
    """
    try:
        result = subprocess.run(
            ["git", "reset", "HEAD~1"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            _logger.debug("Undone recent commit with git reset HEAD~1")
        else:
            _logger.warning(f"Failed to undo commit: {result.stderr}")
    except Exception as e:
        _logger.warning(f"Failed to undo commit: {e}")


def create_feature_257_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 257.

    Orchestrates the complete workflow:
    1. Generate valid markdown content (H1 heading + 2-3 sentences)
    2. Write file to repository root with UTF-8 encoding
    3. Validate file meets all specification requirements
    4. Stage and commit with conventional message
    5. Push to remote feature branch

    On any failure:
    - If file was created but commit failed: file is deleted
    - If commit succeeded but push failed: file is deleted and commit is undone
    - Error is logged at ERROR level and re-raised to caller

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

    filepath = None
    commit_message = None
    commit_created = False

    try:
        # Task 1: Generate valid markdown content
        _logger.info("Task 1: Generating markdown content")
        content = generate_markdown_content()
        _logger.debug(f"Generated {len(content)} bytes of content")

        # Task 2: Write file to disk with proper encoding
        _logger.info("Task 2: Writing markdown file to disk")
        filepath = write_markdown_file(content, MARKDOWN_FILENAME)
        _logger.debug(f"File written to: {filepath}")

        # Task 3: Validate file meets all specification requirements
        _logger.info("Task 3: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Task 4: Stage and commit file with exact conventional message
        _logger.info("Task 4: Staging and committing file")
        commit_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
        _logger.debug(f"Using commit message: {commit_message}")
        commit_result = commit_markdown_file(filepath, content, repo_path, custom_message=commit_message)
        _logger.debug(f"Commit result: {commit_result}")
        commit_created = True

        # Task 5: Push to remote repository
        _logger.info("Task 5: Pushing to remote repository")
        push_result = push_markdown_file(repo_path)
        _logger.debug(f"Push result: {push_result}")

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            "filepath": filepath,
            "content": content,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")

        # Cleanup: If commit was created but push failed, undo the commit
        if commit_created:
            _logger.info("Cleaning up: Undoing commit due to failure")
            _undo_commit(repo_path)

        # Cleanup: If file was created but operation failed, delete it
        if filepath:
            _logger.info("Cleaning up: Deleting created markdown file")
            _cleanup_file(filepath)

        # Re-raise the original exception to caller
        raise


if __name__ == "__main__":
    """Execute feature 257 when run as a script."""
    try:
        result = create_feature_257_markdown_file()
        print("Feature 257 created successfully:")
        print(json.dumps(result, indent=2))
        sys.exit(0)
    except Exception as e:
        print(f"Error: Failed to create feature 257: {e}", file=sys.stderr)
        sys.exit(1)
