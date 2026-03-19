"""Implementation for feature 103: Create markdown file test-uamczl.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 100+ preceding features (001-102). The file is created with:
- Exact filename: test-uamczl.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 400-600 bytes
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
FEATURE_NUMBER = 103
FEATURE_NAME = "markdown-file-creation-4b3d0d"
MARKDOWN_FILENAME = "test-uamczl.md"


def _validate_file_format_comprehensive(filepath: str) -> None:
    """
    Perform comprehensive file format validation after validate_markdown_file().

    Checks:
    - No UTF-8 BOM marker at start
    - No CRLF line endings (LF only)
    - Trailing newline exists
    - H1 heading format (# [text])
    - Blank line after heading
    - 2-3 sentences in prose (count periods)
    - File size within typical range (350-600 bytes, soft guideline)

    Args:
        filepath: Path to markdown file to validate

    Raises:
        ValueError: If any critical validation check fails
    """
    file_path = Path(filepath)

    # Read file in binary mode for low-level checks
    file_bytes = file_path.read_bytes()
    file_text = file_path.read_text(encoding="utf-8")

    # Check 1: No BOM marker
    _logger.debug("Checking for UTF-8 BOM marker")
    if file_bytes.startswith(b'\xef\xbb\xbf'):
        raise ValueError(
            f"File contains UTF-8 BOM marker at start (bytes: EF BB BF). "
            f"Specification requires UTF-8 without BOM."
        )
    _logger.debug("✓ No UTF-8 BOM marker found")

    # Check 2: No CRLF line endings
    _logger.debug("Checking for CRLF line endings")
    if b'\r\n' in file_bytes:
        raise ValueError(
            f"File contains CRLF line endings (\\r\\n). "
            f"Specification requires Unix-style LF line endings (\\n only)."
        )
    _logger.debug("✓ No CRLF line endings found")

    # Check 3: Trailing newline exists
    _logger.debug("Checking for trailing newline")
    if not file_text.endswith('\n'):
        raise ValueError(
            f"File does not end with trailing newline. "
            f"Specification requires Unix convention of trailing newline."
        )
    _logger.debug("✓ Trailing newline present")

    # Parse file structure
    lines = file_text.split('\n')

    # Check 4: H1 heading format
    _logger.debug("Checking H1 heading format")
    if not lines[0].startswith('# '):
        raise ValueError(
            f"First line is not a valid H1 heading. "
            f"Expected format: '# [heading text]', got: '{lines[0]}'"
        )
    _logger.debug(f"✓ H1 heading valid: {lines[0]}")

    # Check 5: Blank line after heading
    _logger.debug("Checking blank line after heading")
    if len(lines) < 2 or lines[1] != '':
        raise ValueError(
            f"No blank line after H1 heading. "
            f"Specification requires blank line between heading and prose."
        )
    _logger.debug("✓ Blank line separator present")

    # Extract prose content (everything after heading and blank line)
    prose_lines = lines[2:]
    # Remove trailing empty strings from final newline
    while prose_lines and prose_lines[-1] == '':
        prose_lines.pop()
    prose_text = '\n'.join(prose_lines).strip()

    # Check 6: 2-3 sentences (count periods)
    _logger.debug("Checking sentence count (period count)")
    sentence_count = prose_text.count('.')
    if not (2 <= sentence_count <= 3):
        raise ValueError(
            f"Prose contains {sentence_count} sentences (detected by period count). "
            f"Specification requires 2-3 sentences. Prose: {prose_text[:100]}..."
        )
    _logger.debug(f"✓ Sentence count valid: {sentence_count} periods found")

    # Check 7: File size in typical range (soft guideline)
    file_size = len(file_bytes)
    _logger.debug(f"Checking file size: {file_size} bytes")
    if file_size < 350:
        _logger.warning(
            f"File size ({file_size} bytes) is below typical guideline range (350-600 bytes). "
            f"Content may be too brief."
        )
    elif file_size > 600:
        _logger.warning(
            f"File size ({file_size} bytes) is above typical guideline range (350-600 bytes). "
            f"Content may be too verbose."
        )
    else:
        _logger.debug(f"✓ File size within typical range: {file_size} bytes")

    _logger.debug("All comprehensive validation checks passed")


def create_feature_103_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 103.

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
        _logger.debug(f"File written to: {filepath}")

        # Task 3: Validate file meets all specification requirements
        _logger.info("Task 3: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.debug("validate_markdown_file() passed")

        # Task 3b: Comprehensive explicit validation checks
        _logger.debug("Task 3b: Running comprehensive file format validation")
        _validate_file_format_comprehensive(filepath)
        _logger.info("File validation passed (all comprehensive checks)")

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
    """Execute feature 103 when run as a script."""
    result = create_feature_103_markdown_file()
    print("Feature 103 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
