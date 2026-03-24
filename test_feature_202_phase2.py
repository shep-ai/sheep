"""
Tests for Feature 202 Phase 2: File Creation & Comprehensive Validation

This test suite validates that:
1. The markdown file is created with proper encoding and line endings
2. All validation checks pass (markdown format, UTF-8 encoding, LF line endings, file size, sentence count)
3. File creation and validation execute successfully with feature 202-specific content
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.create_markdown import (
    create_markdown_file,
    validate_markdown_file,
    generate_markdown_content_for_feature,
)


class TestPhase2Task2CreateMarkdownFile:
    """Task 2-2: Create markdown file with proper structure and encoding."""

    def test_create_markdown_file_returns_path(self, tmp_path):
        """Test that function returns absolute path to created file."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))

        assert result_path is not None
        assert isinstance(result_path, str)
        assert result_path.endswith(filename)

    def test_create_markdown_file_writes_to_disk(self, tmp_path):
        """Test that file is actually written to disk."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))

        assert Path(result_path).exists()
        assert Path(result_path).is_file()

    def test_file_content_matches_input(self, tmp_path):
        """Test that written file contains exact content provided."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))

        written_content = Path(result_path).read_text(encoding='utf-8')
        assert written_content == content

    def test_file_has_utf8_encoding_no_bom(self, tmp_path):
        """Test that file is UTF-8 encoded without BOM (Byte Order Mark)."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))

        # Read raw bytes
        with open(result_path, 'rb') as f:
            raw_bytes = f.read()

        # Check for UTF-8 BOM (xefbbbf)
        assert not raw_bytes.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"

        # Check that file can be decoded as UTF-8
        assert raw_bytes.decode('utf-8') == content

    def test_file_has_lf_line_endings_only(self, tmp_path):
        """Test that file uses Unix LF line endings only (no CRLF or CR)."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))

        # Read raw bytes
        with open(result_path, 'rb') as f:
            raw_bytes = f.read()

        # Check for CRLF (Windows line endings)
        assert b'\r\n' not in raw_bytes, "File should not have CRLF line endings"

        # Check for CR (old Mac line endings)
        assert b'\r' not in raw_bytes, "File should not have CR line endings"

        # Check for LF (Unix line endings)
        assert b'\n' in raw_bytes, "File should have LF line endings"

    def test_file_ends_with_newline(self, tmp_path):
        """Test that file ends with newline character."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))

        with open(result_path, 'rb') as f:
            raw_bytes = f.read()

        assert raw_bytes.endswith(b'\n'), "File should end with newline"

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 250-600 bytes."""
        content = (
            "# Test Title for File Size Validation\n\n"
            "This is the first sentence that provides substantial content to meet the minimum file size requirement. "
            "This is the second sentence that continues to add meaningful text to ensure we reach the required byte count. "
            "This is the third and final sentence that completes the file size validation test requirements.\n"
        )
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        file_size = Path(result_path).stat().st_size

        assert 250 <= file_size <= 600, f"File size {file_size} outside acceptable range 250-600 bytes"


class TestPhase2Task3ValidationFunctions:
    """Task 2-3: Implement encoding and line ending validation."""

    def test_validate_markdown_file_returns_dict(self, tmp_path):
        """Test that validation returns dict with required keys."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        assert isinstance(validation, dict)
        assert 'is_valid' in validation
        assert 'errors' in validation

    def test_validation_passes_for_valid_file(self, tmp_path):
        """Test that validation passes for correctly formatted file."""
        content = (
            "# Test Title for Validation\n\n"
            "This is the first test sentence with enough content to demonstrate proper validation. "
            "This is the second sentence that adds more information and context to the validation test. "
            "This is the third and final sentence that completes the required format for markdown validation.\n"
        )
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        assert validation['is_valid'] is True
        assert len(validation['errors']) == 0

    def test_validation_checks_h1_heading(self, tmp_path):
        """Test that validation checks for H1 heading at file start."""
        # Content without H1 heading
        content = "Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Should have errors related to missing H1
        assert validation['is_valid'] is False
        assert any('heading' in str(e).lower() or 'h1' in str(e).lower()
                  for e in validation['errors'])

    def test_validation_checks_sentence_count(self, tmp_path):
        """Test that validation checks for exactly 2-3 sentences."""
        # Content with only 1 sentence
        content = "# Test Title\n\nTest sentence only.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Should have errors related to sentence count
        assert validation['is_valid'] is False
        assert any('sentence' in str(e).lower()
                  for e in validation['errors'])

    def test_validation_checks_utf8_encoding(self, tmp_path):
        """Test that validation checks for UTF-8 encoding without BOM."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Should pass encoding check
        assert validation['encoding']['is_valid'] is True
        assert 'BOM' not in str(validation['encoding'].get('errors', []))

    def test_validation_checks_lf_line_endings(self, tmp_path):
        """Test that validation checks for LF line endings."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Should pass line ending check (part of encoding validation)
        assert validation['encoding']['is_valid'] is True


class TestPhase2Task4FullExecution:
    """Task 2-4: Execute complete file creation and validation for Feature 202."""

    def test_feature_202_file_creation_and_validation(self, tmp_path):
        """Test complete Phase 2: Create file and validate with feature 202-specific content."""
        # Use deterministic content for feature 202
        with patch('src.create_markdown.create_llm') as mock_create_llm:
            mock_llm = Mock()

            # Feature 202 deterministic content
            generated_content = (
                "# Cloud Computing Infrastructure and Solutions\n\n"
                "Cloud computing provides organizations with scalable computing resources and storage. "
                "Modern cloud platforms enable efficient management of applications and data at global scale. "
                "Best practices include security controls and performance optimization strategies.\n"
            )

            mock_llm.call.return_value = generated_content
            mock_create_llm.return_value = mock_llm

            # Generate content for feature 202
            result = generate_markdown_content_for_feature(feature_number=202)

            # Create markdown file
            filename = "test-1u4gfg.md"
            file_path = create_markdown_file(
                result['full_content'],
                filename=filename,
                filepath=str(tmp_path)
            )

            # Verify file exists
            assert Path(file_path).exists()
            assert Path(file_path).is_file()

            # Execute validation
            validation = validate_markdown_file(file_path)

            # Verify validation passes
            assert validation['is_valid'] is True, f"Validation failed: {validation['errors']}"
            assert len(validation['errors']) == 0

            # Verify file content
            written_content = Path(file_path).read_text(encoding='utf-8')
            assert written_content == result['full_content']

            # Verify file size is within range
            file_size = Path(file_path).stat().st_size
            assert 250 <= file_size <= 600, f"File size {file_size} outside acceptable range"

            # Verify encoding
            assert validation['encoding']['is_valid'] is True

            # Verify structure
            assert validation['structure']['is_valid'] is True

    def test_feature_202_validation_provides_clear_errors(self, tmp_path):
        """Test that validation provides clear, actionable error messages."""
        # Content with only 1 sentence (too few)
        content = "# Test Title\n\nOnly one sentence.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Errors should be non-empty and descriptive
        assert len(validation['errors']) > 0
        assert all(isinstance(e, str) for e in validation['errors'])
        # Error messages should be helpful
        for error in validation['errors']:
            assert len(error) > 0
