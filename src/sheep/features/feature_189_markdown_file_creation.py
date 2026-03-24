"""Implementation for feature 189: Create markdown file test-joedur.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from prior features. The file is created with:
- Exact filename: test-joedur.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 400-600 bytes
- Git staging, commit, and push operations
"""

import subprocess
import sys
from pathlib import Path

# Task 1: Define file content constants
FILENAME = "test-joedur.md"
TITLE = "The Importance of Continuous Learning"
PROSE = "Continuous learning is essential for personal growth and professional success in today's rapidly changing world. By embracing a mindset of curiosity and seeking new knowledge, individuals can adapt to challenges and unlock new opportunities for career advancement. Lifelong learning not only enhances skills and knowledge but also fosters confidence and resilience in the face of uncertainty and change."


def check_file_does_not_exist() -> None:
    """Verify that test-joedur.md does not already exist.

    Raises:
        ValueError: If file exists with descriptive message
    """
    if Path(FILENAME).exists():
        raise ValueError(f"File {FILENAME} already exists")


def create_markdown_file() -> str:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings.

    Returns:
        Path to created file

    Raises:
        OSError: If file write operation fails
    """
    content = f"# {TITLE}\n\n{PROSE}\n"
    Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")
    return str(Path(FILENAME).absolute())


def validate_encoding(filepath: str) -> None:
    """Validate file encoding (UTF-8 without BOM).

    Args:
        filepath: Path to file to validate

    Raises:
        ValueError: If encoding is invalid or has BOM
    """
    binary_content = Path(filepath).read_bytes()

    # Check for UTF-8 BOM
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File must not have UTF-8 BOM")

    # Verify UTF-8 decoding
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("File must be UTF-8 encoded")


def validate_line_endings(filepath: str) -> None:
    """Validate file uses Unix LF line endings only.

    Args:
        filepath: Path to file to validate

    Raises:
        ValueError: If file contains CRLF
    """
    binary_content = Path(filepath).read_bytes()

    if b"\r\n" in binary_content:
        raise ValueError("File must use Unix LF line endings only")


def validate_structure(filepath: str) -> None:
    """Validate markdown structure, sentence count, and file size.

    Checks:
    - First line starts with "# " (H1 heading)
    - Second line is empty (blank line)
    - Contains 2-3 sentences of prose
    - File size between 400-600 bytes
    - File ends with newline

    Args:
        filepath: Path to file to validate

    Raises:
        ValueError: If validation fails
    """
    text_content = Path(filepath).read_text(encoding="utf-8")
    lines = text_content.split("\n")

    # Validate H1 heading on first line
    if not lines[0].startswith("# "):
        raise ValueError("First line must be H1 heading (# )")

    # Validate blank line on second line
    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank (separator after heading)")

    # Get prose content (skip heading and blank line)
    prose_lines = lines[2:]
    while prose_lines and prose_lines[-1] == "":
        prose_lines.pop()

    if not prose_lines:
        raise ValueError("No prose content found after heading")

    prose_content = "\n".join(prose_lines).strip()

    # Validate sentence count
    sentence_count = prose_content.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(f"Content must have 2-3 sentences, found {sentence_count}")

    # Validate file size
    file_size = Path(filepath).stat().st_size
    if file_size < 400 or file_size > 600:
        raise ValueError(f"File size must be 400-600 bytes, found {file_size}")

    # Validate file ends with newline
    if not text_content.endswith("\n"):
        raise ValueError("File must end with trailing newline")


def stage_file(filename: str) -> None:
    """Stage file with git add.

    Args:
        filename: Name of file to stage

    Raises:
        subprocess.CalledProcessError: If git add fails
    """
    subprocess.run(["git", "add", filename], check=True, capture_output=True)


def commit_file(filename: str, message: str) -> None:
    """Commit file with conventional message.

    Args:
        filename: Name of file being committed
        message: Commit message to use

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)


def push_file() -> None:
    """Push commit to remote repository.

    Raises:
        subprocess.CalledProcessError: If git push fails
    """
    subprocess.run(
        ["git", "push", "-u", "origin", "HEAD"],
        check=True,
        capture_output=True
    )


def main() -> None:
    """Orchestrate complete workflow: create, validate, and git operations.

    Phase 1: File Creation & Validation
    - Create markdown file with H1 + 2-3 sentences
    - Validate UTF-8 encoding, Unix LF line endings, structure, and size

    Phase 2: Git Integration
    - Stage file with git add
    - Commit with conventional message
    - Push to remote repository

    Raises:
        ValueError: If validation fails
        OSError: If file operations fail
        subprocess.CalledProcessError: If git operations fail
    """
    try:
        # Phase 1: File Creation & Validation
        print(f"Creating {FILENAME}...")
        check_file_does_not_exist()
        filepath = create_markdown_file()
        print(f"✓ File created: {filepath}")

        print("Validating file...")
        validate_encoding(filepath)
        print("✓ UTF-8 encoding valid")

        validate_line_endings(filepath)
        print("✓ Unix LF line endings valid")

        validate_structure(filepath)
        print("✓ Markdown structure valid")

        # Phase 2: Git Integration
        print("Staging file with git add...")
        stage_file(FILENAME)
        print("✓ File staged")

        commit_message = f"feat(189): create markdown file {FILENAME} with prose content"
        print(f"Committing with message: {commit_message}")
        commit_file(FILENAME, commit_message)
        print("✓ File committed")

        print("Pushing to remote...")
        push_file()
        print("✓ File pushed to remote")

        print(f"\n✓ Successfully created and published {FILENAME}")

    except ValueError as e:
        print(f"✗ Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"✗ File I/O error: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"✗ Git operation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    """Execute feature 189 when run as a script."""
    main()
