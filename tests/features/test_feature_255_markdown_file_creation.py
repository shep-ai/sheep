"""Tests for feature 255: Create markdown file test-i3iccc.md.

Tests cover:
- Content generation with valid markdown structure
- Validation of H1 heading, blank line, sentence count
- Error handling for invalid content
- File writing with UTF-8 encoding and LF line endings
- File verification for encoding, line endings, and structure
- Complete phases 1-2 orchestration (generate + validate + write + verify)
"""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from sheep.features.feature_255_markdown_file_creation import (
    BRANCH_NAME,
    COMMIT_MESSAGE_TEMPLATE,
    FEATURE_NUMBER,
    FILENAME,
    generate_content,
    run,
    validate_content,
    write_file,
    verify_file,
)


class TestModuleConstants:
    """Tests for module-level constants."""

    def test_filename_constant(self):
        """Test FILENAME constant has correct value."""
        assert FILENAME == "test-i3iccc.md"

    def test_feature_number_constant(self):
        """Test FEATURE_NUMBER constant has correct value."""
        assert FEATURE_NUMBER == 255

    def test_branch_name_constant(self):
        """Test BRANCH_NAME constant has correct value."""
        assert BRANCH_NAME == "feat/255-markdown-file-creation-17ca12"

    def test_commit_message_template(self):
        """Test COMMIT_MESSAGE_TEMPLATE has correct format."""
        assert "feat(255)" in COMMIT_MESSAGE_TEMPLATE
        assert "test-i3iccc.md" in COMMIT_MESSAGE_TEMPLATE


class TestGenerateContent:
    """Tests for content generation functionality."""

    def test_generate_content_returns_string(self):
        """Test that generate_content returns a string."""
        mock_content = "# Test Title\n\nThis is test content. This is more content. Final sentence."
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            result = generate_content()
            assert isinstance(result, str)
            assert len(result) > 0

    def test_generate_content_calls_content_generators(self):
        """Test that generate_content calls content_generators.generate_markdown_content()."""
        mock_content = "# Title\n\nSentence one. Sentence two. Sentence three."
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content) as mock_gen:
            result = generate_content()
            mock_gen.assert_called_once()
            assert result == mock_content

    def test_generate_content_returns_valid_markdown(self):
        """Test that generated content is valid markdown."""
        mock_content = "# Understanding APIs\n\nAPIs enable communication between software systems. They define the methods and data formats for requests. This makes integration seamless and efficient.\n"
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            result = generate_content()
            assert result.startswith("# ")
            assert "\n\n" in result
            assert "." in result

    def test_generate_content_handles_api_failure(self):
        """Test that generate_content propagates API failures."""
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   side_effect=ValueError("API call failed")), \
             pytest.raises(ValueError, match="API call failed"):
            generate_content()

    def test_generate_content_handles_network_error(self):
        """Test that generate_content handles network errors."""
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   side_effect=Exception("Network timeout")), \
             pytest.raises(Exception, match="Network timeout"):
            generate_content()


class TestValidateContent:
    """Tests for content validation functionality."""

    def test_validate_content_with_valid_markdown(self):
        """Test validate_content with valid markdown."""
        valid_content = "# Cloud Computing\n\nCloud computing provides on-demand computing resources. Organizations benefit from scalability and cost efficiency. This technology transforms infrastructure management.\n"
        # Should not raise
        validate_content(valid_content)

    def test_validate_content_two_sentences(self):
        """Test validate_content accepts exactly 2 sentences."""
        content = "# Title\n\nFirst sentence. Second sentence.\n"
        # Should not raise
        validate_content(content)

    def test_validate_content_three_sentences(self):
        """Test validate_content accepts exactly 3 sentences."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Should not raise
        validate_content(content)

    def test_validate_content_rejects_empty_content(self):
        """Test validate_content rejects empty content."""
        with pytest.raises(ValueError, match="empty"):
            validate_content("")

    def test_validate_content_rejects_whitespace_only(self):
        """Test validate_content rejects whitespace-only content."""
        with pytest.raises(ValueError, match="empty"):
            validate_content("   \n\n   ")

    def test_validate_content_rejects_missing_h1_heading(self):
        """Test validate_content rejects content without H1 heading."""
        content = "## Secondary Heading\n\nSome content. More content. Even more.\n"
        with pytest.raises(ValueError, match="must start with H1"):
            validate_content(content)

    def test_validate_content_rejects_heading_without_space(self):
        """Test validate_content rejects H1 without space after hash."""
        content = "#NoSpace\n\nContent here. More content. Final content.\n"
        with pytest.raises(ValueError, match="must start with H1"):
            validate_content(content)

    def test_validate_content_rejects_missing_blank_line(self):
        """Test validate_content rejects content without blank line separator."""
        content = "# Title\nDirect prose without blank line separator. More content. Final content.\n"
        with pytest.raises(ValueError, match="Second line must be blank"):
            validate_content(content)

    def test_validate_content_rejects_too_few_sentences(self):
        """Test validate_content rejects content with only 1 sentence."""
        content = "# Title\n\nOnly one sentence.\n"
        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_content(content)

    def test_validate_content_rejects_too_many_sentences(self):
        """Test validate_content rejects content with 4+ sentences."""
        content = "# Title\n\nFirst. Second. Third. Fourth.\n"
        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_content(content)

    def test_validate_content_rejects_missing_prose(self):
        """Test validate_content rejects content with no prose after heading."""
        content = "# Title\n\n"
        with pytest.raises(ValueError, match="No prose content"):
            validate_content(content)

    def test_validate_content_rejects_missing_trailing_newline(self):
        """Test validate_content rejects content without trailing newline."""
        content = "# Title\n\nContent here. More content. Final content."
        with pytest.raises(ValueError, match="trailing newline"):
            validate_content(content)

    def test_validate_content_accepts_multiple_paragraphs(self):
        """Test validate_content handles multiple paragraphs correctly."""
        content = "# Title\n\nFirst paragraph first sentence. First paragraph second sentence.\n\nSecond paragraph third sentence.\n"
        # Should not raise (3 sentences total)
        validate_content(content)


class TestWriteFile:
    """Tests for file writing functionality."""

    def test_write_file_creates_file(self, tmp_path, monkeypatch):
        """Test that write_file creates a file at FILENAME."""
        monkeypatch.chdir(tmp_path)
        content = "# Test Title\n\nThis is sentence one. This is sentence two. This is sentence three.\n"

        result = write_file(content)

        assert result is True
        assert (tmp_path / FILENAME).exists()

    def test_write_file_returns_true_on_success(self, tmp_path, monkeypatch):
        """Test that write_file returns True on successful write."""
        monkeypatch.chdir(tmp_path)
        content = "# Python Basics\n\nPython is an interpreted language. It supports multiple programming paradigms. This makes it versatile for many applications.\n"

        result = write_file(content)

        assert result is True

    def test_write_file_writes_utf8_encoding(self, tmp_path, monkeypatch):
        """Test that write_file uses UTF-8 encoding."""
        monkeypatch.chdir(tmp_path)
        content = "# Encoding Test\n\nUTF-8 supports unicode characters. This includes émojis and spëcial chars. Modern systems use UTF-8 worldwide.\n"

        write_file(content)

        # Read binary to verify UTF-8 encoding
        binary = (tmp_path / FILENAME).read_bytes()
        # Should decode successfully as UTF-8
        decoded = binary.decode("utf-8")
        assert decoded == content

    def test_write_file_uses_lf_line_endings(self, tmp_path, monkeypatch):
        """Test that write_file uses Unix LF line endings."""
        monkeypatch.chdir(tmp_path)
        content = "# Title\n\nFirst. Second. Third.\n"

        write_file(content)

        # Read binary to verify no CRLF
        binary = (tmp_path / FILENAME).read_bytes()
        assert b"\r\n" not in binary
        assert content.encode("utf-8") == binary

    def test_write_file_writes_correct_content(self, tmp_path, monkeypatch):
        """Test that write_file writes the exact content provided."""
        monkeypatch.chdir(tmp_path)
        content = "# Machine Learning\n\nML algorithms learn from data. Neural networks simulate biological systems. Deep learning enables powerful AI applications.\n"

        write_file(content)

        written = (tmp_path / FILENAME).read_text(encoding="utf-8")
        assert written == content

    def test_write_file_rejects_invalid_content(self, tmp_path, monkeypatch):
        """Test that write_file validates content before writing."""
        monkeypatch.chdir(tmp_path)
        invalid_content = "No heading. Just prose. And more prose.\n"

        with pytest.raises(ValueError, match="must start with H1"):
            write_file(invalid_content)

        # File should not be created
        assert not (tmp_path / FILENAME).exists()

    def test_write_file_rejects_empty_content(self, tmp_path, monkeypatch):
        """Test that write_file rejects empty content."""
        monkeypatch.chdir(tmp_path)

        with pytest.raises(ValueError, match="empty"):
            write_file("")

        assert not (tmp_path / FILENAME).exists()

    def test_write_file_rejects_content_without_blank_line(self, tmp_path, monkeypatch):
        """Test that write_file rejects content missing blank line separator."""
        monkeypatch.chdir(tmp_path)
        invalid_content = "# Title\nProse without blank line. More content. Final content.\n"

        with pytest.raises(ValueError, match="Second line must be blank"):
            write_file(invalid_content)

        assert not (tmp_path / FILENAME).exists()

    def test_write_file_rejects_content_with_wrong_sentence_count(self, tmp_path, monkeypatch):
        """Test that write_file rejects content with wrong sentence count."""
        monkeypatch.chdir(tmp_path)
        invalid_content = "# Title\n\nOnly one sentence.\n"

        with pytest.raises(ValueError, match="2-3 sentences"):
            write_file(invalid_content)

        assert not (tmp_path / FILENAME).exists()


class TestVerifyFile:
    """Tests for file verification functionality."""

    def test_verify_file_succeeds_with_valid_file(self, tmp_path, monkeypatch):
        """Test that verify_file passes with valid markdown file."""
        monkeypatch.chdir(tmp_path)
        content = "# Data Science and Machine Learning\n\nData science is an interdisciplinary field that combines statistics, mathematics, and computer science to extract valuable insights. Machine learning algorithms enable systems to learn patterns from data without explicit programming. It enables organizations to extract valuable insights from large datasets and make better decisions.\n"

        # Create valid file
        (tmp_path / FILENAME).write_text(content, encoding="utf-8")

        result = verify_file()

        assert result is True

    def test_verify_file_returns_true_on_success(self, tmp_path, monkeypatch):
        """Test that verify_file returns True on successful verification."""
        monkeypatch.chdir(tmp_path)
        content = "# Web Development and Modern Technologies\n\nWeb development involves frontend and backend technologies working together seamlessly to create powerful applications. HTML, CSS, and JavaScript power the modern web and create interactive user experiences across devices. Modern frameworks like React, Vue, and Angular simplify development significantly and improve productivity.\n"

        (tmp_path / FILENAME).write_text(content, encoding="utf-8")

        result = verify_file()

        assert result is True

    def test_verify_file_rejects_missing_file(self, tmp_path, monkeypatch):
        """Test that verify_file raises FileNotFoundError if file doesn't exist."""
        monkeypatch.chdir(tmp_path)

        with pytest.raises(FileNotFoundError, match="does not exist"):
            verify_file()

    def test_verify_file_checks_h1_heading(self, tmp_path, monkeypatch):
        """Test that verify_file validates H1 heading."""
        monkeypatch.chdir(tmp_path)
        invalid_content = "## Secondary Heading\n\nContent here. More content. Final content.\n"

        (tmp_path / FILENAME).write_text(invalid_content, encoding="utf-8")

        with pytest.raises(ValueError, match="H1"):
            verify_file()

    def test_verify_file_checks_blank_line_separator(self, tmp_path, monkeypatch):
        """Test that verify_file validates blank line separator."""
        monkeypatch.chdir(tmp_path)
        invalid_content = "# Title\nProse without blank line. More content. Final content.\n"

        (tmp_path / FILENAME).write_text(invalid_content, encoding="utf-8")

        with pytest.raises(ValueError, match="Second line must be blank"):
            verify_file()

    def test_verify_file_checks_sentence_count(self, tmp_path, monkeypatch):
        """Test that verify_file validates sentence count."""
        monkeypatch.chdir(tmp_path)
        invalid_content = "# Title\n\nOnly one sentence.\n"

        (tmp_path / FILENAME).write_text(invalid_content, encoding="utf-8")

        with pytest.raises(ValueError, match="2-3 sentences"):
            verify_file()

    def test_verify_file_checks_utf8_encoding(self, tmp_path, monkeypatch):
        """Test that verify_file validates UTF-8 encoding."""
        monkeypatch.chdir(tmp_path)
        # Create file with UTF-8 BOM
        content = "# Title\n\nContent here. More content. Final content.\n"

        (tmp_path / FILENAME).write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))

        with pytest.raises(ValueError, match="BOM"):
            verify_file()

    def test_verify_file_checks_lf_line_endings(self, tmp_path, monkeypatch):
        """Test that verify_file validates Unix LF line endings."""
        monkeypatch.chdir(tmp_path)
        # Create file with CRLF line endings
        content = "# Title\r\n\r\nContent here. More content. Final content.\r\n"

        (tmp_path / FILENAME).write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError, match="CRLF"):
            verify_file()

    def test_verify_file_checks_trailing_newline(self, tmp_path, monkeypatch):
        """Test that verify_file validates trailing newline."""
        monkeypatch.chdir(tmp_path)
        content = "# Title\n\nContent here. More content. Final content."  # No trailing newline

        (tmp_path / FILENAME).write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="trailing newline"):
            verify_file()

    def test_verify_file_checks_file_size(self, tmp_path, monkeypatch):
        """Test that verify_file validates file size range."""
        monkeypatch.chdir(tmp_path)
        # Create very small file (less than 350 bytes)
        small_content = "# Title\n\nShort. Brief. Tiny.\n"

        (tmp_path / FILENAME).write_text(small_content, encoding="utf-8")

        with pytest.raises(ValueError, match="outside acceptable range"):
            verify_file()

    def test_verify_file_accepts_valid_file_size(self, tmp_path, monkeypatch):
        """Test that verify_file accepts file within size range."""
        monkeypatch.chdir(tmp_path)
        # Create file of appropriate size (350-650 bytes)
        content = "# Cybersecurity and Data Protection\n\nCybersecurity protects digital systems from malicious attacks and unauthorized access by implementing comprehensive defensive measures and best practices. Organizations invest heavily in security measures to protect their valuable assets and sensitive information. Threats continue to evolve constantly in today's digital landscape.\n"

        (tmp_path / FILENAME).write_text(content, encoding="utf-8")
        file_size = (tmp_path / FILENAME).stat().st_size

        # Verify size is in acceptable range
        assert 350 <= file_size <= 650

        result = verify_file()
        assert result is True


class TestOrchestration:
    """Tests for main orchestration function (run) - phases 1-2."""

    def test_run_successful_workflow(self, tmp_path, monkeypatch):
        """Test run() completes successfully through phases 1-2."""
        monkeypatch.chdir(tmp_path)
        mock_content = "# Artificial Intelligence and Deep Learning\n\nArtificial intelligence systems learn patterns from data through advanced machine learning algorithms and neural networks. Neural networks enable deep learning capabilities for extremely complex pattern recognition and classification tasks. This technology is transforming industries worldwide by automating decision making and improving human productivity.\n"

        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            result = run()
            assert result is True

        # Verify file was created
        assert (tmp_path / FILENAME).exists()

    def test_run_returns_true_on_success(self, tmp_path, monkeypatch):
        """Test that run() returns True on successful completion of phases 1-2."""
        monkeypatch.chdir(tmp_path)
        mock_content = "# Programming and Software Development\n\nProgramming is the practice of writing computer instructions to solve real-world problems and create innovative solutions. Developers use various programming languages and frameworks to build robust and scalable applications for diverse use cases. The field continues to evolve with new technologies and methodologies each year.\n"
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            result = run()
            assert result is True

        # Verify file was created
        assert (tmp_path / FILENAME).exists()

    def test_run_creates_file_with_correct_content(self, tmp_path, monkeypatch):
        """Test that run() creates file with generated content."""
        monkeypatch.chdir(tmp_path)
        mock_content = "# Blockchain Technology and Decentralization\n\nBlockchain technology enables distributed ledger systems with transparency, immutability and cryptographic security features. Cryptocurrency implementations use blockchain for secure transaction management and permanent record keeping. This architecture is revolutionizing how we think about decentralized systems and trust.\n"
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            run()

        # Verify file content
        written = (tmp_path / FILENAME).read_text(encoding="utf-8")
        assert written == mock_content

    def test_run_fails_on_generation_error(self):
        """Test that run() propagates generation errors."""
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   side_effect=ValueError("Generation failed")), \
             pytest.raises(ValueError):
            run()

    def test_run_fails_on_validation_error(self):
        """Test that run() propagates validation errors from phase 1."""
        mock_content = "# Title\n\nOnly one sentence."
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content), \
             pytest.raises(ValueError, match="2-3 sentences"):
            run()

    def test_run_fails_on_invalid_format(self):
        """Test that run() fails when generated content has invalid format."""
        mock_content = "No heading here. Just content. And more content."
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content), \
             pytest.raises(ValueError, match="must start with H1"):
            run()

    def test_run_validates_blank_line_requirement(self):
        """Test that run() validates blank line separator from phase 1."""
        mock_content = "# Title\nNo blank line here. Just prose. And more prose.\n"
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content), \
             pytest.raises(ValueError, match="Second line must be blank"):
            run()

    def test_run_creates_utf8_file(self, tmp_path, monkeypatch):
        """Test that run() creates file with UTF-8 encoding."""
        monkeypatch.chdir(tmp_path)
        mock_content = "# Unicode and Internationalization Standards\n\nModern applications must support émojis and spëcial characters from many different languages around the world today. UTF-8 encoding handles all unicode symbols worldwide correctly without any data loss or corruption issues. This is the global standard for text representation and has been adopted universally.\n"
        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content):
            run()

        # Verify UTF-8 encoding
        binary = (tmp_path / FILENAME).read_bytes()
        assert binary.decode("utf-8") == mock_content

    def test_run_fails_if_file_verification_fails(self, tmp_path, monkeypatch):
        """Test that run() fails if file verification fails in phase 2."""
        monkeypatch.chdir(tmp_path)
        mock_content = "# Title\n\nContent here. More content. Final content.\n"

        with patch("sheep.features.feature_255_markdown_file_creation.generate_markdown_content",
                   return_value=mock_content), \
             patch("sheep.features.feature_255_markdown_file_creation.verify_file",
                   side_effect=ValueError("Verification failed")), \
             pytest.raises(ValueError, match="Verification failed"):
            run()
