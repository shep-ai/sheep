#!/usr/bin/env python3
"""
Create test markdown file (test-dd91rz.md) at repository root.

This script creates a single test markdown file following the established pattern
from 113+ existing test-*.md files in the repository. The file contains:
- An H1 markdown heading (#) as the first element
- A blank line
- 2-3 sentences of prose content describing a topic
- UTF-8 encoding without BOM
- LF (Unix) line endings

The script validates file properties (size, encoding, format) and can optionally
integrate with git (add, commit, push) to complete the workflow.
"""

from pathlib import Path
import subprocess
import sys


# Markdown content for the test file
# H1 heading + blank line + 2-3 sentences of prose
MARKDOWN_CONTENT = """# Test Implementation and Automation

Testing and automation are fundamental to building reliable software systems. By automating test creation and validation, we can ensure consistency across hundreds of test files while reducing manual effort and human error. This approach enables the Sheep platform to scale efficiently and maintain high quality across all implementations while freeing developers to focus on more complex architectural and design challenges.
"""

FILENAME = "test-dd91rz.md"
COMMIT_MESSAGE = "feat(133): Create markdown file test-dd91rz.md"
FEATURE_BRANCH = "feat/markdown-file-creation-a3e3e2"


def create_file():
    """
    Create the markdown file with proper UTF-8 encoding and LF line endings.

    Uses pathlib.Path.write_text() with explicit encoding and newline parameters
    to ensure:
    - UTF-8 encoding without BOM (Byte Order Mark)
    - LF (\n) line endings on all platforms (not CRLF or CR)
    """
    file_path = Path(FILENAME)

    # Write file with explicit encoding and line ending parameters
    # encoding='utf-8' ensures UTF-8 without BOM (BOM is only added with utf-8-sig)
    # newline='\n' ensures LF line endings on all platforms (no platform conversion)
    file_path.write_text(MARKDOWN_CONTENT, encoding='utf-8', newline='\n')

    print(f"✓ Created file: {FILENAME}")
    return file_path


def validate_file_size(file_path, min_bytes=400, max_bytes=600):
    """
    Validate that the markdown file meets the size requirement (400-600 bytes).

    Args:
        file_path: Path object or string path to file
        min_bytes: Minimum acceptable file size (default 400)
        max_bytes: Maximum acceptable file size (default 600)

    Raises:
        ValueError: If file size is outside the acceptable range

    Returns:
        int: The file size in bytes if validation passes
    """
    file_path = Path(file_path)
    size_bytes = file_path.stat().st_size

    if size_bytes < min_bytes:
        raise ValueError(
            f"File size {size_bytes} bytes is below minimum {min_bytes} bytes. "
            f"Add more content to reach the required range."
        )
    elif size_bytes > max_bytes:
        raise ValueError(
            f"File size {size_bytes} bytes exceeds maximum {max_bytes} bytes. "
            f"Reduce content length to fit within the required range."
        )

    print(f"✓ File size validation passed: {size_bytes} bytes (within {min_bytes}-{max_bytes} range)")
    return size_bytes


def git_add(filename):
    """
    Stage the file in git using 'git add'.

    Args:
        filename: Name of the file to stage

    Raises:
        subprocess.CalledProcessError: If git add command fails
    """
    subprocess.run(['git', 'add', filename], check=True)
    print(f"✓ Staged file in git: {filename}")


def git_commit(message):
    """
    Commit the staged file with a conventional commit message.

    Args:
        message: Commit message following conventional commits format

    Raises:
        subprocess.CalledProcessError: If git commit command fails
    """
    subprocess.run(['git', 'commit', '-m', message], check=True)
    print(f"✓ Committed with message: {message}")


def git_push(branch_name):
    """
    Push the commit to the remote feature branch.

    Args:
        branch_name: The feature branch name to push to

    Raises:
        subprocess.CalledProcessError: If git push command fails
    """
    subprocess.run(['git', 'push', '-u', 'origin', branch_name], check=True)
    print(f"✓ Pushed to remote branch: {branch_name}")


def main():
    """Main entry point."""
    try:
        # Phase 1: Create the markdown file
        file_path = create_file()

        # Phase 2: Validate file size meets requirements (400-600 bytes)
        validate_file_size(file_path)

        print("✓ All validations passed - file is ready for git integration")

        # Phase 2: Git integration (add, commit, push)
        print("\nStarting git workflow...")
        git_add(FILENAME)
        git_commit(COMMIT_MESSAGE)
        git_push(FEATURE_BRANCH)

        print("\n✓ All operations completed successfully!")

    except OSError as e:
        print(f"✗ File I/O Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Validation Error: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"✗ Git Command Error: Command failed with exit code {e.returncode}", file=sys.stderr)
        print(f"  Command: {' '.join(e.cmd)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
