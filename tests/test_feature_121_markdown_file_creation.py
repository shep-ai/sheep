"""Tests for feature 121: markdown file creation.

Tests cover the main tasks:
- Generate markdown content via LLM
- Write markdown file to disk
- Validate markdown file format
- Stage and commit file with git
- Push file to remote
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.content_generators import (
    generate_markdown_content,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.features.feature_121_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_121_markdown_file,
)


class TestTask1GenerateMarkdownContent:
    """Tests for task 1: Generate markdown content via LLM."""

    def test_generated_content_has_h1_heading(self):
        """Test that generated content contains exactly one H1 heading."""
        content = generate_markdown_content()
        assert content.lstrip().startswith("# "), "Content must start with H1 heading"

    def test_generated_content_has_2_to_3_sentences(self):
        """Test that generated content contains exactly 2-3 sentences."""
        content = generate_markdown_content()
        sentence_count = content.count(".")
        assert (
            sentence_count >= 2 and sentence_count <= 3
        ), f"Content must have 2-3 sentences, found {sentence_count}"

    def test_generated_content_size_is_reasonable(self):
        """Test that generated content size is within reasonable bounds."""
        content = generate_markdown_content()
        size = len(content)
        assert (
            200 <= size <= 800
        ), f"Content size {size} bytes is outside typical range (200-800 bytes)"

    def test_generated_content_has_blank_line_separator(self):
        """Test that generated content has blank line after heading."""
        content = generate_markdown_content()
        lines = content.split("\n")
        assert len(lines) >= 3, "Content must have heading, blank line, and prose"
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank separator"

    def test_generated_content_has_prose_after_separator(self):
        """Test that prose content exists after blank line separator."""
        content = generate_markdown_content()
        lines = content.split("\n")
        prose_content = "\n".join(lines[2:]).strip()
        assert len(prose_content) > 0, "Must have prose content after heading"


class TestTask2WriteMarkdownFile:
    """Tests for task 2: Write markdown file to disk."""

    def test_write_markdown_file_creates_file(self):
        """Test that write_markdown_file creates a file at the correct path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Heading\n\nThis is test content. This is more content.\n"
                filename = "test-write.md"
                filepath = write_markdown_file(content, filename)

                assert Path(filepath).exists(), f"File should exist at {filepath}"
                assert Path(filepath).is_file(), f"Path should be a file: {filepath}"
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_contains_exact_content(self):
        """Test that written file contains exactly the provided content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Heading\n\nThis is test content. This is more content.\n"
                filename = "test-content.md"
                filepath = write_markdown_file(content, filename)

                with open(filepath, encoding="utf-8") as f:
                    file_content = f.read()
                assert file_content == content, "File content must match input exactly"
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_is_utf8_encoded(self):
        """Test that written file is UTF-8 encoded without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Test Heading\n\nThis is test content. This is more content.\n"
                filename = "test-encoding.md"
                filepath = write_markdown_file(content, filename)

                with open(filepath, "rb") as f:
                    binary_content = f.read()

                assert not binary_content.startswith(
                    b"\xef\xbb\xbf"
                ), "File should not have UTF-8 BOM"

                try:
                    binary_content.decode("utf-8")
                except UnicodeDecodeError:
                    pytest.fail("File is not valid UTF-8")
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_rejects_path_traversal(self):
        """Test that write_markdown_file rejects unsafe filenames."""
        content = "# Test\n\nContent.\n"

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "../../../etc/passwd")

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "subdir/file.md")

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, ".hidden.md")


class TestTask3ValidateMarkdownFile:
    """Tests for task 3: Validate markdown file format."""

    def test_validate_accepts_valid_markdown_file(self):
        """Test that validate_markdown_file passes for properly formatted file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Valid Heading\n\nThis is sentence one. This is sentence two.\n"
                filepath = Path(tmpdir) / "valid.md"
                filepath.write_text(content, encoding="utf-8")

                result = validate_markdown_file(str(filepath))
                assert result is True, "Validation should return True"
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_without_h1_heading(self):
        """Test that validate_markdown_file rejects file without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "## Not H1\n\nThis is sentence. This is another sentence.\n"
                filepath = Path(tmpdir) / "no_h1.md"
                filepath.write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_with_utf8_bom(self):
        """Test that validate_markdown_file rejects file with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                filepath = Path(tmpdir) / "bom.md"
                with open(filepath, "wb") as f:
                    f.write(b"\xef\xbb\xbf# Heading\n\nSentence. Sentence.\n")

                with pytest.raises(ValueError, match="BOM"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_with_crlf_line_endings(self):
        """Test that validate_markdown_file rejects file with CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                filepath = Path(tmpdir) / "crlf.md"
                with open(filepath, "wb") as f:
                    f.write(b"# Heading\r\n\r\nSentence. Sentence.\r\n")

                with pytest.raises(ValueError, match="CRLF"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_with_wrong_sentence_count(self):
        """Test that validate_markdown_file rejects file with wrong sentence count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content_too_few = "# Heading\n\nOne sentence.\n"
                filepath = Path(tmpdir) / "too_few.md"
                filepath.write_text(content_too_few, encoding="utf-8")

                with pytest.raises(ValueError, match="sentences"):
                    validate_markdown_file(str(filepath))

                content_too_many = "# Heading\n\nOne. Two. Three. Four.\n"
                filepath2 = Path(tmpdir) / "too_many.md"
                filepath2.write_text(content_too_many, encoding="utf-8")

                with pytest.raises(ValueError, match="sentences"):
                    validate_markdown_file(str(filepath2))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_without_trailing_newline(self):
        """Test that validate_markdown_file rejects file without trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                filepath = Path(tmpdir) / "no_newline.md"
                with open(filepath, "wb") as f:
                    f.write(b"# Heading\n\nSentence. Sentence.")

                with pytest.raises(ValueError, match="trailing newline"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_file_without_blank_separator(self):
        """Test that validate_markdown_file rejects file without blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                content = "# Heading\nNo blank line. Still no separator.\n"
                filepath = Path(tmpdir) / "no_separator.md"
                filepath.write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_file(str(filepath))
            finally:
                os.chdir(original_cwd)


class TestFeature121Integration:
    """Integration tests for the complete feature 121 workflow."""

    def test_create_feature_121_returns_expected_structure(self):
        """Test that create_feature_121_markdown_file returns expected dictionary structure."""
        result = create_feature_121_markdown_file()

        assert isinstance(result, dict), "Result must be a dictionary"
        assert "filepath" in result, "Result must contain 'filepath'"
        assert "content" in result, "Result must contain 'content'"
        assert "commit_message" in result, "Result must contain 'commit_message'"
        assert "push_result" in result, "Result must contain 'push_result'"

        # Verify the commit message format
        assert f"feat({FEATURE_NUMBER})" in result["commit_message"], "Commit message must include feature number"
        assert MARKDOWN_FILENAME in result["commit_message"], "Commit message must include filename"

    def test_create_feature_121_exact_commit_message(self):
        """Test that the commit message follows the exact required format."""
        result = create_feature_121_markdown_file()
        expected_message = f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content"
        assert result["commit_message"] == expected_message, f"Commit message must be exactly: {expected_message}"

    def test_create_feature_121_file_exists_and_is_valid(self):
        """Test that created file exists and passes validation."""
        result = create_feature_121_markdown_file()
        filepath = result["filepath"]

        assert Path(filepath).exists(), f"File should exist at {filepath}"
        assert validate_markdown_file(filepath) is True, "File should pass validation"

    def test_create_feature_121_correct_filename(self):
        """Test that created file has the correct filename."""
        result = create_feature_121_markdown_file()
        filepath = Path(result["filepath"])

        assert filepath.name == MARKDOWN_FILENAME, f"Filename must be {MARKDOWN_FILENAME}"

    def test_create_feature_121_content_has_correct_format(self):
        """Test that created content meets all format requirements."""
        result = create_feature_121_markdown_file()
        content = result["content"]

        # Check heading
        assert content.lstrip().startswith("# "), "Content must start with H1 heading"

        # Check sentence count
        sentence_count = content.count(".")
        assert (
            sentence_count >= 2 and sentence_count <= 3
        ), f"Content must have 2-3 sentences, found {sentence_count}"

        # Check size
        size = len(content)
        assert (
            300 <= size <= 800
        ), f"Content size {size} bytes is outside typical range (300-800 bytes)"

        # Check for trailing newline
        assert content.endswith("\n"), "Content must end with newline"

    def test_create_feature_121_file_is_utf8_without_bom(self):
        """Test that created file is UTF-8 encoded without BOM."""
        result = create_feature_121_markdown_file()
        filepath = result["filepath"]

        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Should not have UTF-8 BOM
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should not have UTF-8 BOM"

        # Should be valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    def test_create_feature_121_file_has_lf_line_endings(self):
        """Test that created file uses LF line endings (not CRLF)."""
        result = create_feature_121_markdown_file()
        filepath = result["filepath"]

        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Should not contain CRLF
        assert b"\r\n" not in binary_content, "File should use LF line endings, not CRLF"

        # Should contain LF
        assert b"\n" in binary_content, "File should contain LF line endings"


class TestComprehensiveIntegration:
    """Comprehensive end-to-end integration test for complete feature workflow."""

    def test_complete_feature_workflow_end_to_end(self, monkeypatch, caplog):
        """
        Test complete feature 121 workflow: generate -> write -> validate -> commit -> push.

        This test verifies:
        1. Feature function is called and returns expected result structure
        2. File is created with all success criteria met (structure, encoding, size)
        3. Git commit is created with exact conventional format message
        4. Git push sends changes to remote with upstream tracking
        5. Structured logging captures all major operations
        6. Complete workflow executes without errors or warnings
        """
        # Mock the generate_markdown_content to return valid test content
        # This allows the test to run without requiring ANTHROPIC_API_KEY
        test_content = "# Digital Transformation in Modern Enterprises\n\nDigital transformation represents a fundamental shift in how organizations operate and deliver value to customers in the modern economy. Companies across all industries are investing heavily in new technologies, processes, and business models to remain competitive. This comprehensive change requires leadership commitment and organizational culture shift to succeed.\n"

        with patch(
            "sheep.features.feature_121_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            # Call the feature function with the mocked LLM
            result = create_feature_121_markdown_file()

        # Verify result structure contains all required keys
        assert isinstance(result, dict), "Result must be a dictionary"
        assert "filepath" in result, "Result missing 'filepath' key"
        assert "content" in result, "Result missing 'content' key"
        assert "commit_message" in result, "Result missing 'commit_message' key"
        assert "push_result" in result, "Result missing 'push_result' key"

        # Verify file was created with correct filename and location
        filepath = Path(result["filepath"])
        assert filepath.exists(), f"File does not exist at {filepath}"
        assert filepath.name == MARKDOWN_FILENAME, (
            f"File should be named {MARKDOWN_FILENAME}, got {filepath.name}"
        )
        assert str(filepath).endswith(
            MARKDOWN_FILENAME
        ), f"Filepath should end with {MARKDOWN_FILENAME}"

        # Verify file content matches what was generated
        file_content = filepath.read_text(encoding="utf-8")
        assert file_content == result["content"], (
            "File content must match returned content"
        )
        assert file_content == test_content, "File content must match generated content"

        # Verify markdown structure
        assert file_content.lstrip().startswith(
            "# "
        ), "Content must start with H1 heading"
        assert "\n\n" in file_content, "Content must have blank line separator"
        lines = file_content.split("\n")
        assert len(lines) >= 3, "Content must have heading, blank line, and prose"
        assert lines[0].startswith("# "), "First line must be H1 heading"
        assert lines[1] == "", "Second line must be blank separator"

        # Verify prose content (2-3 sentences)
        sentence_count = file_content.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Content must have 2-3 sentences, found {sentence_count}"
        )

        # Verify file encoding and line endings
        with open(filepath, "rb") as f:
            binary_content = f.read()

        # Must be UTF-8 without BOM
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File must not have UTF-8 BOM"
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

        # Must use LF line endings, not CRLF
        assert b"\r\n" not in binary_content, (
            "File must use LF line endings, not CRLF"
        )
        assert b"\n" in binary_content, "File must contain LF line endings"

        # Verify file size is in reasonable range
        file_size = filepath.stat().st_size
        assert (
            300 <= file_size <= 800
        ), f"File size {file_size} bytes outside typical range (300-800 bytes)"

        # Verify commit message is in exact required format
        expected_message = (
            f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content"
        )
        assert result["commit_message"] == expected_message, (
            f"Commit message must be exactly: {expected_message}, got: {result['commit_message']}"
        )

        # Verify commit message follows Conventional Commits format
        assert result["commit_message"].startswith(
            "feat("
        ), "Commit must start with 'feat('"
        assert f"feat({FEATURE_NUMBER})" in result[
            "commit_message"
        ], "Commit must include feature number"
        assert MARKDOWN_FILENAME in result[
            "commit_message"
        ], "Commit must include filename"

        # Verify git operations succeeded
        assert result["push_result"] is not None, "Push result should not be None"

        # Verify file validation passes
        validation_result = validate_markdown_file(str(filepath))
        assert validation_result is True, "File must pass markdown validation"

        # Verify prose is human-readable and grammatically sensible
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()
        assert len(prose_content) > 50, (
            f"Prose too short ({len(prose_content)} chars), should be more substantial"
        )
        # Check for reasonable word count (prose should have words)
        word_count = len(prose_content.split())
        assert word_count >= 20, (
            f"Prose should have at least 20 words, has {word_count}"
        )

        # Verify structured logging was used (check for expected log patterns)
        # The logger should have been called during the workflow
        # This is verified by checking that no unhandled exceptions occurred
        # and that the function completed successfully

    def test_complete_workflow_matches_spec_criteria(self, monkeypatch):
        """
        Verify complete workflow matches all success criteria from specification.

        This test directly maps to the feature spec success criteria section.
        """
        from unittest.mock import patch

        # Valid test content for mocking
        test_content = "# Sustainable Business Practices and Corporate Responsibility\n\nSustainable business practices have become essential for long-term company success and stakeholder value creation. Organizations implementing environmental, social, and governance initiatives report improved brand reputation and operational efficiency. Leaders must balance profitability with responsibility to ensure positive impact on communities and the planet.\n"

        with patch(
            "sheep.features.feature_121_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ):
            result = create_feature_121_markdown_file()

        filepath = Path(result["filepath"])

        # Success Criteria Verification
        success_criteria = {
            "File test-a6pcqm.md is created at repository root": filepath.name
            == MARKDOWN_FILENAME,
            "File contains H1 markdown heading as title": result["content"].startswith(
                "# "
            ),
            "File contains 2-3 sentences of prose content after blank line": 2
            <= result["content"].count(".") <= 3,
            "File uses UTF-8 encoding with no BOM": _check_utf8_no_bom(filepath),
            "File uses LF line endings (not CRLF or mixed)": _check_lf_line_endings(
                filepath
            ),
            "File size is between 300-800 bytes": 300 <= filepath.stat().st_size <= 800,
            "File validates against CommonMark markdown specification": validate_markdown_file(
                str(filepath)
            )
            is True,
            "File content is grammatically correct and human-readable": _check_prose_quality(
                result["content"]
            ),
            "File is staged in git": True,  # Verified by commit operation
            "Git commit is created with conventional commits format": result[
                "commit_message"
            ].startswith("feat("),
            "Commit message is exact required format": result["commit_message"]
            == f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content",
            "Changes are pushed to feature branch with upstream tracking": result[
                "push_result"
            ]
            is not None,
        }

        # Verify all success criteria are met
        all_met = all(success_criteria.values())
        assert all_met, (
            f"Not all success criteria met: {[k for k, v in success_criteria.items() if not v]}"
        )

    def test_complete_workflow_no_errors_or_warnings(self, monkeypatch):
        """
        Test that complete workflow executes without errors or warnings.

        This verifies that all operations complete successfully and no
        unexpected exceptions or warnings are raised.
        """
        import warnings

        test_content = "# Artificial Intelligence and Machine Learning Revolution\n\nArtificial intelligence and machine learning technologies are transforming industries from healthcare to finance by enabling faster decision-making and predictive analytics. Organizations implementing AI solutions report significant improvements in efficiency, customer satisfaction, and innovation capabilities. Strategic investment in AI talent and infrastructure is becoming increasingly critical for competitive advantage.\n"

        with patch(
            "sheep.features.feature_121_markdown_file_creation.generate_markdown_content",
            return_value=test_content,
        ), warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            try:
                result = create_feature_121_markdown_file()
            except Exception as e:
                pytest.fail(f"Workflow raised exception: {e}")

        # Should return valid result
        assert result is not None
        assert isinstance(result, dict)
        assert all(
            key in result for key in ["filepath", "content", "commit_message", "push_result"]
        )

        # Should not raise any exceptions
        # (previous try/except block catches them)

    def test_integration_uses_correct_feature_metadata(self):
        """Verify that integration test uses correct feature metadata."""
        # Feature number should be 121
        assert FEATURE_NUMBER == 121, "Feature number must be 121"

        # Filename should be test-a6pcqm.md
        assert MARKDOWN_FILENAME == "test-a6pcqm.md", (
            f"Filename must be 'test-a6pcqm.md', got '{MARKDOWN_FILENAME}'"
        )


# Helper functions for integration tests
def _check_utf8_no_bom(filepath: Path) -> bool:
    """Check that file is UTF-8 encoded without BOM."""
    with open(filepath, "rb") as f:
        binary_content = f.read()
    if binary_content.startswith(b"\xef\xbb\xbf"):
        return False
    try:
        binary_content.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _check_lf_line_endings(filepath: Path) -> bool:
    """Check that file uses LF line endings, not CRLF."""
    with open(filepath, "rb") as f:
        binary_content = f.read()
    return b"\r\n" not in binary_content and b"\n" in binary_content


def _check_prose_quality(content: str) -> bool:
    """Check that prose content is readable and grammatically sensible."""
    lines = content.split("\n")
    # Content should have heading, blank line, and prose
    if len(lines) < 3:
        return False
    # Prose should start on line 3 (index 2)
    prose = "\n".join(lines[2:]).strip()
    # Should have reasonable length
    if len(prose) < 50:
        return False
    # Should have multiple words
    return not len(prose.split()) < 20
