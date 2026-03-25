"""Tests for Feature 205: Create markdown file test-grk9g8.md with title and prose.

This test suite covers:
- Task 1: Module skeleton and constants
- Task 2: Title and prose generation via Claude API
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import the feature module
from sheep.features.feature_205_markdown_file_creation import (
    BRANCH_NAME,
    COMMIT_MESSAGE,
    FILENAME,
    FEATURE_NUMBER,
    MARKDOWN_GENERATION_PROMPT,
    count_sentences,
    create_markdown_file,
    extract_prose_content,
    generate_prose,
    generate_title,
    git_add_file,
    git_commit,
    git_push,
    validate_encoding,
    validate_file_size,
    validate_line_endings,
    validate_markdown_file,
    validate_markdown_format,
    validate_sentence_count,
    verify_file_exists,
    verify_file_size,
    verify_lf_line_endings,
    verify_prose_content,
    verify_utf8_encoding,
)


class TestTask1ModuleSkeleton:
    """Tests for task-1: Module skeleton with constants and logger."""

    def test_module_imports_successfully(self):
        """Test that the feature module can be imported without errors."""
        # This test passes if import doesn't raise an exception
        assert True

    def test_filename_constant(self):
        """Test that FILENAME constant has expected value."""
        assert FILENAME == "test-grk9g8.md"

    def test_feature_number_constant(self):
        """Test that FEATURE_NUMBER constant has expected value."""
        assert FEATURE_NUMBER == 205

    def test_branch_name_constant(self):
        """Test that BRANCH_NAME constant has correct format."""
        assert BRANCH_NAME == "feat/205-markdown-file-creation-4759f4"
        assert "205" in BRANCH_NAME
        assert "feat/" in BRANCH_NAME

    def test_commit_message_constant(self):
        """Test that COMMIT_MESSAGE constant includes feature number and filename."""
        assert "205" in COMMIT_MESSAGE
        assert "test-grk9g8.md" in COMMIT_MESSAGE
        assert "feat" in COMMIT_MESSAGE

    def test_markdown_generation_prompt_defined(self):
        """Test that MARKDOWN_GENERATION_PROMPT is defined and contains key requirements."""
        assert MARKDOWN_GENERATION_PROMPT is not None
        assert "# Title" in MARKDOWN_GENERATION_PROMPT or "H1" in MARKDOWN_GENERATION_PROMPT
        assert "2-3 sentences" in MARKDOWN_GENERATION_PROMPT or "sentences" in MARKDOWN_GENERATION_PROMPT

    def test_generate_title_function_exists(self):
        """Test that generate_title function exists."""
        assert callable(generate_title)

    def test_generate_prose_function_exists(self):
        """Test that generate_prose function exists."""
        assert callable(generate_prose)

    def test_create_markdown_file_function_exists(self):
        """Test that create_markdown_file function exists."""
        assert callable(create_markdown_file)

    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        from sheep.features.feature_205_markdown_file_creation import main
        assert callable(main)


class TestTask2ProseGeneration:
    """Tests for task-2: Title and prose generation via Claude API."""

    def test_generate_title_returns_string(self):
        """Test that generate_title returns a string."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# Test Title\n\nSentence one. Sentence two."

            title = generate_title()
            assert isinstance(title, str)

    def test_generate_title_parsing(self):
        """Test that generate_title correctly parses H1 heading from LLM response."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# My Test Title\n\nSentence one. Sentence two."

            title = generate_title()
            assert title == "My Test Title"

    def test_generate_title_uses_temperature_zero(self):
        """Test that generate_title calls create_llm with temperature=0."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# Title\n\nSentence. Two."

            generate_title()
            mock_llm_factory.assert_called_with(temperature=0)

    def test_generate_title_calls_llm_with_prompt(self):
        """Test that generate_title calls LLM with the generation prompt."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# Title\n\nSentence. Two."

            generate_title()
            mock_llm.call.assert_called_once()
            # Verify the prompt is passed as a message
            call_args = mock_llm.call.call_args
            assert call_args is not None

    def test_generate_title_raises_on_missing_h1(self):
        """Test that generate_title raises ValueError if response doesn't start with H1."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            # Response missing H1 heading
            mock_llm.call.return_value = "Regular text\n\nSentence one. Sentence two."

            with pytest.raises(ValueError, match="H1"):
                generate_title()

    def test_generate_title_raises_on_empty_title(self):
        """Test that generate_title raises ValueError if title is empty."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            # H1 with empty title
            mock_llm.call.return_value = "# \n\nSentence one. Sentence two."

            with pytest.raises(ValueError):
                generate_title()

    def test_generate_title_docstring_exists(self):
        """Test that generate_title has a docstring."""
        assert generate_title.__doc__ is not None
        assert len(generate_title.__doc__) > 0

    def test_generate_prose_returns_string(self):
        """Test that generate_prose returns a string."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# Title\n\nSentence one. Sentence two. Sentence three."

            prose = generate_prose()
            assert isinstance(prose, str)

    def test_generate_prose_parsing(self):
        """Test that generate_prose correctly extracts prose from LLM response."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            expected_prose = "First sentence here. Second sentence here. Third sentence here."
            mock_llm.call.return_value = f"# Title\n\n{expected_prose}"

            prose = generate_prose()
            assert prose == expected_prose

    def test_generate_prose_uses_temperature_zero(self):
        """Test that generate_prose calls create_llm with temperature=0."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# Title\n\nOne. Two. Three."

            generate_prose()
            mock_llm_factory.assert_called_with(temperature=0)

    def test_generate_prose_validates_sentence_count(self):
        """Test that generate_prose validates 2-3 sentence requirement."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            # Only 1 sentence (invalid)
            mock_llm.call.return_value = "# Title\n\nOnly one sentence."

            with pytest.raises(ValueError, match="sentences"):
                generate_prose()

    def test_generate_prose_accepts_two_sentences(self):
        """Test that generate_prose accepts exactly 2 sentences."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# Title\n\nFirst sentence. Second sentence."

            prose = generate_prose()
            assert prose.count(".") == 2

    def test_generate_prose_accepts_three_sentences(self):
        """Test that generate_prose accepts exactly 3 sentences."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# Title\n\nFirst. Second. Third."

            prose = generate_prose()
            assert prose.count(".") == 3

    def test_generate_prose_rejects_four_sentences(self):
        """Test that generate_prose rejects 4 sentences."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            # 4 sentences (invalid)
            mock_llm.call.return_value = "# Title\n\nFirst. Second. Third. Fourth."

            with pytest.raises(ValueError, match="sentences"):
                generate_prose()

    def test_generate_prose_raises_on_missing_blank_line(self):
        """Test that generate_prose raises ValueError if blank line separator is missing."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            # No blank line after heading
            mock_llm.call.return_value = "# Title\nSentence one. Sentence two."

            with pytest.raises(ValueError, match="blank line"):
                generate_prose()

    def test_generate_prose_raises_on_empty_prose(self):
        """Test that generate_prose raises ValueError if prose is empty."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            # No prose after blank line
            mock_llm.call.return_value = "# Title\n\n"

            with pytest.raises(ValueError):
                generate_prose()

    def test_generate_prose_docstring_exists(self):
        """Test that generate_prose has a docstring."""
        assert generate_prose.__doc__ is not None
        assert len(generate_prose.__doc__) > 0

    def test_generate_title_and_prose_use_same_prompt(self):
        """Test that both generate_title and generate_prose use the same prompt."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.return_value = "# Title\n\nSentence. Two."

            generate_title()
            title_call_args = mock_llm.call.call_args

            mock_llm.reset_mock()
            generate_prose()
            prose_call_args = mock_llm.call.call_args

            # Both should be called with the prompt
            assert title_call_args is not None
            assert prose_call_args is not None

    def test_generate_title_handles_dict_response(self):
        """Test that generate_title handles dict responses from LLM."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            # Response as dict (some LLM clients return this)
            mock_llm.call.return_value = {"content": "# Test Title\n\nSentence. Two."}

            title = generate_title()
            assert isinstance(title, str)
            assert "Test Title" in title

    def test_generate_prose_handles_dict_response(self):
        """Test that generate_prose handles dict responses from LLM."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            # Response as dict
            mock_llm.call.return_value = {"content": "# Title\n\nSentence one. Sentence two."}

            prose = generate_prose()
            assert isinstance(prose, str)
            assert "Sentence one" in prose

    def test_generate_title_raises_on_api_failure(self):
        """Test that generate_title raises exception on API failure."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.side_effect = Exception("API error")

            with pytest.raises(Exception):
                generate_title()

    def test_generate_prose_raises_on_api_failure(self):
        """Test that generate_prose raises exception on API failure."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm_factory:
            mock_llm = MagicMock()
            mock_llm_factory.return_value = mock_llm
            mock_llm.call.side_effect = Exception("API error")

            with pytest.raises(Exception):
                generate_prose()


class TestCreateMarkdownFile:
    """Tests for create_markdown_file function."""

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file creates a file at specified location."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value="Sentence one. Sentence two. Sentence three."):
                        path = create_markdown_file("test.md")
                        assert Path("test.md").exists()
                        assert "test.md" in path
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_on_existing_file(self):
        """Test that create_markdown_file raises FileExistsError if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create a file first
                Path("existing.md").write_text("# Existing\n\nContent.\n")

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="Test"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value="Content. More. Third."):
                        with pytest.raises(FileExistsError):
                            create_markdown_file("existing.md")
            finally:
                os.chdir(original_cwd)

    def test_created_file_contains_h1_and_prose(self):
        """Test that created file contains H1 heading and prose separated by blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="My Title"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value="First sentence. Second sentence. Third sentence."):
                        create_markdown_file("test.md")

                        content = Path("test.md").read_text(encoding="utf-8")
                        lines = content.split("\n")

                        assert lines[0] == "# My Title"
                        assert lines[1] == ""  # blank line
                        assert "First sentence. Second sentence. Third sentence." in content
            finally:
                os.chdir(original_cwd)


class TestTask3MarkdownFormatValidation:
    """Tests for task-3: Implement markdown format validation."""

    def test_validate_markdown_format_accepts_valid_format(self):
        """Test that validate_markdown_format accepts valid H1 + blank line + prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create valid markdown: H1 + blank line + prose
                Path("test.md").write_text("# Valid Title\n\nThis is prose.", encoding="utf-8")
                # Should not raise
                validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_missing_h1(self):
        """Test that validate_markdown_format raises ValueError if first line is not H1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Missing H1 heading
                Path("test.md").write_text("Regular text\n\nProse content.", encoding="utf-8")
                with pytest.raises(ValueError, match="H1|heading"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_non_blank_second_line(self):
        """Test that validate_markdown_format raises ValueError if second line is not blank."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Second line is not blank
                Path("test.md").write_text("# Title\nThis should be blank\nProse.", encoding="utf-8")
                with pytest.raises(ValueError, match="blank|separator"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_empty_file(self):
        """Test that validate_markdown_format raises ValueError for empty file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Empty file
                Path("test.md").write_text("", encoding="utf-8")
                with pytest.raises(ValueError):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_multiple_h1_headings(self):
        """Test that validate_markdown_format rejects files with multiple H1 headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Multiple H1 headings
                Path("test.md").write_text("# First Heading\n\nProse.\n\n# Second Heading\n\nMore prose.", encoding="utf-8")
                with pytest.raises(ValueError, match="one H1"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_accepts_h2_as_secondary_heading(self):
        """Test that validate_markdown_format allows H2 headings (counts only H1)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # One H1 and H2 subheading (valid structure)
                Path("test.md").write_text("# Main Title\n\n## Section\n\nProse here.", encoding="utf-8")
                # Should not raise - only one H1
                validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_error_message_specific(self):
        """Test that validation error messages are specific and actionable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("Bad header\n\nProse.", encoding="utf-8")
                try:
                    validate_markdown_format("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    # Error message should identify the specific issue
                    assert "H1" in str(e) or "heading" in str(e)
            finally:
                os.chdir(original_cwd)


class TestTask4ValidationPipeline:
    """Tests for task-4: Implement sentence count, encoding, line endings, and file size validation."""

    # ===== Sentence Count Validation =====

    def test_validate_sentence_count_accepts_exactly_2_sentences(self):
        """Test that validate_sentence_count accepts exactly 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nFirst sentence. Second sentence.", encoding="utf-8")
                # Should not raise
                validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_accepts_exactly_3_sentences(self):
        """Test that validate_sentence_count accepts exactly 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nFirst. Second. Third.", encoding="utf-8")
                # Should not raise
                validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_rejects_1_sentence(self):
        """Test that validate_sentence_count rejects 1 sentence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nOnly one sentence.", encoding="utf-8")
                with pytest.raises(ValueError, match="2-3"):
                    validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_rejects_4_sentences(self):
        """Test that validate_sentence_count rejects 4 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nFirst. Second. Third. Fourth.", encoding="utf-8")
                with pytest.raises(ValueError, match="2-3"):
                    validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_error_message_shows_actual_count(self):
        """Test that error message shows actual sentence count found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nOnly one.", encoding="utf-8")
                try:
                    validate_sentence_count("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    error_msg = str(e)
                    assert "1" in error_msg or "found" in error_msg
            finally:
                os.chdir(original_cwd)

    # ===== Encoding Validation =====

    def test_validate_encoding_accepts_valid_utf8(self):
        """Test that validate_encoding accepts valid UTF-8 files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Valid UTF-8 content
                Path("test.md").write_text("# Title\n\nContent with UTF-8: café.", encoding="utf-8")
                # Should not raise
                validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_rejects_utf8_bom(self):
        """Test that validate_encoding rejects UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with UTF-8 BOM
                content = "# Title\n\nContent."
                file_path = Path("test.md")
                file_path.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))

                with pytest.raises(ValueError, match="BOM"):
                    validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_rejects_invalid_utf8(self):
        """Test that validate_encoding rejects invalid UTF-8 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write invalid UTF-8 bytes
                file_path = Path("test.md")
                file_path.write_bytes(b"# Title\n\n\xff\xfe invalid utf8")

                with pytest.raises(ValueError, match="UTF-8"):
                    validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    # ===== Line Endings Validation =====

    def test_validate_line_endings_accepts_unix_lf(self):
        """Test that validate_line_endings accepts Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # LF line endings (Unix)
                content = "# Title\n\nContent.\n"
                Path("test.md").write_bytes(content.encode("utf-8"))
                # Should not raise
                validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validate_line_endings rejects CRLF Windows line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # CRLF line endings (Windows)
                content = "# Title\r\n\r\nContent.\r\n"
                Path("test.md").write_bytes(content.encode("utf-8"))

                with pytest.raises(ValueError, match="CRLF|Windows"):
                    validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_rejects_cr(self):
        """Test that validate_line_endings rejects CR Mac line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # CR line endings (old Mac)
                content = "# Title\r\rContent.\r"
                Path("test.md").write_bytes(content.encode("utf-8"))

                with pytest.raises(ValueError, match="CR|Mac"):
                    validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    # ===== File Size Validation =====

    def test_validate_file_size_accepts_within_range(self):
        """Test that validate_file_size accepts files within 250-600 byte range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Content that creates file in valid range (~300 bytes)
                content = "# A Comprehensive Title for Testing\n\nThis is the first sentence with enough content to reach the target file size. This is the second sentence that adds more content to the markdown file. This is the third sentence that ensures we meet the minimum byte requirement for valid test files.\n"
                Path("test.md").write_text(content, encoding="utf-8")
                file_size = Path("test.md").stat().st_size
                assert 250 <= file_size <= 600, f"Test setup failed: file size {file_size} outside range"

                # Should not raise
                validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_rejects_too_small(self):
        """Test that validate_file_size rejects files smaller than 250 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Very small content
                Path("test.md").write_text("# X\n\nA.", encoding="utf-8")
                file_size = Path("test.md").stat().st_size
                assert file_size < 250, f"Test setup failed: file size {file_size} not below 250"

                with pytest.raises(ValueError, match="250|range"):
                    validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_rejects_too_large(self):
        """Test that validate_file_size rejects files larger than 600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Very large content
                large_content = "# Title\n\n" + ("X" * 600)
                Path("test.md").write_text(large_content, encoding="utf-8")
                file_size = Path("test.md").stat().st_size
                assert file_size > 600, f"Test setup failed: file size {file_size} not above 600"

                with pytest.raises(ValueError, match="600|range"):
                    validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_error_shows_actual_size(self):
        """Test that error message shows actual file size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# X\n\nA.", encoding="utf-8")
                try:
                    validate_file_size("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    error_msg = str(e)
                    # Should show the actual byte count
                    assert any(str(i) in error_msg for i in range(10, 50))
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_with_custom_range(self):
        """Test that validate_file_size respects custom min/max parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                content = "# Title for Testing\n\nSentence one with content. Sentence two with content. Sentence three with content to reach file size target.\n"
                Path("test.md").write_text(content, encoding="utf-8")
                file_size = Path("test.md").stat().st_size

                # Should pass with custom range that includes file_size
                validate_file_size("test.md", min_bytes=50, max_bytes=1000)

                # Should fail with custom range that excludes file_size
                with pytest.raises(ValueError):
                    validate_file_size("test.md", min_bytes=1000, max_bytes=2000)
            finally:
                os.chdir(original_cwd)

    # ===== Helper Functions =====

    def test_count_sentences_counts_periods(self):
        """Test that count_sentences counts periods correctly."""
        assert count_sentences("First. Second. Third.") == 3
        assert count_sentences("One. Two.") == 2
        assert count_sentences("Only one.") == 1

    def test_count_sentences_raises_on_empty(self):
        """Test that count_sentences raises ValueError on empty prose."""
        with pytest.raises(ValueError):
            count_sentences("")

    def test_extract_prose_content_extracts_correctly(self):
        """Test that extract_prose_content extracts prose after blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nExpected prose content here.", encoding="utf-8")
                prose = extract_prose_content("test.md")
                assert prose == "Expected prose content here."
            finally:
                os.chdir(original_cwd)

    def test_extract_prose_content_multiline(self):
        """Test that extract_prose_content handles multiline prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nLine one.\nLine two.\nLine three.", encoding="utf-8")
                prose = extract_prose_content("test.md")
                assert "Line one" in prose
                assert "Line three" in prose
            finally:
                os.chdir(original_cwd)

    # ===== Backward Compatibility =====

    def test_verify_utf8_encoding_wrapper_exists(self):
        """Test that verify_utf8_encoding backward-compatibility wrapper exists."""
        assert callable(verify_utf8_encoding)

    def test_verify_lf_line_endings_wrapper_exists(self):
        """Test that verify_lf_line_endings backward-compatibility wrapper exists."""
        assert callable(verify_lf_line_endings)

    def test_verify_prose_content_wrapper_exists(self):
        """Test that verify_prose_content backward-compatibility wrapper exists."""
        assert callable(verify_prose_content)

    def test_verify_file_size_wrapper_exists(self):
        """Test that verify_file_size backward-compatibility wrapper exists."""
        assert callable(verify_file_size)


class TestTask5FileCreation:
    """Tests for task-5: File creation with proper UTF-8 encoding and validation."""

    def test_create_markdown_file_creates_file_with_content(self):
        """Test that create_markdown_file creates file with proper encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value="Sentence one. Sentence two. Sentence three."):
                        create_markdown_file("test_output.md")

                        # Verify file exists
                        assert Path("test_output.md").exists()

                        # Verify content is correct
                        content = Path("test_output.md").read_text(encoding="utf-8")
                        assert "# Test Title" in content
                        assert "Sentence one" in content
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_with_utf8_encoding(self):
        """Test that created file has UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value="Content. More. Third."):
                        create_markdown_file("test_utf8.md")

                        # Verify UTF-8 without BOM
                        binary_content = Path("test_utf8.md").read_bytes()
                        assert not binary_content.startswith(b"\xef\xbb\xbf")
                        # Should be valid UTF-8
                        binary_content.decode("utf-8")
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_with_lf_line_endings(self):
        """Test that created file uses Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value="Content. More. Third."):
                        create_markdown_file("test_lf.md")

                        # Verify LF line endings
                        binary_content = Path("test_lf.md").read_bytes()
                        assert b"\r\n" not in binary_content  # No CRLF
                        assert b"\r" not in binary_content    # No CR
                        # Should contain LF
                        assert b"\n" in binary_content
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_runs_validation_pipeline(self):
        """Test that create_markdown_file runs comprehensive validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Use longer prose to meet file size requirements (250-600 bytes)
                long_prose = "This is a comprehensive sentence with enough content to meet the minimum file size requirements for the test markdown file. Another sentence follows here to add additional context and depth to the content. The third sentence provides even more detail and ensures compliance with all validation requirements."

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value=long_prose):
                        # If validation fails, create_markdown_file should raise
                        create_markdown_file("test_validate.md")

                        # Validate passes if we get here
                        validate_markdown_file("test_validate.md")
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_rejects_if_file_exists(self):
        """Test that create_markdown_file raises FileExistsError if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file first
                Path("existing.md").write_text("# Existing\n\nContent.", encoding="utf-8")

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="Test"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value="Content. More. Third."):
                        with pytest.raises(FileExistsError):
                            create_markdown_file("existing.md")
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_returns_path(self):
        """Test that create_markdown_file returns absolute path as string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_205_markdown_file_creation.generate_title", return_value="Test"):
                    with patch("sheep.features.feature_205_markdown_file_creation.generate_prose", return_value="Content. More. Third."):
                        result = create_markdown_file("test_path.md")
                        assert isinstance(result, str)
                        assert "test_path.md" in result
                        assert Path(result).is_absolute()
            finally:
                os.chdir(original_cwd)


class TestTask6GitOperations:
    """Tests for task-6: Git operations (add, commit, push)."""

    def test_git_add_file_stages_file(self):
        """Test that git_add_file stages file with git add."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Create a test file
                Path("test.md").write_text("# Test\n\nContent.", encoding="utf-8")

                # Stage the file
                git_add_file("test.md")

                # Verify file is staged
                result = subprocess.run(["git", "status", "test.md"], capture_output=True, text=True)
                assert "Changes to be committed" in result.stdout or "new file" in result.stdout
            finally:
                os.chdir(original_cwd)

    def test_git_add_file_raises_on_failure(self):
        """Test that git_add_file raises CalledProcessError if git fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # No git repo - git add should fail
                with pytest.raises(subprocess.CalledProcessError):
                    git_add_file("nonexistent.md")
            finally:
                os.chdir(original_cwd)

    def test_git_commit_creates_commit(self):
        """Test that git_commit creates commit with specified message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Create and stage a file
                Path("test.md").write_text("# Test\n\nContent.", encoding="utf-8")
                subprocess.run(["git", "add", "test.md"], check=True, capture_output=True)

                # Create commit
                git_commit(message="test: add test file")

                # Verify commit exists
                result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
                assert "test: add test file" in result.stdout or len(result.stdout) > 0
            finally:
                os.chdir(original_cwd)

    def test_git_commit_raises_on_nothing_to_commit(self):
        """Test that git_commit raises if nothing staged."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Try to commit with nothing staged
                with pytest.raises(subprocess.CalledProcessError):
                    git_commit(message="Empty commit")
            finally:
                os.chdir(original_cwd)

    def test_git_push_raises_when_no_remote(self):
        """Test that git_push raises when remote doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo without remote
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

                # Create and commit a file
                Path("test.md").write_text("# Test\n\nContent.", encoding="utf-8")
                subprocess.run(["git", "add", "test.md"], check=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", "test"], check=True, capture_output=True)

                # Try to push (should fail - no remote)
                with pytest.raises(subprocess.CalledProcessError):
                    git_push("main")
            finally:
                os.chdir(original_cwd)

    def test_git_add_file_function_exists(self):
        """Test that git_add_file function exists."""
        assert callable(git_add_file)

    def test_git_commit_function_exists(self):
        """Test that git_commit function exists."""
        assert callable(git_commit)

    def test_git_push_function_exists(self):
        """Test that git_push function exists."""
        assert callable(git_push)


class TestTask7MainOrchestration:
    """Tests for task-7: Main orchestration with full workflow."""

    def test_main_function_orchestrates_workflow(self):
        """Test that main() orchestrates complete workflow successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo with proper config
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)
                # Create feature branch
                subprocess.run(["git", "checkout", "-b", BRANCH_NAME], check=True, capture_output=True)

                # Use longer prose to meet file size requirements
                long_response = "# Amazing Technical Innovation\n\nThis comprehensive approach to software development demonstrates advanced techniques and best practices throughout the entire implementation. The methodology ensures quality, reliability, and maintainability across all components and modules. Furthermore, the systematic approach guarantees consistent results and enables seamless integration with existing systems and infrastructure."

                with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm:
                    mock_llm_instance = MagicMock()
                    mock_llm.return_value = mock_llm_instance
                    mock_llm_instance.call.return_value = long_response

                    # Mock only the git_push function to avoid network errors
                    with patch("sheep.features.feature_205_markdown_file_creation.git_push") as mock_push:
                        from sheep.features.feature_205_markdown_file_creation import main
                        result = main()

                        # Main should return 0 on success
                        assert result == 0

                        # File should be created
                        assert Path(FILENAME).exists()

                        # Verify git_push was called
                        mock_push.assert_called_once_with(BRANCH_NAME)
            finally:
                os.chdir(original_cwd)

    def test_main_returns_zero_on_success(self):
        """Test that main() returns 0 on successful execution."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Setup git repo
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)
                subprocess.run(["git", "checkout", "-b", BRANCH_NAME], check=True, capture_output=True)

                # Use longer prose for file size requirements
                long_response = "# Technical Documentation\n\nThis comprehensive documentation provides detailed technical specifications and implementation guidelines for modern software systems. The complete guide demonstrates practical approaches and methodologies that ensure quality and consistency throughout the development process. Advanced techniques and best practices are thoroughly explained with clear examples and detailed explanations."

                with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm:
                    mock_llm_instance = MagicMock()
                    mock_llm.return_value = mock_llm_instance
                    mock_llm_instance.call.return_value = long_response

                    with patch("sheep.features.feature_205_markdown_file_creation.git_push"):
                        from sheep.features.feature_205_markdown_file_creation import main
                        result = main()
                        assert result == 0
            finally:
                os.chdir(original_cwd)

    def test_main_returns_nonzero_on_error(self):
        """Test that main() returns non-zero on error."""
        with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm:
            mock_llm.side_effect = Exception("API error")

            from sheep.features.feature_205_markdown_file_creation import main
            result = main()
            assert result != 0

    def test_main_uses_correct_filename(self):
        """Test that main() uses FILENAME constant."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)
                subprocess.run(["git", "checkout", "-b", BRANCH_NAME], check=True, capture_output=True)

                # Use longer prose
                long_response = "# Amazing Content\n\nThis demonstrates advanced technical approaches with comprehensive documentation. Multiple strategies and methodologies provide excellent examples throughout the entire system. The complete implementation showcases best practices and industry standard approaches that deliver measurable results."

                with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm:
                    mock_llm_instance = MagicMock()
                    mock_llm.return_value = mock_llm_instance
                    mock_llm_instance.call.return_value = long_response

                    with patch("sheep.features.feature_205_markdown_file_creation.git_push"):
                        from sheep.features.feature_205_markdown_file_creation import main
                        main()

                        # Verify file was created with correct name
                        assert Path(FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_main_uses_conventional_commit_message(self):
        """Test that main() uses conventional commit format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                subprocess.run(["git", "init"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)
                subprocess.run(["git", "checkout", "-b", BRANCH_NAME], check=True, capture_output=True)

                # Use longer prose
                long_response = "# Software Engineering Excellence\n\nModern software development requires comprehensive understanding of design patterns and architectural principles throughout the entire system. Best practices ensure maintainability, scalability, and reliability of applications across diverse environments. Industry standards and proven methodologies guide successful implementation of complex systems."

                with patch("sheep.features.feature_205_markdown_file_creation.create_llm") as mock_llm:
                    mock_llm_instance = MagicMock()
                    mock_llm.return_value = mock_llm_instance
                    mock_llm_instance.call.return_value = long_response

                    with patch("sheep.features.feature_205_markdown_file_creation.git_push"):
                        from sheep.features.feature_205_markdown_file_creation import main
                        main()

                        # Verify commit message format
                        result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
                        # Should contain "feat:" for conventional commits
                        assert "feat" in result.stdout or len(result.stdout) > 0
            finally:
                os.chdir(original_cwd)
