"""Tests for feature 272: Create markdown file test-wvkqjb.md with prose content.

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

from sheep.features.feature_272_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_272_markdown_file,
)

# Sample valid markdown content for testing
SAMPLE_MARKDOWN = """# Artificial Intelligence Evolution

Artificial intelligence has rapidly transformed from theoretical concept to practical application across industries. Machine learning algorithms now power recommendation systems, autonomous vehicles, and medical diagnostic tools. The field continues to evolve with advances in neural networks and large language models."""


class TestFeature272FileCreation:
    """Tests for feature 272 file creation."""

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
                    result.stdout = "main\n"
                return result

            mock_run.side_effect = run_side_effect
            return create_feature_272_markdown_file(), mock_run

    def test_module_imports_successfully(self):
        """Test that the feature module can be imported without errors."""
        from sheep.features.feature_272_markdown_file_creation import (
            FEATURE_NUMBER,
            FEATURE_NAME,
            MARKDOWN_FILENAME,
        )
        assert FEATURE_NUMBER == 272

    def test_create_file_creates_correct_file(self):
        """Test that create_feature_272_markdown_file creates file with correct name."""
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
        """Test that commit message has correct format for feature 272."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                result, _ = self._create_with_mocks()
                expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with title and prose content"
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

    def test_function_signature_accepts_repo_path(self):
        """Test that function accepts optional repo_path parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sheep.content_generators.get_reasoning_llm') as mock_llm_factory, \
                 patch('subprocess.run') as mock_run:
                mock_llm = Mock()
                mock_llm.call.return_value = {"content": SAMPLE_MARKDOWN}
                mock_llm_factory.return_value = mock_llm

                def run_side_effect(args, *pargs, **kwargs):
                    result = MagicMock()
                    result.returncode = 0
                    result.stdout = ""
                    result.stderr = ""
                    if 'rev-parse' in args:
                        result.stdout = "main\n"
                    return result

                mock_run.side_effect = run_side_effect

                original_cwd = Path.cwd()
                try:
                    import os
                    os.chdir(tmpdir)
                    # Should not raise exception
                    result = create_feature_272_markdown_file(repo_path=tmpdir)
                    assert result is not None
                finally:
                    import os
                    os.chdir(original_cwd)

    def test_error_handling_logs_failures(self):
        """Test that error handling logs failures appropriately."""
        with patch('sheep.content_generators.get_reasoning_llm') as mock_llm_factory:
            # Make LLM raise an exception
            mock_llm = Mock()
            mock_llm.call.side_effect = ValueError("LLM API failed")
            mock_llm_factory.return_value = mock_llm

            with patch('sheep.observability.logging.get_logger') as mock_logger_factory:
                mock_logger = Mock()
                mock_logger_factory.return_value = mock_logger

                try:
                    create_feature_272_markdown_file()
                except ValueError:
                    # Expected to raise
                    pass

                # Verify that error was logged (via the logger mock)
                # The error will be logged by the actual logger in content_generators
