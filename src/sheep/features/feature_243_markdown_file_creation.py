"""Implementation for feature 243: Create markdown file test-c2dbie.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 242 preceding features (001-242). The file is created with:
- Exact filename: test-c2dbie.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 400-600 bytes
- Git staging, commit, and push operations
"""

from pathlib import Path

from sheep.config.llm import get_reasoning_llm
from sheep.content_generators import (
    commit_markdown_file,
    push_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 243
FEATURE_NAME = "markdown-file-creation-1fde1c"
MARKDOWN_FILENAME = "test-c2dbie.md"

# Prompt template for prose generation
PROSE_GENERATION_PROMPT = """Generate 2-3 sentences of original prose about any topic you choose.
Use plain text only, no markdown formatting.
Content should be unique, grammatically correct, and meaningful.
Return ONLY the prose sentences, no additional text or explanation."""

TITLE_GENERATION_PROMPT = """Generate a brief, descriptive title (3-5 words) for a markdown document.
The title should be suitable for an H1 heading.
Return ONLY the title text, no markdown symbols, no explanation."""


def generate_prose_content() -> str:
    """
    Generate 2-3 sentences of original prose content using Claude API.

    Uses get_reasoning_llm() with temperature 0.2 for balanced quality and consistency.
    Returns plain text prose without markdown formatting.

    Returns:
        String containing 2-3 sentences of original prose (plain text only).

    Raises:
        ValueError: If content is invalid or doesn't meet sentence requirements.
        Exception: If LLM API call fails.
    """
    llm = get_reasoning_llm()
    _logger.info("Generating prose content with reasoning LLM")

    try:
        # Call LLM with prose generation prompt and temperature 0.2
        response = llm.call(
            [{"role": "user", "content": PROSE_GENERATION_PROMPT}],
            temperature=0.2,
        )

        # Extract the response text
        if isinstance(response, dict):
            content = str(response.get("content", str(response))).strip()
        else:
            content = str(response).strip()

        _logger.debug(f"Generated prose: {content[:100]}...")

        # Validate sentence count (2-3 sentences)
        sentence_count = content.count(".")
        if sentence_count < 2 or sentence_count > 3:
            raise ValueError(
                f"Generated prose must have 2-3 sentences, found {sentence_count}"
            )

        # Check for meaningful content length
        if len(content) < 50:
            raise ValueError("Generated prose is too short to be meaningful")

        _logger.info("Prose content generated successfully")
        return content

    except Exception as e:
        _logger.error(f"Failed to generate prose content: {e}")
        raise


def generate_title_content() -> str:
    """
    Generate a brief title for the markdown document using Claude API.

    Returns:
        String containing a brief, descriptive title.

    Raises:
        Exception: If LLM API call fails.
    """
    llm = get_reasoning_llm()
    _logger.info("Generating title with reasoning LLM")

    try:
        # Call LLM with title generation prompt
        response = llm.call(
            [{"role": "user", "content": TITLE_GENERATION_PROMPT}],
            temperature=0.2,
        )

        # Extract the response text
        if isinstance(response, dict):
            title = str(response.get("content", str(response))).strip()
        else:
            title = str(response).strip()

        # Clean up any markdown symbols that might have been included
        title = title.replace("# ", "").replace("#", "").strip()

        _logger.debug(f"Generated title: {title}")

        if not title:
            raise ValueError("Generated title is empty")

        _logger.info("Title generated successfully")
        return title

    except Exception as e:
        _logger.error(f"Failed to generate title: {e}")
        raise


def write_markdown_file(filename: str, title: str, content: str) -> str:
    """
    Write markdown file with H1 heading, blank line, and prose content.

    Creates a file at the repository root with proper structure:
    # Title

    <prose_content>

    Ensures UTF-8 encoding without BOM and LF line endings.

    Args:
        filename: Name of the file to create (e.g., "test-c2dbie.md").
        title: The H1 heading title.
        content: The 2-3 sentence prose content.

    Returns:
        Path to the created file as a string.

    Raises:
        ValueError: If filename or content is invalid.
        IOError: If file write operation fails.
    """
    # Validate filename
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise ValueError(f"Invalid filename: {filename}")

    # Get repository root (current working directory)
    repo_root = Path.cwd()
    file_path = repo_root / filename

    _logger.info(f"Writing markdown file to {file_path}")

    try:
        # Construct markdown content with proper structure
        # Note: Python's default newline handling on Unix is LF
        markdown_content = f"# {title}\n\n{content}\n"

        # Write file with UTF-8 encoding (no BOM by default)
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(markdown_content)

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


def validate_markdown_file(filepath: str) -> bool:
    """
    Validate that a markdown file meets all specification requirements.

    Checks for:
    - File exists and is readable
    - H1 heading at start (# Title)
    - Blank line after heading
    - 2-3 sentences in prose content
    - UTF-8 encoding without BOM
    - LF line endings (no CRLF)
    - Trailing newline
    - File size approximately 400-600 bytes

    Args:
        filepath: Path to the markdown file to validate.

    Returns:
        True if file passes all validation checks.

    Raises:
        ValueError: If file fails any validation check with descriptive message.
    """
    path = Path(filepath)

    if not path.exists():
        raise ValueError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    _logger.info(f"Validating markdown file: {filepath}")

    try:
        # Read file as binary to check encoding and line endings
        with open(path, "rb") as f:
            binary_content = f.read()

        # Check for UTF-8 BOM
        if binary_content.startswith(b"\xef\xbb\xbf"):
            raise ValueError("File has UTF-8 BOM (should not be present)")

        # Verify valid UTF-8
        try:
            text_content = binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"File is not valid UTF-8: {e}")

        # Check for CRLF line endings
        if b"\r\n" in binary_content:
            raise ValueError("File uses CRLF line endings (should use LF)")

        # Check for H1 heading at start
        if not text_content.lstrip().startswith("# "):
            raise ValueError("File must start with H1 heading (# )")

        lines = text_content.split("\n")

        # Check first line is H1 heading
        if not lines[0].startswith("# "):
            raise ValueError("First line must be H1 heading (# )")

        # Check second line is blank
        if len(lines) < 2 or lines[1] != "":
            raise ValueError("Second line must be blank (separator after heading)")

        # Get prose content (skip heading and blank line)
        prose_lines = lines[2:]

        # Remove trailing empty lines for validation
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        if not prose_lines:
            raise ValueError("No prose content found after heading")

        prose_content = "\n".join(prose_lines).strip()

        # Check sentence count (2-3 periods)
        sentence_count = prose_content.count(".")
        if sentence_count < 2 or sentence_count > 3:
            raise ValueError(
                f"Content must have 2-3 sentences, found {sentence_count}"
            )

        # Check for trailing newline
        if not text_content.endswith("\n"):
            raise ValueError("File must end with trailing newline")

        # Check file size (log warning if outside range, don't fail)
        file_size = len(binary_content)
        if file_size < 400 or file_size > 600:
            _logger.warning(
                f"File size {file_size} bytes is outside expected range 400-600 bytes"
            )

        _logger.info(f"Markdown file validation passed: {filepath}")
        return True

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Unexpected error during validation: {e}")
        raise ValueError(f"Error validating file: {e}")


def create_feature_243_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 243.

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
        # Task 1: Generate title and prose content
        _logger.info("Task 1: Generating title and prose content")
        title = generate_title_content()
        prose = generate_prose_content()
        _logger.debug(f"Generated title: {title}")
        _logger.debug(f"Generated prose: {len(prose)} bytes")

        # Task 2: Write file to disk with proper encoding
        _logger.info("Task 2: Writing markdown file to disk")
        filepath = write_markdown_file(MARKDOWN_FILENAME, title, prose)
        _logger.debug(f"File written to: {filepath}")

        # Task 3: Validate file meets all specification requirements
        _logger.info("Task 3: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Construct full markdown content for commit
        full_content = f"# {title}\n\n{prose}\n"

        # Task 4: Stage and commit file with exact conventional message
        _logger.info("Task 4: Staging and committing file")
        commit_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
        _logger.debug(f"Using commit message: {commit_message}")
        commit_result = commit_markdown_file(filepath, full_content, repo_path, custom_message=commit_message)
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
            "content": full_content,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


if __name__ == "__main__":
    """Execute feature 243 when run as a script."""
    result = create_feature_243_markdown_file()
    print("Feature 243 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
