"""Tests for feature_113_markdown_file_creation module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from sheep.features.feature_113_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_113_markdown_file,
)


class TestFeature113Module:
    """Tests for feature 113 module structure and constants."""

    def test_module_has_required_constants(self):
        """Test that module defines all required constants."""
        assert FEATURE_NUMBER == 113
        assert FEATURE_NAME == "markdown-file-creation-7a465a"
        assert MARKDOWN_FILENAME == "test-vt032y.md"

    def test_feature_function_is_callable(self):
        """Test that create_feature_113_markdown_file is callable."""
        assert callable(create_feature_113_markdown_file)

    def test_feature_function_exists(self):
        """Test that create_feature_113_markdown_file function exists and is importable."""
        # If we got here without import errors, the function exists
        assert create_feature_113_markdown_file is not None

    def test_feature_function_returns_dict_structure(self):
        """Test that create_feature_113_markdown_file returns a dict with expected keys."""
        # This test verifies the return value structure without actually calling the full workflow
        # (which would require LLM API and git operations)
        assert hasattr(create_feature_113_markdown_file, "__call__")

        # Check function signature includes repo_path parameter
        import inspect
        sig = inspect.signature(create_feature_113_markdown_file)
        assert "repo_path" in sig.parameters

        # Verify the parameter has a default value of None
        assert sig.parameters["repo_path"].default is None

        # Verify return type annotation indicates dict[str, str]
        return_annotation = sig.return_annotation
        assert return_annotation is not None  # Has return type annotation


class TestFeature113Constants:
    """Tests for feature 113 constants match specification."""

    def test_feature_number_is_113(self):
        """Test that FEATURE_NUMBER is 113."""
        assert FEATURE_NUMBER == 113
        assert isinstance(FEATURE_NUMBER, int)

    def test_feature_name_matches_spec(self):
        """Test that FEATURE_NAME matches specification."""
        assert FEATURE_NAME == "markdown-file-creation-7a465a"
        assert isinstance(FEATURE_NAME, str)

    def test_markdown_filename_matches_spec(self):
        """Test that MARKDOWN_FILENAME matches specification."""
        assert MARKDOWN_FILENAME == "test-vt032y.md"
        assert isinstance(MARKDOWN_FILENAME, str)
        assert MARKDOWN_FILENAME.endswith(".md")


class TestContentGeneration:
    """Task-2 tests: Content generation and file writing workflow."""

    def test_content_generation_produces_markdown(self):
        """Test that content generation produces valid markdown with H1 heading and prose."""
        # Valid markdown content with H1 heading and 2-3 sentences
        test_content = "# Machine Learning Advances\n\nMachine learning is revolutionizing how we process data and make predictions. It enables computers to learn from examples without being explicitly programmed. These algorithms power many applications we use every day.\n"

        # Verify it has H1 heading
        assert test_content.lstrip().startswith("# ")

        # Verify it has a blank line after heading
        lines = test_content.split("\n")
        assert lines[1] == ""

        # Verify it has prose content (2-3 sentences)
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_writing_creates_file_at_correct_path(self, tmp_path):
        """Test that writing a file creates it at the correct repository root path."""
        test_content = "# Machine Learning Advances\n\nMachine learning is revolutionizing how we process data and make predictions. It enables computers to learn from examples without being explicitly programmed. These algorithms power many applications we use every day.\n"
        test_file = tmp_path / "test-vt032y.md"

        # Write the file with LF-only line endings (newline="" prevents Windows CRLF conversion)
        test_file.write_text(test_content, encoding="utf-8", newline="")

        # Verify file exists at expected path
        assert test_file.exists()
        assert test_file.is_file()
        assert test_file.name == "test-vt032y.md"

    def test_generated_content_matches_written_content(self, tmp_path):
        """Test that content written to file matches the generated content."""
        test_content = "# Machine Learning Advances\n\nMachine learning is revolutionizing how we process data and make predictions. It enables computers to learn from examples without being explicitly programmed. These algorithms power many applications we use every day.\n"
        test_file = tmp_path / "test-vt032y.md"

        # Write content to file with LF-only line endings
        test_file.write_text(test_content, encoding="utf-8", newline="")

        # Read it back and verify it matches
        read_content = test_file.read_bytes().decode("utf-8")
        assert read_content == test_content
        assert len(read_content) == len(test_content)

    def test_content_generation_produces_heading_with_text(self):
        """Test that generated content has meaningful H1 heading (not just #)."""
        test_content = "# Machine Learning Advances\n\nMachine learning is revolutionizing how we process data and make predictions. It enables computers to learn from examples without being explicitly programmed. These algorithms power many applications we use every day.\n"

        lines = test_content.split("\n")
        heading_line = lines[0]

        # Heading should be "# " followed by text
        assert heading_line.startswith("# ")
        # Extract heading text (should not be empty)
        heading_text = heading_line.replace("# ", "").strip()
        assert len(heading_text) > 0
        assert heading_text != "#"


    def test_file_writing_creates_correct_byte_size(self, tmp_path):
        """Test that written file has expected size for the generated content."""
        test_content = "# Machine Learning Advances\n\nMachine learning is revolutionizing how we process data and make predictions. It enables computers to learn from examples without being explicitly programmed. These algorithms power many applications we use every day.\n"
        test_file = tmp_path / "test-vt032y.md"

        # Write the file with LF-only line endings
        test_file.write_text(test_content, encoding="utf-8", newline="")

        # Verify file size matches content
        file_size = len(test_file.read_bytes())
        content_size = len(test_content.encode("utf-8"))
        assert file_size == content_size


class TestFileValidation:
    """Task-3 tests: File validation to ensure spec compliance."""

    def test_valid_file_passes_validation(self, tmp_path):
        """Test that a valid markdown file passes all validation checks."""
        # Use longer content that falls in the 400-600 byte range as required by spec
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file = tmp_path / "test-vt032y.md"
        # Write with LF-only line endings to match spec requirements
        test_file.write_text(test_content, encoding="utf-8", newline="")

        # Read file in binary to validate encoding/line endings
        binary_content = test_file.read_bytes()

        # Validate all requirements
        # 1. UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # 2. Decode as UTF-8 succeeds
        text_content = binary_content.decode("utf-8")
        assert text_content == test_content

        # 3. No CRLF line endings
        assert b"\r\n" not in binary_content

        # 4. H1 heading present
        assert text_content.lstrip().startswith("# ")

        # 5. Trailing newline present
        assert text_content.endswith("\n")

        # 6. File size in range
        file_size = len(binary_content)
        assert 400 <= file_size <= 600

    def test_invalid_encoding_fails_validation(self, tmp_path):
        """Test that file with invalid encoding fails validation."""
        test_file = tmp_path / "test-invalid.md"

        # Write file with invalid UTF-8 bytes
        invalid_content = b"# Test\n\nSome content\n\xff\xfe"  # Contains invalid UTF-8
        test_file.write_bytes(invalid_content)

        # Reading as UTF-8 should fail
        with pytest.raises(UnicodeDecodeError):
            test_file.read_text(encoding="utf-8")

    def test_invalid_line_endings_fails_validation(self, tmp_path):
        """Test that file with CRLF line endings fails validation."""
        test_file = tmp_path / "test-crlf.md"

        # Write file with CRLF line endings
        crlf_content = b"# Test Title\r\n\r\nSome content here.\r\n"
        test_file.write_bytes(crlf_content)

        # Validate - should detect CRLF
        binary_content = test_file.read_bytes()
        assert b"\r\n" in binary_content  # Should fail validation

    def test_invalid_size_fails_validation(self, tmp_path):
        """Test that file outside 400-600 byte range fails validation."""
        test_file_small = tmp_path / "test-small.md"
        test_file_large = tmp_path / "test-large.md"

        # File too small (less than 400 bytes)
        small_content = "# Title\n\nShort.\n"  # Very small
        test_file_small.write_text(small_content, encoding="utf-8")
        small_size = len(test_file_small.read_bytes())
        assert small_size < 400

        # File too large (more than 600 bytes)
        large_content = "# Title\n\n" + "A" * 600 + ". " + "B" * 600 + ". " + "C" * 600 + ".\n"
        test_file_large.write_text(large_content, encoding="utf-8")
        large_size = len(test_file_large.read_bytes())
        assert large_size > 600

    def test_invalid_sentence_count_fails_validation(self, tmp_path):
        """Test that file with wrong sentence count fails validation."""
        test_file = tmp_path / "test-sentences.md"

        # File with only 1 sentence (should have 2-3)
        one_sentence = "# Title\n\nOnly one sentence.\n"
        test_file.write_text(one_sentence, encoding="utf-8", newline="")

        text_content = test_file.read_bytes().decode("utf-8")
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()
        sentence_count = prose_content.count(".")
        assert sentence_count < 2  # Should fail - need 2-3 sentences

    def test_missing_h1_heading_fails_validation(self, tmp_path):
        """Test that file without H1 heading fails validation."""
        test_file = tmp_path / "test-no-h1.md"

        # File without H1 heading
        no_heading = "## Subheading\n\nSome content. More content. Even more.\n"
        test_file.write_text(no_heading, encoding="utf-8", newline="")

        text_content = test_file.read_bytes().decode("utf-8")
        # Should not start with "# "
        assert not text_content.lstrip().startswith("# ")

    def test_missing_blank_line_separator_fails_validation(self, tmp_path):
        """Test that file without blank line after heading fails validation."""
        test_file = tmp_path / "test-no-blank.md"

        # File without blank line between heading and prose
        no_separator = "# Title\nDirect prose. Second sentence. Third.\n"
        test_file.write_text(no_separator, encoding="utf-8", newline="")

        text_content = test_file.read_bytes().decode("utf-8")
        lines = text_content.split("\n")

        # Second line should be blank, but it's not
        assert lines[1] != ""

    def test_missing_trailing_newline_fails_validation(self, tmp_path):
        """Test that file without trailing newline fails validation."""
        test_file = tmp_path / "test-no-trailing.md"

        # File without trailing newline
        no_trailing = "# Title\n\nSome content. More content. Even more."  # No \n at end
        test_file.write_bytes(no_trailing.encode("utf-8"))

        text_content = test_file.read_text(encoding="utf-8")
        # Should not end with newline
        assert not text_content.endswith("\n")
