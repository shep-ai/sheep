"""Implementation for feature 206: Create markdown file test-afcl8i.md with title and prose content.

This module orchestrates the creation of a markdown file with hard-coded, deterministic content.
Following the pattern from feature 205, this implementation uses hard-coded content to demonstrate
straightforward file creation within the Sheep workflow without external API dependencies.

The file is created with:
- Exact filename: test-afcl8i.md
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

import re
import subprocess
import sys
from pathlib import Path

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 206 constants
FILENAME = "test-afcl8i.md"
FEATURE_NUMBER = 206
BRANCH_NAME = "feat/206-markdown-file-creation-f7d8d3"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME}"

# Hard-coded markdown content
# H1 title about the chosen topic
TITLE_TEXT = "The Art of Problem Solving Through Code"

# 2-3 sentences of prose content related to the title
PROSE_CONTENT = (
    "Software development is fundamentally about solving problems through logical thinking and creative solutions. "
    "The ability to break down complex challenges into manageable pieces and implement elegant solutions is a skill "
    "that distinguishes excellent programmers from adequate ones."
)

# Validation constants
H1_PATTERN = r"^# [A-Za-z]"
BOM_BYTES = b"\xef\xbb\xbf"
MIN_FILE_SIZE = 100
MAX_FILE_SIZE = 600


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


def validate_h1_format(file_path: Path) -> bool:
    """Validate that file's first line matches H1 markdown pattern.

    Checks that the first line starts with '# ' followed by alphabetic character.
    Uses regex pattern: ^# [A-Za-z]

    Args:
        file_path: Path to markdown file to validate

    Returns:
        True if H1 format is valid

    Raises:
        ValueError: If H1 heading is missing or malformed
    """
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        lines = content.split("\n")

        if not lines:
            raise ValueError("File is empty: expected H1 heading starting with '# '")

        first_line = lines[0]

        if not re.match(H1_PATTERN, first_line):
            raise ValueError(
                f"H1 heading not found or invalid format: "
                f"first line should start with '# ' followed by text, "
                f"got: '{first_line}'"
            )

        return True

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to validate H1 format: {e}") from e


def validate_blank_separator(file_path: Path) -> bool:
    """Validate that the line after H1 heading is blank.

    The second line must be empty or contain only whitespace.

    Args:
        file_path: Path to markdown file to validate

    Returns:
        True if blank separator is valid

    Raises:
        ValueError: If blank separator is missing or contains text
    """
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        lines = content.split("\n")

        # Check we have at least 2 lines
        if len(lines) < 2:
            raise ValueError(
                "File has fewer than 2 lines: expected H1 heading followed by blank line"
            )

        second_line = lines[1]

        if second_line.strip() != "":
            raise ValueError(
                f"Expected blank line after H1 heading, "
                f"but found text: '{second_line}'"
            )

        return True

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to validate blank separator: {e}") from e


def validate_sentence_count(file_path: Path) -> bool:
    """Validate that prose contains exactly 2-3 sentences.

    Counts periods in the prose section (after the blank line) to determine
    sentence count.

    Args:
        file_path: Path to markdown file to validate

    Returns:
        True if sentence count is valid (2-3)

    Raises:
        ValueError: If sentence count is not 2 or 3
    """
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        lines = content.split("\n")

        # Prose is everything after the second line (blank line)
        if len(lines) < 3:
            raise ValueError(
                "File does not have prose content after blank line"
            )

        prose = "\n".join(lines[2:])
        period_count = prose.count(".")

        if period_count < 2 or period_count > 3:
            raise ValueError(
                f"Expected 2-3 sentences, found {period_count} periods "
                f"in prose section"
            )

        return True

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to validate sentence count: {e}") from e


def validate_encoding(file_path: Path) -> bool:
    """Validate that file is UTF-8 encoded without BOM.

    Checks that file does not start with UTF-8 BOM (0xEF 0xBB 0xBF) and
    can be decoded as valid UTF-8.

    Args:
        file_path: Path to markdown file to validate

    Returns:
        True if encoding is valid UTF-8 without BOM

    Raises:
        ValueError: If BOM is detected or file is not valid UTF-8
    """
    try:
        data = Path(file_path).read_bytes()

        if data.startswith(BOM_BYTES):
            raise ValueError(
                "File encoding has UTF-8 BOM (0xEF 0xBB 0xBF): "
                "expected UTF-8 without BOM"
            )

        # Verify valid UTF-8 by attempting decode
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File is not valid UTF-8 encoding: {e}"
            ) from e

        return True

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to validate encoding: {e}") from e


def validate_line_endings(file_path: Path) -> bool:
    """Validate that file uses Unix LF line endings only.

    Checks that file contains no CRLF (Windows) or CR (Mac) line endings,
    only LF (Unix).

    Args:
        file_path: Path to markdown file to validate

    Returns:
        True if line endings are Unix LF only

    Raises:
        ValueError: If non-LF line endings are detected
    """
    try:
        data = Path(file_path).read_bytes()

        if b"\r\n" in data:
            raise ValueError(
                "File uses CRLF line endings (Windows style), "
                "expected Unix LF line endings"
            )

        if b"\r" in data:
            raise ValueError(
                "File uses CR line endings (old Mac style), "
                "expected Unix LF line endings"
            )

        return True

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to validate line endings: {e}") from e


def validate_file_size(file_path: Path) -> bool:
    """Validate that file size is within specification bounds.

    File size must be between 100-600 bytes inclusive.

    Args:
        file_path: Path to markdown file to validate

    Returns:
        True if file size is within bounds

    Raises:
        ValueError: If file size is outside 100-600 byte range
    """
    try:
        size = Path(file_path).stat().st_size

        if size < MIN_FILE_SIZE or size > MAX_FILE_SIZE:
            raise ValueError(
                f"File size {size} bytes is outside bounds "
                f"(expected {MIN_FILE_SIZE}-{MAX_FILE_SIZE} bytes)"
            )

        return True

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to validate file size: {e}") from e


def validate_markdown_file(file_path: Path) -> bool:
    """Orchestrate comprehensive validation of markdown file.

    Validates in order: (1) file exists, (2) H1 format, (3) blank separator,
    (4) sentence count, (5) encoding, (6) line endings, (7) file size.

    Stops immediately on first validation failure (fail-fast).

    Args:
        file_path: Path to markdown file to validate

    Returns:
        True if all validations pass

    Raises:
        ValueError: If any validation fails
    """
    file_path = Path(file_path)

    try:
        # Check file exists
        if not file_path.exists():
            raise ValueError(f"File does not exist: {file_path}")

        _logger.debug(f"File exists: {file_path}")

        # Validate H1 heading format
        validate_h1_format(file_path)
        _logger.debug("H1 heading format validation passed")

        # Validate blank separator line
        validate_blank_separator(file_path)
        _logger.debug("Blank separator line validation passed")

        # Validate sentence count
        validate_sentence_count(file_path)
        _logger.debug("Sentence count validation passed")

        # Validate UTF-8 encoding without BOM
        validate_encoding(file_path)
        _logger.debug("UTF-8 encoding validation passed")

        # Validate Unix LF line endings
        validate_line_endings(file_path)
        _logger.debug("Unix LF line endings validation passed")

        # Validate file size
        validate_file_size(file_path)
        _logger.debug("File size validation passed")

        _logger.info(f"All validations passed for {file_path}")
        return True

    except ValueError as e:
        _logger.error(f"Validation failed: {e}")
        raise


def git_add() -> None:
    """Stage markdown file in git index using 'git add' command.

    Uses subprocess.run() with check=True for fail-fast behavior. Any git
    error raises CalledProcessError with stderr context for debugging.

    Raises:
        subprocess.CalledProcessError: If git add command fails (including
            missing git, no repository, permission issues, etc.)
    """
    try:
        _logger.debug(f"Staging file with git add: {FILENAME}")

        subprocess.run(
            ["git", "add", FILENAME],
            check=True,
            capture_output=True,
            text=True,
        )

        _logger.info(f"Successfully staged {FILENAME} with git add")

    except subprocess.CalledProcessError as e:
        error_msg = f"git add failed: {e.stderr}" if e.stderr else str(e)
        _logger.error(f"Failed to stage file: {error_msg}")
        raise


def git_commit() -> None:
    """Create git commit with conventional commit message.

    Uses subprocess.run() with check=True for fail-fast behavior. Commit
    message follows conventional commits format: feat(206): description

    Any git error raises CalledProcessError with stderr context for debugging.

    Raises:
        subprocess.CalledProcessError: If git commit command fails (including
            no staged changes, git configuration issues, hook failures, etc.)
    """
    try:
        _logger.debug(f"Creating git commit with message: {COMMIT_MESSAGE}")

        subprocess.run(
            ["git", "commit", "-m", COMMIT_MESSAGE],
            check=True,
            capture_output=True,
            text=True,
        )

        _logger.info(f"Successfully created commit: {COMMIT_MESSAGE}")

    except subprocess.CalledProcessError as e:
        error_msg = f"git commit failed: {e.stderr}" if e.stderr else str(e)
        _logger.error(f"Failed to commit file: {error_msg}")
        raise


def git_push() -> None:
    """Push commit to feature branch using 'git push' command.

    Uses subprocess.run() with check=True for fail-fast behavior. The -u flag
    sets upstream tracking on the first push, establishing the relationship
    between the local feature branch and remote tracking branch.

    Any git error raises CalledProcessError with stderr context for debugging.
    This captures network errors, authentication failures, branch protection
    rules, and other push-related issues.

    Raises:
        subprocess.CalledProcessError: If git push command fails (including
            network errors, authentication issues, branch protection, etc.)
    """
    try:
        _logger.debug(f"Pushing commit to remote branch: {BRANCH_NAME}")

        subprocess.run(
            ["git", "push", "-u", "origin", BRANCH_NAME],
            check=True,
            capture_output=True,
            text=True,
        )

        _logger.info(f"Successfully pushed commit to {BRANCH_NAME}")

    except subprocess.CalledProcessError as e:
        error_msg = f"git push failed: {e.stderr}" if e.stderr else str(e)
        _logger.error(f"Failed to push commit: {error_msg}")
        raise


def main() -> int:
    """Orchestrate complete workflow: create file, validate, stage, commit, push.

    Orchestrates the full feature 206 workflow in sequence:
    1. Create markdown file with hard-coded content
    2. Validate file structure, encoding, size, and format
    3. Stage file with 'git add'
    4. Create commit with conventional message
    5. Push commit to feature branch

    Wraps entire workflow in try-except to catch any step failure and log
    appropriate error messages. Returns success code 0 if all steps complete
    successfully, failure code 1 if any step fails.

    Returns:
        int: 0 on successful completion, 1 on any failure

    Logs:
        - info: Major workflow steps (file created, validations passed, etc.)
        - error: Any failure with specific error details
        - info: Overall completion status (success or failure)
    """
    try:
        _logger.info("Starting feature 206 workflow: markdown file creation")

        # Step 1: Create markdown file
        _logger.info("Step 1/5: Creating markdown file")
        file_path = create_markdown_file()

        # Step 2: Validate markdown file
        _logger.info("Step 2/5: Validating markdown file")
        validate_markdown_file(file_path)
        _logger.info("All validations passed")

        # Step 3: Stage file with git add
        _logger.info("Step 3/5: Staging file with git add")
        git_add()

        # Step 4: Create commit
        _logger.info("Step 4/5: Creating git commit")
        git_commit()

        # Step 5: Push to feature branch
        _logger.info("Step 5/5: Pushing to feature branch")
        git_push()

        # Success
        _logger.info(
            f"Feature 206 workflow completed successfully: "
            f"{FILENAME} created, validated, committed, and pushed"
        )
        return 0

    except Exception as e:
        _logger.error(f"Feature 206 workflow failed: {e}")
        return 1


if __name__ == "__main__":
    """Entry point for direct script execution."""
    exit_code = main()
    sys.exit(exit_code)
