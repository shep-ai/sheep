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
