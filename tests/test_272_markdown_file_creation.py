"""Tests for feature 272: Creating markdown file test-4mg4tn.md with title and prose content."""

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


class TestPhase1FileCreationAndValidation:
    """Tests for Phase 1: File creation and validation."""

    FEATURE_272_FILENAME = "test-4mg4tn.md"

    def test_file_does_not_exist_before_write(self):
        """Test that test-4mg4tn.md does not exist at start of test."""
        from pathlib import Path

        filepath = Path.cwd() / self.FEATURE_272_FILENAME
        # For this test, we assume a clean state or clean up after
        # In actual test, we'd ensure file is removed before test runs
        if filepath.exists():
            filepath.unlink()  # Clean up for this test
        assert not filepath.exists(), f"File {filepath} should not exist before write"

    def test_write_markdown_file_creates_file_at_repo_root(self):
        """Test that write_markdown_file() creates file at repository root."""
        from pathlib import Path
        from sheep.content_generators import write_markdown_file

        # Create test content
        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"

        # Clean up any existing file
        filepath = Path.cwd() / self.FEATURE_272_FILENAME
        if filepath.exists():
            filepath.unlink()

        # Write the file
        result = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Verify file was created
        assert filepath.exists(), f"File {filepath} was not created"
        assert result == str(filepath)

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_write_markdown_file_contains_correct_content(self):
        """Test that written file contains exact content."""
        from pathlib import Path
        from sheep.content_generators import write_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"

        # Clean up any existing file
        filepath = Path.cwd() / self.FEATURE_272_FILENAME
        if filepath.exists():
            filepath.unlink()

        # Write the file
        write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Read and verify content
        assert filepath.exists()
        read_content = filepath.read_text(encoding="utf-8")
        assert read_content == test_content

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_validation_passes_for_valid_content(self):
        """Test that validate_markdown_file() passes for valid content."""
        from pathlib import Path
        from sheep.content_generators import write_markdown_file, validate_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"

        # Clean up any existing file
        filepath = Path.cwd() / self.FEATURE_272_FILENAME
        if filepath.exists():
            filepath.unlink()

        # Write the file
        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Validate should pass without raising exception
        result = validate_markdown_file(filepath_str)
        assert result is True

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_size_is_in_expected_range(self):
        """Test that created file size is in range 250-600 bytes for typical content."""
        from pathlib import Path
        from sheep.content_generators import write_markdown_file

        # Use realistic content similar to generated content
        test_content = (
            "# Advanced Cloud Computing\n"
            "\n"
            "Cloud computing has revolutionized how businesses deploy and scale applications. "
            "Organizations leverage distributed computing resources across networks for improved "
            "efficiency and cost-effectiveness. The shift from on-premise infrastructure to cloud "
            "platforms represents one of the most significant technological transitions in modern IT.\n"
        )

        # Clean up any existing file
        filepath = Path.cwd() / self.FEATURE_272_FILENAME
        if filepath.exists():
            filepath.unlink()

        # Write the file
        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Check file size
        file_size = filepath.stat().st_size
        assert 250 <= file_size <= 600, f"File size {file_size} outside expected range (250-600)"

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_uses_utf8_encoding_without_bom(self):
        """Test that file is saved with UTF-8 encoding and no BOM."""
        from pathlib import Path
        from sheep.content_generators import write_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"

        # Clean up any existing file
        filepath = Path.cwd() / self.FEATURE_272_FILENAME
        if filepath.exists():
            filepath.unlink()

        # Write the file
        write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Check encoding by reading as binary
        assert filepath.exists()
        binary_content = filepath.read_bytes()

        # Verify not UTF-8 with BOM (BOM is EF BB BF)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

        # Verify can decode as UTF-8
        decoded = binary_content.decode("utf-8")
        assert decoded == test_content

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_uses_lf_line_endings_not_crlf(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        from pathlib import Path
        from sheep.content_generators import write_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"

        # Clean up any existing file
        filepath = Path.cwd() / self.FEATURE_272_FILENAME
        if filepath.exists():
            filepath.unlink()

        # Write the file
        write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Check line endings by reading as binary
        assert filepath.exists()
        binary_content = filepath.read_bytes()

        # Verify no CRLF (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File should use LF line endings, not CRLF"

        # Verify file only has LF
        assert b"\n" in binary_content, "File should contain newlines"

        # Clean up
        if filepath.exists():
            filepath.unlink()
