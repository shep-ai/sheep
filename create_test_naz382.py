#!/usr/bin/env python3
"""Create test-naz382.md markdown file following the established pattern."""

from pathlib import Path


def create_markdown_file():
    """Create test-naz382.md with prose content using pathlib."""

    filename = "test-naz382.md"

    # Define markdown content: H1 heading + blank line + 2-3 sentences of prose
    # Topic: Adaptability in Modern Technology
    prose_content = """# Adaptability in Modern Technology

Cloud computing has fundamentally transformed how organizations deploy and manage their infrastructure. The ability to scale resources dynamically in response to demand enables businesses to optimize costs while maintaining reliability. This flexibility demonstrates the power of designing systems that anticipate change rather than resist it."""

    # Create file using pathlib with explicit UTF-8 encoding and LF line endings
    # The newline='\n' parameter ensures LF line endings across all platforms
    Path(filename).write_text(prose_content, encoding='utf-8', newline='\n')

    print(f"✓ Created {filename}")
    print(f"  Encoding: UTF-8 (no BOM)")
    print(f"  Line endings: Unix-style LF (\\n)")
    print(f"  Content length: {len(prose_content)} characters")


if __name__ == '__main__':
    create_markdown_file()
