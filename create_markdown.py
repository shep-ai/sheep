#!/usr/bin/env python3
"""Create test-oyjp7x.md markdown file with H1 heading and prose content."""

from pathlib import Path

# Define the content: H1 heading + blank line + 2-3 sentences of prose
heading = "# The Harmony of Code and Creativity"

prose = """Code and creativity are more intertwined than many realize, with programming serving as both a logical discipline and an artistic expression. When developers craft elegant solutions, they balance the structure of language with the freedom to innovate and solve problems in unexpected ways. This symbiosis between technical precision and creative thinking is what transforms ordinary code into something truly remarkable."""

# Combine heading and prose with proper formatting
content = f"{heading}\n\n{prose}\n"

# Write to file with explicit UTF-8 encoding (no BOM) and LF line endings
# Use open() with newline='' to prevent CRLF conversion on Windows
with open("test-oyjp7x.md", 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("File test-oyjp7x.md created successfully")
print(f"Content length: {len(content)} characters")
print(f"File size: {len(content.encode('utf-8'))} bytes")
