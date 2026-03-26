"""Implementation for feature 228: Create markdown file test-2kjyci.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 227 preceding features (001-227). The file is created with:
- Exact filename: test-2kjyci.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 400-600 bytes
"""

from pathlib import Path

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 228
FEATURE_NAME = "markdown-file-creation-7fd4b2"
MARKDOWN_FILENAME = "test-2kjyci.md"

# Hardcoded prose content for feature 228
# This follows the established pattern from features 224-227 using hand-written prose
MARKDOWN_CONTENT = """# The Art of Learning

Learning is a transformative journey that expands our understanding and opens new possibilities for personal and professional growth. Through continuous curiosity and engagement with new ideas, we develop wisdom and resilience that enrich both our individual capabilities and our ability to contribute meaningfully to our communities. The pursuit of knowledge is not a destination but a lifelong adventure that shapes who we become, helping us navigate challenges with greater insight and purpose.
"""


def create_feature_228_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 228.

    Orchestrates the file creation workflow:
    1. Use hardcoded prose content (following specification for feature 228)
    2. Write file to repository root with UTF-8 encoding and Unix LF line endings
    3. Validate file meets all specification requirements

    Args:
        repo_path: Path to git repository (defaults to current directory).

    Returns:
        Dictionary containing:
        - filepath: Full path to created file
        - content: Markdown content
        - filename: Markdown filename

    Raises:
        ValueError: If content or file is invalid
        IOError: If file operations fail
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    _logger.info(
        f"Creating feature {FEATURE_NUMBER} markdown file: {MARKDOWN_FILENAME}"
    )

    try:
        # Task 1: Use hardcoded prose content
        _logger.info("Task 1: Using hardcoded markdown content")
        content = MARKDOWN_CONTENT
        _logger.debug(f"Using {len(content)} bytes of hardcoded content")

        # Task 2: Write file to disk with proper encoding and line endings
        _logger.info("Task 2: Writing markdown file to disk")
        filepath = _write_markdown_file(content, MARKDOWN_FILENAME, repo_path)
        _logger.debug(f"File written to: {filepath}")

        # Task 3: Validate file meets all specification requirements
        _logger.info("Task 3: Validating markdown file")
        _validate_markdown_file(filepath)
        _logger.info("File validation passed")

        _logger.info(
            f"Successfully created feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            "filepath": filepath,
            "content": content,
            "filename": MARKDOWN_FILENAME,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


def _write_markdown_file(
    content: str, filename: str, repo_path: str | None = None
) -> str:
    """
    Write markdown content to a file at the repository root.

    Args:
        content: The markdown content to write.
        filename: The filename to create (e.g., "test-2kjyci.md").
        repo_path: Path to repository root (defaults to current working directory).

    Returns:
        Path to the created file as a string on success.

    Raises:
        ValueError: If filename is unsafe or content is invalid.
        IOError: If file write operation fails.
    """
    # Validate that filename is safe (not a path traversal)
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise ValueError(f"Invalid filename: {filename}")

    if repo_path is None:
        repo_path = str(Path.cwd())

    # Resolve the repository root
    repo_root = Path(repo_path)
    file_path = repo_root / filename

    _logger.info(f"Writing markdown file to {file_path}")

    try:
        # Write file with UTF-8 encoding and explicit Unix LF line endings
        # Using newline='\n' ensures Unix LF line endings on all platforms (Windows, Linux, macOS)
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

        # Verify file was created
        if not file_path.exists():
            raise OSError(f"File was not created: {file_path}")

        # Verify file has content
        file_size = file_path.stat().st_size
        if file_size == 0:
            raise OSError(f"File was created but is empty: {file_path}")

        _logger.info(
            f"Successfully wrote markdown file: {file_path} ({file_size} bytes)"
        )
        return str(file_path)

    except Exception as e:
        _logger.error(f"Failed to write markdown file: {e}")
        raise


def _validate_markdown_file(filepath: str) -> bool:
    """
    Validate that a markdown file meets all specification requirements.

    Checks for:
    - File exists and is readable
    - UTF-8 encoding with no BOM (Byte Order Mark)
    - Unix LF line endings (not CRLF)
    - Proper markdown structure (H1 heading, blank line, prose)
    - Content format (2-3 sentences)
    - File size in expected range (400-600 bytes)

    Args:
        filepath: Path to the markdown file to validate.

    Returns:
        True if file passes all validation checks.

    Raises:
        ValueError: If file fails any validation check with descriptive message.
        IOError: If file cannot be read.
    """
    path = Path(filepath)

    if not path.exists():
        raise OSError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise OSError(f"Path is not a file: {filepath}")

    _logger.info(f"Validating markdown file: {filepath}")

    try:
        # Read file as binary to check encoding and line endings
        with open(path, "rb") as f:
            binary_content = f.read()

        # Check for UTF-8 BOM (should not be present)
        if binary_content.startswith(b"\xef\xbb\xbf"):
            raise ValueError("File has UTF-8 BOM (should not be present)")

        # Decode as UTF-8 to verify encoding
        try:
            text_content = binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"File is not valid UTF-8: {e}")

        # Check for CRLF line endings (should use LF instead)
        if b"\r\n" in binary_content:
            raise ValueError("File uses CRLF line endings (should use LF)")

        # Check for H1 heading at start
        if not text_content.lstrip().startswith("# "):
            raise ValueError("File must start with H1 heading (# )")

        lines = text_content.split("\n")

        # Check that first line is H1 heading
        if not lines[0].startswith("# "):
            raise ValueError("First line must be H1 heading (# )")

        # Check that second line is blank (separator)
        if len(lines) < 2 or lines[1] != "":
            raise ValueError("Second line must be blank (separator after heading)")

        # Get prose content (skip heading and blank line)
        prose_lines = lines[2:]

        # Remove trailing empty lines for prose validation
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        if not prose_lines:
            raise ValueError("No prose content found after heading")

        prose_content = "\n".join(prose_lines).strip()

        # Validate sentence count (count periods)
        sentence_count = prose_content.count(".")
        if sentence_count < 2 or sentence_count > 3:
            raise ValueError(
                f"Content must have 2-3 sentences, found {sentence_count}"
            )

        # Check for trailing newline (Unix convention)
        if not text_content.endswith("\n"):
            raise ValueError("File must end with trailing newline")

        # Check file size is in expected range (400-600 bytes)
        file_size = path.stat().st_size
        if file_size < 400 or file_size > 600:
            _logger.warning(
                f"File size {file_size} bytes is outside expected range (400-600 bytes)"
            )

        _logger.info(f"Markdown file validation passed: {filepath}")
        return True

    except (OSError, ValueError):
        raise
    except Exception as e:
        _logger.error(f"Unexpected error during validation: {e}")
        raise OSError(f"Error validating file: {e}")


if __name__ == "__main__":
    """Execute feature 228 when run as a script."""
    result = create_feature_228_markdown_file()
    print("Feature 228 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
