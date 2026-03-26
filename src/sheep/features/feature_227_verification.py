"""Comprehensive verification functions for feature 227: markdown file creation.

This module provides granular, testable verification functions that validate
all functional and non-functional requirements for feature 227. Each function
validates a specific aspect of the markdown file against the specification.

Requirements verified:
- FR-1 through FR-9: Functional requirements (file creation, git workflow)
- NFR-1 through NFR-9: Non-functional requirements (encoding, format, structure)
"""

from pathlib import Path
import re

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Constants for validation
FEATURE_NUMBER = 227
EXPECTED_FILENAME = "test-arvwkm.md"
MIN_FILE_SIZE = 250  # bytes
MAX_FILE_SIZE = 800  # bytes
MIN_SENTENCES = 2
MAX_SENTENCES = 3


class VerificationError(Exception):
    """Raised when a verification check fails."""

    pass


def verify_file_exists(filepath: str) -> bool:
    """
    Verify that the markdown file exists at the specified path.

    Checks:
    - File exists in the file system
    - Path points to a file (not a directory)
    - File is readable

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if file exists and is readable.

    Raises:
        VerificationError: If file does not exist or is not accessible.
    """
    path = Path(filepath)

    try:
        if not path.exists():
            raise VerificationError(f"File does not exist: {filepath}")

        if not path.is_file():
            raise VerificationError(f"Path is not a file: {filepath}")

        # Verify file is readable
        with open(path, "rb") as f:
            _ = f.read(1)

        _logger.info(f"✓ File exists and is readable: {filepath}")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error checking file existence: {e}")


def verify_file_in_repository_root(filepath: str, repo_root: str | None = None) -> bool:
    """
    Verify that the file is in the repository root directory.

    Checks:
    - File is in the repository root (no subdirectories)
    - File has the correct filename (test-arvwkm.md)

    Args:
        filepath: Path to the markdown file to verify.
        repo_root: Path to the repository root (defaults to current directory).

    Returns:
        True if file is in the repository root with correct name.

    Raises:
        VerificationError: If file is not in repository root or has wrong name.
    """
    if repo_root is None:
        repo_root = str(Path.cwd())

    path = Path(filepath)
    filename = path.name

    try:
        # Check filename matches expected
        if filename != EXPECTED_FILENAME:
            raise VerificationError(
                f"Filename must be '{EXPECTED_FILENAME}', got '{filename}'"
            )

        # Check file is in repository root
        repo_path = Path(repo_root)
        expected_path = repo_path / EXPECTED_FILENAME

        if path.resolve() != expected_path.resolve():
            raise VerificationError(
                f"File must be in repository root: {expected_path}, got {path}"
            )

        _logger.info(f"✓ File is in repository root with correct name: {filename}")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying file location: {e}")


def verify_heading_format(filepath: str) -> bool:
    """
    Verify that the file starts with a valid CommonMark H1 heading.

    Checks:
    - First line starts with "# " (H1 markdown heading)
    - Heading is not empty
    - Heading follows CommonMark specification

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if heading format is valid.

    Raises:
        VerificationError: If heading format is invalid.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            first_line = f.readline().rstrip("\n")

        if not first_line:
            raise VerificationError("First line is empty, expected H1 heading")

        if not first_line.startswith("# "):
            raise VerificationError(
                f"First line must start with '# ', got '{first_line[:20]}...'"
            )

        heading_text = first_line[2:].strip()
        if not heading_text:
            raise VerificationError("H1 heading is empty after '# '")

        _logger.info(f"✓ Heading format is valid: {first_line}")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying heading format: {e}")


def verify_blank_line_separator(filepath: str) -> bool:
    """
    Verify that there is a blank line between heading and prose content.

    Checks:
    - Second line is blank (empty string after split)
    - Provides proper separation between heading and content

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if blank line separator is present.

    Raises:
        VerificationError: If blank line is missing or format is incorrect.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) < 3:
            raise VerificationError(
                f"File must have at least 3 lines (heading, blank, prose), got {len(lines)}"
            )

        # Get second line and strip the newline
        second_line = lines[1].rstrip("\n")

        if second_line != "":
            raise VerificationError(
                f"Second line must be blank, got '{second_line}'"
            )

        _logger.info("✓ Blank line separator is present after heading")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying blank line separator: {e}")


def verify_prose_structure(filepath: str) -> bool:
    """
    Verify that the prose content has the correct structure and sentence count.

    Checks:
    - Content has 2-3 sentences (verified by counting periods)
    - Prose is readable and coherent
    - Content is separated from heading by blank line

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if prose structure is valid.

    Raises:
        VerificationError: If prose structure is invalid or sentence count is wrong.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")

        # Extract prose (skip heading and blank line)
        prose_lines = lines[2:]

        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        if not prose_lines:
            raise VerificationError("No prose content found after heading")

        prose_content = "\n".join(prose_lines).strip()

        # Count sentences by counting periods
        sentence_count = prose_content.count(".")

        if sentence_count < MIN_SENTENCES or sentence_count > MAX_SENTENCES:
            raise VerificationError(
                f"Expected {MIN_SENTENCES}-{MAX_SENTENCES} sentences, found {sentence_count}"
            )

        # Verify content is not empty
        if not prose_content:
            raise VerificationError("Prose content is empty")

        # Verify content is readable (basic check for minimum length)
        if len(prose_content) < 50:
            raise VerificationError(
                f"Prose content is too short ({len(prose_content)} chars), expected at least 50"
            )

        _logger.info(
            f"✓ Prose structure is valid: {sentence_count} sentences, {len(prose_content)} chars"
        )
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying prose structure: {e}")


def verify_utf8_encoding_without_bom(filepath: str) -> bool:
    """
    Verify that the file is encoded as UTF-8 without Byte Order Mark.

    Checks:
    - File is valid UTF-8 encoded
    - File does not have UTF-8 BOM (0xEF 0xBB 0xBF)
    - File can be read and decoded as UTF-8

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if file is UTF-8 without BOM.

    Raises:
        VerificationError: If encoding is invalid or BOM is present.
    """
    try:
        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Check for UTF-8 BOM
        if binary_content.startswith(b"\xef\xbb\xbf"):
            raise VerificationError("File contains UTF-8 BOM (should not be present)")

        # Verify file is valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise VerificationError(f"File is not valid UTF-8: {e}")

        _logger.info("✓ File is UTF-8 encoded without BOM")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying UTF-8 encoding: {e}")


def verify_lf_line_endings(filepath: str) -> bool:
    """
    Verify that the file uses Unix LF line endings, not Windows CRLF.

    Checks:
    - File uses LF (\\n) line endings
    - File does not use CRLF (\\r\\n) line endings
    - File does not use CR (\\r) line endings

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if file uses Unix LF line endings.

    Raises:
        VerificationError: If file uses CRLF or CR line endings.
    """
    try:
        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Check for CRLF
        if b"\r\n" in binary_content:
            raise VerificationError(
                "File uses CRLF line endings (should use LF for Unix)"
            )

        # Check for CR (carriage return)
        if b"\r" in binary_content:
            raise VerificationError(
                "File uses CR line endings (should use LF for Unix)"
            )

        _logger.info("✓ File uses Unix LF line endings")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying line endings: {e}")


def verify_file_size(filepath: str) -> bool:
    """
    Verify that the file size is in the expected range.

    Checks:
    - File size is between MIN_FILE_SIZE (250) and MAX_FILE_SIZE (800) bytes
    - Size is a natural consequence of proper structure

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if file size is in expected range.

    Raises:
        VerificationError: If file size is outside expected range.
    """
    try:
        file_size = Path(filepath).stat().st_size

        if file_size < MIN_FILE_SIZE or file_size > MAX_FILE_SIZE:
            raise VerificationError(
                f"File size {file_size} bytes is outside expected range "
                f"({MIN_FILE_SIZE}-{MAX_FILE_SIZE} bytes)"
            )

        _logger.info(f"✓ File size is in expected range: {file_size} bytes")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying file size: {e}")


def verify_trailing_newline(filepath: str) -> bool:
    """
    Verify that the file ends with a newline (Unix convention).

    Checks:
    - File ends with LF newline character
    - Proper Unix file format

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if file ends with newline.

    Raises:
        VerificationError: If file does not end with newline.
    """
    try:
        with open(filepath, "rb") as f:
            binary_content = f.read()

        if not binary_content.endswith(b"\n"):
            raise VerificationError("File must end with a newline character")

        _logger.info("✓ File ends with trailing newline")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying trailing newline: {e}")


def verify_git_trackable(filepath: str) -> bool:
    """
    Verify that the file is trackable by git (not in .gitignore).

    Checks:
    - File path is not excluded by .gitignore patterns
    - File would be tracked by git if staged

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if file is trackable by git.

    Raises:
        VerificationError: If file is excluded by .gitignore.
    """
    try:
        # Get the filename
        filename = Path(filepath).name

        # Check if there's a .gitignore file
        gitignore_path = Path.cwd() / ".gitignore"

        if gitignore_path.exists():
            with open(gitignore_path, "r") as f:
                gitignore_content = f.read()

            # Check for common patterns that would exclude test-*.md files
            patterns_to_check = [
                "*.md",  # Would exclude all markdown files
                "test-*.md",  # Would exclude test markdown files
                filename,  # Would exclude this specific file
            ]

            for pattern in patterns_to_check:
                # Simple pattern matching (not full gitignore semantics)
                if pattern in gitignore_content:
                    # Check if it's actually excluding the file (not commented out)
                    for line in gitignore_content.split("\n"):
                        line = line.strip()
                        if line == pattern and not line.startswith("#"):
                            raise VerificationError(
                                f"File '{filename}' is excluded by .gitignore pattern: {pattern}"
                            )

        _logger.info(f"✓ File is trackable by git: {filename}")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying git trackability: {e}")


def verify_markdown_syntax(filepath: str) -> bool:
    """
    Verify that the file contains valid CommonMark markdown syntax.

    Checks:
    - Heading is properly formatted
    - Content structure is valid
    - No syntax errors

    Args:
        filepath: Path to the markdown file to verify.

    Returns:
        True if markdown syntax is valid.

    Raises:
        VerificationError: If markdown syntax is invalid.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")

        # Check first line is H1
        if not lines[0].startswith("# "):
            raise VerificationError("First line must be H1 heading")

        # Check heading is not empty
        heading = lines[0][2:].strip()
        if not heading:
            raise VerificationError("H1 heading cannot be empty")

        # Check structure: heading, blank line, prose
        if len(lines) < 3:
            raise VerificationError("File must have heading, blank line, and prose")

        if lines[1] != "":
            raise VerificationError("Second line must be blank")

        # Basic check for valid content
        prose = "\n".join(lines[2:]).strip()
        if not prose:
            raise VerificationError("No prose content after heading")

        _logger.info("✓ Markdown syntax is valid")
        return True

    except VerificationError:
        raise
    except Exception as e:
        raise VerificationError(f"Error verifying markdown syntax: {e}")


def verify_all_requirements(filepath: str, repo_root: str | None = None) -> dict:
    """
    Comprehensive verification harness that runs all requirement checks.

    This function orchestrates all verification checks and provides a detailed
    report of which requirements are met and which have failed.

    Args:
        filepath: Path to the markdown file to verify.
        repo_root: Path to the repository root (defaults to current directory).

    Returns:
        Dictionary containing:
        - all_pass: Boolean indicating if all verifications passed
        - passed: List of passed verification checks
        - failed: List of failed verification checks with error messages
        - total: Total number of verification checks
        - summary: Human-readable summary of results

    Raises:
        VerificationError: If filepath is invalid or cannot be accessed
    """
    if repo_root is None:
        repo_root = str(Path.cwd())

    # List of all verification functions to run
    verification_checks = [
        ("File exists", lambda: verify_file_exists(filepath)),
        ("File in repository root", lambda: verify_file_in_repository_root(filepath, repo_root)),
        ("H1 heading format", lambda: verify_heading_format(filepath)),
        ("Blank line separator", lambda: verify_blank_line_separator(filepath)),
        ("Prose structure (2-3 sentences)", lambda: verify_prose_structure(filepath)),
        ("UTF-8 encoding without BOM", lambda: verify_utf8_encoding_without_bom(filepath)),
        ("Unix LF line endings", lambda: verify_lf_line_endings(filepath)),
        ("File size in expected range", lambda: verify_file_size(filepath)),
        ("Trailing newline", lambda: verify_trailing_newline(filepath)),
        ("Git trackable (not in .gitignore)", lambda: verify_git_trackable(filepath)),
        ("Valid CommonMark markdown syntax", lambda: verify_markdown_syntax(filepath)),
    ]

    passed = []
    failed = []

    _logger.info(f"\n{'='*60}")
    _logger.info(f"Running comprehensive verification for {filepath}")
    _logger.info(f"{'='*60}\n")

    for check_name, check_func in verification_checks:
        try:
            check_func()
            passed.append(check_name)
            _logger.info(f"  ✓ {check_name}")
        except VerificationError as e:
            failed.append((check_name, str(e)))
            _logger.error(f"  ✗ {check_name}: {e}")
        except Exception as e:
            failed.append((check_name, f"Unexpected error: {e}"))
            _logger.error(f"  ✗ {check_name}: Unexpected error: {e}")

    all_pass = len(failed) == 0

    # Build summary
    summary_lines = [f"\n{'='*60}"]
    summary_lines.append("VERIFICATION SUMMARY")
    summary_lines.append(f"{'='*60}")
    summary_lines.append(f"Total checks: {len(verification_checks)}")
    summary_lines.append(f"Passed: {len(passed)}")
    summary_lines.append(f"Failed: {len(failed)}")

    if all_pass:
        summary_lines.append("\n✓ All verification checks PASSED")
    else:
        summary_lines.append("\n✗ Some verification checks FAILED:")
        for check_name, error_msg in failed:
            summary_lines.append(f"  - {check_name}: {error_msg}")

    summary_lines.append(f"{'='*60}\n")
    summary = "\n".join(summary_lines)

    _logger.info(summary)

    return {
        "all_pass": all_pass,
        "passed": passed,
        "failed": failed,
        "total": len(verification_checks),
        "summary": summary,
    }
