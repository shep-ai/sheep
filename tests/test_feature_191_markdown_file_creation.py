"""Tests for feature 191: Creating markdown file test-u1rtbw.md with title and prose content."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest


class TestFeature191Constants:
    """Tests for task 1: Define file content constants."""

    def test_filename_constant(self):
        """Test that FILENAME constant is correct."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        assert FILENAME == "test-u1rtbw.md"

    def test_title_constant_is_non_empty_string(self):
        """Test that TITLE is a non-empty string."""
        from sheep.features.feature_191_markdown_file_creation import TITLE

        assert isinstance(TITLE, str)
        assert len(TITLE) > 0

    def test_prose_constant_contains_2_to_3_sentences(self):
        """Test that PROSE contains exactly 2-3 sentences."""
        from sheep.features.feature_191_markdown_file_creation import PROSE

        # Count sentences by periods
        sentence_count = PROSE.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    def test_prose_is_substantive_not_placeholder(self):
        """Test that PROSE is meaningful content, not placeholder."""
        from sheep.features.feature_191_markdown_file_creation import PROSE

        # Check that content is substantive (contains real words, not lorem ipsum)
        assert len(PROSE) > 100, "Prose should be substantive (>100 chars)"
        assert "lorem" not in PROSE.lower(), "Should not contain lorem ipsum"

    def test_constants_exist_and_are_importable(self):
        """Test that all required constants can be imported."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            PROSE,
            TITLE,
        )

        assert FILENAME is not None
        assert TITLE is not None
        assert PROSE is not None

    def test_file_content_structure_size(self):
        """Test that constants produce content in expected size range."""
        from sheep.features.feature_191_markdown_file_creation import PROSE, TITLE

        # Simulate the content that will be written to file
        content = f"# {TITLE}\n\n{PROSE}\n"
        content_size = len(content.encode("utf-8"))

        # Feature 191 spec requires 450-550 bytes
        assert 450 <= content_size <= 550, f"Content should be 450-550 bytes, got {content_size}"
