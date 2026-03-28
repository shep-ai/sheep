#!/usr/bin/env python3
"""
Test suite for feature 203 phase 1: Content Generation

Tests the following functions:
- generate_prose(): Deterministic prose generation via Claude API (temperature=0)
- generate_title(): Deterministic title generation via Claude API (temperature=0)
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path to import the feature module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.features.feature_203_markdown_file_creation import (
    generate_prose,
    generate_title,
)


class TestGenerateProse:
    """Test suite for generate_prose function."""

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_prose_returns_string_with_sentences(self, mock_create_llm):
        """Test that generate_prose returns a string with periods (sentences)."""
        # Mock the LLM to return content with H1 and prose
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Sample Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence."
        }
        mock_create_llm.return_value = mock_llm

        result = generate_prose()

        assert isinstance(result, str)
        assert result.count(".") >= 2  # At least 2 sentences
        assert result.count(".") <= 3  # At most 3 sentences
        assert "This is the" in result

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_prose_is_deterministic(self, mock_create_llm):
        """Test that generate_prose returns identical output on repeated calls."""
        # Mock the LLM to return consistent content
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Sample Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence."
        }
        mock_create_llm.return_value = mock_llm

        result1 = generate_prose()
        result2 = generate_prose()

        assert result1 == result2

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_prose_validates_sentence_count(self, mock_create_llm):
        """Test that generate_prose raises ValueError if sentence count is wrong."""
        # Mock the LLM to return only 1 sentence
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nOnly one sentence."
        }
        mock_create_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="expected 2-3"):
            generate_prose()

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_prose_handles_dict_response(self, mock_create_llm):
        """Test that generate_prose handles both dict and string LLM responses."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nThis is sentence one. This is sentence two. This is sentence three."
        }
        mock_create_llm.return_value = mock_llm

        result = generate_prose()
        assert isinstance(result, str)
        assert len(result) > 0

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_prose_raises_on_missing_blank_line(self, mock_create_llm):
        """Test that generate_prose raises ValueError if blank line separator is missing."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\nNo blank line separator.\n"
        }
        mock_create_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="blank line"):
            generate_prose()

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_prose_raises_on_too_many_sentences(self, mock_create_llm):
        """Test that generate_prose raises ValueError if too many sentences."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nFirst. Second. Third. Fourth.\n"
        }
        mock_create_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="expected 2-3"):
            generate_prose()


class TestGenerateTitle:
    """Test suite for generate_title function."""

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_title_returns_string(self, mock_create_llm):
        """Test that generate_title returns a non-empty string."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Sample Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence."
        }
        mock_create_llm.return_value = mock_llm

        result = generate_title()

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Sample Title" in result

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_title_is_deterministic(self, mock_create_llm):
        """Test that generate_title returns identical output on repeated calls."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Consistent Title\n\nSentence one. Sentence two. Sentence three."
        }
        mock_create_llm.return_value = mock_llm

        result1 = generate_title()
        result2 = generate_title()

        assert result1 == result2

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_title_validates_h1_format(self, mock_create_llm):
        """Test that generate_title raises ValueError if H1 heading is missing."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "No H1 heading here\n\nSentence one. Sentence two. Sentence three."
        }
        mock_create_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="must start with H1"):
            generate_title()

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_title_removes_hash_prefix(self, mock_create_llm):
        """Test that generate_title removes the # prefix from the title."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# My Great Title\n\nSentence one. Sentence two. Sentence three."
        }
        mock_create_llm.return_value = mock_llm

        result = generate_title()

        assert result == "My Great Title"
        assert not result.startswith("#")

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_title_raises_on_h2_heading(self, mock_create_llm):
        """Test that generate_title raises ValueError for H2 heading instead of H1."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "## H2 Title\n\nSentence one. Sentence two. Sentence three."
        }
        mock_create_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="H1 heading"):
            generate_title()

    @patch("sheep.features.feature_203_markdown_file_creation.create_llm")
    def test_generate_title_raises_on_empty_title(self, mock_create_llm):
        """Test that generate_title raises ValueError if title is empty."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# \n\nSentence one. Sentence two. Sentence three."
        }
        mock_create_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="empty"):
            generate_title()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
