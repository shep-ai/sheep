"""
Tests for Feature 201 Phase 2: File Creation & Comprehensive Validation

This test suite validates that:
1. The file writing function works correctly (task-2-1)
2. The comprehensive validation function works correctly (task-2-2)
3. File creation and validation are executed successfully (task-2-3)
"""

from pathlib import Path

from src.create_markdown import (
    create_markdown_file,
    validate_markdown_file,
)


class TestPhase2Task1FileWriting:
    """Task 2-1: Implement file writing function with pathlib and proper encoding."""

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

    def test_file_has_utf8_encoding(self, tmp_path):
        """Test that file is UTF-8 encoded without BOM."""
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

    def test_file_has_lf_line_endings(self, tmp_path):
        """Test that file uses Unix LF line endings only."""
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


class TestPhase2Task2Validation:
    """Task 2-2: Implement comprehensive validation function."""

    def test_validation_returns_dict_with_required_keys(self, tmp_path):
        """Test that validation returns dict with 'valid' and 'errors' keys."""
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
        """Test that validation checks for H1 heading."""
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
        """Test that validation checks for UTF-8 encoding."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Should pass encoding check
        assert validation['encoding']['is_valid'] is True

    def test_validation_checks_lf_line_endings(self, tmp_path):
        """Test that validation checks for LF line endings."""
        content = "# Test Title\n\nTest sentence one. Test sentence two. Test sentence three.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Should pass line ending check
        assert validation['encoding']['is_valid'] is True

    def test_validation_checks_file_size(self, tmp_path):
        """Test that validation checks file size is within range."""
        content = (
            "# Test Title for File Size Validation\n\n"
            "This is the first sentence that provides substantial content to meet the minimum file size requirement of 250 bytes. "
            "This is the second sentence that continues to add meaningful text to ensure we reach the required byte count. "
            "This is the third and final sentence that completes the file size validation test requirements.\n"
        )
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Valid file should be within 250-600 bytes
        assert validation['is_valid'] is True

    def test_validation_provides_clear_errors(self, tmp_path):
        """Test that validation provides clear, actionable error messages."""
        # Content with only 1 sentence (too few)
        content = "# Test Title\n\nOnly one sentence.\n"
        filename = "test_file.md"

        result_path = create_markdown_file(content, filename=filename, filepath=str(tmp_path))
        validation = validate_markdown_file(result_path)

        # Errors should be non-empty and descriptive
        assert len(validation['errors']) > 0
        assert all(isinstance(e, str) for e in validation['errors'])


class TestPhase2Task3Execution:
    """Task 2-3: Execute file creation and validation."""

    def test_feature_201_file_creation_and_validation(self, tmp_path):
        """Test complete task 2-3: Execute file creation and validation with Phase 1 content."""
        # Content from Phase 1 (task 1-2)
        title = "Automated Implementation Excellence"
        prose = (
            "Automated systems achieve excellence through systematic design and careful validation. "
            "The Sheep platform demonstrates how agents can generate high-quality artifacts consistently. "
            "Every implementation follows strict standards for reliability and maintainability."
        )

        # Construct full content as it would be created by Phase 1
        full_content = f"# {title}\n\n{prose}\n"

        # Task 2-3: Execute file creation
        filename = "test_feature_201.md"
        result_path = create_markdown_file(full_content, filename=filename, filepath=str(tmp_path))

        # Verify file exists
        assert Path(result_path).exists()
        assert Path(result_path).is_file()

        # Task 2-3: Execute validation
        validation = validate_markdown_file(result_path)

        # Verify validation passes
        assert validation['is_valid'] is True
        assert len(validation['errors']) == 0

        # Verify file content
        written_content = Path(result_path).read_text(encoding='utf-8')
        assert written_content == full_content

    def test_file_creation_and_validation_for_test_y9go1c_md(self):
        """Test file creation and validation for actual test-y9go1c.md in repo root."""
        # Use current working directory (repo root)
        title = "Automated Implementation Excellence"
        prose = (
            "Automated systems achieve excellence through systematic design and careful validation. "
            "The Sheep platform demonstrates how agents can generate high-quality artifacts consistently. "
            "Every implementation follows strict standards for reliability and maintainability."
        )

        full_content = f"# {title}\n\n{prose}\n"
        filename = "test_y9go1c.md"

        # Create the file
        result_path = create_markdown_file(full_content, filename=filename, filepath=None)

        try:
            # Verify file was created
            assert Path(result_path).exists()

            # Validate the file
            validation = validate_markdown_file(result_path)

            # Verify validation passes all checks
            assert validation['is_valid'] is True
            assert len(validation['errors']) == 0

            # Verify file content
            written_content = Path(result_path).read_text(encoding='utf-8')
            assert written_content == full_content

            # Verify encoding
            with open(result_path, 'rb') as f:
                raw_bytes = f.read()
            assert not raw_bytes.startswith(b'\xef\xbb\xbf')  # No BOM
            assert b'\r\n' not in raw_bytes  # No CRLF

            # Verify file size
            file_size = len(raw_bytes)
            assert 250 <= file_size <= 600, f"File size {file_size} outside valid range"

        finally:
            # Clean up - remove the file if it was created
            if Path(result_path).exists():
                Path(result_path).unlink()
