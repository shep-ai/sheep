"""Test script that creates test-szyfny.md with mocked LLM but real git operations.

This script is used to verify the orchestration works end-to-end without
requiring a real Anthropic API key.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directories to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sheep.content_generators import create_markdown_file
from sheep.observability.logging import get_logger

logger = get_logger(__name__)


def main(filename: str = "test-szyfny.md", repo_path: str | None = None) -> int:
    """
    Orchestrate markdown file creation with mocked LLM for testing.

    Args:
        filename: The markdown file to create (default: "test-szyfny.md").
        repo_path: Path to the git repository. If None, uses current directory.

    Returns:
        0 on success, non-zero on failure.
    """
    # Use current working directory if repo_path not specified
    if repo_path is None:
        repo_path = str(Path.cwd())

    logger.info(f"Creating markdown file '{filename}' in {repo_path} (with mocked LLM)")

    try:
        # Validate that repo_path exists and is a directory
        repo_dir = Path(repo_path)
        if not repo_dir.exists():
            logger.error(f"Repository path does not exist: {repo_path}")
            return 2

        if not repo_dir.is_dir():
            logger.error(f"Repository path is not a directory: {repo_path}")
            return 2

        # Mock the LLM to return test content
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Software Engineering Best Practices\n\nWriting clean and maintainable code requires consistent application of design principles and patterns. Testing is essential for ensuring code quality and preventing regressions. Documentation helps future developers understand the codebase and maintain consistency across the project.\n"
        }

        with patch("sheep.content_generators.get_reasoning_llm", return_value=mock_llm):
            # Call the orchestration function
            logger.info("Starting markdown file creation workflow (with mocked LLM)")
            result = create_markdown_file(filename, repo_path)

            # Log success details
            logger.info(f"✓ File created successfully: {result['filepath']}")
            logger.info(f"✓ File size: {len(result['content'])} bytes")
            logger.info(f"✓ Commit message: {result['commit_message']}")
            logger.info(f"✓ Push result: {result['push_result']}")

            return 0

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return 1
    except IOError as e:
        logger.error(f"File I/O error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
