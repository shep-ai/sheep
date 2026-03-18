"""Tests for feature 100 Phase 1: Content Generation & Validation."""

from unittest.mock import MagicMock, patch
import pytest

from sheep.content_generators import generate_markdown_content, _validate_markdown_content


class TestPhase1ContentGeneration:
    """Task 1-1: Generate markdown content via Claude API."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generate_markdown_content_returns_string(self, mock_get_llm):
        """Test that generated content is a string type."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Automated Testing\n\nAutomated testing improves code reliability. It catches regressions early in development. Continuous testing enables faster deployment cycles."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert isinstance(content, str), "Content should be a string"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_has_h1_heading(self, mock_get_llm):
        """Test that generated content contains H1 heading (# format)."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Software Architecture\n\nArchitecture defines system structure and organization. Good architecture supports scalability and maintainability. Design decisions impact long-term project success."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert content.lstrip().startswith("# "), "Content should start with H1 heading (# )"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_has_2_to_3_sentences(self, mock_get_llm):
        """Test that generated prose contains exactly 2 or 3 sentences."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# API Design Patterns\n\nREST APIs follow architectural constraints for scalability. Proper resource modeling simplifies client implementations. Versioning strategies manage backward compatibility."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        # Skip heading and blank line, join prose
        prose = "\n".join(lines[2:]).strip()
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_uses_professional_tone(self, mock_get_llm):
        """Test that generated content uses professional/technical tone."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Database Optimization\n\nQuery optimization reduces latency and resource consumption. Proper indexing strategies improve performance significantly. Monitoring tools enable proactive performance management."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Professional tone indicators: technical terms, formal structure
        assert any(word in content.lower() for word in ["optimization", "performance", "architecture", "design"]), \
            "Content should contain technical/professional terminology"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_has_blank_line_after_heading(self, mock_get_llm):
        """Test that blank line separates heading from prose."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Deployment Strategies\n\nBlue-green deployments minimize downtime. Rolling updates gradually transition traffic. Canary releases test changes with limited users first."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank separator"


class TestPhase1ContentValidation:
    """Task 1-2: Validate generated content against specification."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_validate_generated_content_passes(self, mock_get_llm):
        """Test that valid generated content passes validation."""
        mock_llm = MagicMock()
        valid_content = "# Version Control Systems\n\nGit enables distributed collaboration among developers. Branching strategies organize parallel development work. Merge conflicts require careful resolution to maintain code integrity.\n"
        mock_llm.call.return_value = {"content": valid_content}
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Should not raise exception
        try:
            _validate_markdown_content(content)
            assert True, "Validation should pass for valid content"
        except ValueError as e:
            pytest.fail(f"Validation failed unexpectedly: {e}")

    def test_validate_markdown_content_detects_missing_heading(self):
        """Test that validation catches missing H1 heading."""
        content = "No heading here\n\nJust some prose content. Missing the title. Still no title."
        with pytest.raises(ValueError, match="must start with H1 heading"):
            _validate_markdown_content(content)

    def test_validate_markdown_content_detects_insufficient_sentences(self):
        """Test that validation catches content with less than 2 sentences."""
        # Content with 1 sentence but meeting length requirement (>50 chars)
        content = "# Title\n\nThis is a comprehensive single sentence that contains substantial content and meets the minimum length requirement for validation."
        with pytest.raises(ValueError, match="2-3 sentences"):
            _validate_markdown_content(content)

    def test_validate_markdown_content_detects_too_many_sentences(self):
        """Test that validation catches content with more than 3 sentences."""
        content = "# Title\n\nSentence one is meaningful. Sentence two continues the discussion. Sentence three adds more information. Sentence four exceeds the limit.\n"
        with pytest.raises(ValueError, match="2-3 sentences"):
            _validate_markdown_content(content)

    def test_validate_markdown_content_accepts_two_sentences(self):
        """Test that validation accepts exactly 2 sentences."""
        # Two sentences with substantial content (>50 chars)
        content = "# Title\n\nThis is the first comprehensive sentence that provides meaningful information and meets the minimum content requirements. This second sentence adds additional context and meets length constraints.\n"
        try:
            _validate_markdown_content(content)
            assert True, "Validation should accept 2 sentences"
        except ValueError as e:
            pytest.fail(f"Validation failed for 2 sentences: {e}")

    def test_validate_markdown_content_accepts_three_sentences(self):
        """Test that validation accepts exactly 3 sentences."""
        content = "# Title\n\nThis is the first comprehensive sentence that provides meaningful information and meets content requirements. The second sentence adds additional context and discussion about the topic. This third sentence concludes the prose with final important details.\n"
        try:
            _validate_markdown_content(content)
            assert True, "Validation should accept 3 sentences"
        except ValueError as e:
            pytest.fail(f"Validation failed for 3 sentences: {e}")

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_meets_all_validation_requirements(self, mock_get_llm):
        """Test that generated content meets all validation requirements."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Continuous Integration\n\nCI pipelines automate build and test processes. Early feedback on code changes prevents integration issues. Automated checks maintain code quality standards.\n"
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()

        # Validation checks from _validate_markdown_content
        assert content.strip(), "Content should not be empty"
        assert content.lstrip().startswith("# "), "Should have H1 heading"
        assert len(content) >= 50, "Content should be reasonably long"
        sentence_count = content.count(".")
        assert 2 <= sentence_count <= 3, "Should have 2-3 sentences"
        assert content.endswith("\n"), "Should end with newline"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_content_validation_workflow_with_retry(self, mock_get_llm):
        """Test that validation workflow would retry on failure."""
        # First call returns invalid content (too short)
        invalid_response = {"content": "# Title\n\nShort."}
        # Second call returns valid content
        valid_response = {"content": "# Cloud Computing\n\nCloud infrastructure provides scalable computing resources. Services like AWS, Azure, and GCP dominate the market. Organizations benefit from reduced operational overhead.\n"}

        mock_llm = MagicMock()
        mock_llm.call.side_effect = [invalid_response, valid_response]
        mock_get_llm.return_value = mock_llm

        # Simulate retry logic: attempt 1 fails validation, attempt 2 succeeds
        attempt = 1
        max_attempts = 3
        content = None

        while attempt <= max_attempts:
            response = mock_llm.call([{"role": "user", "content": "Generate markdown"}])
            content_str = response.get("content", "")
            try:
                _validate_markdown_content(content_str)
                content = content_str
                break
            except ValueError:
                attempt += 1
                if attempt > max_attempts:
                    raise

        assert content is not None, "Should have valid content after retry"
        _validate_markdown_content(content)  # Should not raise
        assert mock_llm.call.call_count == 2, "Should have retried once"
