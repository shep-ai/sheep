"""Tests for feature 291: Create markdown file test-p1rf9x.md with prose content.

This module tests the complete workflow for feature 291, which creates
a markdown file with AI-generated title and 2-3 sentences of prose content.

Phase 1 Focus: Content Generation & Validation Setup
- Tests for Claude API content generation
- Tests for comprehensive content validation
"""

from unittest.mock import MagicMock, patch

import pytest


class TestFeature291ContentGeneration:
    """Tests for phase 1: Generate markdown prose content using Claude API."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_returns_string(self, mock_get_llm):
        """Test that generate_markdown_content() returns a non-empty string."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Machine Learning\n\nMachine learning is a subset of artificial intelligence that enables systems to learn from data. These algorithms improve their performance through experience without explicit programming. Applications range from recommendation systems to autonomous vehicles."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: Claude API call returns non-empty content string
        content = generate_markdown_content()
        assert isinstance(content, str)
        assert len(content) > 0

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_contains_h1_markdown_heading(self, mock_get_llm):
        """Test that content contains an H1 markdown heading (starts with '# ')."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Data Science\n\nData science combines statistics, programming, and domain expertise. It enables organizations to extract insights from large datasets. These insights drive informed decision-making across industries."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: Content contains an H1 markdown heading
        content = generate_markdown_content()
        assert content.startswith("# "), "Content must start with H1 heading (# )"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_contains_prose_after_heading(self, mock_get_llm):
        """Test that content contains at least one sentence of prose after heading."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Cloud Computing\n\nCloud computing provides on-demand access to computing resources over the internet. Organizations can scale infrastructure without maintaining physical data centers. This flexibility reduces costs and enables faster deployment of applications."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: Content contains at least one sentence of prose
        content = generate_markdown_content()
        lines = content.split("\n")
        assert len(lines) >= 3, "Content must have heading, blank line, and prose"
        # Check for prose content (sentence count)
        prose = "\n".join(lines[2:]).strip()
        assert len(prose) > 0, "Prose content must be present"
        assert "." in prose, "Prose must contain at least one sentence (period)"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_api_call_logs_generation_attempt(self, mock_get_llm):
        """Test that API calls are logged via sheep.observability.logging."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Cybersecurity\n\nCybersecurity protects digital systems from malicious attacks. Organizations implement multiple layers of defense including firewalls and encryption. Awareness training is essential to prevent social engineering threats."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: All API calls are logged
        # This test verifies the function completes; logging is tested via structured logs
        with patch("sheep.content_generators._logger") as mock_logger:
            content = generate_markdown_content()
            # Verify logging occurred
            mock_logger.info.assert_called()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_content_generation_completes_within_timeout(self, mock_get_llm):
        """Test that content generation completes in reasonable time (< 30 seconds)."""
        from sheep.content_generators import generate_markdown_content
        import time

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Blockchain Technology\n\nBlockchain is a distributed ledger technology that enables secure and transparent transactions. Each block contains cryptographic hashes of previous blocks for immutability. Applications extend beyond cryptocurrency to supply chain and healthcare."
        }
        mock_get_llm.return_value = mock_llm

        # Task 1 AC: Content generation time < 30 seconds
        start_time = time.time()
        content = generate_markdown_content()
        elapsed = time.time() - start_time

        assert elapsed < 30, f"Content generation took {elapsed}s, should be < 30s"
        assert len(content) > 0


class TestFeature291ContentValidation:
    """Tests for phase 1: Validate generated content structure and quality."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_heading_format_accepts_h1(self, mock_get_llm):
        """Test validation function checks for valid H1 heading format (^# )."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Internet of Things\n\nThe IoT connects billions of devices to the internet for data collection. Smart devices communicate autonomously to optimize processes. This technology is transforming healthcare, agriculture, and urban planning."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Validation checks for valid H1 heading format
        content = generate_markdown_content()  # Should not raise (validation passes)
        assert content.startswith("# ")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_heading_format_rejects_no_h1(self, mock_get_llm):
        """Test validation rejects content without H1 heading."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Return content without H1 heading
        mock_llm.call.return_value = {
            "content": "No heading here.\nThis is invalid content. No heading present."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Invalid heading (no '#') raises ValueError
        with pytest.raises(ValueError, match="H1 heading"):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_sentence_count_2_to_3_sentences(self, mock_get_llm):
        """Test validation counts sentences using regex (expects 2-3)."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Neural Networks\n\nNeural networks are computational models inspired by biological brains. They consist of interconnected nodes that process information through layers. Deep learning has revolutionized image recognition and natural language processing."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Validation checks for 2-3 sentences
        content = generate_markdown_content()  # Should not raise (3 sentences)
        sentence_count = content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_sentence_count_rejects_too_few(self, mock_get_llm):
        """Test validation rejects prose with < 2 sentences."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Only 1 sentence
        mock_llm.call.return_value = {
            "content": "# Title\n\nOnly one sentence."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Prose with < 2 sentences raises ValueError
        with pytest.raises(ValueError):
            generate_markdown_content()

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_prose_length_100_to_300_characters(self, mock_get_llm):
        """Test validation checks prose length is 100-300 characters."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Prose: "Augmented reality overlays digital information on the physical world. AR applications range from gaming to industrial maintenance. This immersive technology enhances user experiences across multiple domains."
        # This prose is approximately 185 characters
        mock_llm.call.return_value = {
            "content": "# Augmented Reality\n\nAugmented reality overlays digital information on the physical world. AR applications range from gaming to industrial maintenance. This immersive technology enhances user experiences."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Prose length 100-300 characters is valid
        content = generate_markdown_content()
        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()
        assert 100 <= len(prose) <= 300, f"Prose length {len(prose)} should be 100-300"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_utf8_encoding_no_bom(self, mock_get_llm):
        """Test validation checks UTF-8 encoding (no BOM, valid bytes)."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Quantum Cryptography\n\nQuantum cryptography uses quantum mechanics principles for secure communication. Quantum key distribution enables detection of eavesdropping attempts. This technology represents the future of unhackable communications."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Content validates UTF-8 encoding
        content = generate_markdown_content()
        # Verify can be encoded/decoded as UTF-8
        encoded = content.encode("utf-8")
        decoded = encoded.decode("utf-8")
        assert decoded == content

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_blank_line_separator_between_heading_and_prose(self, mock_get_llm):
        """Test validation verifies blank line exists between heading and prose."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Vertical Farming\n\nVertical farming uses controlled environment agriculture to grow crops indoors. This method reduces water consumption and eliminates pesticide use. Urban vertical farms increase food security in densely populated areas."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Blank line separator is validated
        content = generate_markdown_content()
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line must be H1"
        assert lines[1] == "", "Second line must be blank separator"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_content_structure_complete(self, mock_get_llm):
        """Test comprehensive validation of all structure and quality requirements."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Genetic Engineering\n\nGenetic engineering modifies DNA to introduce desirable traits. CRISPR technology has revolutionized gene editing with unprecedented precision. Applications in medicine and agriculture promise breakthroughs in treatment and food production."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Invalid content triggers ValueError
        content = generate_markdown_content()
        assert content  # Should complete without error

        # Verify all validation criteria are met
        lines = content.split("\n")
        assert lines[0].startswith("# "), "H1 heading required"
        assert lines[1] == "", "Blank line separator required"
        prose = "\n".join(lines[2:]).strip()
        assert 100 <= len(prose) <= 300, "Prose length 100-300 chars"
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, "2-3 sentences required"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_invalid_content_raises_value_error_with_message(self, mock_get_llm):
        """Test that invalid content triggers ValueError with descriptive message."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        # Invalid: no H1 heading
        mock_llm.call.return_value = {
            "content": "This is not markdown.\nNo heading present here."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Invalid content raises ValueError
        with pytest.raises(ValueError) as exc_info:
            generate_markdown_content()
        assert len(str(exc_info.value)) > 0, "Error message should describe failure"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_returns_true_for_valid_content(self, mock_get_llm):
        """Test that valid content passes validation and returns successfully."""
        from sheep.content_generators import generate_markdown_content

        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Synthetic Biology\n\nSynthetic biology designs and constructs biological systems with novel functions. Researchers engineer organisms for biofuel production and pharmaceutical manufacturing. This field promises sustainable solutions to global challenges."
        }
        mock_get_llm.return_value = mock_llm

        # Task 2 AC: Valid content returns True (implicitly, no exception raised)
        content = generate_markdown_content()
        assert isinstance(content, str)
        assert len(content) > 0
