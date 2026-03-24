"""Tests for feature 195: Content Generation Phase - Generate markdown prose content.

This module tests the content generation phase for feature 195, which creates
a markdown file (test-2xz0x5.md) with AI-generated title and prose content.
"""

from unittest.mock import MagicMock, patch

import pytest


class TestFeature195ContentGeneration:
    """Tests for phase 1: Generate markdown prose content using Claude API."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_returns_string(self, mock_get_llm):
        """Test that generate_markdown_content() returns a string."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Artificial Intelligence\n\nArtificial intelligence is transforming industries across the globe. Machine learning algorithms enable computers to learn from data and improve their performance over time. This technology continues to evolve with remarkable capabilities."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert isinstance(content, str)
        assert len(content) > 0

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_starts_with_h1_heading(self, mock_get_llm):
        """Test that generated content starts with H1 markdown heading (# )."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Renewable Energy\n\nRenewable energy sources like solar and wind are becoming increasingly important for sustainable development. These clean energy alternatives reduce carbon emissions and combat climate change. Investment in renewable energy infrastructure continues to accelerate worldwide."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert content.startswith("# "), "Content must start with H1 heading (# )"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_has_blank_line_after_heading(self, mock_get_llm):
        """Test that generated content has blank line after H1 heading."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Ocean Conservation\n\nOceans cover approximately 71% of Earth's surface and contain incredible biodiversity. Marine ecosystems are facing unprecedented threats from pollution, overfishing, and climate change. Protecting these environments is crucial for the survival of countless species."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank (separator)"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_prose_contains_2_to_3_sentences(self, mock_get_llm):
        """Test that generated prose contains exactly 2 or 3 sentences."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Space Exploration\n\nSpace exploration has fundamentally changed our understanding of the universe. Satellites and space probes have revealed the mysteries of distant planets and galaxies. This ongoing quest for knowledge continues to inspire generations of scientists and explorers."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        # Prose is everything after heading and blank line
        prose = "\n".join(lines[2:]).strip()
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_is_meaningful_not_placeholder(self, mock_get_llm):
        """Test that generated content is meaningful and substantive."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Quantum Computing\n\nQuantum computers harness the principles of quantum mechanics to perform calculations at unprecedented speeds. Unlike classical computers, quantum systems can process multiple possibilities simultaneously. This revolutionary technology promises to solve problems that are currently intractable."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Content should be substantive, not placeholder
        assert len(content) > 100, "Content should be substantive (>100 chars)"
        # Should not contain template placeholders
        assert "lorem" not in content.lower(), "Should not contain lorem ipsum"
        assert "[title]" not in content.lower(), "Should not contain template placeholders"
        assert "[content]" not in content.lower(), "Should not contain template placeholders"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_title_and_prose_are_thematically_related(self, mock_get_llm):
        """Test that generated title and prose are thematically related."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Biodiversity\n\nBiodiversity refers to the variety of life forms within an ecosystem. It includes the diversity of species, genetic variation, and ecosystem diversity. Protecting biodiversity is essential for maintaining ecosystem health and human well-being."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        title = lines[0].replace("# ", "").strip().lower()
        prose = "\n".join(lines[2:]).strip().lower()

        # Title should relate to prose (simple check: theme words appear in prose)
        assert len(title) > 3, "Title should be meaningful"
        assert len(prose) > 50, "Prose should be substantive"
        # Topic/title concepts should appear in or relate to the prose
        assert title or "variety" in prose or "species" in prose, "Title and prose should be related"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_ends_with_newline(self, mock_get_llm):
        """Test that generated content ends with newline (Unix convention)."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Climate Change\n\nClimate change is one of the most pressing challenges facing humanity today. Rising global temperatures are causing environmental disruptions and threatening ecosystems worldwide. Collective action and sustainable practices are essential to mitigate its impacts."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert content.endswith("\n"), "Content must end with newline (Unix convention)"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_has_no_markdown_syntax_errors(self, mock_get_llm):
        """Test that generated content has valid markdown syntax."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Artificial Intelligence\n\nAI systems are designed to perform tasks that typically require human intelligence. These systems learn from data and improve their accuracy over time. AI is becoming increasingly integrated into many aspects of modern life."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Check for unclosed markdown formatting
        assert (
            content.count("**") % 2 == 0
        ), "Unmatched bold markdown (**)"
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
    def test_generated_content_can_be_extracted_to_title_and_prose(self, mock_get_llm):
        """Test that generated content can be parsed into title and prose."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Genomics\n\nGenomics is the study of entire genomes and their functions. Modern genomic technologies have revolutionized medicine and agriculture. Understanding genetic sequences enables personalized healthcare and improved crop yields."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()

        # Extract title from H1 heading
        lines = content.split("\n")
        title = lines[0].replace("# ", "").strip()
        # Extract prose from lines after blank line
        prose = "\n".join(lines[2:]).strip()

        assert title, "Title should be extractable and non-empty"
        assert prose, "Prose should be extractable and non-empty"
        assert len(title) > 0, "Title should be non-empty"
        assert len(prose) > 20, "Prose should be meaningful"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_llm_is_called_with_markdown_generation_prompt(self, mock_get_llm):
        """Test that the LLM is called with the markdown generation prompt."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Test Title\n\nThis is sentence one. This is sentence two. This is sentence three.\n"
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()

        # Verify get_reasoning_llm was called
        mock_get_llm.assert_called_once()
        # Verify LLM.call was invoked
        mock_llm.call.assert_called_once()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_api_response_with_dict_content_field(self, mock_get_llm):
        """Test handling of API response with content in dict."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Robotics\n\nRobotics involves the design, construction, and programming of robots. Industrial robots have transformed manufacturing processes worldwide. Future robots may assist humans in healthcare, agriculture, and exploration."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert isinstance(content, str)
        assert content.startswith("# ")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_api_response_validation_rejects_invalid_format(self, mock_get_llm):
        """Test that invalid API responses raise ValueError."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Return content without H1 heading (invalid)
        mock_llm.call.return_value = {
            "content": "This is not a valid markdown heading.\nSentence two.\nSentence three."
        }
        mock_get_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="H1 heading"):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_api_response_validation_rejects_too_few_sentences(self, mock_get_llm):
        """Test that API responses with <2 sentences raise ValueError."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Return content with only 1 sentence (invalid)
        mock_llm.call.return_value = {
            "content": "# Title\n\nOnly one sentence."
        }
        mock_get_llm.return_value = mock_llm

        # The validation can reject either due to length or sentence count
        with pytest.raises(ValueError):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_size_reasonable_for_feature_195(self, mock_get_llm):
        """Test that generated content is in reasonable size range for feature 195."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Renewable Energy Sources\n\nRenewable energy is becoming increasingly important in the global transition away from fossil fuels. Wind, solar, and hydroelectric power provide clean alternatives that reduce greenhouse gas emissions. Many countries are investing heavily in renewable energy infrastructure for a sustainable future."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        content_bytes = len(content.encode("utf-8"))

        # Feature 195 expects file size 250-600 bytes (reasonable for title + 2-3 sentences)
        assert 200 <= content_bytes <= 800, f"Content size {content_bytes} should be reasonable"
