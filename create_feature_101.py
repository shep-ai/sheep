#!/usr/bin/env python3
"""Script to create markdown file for feature 101."""

from pathlib import Path

from src.sheep.content_generators import (
    generate_markdown_content,
    validate_markdown_file,
    write_markdown_file,
)


def main():
    """Create markdown file test-59xln4.md with validation."""
    print("Feature 101: Creating markdown file test-59xln4.md")
    print("=" * 60)

    # Task 1: Generate content
    print("\nTask 1: Generating markdown content...")
    try:
        content = generate_markdown_content()
        print(f"✓ Generated {len(content)} bytes of content")
        print(f"\nContent preview (first 200 chars):\n{content[:200]}...")
    except Exception as e:
        print(f"✗ Failed to generate content: {e}")
        return False

    # Task 2: Write file to disk
    print("\nTask 2: Writing markdown file to disk...")
    try:
        filepath = write_markdown_file(content, "test-59xln4.md")
        print(f"✓ File written to: {filepath}")

        # Verify file exists
        if Path(filepath).exists():
            file_size = Path(filepath).stat().st_size
            print(f"✓ File verified: {file_size} bytes")
        else:
            print("✗ File was not created!")
            return False
    except Exception as e:
        print(f"✗ Failed to write file: {e}")
        return False

    # Task 3: Validate file
    print("\nTask 3: Validating markdown file...")
    try:
        validate_markdown_file(filepath)
        print("✓ File validation passed")
        print("\nValidation checks:")
        print("  ✓ UTF-8 encoding without BOM")
        print("  ✓ LF line endings (no CRLF)")
        print("  ✓ H1 heading present")
        print("  ✓ Blank line separator")
        print("  ✓ 2-3 sentences of prose")
        print("  ✓ Trailing newline")
        print("  ✓ File size in range (400-600 bytes)")
    except Exception as e:
        print(f"✗ File validation failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("✓ Feature 101 phase 1 complete!")
    print("  File: test-59xln4.md")
    print("  Ready for git operations (commit & push)")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
