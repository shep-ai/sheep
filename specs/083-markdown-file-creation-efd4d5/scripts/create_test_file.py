"""Orchestration script for feature 083: create markdown file test-szyfny.md.

This script orchestrates the complete workflow to create a markdown file
named test-szyfny.md at the repository root. It calls the established
content generation infrastructure to:
1. Generate markdown content (title + 2-3 sentences)
2. Write file to disk at repository root
3. Validate the file meets all requirements
4. Stage and commit with conventional commit message
5. Push to remote repository

Exit codes:
- 0: Success - file created, committed, and pushed
- 1: General error - file/git operations failed
- 2: Configuration error - repo_path or other config invalid
"""

import sys
from pathlib import Path

# Add parent directories to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sheep.content_generators import create_markdown_file
from sheep.observability.logging import get_logger

logger = get_logger(__name__)


def main(filename: str = "test-szyfny.md", repo_path: str | None = None) -> int:
    """
    Orchestrate the markdown file creation workflow.

    This is the main entry point for feature 083. It calls create_markdown_file()
    with the specified filename and repository path.

    Args:
        filename: The markdown file to create (default: "test-szyfny.md").
        repo_path: Path to the git repository. If None, uses current directory.

    Returns:
        0 on success, non-zero on failure.
    """
    # Use current working directory if repo_path not specified
    if repo_path is None:
        repo_path = str(Path.cwd())

    logger.info(f"Feature 083: Creating markdown file '{filename}' in {repo_path}")

    try:
        # Validate that repo_path exists and is a directory
        repo_dir = Path(repo_path)
        if not repo_dir.exists():
            logger.error(f"Repository path does not exist: {repo_path}")
            return 2

        if not repo_dir.is_dir():
            logger.error(f"Repository path is not a directory: {repo_path}")
            return 2

        # Call the orchestration function from content_generators
        logger.info("Starting markdown file creation workflow")
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
