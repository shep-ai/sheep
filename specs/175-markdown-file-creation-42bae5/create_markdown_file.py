"""
Feature 175: Create markdown file with title and prose content.

This module creates a markdown file (test-rh39t2.md) following the established
pattern from 170+ prior features. The file includes an H1 heading, blank line,
2-3 sentences of prose content, and is properly validated before git operations.
"""
from pathlib import Path
import subprocess
import sys


# Module-level constants
FILENAME = "test-rh39t2.md"
TITLE = "The Architecture of Resilience"
PROSE = (
    "Building reliable systems requires intentional design at every layer, "
    "from database consistency to graceful error handling. Modern distributed systems "
    "face inherent challenges of network latency, partial failures, and asynchronous operations "
    "that demand sophisticated approaches to state management and recovery. The most resilient "
    "architectures embrace failure as inevitable and design systems to detect, isolate, and "
    "recover from failures with minimal disruption to users."
)
COMMIT_MESSAGE = "feat(175): create markdown file test-rh39t2.md with prose content"


def create_file():
    """
    Create markdown file with title and prose content.

    Creates a file in the repository root with the following structure:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content starting on line 3
    - Trailing newline at end

    Uses UTF-8 encoding without BOM and Unix LF line endings on all platforms.

    Raises:
        OSError: If file cannot be created (permissions, disk space, etc.)
    """
    # Construct markdown content with proper structure
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Write file with explicit UTF-8 encoding and Unix LF line endings
    # newline='\n' ensures LF on all platforms (Windows, Linux, macOS)
    # encoding='utf-8' ensures UTF-8 without BOM (BOM only appears with 'utf-8-sig')
    file_path = Path(FILENAME)
    file_path.write_text(content, encoding='utf-8', newline='\n')


def validate_file(filename):
    """
    Validate markdown file structure, encoding, and size.

    Performs comprehensive validation before git operations:
    - File exists and has non-zero size
    - UTF-8 encoding without BOM
    - Unix LF line endings (no CRLF)
    - H1 heading on first line
    - Blank line on second line
    - 2-3 sentences of prose content
    - File ends with newline
    - File size within 300-800 byte range

    Args:
        filename: Path to file to validate

    Raises:
        ValueError: If validation fails with descriptive error message
    """
    file_path = Path(filename)

    # Check file exists
    if not file_path.exists():
        raise ValueError(f"File {filename} does not exist")

    # Check file has content
    if file_path.stat().st_size == 0:
        raise ValueError(f"File {filename} is empty")

    # Read file as binary to check encoding and line endings
    content_bytes = file_path.read_bytes()

    # Check for UTF-8 BOM
    if content_bytes.startswith(b'\xef\xbb\xbf'):
        raise ValueError(f"File {filename} has UTF-8 BOM")

    # Check for CRLF line endings
    if b'\r\n' in content_bytes:
        raise ValueError(f"File {filename} has CRLF line endings (should be LF)")

    # Read file as text for structure validation
    try:
        content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"File {filename} is not valid UTF-8: {e}")

    # Check file ends with newline
    if not content.endswith('\n'):
        raise ValueError(f"File {filename} does not end with newline")

    # Parse lines
    lines = content.split('\n')

    # Check H1 heading on first line
    if not lines[0].startswith('# '):
        raise ValueError(f"File {filename} missing H1 heading on line 1")

    if len(lines[0]) <= 2:
        raise ValueError(f"File {filename} has empty heading")

    # Check blank line on second line
    if len(lines) < 2 or lines[1] != '':
        raise ValueError(f"File {filename} missing blank line on line 2")

    # Check prose content with 2-3 sentences
    prose_lines = lines[2:-1]  # Exclude heading, blank line, and trailing empty line
    prose_text = '\n'.join(prose_lines).strip()

    if not prose_text:
        raise ValueError(f"File {filename} missing prose content")

    # Count sentences (periods)
    sentence_count = prose_text.count('.')
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"File {filename} has {sentence_count} sentences; expected 2-3"
        )

    # Check file size (300-800 bytes) - check last so structural issues are caught first
    file_size = file_path.stat().st_size
    if file_size < 300:
        raise ValueError(f"File {filename} is {file_size} bytes; minimum is 300")
    if file_size > 800:
        raise ValueError(f"File {filename} is {file_size} bytes; maximum is 800")


def git_add(filename):
    """
    Stage file in git.

    Args:
        filename: Path to file to stage

    Raises:
        subprocess.CalledProcessError: If git add fails
    """
    subprocess.run(['git', 'add', filename], check=True, capture_output=True, text=True)


def git_commit(message):
    """
    Create commit with provided message.

    Args:
        message: Commit message

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    subprocess.run(
        ['git', 'commit', '-m', message],
        check=True,
        capture_output=True,
        text=True
    )


def git_push():
    """
    Push commit to remote on current branch.

    Pushes to HEAD (current branch) with -u flag to set upstream tracking.

    Raises:
        subprocess.CalledProcessError: If git push fails
    """
    subprocess.run(
        ['git', 'push', '-u', 'origin', 'HEAD'],
        check=True,
        capture_output=True,
        text=True
    )


def main():
    """
    Orchestrate markdown file creation, validation, and git operations.

    Workflow:
    1. Create markdown file with title and prose
    2. Validate file structure, encoding, size
    3. Stage file in git
    4. Create commit with conventional message
    5. Push to feature branch

    Exit codes:
    - 0: Success
    - 1: Failure (validation error, file I/O error, or git error)
    """
    try:
        # Phase 1: Create file
        create_file()

        # Phase 2: Validate file before git operations (FR-8)
        validate_file(FILENAME)

        # Phase 3: Git workflow
        git_add(FILENAME)
        git_commit(COMMIT_MESSAGE)
        git_push()

        print(f"✓ Successfully created and pushed {FILENAME}")
        sys.exit(0)

    except ValueError as e:
        # Validation error
        print(f"✗ Validation error: {e}", file=sys.stderr)
        sys.exit(1)

    except OSError as e:
        # File I/O error
        print(f"✗ File I/O error: {e}", file=sys.stderr)
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        # Git command error
        print(f"✗ Git error: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        # Unexpected error
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
