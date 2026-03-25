"""Implementation for feature 206: Create markdown file test-afcl8i.md with title and prose content.

This module orchestrates the creation of a markdown file with hard-coded, deterministic content.
Following the pattern from feature 205, this implementation uses hard-coded content to demonstrate
straightforward file creation within the Sheep workflow without external API dependencies.

The file is created with:
- Exact filename: test-afcl8i.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations

This approach provides:
- Deterministic output (identical on repeated execution)
- Transparent, auditable content (no API dependencies)
- Simplified error handling (no network failures)
- Faster execution (no API latency)
- Reliable testing and review (reproducible results)
"""

import re
import subprocess
import sys
from pathlib import Path

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 206 constants
FILENAME = "test-afcl8i.md"
FEATURE_NUMBER = 206
BRANCH_NAME = "feat/206-markdown-file-creation-f7d8d3"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME}"

# Hard-coded markdown content
# H1 title about the chosen topic
TITLE_TEXT = "The Art of Problem Solving Through Code"

# 2-3 sentences of prose content related to the title
PROSE_CONTENT = (
    "Software development is fundamentally about solving problems through logical thinking and creative solutions. "
    "The ability to break down complex challenges into manageable pieces and implement elegant solutions is a skill "
    "that distinguishes excellent programmers from adequate ones. Mastering this skill requires patience, practice, "
    "and a commitment to continuous learning."
)
