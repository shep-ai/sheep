"""Tests for markdown content generation."""

from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import generate_markdown_content


class TestGenerateMarkdownContent:
    """Tests for markdown content generation with Claude API."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_returns_string_with_h1_heading(self, mock_get_llm):
        """Test that generated content starts with H1 markdown heading."""
        # Mock the LLM response
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Machine Learning\n\nMachine learning is a subset of artificial intelligence. It enables computers to learn from data without explicit programming. This technology powers many modern applications."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert isinstance(content, str)
        assert content.startswith("# "), "Content should start with H1 heading (# )"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_contains_2_to_3_sentences(self, mock_get_llm):
        """Test that generated prose contains 2-3 sentences."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Quantum Physics\n\nQuantum physics describes the behavior of matter at atomic scales. It introduces concepts like superposition and entanglement. These phenomena challenge our intuition about reality."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Split by heading
        lines = content.split("\n")
        # Skip the heading line and blank line
        prose = "\n".join(lines[2:])
        # Count sentences by periods
        sentence_count = prose.count(".")
        assert (
            2 <= sentence_count <= 3
        ), f"Expected 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_has_blank_line_after_heading(self, mock_get_llm):
        """Test that there's a blank line after the H1 heading."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Python Programming\n\nPython is a versatile programming language. It emphasizes code readability. Many developers prefer it for its simplicity."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        assert lines[0].startswith(
            "# "
        ), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_no_markdown_syntax_errors(self, mock_get_llm):
        """Test that generated content has no obvious markdown syntax errors."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Astronomy\n\nStars are massive celestial bodies. They produce energy through nuclear fusion. This energy travels to us as light and heat."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Check for unclosed markdown formatting
        assert (
            content.count("**") % 2 == 0
        ), "Unmatched bold markdown (**))"
        assert (
            content.count("__") % 2 == 0
        ), "Unmatched bold markdown (__)"
        assert (
            content.count("*") % 2 == 0
        ), "Unmatched italic markdown (*)"
        assert (
            content.count("_") % 2 == 0
        ), "Unmatched italic markdown (_)"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_is_extractable(self, mock_get_llm):
        """Test that topic can be identified from generated prose."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Ocean Ecosystems\n\nOceans cover most of Earth's surface. They support incredible biodiversity. These ecosystems face unprecedented challenges from climate change."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        # First line is heading (title)
        title = lines[0].replace("# ", "").strip()
        # Prose is lines 2+ (skipping heading and blank line)
        prose = "\n".join(lines[2:]).strip()

        assert title, "Title should be non-empty"
        assert prose, "Prose should be non-empty"
        # Topic/title should appear in prose or be conceptually related
        assert len(title) > 3, "Title should be meaningful (not too short)"
        assert len(prose) > 20, "Prose should be meaningful (not too short)"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_content_format_structure(self, mock_get_llm):
        """Test the overall structure of generated markdown."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Neuroscience\n\nThe brain is the most complex organ in the body. It contains billions of neurons. These cells communicate through electrical and chemical signals."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Should have newlines
        assert "\n" in content
        # Should end with newline (Unix convention)
        assert content.endswith("\n")
        # Should have exactly one H1 heading
        h1_count = content.count("# ")
        assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"
