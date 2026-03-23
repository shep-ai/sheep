#!/usr/bin/env python
"""Script to generate markdown content for feature 184, task-1."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import generate_markdown_content


def main():
    """Generate markdown content and display it."""
    print("Generating markdown content for feature 184 (task-1)...")
    print("=" * 70)

    try:
        content = generate_markdown_content()

        print("\nGenerated Content:")
        print("-" * 70)
        print(content)
        print("-" * 70)

        # Validate and report
        lines = content.split("\n")
        content_bytes = len(content.encode('utf-8'))
        prose_lines = lines[2:]
        prose = "\n".join(prose_lines).strip()
        sentence_count = prose.count(".")

        print("\nValidation Report:")
        print(f"  Content length: {content_bytes} bytes (target: 300-600)")
        print(f"  H1 heading present: {lines[0].startswith('# ')}")
        print(f"  Blank line separator: {len(lines) > 1 and lines[1] == ''}")
        print(f"  Sentence count: {sentence_count} (target: 2-3)")
        print(f"  Content ends with newline: {content.endswith(chr(10))}")

        # Check if content is valid
        is_valid = (
            300 <= content_bytes <= 600 and
            lines[0].startswith("# ") and
            (len(lines) > 1 and lines[1] == "") and
            2 <= sentence_count <= 3 and
            content.endswith("\n")
        )

        print(f"\nOverall validity: {'✓ VALID' if is_valid else '✗ INVALID'}")

        return 0 if is_valid else 1

    except Exception as e:
        print(f"Error generating content: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
