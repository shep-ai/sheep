"""Implementation for feature 191: Create markdown file test-u1rtbw.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from prior features. The file is created with:
- Exact filename: test-u1rtbw.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 450-550 bytes
- Git staging, commit, and push operations
"""

import subprocess
import sys
from pathlib import Path

# Task 1: Define file content constants
FILENAME = "test-u1rtbw.md"
TITLE = "The Value of Clear Code Documentation"
PROSE = "Clear documentation is essential for building maintainable software systems that teams can understand and modify across different time periods and expertise levels. Well-documented code reduces cognitive load for developers and accelerates onboarding of new team members. By investing time in clear documentation, comments, and examples, developers create a foundation for long-term success and help teams deliver higher quality software."
