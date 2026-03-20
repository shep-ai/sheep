"""Feature 123: Create markdown file test-b3x0s1.md with title and 2-3 sentences of content.

This module implements the workflow to create a single markdown file following
the established pattern from 122+ prior markdown-file-creation features.

Phase 1 Implementation:
- Module foundation: Constants, imports, and module structure
Phase 2 Implementation:
- Task 2: Generate markdown content (H1 heading + 2-3 sentences)
- Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings
"""

from pathlib import Path

from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
    validate_markdown_file,
    commit_markdown_file,
    push_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Configuration for feature 123
FEATURE_NUMBER = 123
FILENAME = "test-b3x0s1.md"
