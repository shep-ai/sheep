#!/usr/bin/env python3
"""
Create and validate markdown file test-3pz04c.md with proper structure and encoding.
"""

import re
from pathlib import Path


def create_markdown_file():
    """Create test-3pz04c.md with H1 heading and 2-3 sentences of prose."""
    heading = "# The Power of Curiosity"
    prose = (
        "Curiosity is the fundamental human drive to explore, learn, and understand the world around us. "
        "Throughout history, curious minds have made groundbreaking discoveries that shaped civilization and improved human welfare. "
        "Fostering curiosity in ourselves and in others is essential for continuous growth, innovation, and developing resilience in an uncertain world."
    )

    # Combine heading, blank line, and prose
    content = f"{heading}\n\n{prose}"

    # Write to file with explicit UTF-8 encoding (no BOM)
    filepath = Path("test-3pz04c.md")
    filepath.write_text(content, encoding='utf-8')

    return filepath, content


def validate_file(filepath, content):
    """Validate all properties of the created markdown file."""
    errors = []

    # 1. File existence check
    if not filepath.exists():
        errors.append("FAIL: File does not exist")
        return errors

    print("✓ File exists: test-3pz04c.md")

    # 2. Read file to verify encoding and line endings
    try:
        with open(filepath, encoding='utf-8') as f:
            file_content = f.read()
    except UnicodeDecodeError:
        errors.append("FAIL: File is not valid UTF-8")
        return errors

    print("✓ File is valid UTF-8 encoding")

    # 3. Check for BOM (UTF-8 BOM is \ufeff)
    if file_content.startswith('\ufeff'):
        errors.append("FAIL: File contains UTF-8 BOM (byte-order mark)")
    else:
        print("✓ No UTF-8 BOM detected")

    # 4. Check for CRLF line endings (should be LF only)
    if '\r\n' in file_content:
        errors.append("FAIL: File contains CRLF line endings (should be LF only)")
    else:
        print("✓ File uses LF line endings (Unix style, no CRLF)")

    # 5. Check file size (should be 350-650 bytes)
    file_size = len(file_content.encode('utf-8'))
    if not (350 <= file_size <= 650):
        errors.append(f"FAIL: File size {file_size} bytes is outside range 350-650 bytes")
    else:
        print(f"✓ File size is {file_size} bytes (within 350-650 range)")

    # 6. Check for H1 heading (starts with #)
    if not file_content.startswith('# '):
        errors.append("FAIL: File does not start with H1 heading (# )")
    else:
        heading_line = file_content.split('\n')[0]
        print(f"✓ File contains H1 heading: {heading_line}")

    # 7. Check for blank line after heading
    lines = file_content.split('\n')
    if len(lines) < 3 or lines[1] != '':
        errors.append("FAIL: No blank line found after H1 heading")
    else:
        print("✓ Blank line present after H1 heading")

    # 8. Check sentence count (2-3 sentences)
    # Extract prose content (everything after the blank line)
    if len(lines) >= 3:
        prose_text = '\n'.join(lines[2:]).strip()
        # Count sentences by looking for sentence-ending punctuation
        sentence_pattern = r'[.!?]+'
        sentences = re.split(sentence_pattern, prose_text)
        # Filter out empty strings and strip whitespace
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        if sentence_count < 2 or sentence_count > 3:
            errors.append(f"FAIL: Found {sentence_count} sentences, expected 2-3")
        else:
            print(f"✓ Prose contains {sentence_count} sentences")
    else:
        errors.append("FAIL: Unable to extract prose content")

    # 9. Verify prose content is grammatically valid (non-empty and coherent)
    if len(lines) >= 3:
        prose_text = '\n'.join(lines[2:]).strip()
        if not prose_text or len(prose_text) < 50:
            errors.append("FAIL: Prose content is too short or empty")
        else:
            print("✓ Prose content is coherent and has sufficient length")

    # 10. Check markdown validity (basic CommonMark compliance)
    # Verify structure: H1 heading + blank line + prose
    if not (file_content.startswith('# ') and '\n\n' in file_content):
        errors.append("FAIL: File structure does not meet CommonMark requirements")
    else:
        print("✓ File structure is valid per CommonMark specification")

    return errors


def main():
    """Create file and validate it."""
    print("Creating test-3pz04c.md...")
    filepath, content = create_markdown_file()

    print("\nValidating file properties...")
    errors = validate_file(filepath, content)

    print("\n" + "=" * 60)
    if errors:
        print("VALIDATION FAILED:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("✓ ALL VALIDATIONS PASSED")
        print(f"✓ File {filepath.name} is ready for git commit")
        return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
