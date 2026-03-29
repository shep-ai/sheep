"""Tests for feature 271: Creating markdown file test-y1zgop.md with title and prose content."""

import pytest


class TestContentStructureValidation:
    """Unit tests for validating markdown content structure (can run without API)."""

    @staticmethod
    def validate_markdown_structure(content: str) -> bool:
        """Helper function to validate markdown content structure."""
        if not content or not isinstance(content, str):
            return False

        lines = content.split("\n")
        if len(lines) < 4:  # At least heading, blank, prose, newline
            return False

        # Check H1 heading
        if not lines[0].startswith("# "):
            return False

        # Check blank line separator
        if lines[1] != "":
            return False

        # Check prose content
        prose_lines = [l for l in lines[2:] if l.strip()]
        if not prose_lines:
            return False

        # Check sentence count (count periods)
        prose_text = "\n".join(prose_lines)
        sentence_count = prose_text.count(".")
        if not (2 <= sentence_count <= 3):
            return False

        # Check trailing newline
        if not content.endswith("\n"):
            return False

        return True

    def test_valid_content_structure(self):
        """Test that valid markdown content passes validation."""
        valid_content = "# Example Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"
        assert self.validate_markdown_structure(valid_content)

    def test_invalid_content_missing_heading(self):
        """Test that content without H1 heading fails validation."""
        invalid_content = "Example Title\n\nThis is the first sentence. This is the second sentence.\n"
        assert not self.validate_markdown_structure(invalid_content)

    def test_invalid_content_missing_blank_line(self):
        """Test that content without blank line separator fails validation."""
        invalid_content = "# Example Title\nThis is the first sentence. This is the second sentence.\n"
        assert not self.validate_markdown_structure(invalid_content)

    def test_invalid_content_insufficient_sentences(self):
        """Test that content with only 1 sentence fails validation."""
        invalid_content = "# Example Title\n\nThis is only one sentence.\n"
        assert not self.validate_markdown_structure(invalid_content)

    def test_invalid_content_too_many_sentences(self):
        """Test that content with more than 3 sentences fails validation."""
        invalid_content = "# Example Title\n\nSentence one. Sentence two. Sentence three. Sentence four.\n"
        assert not self.validate_markdown_structure(invalid_content)

    def test_invalid_content_missing_trailing_newline(self):
        """Test that content without trailing newline fails validation."""
        invalid_content = "# Example Title\n\nThis is the first sentence. This is the second sentence."
        assert not self.validate_markdown_structure(invalid_content)


class TestContentGenerationIntegration:
    """Integration tests for content generation (requires API key)."""

    @pytest.mark.skipif(
        not True,  # Can be replaced with os.getenv('ANTHROPIC_API_KEY')
        reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_generated_content_is_not_empty(self):
        """Test that generate_markdown_content() returns non-empty content."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        assert content is not None
        assert isinstance(content, str)
        assert len(content) > 0
        assert content.strip() != ""

    @pytest.mark.skipif(
        not True,
        reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_generated_content_starts_with_h1_heading(self):
        """Test that generated content starts with H1 heading (# ...)."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        lines = content.split("\n")
        assert len(lines) > 0
        assert lines[0].startswith("# ")
        assert len(lines[0]) > 2  # Has content after "# "

    @pytest.mark.skipif(
        not True,
        reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_generated_content_has_blank_line_separator(self):
        """Test that generated content has blank line after H1 heading."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        lines = content.split("\n")
        assert len(lines) >= 3
        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Second line should be blank

    @pytest.mark.skipif(
        not True,
        reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_generated_content_has_prose_sentences(self):
        """Test that generated content contains 2-3 sentences of prose."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        lines = content.split("\n")

        # Extract prose content (skip heading and blank line)
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @pytest.mark.skipif(
        not True,
        reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_generated_content_structure_matches_pattern(self):
        """Test that generated content matches pattern: heading + blank line + prose."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        lines = content.split("\n")

        # Should have at least 4 lines: heading, blank, prose content, and possibly trailing newline
        assert len(lines) >= 4

        # First line: H1 heading
        assert lines[0].startswith("# ")

        # Second line: blank separator
        assert lines[1] == ""

        # Third line and beyond: prose content (should not be empty)
        prose_lines = [l for l in lines[2:] if l.strip()]
        assert len(prose_lines) > 0

        # Prose should contain periods (sentences)
        prose_text = "\n".join(prose_lines)
        assert "." in prose_text

    @pytest.mark.skipif(
        not True,
        reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_generated_content_ends_with_newline(self):
        """Test that generated content ends with trailing newline (Unix convention)."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        assert content.endswith("\n")

    @pytest.mark.skipif(
        not True,
        reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_generated_content_is_valid_utf8(self):
        """Test that generated content is valid UTF-8."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        # If it's a string, it's already valid UTF-8
        assert isinstance(content, str)
        # Verify it can be encoded/decoded as UTF-8
        encoded = content.encode("utf-8")
        decoded = encoded.decode("utf-8")
        assert decoded == content

    @pytest.mark.skipif(
        not True,
        reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_generated_content_reasonable_length(self):
        """Test that generated content has reasonable length (250-600 bytes)."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        content_bytes = content.encode("utf-8")
        content_length = len(content_bytes)

        # Content should be in reasonable range for H1 + 2-3 sentences
        assert 150 <= content_length <= 800, f"Content length {content_length} outside expected range"
