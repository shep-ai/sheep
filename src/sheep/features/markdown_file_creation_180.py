"""Feature 180: Create markdown file test-hylnjg.md with prose content."""

from pathlib import Path

from sheep.content_generators import (
    write_markdown_file,
    validate_markdown_file,
    commit_markdown_file,
    push_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

FILENAME = "test-hylnjg.md"
CUSTOM_COMMIT_MESSAGE = "feat(180): create markdown file test-hylnjg.md with prose content"

# Prose content with H1 heading and 3 sentences
TEST_CONTENT = """# The Power of Persistence

Persistence is the unwavering determination to pursue goals despite obstacles and setbacks. It transforms challenges into opportunities for growth and enables us to achieve what initially seemed impossible. With each step forward, we build resilience and discover the strength within ourselves to overcome any adversity.
"""


def main() -> None:
    """
    Create markdown file test-hylnjg.md using content_generators utilities.

    This function sequences the content_generators module functions:
    1. Write markdown content to disk with UTF-8 encoding, LF line endings
    2. Validate markdown structure and properties
    3. Stage and commit with custom message (feat(180))
    4. Push to remote feature branch

    The custom_message parameter is used to override the hardcoded feature
    number in commit_markdown_file() (which defaults to "feat(145)").
    """
    repo_path = str(Path.cwd())

    _logger.info(f"Starting feature 180: create {FILENAME}")
    _logger.info(f"Repository path: {repo_path}")

    try:
        # Step 1: Write file to disk
        _logger.info("Step 1: Writing markdown file to disk")
        filepath = write_markdown_file(TEST_CONTENT, FILENAME)
        _logger.info(f"File written to: {filepath}")
        _logger.info(f"Content size: {len(TEST_CONTENT)} bytes")

        # Step 2: Validate file
        _logger.info("Step 2: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Step 3: Commit file with custom message (feature 180)
        _logger.info("Step 3: Committing markdown file")
        _logger.info(f"Using custom commit message: {CUSTOM_COMMIT_MESSAGE}")
        commit_result = commit_markdown_file(
            filepath=filepath,
            content=TEST_CONTENT,
            repo_path=repo_path,
            custom_message=CUSTOM_COMMIT_MESSAGE,
        )
        _logger.info(f"Commit result: {commit_result}")

        # Step 4: Push to remote
        _logger.info("Step 4: Pushing to remote repository")
        push_result = push_markdown_file(repo_path=repo_path)
        _logger.info(f"Push result: {push_result}")

        _logger.info(f"Successfully created and published {FILENAME}")
        return

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


if __name__ == "__main__":
    main()
