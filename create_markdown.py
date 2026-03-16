"""
Create test-zo2ge0.md markdown file with title and prose content.

This script generates a markdown file with:
- Exactly one level-1 heading (#) as the title
- One blank line after the heading
- 2-3 sentences of meaningful prose content
- UTF-8 encoding (no BOM)
- LF line endings
- File size between 400-600 bytes
"""

from pathlib import Path


def create_markdown_file():
    """Create test-zo2ge0.md with proper structure and encoding."""

    filename = Path("test-zo2ge0.md")

    # Markdown content: heading + blank line + 2-3 sentences
    content = """# The Art of Thoughtful Design

The most impactful creations in technology and life emerge from careful consideration of both purpose and consequence. Great design balances elegance with functionality, ensuring that solutions serve their users meaningfully and intuitively. When we invest time in understanding the needs, context, and values of those we serve, we unlock the potential to create something truly worth sharing."""

    # Write to file with UTF-8 encoding (no BOM)
    # pathlib.write_text() automatically uses LF line endings on Unix systems
    filename.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    create_markdown_file()
    print("✓ Created test-zo2ge0.md")
