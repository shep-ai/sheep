"""Implementation for feature 263: Create markdown file test-i3yjp8.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 262 preceding features (001-262). The file is created with:
- Exact filename: test-i3yjp8.md
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
    validate_markdown_file,
    write_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 263
FEATURE_NAME = "markdown-file-creation-f45b99"
MARKDOWN_FILENAME = "test-i3yjp8.md"


def create_feature_263_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 263.

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
        # Task 1: Generate valid markdown content
        _logger.info("Task 1: Generating markdown content")
        content = generate_markdown_content()
        _logger.debug(f"Generated {len(content)} bytes of content")

        # Task 2: Write file to disk with proper encoding
        _logger.info("Task 2: Writing markdown file to disk")
        filepath = write_markdown_file(content, MARKDOWN_FILENAME)
        file_size = len(content)
        _logger.info(f"File created at {filepath} ({file_size} bytes)")

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
        raise


if __name__ == "__main__":
    """Execute feature 263 when run as a script."""
    import sys

    # Parse optional --repo-path argument
    repo_path = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage: python -m sheep.features.feature_263_markdown_file_creation [--repo-path PATH]")
            print("")
            print("Create markdown file test-i3yjp8.md in the repository root.")
            print("")
            print("Options:")
            print("  --repo-path PATH  Path to git repository (default: current directory)")
            print("  -h, --help        Show this help message")
            sys.exit(0)
        elif sys.argv[1] == "--repo-path" and len(sys.argv) > 2:
            repo_path = sys.argv[2]
        else:
            print(f"Error: Unknown argument {sys.argv[1]}")
            print("Use --help for usage information")
            sys.exit(1)

    try:
        result = create_feature_263_markdown_file(repo_path=repo_path)
        print("✓ Feature 263 created successfully")
        print(f"  File:    {result['filepath']}")
        print(f"  Size:    {len(result['content'])} bytes")
        print(f"  Message: {result['commit_message']}")
        print(f"  Push:    {result['push_result']}")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Failed to create feature 263: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
