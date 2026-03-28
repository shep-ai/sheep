#!/usr/bin/env python3
"""
Create markdown file test-5dl5yi.md for feature 145 (demonstration version).

Demonstrates the markdown file creation workflow using mocked LLM content
to avoid requiring API keys. In production, this uses the real Claude API.

The workflow:
1. Generate markdown content (mocked here)
2. Write file to disk with UTF-8 encoding
3. Validate file structure and encoding
4. Stage and commit with conventional message
5. Push to remote origin
"""

import sys
from pathlib import Path

# Add src to path so we can import sheep modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import (
    commit_markdown_file,
    push_markdown_file,
    validate_markdown_file,
    write_markdown_file,
)


def main():
    """Create test-5dl5yi.md markdown file with demonstrative content."""
    filename = "test-5dl5yi.md"

    # Content generated from Claude API (using example content for demonstration)
    content = """# Quantum Computing

Quantum computers exploit quantum mechanical phenomena like superposition and entanglement to process information. They have the potential to solve certain computational problems exponentially faster than classical computers. This technology could revolutionize cryptography, drug discovery, and optimization problems.
"""

    try:
        print("Phase 1: Creating markdown file (test-5dl5yi.md)")
        print("=" * 60)

        # Step 1: Write the file
        print("\nStep 1: Writing file with UTF-8 encoding...")
        filepath = write_markdown_file(content, filename)
        print(f"✓ File created at: {filepath}")

        # Step 2: Validate the file
        print("\nStep 2: Validating file structure and encoding...")
        validate_markdown_file(filepath)
        print("✓ File validation passed")

        # Step 3: Commit the file
        print("\nStep 3: Staging and committing...")
        commit_result = commit_markdown_file(
            filepath,
            content,
            custom_message="feat(145): create markdown file test-5dl5yi.md with prose content"
        )
        print("✓ Commit successful")

        # Step 4: Push to remote
        print("\nStep 4: Pushing to remote...")
        push_result = push_markdown_file()
        print("✓ Pushed to origin")

        print("\n" + "=" * 60)
        print("✓ Phase 1 Complete - test-5dl5yi.md created successfully!")
        print(f"  File: {filename}")
        print(f"  Size: {Path(filepath).stat().st_size} bytes")
        print("  Commit: feat(145): create markdown file test-5dl5yi.md with prose content")

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
