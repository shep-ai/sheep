"""Implementation for feature 205: Create markdown file test-grk9g8.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from prior features. The file is created with:
- Exact filename: test-grk9g8.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations
"""

import subprocess
import sys
from pathlib import Path

from sheep.config.llm import create_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 205 constants
FILENAME = "test-grk9g8.md"
FEATURE_NUMBER = 205
BRANCH_NAME = "feat/205-markdown-file-creation-4759f4"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with title and prose content"

# Prompt template for deterministic markdown content generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following requirements:
1. Create an H1 heading (format: # Title) on a topic of your choice
2. Write exactly 2-3 sentences of meaningful, coherent prose about that topic
3. Ensure the prose is thematically related to the title

Return ONLY the markdown content with no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""


def generate_prose(feature_number: int = FEATURE_NUMBER) -> str:
    """Generate 2-3 sentences of prose content using Claude API.

    Uses Claude API with temperature=0 for deterministic, reproducible output.
    Same feature input produces identical prose output on repeated calls.

    Args:
        feature_number: Feature number to seed generation (default: 205)

    Returns:
        String containing 2-3 sentences of meaningful, coherent prose

    Raises:
        ValueError: If generated prose is invalid or doesn't meet requirements
        Exception: If Claude API call fails
    """
    _logger.info("Generating prose content using Claude API (temperature=0)")

    try:
        # Create LLM with temperature=0 for deterministic generation
        llm = create_llm(temperature=0)

        # Call Claude API with the generation prompt
        response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

        # Extract response text
        if isinstance(response, dict):
            content = str(response.get("content", str(response)))
        else:
            content = str(response)

        _logger.debug(f"Raw LLM response (first 100 chars): {content[:100]}...")

        # Parse prose from markdown content (second paragraph after blank line)
        lines = content.strip().split("\n")

        # Find blank line separator (should be after title)
        blank_line_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "" and i > 0:
                blank_line_idx = i
                break

        if blank_line_idx is None:
            raise ValueError("Generated content missing blank line separator after heading")

        # Extract prose content (all lines after blank line)
        prose_lines = lines[blank_line_idx + 1:]
        prose = "\n".join(prose_lines).strip()

        if not prose:
            raise ValueError("Generated prose content is empty")

        # Validate sentence count
        sentence_count = prose.count(".")
        if not (2 <= sentence_count <= 3):
            raise ValueError(
                f"Generated prose has {sentence_count} sentences, expected 2-3"
            )

        _logger.info(f"Successfully generated prose with {sentence_count} sentences")
        return prose

    except Exception as e:
        _logger.error(f"Failed to generate prose: {e}")
        raise


def generate_title(feature_number: int = FEATURE_NUMBER) -> str:
    """Generate H1 markdown title using Claude API.

    Uses Claude API with temperature=0 for deterministic, reproducible output.
    Same feature input produces identical title output on repeated calls.

    Args:
        feature_number: Feature number to seed generation (default: 205)

    Returns:
        String containing H1 markdown heading (without # prefix)

    Raises:
        ValueError: If generated title is invalid
        Exception: If Claude API call fails
    """
    _logger.info("Generating title using Claude API (temperature=0)")

    try:
        # Create LLM with temperature=0 for deterministic generation
        llm = create_llm(temperature=0)

        # Call Claude API with the generation prompt
        response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

        # Extract response text
        if isinstance(response, dict):
            content = str(response.get("content", str(response)))
        else:
            content = str(response)

        _logger.debug(f"Raw LLM response (first 100 chars): {content[:100]}...")

        # Parse title from markdown content (first line should be H1)
        lines = content.strip().split("\n")

        if not lines or not lines[0].startswith("# "):
            raise ValueError("Generated content must start with H1 heading (# Title)")

        # Extract title (remove # prefix and whitespace)
        title = lines[0].replace("# ", "").strip()

        if not title:
            raise ValueError("Generated title is empty")

        _logger.info(f"Successfully generated title: '{title}'")
        return title

    except Exception as e:
        _logger.error(f"Failed to generate title: {e}")
        raise


def create_markdown_file(filename: str = FILENAME) -> str:
    """Create markdown file with H1 title and 2-3 sentences of prose.

    Generates title and prose content, constructs markdown file with proper format,
    writes to disk using UTF-8 encoding and Unix LF line endings.

    Args:
        filename: Filename for markdown file (default: FILENAME constant)

    Returns:
        Absolute path to created file as string

    Raises:
        FileExistsError: If file already exists
        OSError: If file creation fails
        ValueError: If content generation fails
    """
    _logger.info(f"Creating markdown file: {filename}")

    try:
        # Check if file already exists
        file_path = Path(filename)
        if file_path.exists():
            raise FileExistsError(f"File already exists: {filename}")

        # Generate title and prose
        _logger.debug("Generating title and prose content")
        title = generate_title()
        prose = generate_prose()

        # Construct markdown content: # Title\n\nProse\n
        markdown_content = f"# {title}\n\n{prose}\n"

        _logger.debug(f"Markdown content ({len(markdown_content)} bytes): {markdown_content[:100]}...")

        # Write file with UTF-8 encoding (Unix LF line endings by default on Unix)
        file_path.write_text(markdown_content, encoding="utf-8")

        # Verify file was created
        if not file_path.exists():
            raise OSError(f"File was not created: {filename}")

        file_size = file_path.stat().st_size
        _logger.info(f"Successfully created {filename} ({file_size} bytes)")

        return str(file_path.absolute())

    except (FileExistsError, OSError):
        raise
    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


def verify_file_exists(filename: str = FILENAME) -> None:
    """Verify markdown file exists.

    Args:
        filename: Filename to check

    Raises:
        FileNotFoundError: If file does not exist
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")


def validate_markdown_format(filename: str = FILENAME) -> None:
    """Validate markdown file structure.

    Checks:
    - First line is H1 heading (starts with "# ")
    - Second line is blank
    - Exactly one H1 heading exists

    Args:
        filename: File to validate

    Raises:
        ValueError: If markdown structure is invalid
    """
    _logger.debug(f"Validating markdown format: {filename}")

    try:
        file_path = Path(filename)
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        if not lines:
            raise ValueError("File is empty")

        # Check first line is H1 heading
        if not lines[0].startswith("# "):
            raise ValueError(f"First line must be H1 heading (# ...), got: {lines[0][:50]}")

        # Check second line is blank
        if len(lines) < 2 or lines[1] != "":
            raise ValueError("Second line must be blank (separator after heading)")

        # Count H1 headings (lines starting with "# " but not "# #")
        h1_count = sum(1 for line in lines if line.startswith("# ") and not line.startswith("# #"))
        if h1_count != 1:
            raise ValueError(f"Expected exactly one H1 heading, found {h1_count}")

        _logger.debug("Markdown format validation passed")

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Error validating markdown format: {e}")
        raise ValueError(f"Failed to validate markdown format: {e}") from e


def validate_encoding(filename: str = FILENAME) -> None:
    """Validate UTF-8 encoding without BOM.

    Checks:
    - File is valid UTF-8
    - No UTF-8 BOM present

    Args:
        filename: File to validate

    Raises:
        ValueError: If encoding is invalid
    """
    _logger.debug(f"Validating encoding: {filename}")

    try:
        file_path = Path(filename)
        binary_content = file_path.read_bytes()

        # Check for UTF-8 BOM
        if binary_content.startswith(b"\xef\xbb\xbf"):
            raise ValueError("File has UTF-8 BOM (Byte Order Mark) - should not be present")

        # Check if valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"File is not valid UTF-8: {e}") from e

        _logger.debug("Encoding validation passed")

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Error validating encoding: {e}")
        raise ValueError(f"Failed to validate encoding: {e}") from e


def verify_utf8_encoding(filename: str = FILENAME) -> None:
    """Backward-compatibility wrapper for validate_encoding."""
    validate_encoding(filename)


def validate_line_endings(filename: str = FILENAME) -> None:
    """Validate Unix LF line endings only.

    Checks:
    - No CRLF (Windows) line endings
    - No CR (old Mac) line endings
    - Only LF (Unix) line endings

    Args:
        filename: File to validate

    Raises:
        ValueError: If line endings are not Unix LF
    """
    _logger.debug(f"Validating line endings: {filename}")

    try:
        file_path = Path(filename)
        binary_content = file_path.read_bytes()

        # Check for CRLF first (Windows line endings)
        if b"\r\n" in binary_content:
            raise ValueError("File has CRLF (Windows) line endings - should use Unix LF only")

        # Check for CR (old Mac line endings)
        if b"\r" in binary_content:
            raise ValueError("File has CR (old Mac) line endings - should use Unix LF only")

        _logger.debug("Line endings validation passed")

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Error validating line endings: {e}")
        raise ValueError(f"Failed to validate line endings: {e}") from e


def verify_lf_line_endings(filename: str = FILENAME) -> None:
    """Backward-compatibility wrapper for validate_line_endings."""
    validate_line_endings(filename)


def validate_file_size(
    filename: str = FILENAME, min_bytes: int = 250, max_bytes: int = 600
) -> None:
    """Validate file size is within range.

    Args:
        filename: File to validate
        min_bytes: Minimum file size in bytes (default: 250)
        max_bytes: Maximum file size in bytes (default: 600)

    Raises:
        ValueError: If file size is outside range
    """
    _logger.debug(f"Validating file size: {filename}")

    try:
        file_path = Path(filename)
        file_size = file_path.stat().st_size

        if file_size < min_bytes or file_size > max_bytes:
            raise ValueError(
                f"File size {file_size} bytes is outside range [{min_bytes}, {max_bytes}]"
            )

        _logger.debug(f"File size validation passed ({file_size} bytes)")

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Error validating file size: {e}")
        raise ValueError(f"Failed to validate file size: {e}") from e


def verify_file_size(
    filename: str = FILENAME, min_bytes: int = 250, max_bytes: int = 600
) -> None:
    """Backward-compatibility wrapper for validate_file_size."""
    validate_file_size(filename, min_bytes, max_bytes)


def extract_prose_content(filename: str = FILENAME) -> str:
    """Extract prose content from markdown file.

    Finds the first blank line after heading and returns content after it.

    Args:
        filename: File to extract from

    Returns:
        Prose content string

    Raises:
        ValueError: If prose content cannot be extracted
    """
    try:
        file_path = Path(filename)
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Find blank line after heading
        blank_line_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "" and i > 0:
                blank_line_idx = i
                break

        if blank_line_idx is None:
            raise ValueError("No blank line separator found after heading")

        # Extract content after blank line
        prose_lines = lines[blank_line_idx + 1:]
        prose = "\n".join(prose_lines).strip()

        if not prose:
            raise ValueError("Prose content is empty")

        return prose

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Error extracting prose content: {e}")
        raise ValueError(f"Failed to extract prose content: {e}") from e


def count_sentences(prose: str) -> int:
    """Count sentences in prose (by counting periods).

    Args:
        prose: Prose text to count sentences in

    Returns:
        Number of sentences (period count)

    Raises:
        ValueError: If prose is empty
    """
    if not prose or not prose.strip():
        raise ValueError("Prose content is empty")

    return prose.count(".")


def validate_sentence_count(filename: str = FILENAME) -> None:
    """Validate prose contains exactly 2-3 sentences.

    Args:
        filename: File to validate

    Raises:
        ValueError: If sentence count is not 2-3
    """
    _logger.debug(f"Validating sentence count: {filename}")

    try:
        prose = extract_prose_content(filename)
        sentence_count = count_sentences(prose)

        if not (2 <= sentence_count <= 3):
            raise ValueError(
                f"Expected 2-3 sentences, found {sentence_count}"
            )

        _logger.debug(f"Sentence count validation passed ({sentence_count} sentences)")

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Error validating sentence count: {e}")
        raise ValueError(f"Failed to validate sentence count: {e}") from e


def verify_prose_content(filename: str = FILENAME) -> None:
    """Backward-compatibility wrapper for validate_sentence_count."""
    validate_sentence_count(filename)


def validate_markdown_file(filename: str = FILENAME) -> None:
    """Comprehensive validation pipeline for markdown file.

    Runs all validators in sequence, failing on first error.

    Validators (in order):
    1. File exists
    2. Markdown format (H1, blank line, single heading)
    3. Sentence count (2-3 sentences)
    4. UTF-8 encoding without BOM
    5. Unix LF line endings
    6. File size (250-600 bytes)

    Args:
        filename: File to validate

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If any validation fails
    """
    _logger.info(f"Starting comprehensive validation: {filename}")

    try:
        # Validator 1: File exists
        _logger.debug("Check 1: Verifying file exists")
        verify_file_exists(filename)

        # Validator 2: Markdown format
        _logger.debug("Check 2: Validating markdown format")
        validate_markdown_format(filename)

        # Validator 3: Sentence count
        _logger.debug("Check 3: Validating sentence count")
        validate_sentence_count(filename)

        # Validator 4: Encoding
        _logger.debug("Check 4: Validating UTF-8 encoding")
        validate_encoding(filename)

        # Validator 5: Line endings
        _logger.debug("Check 5: Validating Unix LF line endings")
        validate_line_endings(filename)

        # Validator 6: File size
        _logger.debug("Check 6: Validating file size")
        validate_file_size(filename)

        _logger.info(f"All validation checks passed for: {filename}")

    except (FileNotFoundError, ValueError):
        raise
    except Exception as e:
        _logger.error(f"Unexpected error during validation: {e}")
        raise


def git_add_file(filename: str = FILENAME) -> None:
    """Stage file with git add.

    Args:
        filename: Filename to stage (default: FILENAME constant)

    Raises:
        subprocess.CalledProcessError: If git add fails
    """
    _logger.info(f"Staging file with git add: {filename}")

    try:
        result = subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.info(f"Successfully staged file: {filename}")
        if result.stdout:
            _logger.debug(f"git add stdout: {result.stdout}")

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        _logger.error(f"Failed to stage file: {error_msg}")
        raise


def git_commit(filename: str = FILENAME, message: str = COMMIT_MESSAGE) -> None:
    """Create git commit with specified message.

    Args:
        filename: Filename being committed (used for logging, not in command)
        message: Commit message to use (default: COMMIT_MESSAGE constant)

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    _logger.info(f"Creating git commit: {message}")

    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.info(f"Successfully committed: {message}")
        if result.stdout:
            _logger.debug(f"git commit stdout: {result.stdout}")

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        _logger.error(f"Failed to commit: {error_msg}")
        raise


def git_push(branch: str = BRANCH_NAME) -> None:
    """Push commits to remote feature branch.

    Args:
        branch: Branch name to push to (default: BRANCH_NAME constant)

    Raises:
        subprocess.CalledProcessError: If git push fails
    """
    _logger.info(f"Pushing to remote branch: {branch}")

    try:
        result = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.info(f"Successfully pushed to branch: {branch}")
        if result.stdout:
            _logger.debug(f"git push stdout: {result.stdout}")

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        _logger.error(f"Failed to push to branch: {error_msg}")
        raise


def main() -> int:
    """Orchestration function for feature 205.

    Coordinates complete workflow:
    1. Create markdown file with generated content
    2. Validate file against all requirements
    3. Stage file with git add
    4. Commit with conventional message
    5. Push to feature branch

    Returns:
        0 on success, 1 on failure
    """
    _logger.info(f"Starting Feature 205: {FILENAME} creation")

    try:
        # Step 1: Create markdown file
        _logger.info("Phase 1: Creating markdown file")
        file_path = create_markdown_file(FILENAME)
        _logger.info(f"File created: {file_path}")

        # Step 2: Validate file
        _logger.info("Phase 2: Validating markdown file")
        validate_markdown_file(FILENAME)
        _logger.info("Validation passed")

        # Step 3: Stage file with git
        _logger.info("Phase 3: Staging file with git")
        git_add_file(FILENAME)

        # Step 4: Commit with conventional message
        _logger.info("Phase 4: Committing file")
        git_commit(FILENAME, COMMIT_MESSAGE)

        # Step 5: Push to feature branch
        _logger.info("Phase 5: Pushing to feature branch")
        git_push(BRANCH_NAME)

        _logger.info("Feature 205 completed successfully")
        return 0

    except FileExistsError as e:
        _logger.error(f"File already exists: {e}")
        return 1
    except FileNotFoundError as e:
        _logger.error(f"File not found: {e}")
        return 1
    except ValueError as e:
        _logger.error(f"Validation error: {e}")
        return 1
    except subprocess.CalledProcessError as e:
        _logger.error(f"Git operation failed: {e.stderr if e.stderr else str(e)}")
        return 1
    except OSError as e:
        _logger.error(f"File system error: {e}")
        return 1
    except Exception as e:
        _logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
