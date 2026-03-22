#!/usr/bin/env python3
"""
Feature 154: Create markdown file test-gbki7t.md with prose content.
Phase 1: File Creation & Validation
"""

from pathlib import Path


# Task 1: Create and validate prose content string
def create_prose_content():
    """Create prose content with H1 heading and 2-3 sentences."""
    content = """# Artificial Intelligence

Artificial intelligence has revolutionized how we process information and solve complex problems across industries. Machine learning algorithms enable systems to learn from data without explicit programming, making them increasingly adaptable and powerful. As AI continues to evolve, it promises to unlock new possibilities in healthcare, education, and scientific discovery."""

    # Validate content structure
    assert content.startswith('# '), "Content must start with H1 heading"
    assert '\n\n' in content, "Content must have blank line after heading"

    # Split by double newline to separate heading from prose
    parts = content.split('\n\n', 1)
    assert len(parts) == 2, "Content must have heading followed by blank line and prose"
    
    heading, prose = parts

    # Count sentences (simplified: count periods, exclamation marks, question marks)
    sentence_count = prose.count('.') + prose.count('!') + prose.count('?')
    assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, found {sentence_count}"

    return content


# Task 2: Write markdown file with pathlib and proper encoding/line endings
def write_markdown_file(content):
    """Write markdown file with UTF-8 encoding and LF line endings."""
    filepath = Path("test-gbki7t.md")

    # Verify file doesn't exist before creation (or will be overwritten)
    if filepath.exists():
        filepath.unlink()

    # Write file with explicit UTF-8 encoding and LF line endings
    filepath.write_text(content, encoding='utf-8', newline='\n')

    # Verify file was created
    assert filepath.exists(), "File was not created"

    # Verify file is readable and contains expected content
    read_content = filepath.read_text(encoding='utf-8')
    assert read_content == content, "File content does not match"

    return filepath


# Task 3: Verify file encoding, line endings, and markdown format compliance
def validate_markdown_file(filepath):
    """Validate file encoding, line endings, and markdown format."""
    # Read file as binary to check encoding
    file_bytes = filepath.read_bytes()

    # Check for UTF-8 BOM (should not be present)
    assert file_bytes[:3] != b'\xef\xbb\xbf', "File must not contain UTF-8 BOM"

    # Check for CRLF line endings (should use LF only)
    assert b'\r\n' not in file_bytes, "File must use LF line endings, not CRLF"

    # Read as text and validate structure
    file_text = filepath.read_text(encoding='utf-8')

    # Verify H1 heading exists and is first line
    assert file_text.startswith('# '), "File must start with H1 heading"

    # Verify blank line after heading
    lines = file_text.split('\n')
    assert len(lines) >= 3, "File must have heading, blank line, and prose"
    assert lines[0].startswith('# '), "First line must be H1 heading"
    assert lines[1] == '', "Second line must be blank"

    # Count sentences in prose section
    prose_section = '\n'.join(lines[2:])
    sentence_count = prose_section.count('.') + prose_section.count('!') + prose_section.count('?')
    assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, found {sentence_count}"

    # Verify file size is in expected range (400-600 bytes guideline)
    file_size = len(file_bytes)
    assert 200 <= file_size <= 1000, f"File size {file_size} bytes is outside reasonable range"

    print("[PASS] File validation passed")
    print("  - Encoding: UTF-8 (no BOM)")
    print("  - Line endings: LF")
    print("  - Heading: Present")
    print("  - Sentences: {}".format(sentence_count))
    print("  - Size: {} bytes".format(file_size))


def main():
    """Run all tasks for phase 1: File Creation & Validation."""
    print("Phase 1: File Creation & Validation")
    print("=" * 50)

    # Task 1: Create prose content
    print("\nTask 1: Create and validate prose content string...")
    content = create_prose_content()
    print("[PASS] Prose content created and validated")

    # Task 2: Write markdown file
    print("\nTask 2: Write markdown file with pathlib...")
    filepath = write_markdown_file(content)
    print("[PASS] File created: {}".format(filepath))

    # Task 3: Validate file
    print("\nTask 3: Verify file encoding, line endings, and format...")
    validate_markdown_file(filepath)

    print("\n" + "=" * 50)
    print("Phase 1 complete: All tasks passed")


if __name__ == '__main__':
    main()
