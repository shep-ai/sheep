"""Content generation utilities for creating markdown and other content."""

import re
from pathlib import Path

from sheep.config.llm import get_reasoning_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Prompt template for markdown generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following structure:
1. An H1 heading (using #) with a title about any topic you choose
2. A blank line
3. Exactly 2-3 sentences of coherent prose about that topic

Return ONLY the markdown content, no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""


def generate_markdown_content() -> str:
    """
    Generate markdown content with an H1 heading and 2-3 sentences of prose.

    Uses Claude API via CrewAI LLM framework to generate coherent,
    contextually-appropriate prose about any topic.

    Returns:
        String containing valid markdown with H1 heading and prose content.

    Raises:
        ValueError: If generated content doesn't meet format requirements.
        Exception: If LLM API call fails.
    """
    llm = get_reasoning_llm()
    _logger.info("Generating markdown content with reasoning LLM")

    try:
        # Call LLM with the prompt
        response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

        # Extract the response text
        if isinstance(response, dict):
            content = response.get("content", str(response))
        else:
            content = str(response)

        _logger.debug(f"Raw LLM response: {content[:100]}...")

        # Ensure trailing newline (Unix convention)
        if not content.endswith("\n"):
            content = content + "\n"

        # Validate the response format
        _validate_markdown_content(content)

        _logger.info("Markdown content generated successfully")
        return content

    except Exception as e:
        _logger.error(f"Failed to generate markdown content: {e}")
        raise


def _validate_markdown_content(content: str) -> None:
    """
    Validate that generated content meets markdown format requirements.

    Args:
        content: The generated markdown content to validate.

    Raises:
        ValueError: If content doesn't meet format requirements.
    """
    # Check that content is not empty
    if not content or not content.strip():
        raise ValueError("Generated content is empty")

    # Check for H1 heading
    if not content.lstrip().startswith("# "):
        raise ValueError("Content must start with H1 heading (# )")

    # Check that content has reasonable length
    if len(content) < 50:
        raise ValueError("Generated content is too short to be meaningful")

    # Check for sentence structure (count periods)
    sentence_count = content.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"Content should have 2-3 sentences, found {sentence_count}"
        )


def write_markdown_file(content: str, filename: str) -> str:
    """
    Write generated markdown content to a file at the repository root.

    Args:
        content: The markdown content to write.
        filename: The filename to create (e.g., "test-9veux3.md").

    Returns:
        Path to the created file as a string on success.

    Raises:
        ValueError: If content is invalid or file path is unsafe.
        IOError: If file write operation fails.
    """
    # Validate that filename is safe (not a path traversal)
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise ValueError(f"Invalid filename: {filename}")

    # Resolve the repository root (current working directory)
    repo_root = Path.cwd()
    file_path = repo_root / filename

    _logger.info(f"Writing markdown file to {file_path}")

    try:
        # Write file with UTF-8 encoding (handles LF line endings on Unix)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Verify file was created
        if not file_path.exists():
            raise IOError(f"File was not created: {file_path}")

        # Verify file has content
        file_size = file_path.stat().st_size
        if file_size == 0:
            raise IOError(f"File was created but is empty: {file_path}")

        _logger.info(
            f"Successfully wrote markdown file: {file_path} ({file_size} bytes)"
        )
        return str(file_path)

    except Exception as e:
        _logger.error(f"Failed to write markdown file: {e}")
        raise


def validate_markdown_file(filepath: str) -> bool:
    """
    Validate that a markdown file meets all non-functional requirements.

    Checks for:
    - Valid markdown syntax (H1 heading, blank line separator)
    - Proper prose content (2-3 sentences)
    - UTF-8 encoding with no BOM
    - Unix LF line endings (not CRLF)
    - Trailing newline

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
        raise IOError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise IOError(f"Path is not a file: {filepath}")

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

        _logger.info(f"Markdown file validation passed: {filepath}")
        return True

    except (IOError, ValueError):
        raise
    except Exception as e:
        _logger.error(f"Unexpected error during validation: {e}")
        raise IOError(f"Error validating file: {e}")
