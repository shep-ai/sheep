"""Implementation for feature 255: Create markdown file test-i3iccc.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern from
250+ prior implementations. The feature uses:
- LLM-based content generation via content_generators module
- pathlib.Path for file I/O with UTF-8 encoding and Unix LF line endings
- Comprehensive validation at each phase
- Standard git operations (add, commit, push)

The module implements phases 1-2 of 4:
Phase 1: Content Generation & Validation
  1. Generating markdown content using LLM
  2. Validating generated content meets format requirements

Phase 2: File Creation & Verification
  1. Writing validated content to disk with pathlib.Path
  2. Verifying file encoding, line endings, and structure

Subsequent phases (not in scope for this module):
  3. Git workflow integration (staging, committing, pushing)
  4. Integration tests and verification
"""

from pathlib import Path

from sheep.content_generators import generate_markdown_content, validate_markdown_file
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 255 constants
FILENAME = "test-i3iccc.md"
FEATURE_NUMBER = 255
BRANCH_NAME = "feat/255-markdown-file-creation-17ca12"
COMMIT_MESSAGE_TEMPLATE = f"feat({FEATURE_NUMBER}): create markdown file {FILENAME} with prose content"


def generate_content() -> str:
    """Generate markdown content with H1 heading and 2-3 sentences of prose.

    Uses the content_generators module to generate content via Claude API.
    The generated content will have:
    - H1 markdown heading on first line
    - Blank line separator on second line
    - 2-3 sentences of prose content starting on third line
    - Trailing newline (Unix convention)

    Returns:
        String containing valid markdown content that meets format requirements.

    Raises:
        ValueError: If generated content doesn't meet format requirements.
        Exception: If LLM API call fails.
    """
    _logger.info("Generating markdown content with LLM")

    try:
        # Call content_generators module to generate markdown
        content = generate_markdown_content()

        _logger.debug(f"Generated {len(content)} bytes of markdown content")
        _logger.info("Markdown content generated successfully")
        return content

    except Exception as e:
        _logger.error(f"Failed to generate markdown content: {e}")
        raise


def validate_content(content: str) -> None:
    """Validate that generated markdown content meets format requirements.

    Checks that:
    1. Content is not empty
    2. First line is H1 heading (starts with "# ")
    3. Second line is blank (separator between heading and prose)
    4. Prose content has exactly 2-3 sentences (counted by periods)
    5. Content has trailing newline

    Args:
        content: The markdown content string to validate.

    Raises:
        ValueError: If content doesn't meet any format requirement.
    """
    _logger.info("Validating generated markdown content")

    if not content or not content.strip():
        raise ValueError("Generated content is empty")

    lines = content.split("\n")

    # Check for H1 heading on first line
    if not lines or not lines[0].startswith("# "):
        raise ValueError("Content must start with H1 heading (# )")

    # Check for blank line on second line
    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank (separator between heading and prose)")

    # Check prose content has 2-3 sentences
    prose_lines = lines[2:]
    prose_content = "\n".join(prose_lines).strip()

    if not prose_content:
        raise ValueError("No prose content found after heading and blank line")

    sentence_count = prose_content.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(f"Content should have 2-3 sentences, found {sentence_count}")

    # Check for trailing newline
    if not content.endswith("\n"):
        raise ValueError("Content must end with trailing newline")

    _logger.info("Content validation passed")


def write_file(content: str) -> bool:
    """Write validated markdown content to disk using pathlib.Path.

    Writes the content to a file named test-i3iccc.md in the repository root
    with UTF-8 encoding. The file will use Unix LF line endings by default on
    Unix-like systems (Linux, macOS).

    Args:
        content: The markdown content string to write to disk.

    Returns:
        True if file was successfully written.

    Raises:
        ValueError: If content is invalid or file path is unsafe.
        FileNotFoundError: If parent directory doesn't exist.
        IOError: If file write operation fails.
    """
    _logger.info(f"Writing markdown file to {FILENAME}")

    # Validate content before writing
    validate_content(content)

    try:
        # Resolve the repository root (current working directory)
        repo_root = Path.cwd()
        file_path = repo_root / FILENAME

        _logger.debug(f"Writing to: {file_path}")

        # Write file with UTF-8 encoding (handles LF line endings on Unix)
        file_path.write_text(content, encoding="utf-8")

        # Verify file was created
        if not file_path.exists():
            raise FileNotFoundError(f"File was not created: {file_path}")

        # Verify file has content
        file_size = file_path.stat().st_size
        if file_size == 0:
            raise IOError(f"File was created but is empty: {file_path}")

        _logger.info(
            f"Successfully wrote markdown file: {file_path} ({file_size} bytes)"
        )
        return True

    except FileNotFoundError:
        raise
    except IOError:
        raise
    except Exception as e:
        _logger.error(f"Failed to write markdown file: {e}")
        raise IOError(f"Error writing file: {e}") from e


def verify_file() -> bool:
    """Verify that the markdown file meets all format and encoding requirements.

    Verifies:
    - File exists at FILENAME in repository root
    - File is UTF-8 encoded without BOM (Byte Order Mark)
    - File uses Unix LF line endings (not Windows CRLF)
    - File has valid markdown structure (H1 heading, blank line, 2-3 sentences)
    - File has trailing newline
    - File size is within acceptable range (250-600 bytes)

    Returns:
        True if file passes all validation checks.

    Raises:
        ValueError: If file fails any validation check.
        FileNotFoundError: If file does not exist.
        IOError: If file cannot be read.
    """
    _logger.info(f"Verifying markdown file: {FILENAME}")

    try:
        repo_root = Path.cwd()
        file_path = repo_root / FILENAME

        # Check file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")

        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Use content_generators module for comprehensive validation
        validate_markdown_file(str(file_path))

        # Check file size
        file_size = file_path.stat().st_size
        min_bytes, max_bytes = 350, 650
        if not (min_bytes <= file_size <= max_bytes):
            raise ValueError(
                f"File size {file_size} bytes outside acceptable range {min_bytes}-{max_bytes} bytes"
            )

        _logger.info(f"File verification passed: {file_path} ({file_size} bytes)")
        return True

    except (FileNotFoundError, ValueError):
        raise
    except Exception as e:
        _logger.error(f"File verification failed: {e}")
        raise ValueError(f"Error verifying file: {e}") from e


def run() -> bool:
    """Main orchestration function for feature 255 phases 1-2.

    Coordinates content generation, validation, file creation, and file verification:

    Phase 1: Content Generation & Validation
      1a. Generate markdown content using LLM
      1b. Validate generated content meets all format requirements

    Phase 2: File Creation & Verification
      2a. Write validated content to disk using pathlib.Path
      2b. Verify file encoding, line endings, and structure

    Returns:
        True on success.

    Raises:
        ValueError: If validation fails.
        FileNotFoundError: If file operations fail.
        IOError: If disk write fails.
        Exception: If content generation or other operations fail.
    """
    _logger.info("Starting feature 255 phases 1-2: Content Generation, Validation, File Creation & Verification")

    try:
        # Phase 1a: Generate content
        _logger.info("Phase 1a: Generating markdown content")
        content = generate_content()

        # Phase 1b: Validate content
        _logger.info("Phase 1b: Validating generated content")
        validate_content(content)

        # Phase 2a: Write file
        _logger.info("Phase 2a: Writing markdown file to disk")
        write_file(content)

        # Phase 2b: Verify file
        _logger.info("Phase 2b: Verifying file encoding and structure")
        verify_file()

        _logger.info("✓ Feature 255 phases 1-2 completed successfully")
        return True

    except ValueError as e:
        _logger.error(f"Validation failed: {e}")
        raise
    except FileNotFoundError as e:
        _logger.error(f"File operation failed: {e}")
        raise
    except IOError as e:
        _logger.error(f"Disk write failed: {e}")
        raise
    except Exception as e:
        _logger.error(f"Feature 255 phases 1-2 failed: {e}")
        raise


if __name__ == "__main__":
    run()
