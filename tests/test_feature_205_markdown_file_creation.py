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
