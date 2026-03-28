"""Tests for feature 255: Create markdown file test-i3iccc.md.

Tests cover:
- Content generation with valid markdown structure
- Validation of H1 heading, blank line, sentence count
- Error handling for invalid content
- Complete phase 1 orchestration (generate + validate)
"""

import pytest
from unittest.mock import patch, MagicMock

from sheep.features.feature_255_markdown_file_creation import (
    FILENAME,
    FEATURE_NUMBER,
    BRANCH_NAME,
    COMMIT_MESSAGE_TEMPLATE,
    generate_content,
    validate_content,
    run,
)


class TestModuleConstants:
    """Tests for module-level constants."""

    def test_filename_constant(self):
        """Test FILENAME constant has correct value."""
        assert FILENAME == "test-i3iccc.md"

    def test_feature_number_constant(self):
        """Test FEATURE_NUMBER constant has correct value."""
        assert FEATURE_NUMBER == 255

    def test_branch_name_constant(self):
        """Test BRANCH_NAME constant has correct value."""
        assert BRANCH_NAME == "feat/255-markdown-file-creation-17ca12"

    def test_commit_message_template(self):
        """Test COMMIT_MESSAGE_TEMPLATE has correct format."""
        assert "feat(255)" in COMMIT_MESSAGE_TEMPLATE
        assert "test-i3iccc.md" in COMMIT_MESSAGE_TEMPLATE


class TestGenerateContent:
    """Tests for content generation functionality."""

    def test_generate_content_returns_string(self):
        """Test that generate_content returns a string."""
        mock_content = "# Test Title\n\nThis is test content. This is more content. Final sentence."
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            result = generate_content()
            assert isinstance(result, str)
            assert len(result) > 0

    def test_generate_content_calls_content_generators(self):
        """Test that generate_content calls content_generators.generate_markdown_content()."""
        mock_content = "# Title\n\nSentence one. Sentence two. Sentence three."
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content) as mock_gen:
            result = generate_content()
            mock_gen.assert_called_once()
            assert result == mock_content

    def test_generate_content_returns_valid_markdown(self):
        """Test that generated content is valid markdown."""
        mock_content = "# Understanding APIs\n\nAPIs enable communication between software systems. They define the methods and data formats for requests. This makes integration seamless and efficient.\n"
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            result = generate_content()
            assert result.startswith("# ")
            assert "\n\n" in result
            assert "." in result

    def test_generate_content_handles_api_failure(self):
        """Test that generate_content propagates API failures."""
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   side_effect=ValueError("API call failed")):
            with pytest.raises(ValueError, match="API call failed"):
                generate_content()

    def test_generate_content_handles_network_error(self):
        """Test that generate_content handles network errors."""
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   side_effect=Exception("Network timeout")):
            with pytest.raises(Exception, match="Network timeout"):
                generate_content()


class TestValidateContent:
    """Tests for content validation functionality."""

    def test_validate_content_with_valid_markdown(self):
        """Test validate_content with valid markdown."""
        valid_content = "# Cloud Computing\n\nCloud computing provides on-demand computing resources. Organizations benefit from scalability and cost efficiency. This technology transforms infrastructure management.\n"
        # Should not raise
        validate_content(valid_content)

    def test_validate_content_two_sentences(self):
        """Test validate_content accepts exactly 2 sentences."""
        content = "# Title\n\nFirst sentence. Second sentence.\n"
        # Should not raise
        validate_content(content)

    def test_validate_content_three_sentences(self):
        """Test validate_content accepts exactly 3 sentences."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Should not raise
        validate_content(content)

    def test_validate_content_rejects_empty_content(self):
        """Test validate_content rejects empty content."""
        with pytest.raises(ValueError, match="empty"):
            validate_content("")

    def test_validate_content_rejects_whitespace_only(self):
        """Test validate_content rejects whitespace-only content."""
        with pytest.raises(ValueError, match="empty"):
            validate_content("   \n\n   ")

    def test_validate_content_rejects_missing_h1_heading(self):
        """Test validate_content rejects content without H1 heading."""
        content = "## Secondary Heading\n\nSome content. More content. Even more.\n"
        with pytest.raises(ValueError, match="must start with H1"):
            validate_content(content)

    def test_validate_content_rejects_heading_without_space(self):
        """Test validate_content rejects H1 without space after hash."""
        content = "#NoSpace\n\nContent here. More content. Final content.\n"
        with pytest.raises(ValueError, match="must start with H1"):
            validate_content(content)

    def test_validate_content_rejects_missing_blank_line(self):
        """Test validate_content rejects content without blank line separator."""
        content = "# Title\nDirect prose without blank line separator. More content. Final content.\n"
        with pytest.raises(ValueError, match="Second line must be blank"):
            validate_content(content)

    def test_validate_content_rejects_too_few_sentences(self):
        """Test validate_content rejects content with only 1 sentence."""
        content = "# Title\n\nOnly one sentence.\n"
        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_content(content)

    def test_validate_content_rejects_too_many_sentences(self):
        """Test validate_content rejects content with 4+ sentences."""
        content = "# Title\n\nFirst. Second. Third. Fourth.\n"
        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_content(content)

    def test_validate_content_rejects_missing_prose(self):
        """Test validate_content rejects content with no prose after heading."""
        content = "# Title\n\n"
        with pytest.raises(ValueError, match="No prose content"):
            validate_content(content)

    def test_validate_content_rejects_missing_trailing_newline(self):
        """Test validate_content rejects content without trailing newline."""
        content = "# Title\n\nContent here. More content. Final content."
        with pytest.raises(ValueError, match="trailing newline"):
            validate_content(content)

    def test_validate_content_accepts_multiple_paragraphs(self):
        """Test validate_content handles multiple paragraphs correctly."""
        content = "# Title\n\nFirst paragraph first sentence. First paragraph second sentence.\n\nSecond paragraph third sentence.\n"
        # Should not raise (3 sentences total)
        validate_content(content)


class TestOrchestration:
    """Tests for main orchestration function (run)."""

    def test_run_successful_workflow(self):
        """Test run() completes successfully with valid generated content."""
        mock_content = "# Artificial Intelligence\n\nAI systems learn from data through machine learning algorithms. Neural networks enable deep learning for complex pattern recognition. This technology is transforming industries worldwide.\n"

        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            result = run()
            assert result is True

    def test_run_returns_true_on_success(self):
        """Test that run() returns True on successful completion."""
        mock_content = "# Test\n\nSentence one. Sentence two. Sentence three.\n"
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            result = run()
            assert result is True

    def test_run_fails_on_generation_error(self):
        """Test that run() propagates generation errors."""
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   side_effect=ValueError("Generation failed")):
            with pytest.raises(ValueError):
                run()

    def test_run_fails_on_validation_error(self):
        """Test that run() propagates validation errors."""
        mock_content = "# Title\n\nOnly one sentence."
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            with pytest.raises(ValueError, match="2-3 sentences"):
                run()

    def test_run_fails_on_invalid_format(self):
        """Test that run() fails when generated content has invalid format."""
        mock_content = "No heading here. Just content. And more content."
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            with pytest.raises(ValueError, match="must start with H1"):
                run()

    def test_run_validates_blank_line_requirement(self):
        """Test that run() validates blank line separator."""
        mock_content = "# Title\nNo blank line here. Just prose. And more prose.\n"
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            with pytest.raises(ValueError, match="Second line must be blank"):
                run()
