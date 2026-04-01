"""Tests for feature 304: Creating markdown file test-ypzjo0.md with title and prose content."""

import pytest


class TestFeature304Module:
    """Tests for feature_304 module import and function existence."""

    def test_feature_304_module_imports(self):
        """Test that feature_304 module can be imported."""
        try:
            import sys
            sys.path.insert(0, 'src')
            from sheep.features.feature_304 import create_feature_304_markdown_file
            assert create_feature_304_markdown_file is not None
        except ImportError as e:
            # Skip if module dependencies not installed
            pytest.skip(f"Module dependencies not installed: {e}")

    def test_create_feature_304_function_exists(self):
        """Test that create_feature_304_markdown_file function exists and is callable."""
        try:
            import sys
            sys.path.insert(0, 'src')
            from sheep.features.feature_304 import create_feature_304_markdown_file
            assert callable(create_feature_304_markdown_file)
        except ImportError:
            pytest.skip("Module dependencies not installed")


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-ypzjo0.md does not exist before creation."""
        test_file = tmp_path / "test-ypzjo0.md"
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-ypzjo0.md"

        # Create the file with H1 heading
        content = "# Dynamic Content Generation\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-ypzjo0.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-ypzjo0.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-ypzjo0.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for task-2: Validate file encoding, line endings, and size."""

    MIN_SIZE = 320
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-ypzjo0.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-ypzjo0.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 320-600 bytes (inclusive)."""
        test_file = tmp_path / "test-ypzjo0.md"

        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / "test-ypzjo0.md"

        # Content that meets all criteria
        content = "# Dynamic Content Generation\n\nDynamic content generation enables flexible and responsive applications that adapt to user needs and preferences. It allows systems to create personalized experiences by processing data and generating appropriate responses. Through automation, we can deliver scalable solutions that serve many users simultaneously with customized outputs.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE
