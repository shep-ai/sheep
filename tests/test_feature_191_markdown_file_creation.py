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


class TestFeature191FileCreation:
    """Tests for task 2: Implement markdown file creation with UTF-8 and Unix LF."""

    def setup_method(self):
        """Clean up any existing test file before each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def teardown_method(self):
        """Clean up test file after each test."""
        from sheep.features.feature_191_markdown_file_creation import FILENAME

        test_file = Path(FILENAME)
        if test_file.exists():
            test_file.unlink()

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file() creates the file at correct path."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        result = create_markdown_file()

        assert Path(FILENAME).exists(), f"File {FILENAME} should exist after creation"
        assert result == str(Path(FILENAME).absolute())

    def test_create_markdown_file_content_structure(self):
        """Test that file contains H1 heading, blank line, and prose."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            TITLE,
            PROSE,
            create_markdown_file,
        )

        create_markdown_file()
        content = Path(FILENAME).read_text(encoding="utf-8")

        expected_content = f"# {TITLE}\n\n{PROSE}\n"
        assert content == expected_content

    def test_create_markdown_file_utf8_encoding(self):
        """Test that file is encoded as UTF-8 without BOM."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        create_markdown_file()
        binary_content = Path(FILENAME).read_bytes()

        # Check for UTF-8 BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

        # Verify UTF-8 decoding works
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File must be valid UTF-8")

    def test_create_markdown_file_unix_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        create_markdown_file()
        binary_content = Path(FILENAME).read_bytes()

        # Check that there are no CRLF sequences
        assert b"\r\n" not in binary_content, "File must use Unix LF line endings (no CRLF)"

        # Verify file ends with LF, not CR
        assert binary_content.endswith(b"\n"), "File must end with LF"
        assert not binary_content.endswith(b"\r\n"), "File must not end with CRLF"

    def test_create_markdown_file_raises_if_exists(self):
        """Test that create_markdown_file() raises error if file already exists."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        # Create file once
        create_markdown_file()

        # Attempting to create again should raise error
        with pytest.raises(FileExistsError):
            create_markdown_file()

    def test_create_markdown_file_file_size_in_range(self):
        """Test that created file is in the expected size range (450-550 bytes)."""
        from sheep.features.feature_191_markdown_file_creation import (
            FILENAME,
            create_markdown_file,
        )

        create_markdown_file()
        file_size = Path(FILENAME).stat().st_size

        assert 450 <= file_size <= 550, f"File size should be 450-550 bytes, got {file_size}"
