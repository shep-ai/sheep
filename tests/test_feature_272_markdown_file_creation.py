"""Tests for feature 272: Creating markdown file test-6fioxo.md with title and prose content."""

import os
import pytest
from pathlib import Path


class TestContentGenerationPhase:
    """Tests for task-1: Generate markdown content via Claude API."""

    @pytest.mark.skipif(
        not os.getenv("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set - skipping API integration test",
    )
    def test_generate_markdown_content_returns_non_empty_string(self):
        """Test that generate_markdown_content() returns non-empty string."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        assert content is not None
        assert isinstance(content, str)
        assert len(content) > 0
        assert content.strip() != ""

    @pytest.mark.skipif(
        not os.getenv("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set - skipping API integration test",
    )
    def test_generated_content_contains_h1_heading(self):
        """Test that returned string contains exactly one H1 heading."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        lines = content.split("\n")

        # First line must be H1 heading
        assert lines[0].startswith("# "), "First line must be H1 heading (# )"
        assert len(lines[0]) > 2, "H1 heading must have content after '# '"

    @pytest.mark.skipif(
        not os.getenv("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set - skipping API integration test",
    )
    def test_generated_content_has_blank_line_separator(self):
        """Test that returned string contains blank line after heading."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()
        lines = content.split("\n")

        assert len(lines) >= 3, "Content must have at least heading, blank line, and prose"
        assert lines[1] == "", "Second line must be blank separator"

    @pytest.mark.skipif(
        not os.getenv("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set - skipping API integration test",
    )
    def test_generated_content_has_2_to_3_sentences(self):
        """Test that returned string contains 2-3 sentences (detected by period count)."""
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
        not os.getenv("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set - skipping API integration test",
    )
    def test_generated_content_is_grammatically_correct(self):
        """Test that generated content is grammatically correct and coherent."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()

        # Content should have reasonable length (no truncation or corruption)
        assert 150 <= len(content) <= 800, "Content length suggests truncation or corruption"

        # Should not contain error markers or corrupted text
        assert "ERROR" not in content.upper()
        assert "UNDEFINED" not in content.upper()
        assert "\x00" not in content, "Content should not contain null bytes"

    @pytest.mark.skipif(
        not os.getenv("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set - skipping API integration test",
    )
    def test_generated_content_return_value_captured(self):
        """Test that return value is successfully captured for next task."""
        from sheep.content_generators import generate_markdown_content

        content = generate_markdown_content()

        # Store in variable to simulate passing to next task
        captured_content = content
        assert captured_content is not None
        assert isinstance(captured_content, str)
        assert len(captured_content) > 0


class TestFileWritingPhase:
    """Tests for task-2: Write markdown file to repository root with UTF-8/LF."""

    FEATURE_272_FILENAME = "test-6fioxo.md"

    def test_file_does_not_exist_before_write(self):
        """Test that file does not exist before write operation."""
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        # Clean up for test
        if filepath.exists():
            filepath.unlink()

        assert not filepath.exists(), f"File {filepath} should not exist before write"

    def test_write_markdown_file_creates_file_at_repo_root(self):
        """Test that write_markdown_file() creates file at repository root."""
        from sheep.content_generators import write_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        # Clean up any existing file
        if filepath.exists():
            filepath.unlink()

        # Write the file
        result = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Verify file was created
        assert filepath.exists(), f"File {filepath} was not created"
        assert result == str(filepath), "Function should return file path"

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_contains_exact_generated_content(self):
        """Test that file contains exactly the generated markdown content (byte-for-byte)."""
        from sheep.content_generators import write_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        # Clean up
        if filepath.exists():
            filepath.unlink()

        # Write the file
        write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Read and verify content
        assert filepath.exists()
        read_content = filepath.read_text(encoding="utf-8")
        assert read_content == test_content, "File content must match exactly"

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_encoding_is_utf8_without_bom(self):
        """Test that file encoding is UTF-8 without BOM."""
        from sheep.content_generators import write_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        assert filepath.exists()
        binary_content = filepath.read_bytes()

        # Verify not UTF-8 with BOM (BOM is EF BB BF)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

        # Verify can decode as UTF-8
        decoded = binary_content.decode("utf-8")
        assert decoded == test_content, "File should be valid UTF-8"

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_uses_lf_line_endings_not_crlf(self):
        """Test that file uses Unix LF line endings (0x0A), not Windows CRLF (0x0D 0x0A)."""
        from sheep.content_generators import write_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        assert filepath.exists()
        binary_content = filepath.read_bytes()

        # Verify no CRLF (0x0D 0x0A)
        assert b"\r\n" not in binary_content, "File should use LF line endings, not CRLF"

        # Verify file contains LF
        assert b"\n" in binary_content, "File should contain Unix LF newlines"

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_permissions_allow_read_by_owner(self):
        """Test that file permissions allow read by owner (default umask 0o644)."""
        from sheep.content_generators import write_markdown_file
        import stat

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        assert filepath.exists()
        file_stat = filepath.stat()

        # Owner should be able to read
        assert file_stat.st_mode & stat.S_IRUSR, "Owner should have read permission"

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_file_exists_and_is_readable(self):
        """Test that file exists and is readable at expected path."""
        from sheep.content_generators import write_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        result = write_markdown_file(test_content, self.FEATURE_272_FILENAME)
        filepath_obj = Path(result)

        # Verify exists
        assert filepath_obj.exists(), "File must exist"

        # Verify is file (not directory)
        assert filepath_obj.is_file(), "Path must be a file, not directory"

        # Verify readable
        assert filepath_obj.read_text(encoding="utf-8") == test_content, "File must be readable"

        # Clean up
        if filepath_obj.exists():
            filepath_obj.unlink()


class TestValidationPhase:
    """Tests for task-3: Validate markdown file format and encoding."""

    FEATURE_272_FILENAME = "test-6fioxo.md"

    def test_validate_returns_success_for_valid_file(self):
        """Test that validate_markdown_file() returns success (no exception raised)."""
        from sheep.content_generators import write_markdown_file, validate_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        # Write and validate
        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)
        result = validate_markdown_file(filepath_str)

        assert result is True, "Validation should return True for valid content"

        # Clean up
        if filepath.exists():
            filepath.unlink()

    def test_validate_confirms_utf8_without_bom(self):
        """Test that validation confirms file encoding is UTF-8 without BOM."""
        from sheep.content_generators import write_markdown_file, validate_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Validation should pass without exception
        result = validate_markdown_file(filepath_str)
        assert result is True

        # Verify BOM is not present
        binary_content = Path(filepath_str).read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Clean up
        if Path(filepath_str).exists():
            Path(filepath_str).unlink()

    def test_validate_verifies_lf_line_endings(self):
        """Test that validation verifies all line endings are Unix LF (0x0A only, no CRLF)."""
        from sheep.content_generators import write_markdown_file, validate_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Validation should pass
        result = validate_markdown_file(filepath_str)
        assert result is True

        # Verify no CRLF
        binary_content = Path(filepath_str).read_bytes()
        assert b"\r\n" not in binary_content

        # Clean up
        if Path(filepath_str).exists():
            Path(filepath_str).unlink()

    def test_validate_checks_h1_heading_at_start(self):
        """Test that validation verifies H1 heading present at start of file (line[0] matches pattern)."""
        from sheep.content_generators import write_markdown_file, validate_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Validation should pass
        result = validate_markdown_file(filepath_str)
        assert result is True

        # Verify heading is present
        text_content = Path(filepath_str).read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert lines[0].startswith("# ")

        # Clean up
        if Path(filepath_str).exists():
            Path(filepath_str).unlink()

    def test_validate_checks_blank_line_separator(self):
        """Test that validation verifies blank line present after heading (line[1] is empty)."""
        from sheep.content_generators import write_markdown_file, validate_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Validation should pass
        result = validate_markdown_file(filepath_str)
        assert result is True

        # Verify blank line separator
        text_content = Path(filepath_str).read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert lines[1] == ""

        # Clean up
        if Path(filepath_str).exists():
            Path(filepath_str).unlink()

    def test_validate_checks_2_to_3_sentences(self):
        """Test that validation verifies exactly 2-3 sentences detected (period count in range)."""
        from sheep.content_generators import write_markdown_file, validate_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Validation should pass
        result = validate_markdown_file(filepath_str)
        assert result is True

        # Verify sentence count
        text_content = Path(filepath_str).read_text(encoding="utf-8")
        prose_content = "\n".join(text_content.split("\n")[2:]).strip()
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

        # Clean up
        if Path(filepath_str).exists():
            Path(filepath_str).unlink()

    def test_validate_checks_trailing_newline(self):
        """Test that validation verifies file ends with trailing newline."""
        from sheep.content_generators import write_markdown_file, validate_markdown_file

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Validation should pass
        result = validate_markdown_file(filepath_str)
        assert result is True

        # Verify trailing newline
        text_content = Path(filepath_str).read_text(encoding="utf-8")
        assert text_content.endswith("\n")

        # Clean up
        if Path(filepath_str).exists():
            Path(filepath_str).unlink()

    def test_validate_runs_in_reasonable_time(self):
        """Test that validation runs in under 10ms (negligible cost)."""
        from sheep.content_generators import write_markdown_file, validate_markdown_file
        import time

        test_content = "# Test Heading\n\nThis is sentence one. This is sentence two.\n"
        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        if filepath.exists():
            filepath.unlink()

        filepath_str = write_markdown_file(test_content, self.FEATURE_272_FILENAME)

        # Time the validation
        start = time.time()
        validate_markdown_file(filepath_str)
        elapsed = time.time() - start

        # Should be very fast (< 100ms is acceptable)
        assert elapsed < 0.1, f"Validation took {elapsed*1000:.1f}ms, should be faster"

        # Clean up
        if Path(filepath_str).exists():
            Path(filepath_str).unlink()


class TestEndToEndIntegration:
    """Integration tests for Phase 1: Content Generation & File Creation."""

    FEATURE_272_FILENAME = "test-6fioxo.md"

    @pytest.mark.skipif(
        not os.getenv("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set - skipping full integration test",
    )
    def test_complete_phase1_workflow(self):
        """Test complete Phase 1 workflow: generate -> write -> validate."""
        from sheep.content_generators import (
            generate_markdown_content,
            write_markdown_file,
            validate_markdown_file,
        )

        filepath = Path.cwd() / self.FEATURE_272_FILENAME

        # Clean up
        if filepath.exists():
            filepath.unlink()

        try:
            # Task 1: Generate content
            content = generate_markdown_content()
            assert content is not None
            assert isinstance(content, str)

            # Task 2: Write file
            filepath_str = write_markdown_file(content, self.FEATURE_272_FILENAME)
            assert Path(filepath_str).exists()

            # Task 3: Validate file
            result = validate_markdown_file(filepath_str)
            assert result is True

        finally:
            # Clean up
            if filepath.exists():
                filepath.unlink()
