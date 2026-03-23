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
    - H1 heading on line 1: "# [Title]"
    - Blank line on line 2: empty line for readability
    - 2-3 sentences of prose content starting on line 3
    - Trailing newline at end: ensures POSIX compliance

    The file is encoded in UTF-8 without Byte Order Mark (BOM) and uses Unix LF
    line endings (\n) exclusively, ensuring consistent behavior across all platforms
    (Windows, Linux, macOS) regardless of git configuration (autocrlf settings).

    Implementation Notes:
    - Uses pathlib.Path.write_text() for cross-platform compatibility
    - Explicit encoding='utf-8' (not 'utf-8-sig') prevents BOM insertion
    - Explicit newline='\n' prevents platform-specific line ending conversion
    - File is created in the current working directory (repository root)

    Raises:
        OSError: If file cannot be created due to permissions, disk space, or
                  other file system errors.

    Returns:
        None (side effect: creates file on disk)
    """
    # Construct markdown content with proper structure and line endings
    # Format: H1 heading, blank line, prose, trailing newline
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Write file with explicit UTF-8 encoding and Unix LF line endings
    # newline='\n' ensures LF on all platforms (Windows, Linux, macOS)
    # encoding='utf-8' ensures UTF-8 without BOM (BOM only appears with 'utf-8-sig')
    # This approach has been validated across 170+ prior features in this repository
    file_path = Path(FILENAME)
    file_path.write_text(content, encoding='utf-8', newline='\n')


def validate_file(filename):
    """
    Validate markdown file structure, encoding, and size before git operations.

    Performs comprehensive validation to ensure the file meets all requirements
    before committing to git. This pre-commit validation prevents invalid files
    from entering the repository, maintaining data integrity and consistency.

    Validation checks (in order of execution):
    1. File existence: File must exist on disk
    2. File size: File must have non-zero size (not empty)
    3. UTF-8 encoding: File must be UTF-8 encoded (detects BOM bytes EF BB BF)
    4. Line endings: File must use Unix LF (\n), not Windows CRLF (\r\n)
    5. Structure: Must contain H1 heading, blank line, prose, trailing newline
    6. Prose content: Must have 2-3 sentences separated by periods
    7. File size range: Must be between 300-800 bytes (ensures reasonable prose length)

    Validation order is designed to fail fast on structural issues before checking
    size constraints, enabling users to understand and fix problems efficiently.

    Args:
        filename: Path to file to validate (relative or absolute)

    Raises:
        ValueError: If any validation check fails, includes clear error message
                    indicating the specific issue and expected constraint.

    Implementation Notes:
    - Uses binary file inspection for encoding/line ending checks (platform-independent)
    - Detects UTF-8 BOM by checking for bytes EF BB BF at file start
    - Detects CRLF by searching for byte sequence \r\n in binary content
    - Counts sentences by counting periods (.) in prose text
    - Extracts prose by splitting on newlines and stripping heading/blank line
    - File size checked last to avoid masking structural errors
    """
    file_path = Path(filename)

    # ===== PHASE 1: File existence and basic properties =====
    # Check file exists on disk
    if not file_path.exists():
        raise ValueError(f"File {filename} does not exist")

    # Check file has content (not empty)
    file_stat = file_path.stat()
    if file_stat.st_size == 0:
        raise ValueError(f"File {filename} is empty")

    # ===== PHASE 2: Encoding and line ending validation (binary inspection) =====
    # Read file as binary bytes to inspect encoding and line endings
    # Binary inspection is platform-independent and detects byte patterns reliably
    content_bytes = file_path.read_bytes()

    # Check for UTF-8 BOM (Byte Order Mark): EF BB BF in hex
    # UTF-8 BOM is optional and often undesired; this file must not have one
    if content_bytes.startswith(b'\xef\xbb\xbf'):
        raise ValueError(f"File {filename} has UTF-8 BOM")

    # Check for Windows CRLF line endings: \r\n (CR LF bytes)
    # File must use Unix LF (\n) exclusively, even on Windows
    # Git autocrlf conversion happens at commit time; source file must have LF
    if b'\r\n' in content_bytes:
        raise ValueError(f"File {filename} has CRLF line endings (should be LF)")

    # ===== PHASE 3: Structure validation (text parsing) =====
    # Read file as UTF-8 text for structural validation
    # Will raise ValueError if file is not valid UTF-8 (already checked for BOM above)
    try:
        content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"File {filename} is not valid UTF-8: {e}")

    # Check file ends with newline (POSIX compliance)
    # All text files should end with a newline character per POSIX standard
    if not content.endswith('\n'):
        raise ValueError(f"File {filename} does not end with newline")

    # Parse content into lines for structure validation
    # split('\n') includes empty string for trailing newline, which we exclude later
    lines = content.split('\n')

    # ===== PHASE 4: Heading validation =====
    # Check H1 heading on first line (CommonMark format: "# ")
    if not lines[0].startswith('# '):
        raise ValueError(f"File {filename} missing H1 heading on line 1")

    # Check heading is not empty (must have content after "# ")
    if len(lines[0]) <= 2:
        raise ValueError(f"File {filename} has empty heading")

    # ===== PHASE 5: Blank line validation =====
    # Check blank line on second line (provides readability after heading)
    # This is a markdown convention: heading followed by blank line before content
    if len(lines) < 2 or lines[1] != '':
        raise ValueError(f"File {filename} missing blank line on line 2")

    # ===== PHASE 6: Prose content validation =====
    # Extract prose content (lines after blank line, excluding trailing empty line)
    # lines[2:-1] excludes: heading (line 0), blank line (line 1), trailing empty (last)
    # The trailing empty string appears because content.split('\n') with trailing \n
    prose_lines = lines[2:-1]
    prose_text = '\n'.join(prose_lines).strip()

    # Check prose content exists (not empty)
    if not prose_text:
        raise ValueError(f"File {filename} missing prose content")

    # Count sentences by counting periods (.)
    # Valid file must have 2-3 sentences per specification
    sentence_count = prose_text.count('.')
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"File {filename} has {sentence_count} sentences; expected 2-3"
        )

    # ===== PHASE 7: File size validation =====
    # Check file size is within acceptable range (300-800 bytes per specification)
    # This constraint ensures:
    # - Minimum 300 bytes: sufficient for substantial prose content
    # - Maximum 800 bytes: prevents excessively long files
    # Size checked last so structural errors are reported before size issues
    file_size = file_path.stat().st_size
    if file_size < 300:
        raise ValueError(f"File {filename} is {file_size} bytes; minimum is 300")
    if file_size > 800:
        raise ValueError(f"File {filename} is {file_size} bytes; maximum is 800")


def git_add(filename):
    """
    Stage file in git (add to index/staging area).

    Stages the specified file in git's staging area, marking it for inclusion
    in the next commit. This operation must succeed before the file can be
    committed to the repository.

    Implementation:
    - Uses subprocess.run() with check=True for explicit error handling
    - Uses args as list (not shell=True) to prevent command injection
    - Captures output for debugging purposes

    Args:
        filename: Path to file to stage (relative or absolute)

    Raises:
        subprocess.CalledProcessError: If git add fails (e.g., file not found,
                                       not a git repository, permissions error).
                                       Includes exit code and stderr from git.

    Returns:
        None (side effect: stages file in git index)
    """
    subprocess.run(['git', 'add', filename], check=True, capture_output=True, text=True)


def git_commit(message):
    """
    Create commit with conventional commit message.

    Creates a commit in the current git repository with the provided message.
    The commit captures the staged changes (file creation) and includes metadata
    (author, timestamp, message) in git history.

    Implementation:
    - Uses subprocess.run() with check=True for explicit error handling
    - Uses -m flag to specify commit message directly (no editor)
    - Uses args as list (not shell=True) to prevent command injection

    Args:
        message: Commit message in conventional commit format
                 (e.g., "feat(175): create markdown file test-rh39t2.md with prose content")

    Raises:
        subprocess.CalledProcessError: If git commit fails (e.g., no staged changes,
                                       git not configured with user.name/user.email,
                                       repository in invalid state).
                                       Includes exit code and stderr from git.

    Returns:
        None (side effect: creates commit in git history)
    """
    subprocess.run(
        ['git', 'commit', '-m', message],
        check=True,
        capture_output=True,
        text=True
    )


def git_push():
    """
    Push commit to remote repository on current branch.

    Pushes the created commit to the remote repository (origin) on the current
    branch, making the changes available to other users and CI/CD systems.
    The -u flag establishes upstream branch tracking.

    Implementation:
    - Uses HEAD (current branch) for branch-agnostic operation
    - Uses -u flag to set upstream tracking for subsequent operations
    - Uses subprocess.run() with check=True for explicit error handling
    - Uses args as list (not shell=True) to prevent command injection

    Args:
        None (operates on current git branch)

    Raises:
        subprocess.CalledProcessError: If git push fails (e.g., network error,
                                       remote repository unreachable, push rejected
                                       due to branch protection or conflicts).
                                       Includes exit code and stderr from git.

    Returns:
        None (side effect: pushes commits to remote repository)
    """
    subprocess.run(
        ['git', 'push', '-u', 'origin', 'HEAD'],
        check=True,
        capture_output=True,
        text=True
    )


def main():
    """
    Orchestrate complete markdown file creation workflow.

    Implements the full pipeline for creating and committing a markdown file:

    Workflow (in order):
    1. **Create file**: Generate markdown file with H1 heading and prose content
    2. **Validate file**: Verify structure, encoding, size before git operations
    3. **Stage in git**: Add file to git's staging area
    4. **Commit**: Create commit with conventional commit message
    5. **Push**: Push commit to remote repository on current branch

    This orchestration ensures:
    - Invalid files are caught before entering git repository (FR-8)
    - Clear error messages guide users to fix issues (NFR-6)
    - Proper exit codes integrate with CI/CD pipelines and shell scripts
    - Consistent workflow across all markdown file creation features

    Exit Codes:
    - 0: Success (file created, validated, committed, and pushed)
    - 1: Failure (any error in validation, file I/O, or git operations)

    Error Handling:
    - ValueError: Validation errors (structure, encoding, size) - user-facing
    - OSError: File I/O errors (permissions, disk space) - system-level
    - CalledProcessError: Git operation failures - operation-specific
    - Exception: Unexpected errors - catches any unforeseen issues

    All errors are logged to stderr with clear context before exiting with code 1.
    Success is logged to stdout before exiting with code 0.

    Returns:
        None (function calls sys.exit() to set process exit code)
    """
    try:
        # ===== PHASE 1: File Creation =====
        # Create markdown file with title and prose content
        # Uses pathlib.Path.write_text() with explicit UTF-8 encoding and LF line endings
        create_file()

        # ===== PHASE 2: File Validation =====
        # Validate file structure, encoding, size, and line endings before git operations
        # This pre-commit validation (FR-8) prevents invalid files from entering repository
        # Validation checks: existence, content, encoding, line endings, structure, prose, size
        validate_file(FILENAME)

        # ===== PHASE 3: Git Workflow =====
        # Stage the validated file in git's index/staging area
        git_add(FILENAME)

        # Create commit with conventional commit message
        # Message format: "feat(175): create markdown file test-rh39t2.md with prose content"
        git_commit(COMMIT_MESSAGE)

        # Push commit to remote repository on current branch
        # Uses HEAD for branch-agnostic operation and -u for upstream tracking
        git_push()

        # Success: all phases completed without error
        print(f"✓ Successfully created and pushed {FILENAME}")
        sys.exit(0)

    except ValueError as e:
        # Validation error: file structure, encoding, size, or line endings
        # These are user-facing errors that indicate the file needs to be corrected
        print(f"✗ Validation error: {e}", file=sys.stderr)
        sys.exit(1)

    except OSError as e:
        # File I/O error: permissions denied, disk space, file not found after creation
        # These indicate system-level issues that may require administrator intervention
        print(f"✗ File I/O error: {e}", file=sys.stderr)
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        # Git command error: network issue, invalid repository, permissions, branch protection
        # These indicate problems with git operations that may require git configuration
        print(f"✗ Git error: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        # Unexpected error: catches any unforeseen exceptions
        # Included for robustness; should not occur in normal operation
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
