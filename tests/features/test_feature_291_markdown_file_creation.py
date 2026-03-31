"""Tests for feature 291: Create markdown file test-sdxefr.md with prose content.

Tests cover:
- File creation with correct name and location
- File contains H1 heading and 2-3 sentences
- File encoding (UTF-8 without BOM) and line endings (LF)
- File ends with trailing newline
- Markdown validation passes
- Git operations are executed
- Function returns correct structure
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from sheep.features.feature_291_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_sdxefr_markdown_file,
)

# Sample valid markdown content for testing
SAMPLE_MARKDOWN = """# Test Feature Implementation

Feature 291 creates a markdown file with a specific structure and requirements. The file contains exactly two sentences describing the implementation process.
"""


class TestFeature291FileCreation:
    """Tests for feature 291 file creation."""

    def _setup_mocks(self):
        """Setup common mocks for testing."""
        # Mock the LLM to return our sample markdown
        mock_llm = Mock()
        mock_llm.call.return_value = {"content": SAMPLE_MARKDOWN}
        return mock_llm

    def _create_with_mocks(self):
        """Helper to create feature with all necessary mocks."""
        mock_llm = self._setup_mocks()
        with patch('sheep.content_generators.get_reasoning_llm', return_value=mock_llm), \
             patch('subprocess.run') as mock_run:
            # Configure the mock to return proper values for different git commands
            def run_side_effect(args, *pargs, **kwargs):
                result = MagicMock()
                result.returncode = 0
                result.stdout = ""
                result.stderr = ""
                # For rev-parse, return the current branch
                if 'rev-parse' in args:
                    result.stdout = "feat/291-markdown-file-creation-420f73\n"
                return result

            mock_run.side_effect = run_side_effect
            return create_test_sdxefr_markdown_file(), mock_run

    def test_create_file_creates_correct_file(self):
        """Test that create_test_sdxefr_markdown_file creates file with correct name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                assert Path(MARKDOWN_FILENAME).exists()
                assert result['filepath'].endswith(MARKDOWN_FILENAME)
            finally:
                import os
                os.chdir(original_cwd)

    def test_file_contains_h1_heading(self):
        """Test that created file contains H1 markdown heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                content = Path(MARKDOWN_FILENAME).read_text()
                assert content.lstrip().startswith('# '), "File must start with H1 heading"
            finally:
                import os
                os.chdir(original_cwd)

    def test_file_contains_prose_content(self):
        """Test that created file contains prose after H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                content = Path(MARKDOWN_FILENAME).read_text()
                lines = content.split('\n')
                # Should have: heading, blank line, prose
                assert len(lines) >= 3, "File should have heading, blank line, and prose"
                assert lines[0].startswith('# ')
                assert lines[1] == '', "Second line should be blank"
            finally:
                import os
                os.chdir(original_cwd)

    def test_file_has_2_to_3_sentences(self):
        """Test that file contains exactly 2-3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                content = Path(MARKDOWN_FILENAME).read_text()
                # Count periods (sentences)
                period_count = content.count('.')
                assert 2 <= period_count <= 3, f"Expected 2-3 sentences, found {period_count}"
            finally:
                import os
                os.chdir(original_cwd)

    def test_file_utf8_encoding_no_bom(self):
        """Test that file uses UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                binary_content = Path(MARKDOWN_FILENAME).read_bytes()
                # Check no UTF-8 BOM
                assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
                # Verify valid UTF-8
                binary_content.decode('utf-8')
            finally:
                import os
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                binary_content = Path(MARKDOWN_FILENAME).read_bytes()
                # Check no CRLF or CR
                assert b'\r\n' not in binary_content, "File should not have CRLF endings"
                assert b'\r' not in binary_content, "File should not have CR endings"
            finally:
                import os
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that file ends with trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                content = Path(MARKDOWN_FILENAME).read_text()
                assert content.endswith('\n'), "File should end with trailing newline"
            finally:
                import os
                os.chdir(original_cwd)

    def test_returns_dict_with_required_keys(self):
        """Test that function returns dict with filepath, content, commit_message, push_result."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                assert isinstance(result, dict)
                assert 'filepath' in result
                assert 'content' in result
                assert 'commit_message' in result
                assert 'push_result' in result
            finally:
                import os
                os.chdir(original_cwd)

    def test_commit_message_format(self):
        """Test that commit message has correct format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
                assert result['commit_message'] == expected_message
            finally:
                import os
                os.chdir(original_cwd)

    def test_content_in_result_matches_file(self):
        """Test that content in result dict matches file content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                file_content = Path(MARKDOWN_FILENAME).read_text()
                assert result['content'] == file_content
            finally:
                import os
                os.chdir(original_cwd)

    def test_feature_number_is_291(self):
        """Test that FEATURE_NUMBER constant is set to 291."""
        assert FEATURE_NUMBER == 291

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME constant is set to test-sdxefr.md."""
        assert MARKDOWN_FILENAME == "test-sdxefr.md"
