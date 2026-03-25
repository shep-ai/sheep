"""Implementation for feature 205: Create markdown file test-axs39z.md with title and prose content.

This module orchestrates the creation of a markdown file with hardcoded content following the
established pattern from prior features. The file is created with:
- Exact filename: test-axs39z.md
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

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 205 constants
FILENAME = "test-axs39z.md"
TITLE = "Markdown File Creation"
PROSE_CONTENT = "This feature demonstrates markdown file creation with validation. The implementation uses Python pathlib for file operations and subprocess for git integration. All validation occurs before git operations to maintain repository quality."
FEATURE_NUMBER = 205
BRANCH_NAME = "feat/205-markdown-file-creation-e38c99"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): create markdown file {FILENAME} with prose content"


def _validate_file_exists(filename: str) -> None:
    """Validate that file exists immediately after creation.

    Args:
        filename: Path to file to validate

    Raises:
        ValueError: If file does not exist
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise ValueError(f"File {filename} was not created")


def create_markdown_file(filename: str = FILENAME, title: str = TITLE, prose: str = PROSE_CONTENT) -> str:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings via pathlib.Path.write_text().

    Args:
        filename: Name of file to create (defaults to FILENAME)
        title: H1 heading title (defaults to TITLE)
        prose: Prose content (defaults to PROSE_CONTENT)

    Returns:
        Absolute path to created file

    Raises:
        FileExistsError: If file already exists
        ValueError: If file write or validation fails
    """
    _logger.info(f"Creating markdown file: {filename}")

    try:
        # Check file doesn't already exist
        file_path = Path(filename)
        if file_path.exists():
            raise FileExistsError(f"File {filename} already exists")

        # Construct markdown content
        content = f"# {title}\n\n{prose}\n"

        # Write file with UTF-8 encoding and LF line endings
        _logger.info(f"Writing file to {file_path}")
        file_path.write_text(content, encoding="utf-8")

        # Verify file was created
        _validate_file_exists(filename)

        file_size = file_path.stat().st_size
        _logger.info(f"Successfully created {filename} ({file_size} bytes)")

        return str(file_path.absolute())

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
    prose_text = extract_prose_content(filename)
    sentence_count = count_sentences(prose_text)

    if not (2 <= sentence_count <= 3):
        raise ValueError(
            f"Expected 2-3 sentences, found {sentence_count}"
        )


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
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    binary_content = file_path.read_bytes()

    if b"\r\n" in binary_content:
        raise ValueError("File contains Windows CRLF (\\r\\n) line endings")

    if b"\r" in binary_content:
        raise ValueError("File contains Mac CR (\\r) line endings")


def validate_file_size(filename: str = FILENAME, min_bytes: int = 300, max_bytes: int = 600) -> None:
    """Validate file size is within acceptable range.

    Checks that file size is between min_bytes and max_bytes (inclusive).
    Default range: 300-600 bytes (per specification).

    Args:
        filename: Path to file to validate
        min_bytes: Minimum acceptable file size in bytes (default: 300)
        max_bytes: Maximum acceptable file size in bytes (default: 600)

    Raises:
        ValueError: If file size is outside the acceptable range
        FileNotFoundError: If file does not exist
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    file_size = file_path.stat().st_size

    if not (min_bytes <= file_size <= max_bytes):
        raise ValueError(
            f"File size {file_size} bytes outside acceptable range {min_bytes}-{max_bytes} bytes"
        )


def validate_trailing_newline(filename: str = FILENAME) -> None:
    """Validate file ends with a newline character.

    Args:
        filename: Path to file to validate

    Raises:
        ValueError: If file does not end with newline
        FileNotFoundError: If file does not exist
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")

    if not content.endswith("\n"):
        raise ValueError("File must end with a newline character")


def validate_markdown_file(filename: str = FILENAME) -> None:
    """Comprehensive validation pipeline for markdown file.

    Runs all validation checks required by the specification:
    1. File exists at the specified path
    2. Markdown format is valid (H1 heading, blank line, prose)
    3. Sentence count is exactly 2-3
    4. File encoding is UTF-8 without BOM
    5. File uses Unix LF line endings
    6. File size is 300-600 bytes
    7. File ends with trailing newline

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

        # Check 6: File size (300-600 bytes)
        _logger.info("Check 6: Validating file size")
        validate_file_size(filename)
        _logger.debug("✓ File size is within valid range")

        # Check 7: Trailing newline
        _logger.info("Check 7: Validating trailing newline")
        validate_trailing_newline(filename)
        _logger.debug("✓ File ends with newline")

        _logger.info(f"All validation checks passed for {filename}")

    except FileNotFoundError as e:
        _logger.error(f"File validation failed - file not found: {e}")
        raise
    except ValueError as e:
        _logger.error(f"File validation failed: {e}")
        raise


def git_add_file(filename: str = FILENAME) -> None:
    """Stage file for commit using git add.

    Args:
        filename: Path to file to stage (defaults to FILENAME)

    Raises:
        subprocess.CalledProcessError: If git add fails
    """
    _logger.info(f"Staging file with git: {filename}")

    try:
        result = subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.info(f"Successfully staged {filename}")
    except subprocess.CalledProcessError as e:
        error_msg = f"git add failed: {e.stderr or e.stdout}"
        _logger.error(error_msg)
        raise subprocess.CalledProcessError(
            e.returncode, e.cmd, output=error_msg
        ) from e


def git_commit(filename: str = FILENAME, message: str = COMMIT_MESSAGE) -> None:
    """Create a commit with conventional commit message.

    Args:
        filename: Name of file being committed (for logging)
        message: Commit message (defaults to COMMIT_MESSAGE)

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    _logger.info(f"Creating commit: {message}")

    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.info(f"Successfully committed changes")
    except subprocess.CalledProcessError as e:
        error_msg = f"git commit failed: {e.stderr or e.stdout}"
        _logger.error(error_msg)
        raise subprocess.CalledProcessError(
            e.returncode, e.cmd, output=error_msg
        ) from e


def git_push(branch: str = BRANCH_NAME) -> None:
    """Push changes to remote branch.

    Args:
        branch: Branch name to push to (defaults to BRANCH_NAME)

    Raises:
        subprocess.CalledProcessError: If git push fails
    """
    _logger.info(f"Pushing to branch: {branch}")

    try:
        result = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.info(f"Successfully pushed to {branch}")
    except subprocess.CalledProcessError as e:
        error_msg = f"git push failed: {e.stderr or e.stdout}"
        _logger.error(error_msg)
        raise subprocess.CalledProcessError(
            e.returncode, e.cmd, output=error_msg
        ) from e


def main() -> None:
    """Main orchestration function for feature 205 (all phases).

    Executes the complete workflow:
    1. Create markdown file with hardcoded content
    2. Validate all success criteria before committing
    3. Stage file with git add
    4. Create commit with conventional message
    5. Push to feature branch

    Raises:
        ValueError: If any validation check fails
        OSError: If file operations fail
        subprocess.CalledProcessError: If git operations fail
    """
    try:
        print("=" * 60)
        print("Feature 205: Create Markdown File test-axs39z.md")
        print("=" * 60)

        # Phase 1: File Creation
        print("\nPhase 1: File Creation")
        print("-" * 60)

        # Step 1: Create markdown file
        _logger.info("Step 1: Creating markdown file with hardcoded content")
        filepath = create_markdown_file()
        print(f"✓ File created: {filepath}")

        # Phase 2: Validation Pipeline
        print("\nPhase 2: Validation Pipeline")
        print("-" * 60)

        # Step 2: Run comprehensive validation pipeline
        _logger.info("Step 2: Running comprehensive validation pipeline")
        validate_markdown_file()
        print("✓ File validation passed:")
        print("  - Markdown format (H1 heading + blank line)")
        print("  - Sentence count (2-3 sentences)")
        print("  - UTF-8 encoding without BOM")
        print("  - Unix LF line endings")
        print("  - File size (300-600 bytes)")
        print("  - Trailing newline")

        # Phase 3: Git Integration & Orchestration
        print("\nPhase 3: Git Integration & Orchestration")
        print("-" * 60)

        # Step 3: Stage file
        _logger.info("Step 3: Staging file with git add")
        git_add_file(FILENAME)
        print(f"✓ File staged: git add {FILENAME}")

        # Step 4: Commit changes
        _logger.info("Step 4: Creating commit with conventional message")
        git_commit(FILENAME, COMMIT_MESSAGE)
        print(f"✓ Commit created: {COMMIT_MESSAGE}")

        # Step 5: Push to remote
        _logger.info("Step 5: Pushing to remote branch")
        git_push(BRANCH_NAME)
        print(f"✓ Pushed to branch: {BRANCH_NAME}")

        print()
        print("=" * 60)
        print("✓ Feature 205 Complete (All Phases)!")
        print("  - File created and validated")
        print("  - Changes committed and pushed")
        print("=" * 60)

    except FileExistsError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"✗ File operation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"✗ Git operation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
