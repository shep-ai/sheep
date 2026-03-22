"""
Implementation for Feature 160: Create markdown file test-9ehmdc.md with prose content

Uses pathlib.Path.write_text() with UTF-8 encoding following the established pattern
from 170+ existing test files in the repository.
"""

from pathlib import Path


def create_markdown_file() -> Path:
    """
    Create test-9ehmdc.md at repository root with H1 heading and 2-3 sentences of prose.

    File structure:
    - Line 1: H1 markdown heading (# Title)
    - Line 2: Blank line
    - Line 3: 2-3 sentences of coherent prose
    - Encoding: UTF-8 without BOM
    - Line endings: LF (Unix-style)
    """
    # Compose the file content following the established pattern
    heading = "# The Importance of Resilience"
    prose = (
        "Resilience is the ability to bounce back from adversity and maintain composure "
        "in the face of challenges, which has become increasingly important in our fast-paced "
        "world. By developing resilience, individuals can navigate obstacles with greater ease "
        "and emerge stronger from difficult experiences. This quality not only contributes to "
        "personal well-being but also enables people to achieve their goals despite setbacks."
    )

    # Build complete content: heading + blank line + prose
    content = f"{heading}\n\n{prose}\n"

    # Create the file using pathlib.Path.write_text() with explicit UTF-8 encoding
    # This ensures UTF-8 encoding without BOM and proper line endings on Unix systems
    file_path = Path("test-9ehmdc.md")
    file_path.write_text(content, encoding="utf-8")

    return file_path


if __name__ == "__main__":
    create_markdown_file()
    print("✓ Created test-9ehmdc.md")
