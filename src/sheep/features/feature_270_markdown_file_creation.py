"""Implementation for feature 270: Create markdown file test-2sqwpg.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 269 preceding features (001-269). The file is created with:
- Exact filename: test-2sqwpg.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 400-600 bytes
- Git staging, commit, and push operations

Unlike feature 269, feature 270 uses deterministic hardcoded generic prose content
instead of LLM-based auto-generation, reducing complexity and improving performance.
"""

from pathlib import Path

from sheep.content_generators import (
    commit_markdown_file,
    push_markdown_file,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 270
FEATURE_NAME = "markdown-file-creation-f37f64"
MARKDOWN_FILENAME = "test-2sqwpg.md"

# Hardcoded content constants (deterministic, no external dependencies)
TITLE = "Software Engineering Practices"
PROSE = "Software development is a continuous journey that requires dedication to learning and continuous improvement. Modern approaches emphasize automated testing, continuous integration, and collaborative code reviews to ensure quality and maintainability across projects. The intersection of technical excellence and clear communication enables teams to deliver reliable software that solves real problems and creates lasting value."


def create_markdown_file(repo_path: str = ".") -> Path:
    """
    Create a markdown file at the repository root with UTF-8 encoding and Unix LF line endings.

    This function creates test-2sqwpg.md with proper formatting:
    - H1 heading on line 1
    - Blank line on line 2
    - Prose content starting on line 3
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Args:
        repo_path: Path to repository root (defaults to current directory).

    Returns:
        pathlib.Path object pointing to the created file.

    Raises:
        IOError: If file creation fails.
    """
    repo_root = Path(repo_path)
    file_path = repo_root / MARKDOWN_FILENAME

    # Format content: H1 heading + blank line + prose + trailing newline
    content = f"# {TITLE}\n\n{PROSE}\n"

    _logger.info(f"Creating markdown file: {file_path}")

    try:
        # Use pathlib.Path.write_text() with explicit UTF-8 encoding and Unix LF
        # The newline='\n' parameter ensures Unix LF (\n) line endings across all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")

        _logger.info(f"File created successfully: {file_path}")
        return file_path

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


def validate_created_file(filepath: str | Path) -> bool:
    """
    Validate that a created markdown file meets all specification requirements.

    Validates:
    - File exists
    - File size is between 400-600 bytes (inclusive)
    - UTF-8 encoding without BOM (Byte Order Mark)
    - Unix LF line endings (not CRLF)
    - H1 heading on line 1
    - Blank line on line 2
    - Exactly 2-3 sentences of prose on line 3+

    Args:
        filepath: Path to the markdown file to validate (str or Path).

    Returns:
        True if all validations pass.

    Raises:
        ValueError: If any validation fails with descriptive message.
    """
    path = Path(filepath)

    _logger.info(f"Validating markdown file: {path}")

    # Check 1: File exists
    if not path.exists():
        raise ValueError(f"File does not exist: {filepath}")

    # Check 2: File size is in valid range (400-600 bytes)
    file_size = path.stat().st_size
    if not (400 <= file_size <= 600):
        raise ValueError(
            f"File size {file_size} bytes is outside valid range (400-600). "
            f"Expected approximately 400-600 bytes for H1 heading + blank line + 2-3 sentences."
        )

    # Read file as binary to check encoding and line endings
    binary_content = path.read_bytes()

    # Check 3: File encoding is UTF-8 without BOM
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File has UTF-8 BOM (Byte Order Mark) — should not be present")

    try:
        text_content = binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8 encoding: {e}")

    # Check 4: File uses Unix LF line endings (not CRLF)
    if b"\r\n" in binary_content:
        raise ValueError(
            "File uses Windows CRLF line endings (\\r\\n) — should use Unix LF (\\n)"
        )

    # Check 5: File ends with newline
    if not text_content.endswith("\n"):
        raise ValueError("File must end with a trailing newline character")

    # Check 6: H1 heading on first line
    lines = text_content.split("\n")
    if not lines[0].startswith("# "):
        raise ValueError(f"First line must be H1 heading (# ) — found: {lines[0]}")

    # Check 7: Blank line on second line
    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank (separator after heading)")

    # Check 8: Exactly 2-3 sentences of prose
    prose_lines = lines[2:]
    # Remove trailing empty lines
    while prose_lines and prose_lines[-1] == "":
        prose_lines.pop()

    if not prose_lines:
        raise ValueError("No prose content found after heading and blank line")

    prose_content = "\n".join(prose_lines).strip()
    sentence_count = prose_content.count(".")
    if not (2 <= sentence_count <= 3):
        raise ValueError(
            f"Prose must contain exactly 2-3 sentences (periods). "
            f"Found {sentence_count} sentences: {prose_content[:100]}..."
        )

    _logger.info("File validation passed — all checks successful")
    return True


def create_feature_270_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 270.

    Orchestrates the complete workflow:
    1. Prepare hardcoded markdown content (H1 heading + 2-3 sentences)
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
        # Task 1: Prepare hardcoded markdown content
        _logger.info("Task 1: Preparing markdown content (hardcoded)")
        content = _prepare_markdown_content()
        _logger.debug(f"Generated {len(content)} bytes of content")

        # Task 2: Write file to disk with proper encoding
        _logger.info("Task 2: Writing markdown file to disk")
        filepath = create_markdown_file(repo_path)
        _logger.debug(f"File written to: {filepath}")

        # Task 3: Validate file meets all specification requirements
        _logger.info("Task 3: Validating markdown file")
        validate_created_file(filepath)
        _logger.info("File validation passed")

        # Task 4: Stage and commit file with exact conventional message
        _logger.info("Task 4: Staging and committing file")
        commit_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME}"
        _logger.debug(f"Using commit message: {commit_message}")
        commit_result = commit_markdown_file(str(filepath), content, repo_path, custom_message=commit_message)
        _logger.debug(f"Commit result: {commit_result}")

        # Task 5: Push to remote repository
        _logger.info("Task 5: Pushing to remote repository")
        push_result = push_markdown_file(repo_path)
        _logger.debug(f"Push result: {push_result}")

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            "filepath": str(filepath),
            "content": content,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


def _prepare_markdown_content() -> str:
    """
    Prepare markdown content with hardcoded title and prose.

    Returns:
        String containing valid markdown with H1 heading and 2-3 sentences of prose.
    """
    content = f"# {TITLE}\n\n{PROSE}\n"
    return content


if __name__ == "__main__":
    """Execute feature 270 when run as a script."""
    result = create_feature_270_markdown_file()
    print("Feature 270 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
