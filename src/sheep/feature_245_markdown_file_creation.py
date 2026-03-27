"""Feature 245: Create markdown file test-nxclc0.md with title and 2-3 sentences of content.

This module implements the complete workflow to create a single markdown file following
the established pattern from 244 preceding markdown-file-creation features.

Phase 1 Implementation (Feature Module Foundation):
- Create module skeleton with constants, imports, and logging setup
- Define task function stubs for phases 2-4

Phase 2 Implementation (Content Generation & File Writing):
- Task 2: Generate markdown content (H1 heading + 2-3 sentences)
- Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings

Phase 3 Implementation (Git Workflow Integration):
- Task 4: Stage and commit the markdown file
- Task 5: Push changes to remote repository

Phase 4 Implementation (Integration Testing & Verification):
- Execute complete workflow and verify all success criteria
"""

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

# Configuration for feature 245
FEATURE_NUMBER = 245
FILENAME = "test-nxclc0.md"


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

        _logger.info(
            f"Task 2 complete: Generated {len(content)} bytes of markdown content"
        )
        return content

    except Exception as e:
        _logger.error(f"Task 2 failed: {e}")
        raise


def task_3_write_markdown_file_to_disk(content: str) -> str:
    """
    Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings.

    This task calls the existing write_markdown_file() function which:
    - Persists markdown content to test-nxclc0.md in repository root
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


def task_4_commit_markdown_file(filepath: str, content: str) -> str:
    """
    Task 4: Stage and commit the markdown file with conventional commit message.

    This task calls the existing commit_markdown_file() function which:
    - Stages the file using GitCommitTool
    - Creates a commit with conventional commit format
    - Message format: feat(245): create markdown file test-nxclc0.md with prose content

    Args:
        filepath: Path to the markdown file to commit (from task 3).
        content: The markdown content (used for topic extraction if needed).

    Returns:
        The commit result message from GitCommitTool.

    Raises:
        ValueError: If file path is invalid.
        Exception: If git commit fails.
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Task 4: Committing markdown file")

    try:
        # Construct the exact commit message required by specification
        commit_message = (
            f"feat({FEATURE_NUMBER}): create markdown file {FILENAME} with prose content"
        )

        # Call the existing commit_markdown_file function
        result = commit_markdown_file(
            filepath, content, custom_message=commit_message
        )

        _logger.info(f"Task 4 complete: Committed {FILENAME}")
        return result

    except Exception as e:
        _logger.error(f"Task 4 failed: {e}")
        raise


def task_5_push_markdown_file() -> str:
    """
    Task 5: Push the committed markdown file to remote repository.

    This task calls the existing push_markdown_file() function which:
    - Uses GitPushTool to push changes to remote
    - Sets upstream tracking for the feature branch
    - Handles authentication and network errors

    Returns:
        The push result message from GitPushTool.

    Raises:
        Exception: If git push fails.
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Task 5: Pushing to remote repository")

    try:
        # Call the existing push_markdown_file function
        result = push_markdown_file()

        _logger.info(f"Task 5 complete: Pushed to remote repository")
        return result

    except Exception as e:
        _logger.error(f"Task 5 failed: {e}")
        raise


def main() -> dict[str, str]:
    """
    Execute all phases of feature 245 implementation.

    This function orchestrates the complete workflow:
    - Phase 2: Generate markdown content and write file to disk
    - Phase 3: Stage, commit, and push changes
    - Phase 4: Verification happens in integration testing

    Tasks executed in strict sequence:
    - Task 2: Generate markdown content
    - Task 3: Write markdown file to disk
    - Task 4: Stage and commit with conventional message
    - Task 5: Push to remote repository

    Returns:
        Dictionary with results:
        - content: The generated markdown content
        - filepath: Full path to the created file
        - commit_message: The git commit message used
        - push_result: The result from git push operation

    Raises:
        Any exceptions from task 2-5 are propagated to the caller.
    """
    _logger.info(
        f"Feature {FEATURE_NUMBER} - Complete Workflow: "
        "Generating, Writing, Committing, and Pushing markdown file"
    )

    try:
        # Execute task 2: Generate markdown content
        content = task_2_generate_markdown_content()

        # Execute task 3: Write markdown file to disk
        filepath = task_3_write_markdown_file_to_disk(content)

        # Validate the file meets all requirements
        _logger.info(f"Feature {FEATURE_NUMBER} - Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("Markdown file validation passed")

        # Execute task 4: Stage and commit
        commit_message = (
            f"feat({FEATURE_NUMBER}): create markdown file {FILENAME} with prose content"
        )
        commit_result = task_4_commit_markdown_file(filepath, content)

        # Execute task 5: Push to remote
        push_result = task_5_push_markdown_file()

        _logger.info(f"Feature {FEATURE_NUMBER} - Workflow complete")

        return {
            "content": content,
            "filepath": filepath,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Feature {FEATURE_NUMBER} - Workflow failed: {e}")
        raise


if __name__ == "__main__":
    # Allow running this module directly for testing
    result = main()
    print(f"Success! Created file: {result['filepath']}")
    print(f"File contains {len(result['content'])} bytes of content")
    print(f"Commit message: {result['commit_message']}")
