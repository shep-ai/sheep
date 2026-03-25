"""Implementation for feature 205: Create markdown file test-m6zeml.md with title and prose content.

This module orchestrates the creation of a markdown file with hard-coded, deterministic content.
Unlike feature 204 which uses Claude API for dynamic generation, feature 205 uses hard-coded
content to demonstrate straightforward file creation within the Sheep workflow without external
API dependencies.

The file is created with:
- Exact filename: test-m6zeml.md
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

import subprocess
import sys
from pathlib import Path

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 205 constants
FILENAME = "test-m6zeml.md"
FEATURE_NUMBER = 205
BRANCH_NAME = "feat/205-markdown-file-creation-870df7"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME}"

# Hard-coded markdown content
# H1 title about the chosen topic
TITLE_TEXT = "The Importance of Code Documentation"

# 2-3 sentences of prose content related to the title
PROSE_CONTENT = (
    "Effective documentation is essential for code maintainability and team collaboration. "
    "Clear, concise documentation helps new team members onboard quickly and reduces cognitive "
    "load for future developers. Writing good documentation is an investment that pays dividends "
    "throughout a project's lifecycle."
)
