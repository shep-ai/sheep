#!/usr/bin/env python
"""Verify all success criteria from the feature specification."""

import sys
from pathlib import Path
import subprocess

filepath = Path("test-5iigac.md")

print("=" * 70)
print("VERIFYING FEATURE 166 SUCCESS CRITERIA")
print("=" * 70)

checks = []

# Check 1: File exists
exists = filepath.exists()
checks.append(("✓" if exists else "✗", f"File exists: {filepath}"))

if not exists:
    print("\n".join(f"{check[0]} {check[1]}" for check in checks))
    sys.exit(1)

# Check 2: File size
size = filepath.stat().st_size
size_check = 300 <= size <= 600
checks.append(("✓" if size_check else "⚠", f"File size: {size} bytes (guideline 300-600)"))

# Check 3: Read content
content = filepath.read_text(encoding="utf-8")
lines = content.split("\n")

# Check 4: H1 heading on first line
h1_check = lines[0].startswith("# ")
checks.append(("✓" if h1_check else "✗", f"First line is H1 heading: {lines[0][:40]}"))

# Check 5: Blank line separator
blank_line_check = len(lines) > 1 and lines[1] == ""
checks.append(("✓" if blank_line_check else "✗", f"Second line is blank separator"))

# Check 6: Prose content (2-3 sentences)
prose_lines = lines[2:]
while prose_lines and prose_lines[-1] == "":
    prose_lines.pop()
prose_content = "\n".join(prose_lines).strip()
sentence_count = prose_content.count(".")
prose_check = 2 <= sentence_count <= 3
checks.append(("✓" if prose_check else "✗", f"Prose has 2-3 sentences: {sentence_count} found"))

# Check 7: UTF-8 encoding without BOM
binary = filepath.read_bytes()
bom_check = not binary.startswith(b"\xef\xbb\xbf")
checks.append(("✓" if bom_check else "✗", f"UTF-8 encoding without BOM"))

# Check 8: LF line endings (not CRLF)
lf_check = b"\r\n" not in binary and b"\n" in binary
checks.append(("✓" if lf_check else "✗", f"Uses Unix LF line endings (not CRLF)"))

# Check 9: Trailing newline
trailing_check = content.endswith("\n")
checks.append(("✓" if trailing_check else "✗", f"Ends with trailing newline"))

# Check 10: Git status
git_status = subprocess.run(
    ["git", "log", "--oneline", "-n", "1"],
    capture_output=True,
    text=True
).stdout.strip()
checks.append(("✓", f"Latest commit: {git_status[:60]}"))

# Check 11: Commit message
commit_msg = subprocess.run(
    ["git", "log", "-1", "--format=%B"],
    capture_output=True,
    text=True
).stdout.strip()
msg_check = "feat(166): Create markdown file test-5iigac.md with prose content" in commit_msg
checks.append(("✓" if msg_check else "✗", f"Commit message correct: {msg_check}"))

# Print results
print()
for check in checks:
    print(f"{check[0]} {check[1]}")

# Summary
print()
print("=" * 70)
all_passed = all(c[0] == "✓" for c in checks)
if all_passed or all(c[0] in ("✓", "⚠") for c in checks):
    print("✓ ALL SUCCESS CRITERIA VERIFIED")
    sys.exit(0)
else:
    print("✗ SOME CRITERIA FAILED")
    sys.exit(1)
