"""
Utilities for deterministic content generation and markdown file operations in feature 270.

This module provides reusable functions for:
1. Deterministic content selection from template pool using hash-based seeding
2. File creation with proper UTF-8 encoding and Unix LF line endings
3. File validation with retry logic and exponential backoff
4. Git operations (stage, commit, push) with comprehensive error handling
"""

import hashlib
import subprocess
import time
from pathlib import Path

from templates import TEMPLATES


# ============================================================================
# Content Selection Functions
# ============================================================================


def select_content(feature_number: int) -> dict[str, str]:
    """
    Deterministically select a template from the pool based on feature number.

    Uses hashlib.md5() for hashing the feature number, then converts to integer
    for modulo-based indexing into the template pool. This ensures:
    - Reproducibility: same feature number always produces identical template
    - Distribution: hash function provides good distribution across pool
    - Speed: hash lookup is O(1) with minimal overhead

    Args:
        feature_number: The feature number (e.g., 270).

    Returns:
        Dictionary with 'title' and 'prose' keys selected from template pool.

    Raises:
        ValueError: If feature_number is not a valid integer.
        IndexError: If template pool is empty (should never happen).

    Examples:
        >>> content = select_content(270)
        >>> content['title']  # Some title from pool
        >>> content['prose']  # Corresponding prose
        >>> # Calling with same feature number returns same content:
        >>> select_content(270) == select_content(270)
        True
    """
    if not isinstance(feature_number, int):
        raise ValueError(f"feature_number must be an integer, got {type(feature_number)}")

    if feature_number < 0:
        raise ValueError(f"feature_number must be non-negative, got {feature_number}")

    # Generate hash from feature number
    hash_bytes = str(feature_number).encode('utf-8')
    hash_hex = hashlib.md5(hash_bytes).hexdigest()
    hash_int = int(hash_hex, 16)

    # Select template using modulo indexing
    template_index = hash_int % len(TEMPLATES)
    return TEMPLATES[template_index]


# ============================================================================
# File Creation Functions
# ============================================================================


def format_markdown_content(title: str, prose: str) -> str:
    """
    Format title and prose into markdown structure.

    Creates markdown content with structure:
    # Title\n\nProse\n

    Args:
        title: The H1 heading text (without the '# ' prefix).
        prose: The prose paragraph content.

    Returns:
        Formatted markdown content as string.
    """
    return f"# {title}\n\n{prose}\n"


def create_markdown_file(
    filepath: str | Path,
    title: str,
    prose: str,
) -> Path:
    """
    Create a markdown file with proper UTF-8 encoding and Unix LF line endings.

    Creates a file at the specified path with:
    - UTF-8 encoding without BOM
    - Unix LF (\n) line endings (not CRLF)
    - Trailing newline at end of file

    Args:
        filepath: Path where file should be created (string or Path object).
        title: The H1 heading text.
        prose: The prose paragraph content.

    Returns:
        Path object pointing to the created file.

    Raises:
        OSError: If file creation fails (permissions, path issues, etc.).
        ValueError: If title or prose are empty strings.

    Examples:
        >>> path = create_markdown_file("test.md", "My Title", "My prose here.")
        >>> path.exists()
        True
    """
    if not title:
        raise ValueError("title cannot be empty")
    if not prose:
        raise ValueError("prose cannot be empty")

    # Convert to Path if string was provided
    file_path = Path(filepath)

    # Format content
    content = format_markdown_content(title, prose)

    # Write file with UTF-8 encoding and Unix LF line endings
    # The newline='\n' parameter ensures LF on all platforms (Windows, Linux, macOS)
    file_path.write_text(content, encoding='utf-8', newline='\n')

    return file_path


# ============================================================================
# File Validation Functions
# ============================================================================


def _count_sentence_endings(text: str) -> int:
    """Count sentence-ending punctuation marks (. ! ?) in text."""
    return sum(1 for char in text if char in '.!?')


def _validate_heading(content: str) -> tuple[bool, str | None]:
    """Validate that content has H1 heading (starts with '# ')."""
    if not content.startswith('# '):
        return False, "Content must start with '# ' (H1 heading)"
    return True, None


def _validate_sentence_count(content: str) -> tuple[bool, str | None]:
    """Validate that content has 2-3 sentences."""
    sentence_count = _count_sentence_endings(content)
    if sentence_count < 2 or sentence_count > 3:
        return False, f"Content must have 2-3 sentences, got {sentence_count}"
    return True, None


def _validate_file_size(file_path: Path) -> tuple[bool, str | None]:
    """Validate that file size is 400-600 bytes."""
    byte_size = file_path.stat().st_size
    if byte_size < 400 or byte_size > 600:
        return False, f"File size must be 400-600 bytes, got {byte_size}"
    return True, None


def _validate_encoding(file_path: Path) -> tuple[bool, str | None]:
    """Validate that file is UTF-8 encoded without BOM."""
    try:
        raw_bytes = file_path.read_bytes()

        # Check for BOM (should not have one)
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            return False, "File must not have UTF-8 BOM"

        # Try to decode as UTF-8
        raw_bytes.decode('utf-8')
        return True, None
    except UnicodeDecodeError:
        return False, "File must be valid UTF-8"


def _validate_line_endings(file_path: Path) -> tuple[bool, str | None]:
    """Validate that file uses Unix LF line endings (not CRLF)."""
    raw_bytes = file_path.read_bytes()

    # Check for CRLF (Windows line endings)
    if b'\r\n' in raw_bytes:
        return False, "File must use Unix LF line endings, found CRLF"

    return True, None


def _validate_trailing_newline(file_path: Path) -> tuple[bool, str | None]:
    """Validate that file ends with newline."""
    raw_bytes = file_path.read_bytes()

    if not raw_bytes.endswith(b'\n'):
        return False, "File must end with newline"

    return True, None


def validate_markdown_file(
    file_path: str | Path,
    max_retries: int = 2,
    initial_delay: float = 0.1,
) -> bool:
    """
    Validate a markdown file meets all requirements with retry logic.

    Performs comprehensive validation checks:
    - H1 heading present (starts with '# ')
    - Sentence count is 2-3 (counts sentence-ending punctuation)
    - File size is 400-600 bytes
    - UTF-8 encoding without BOM
    - Unix LF line endings (no CRLF)
    - Trailing newline at end

    On validation failure, retries with exponential backoff:
    - First retry after initial_delay (default 0.1s)
    - Second retry after 2x initial_delay (default 0.2s)
    - Raises AssertionError if all retries fail

    Args:
        file_path: Path to file to validate (string or Path object).
        max_retries: Maximum number of validation attempts (default: 2).
        initial_delay: Initial delay in seconds for exponential backoff (default: 0.1).

    Returns:
        True if file passes all validation checks.

    Raises:
        AssertionError: If file fails validation after all retry attempts.
        FileNotFoundError: If file does not exist.

    Examples:
        >>> validate_markdown_file("test.md")
        True
        >>> validate_markdown_file("invalid.md")  # Will raise AssertionError
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # List of validation checks to perform
    checks = [
        ("heading", lambda: _validate_heading(file_path.read_text(encoding='utf-8'))),
        ("sentence_count", lambda: _validate_sentence_count(file_path.read_text(encoding='utf-8'))),
        ("file_size", lambda: _validate_file_size(file_path)),
        ("encoding", lambda: _validate_encoding(file_path)),
        ("line_endings", lambda: _validate_line_endings(file_path)),
        ("trailing_newline", lambda: _validate_trailing_newline(file_path)),
    ]

    # Perform validation with retries
    for attempt in range(max_retries):
        all_valid = True
        first_error = None

        try:
            for check_name, check_fn in checks:
                is_valid, error = check_fn()
                if not is_valid:
                    all_valid = False
                    if first_error is None:
                        first_error = error
                    # Continue checking all validations for detailed error reporting

            if all_valid:
                return True

        except (UnicodeDecodeError, ValueError) as e:
            all_valid = False
            first_error = f"Encoding or format error: {e}"

        # Retry if not final attempt
        if attempt < max_retries - 1:
            delay = initial_delay * (2 ** attempt)  # Exponential backoff
            time.sleep(delay)

    # All retries failed
    raise AssertionError(
        f"Markdown file validation failed: {first_error}"
    )


# ============================================================================
# Git Operation Functions
# ============================================================================


def git_stage(filename: str) -> None:
    """
    Stage a file for commit using 'git add'.

    Args:
        filename: Name of file to stage.

    Raises:
        RuntimeError: If git add fails.
    """
    try:
        subprocess.run(
            ['git', 'add', filename],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to stage file '{filename}': {e.stderr or e.stdout}"
        ) from e


def git_commit(filename: str, feature_number: int) -> None:
    """
    Commit a staged file with conventional commit message.

    Creates commit with message format:
    feat(###): create markdown file <filename> with title and prose content

    Args:
        filename: Name of file to commit.
        feature_number: Feature number for commit message.

    Raises:
        RuntimeError: If git commit fails.
    """
    commit_message = (
        f"feat({feature_number}): create markdown file {filename} "
        "with title and prose content"
    )

    try:
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to commit file '{filename}': {e.stderr or e.stdout}"
        ) from e


def git_push() -> None:
    """
    Push commits to origin with upstream tracking.

    Uses 'git push -u origin HEAD' to establish upstream tracking
    and push all commits on current branch.

    Raises:
        RuntimeError: If git push fails.
    """
    try:
        subprocess.run(
            ['git', 'push', '-u', 'origin', 'HEAD'],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to push commits: {e.stderr or e.stdout}"
        ) from e
