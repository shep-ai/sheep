"""Implementation for feature 205: Create markdown file test-m6zeml.md with title and prose content.

This module orchestrates the creation of a markdown file with hard-coded, deterministic content.
Unlike feature 204 which uses Claude API for dynamic generation, feature 205 uses hard-coded
content to demonstrate straightforward file creation within the Sheep workflow without external
API dependencies.

The file is created with:
- Exact filename: test-m6zeml.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations

This approach provides:
- Deterministic output (identical on repeated execution)
- Transparent, auditable content (no API dependencies)
- Simplified error handling (no network failures)
- Faster execution (no API latency)
- Reliable testing and review (reproducible results)
"""

import subprocess
from pathlib import Path

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 205 constants
FILENAME = "test-m6zeml.md"
FEATURE_NUMBER = 205
BRANCH_NAME = "feat/205-markdown-file-creation-870df7"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME}"

# Hard-coded markdown content
# H1 title about the chosen topic
TITLE_TEXT = "The Importance of Code Documentation"

# 2-3 sentences of prose content related to the title
PROSE_CONTENT = (
    "Effective documentation is essential for code maintainability and team collaboration. "
    "Clear, concise documentation helps new team members onboard quickly and reduces cognitive "
    "load for future developers. Writing good documentation is an investment that pays dividends "
    "throughout a project's lifecycle."
)


def create_markdown_file() -> Path:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings via pathlib.Path.write_text().

    Returns:
        Path object pointing to created file

    Raises:
        ValueError: If file creation fails
        OSError: If file write operation fails
    """
    _logger.info(f"Creating markdown file: {FILENAME}")

    try:
        # Construct markdown content: # Title \n \n Prose
        markdown_content = f"# {TITLE_TEXT}\n\n{PROSE_CONTENT}\n"

        # Write file with UTF-8 encoding and LF line endings
        file_path = Path(FILENAME)
        file_path.write_text(markdown_content, encoding="utf-8")

        # Verify file was created
        if not file_path.exists():
            raise OSError(f"File was not created: {file_path}")

        file_size = file_path.stat().st_size
        _logger.info(f"Successfully created {FILENAME} ({file_size} bytes)")

        return file_path

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


def verify_file_exists(filename: str = FILENAME) -> None:
    """Verify that the markdown file exists.

    Args:
        filename: Path to file to verify (defaults to FILENAME)

    Raises:
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Checking file exists: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")


def validate_markdown_format(filename: str = FILENAME) -> None:
    """Validate markdown file structure: H1 heading, blank line, prose.

    Checks that:
    1. File starts with exactly one H1 heading (# Title)
    2. Line 2 is blank (separator between heading and prose)
    3. Exactly one H1 heading exists in the file

    Args:
        filename: Path to markdown file to validate

    Raises:
        ValueError: If markdown format is invalid
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating markdown format: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Check first line is H1 heading
    if not lines or not lines[0].startswith("# "):
        raise ValueError("File must start with H1 heading (# Title)")

    # Check second line is blank (blank line separator)
    if len(lines) < 2 or lines[1].strip() != "":
        raise ValueError("Second line must be blank (separator between heading and prose)")

    # Check exactly one H1 heading exists
    h1_count = sum(1 for line in lines if line.startswith("# ") and not line.startswith("# #"))
    if h1_count != 1:
        raise ValueError(f"File must contain exactly one H1 heading, found {h1_count}")


def extract_prose_content(filename: str = FILENAME) -> str:
    """Extract prose content from markdown file.

    Extracts the text content that appears after the H1 heading and blank line.
    This helper function is used by other validation functions.

    Args:
        filename: Path to markdown file

    Returns:
        Prose content as string (empty if no prose found)

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file structure is invalid
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Find blank line after heading (should be at index 1)
    blank_line_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "" and i > 0:
            blank_line_idx = i
            break

    if blank_line_idx is None:
        raise ValueError("No blank line separator found after heading")

    # Extract prose content (all lines after blank line)
    prose_lines = lines[blank_line_idx + 1:]
    prose_text = "\n".join(prose_lines).strip()

    return prose_text


def count_sentences(prose: str) -> int:
    """Count sentences in prose text using period counting.

    Counts the number of periods (.) in the prose content. This is a simple
    but effective approach for validating sentence count in typical prose.

    Args:
        prose: Text content to count sentences in

    Returns:
        Number of periods found in the prose

    Raises:
        ValueError: If prose is empty
    """
    if not prose:
        raise ValueError("Prose content is empty")

    return prose.count(".")


def validate_sentence_count(filename: str = FILENAME) -> None:
    """Validate file contains exactly 2-3 sentences of prose.

    Extracts prose content and counts periods to validate exactly 2-3 sentences.
    This function uses the extract_prose_content() and count_sentences() helpers.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If sentence count is not 2-3
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating sentence count: {filename}")
    prose_text = extract_prose_content(filename)
    sentence_count = count_sentences(prose_text)

    if not (2 <= sentence_count <= 3):
        raise ValueError(f"Expected 2-3 sentences, found {sentence_count}")


def validate_encoding(filename: str = FILENAME) -> None:
    """Validate file is UTF-8 encoded without BOM.

    Checks that:
    1. File does not start with UTF-8 BOM (byte order mark)
    2. File can be decoded as valid UTF-8

    Args:
        filename: Path to file to validate

    Raises:
        ValueError: If file has BOM or is not valid UTF-8
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating encoding: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    binary_content = file_path.read_bytes()

    # Check for UTF-8 BOM
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File contains UTF-8 BOM (byte order mark)")

    # Verify UTF-8 encoding
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File contains invalid UTF-8 encoding: {e}") from e


def validate_line_endings(filename: str = FILENAME) -> None:
    """Validate file uses Unix LF line endings exclusively.

    Checks that:
    1. File does not contain CRLF (\\r\\n) Windows line endings
    2. File does not contain CR (\\r) Mac line endings
    3. File uses only LF (\\n) Unix line endings

    Args:
        filename: Path to file to validate

    Raises:
        ValueError: If file contains CRLF or CR line endings
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating line endings: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    binary_content = file_path.read_bytes()

    if b"\r\n" in binary_content:
        raise ValueError("File contains Windows CRLF (\\r\\n) line endings")

    if b"\r" in binary_content:
        raise ValueError("File contains Mac CR (\\r) line endings")


def validate_file_size(filename: str = FILENAME, min_bytes: int = 250, max_bytes: int = 600) -> None:
    """Validate file size is within acceptable range.

    Checks that file size is between min_bytes and max_bytes (inclusive).
    Default range: 250-600 bytes (per specification).

    Args:
        filename: Path to file to validate
        min_bytes: Minimum acceptable file size in bytes (default: 250)
        max_bytes: Maximum acceptable file size in bytes (default: 600)

    Raises:
        ValueError: If file size is outside the acceptable range
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating file size: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    file_size = file_path.stat().st_size

    if not (min_bytes <= file_size <= max_bytes):
        raise ValueError(
            f"File size {file_size} bytes outside acceptable range {min_bytes}-{max_bytes} bytes"
        )


def validate_markdown_file(filename: str = FILENAME) -> None:
    """Comprehensive validation pipeline for markdown file.

    Runs all validation checks required by the specification:
    1. File exists at the specified path
    2. Markdown format is valid (H1 heading, blank line, prose)
    3. Sentence count is exactly 2-3
    4. File encoding is UTF-8 without BOM
    5. File uses Unix LF line endings
    6. File size is 250-600 bytes

    This function validates all success criteria and fails fast on the first
    error, providing clear error messages for debugging.

    Args:
        filename: Path to markdown file to validate

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If any validation check fails
    """
    _logger.info(f"Starting comprehensive validation pipeline for {filename}")

    try:
        # Check 1: File exists
        _logger.info("Check 1: Verifying file exists")
        verify_file_exists(filename)
        _logger.debug(f"✓ File exists: {filename}")

        # Check 2: Markdown format (H1 heading, blank line, prose)
        _logger.info("Check 2: Validating markdown format")
        validate_markdown_format(filename)
        _logger.debug("✓ Markdown format is valid")

        # Check 3: Sentence count (2-3 sentences)
        _logger.info("Check 3: Validating sentence count")
        validate_sentence_count(filename)
        _logger.debug("✓ Sentence count is valid (2-3)")

        # Check 4: UTF-8 encoding without BOM
        _logger.info("Check 4: Validating file encoding")
        validate_encoding(filename)
        _logger.debug("✓ File encoding is valid UTF-8 without BOM")

        # Check 5: Unix LF line endings
        _logger.info("Check 5: Validating line endings")
        validate_line_endings(filename)
        _logger.debug("✓ File uses Unix LF line endings")

        # Check 6: File size (250-600 bytes)
        _logger.info("Check 6: Validating file size")
        validate_file_size(filename)
        _logger.debug("✓ File size is within valid range")

        _logger.info(f"All validation checks passed for {filename}")

    except FileNotFoundError as e:
        _logger.error(f"File validation failed - file not found: {e}")
        raise
    except ValueError as e:
        _logger.error(f"File validation failed: {e}")
        raise


def git_add_file(filename: str = FILENAME) -> None:
    """Stage the markdown file for commit using git add.

    Executes `git add <filename>` to stage the file for the next commit.
    Uses subprocess.run() with shell=False for security and fail-fast behavior.

    Args:
        filename: Path to file to stage (defaults to FILENAME)

    Raises:
        subprocess.CalledProcessError: If git add command fails
        OSError: If git command is not available
    """
    _logger.info(f"Staging file with git add: {filename}")

    try:
        subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug(f"✓ Successfully staged {filename}")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Git add failed: {e.stderr}")
        raise


def git_commit(commit_message: str = COMMIT_MESSAGE) -> None:
    """Create a git commit with the specified message.

    Executes `git commit -m <message>` to commit staged changes.
    Uses subprocess.run() with shell=False for security and fail-fast behavior.

    Args:
        commit_message: Commit message following conventional commits format

    Raises:
        subprocess.CalledProcessError: If git commit command fails
        OSError: If git command is not available
    """
    _logger.info(f"Creating commit with message: {commit_message}")

    try:
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug("✓ Successfully created commit")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Git commit failed: {e.stderr}")
        raise


def git_push(branch_name: str = BRANCH_NAME) -> None:
    """Push the commit to the remote repository.

    Executes `git push -u origin <branch>` to push the branch to the remote.
    The -u flag establishes tracking for the branch.
    Uses subprocess.run() with shell=False for security and fail-fast behavior.

    Args:
        branch_name: Branch name to push to (defaults to BRANCH_NAME)

    Raises:
        subprocess.CalledProcessError: If git push command fails
        OSError: If git command is not available
    """
    _logger.info(f"Pushing branch to remote: {branch_name}")

    try:
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug(f"✓ Successfully pushed branch {branch_name}")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Git push failed: {e.stderr}")
        raise


def main() -> int:
    """Orchestration function for complete feature 205 workflow.

    Coordinates the following steps:
    1. Create markdown file with hard-coded content
    2. Validate file meets all specification requirements
    3. Stage file with git add
    4. Commit file with conventional commit message
    5. Push commit to remote branch

    Returns:
        0 on success, 1 on any failure (fail-fast principle).

    Logs all major workflow steps and validation results.
    """
    _logger.info("Starting feature 205 implementation workflow")

    try:
        # Phase 1: Create markdown file
        _logger.info("Phase 1: Creating markdown file")
        create_markdown_file()

        # Phase 2: Validate file
        _logger.info("Phase 2: Validating markdown file")
        validate_markdown_file()

        # Phase 3: Git operations
        _logger.info("Phase 3: Executing git operations")
        git_add_file()
        git_commit()
        git_push()

        _logger.info("✓ Feature 205 implementation completed successfully")
        return 0

    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as e:
        _logger.error(f"Feature 205 workflow failed: {e}")
        return 1
    except Exception as e:
        _logger.error(f"Unexpected error in feature 205 workflow: {e}")
        return 1


if __name__ == "__main__":
    main()
