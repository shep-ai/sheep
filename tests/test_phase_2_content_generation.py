"""Tests for phase 2: Content Generation & File Operations for feature 239.

Tests the three main tasks:
1. Markdown content generation via CrewAI (task-2-1)
2. File writing with UTF-8 encoding and proper line endings (task-2-2)
3. CommonMark validation logic (task-2-3)
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

# Add src to path to enable imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


class TestTask21ContentGeneration:
    """Task 2-1: Implement markdown content generation via CrewAI."""

    def test_generate_markdown_content_returns_string(self):
        """Generated content should be a non-empty string."""
        from sheep.content_generators import generate_markdown_content

        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm_factory:
            # Mock the LLM call to return valid markdown
            mock_llm = mock.MagicMock()
            mock_llm.call.return_value = {
                "content": "# Test Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"
            }
            mock_llm_factory.return_value = mock_llm

            content = generate_markdown_content()

            assert isinstance(content, str)
            assert len(content) > 0

    def test_generate_markdown_content_contains_h1_heading(self):
        """Generated content must contain H1 heading (# format)."""
        from sheep.content_generators import generate_markdown_content

        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm_factory:
            mock_llm = mock.MagicMock()
            mock_llm.call.return_value = {
                "content": "# Example Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            }
            mock_llm_factory.return_value = mock_llm

            content = generate_markdown_content()

            assert content.startswith("# ")
            assert "# " in content

    def test_generate_markdown_content_has_prose_with_sentences(self):
        """Generated content must contain 2-3 sentences after the H1 heading."""
        from sheep.content_generators import generate_markdown_content

        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm_factory:
            mock_llm = mock.MagicMock()
            mock_llm.call.return_value = {
                "content": "# Title\n\nSentence one. Sentence two. Sentence three.\n"
            }
            mock_llm_factory.return_value = mock_llm

            content = generate_markdown_content()

            # Count sentences (periods)
            period_count = content.count(".")
            assert 2 <= period_count <= 3

    def test_generate_markdown_content_has_trailing_newline(self):
        """Generated content must end with trailing newline."""
        from sheep.content_generators import generate_markdown_content

        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm_factory:
            mock_llm = mock.MagicMock()
            mock_llm.call.return_value = {
                "content": "# Example Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence."
            }
            mock_llm_factory.return_value = mock_llm

            content = generate_markdown_content()

            assert content.endswith("\n")

    def test_generate_markdown_content_uses_crewtai_llm(self):
        """Content generation should use CrewAI LLM framework."""
        from sheep.content_generators import generate_markdown_content

        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm_factory:
            mock_llm = mock.MagicMock()
            mock_llm.call.return_value = {
                "content": "# Important Test Topic\n\nThis is the first sentence about the topic. This is the second sentence providing details. This is the third sentence concluding the thought.\n"
            }
            mock_llm_factory.return_value = mock_llm

            content = generate_markdown_content()

            # Verify get_reasoning_llm was called
            mock_llm_factory.assert_called_once()
            # Verify llm.call was invoked
            mock_llm.call.assert_called_once()

    def test_generate_markdown_content_returns_valid_utf8(self):
        """Generated content should be valid UTF-8."""
        from sheep.content_generators import generate_markdown_content

        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm_factory:
            mock_llm = mock.MagicMock()
            mock_llm.call.return_value = {
                "content": "# UTF-8 Encoding Test\n\nThis content should be valid UTF-8 encoded text. All characters should be properly represented. The encoding validates successfully.\n"
            }
            mock_llm_factory.return_value = mock_llm

            content = generate_markdown_content()

            # Should be encodable/decodable as UTF-8
            content_bytes = content.encode("utf-8")
            decoded = content_bytes.decode("utf-8")
            assert decoded == content


class TestTask22FileWriting:
    """Task 2-2: Implement file writing with UTF-8 encoding and validation."""

    def test_write_markdown_file_creates_file(self):
        """File should be created at repository root."""
        from sheep.content_generators import write_markdown_file

        content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-abc123.md")

                assert Path(filepath).exists()
                assert Path(filepath).is_file()
                assert filepath.endswith("test-abc123.md")
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_uses_utf8_encoding(self):
        """File should be written with UTF-8 encoding without BOM."""
        from sheep.content_generators import write_markdown_file

        content = "# Title\n\nContent. More. Done.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-xyz789.md")

                with open(filepath, "rb") as f:
                    binary_content = f.read()

                # Check for UTF-8 BOM (should NOT be present)
                assert not binary_content.startswith(b"\xef\xbb\xbf")

                # Should be valid UTF-8
                decoded = binary_content.decode("utf-8")
                assert decoded == content
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_uses_lf_line_endings(self):
        """File should use Unix LF line endings, not CRLF."""
        from sheep.content_generators import write_markdown_file

        content = "# Title\n\nFirst. Second. Third.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-lf-test.md")

                with open(filepath, "rb") as f:
                    binary_content = f.read()

                # Should NOT contain CRLF
                assert b"\r\n" not in binary_content
                # Should contain LF
                assert b"\n" in binary_content
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_returns_filepath(self):
        """Function should return the filepath as a string."""
        from sheep.content_generators import write_markdown_file

        content = "# Test\n\nOne. Two. Three.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-return.md")

                assert isinstance(filepath, str)
                assert len(filepath) > 0
                assert filepath.endswith("test-return.md")
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_has_correct_content(self):
        """File content should match the input content exactly."""
        from sheep.content_generators import write_markdown_file

        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-content.md")

                with open(filepath, "r", encoding="utf-8") as f:
                    written_content = f.read()

                assert written_content == content
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_size_in_valid_range(self):
        """File size should be reasonable for valid H1 + 2-3 sentences."""
        from sheep.content_generators import write_markdown_file

        # Longer, more realistic content
        content = "# The Importance of Markdown Documentation\n\nMarkdown has become the standard format for documenting software projects and writing technical content across the internet. Its simplicity combined with powerful formatting capabilities makes it ideal for creating readable documents that work well in both human and machine-readable formats. By using consistent markdown structure with proper headings and clean prose, teams can maintain documentation that is easy to understand and maintain over time.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-size.md")

                file_size = Path(filepath).stat().st_size
                assert file_size > 150, f"File size {file_size} should be reasonable"
            finally:
                os.chdir(original_cwd)

    def test_write_markdown_file_rejects_invalid_filename(self):
        """Should reject filenames with path traversal attempts."""
        from sheep.content_generators import write_markdown_file

        content = "# Title\n\nContent. More. Done.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Try path traversal
                try:
                    write_markdown_file(content, "../test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "Invalid filename" in str(e)
            finally:
                os.chdir(original_cwd)


class TestTask23Validation:
    """Task 2-3: Implement CommonMark validation logic."""

    def test_validate_markdown_file_accepts_valid_file(self):
        """Should accept files that meet all requirements."""
        from sheep.content_generators import validate_markdown_file, write_markdown_file

        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-valid.md")

                # Should not raise
                result = validate_markdown_file(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_missing_h1_heading(self):
        """Should reject files without H1 heading."""
        from sheep.content_generators import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write file without H1
                filepath = Path("test-no-h1.md")
                filepath.write_text("No heading. Just. Text.\n", encoding="utf-8", newline="")

                try:
                    validate_markdown_file(str(filepath))
                    assert False, "Should have raised ValueError"
                except (ValueError, OSError) as e:
                    assert "H1" in str(e) or "heading" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_wrong_sentence_count(self):
        """Should reject files with wrong number of sentences."""
        from sheep.content_generators import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Only 1 sentence
                filepath = Path("test-one-sentence.md")
                filepath.write_text("# Title\n\nJust one.\n", encoding="utf-8", newline="")

                try:
                    validate_markdown_file(str(filepath))
                    assert False, "Should have raised ValueError"
                except (ValueError, OSError) as e:
                    assert "sentence" in str(e).lower() or "period" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_crlf_line_endings(self):
        """Should reject files with CRLF line endings."""
        from sheep.content_generators import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write with CRLF manually
                filepath = Path("test-crlf.md")
                content = "# Title\r\n\r\nFirst. Second. Third.\r\n"
                filepath.write_bytes(content.encode("utf-8"))

                try:
                    validate_markdown_file(str(filepath))
                    assert False, "Should have raised ValueError"
                except (ValueError, OSError) as e:
                    assert "CRLF" in str(e) or "line ending" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_utf8_bom(self):
        """Should reject files with UTF-8 BOM."""
        from sheep.content_generators import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write with UTF-8 BOM manually
                filepath = Path("test-bom.md")
                content = "# Title\n\nFirst. Second. Third.\n"
                filepath.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))

                try:
                    validate_markdown_file(str(filepath))
                    assert False, "Should have raised ValueError"
                except (ValueError, OSError) as e:
                    assert "BOM" in str(e) or "encoding" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_requires_blank_line_after_heading(self):
        """Should require blank line separator after H1 heading."""
        from sheep.content_generators import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # No blank line after heading
                filepath = Path("test-no-blank.md")
                filepath.write_text("# Title\nFirst. Second. Third.\n", encoding="utf-8", newline="")

                try:
                    validate_markdown_file(str(filepath))
                    assert False, "Should have raised ValueError"
                except (ValueError, OSError) as e:
                    assert "blank" in str(e).lower() or "separator" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_requires_trailing_newline(self):
        """Should require file to end with trailing newline."""
        from sheep.content_generators import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # No trailing newline
                filepath = Path("test-no-trailing.md")
                filepath.write_bytes(b"# Title\n\nFirst. Second. Third.")

                try:
                    validate_markdown_file(str(filepath))
                    assert False, "Should have raised ValueError"
                except (ValueError, OSError) as e:
                    assert "newline" in str(e).lower()
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_checks_file_size(self):
        """File size should be reasonable for valid content."""
        from sheep.content_generators import validate_markdown_file, write_markdown_file

        # Longer, more realistic content
        content = "# The Importance of Markdown Documentation\n\nMarkdown has become the standard format for documenting software projects and writing technical content across the internet. Its simplicity combined with powerful formatting capabilities makes it ideal for creating readable documents that work well in both human and machine-readable formats. By using consistent markdown structure with proper headings and clean prose, teams can maintain documentation that is easy to understand and maintain over time.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-size.md")

                # Validation should pass
                file_size = Path(filepath).stat().st_size
                validate_markdown_file(filepath)

                assert file_size > 150
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_nonexistent_file(self):
        """Should reject if file doesn't exist."""
        from sheep.content_generators import validate_markdown_file

        try:
            validate_markdown_file("/nonexistent/path/file.md")
            assert False, "Should have raised OSError"
        except (ValueError, OSError) as e:
            assert "not exist" in str(e).lower() or "no such" in str(e).lower()


class TestPhase2Integration:
    """Integration tests combining all three tasks."""

    def test_generate_write_validate_workflow(self):
        """Complete workflow: generate → write → validate."""
        from sheep.content_generators import (
            generate_markdown_content,
            write_markdown_file,
            validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm_factory:
                    mock_llm = mock.MagicMock()
                    mock_llm.call.return_value = {
                        "content": "# Important Topic\n\nThis is the first sentence. This is the second sentence. This is the third sentence.\n"
                    }
                    mock_llm_factory.return_value = mock_llm

                    # Task 2-1: Generate
                    content = generate_markdown_content()
                    assert len(content) > 0

                    # Task 2-2: Write
                    filepath = write_markdown_file(content, "test-workflow.md")
                    assert Path(filepath).exists()

                    # Task 2-3: Validate
                    result = validate_markdown_file(filepath)
                    assert result is True
            finally:
                os.chdir(original_cwd)
