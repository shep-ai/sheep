"""Implementation for feature 198: Create markdown file test-p27cj6.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from prior features. The file is created with:
- Exact filename: test-p27cj6.md
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

# Task 1: Define file content constants
FILENAME = "test-p27cj6.md"
TITLE = "The Power of Effective Communication"
PROSE = "Clear and thoughtful communication serves as the foundation for building strong relationships and achieving shared goals. When people express their ideas with clarity and listen with genuine empathy, misunderstandings dissolve and collaboration flourishes. Mastering the art of communication transforms both personal and professional endeavors into opportunities for meaningful connection and growth."


# Task 2: Implement file creation with encoding and line ending validation
def check_file_does_not_exist() -> None:
    """Verify that test-p27cj6.md does not already exist.

    Raises:
        FileExistsError: If file exists with descriptive message
    """
    if Path(FILENAME).exists():
        raise FileExistsError(f"File {FILENAME} already exists")


def create_markdown_file() -> str:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings.

    Returns:
        Path to created file

    Raises:
        FileExistsError: If file already exists
        OSError: If file write operation fails
    """
    check_file_does_not_exist()
    content = f"# {TITLE}\n\n{PROSE}\n"
    Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")
    return str(Path(FILENAME).absolute())


def validate_encoding() -> None:
    """Validate that file is properly encoded as UTF-8 without BOM.

    Checks:
    - File exists
    - File does not contain UTF-8 BOM (byte order mark: 0xEF 0xBB 0xBF)
    - File content is valid UTF-8 text

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file has UTF-8 BOM or invalid UTF-8 encoding
    """
    file_path = Path(FILENAME)

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File {FILENAME} does not exist")

    # Read file as binary to check for BOM and encoding
    binary_content = file_path.read_bytes()

    # Check for UTF-8 BOM (byte order mark)
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"File {FILENAME} contains UTF-8 BOM (byte order mark)")

    # Verify content is valid UTF-8
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File {FILENAME} contains invalid UTF-8 encoding: {e}") from e


def validate_line_endings(filename: str = FILENAME) -> None:
    """Validate that file uses Unix LF line endings exclusively.

    Rejects files with Windows CRLF (\\r\\n) or Mac CR (\\r) line endings.
    Ensures cross-platform consistency for markdown files.

    Args:
        filename: Path to file to validate (defaults to FILENAME)

    Raises:
        ValueError: If file contains CRLF or CR line endings
        FileNotFoundError: If file does not exist
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} not found")

    binary_content = file_path.read_bytes()

    # Check for CRLF (Windows line endings)
    if b"\r\n" in binary_content:
        raise ValueError(
            f"File {filename} contains Windows CRLF (\\r\\n) line endings. "
            "Only Unix LF (\\n) line endings are allowed."
        )

    # Check for CR without LF (old Mac line endings)
    if b"\r" in binary_content:
        raise ValueError(
            f"File {filename} contains Mac CR (\\r) carriage return characters. "
            "Only Unix LF (\\n) line endings are allowed."
        )


def count_sentences(text: str) -> int:
    """Count sentences in text based on periods.

    Counts the number of periods in the text, treating each period as
    the end of one sentence.

    Args:
        text: Text to count sentences in

    Returns:
        Number of sentences (count of periods)
    """
    return text.count(".")


def validate_structure(filename: str) -> None:
    """Validate markdown file structure: H1 heading and 2-3 sentences.

    Verifies that the file contains:
    - Exactly one H1 heading (line starting with "# ")
    - 2-3 sentences of prose content (counted by periods)

    Args:
        filename: Path to file to validate

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If H1 heading is missing or sentence count is not 2-3
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")

    # Check for H1 heading (must start with "# ")
    lines = content.split("\n")
    if not lines or not lines[0].startswith("# "):
        raise ValueError(
            "Invalid markdown structure: file must start with H1 heading (# Title)"
        )

    # Get prose content (everything after the heading and blank line)
    # Typically: lines[0] = "# Title", lines[1] = "", lines[2+] = prose
    prose_lines = []
    if len(lines) > 2:
        # Join all lines after the blank line, excluding the final empty line from trailing \n
        prose_lines = lines[2:]

    prose_text = "\n".join(prose_lines).strip()
    sentence_count = count_sentences(prose_text)

    if not (2 <= sentence_count <= 3):
        raise ValueError(
            f"Invalid markdown structure: expected 2-3 sentences, found {sentence_count}"
        )


def validate_file_size(filename: str) -> None:
    """Validate that file size is within acceptable range (300-600 bytes).

    Checks that the file exists and has a size between 300 and 600 bytes,
    inclusive. File sizes outside this range indicate potential truncation,
    padding, or content issues.

    Args:
        filename: Path to file to validate

    Raises:
        ValueError: If file size is outside the acceptable range (300-600 bytes)
    """
    min_size = 300
    max_size = 600

    file_path = Path(filename)
    file_size = file_path.stat().st_size

    if not (min_size <= file_size <= max_size):
        raise ValueError(
            f"File size {file_size} bytes outside acceptable range {min_size}-{max_size} bytes"
        )


def git_add(filename: str = FILENAME) -> None:
    """Stage file for commit using git add.

    Args:
        filename: Path to file to stage (defaults to FILENAME)

    Raises:
        subprocess.CalledProcessError: If git add command fails
    """
    subprocess.run(["git", "add", filename], check=True, capture_output=True)


def git_commit(message: str = "feat(198): Create markdown file test-p27cj6.md with title and prose content") -> None:
    """Commit staged changes with conventional commit message.

    Args:
        message: Commit message (defaults to feature 198 conventional format)

    Raises:
        subprocess.CalledProcessError: If git commit command fails
    """
    subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)


def git_push() -> None:
    """Push committed changes to remote repository.

    Pushes to origin with -u flag to set upstream tracking.

    Raises:
        subprocess.CalledProcessError: If git push command fails
    """
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True, capture_output=True)


def main() -> None:
    """Main orchestration function for feature 198.

    Executes the complete workflow:
    1. Create markdown file with H1 heading and prose content
    2. Validate encoding (UTF-8, no BOM)
    3. Validate line endings (Unix LF only)
    4. Validate structure (H1 heading + 2-3 sentences)
    5. Validate file size (300-600 bytes)
    6. Stage file with git add
    7. Commit with conventional message
    8. Push to remote repository

    All validation checks complete before any git operations begin.

    Raises:
        FileExistsError: If file already exists
        FileNotFoundError: If validation checks fail to find file
        ValueError: If any validation check fails
        subprocess.CalledProcessError: If any git operation fails
    """
    try:
        # Phase 1: Create file
        create_markdown_file()
        print(f"✓ Created {FILENAME}")

        # Phase 2: Run all validations before git operations
        validate_encoding()
        print("✓ Validated UTF-8 encoding")

        validate_line_endings()
        print("✓ Validated Unix LF line endings")

        validate_structure(FILENAME)
        print("✓ Validated markdown structure")

        validate_file_size(FILENAME)
        print("✓ Validated file size (300-600 bytes)")

        # Phase 3: Git operations (only if all validations pass)
        git_add()
        print("✓ Staged file with git add")

        git_commit()
        print("✓ Committed with message: feat(198): Create markdown file test-p27cj6.md with title and prose content")

        git_push()
        print("✓ Pushed to remote repository")

        print(f"\n✓ Feature 198 completed successfully: {FILENAME}")

    except FileExistsError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except (FileNotFoundError, ValueError) as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"✗ Git operation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
