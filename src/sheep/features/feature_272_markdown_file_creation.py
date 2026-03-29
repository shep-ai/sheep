"""Implementation for feature 272: Create markdown file test-wvkqjb.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 271 preceding features (001-271). The file is created with:
- Exact filename: test-wvkqjb.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 250-600 bytes
- Git staging, commit, and push operations
"""

from pathlib import Path

from sheep.content_generators import (
    commit_markdown_file,
    generate_markdown_content,
    push_markdown_file,
    validate_file_properties,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 272
FEATURE_NAME = "markdown-file-creation-e18c7f"
MARKDOWN_FILENAME = "test-wvkqjb.md"


def create_feature_272_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 272.

    Orchestrates the complete workflow:
    1. Generate valid markdown content (H1 heading + 2-3 sentences)
    2. Write file to repository root with UTF-8 encoding
    3. Validate file meets all specification requirements
    4. Stage and commit with conventional message
    5. Push to remote feature branch

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
        # Phase 2 Task-3: Generate valid markdown content via Claude API
        _logger.info("Phase 2 Task-3: Generating markdown content")
        content = generate_markdown_content()
        _logger.debug(f"Generated {len(content)} bytes of content")
        _logger.info(f"Content preview (first 100 chars): {content[:100]}")

        # Phase 2 Task-4: Write file to disk with proper encoding
        _logger.info("Phase 2 Task-4: Writing markdown file to disk")
        filepath = write_markdown_file(content, MARKDOWN_FILENAME)
        _logger.debug(f"File written to: {filepath}")

        # Log file size after successful write
        file_size = Path(filepath).stat().st_size
        _logger.info(f"File size: {file_size} bytes")

        # Validate file meets all specification requirements
        _logger.info("Validating markdown file structure")
        validate_markdown_file(filepath)
        _logger.info("Markdown format validation passed")

        # Phase 2 Task-5: Explicit validation of file encoding and line endings
        _logger.info("Phase 2 Task-5: Validating file encoding and line endings")
        validate_file_properties(filepath)
        _logger.info("File encoding (UTF-8 no BOM) and line endings (LF) validated")

        # Phase 3: Stage and commit file with exact conventional message
        _logger.info("Phase 3: Staging and committing file")
        commit_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with title and prose content"
        _logger.debug(f"Using commit message: {commit_message}")
        commit_result = commit_markdown_file(filepath, content, repo_path, custom_message=commit_message)
        _logger.debug(f"Commit result: {commit_result}")

        # Phase 3: Push to remote repository
        _logger.info("Phase 3: Pushing to remote repository")
        push_result = push_markdown_file(repo_path)
        _logger.debug(f"Push result: {push_result}")

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            "filepath": filepath,
            "content": content[:200],  # Truncate to first 200 chars for readability
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


if __name__ == "__main__":
    """Execute feature 272 when run as a script."""
    result = create_feature_272_markdown_file()
    print("Feature 272 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
