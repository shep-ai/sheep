#!/usr/bin/env python3
"""
Create test markdown file (test-jnjm6g.md) at repository root.

This script creates a single test markdown file following the established pattern
from 65+ existing test-*.md files in the repository. The file contains:
- An H1 markdown heading (#) as the first element
- A blank line
- 2-3 sentences of prose content describing a topic
- UTF-8 encoding without BOM
- LF (Unix) line endings

The script validates file properties (encoding, format) and integrates with git
(add, commit, push) to complete the workflow.
"""

from pathlib import Path
import subprocess
import sys


# Markdown content for the test file
# H1 heading + blank line + 2-3 sentences of prose
MARKDOWN_CONTENT = """# The Art of Continuous Learning

Learning is not a destination but an ongoing journey that shapes how we understand and interact with the world. When we embrace curiosity and approach challenges as opportunities to grow, we develop resilience and adaptability that serve us throughout our lives. By cultivating a mindset of continuous improvement, we unlock our potential to solve complex problems and create meaningful impact.
"""

FILENAME = "test-jnjm6g.md"
COMMIT_MESSAGE = "feat(134): create markdown file test-jnjm6g.md with prose content"
FEATURE_BRANCH = "feat/markdown-sample-file-ad20e9"


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


def validate_file(file_path):
    """
    Validate that the markdown file meets all structural and encoding requirements.

    Checks:
    - File exists and has non-zero size
    - Content is valid UTF-8
    - File contains H1 heading on first line
    - File contains blank line after heading
    - File contains prose content (sentences)
    - File has no BOM bytes (UTF-8 without BOM)
    - File uses LF line endings, not CRLF
    - File ends with newline character

    Args:
        file_path: Path object or string path to file

    Raises:
        ValueError: If any validation check fails

    Returns:
        dict: Validation results with file size and content summary
    """
    file_path = Path(file_path)

    # Check file exists and has content
    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    size_bytes = file_path.stat().st_size
    if size_bytes == 0:
        raise ValueError(f"File is empty: {file_path}")

    print(f"✓ File exists with size: {size_bytes} bytes")

    # Read file as binary to check BOM and CRLF
    with open(file_path, 'rb') as f:
        binary_content = f.read()

    # Check for UTF-8 BOM (EF BB BF)
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File contains UTF-8 BOM; expected UTF-8 without BOM")

    print("✓ No UTF-8 BOM detected")

    # Check for CRLF (Windows line endings)
    if b'\r\n' in binary_content:
        raise ValueError("File contains CRLF line endings; expected Unix LF")

    print("✓ Unix LF line endings confirmed (no CRLF)")

    # Decode and validate text structure
    try:
        text_content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")

    print("✓ Valid UTF-8 encoding")

    # Check file ends with newline
    if not text_content.endswith('\n'):
        raise ValueError("File does not end with newline character")

    print("✓ File ends with newline")

    # Split into lines and validate structure
    lines = text_content.rstrip('\n').split('\n')

    if not lines:
        raise ValueError("File is empty (no lines)")

    # Check first line is H1 heading
    if not lines[0].startswith('# '):
        raise ValueError(f"First line is not H1 heading; got: {lines[0][:30]}")

    print(f"✓ H1 heading found: {lines[0]}")

    # Check second line is blank
    if len(lines) < 2:
        raise ValueError("File too short; needs heading, blank line, and prose")

    if lines[1] != '':
        raise ValueError(f"Second line should be blank; got: {lines[1][:30]}")

    print("✓ Blank line after heading confirmed")

    # Check prose content exists (sentences should have periods)
    if len(lines) < 3:
        raise ValueError("File too short; needs heading, blank line, and prose")

    prose_text = '\n'.join(lines[2:])
    sentence_count = prose_text.count('.')

    if sentence_count < 2:
        raise ValueError(f"Prose should contain 2-3 sentences; found {sentence_count}")

    print(f"✓ Prose content found: {sentence_count} sentences")

    # Validate typical file size (400-600 bytes is natural outcome of proper structure)
    if 350 < size_bytes < 700:
        print(f"✓ File size in typical range: {size_bytes} bytes")
    else:
        print(f"⚠ File size {size_bytes} bytes is outside typical 400-600 range (not critical)")

    return {
        'size_bytes': size_bytes,
        'heading': lines[0],
        'sentence_count': sentence_count
    }


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
        print("Phase 1: Creating markdown file...")
        # Phase 1: Create the markdown file
        file_path = create_file()

        # Phase 1: Validate file meets all requirements
        print("\nPhase 1: Validating file...")
        validation_results = validate_file(file_path)

        print("\n✓ Phase 1 complete - file created and validated")

        # Phase 2: Git integration (add, commit, push)
        print("\nPhase 2: Git integration...")
        git_add(FILENAME)
        git_commit(COMMIT_MESSAGE)
        git_push(FEATURE_BRANCH)

        print("\n✓ All operations completed successfully!")
        print(f"\nSummary:")
        print(f"  File: {FILENAME}")
        print(f"  Size: {validation_results['size_bytes']} bytes")
        print(f"  Heading: {validation_results['heading']}")
        print(f"  Sentences: {validation_results['sentence_count']}")

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
