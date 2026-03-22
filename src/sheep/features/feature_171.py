"""Implementation for feature 171: Create markdown file test-jn0b4n.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 170 preceding features (001-170). Unlike feature 170, this implementation uses ONLY
Python 3.11+ standard library (pathlib, subprocess, re) with no external dependencies.

The file is created with:
- Exact filename: test-jn0b4n.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations

Key differences from feature 170:
- Content is hard-coded deterministic prose (not LLM-generated via CrewAI)
- All validation uses only standard library (str, re, pathlib)
- Git operations use subprocess + system git CLI (not GitPython)
- No external package dependencies (NFR-6 constraint)
"""

import re
import subprocess
import sys
from pathlib import Path

try:
    from sheep.observability.logging import get_logger
except ImportError:
    # Fallback if logging module not available
    import logging
    def get_logger(name):
        return logging.getLogger(name)

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 171
MARKDOWN_FILENAME = "test-jn0b4n.md"
COMMIT_MESSAGE = "feat(171): Create markdown file test-jn0b4n.md with prose content"


def generate_content() -> str:
    """
    Generate hard-coded markdown content with H1 heading and 2-3 sentences.

    Returns a deterministic markdown string with:
    - H1 heading (# followed by space and title)
    - Blank line separator
    - Exactly 2-3 sentences of coherent prose
    - Trailing newline

    Returns:
        String containing markdown with H1 heading and prose content.
    """
    # Hard-coded deterministic prose about a meaningful topic
    content = """# The Power of Consistent Practice

Developing any skill requires consistent, deliberate practice over extended periods. Small daily improvements compound into significant progress, transforming novices into experts through dedication. The key to mastery lies not in talent, but in the persistent application of effort toward meaningful goals.
"""
    return content


def validate_markdown_structure(content: str) -> None:
    """
    Validate markdown structure: H1 heading on first line, blank line separator.

    Checks:
    - First line is H1 heading (# followed by space)
    - H1 heading has title text
    - Second line is blank (separator)

    Args:
        content: The markdown content string to validate.

    Raises:
        ValueError: If markdown structure is invalid.
    """
    if not content or not content.strip():
        raise ValueError("Content is empty")

    lines = content.split('\n')

    # Check for H1 heading on first line
    if not lines[0].startswith('# '):
        raise ValueError(f"First line must be H1 heading (# ), got: {lines[0]!r}")

    # Check that title has text after '# '
    title = lines[0][2:].strip()
    if not title:
        raise ValueError("H1 heading title is empty")

    # Check for blank line separator (second line)
    if len(lines) < 2:
        raise ValueError("Content must have blank line after H1 heading")

    if lines[1] != '':
        raise ValueError(f"Second line must be blank (separator), got: {lines[1]!r}")


def validate_sentence_count(content: str) -> None:
    """
    Validate that content contains exactly 2-3 complete sentences.

    Counts sentence-ending punctuation (., !, ?) and verifies count is 2 or 3.

    Args:
        content: The text content to validate.

    Raises:
        ValueError: If sentence count is not 2-3.
    """
    if not content or not content.strip():
        raise ValueError("Content is empty")

    # Count sentence-ending punctuation
    sentence_count = content.count('.') + content.count('!') + content.count('?')

    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"Content must have 2-3 sentences, found {sentence_count} (counted . ! ?)"
        )


def validate_encoding(filepath: str) -> None:
    """
    Validate file uses UTF-8 encoding without BOM.

    Checks:
    - File exists and is readable
    - File starts with UTF-8 content (not BOM bytes)
    - File can be decoded as UTF-8

    Args:
        filepath: Path to the file to validate.

    Raises:
        ValueError: If file has BOM or invalid UTF-8 encoding.
    """
    path = Path(filepath)

    if not path.exists():
        raise ValueError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    # Read file as binary to check encoding
    try:
        with open(path, 'rb') as f:
            binary_content = f.read()
    except IOError as e:
        raise ValueError(f"Cannot read file: {e}")

    # Check for UTF-8 BOM (should not be present)
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File has UTF-8 BOM (should not be present)")

    # Verify the file is valid UTF-8
    try:
        binary_content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")


def validate_file_size(filepath: str) -> None:
    """
    Validate file size is within expected range (300-600 bytes inclusive).

    Args:
        filepath: Path to the file to validate.

    Raises:
        ValueError: If file size is outside 300-600 byte range.
    """
    path = Path(filepath)

    if not path.exists():
        raise ValueError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    file_size = path.stat().st_size
    if file_size < 300 or file_size > 600:
        raise ValueError(
            f"File size {file_size} bytes is outside expected range 300-600"
        )


def validate_line_endings(filepath: str) -> None:
    """
    Validate file uses Unix LF line endings (not CRLF).

    Args:
        filepath: Path to the file to validate.

    Raises:
        ValueError: If file uses CRLF or other non-LF line endings.
    """
    path = Path(filepath)

    if not path.exists():
        raise ValueError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    # Read file as binary to check line endings
    try:
        with open(path, 'rb') as f:
            binary_content = f.read()
    except IOError as e:
        raise ValueError(f"Cannot read file: {e}")

    # Check for CRLF line endings (should use LF instead)
    if b'\r\n' in binary_content:
        raise ValueError("File uses CRLF line endings (should use LF)")


def validate_content_structure(content: str) -> None:
    """
    Validate markdown content structure and format requirements.

    Orchestrates all content validations:
    - Markdown structure (H1 heading, blank line separator)
    - Sentence count (2-3 sentences)
    - Trailing newline

    Args:
        content: The markdown content string to validate.

    Raises:
        ValueError: If content fails any validation check.
    """
    # Validate markdown structure
    validate_markdown_structure(content)

    # Get prose content (skip heading and blank line)
    lines = content.split('\n')
    prose_lines = lines[2:]

    # Remove trailing empty lines
    while prose_lines and prose_lines[-1] == '':
        prose_lines.pop()

    if not prose_lines:
        raise ValueError("No prose content found after heading")

    prose_content = '\n'.join(prose_lines).strip()

    # Validate sentence count in prose
    validate_sentence_count(prose_content)

    # Check for trailing newline
    if not content.endswith('\n'):
        raise ValueError("Content must end with newline")


def validate_file_properties(filepath: str) -> None:
    """
    Validate file encoding and line ending properties.

    Orchestrates all file property validations:
    - UTF-8 encoding with no BOM
    - Unix LF line endings (not CRLF)
    - File size in expected range (300-600 bytes)

    Args:
        filepath: Path to the file to validate.

    Raises:
        ValueError: If file fails any validation check.
    """
    # Validate encoding (UTF-8 without BOM)
    validate_encoding(filepath)

    # Validate line endings (Unix LF only)
    validate_line_endings(filepath)

    # Validate file size (300-600 bytes)
    validate_file_size(filepath)


def write_markdown_file(content: str, filename: str, repo_path: str | None = None) -> str:
    """
    Write markdown content to file at repository root.

    Uses pathlib with explicit UTF-8 encoding and Unix LF line endings.

    Args:
        content: The markdown content to write.
        filename: The filename to create (e.g., "test-jn0b4n.md").
        repo_path: Path to git repository (defaults to current directory).

    Returns:
        Path to the created file as a string.

    Raises:
        ValueError: If filename is unsafe or content invalid.
        IOError: If file write operation fails.
    """
    # Validate filename safety (no path traversal)
    if '/' in filename or '\\' in filename or filename.startswith('.'):
        raise ValueError(f"Invalid filename: {filename}")

    if repo_path is None:
        repo_path = str(Path.cwd())

    repo_root = Path(repo_path)
    file_path = repo_root / filename

    _logger.info(f"Writing markdown file to {file_path}")

    try:
        # Write with UTF-8 encoding, newline='' to preserve literal LF
        # (prevents Python from translating \n to \r\n on Windows)
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)

        # Verify file was created and has content
        if not file_path.exists():
            raise IOError(f"File was not created: {file_path}")

        file_size = file_path.stat().st_size
        if file_size == 0:
            raise IOError(f"File was created but is empty: {file_path}")

        _logger.info(f"Successfully wrote markdown file: {file_path} ({file_size} bytes)")
        return str(file_path)

    except Exception as e:
        _logger.error(f"Failed to write markdown file: {e}")
        raise


def git_add(filepath: str, repo_path: str | None = None) -> None:
    """
    Stage file with git add command.

    Args:
        filepath: Path to file to stage.
        repo_path: Path to git repository (defaults to current directory).

    Raises:
        RuntimeError: If git add fails.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    filename = Path(filepath).name
    _logger.info(f"Staging file with git: {filename}")

    try:
        result = subprocess.run(
            ['git', 'add', filename],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        _logger.info(f"Successfully staged file: {filename}")
    except subprocess.CalledProcessError as e:
        _logger.error(f"git add failed: {e.stderr}")
        raise RuntimeError(f"git add failed: {e.stderr}") from e
    except FileNotFoundError:
        raise RuntimeError("git command not found. Ensure git is installed and in PATH")
    except Exception as e:
        _logger.error(f"Unexpected error during git add: {e}")
        raise RuntimeError(f"git add failed: {e}") from e


def git_commit(commit_message: str, repo_path: str | None = None) -> str:
    """
    Create git commit with conventional message.

    Args:
        commit_message: Conventional commit message to use.
        repo_path: Path to git repository (defaults to current directory).

    Returns:
        Git commit output.

    Raises:
        RuntimeError: If git commit fails.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    _logger.info(f"Committing with message: {commit_message}")

    try:
        result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        _logger.info(f"Successfully committed: {commit_message}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        _logger.error(f"git commit failed: {e.stderr}")
        raise RuntimeError(f"git commit failed: {e.stderr}") from e
    except FileNotFoundError:
        raise RuntimeError("git command not found. Ensure git is installed and in PATH")
    except Exception as e:
        _logger.error(f"Unexpected error during git commit: {e}")
        raise RuntimeError(f"git commit failed: {e}") from e


def git_push(repo_path: str | None = None, remote: str = 'origin') -> str:
    """
    Push commits to remote repository.

    Args:
        repo_path: Path to git repository (defaults to current directory).
        remote: Remote name to push to (default: 'origin').

    Returns:
        Git push output.

    Raises:
        RuntimeError: If git push fails.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    _logger.info(f"Pushing to remote {remote}")

    try:
        result = subprocess.run(
            ['git', 'push', '-u', remote, 'HEAD'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        _logger.info(f"Successfully pushed to {remote}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        _logger.error(f"git push failed: {e.stderr}")
        raise RuntimeError(f"git push failed: {e.stderr}") from e
    except FileNotFoundError:
        raise RuntimeError("git command not found. Ensure git is installed and in PATH")
    except Exception as e:
        _logger.error(f"Unexpected error during git push: {e}")
        raise RuntimeError(f"git push failed: {e}") from e


def create_feature_171_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 171.

    Orchestrates the complete workflow:
    1. Generate hard-coded markdown content (H1 heading + 2-3 sentences)
    2. Validate content structure
    3. Write file to repository root with UTF-8 encoding, Unix LF line endings
    4. Validate file properties (encoding, line endings, size)
    5. Stage file with git add
    6. Commit with conventional message
    7. Push to remote

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
        RuntimeError: If git operations fail
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    _logger.info(f"Creating feature {FEATURE_NUMBER} markdown file: {MARKDOWN_FILENAME}")

    try:
        # Task 1: Generate hard-coded markdown content
        _logger.info("Task 1: Generating markdown content")
        content = generate_content()
        _logger.debug(f"Generated {len(content)} bytes of content")

        # Task 2: Validate content structure
        _logger.info("Task 2: Validating content structure")
        validate_content_structure(content)
        _logger.info("Content structure validation passed")

        # Task 3: Write file to disk with proper encoding
        _logger.info("Task 3: Writing markdown file to disk")
        filepath = write_markdown_file(content, MARKDOWN_FILENAME, repo_path)
        _logger.debug(f"File written to: {filepath}")

        # Task 4: Validate file properties (encoding, line endings, size)
        _logger.info("Task 4: Validating file properties")
        validate_file_properties(filepath)
        _logger.info("File property validation passed")

        # Task 5: Stage file with git
        _logger.info("Task 5: Staging file")
        git_add(filepath, repo_path)

        # Task 6: Commit file with conventional message
        _logger.info("Task 6: Committing file")
        _logger.debug(f"Using commit message: {COMMIT_MESSAGE}")
        commit_result = git_commit(COMMIT_MESSAGE, repo_path)
        _logger.debug(f"Commit result: {commit_result}")

        # Task 7: Push to remote repository
        _logger.info("Task 7: Pushing to remote repository")
        push_result = git_push(repo_path)
        _logger.debug(f"Push result: {push_result}")

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            'filepath': filepath,
            'content': content,
            'commit_message': COMMIT_MESSAGE,
            'push_result': push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


def main(repo_path: str | None = None) -> dict[str, str]:
    """
    Main orchestration function for feature 171.

    This is the primary entry point that orchestrates the complete workflow:
    1. Generate hard-coded markdown content with H1 heading and 2-3 sentences
    2. Validate content structure, sentence count, and markdown format
    3. Write validated content to file with UTF-8 encoding and Unix LF line endings
    4. Validate file properties (encoding, line endings, file size)
    5. Stage file to git index
    6. Create git commit with conventional message format
    7. Push commit to remote repository

    Args:
        repo_path: Path to git repository (defaults to current working directory).

    Returns:
        Dictionary containing:
        - filepath: Full path to created markdown file
        - content: Markdown content that was written
        - commit_message: Conventional commit message used
        - push_result: Output from git push command

    Raises:
        ValueError: If content validation fails
        IOError: If file write operation fails
        RuntimeError: If git operations fail

    Example:
        >>> result = main()
        >>> print(result['filepath'])
        /path/to/repo/test-jn0b4n.md
        >>> print(result['commit_message'])
        feat(171): Create markdown file test-jn0b4n.md with prose content
    """
    return create_feature_171_markdown_file(repo_path=repo_path)


if __name__ == '__main__':
    """Execute feature 171 when run as a script."""
    result = main()
    print("Feature 171 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
