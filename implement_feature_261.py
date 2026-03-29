#!/usr/bin/env python3
"""
Implementation for feature 261: Create markdown file test-m6or7y.md
with H1 title, blank line, and 2-3 sentences of prose content.
"""

from pathlib import Path

# Define content components
TITLE = "Metamorphosis in Nature"

PROSE = (
    "Throughout the natural world, transformation is a fundamental process that shapes the evolution and adaptation of "
    "living organisms. Metamorphosis—from butterflies breaking free from cocoons to tadpoles developing into frogs—represents "
    "one of nature's most remarkable demonstrations of change and growth. These profound transformations remind us that change "
    "is not merely inevitable, but often necessary for survival and flourishing."
)

# Create content using f-string template: # TITLE\n\n PROSE\n
content = f"# {TITLE}\n\n{PROSE}\n"

# Create file in repository root using pathlib with explicit encoding and line endings
file_path = Path("test-m6or7y.md")
file_path.write_text(content, encoding="utf-8", newline="\n")

print(f"[OK] Created file: {file_path}")
print(f"[OK] File size: {file_path.stat().st_size} bytes")
print(f"[OK] Encoding: UTF-8 without BOM")
print(f"[OK] Line endings: Unix LF")
