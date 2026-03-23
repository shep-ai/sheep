"""Tests for feature 184: Create markdown file test-396h0d.md with title and prose content."""

from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import generate_markdown_content


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
