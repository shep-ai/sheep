#!/usr/bin/env python3
"""Create test-z5u8bz.md markdown file with proper structure and encoding."""

from pathlib import Path

# Prose content: markdown heading (# Title) + blank line + 3 sentences of coherent prose
prose_content = "# The Power of Patience and Persistence\n\nSuccess rarely comes from a single brilliant moment but rather from consistent effort applied over time toward meaningful goals. Every expert started as a beginner, learning incrementally through repetition, reflection, and refinement of technique. By embracing patience and trusting the process, we give ourselves the opportunity to develop mastery and achieve things we thought impossible.\n"

# Create file at repository root with proper encoding and line endings
# encoding="utf-8": UTF-8 text encoding (not utf-8-sig to avoid BOM)
# newline="\n": Force Unix-style LF line endings (not platform-dependent CRLF)
file_path = Path("test-z5u8bz.md")
file_path.write_text(prose_content, encoding="utf-8", newline="\n")

print(f"Created {file_path}")
print(f"File size: {file_path.stat().st_size} bytes")
