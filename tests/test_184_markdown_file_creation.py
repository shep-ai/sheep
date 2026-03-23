"""Tests for feature 184: Create markdown file test-396h0d.md with title and prose content."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
    validate_markdown_file,
    validate_file_properties,
)

# Test content that meets all requirements for feature 184
# This represents the markdown content to be generated and written to test-396h0d.md
TEST_CONTENT = """# Artificial Intelligence and Machine Learning

Artificial intelligence and machine learning technologies are fundamentally transforming how we live and work, enabling computers to learn from data and make intelligent decisions. These powerful tools are already being applied across industries, from healthcare diagnostics to autonomous vehicles, improving efficiency and creating new possibilities. As AI continues to advance, it promises to unlock solutions to some of humanity's greatest challenges while requiring thoughtful consideration of ethical implications.
"""


class TestGenerateMarkdownContentForFeature184:
    """Tests for task-1: Generate markdown content via LLM for feature 184."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_returns_non_empty_string(self, mock_get_llm):
        """Test that generate_markdown_content() returns a non-empty string."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Artificial Intelligence\n\nArtificial intelligence is transforming how we live and work. Machine learning algorithms can now recognize patterns in vast amounts of data. This technology promises to solve many of humanity's greatest challenges."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert isinstance(content, str), "Content should be a string"
        assert len(content) > 0, "Content should not be empty"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_contains_h1_heading(self, mock_get_llm):
        """Test that generated content contains exactly one H1 heading (line starts with '#')."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# The Power of Meaningful Work\n\nWork provides more than just income; it gives us purpose and identity. Meaningful careers allow us to contribute to society and achieve personal fulfillment. When work aligns with our values, life becomes richer and more satisfying."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert content.startswith("# "), "Content should start with H1 heading (# )"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_contains_exactly_2_to_3_sentences(self, mock_get_llm):
        """Test that generated content contains exactly 2-3 sentences (verified by period count)."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Mountain Ecosystems\n\nMountain ecosystems are among the most biodiverse regions on Earth. They provide crucial water resources and harbor unique species found nowhere else. These fragile environments require careful conservation and protection."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        # Extract prose (skip heading and blank line)
        prose_lines = lines[2:]
        prose = "\n".join(prose_lines).strip()

        # Count sentences by periods
        sentence_count = prose.count(".")
        assert (
            2 <= sentence_count <= 3
        ), f"Content should have exactly 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_content_length_in_range(self, mock_get_llm):
        """Test that generated content is between 300-600 bytes."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Digital Transformation\n\nDigital transformation is fundamentally reshaping industries and business models across the global marketplace. Organizations are increasingly adopting cloud technologies, artificial intelligence, and advanced data analytics to remain competitive. This profound shift requires developing new skills, fostering a culture of continuous learning and innovation, and reimagining organizational structures and processes."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        content_bytes = len(content.encode('utf-8'))

        assert (
            300 <= content_bytes <= 600
        ), f"Content should be 300-600 bytes, got {content_bytes} bytes"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_content_is_coherent(self, mock_get_llm):
        """Test that generated content is semantically coherent and grammatically correct."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Sustainable Agriculture\n\nSustainable agriculture practices balance productivity with environmental stewardship. Farmers using organic methods, crop rotation, and natural pest control create healthier ecosystems. These approaches demonstrate that feeding the world and protecting nature are complementary goals."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()

        # Verify content has sentences (ends with periods)
        assert "." in content, "Content should contain complete sentences"

        # Verify content is not obviously corrupted (has reasonable characters)
        assert content.count("\n") >= 1, "Content should have line breaks"

        # Verify no repeated suspicious patterns
        lines = content.split("\n")
        assert len(lines) >= 3, "Content should have at least 3 lines (heading, blank, prose)"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_with_blank_line_separator(self, mock_get_llm):
        """Test that generated content has proper markdown structure with blank line separator."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Climate Science\n\nClimate science uses data from satellites, weather stations, and ice cores. Scientists have documented rapid changes in global temperature and atmospheric composition. This evidence guides international efforts to mitigate climate change impacts."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")

        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank separator"
        assert len(lines) > 2, "Should have content after blank line"


class TestWriteMarkdownFileForFeature184:
    """Tests for task-2: Write markdown file to disk for feature 184."""

    def test_write_markdown_file_exists(self, tmp_path):
        """Test that write_markdown_file() creates file test-396h0d.md."""
        # Change to temp directory for this test
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            filepath = write_markdown_file(content, "test-396h0d.md")

            # Verify file was created
            assert Path(filepath).exists(), f"File should exist at {filepath}"
            assert Path(filepath).is_file(), f"Path should be a file: {filepath}"
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_has_correct_content(self, tmp_path):
        """Test that file contains exact content written to it."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            content = "# Sample Markdown\n\nThis is sample content. It has sentences. Multiple ones.\n"
            filepath = write_markdown_file(content, "test-396h0d.md")

            # Read file and verify content matches
            with open(filepath, "r", encoding="utf-8") as f:
                read_content = f.read()

            assert read_content == content, "File content should match written content exactly"
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_in_repo_root(self, tmp_path):
        """Test that file is created in repository root, not subdirectory."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            content = "# Root Test\n\nThis file is at root. Not in subdirectory. That matters.\n"
            filepath = write_markdown_file(content, "test-396h0d.md")

            # Verify file is directly in repo root (tmp_path), not in any subdirectory
            file_path = Path(filepath)
            assert file_path.parent == tmp_path, f"File should be in repo root ({tmp_path}), not {file_path.parent}"
        finally:
            os.chdir(original_cwd)

    def test_write_markdown_file_rejects_path_traversal(self, tmp_path):
        """Test that write_markdown_file rejects filenames with path separators."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            content = "# Test\n\nTest content. More content. Even more.\n"

            # Should raise ValueError for path traversal attempts
            with pytest.raises(ValueError):
                write_markdown_file(content, "../test-396h0d.md")

            with pytest.raises(ValueError):
                write_markdown_file(content, "subdir/test-396h0d.md")
        finally:
            os.chdir(original_cwd)


class TestValidateMarkdownStructureForFeature184:
    """Tests for task-3: Validate markdown structure for feature 184."""

    def test_validate_h1_heading_on_first_line(self, tmp_path):
        """Test that file line 1 contains H1 heading (starts with '# ')."""
        content = "# Valid Heading\n\nFirst sentence here. Second sentence here. Third one.\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_bytes(content.encode("utf-8"))

        # Should not raise exception
        assert validate_markdown_file(str(filepath)) is True

    def test_validate_blank_line_separator(self, tmp_path):
        """Test that file line 2 is blank (separator after heading)."""
        content = "# Title\n\nContent sentence one. Sentence two. Sentence three.\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_bytes(content.encode("utf-8"))

        assert validate_markdown_file(str(filepath)) is True

    def test_validate_fails_without_blank_line(self, tmp_path):
        """Test that validation fails if blank line is missing."""
        content = "# Title\nContent without blank line. This should fail. Not valid format.\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError, match="blank"):
            validate_markdown_file(str(filepath))

    def test_validate_prose_content(self, tmp_path):
        """Test that prose content exists and is properly formatted."""
        content = "# Topic\n\nFirst meaningful sentence. Second meaningful sentence. Third one.\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_bytes(content.encode("utf-8"))

        assert validate_markdown_file(str(filepath)) is True

    def test_validate_fails_without_prose(self, tmp_path):
        """Test that validation fails if no prose content after heading."""
        content = "# Title\n\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError, match="prose"):
            validate_markdown_file(str(filepath))

    def test_validate_fails_with_wrong_sentence_count(self, tmp_path):
        """Test that validation fails if sentence count is not 2-3."""
        # One sentence - should fail
        content = "# Title\n\nOnly one sentence.\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_markdown_file(str(filepath))


class TestValidateFileEncodingForFeature184:
    """Tests for task-4: Validate file encoding and properties for feature 184."""

    def test_validate_utf8_encoding(self, tmp_path):
        """Test that file is valid UTF-8."""
        content = "# UTF-8 Test\n\nThis file is UTF-8 encoded. No BOM present. All valid.\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_bytes(content.encode("utf-8"))

        # Should not raise exception
        assert validate_file_properties(str(filepath)) is True

    def test_validate_fails_with_utf8_bom(self, tmp_path):
        """Test that validation fails if UTF-8 BOM is present."""
        content = "# Title\n\nContent here. More content. Even more.\n"
        filepath = tmp_path / "test-396h0d.md"

        # Write with UTF-8 BOM
        with open(filepath, "wb") as f:
            f.write(b"\xef\xbb\xbf")  # UTF-8 BOM
            f.write(content.encode("utf-8"))

        with pytest.raises(ValueError, match="BOM"):
            validate_file_properties(str(filepath))

    def test_validate_fails_with_crlf_line_endings(self, tmp_path):
        """Test that validation fails if file uses CRLF instead of LF."""
        content = "# Title\r\n\r\nContent sentence. Another one. Third sentence.\r\n"
        filepath = tmp_path / "test-396h0d.md"

        # Write with CRLF line endings
        with open(filepath, "wb") as f:
            f.write(content.encode("utf-8"))

        with pytest.raises(ValueError, match="CRLF"):
            validate_file_properties(str(filepath))

    def test_validate_file_size_in_range(self, tmp_path):
        """Test that file size is between 300-600 bytes."""
        # A realistic markdown file in the expected size range (longer content)
        content = "# Advancements in Renewable Energy Technology\n\nRenewable energy sources such as solar, wind, and hydroelectric power have become increasingly important in our global efforts to combat climate change and reduce dependence on fossil fuels. These technologies continue to improve in efficiency and affordability, making them accessible to more communities around the world. The transition to renewable energy represents one of the most critical challenges and opportunities of our time, requiring investment, innovation, and commitment from governments, businesses, and individuals alike.\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_bytes(content.encode("utf-8"))

        file_size = filepath.stat().st_size
        assert 300 <= file_size <= 600, f"File size {file_size} should be 300-600 bytes"

        # Should not raise exception
        assert validate_file_properties(str(filepath)) is True

    def test_validate_fails_if_too_small(self, tmp_path):
        """Test that validation fails if file is too small (< 300 bytes)."""
        content = "# X\n\nSmall. Tiny.\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_text(content, encoding="utf-8")

        # File is too small
        with pytest.raises(ValueError):
            validate_file_properties(str(filepath))

    def test_validate_fails_if_too_large(self, tmp_path):
        """Test that validation fails if file is too large (> 600 bytes)."""
        # Create content that's definitely > 600 bytes
        content = "# Very Long Title\n\n" + "This is a very long sentence that goes on and on. " * 20 + "\n"
        filepath = tmp_path / "test-396h0d.md"
        filepath.write_text(content, encoding="utf-8")

        # File is too large
        with pytest.raises(ValueError):
            validate_file_properties(str(filepath))

    def test_validate_with_lf_line_endings(self, tmp_path):
        """Test that validation passes with LF line endings."""
        content = "# Title\n\nFirst sentence with LF. Second sentence. Third.\n"
        filepath = tmp_path / "test-396h0d.md"

        # Write with explicit LF line endings
        with open(filepath, "wb") as f:
            f.write(content.encode("utf-8"))

        # Should pass - LF line endings are correct
        assert validate_file_properties(str(filepath)) is True


class TestCreateMarkdownFileIntegration:
    """Integration tests for feature 184: Create test-396h0d.md with prose content."""

    def test_file_does_not_exist_before_creation(self):
        """Test that file test-396h0d.md does not exist before creation."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"
        # Clean up if it exists from a previous run
        if test_file.exists():
            test_file.unlink()
        assert not test_file.exists()

    def test_creates_file_with_content_generators(self):
        """Test that file is created with write_markdown_file() from TEST_CONTENT."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        # Clean up before test
        if test_file.exists():
            test_file.unlink()

        # Write file using content_generators with TEST_CONTENT
        file_path = write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        assert test_file.exists(), "File test-396h0d.md should exist"
        assert file_path == str(test_file), "Returned path should match file path"
        assert test_file.read_bytes() == TEST_CONTENT.encode("utf-8"), "File content should match TEST_CONTENT exactly"

    def test_file_contains_valid_h1_heading(self):
        """Test that file contains exactly one H1 heading (starts with '# ')."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        # Ensure file exists
        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# "), "First line should be H1 heading"

    def test_file_contains_valid_sentence_count(self):
        """Test that file contains exactly 2-3 sentences (ending with periods)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        # Ensure file exists
        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = [line for line in lines[2:] if line.strip()]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, found {sentence_count}"

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after H1 heading."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank separator"

    def test_file_not_utf8_bom(self):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

    def test_file_has_lf_line_endings(self):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File should not have CRLF line endings"
        # Assert file contains LF sequences
        assert b"\n" in binary_content, "File should have LF line endings"

    def test_file_size_within_range(self):
        """Test that file size is between 300-600 bytes (inclusive)."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        file_size = len(test_file.read_bytes())
        assert 300 <= file_size <= 600, f"File size {file_size} should be 300-600 bytes"

    def test_file_passes_validate_markdown_file(self):
        """Test that file passes comprehensive validation."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        # Should not raise any exception
        result = validate_markdown_file(str(test_file))
        assert result is True, "File validation should pass"

    def test_file_passes_validate_file_properties(self):
        """Test that file passes encoding and properties validation."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        # Should not raise any exception
        result = validate_file_properties(str(test_file))
        assert result is True, "File properties validation should pass"

    def test_validation_all_criteria_met(self):
        """Test that file passes all validation criteria together."""
        repo_root = Path(__file__).parent.parent
        test_file = repo_root / "test-396h0d.md"

        write_markdown_file(TEST_CONTENT, "test-396h0d.md")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "No UTF-8 BOM"

        # Check no CRLF
        assert b"\r\n" not in binary_content, "No CRLF line endings"

        # Check file size
        assert 300 <= file_size <= 600, f"File size {file_size} in range 300-600"

        # Check markdown validation
        assert validate_markdown_file(str(test_file)) is True, "Markdown validation passes"

        # Check file properties validation
        assert validate_file_properties(str(test_file)) is True, "Properties validation passes"
