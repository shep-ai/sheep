"""Feature 123: Create markdown file test-b3x0s1.md with title and 2-3 sentences of content.

This module implements the workflow to create a single markdown file following
the established pattern from 122+ prior markdown-file-creation features.

Phase 1 Implementation:
- Module foundation: Constants, imports, and module structure
Phase 2 Implementation:
- Task 2: Generate markdown content (H1 heading + 2-3 sentences)
- Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings
"""

from pathlib import Path

from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
    validate_markdown_file,
    commit_markdown_file,
    push_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Configuration for feature 123
FEATURE_NUMBER = 123
FILENAME = "test-b3x0s1.md"


def task_2_generate_markdown_content() -> str:
    """
    Task 2: Generate markdown content with H1 heading and 2-3 sentences.

    This task calls the existing generate_markdown_content() function which:
    - Uses the CrewAI LLM framework to generate coherent prose
    - Returns markdown with H1 heading about an implementer-chosen topic
    - Ensures 2-3 sentences of prose content
    - Adds trailing newline for Unix convention

    Returns:
        String containing valid markdown (H1 heading + blank line + 2-3 sentences).

    Raises:
        ValueError: If generated content doesn't meet format requirements.
        Exception: If LLM API call fails.
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Task 2: Generating markdown content")

    try:
        # Call the existing generate_markdown_content function
        content = generate_markdown_content()

        # Validate sentence count (hard requirement: must be 2-3 sentences)
        sentence_count = content.count(".")
        if sentence_count < 2 or sentence_count > 3:
            raise ValueError(
                f"Content validation failed: expected 2-3 sentences, found {sentence_count}"
            )

        _logger.info(
            f"Task 2 complete: Generated {len(content)} bytes of markdown content "
            f"with {sentence_count} sentences"
        )
        return content

    except Exception as e:
        _logger.error(f"Task 2 failed: {e}")
        raise


def task_3_write_markdown_file_to_disk(content: str) -> str:
    """
    Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings.

    This task calls the existing write_markdown_file() function which:
    - Persists markdown content to test-b3x0s1.md in repository root
    - Uses UTF-8 encoding without BOM
    - Ensures Unix-style LF line endings (not CRLF)
    - Validates file was created successfully

    Args:
        content: The markdown content to write (from task 2).

    Returns:
        Full path to the created file.

    Raises:
        ValueError: If content is invalid or filename is unsafe.
        IOError: If file write operation fails.
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Task 3: Writing markdown file to disk")

    try:
        # Check that file does not already exist (fail-fast on conflicts)
        repo_root = Path.cwd()
        file_path = repo_root / FILENAME
        if file_path.exists():
            raise ValueError(f"File already exists: {FILENAME}")

        # Call the existing write_markdown_file function
        filepath = write_markdown_file(content, FILENAME)

        _logger.info(
            f"Task 3 complete: Wrote markdown file to {filepath} "
            f"({Path(filepath).stat().st_size} bytes)"
        )
        return filepath

    except Exception as e:
        _logger.error(f"Task 3 failed: {e}")
        raise


def task_4_commit_changes(filepath: str, content: str) -> str:
    """
    Task 4: Stage and commit the markdown file with conventional message.

    This task calls the existing commit_markdown_file() function with the
    exact commit message format specified in the feature requirements:
    "feat(123): Create markdown file test-b3x0s1.md with prose content (#192)"

    Args:
        filepath: Full path to the markdown file to commit.
        content: The markdown content (passed to commit_markdown_file).

    Returns:
        Result message from the git commit operation.

    Raises:
        ValueError: If git commit fails.
        Exception: If git operations fail.
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Task 4: Committing changes to git")

    try:
        # Conventional commit message with feature number and exact filename
        commit_message = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with prose content (#192)"

        # Call the existing commit_markdown_file function with custom message
        result = commit_markdown_file(
            filepath=filepath,
            content=content,
            custom_message=commit_message,
        )

        _logger.info(
            f"Task 4 complete: Committed {FILENAME} with message: {commit_message}"
        )
        return result

    except Exception as e:
        _logger.error(f"Task 4 failed: {e}")
        raise


def task_5_push_changes() -> str:
    """
    Task 5: Push committed changes to remote origin with upstream tracking.

    This task calls the existing push_markdown_file() function which:
    - Pushes the current branch to origin remote
    - Sets upstream tracking with -u flag
    - Returns push result status

    Returns:
        Result message from the git push operation.

    Raises:
        Exception: If git push fails (network error, auth error, etc.).
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Task 5: Pushing changes to remote origin")

    try:
        # Call the existing push_markdown_file function
        result = push_markdown_file(remote="origin")

        _logger.info(f"Task 5 complete: Pushed to remote origin")
        return result

    except Exception as e:
        _logger.error(f"Task 5 failed: {e}")
        raise


def main() -> bool:
    """
    Execute phase 5: Orchestration & Validation.

    This function orchestrates all tasks in sequence:
    - Task 2: Generate markdown content
    - Task 3: Write to disk
    - Task 4: Commit with git
    - Task 5: Push to remote

    Returns:
        True if all tasks complete successfully, False on failure.

    Raises:
        Any exceptions from tasks 2-5 are logged and return False.
    """
    _logger.info(f"Starting feature {FEATURE_NUMBER} execution")
    _logger.info(f"Feature {FEATURE_NUMBER} - Phase 5: Orchestration & Validation")

    try:
        # Execute task 2: Generate markdown content
        content = task_2_generate_markdown_content()

        # Execute task 3: Write markdown file to disk
        filepath = task_3_write_markdown_file_to_disk(content)

        # Execute task 4: Commit changes to git
        commit_result = task_4_commit_changes(filepath, content)

        # Execute task 5: Push changes to remote origin
        push_result = task_5_push_changes()

        _logger.info(f"Feature {FEATURE_NUMBER} completed successfully")
        return True

    except Exception as e:
        _logger.error(f"Feature {FEATURE_NUMBER} failed: {e}")
        return False


if __name__ == "__main__":
    # Allow running this module directly for testing
    success = main()
    exit(0 if success else 1)
