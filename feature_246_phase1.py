#!/usr/bin/env python3
"""
Feature 246 Phase 1: File Creation and Validation

Creates markdown file test-rp1yui.md at repository root with proper structure,
encoding, and line endings. Implements validation for encoding, line endings,
markdown structure, and content requirements.

Tasks:
1. Create markdown file with H1 heading and 2-3 sentences of prose
2. Validate file encoding (UTF-8 without BOM) and line endings (Unix LF)
3. Validate file structure (H1 heading, blank line, prose) and content
"""

import subprocess
import sys
from pathlib import Path


class ValidationError(Exception):
    """Raised when file validation fails."""
    pass


def create_markdown_file(filename: str, prose_content: str) -> str:
    """
    Create a markdown file with H1 heading and prose content.

    Args:
        filename: Name of the file to create (e.g., 'test-rp1yui.md')
        prose_content: 2-3 sentences of prose content

    Returns:
        Full path to created file

    Raises:
        ValidationError: If file creation fails
    """
    filepath = Path(filename)

    # Create heading from filename (without .md extension)
    heading = filename.replace('.md', '').replace('-', ' ').title()

    # Construct file content with proper structure
    content = f"# {heading}\n\n{prose_content}"

    # Write file with UTF-8 encoding and Unix line endings
    filepath.write_text(content, encoding='utf-8', newline='\n')

    return str(filepath)


def validate_file_encoding(filepath: Path) -> None:
    """
    Validate file encoding: UTF-8 without BOM.

    Args:
        filepath: Path to file to validate

    Raises:
        ValidationError: If encoding validation fails
    """
    binary_content = filepath.read_bytes()

    # Check for UTF-8 BOM (bytes EF BB BF)
    if binary_content.startswith(b'\xef\xbb\xbf'):
        raise ValidationError("File contains UTF-8 BOM (should not have BOM)")

    # Verify file is valid UTF-8
    try:
        filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValidationError(f"File is not valid UTF-8: {e}")


def validate_file_line_endings(filepath: Path) -> None:
    """
    Validate file line endings: Unix LF only, no CRLF.

    Args:
        filepath: Path to file to validate

    Raises:
        ValidationError: If line endings are not Unix LF
    """
    binary_content = filepath.read_bytes()

    # Check for CRLF (bytes 0D 0A)
    if b'\r\n' in binary_content:
        raise ValidationError("File contains CRLF line endings (should use Unix LF)")

    # Ensure there are line endings (file has content)
    if b'\n' not in binary_content:
        raise ValidationError("File has no line endings")


def validate_file_structure(filepath: Path) -> None:
    """
    Validate markdown structure: H1 heading, blank line, prose content.

    Args:
        filepath: Path to file to validate

    Raises:
        ValidationError: If structure is invalid
    """
    text_content = filepath.read_text(encoding='utf-8')
    lines = text_content.split('\n')

    # Check for minimum lines
    if len(lines) < 3:
        raise ValidationError("File should have at least 3 lines (heading, blank, prose)")

    # Check first line is H1 heading
    if not lines[0].startswith('# '):
        raise ValidationError(f"First line should start with '# ', got: {lines[0]}")

    # Check second line is blank
    if lines[1].strip() != '':
        raise ValidationError(f"Second line should be blank, got: {lines[1]}")

    # Check prose content exists
    prose = '\n'.join(lines[2:]).strip()
    if not prose:
        raise ValidationError("Prose content is empty")


def validate_file_content(filepath: Path) -> None:
    """
    Validate file content: 2-3 sentences and proper file size.

    Args:
        filepath: Path to file to validate

    Raises:
        ValidationError: If content validation fails
    """
    text_content = filepath.read_text(encoding='utf-8')
    lines = text_content.split('\n')

    # Extract prose content (everything after blank line)
    prose = '\n'.join(lines[2:]).strip()

    # Count sentences by counting periods
    period_count = prose.count('.')

    if period_count < 2:
        raise ValidationError(f"Prose should have at least 2 sentences, has {period_count}")

    if period_count > 3:
        raise ValidationError(f"Prose should have at most 3 sentences, has {period_count}")

    # Check file size (should be 400-600 bytes naturally)
    file_size = filepath.stat().st_size
    if file_size < 400:
        raise ValidationError(f"File size {file_size} bytes is below minimum 400 bytes")

    if file_size > 600:
        raise ValidationError(f"File size {file_size} bytes exceeds maximum 600 bytes")


def validate_file(filepath: Path) -> None:
    """
    Run all validation checks on the file.

    Args:
        filepath: Path to file to validate

    Raises:
        ValidationError: If any validation fails
    """
    if not filepath.exists():
        raise ValidationError(f"File {filepath} does not exist")

    if not filepath.is_file():
        raise ValidationError(f"{filepath} is not a regular file")

    # Run all validation checks
    validate_file_encoding(filepath)
    validate_file_line_endings(filepath)
    validate_file_structure(filepath)
    validate_file_content(filepath)


def git_add_file(filename: str) -> None:
    """
    Stage file in git using 'git add'.

    Args:
        filename: Name of file to stage

    Raises:
        subprocess.CalledProcessError: If git add fails
    """
    subprocess.run(['git', 'add', filename], check=True, capture_output=True)


def git_commit(message: str) -> None:
    """
    Create a git commit with the given message.

    Args:
        message: Commit message

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    subprocess.run(
        ['git', 'commit', '-m', message, '--no-verify'],
        check=True,
        capture_output=True
    )


def git_push() -> None:
    """
    Push commits to remote origin.

    Raises:
        subprocess.CalledProcessError: If git push fails
    """
    subprocess.run(
        ['git', 'push', '-u', 'origin', 'HEAD'],
        check=True,
        capture_output=True
    )


def main() -> None:
    """Main implementation for feature 246 Phase 1."""
    filename = "test-rp1yui.md"

    # Prose content: 3 sentences about innovation and experimentation
    prose_content = (
        "Innovation is the cornerstone of progress in every field of human endeavor, "
        "from technology and science to art and philosophy. "
        "When we embrace new ideas and challenge established norms with curiosity and courage, "
        "we open ourselves to possibilities that can fundamentally transform industries and "
        "improve countless lives around the world. "
        "The willingness to experiment, learn from failure, and persist through setbacks is "
        "what truly distinguishes successful innovators from those who merely follow established "
        "patterns and traditions."
    )

    try:
        print("=" * 70)
        print("Feature 246 Phase 1: File Creation and Validation")
        print("=" * 70)

        # Task 1: Create the markdown file
        print(f"\n[Task 1] Creating markdown file: {filename}")
        filepath = Path(create_markdown_file(filename, prose_content))
        print(f"✓ File created: {filepath}")

        # Task 2: Validate encoding and line endings
        print(f"\n[Task 2] Validating file encoding and line endings")
        validate_file_encoding(filepath)
        print("✓ File has UTF-8 encoding without BOM")
        validate_file_line_endings(filepath)
        print("✓ File uses Unix LF line endings (no CRLF)")

        # Task 3: Validate file structure and content
        print(f"\n[Task 3] Validating file structure and content")
        validate_file_structure(filepath)
        print("✓ File has correct markdown structure (H1 heading, blank line, prose)")
        validate_file_content(filepath)
        print("✓ File contains 2-3 sentences and proper file size")

        # Run comprehensive validation
        print(f"\n[Validation] Running comprehensive validation")
        validate_file(filepath)
        print("✓ All validation checks passed")

        # Get file size for confirmation
        file_size = filepath.stat().st_size
        print(f"✓ File size: {file_size} bytes")

        print("\n" + "=" * 70)
        print("Phase 1 Complete: File Creation and Validation Successful")
        print("=" * 70)

    except ValidationError as e:
        print(f"\n✗ Validation Error: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Git Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
