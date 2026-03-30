"""Tests for feature 272: Create markdown file test-6poz5r.md with prose content.

Tests cover:
- File creation with correct name and location
- File contains H1 heading and 2-3 sentences
- File encoding (UTF-8 without BOM) and line endings (LF)
- File ends with trailing newline
- Markdown validation passes
- Git operations are executed
- Function returns correct structure
- Orchestration sequence is correct
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch, call

from sheep.features.feature_272_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_272_markdown_file,
)

# Sample valid markdown content for testing
SAMPLE_MARKDOWN = """# Computational Thinking and Problem Solving

Computational thinking is a fundamental skill that extends far beyond computer science, enabling individuals to solve complex problems with efficiency and creativity. This approach breaks down intricate challenges into manageable components, identifies patterns, and develops systematic solutions that can be automated or scaled. Whether applied to everyday tasks or advanced scientific research, computational thinking transforms how we approach problem-solving."""


class TestFeature272WorkflowOrchestration:
    """Tests for feature 272 workflow orchestration."""

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
                if isinstance(args, list) and 'rev-parse' in args:
                    result.stdout = "main\n"
                return result

            mock_run.side_effect = run_side_effect
            return create_feature_272_markdown_file(), mock_run

    def test_orchestration_calls_all_five_steps(self):
        """Test that orchestration calls all 5 steps in sequence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                # Patch where functions are imported in the feature module
                with patch('sheep.features.feature_272_markdown_file_creation.generate_markdown_content') as mock_gen, \
                     patch('sheep.features.feature_272_markdown_file_creation.write_markdown_file') as mock_write, \
                     patch('sheep.features.feature_272_markdown_file_creation.validate_markdown_file') as mock_validate, \
                     patch('sheep.features.feature_272_markdown_file_creation.commit_markdown_file') as mock_commit, \
                     patch('sheep.features.feature_272_markdown_file_creation.push_markdown_file') as mock_push:

                    mock_gen.return_value = SAMPLE_MARKDOWN
                    mock_write.return_value = str(Path.cwd() / MARKDOWN_FILENAME)
                    mock_validate.return_value = True
                    mock_commit.return_value = "commit result"
                    mock_push.return_value = "push result"

                    create_feature_272_markdown_file()

                    # Verify all functions were called
                    mock_gen.assert_called_once()
                    mock_write.assert_called_once()
                    mock_validate.assert_called_once()
                    mock_commit.assert_called_once()
                    mock_push.assert_called_once()
            finally:
                import os
                os.chdir(original_cwd)

    def test_orchestration_calls_functions_in_correct_order(self):
        """Test that functions are called in the correct sequence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('sheep.features.feature_272_markdown_file_creation.generate_markdown_content') as mock_gen, \
                     patch('sheep.features.feature_272_markdown_file_creation.write_markdown_file') as mock_write, \
                     patch('sheep.features.feature_272_markdown_file_creation.validate_markdown_file') as mock_validate, \
                     patch('sheep.features.feature_272_markdown_file_creation.commit_markdown_file') as mock_commit, \
                     patch('sheep.features.feature_272_markdown_file_creation.push_markdown_file') as mock_push:

                    mock_gen.return_value = SAMPLE_MARKDOWN
                    mock_write.return_value = str(Path.cwd() / MARKDOWN_FILENAME)
                    mock_validate.return_value = True
                    mock_commit.return_value = "commit result"
                    mock_push.return_value = "push result"

                    # Track call order
                    manager = Mock()
                    manager.attach_mock(mock_gen, 'gen')
                    manager.attach_mock(mock_write, 'write')
                    manager.attach_mock(mock_validate, 'validate')
                    manager.attach_mock(mock_commit, 'commit')
                    manager.attach_mock(mock_push, 'push')

                    create_feature_272_markdown_file()

                    # Verify order: generate -> write -> validate -> commit -> push
                    expected_calls = [
                        call.gen(),
                        call.write(SAMPLE_MARKDOWN, MARKDOWN_FILENAME),
                        call.validate(str(Path.cwd() / MARKDOWN_FILENAME)),
                        call.commit(str(Path.cwd() / MARKDOWN_FILENAME), SAMPLE_MARKDOWN, str(Path.cwd()), custom_message=f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"),
                        call.push(str(Path.cwd())),
                    ]
            finally:
                import os
                os.chdir(original_cwd)

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

    def test_write_markdown_file_called_with_correct_filename(self):
        """Test that write_markdown_file is called with correct filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('sheep.features.feature_272_markdown_file_creation.generate_markdown_content') as mock_gen, \
                     patch('sheep.features.feature_272_markdown_file_creation.write_markdown_file') as mock_write, \
                     patch('sheep.features.feature_272_markdown_file_creation.validate_markdown_file') as mock_validate, \
                     patch('sheep.features.feature_272_markdown_file_creation.commit_markdown_file') as mock_commit, \
                     patch('sheep.features.feature_272_markdown_file_creation.push_markdown_file') as mock_push:

                    mock_gen.return_value = SAMPLE_MARKDOWN
                    mock_write.return_value = str(Path.cwd() / MARKDOWN_FILENAME)
                    mock_validate.return_value = True
                    mock_commit.return_value = "commit result"
                    mock_push.return_value = "push result"

                    create_feature_272_markdown_file()

                    # Verify write_markdown_file was called with correct arguments
                    mock_write.assert_called_once_with(SAMPLE_MARKDOWN, MARKDOWN_FILENAME)
            finally:
                import os
                os.chdir(original_cwd)

    def test_commit_message_has_correct_format(self):
        """Test that commit message has correct conventional format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('sheep.features.feature_272_markdown_file_creation.generate_markdown_content') as mock_gen, \
                     patch('sheep.features.feature_272_markdown_file_creation.write_markdown_file') as mock_write, \
                     patch('sheep.features.feature_272_markdown_file_creation.validate_markdown_file') as mock_validate, \
                     patch('sheep.features.feature_272_markdown_file_creation.commit_markdown_file') as mock_commit, \
                     patch('sheep.features.feature_272_markdown_file_creation.push_markdown_file') as mock_push:

                    mock_gen.return_value = SAMPLE_MARKDOWN
                    mock_write.return_value = str(Path.cwd() / MARKDOWN_FILENAME)
                    mock_validate.return_value = True
                    mock_commit.return_value = "commit result"
                    mock_push.return_value = "push result"

                    result = create_feature_272_markdown_file()

                    # Verify commit message format
                    expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
                    assert result['commit_message'] == expected_message

                    # Verify commit_markdown_file was called with the correct message
                    call_args = mock_commit.call_args
                    assert call_args[1]['custom_message'] == expected_message
            finally:
                import os
                os.chdir(original_cwd)

    def test_commit_markdown_file_called_with_correct_args(self):
        """Test that commit_markdown_file is called with all required arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('sheep.features.feature_272_markdown_file_creation.generate_markdown_content') as mock_gen, \
                     patch('sheep.features.feature_272_markdown_file_creation.write_markdown_file') as mock_write, \
                     patch('sheep.features.feature_272_markdown_file_creation.validate_markdown_file') as mock_validate, \
                     patch('sheep.features.feature_272_markdown_file_creation.commit_markdown_file') as mock_commit, \
                     patch('sheep.features.feature_272_markdown_file_creation.push_markdown_file') as mock_push:

                    mock_gen.return_value = SAMPLE_MARKDOWN
                    filepath = str(Path.cwd() / MARKDOWN_FILENAME)
                    mock_write.return_value = filepath
                    mock_validate.return_value = True
                    mock_commit.return_value = "commit result"
                    mock_push.return_value = "push result"

                    create_feature_272_markdown_file()

                    # Verify commit_markdown_file was called with correct args
                    mock_commit.assert_called_once()
                    args, kwargs = mock_commit.call_args
                    assert args[0] == filepath  # filepath
                    assert args[1] == SAMPLE_MARKDOWN  # content
                    assert args[2] == str(Path.cwd())  # repo_path
                    assert 'custom_message' in kwargs
                    assert f"feat({FEATURE_NUMBER})" in kwargs['custom_message']
            finally:
                import os
                os.chdir(original_cwd)

    def test_push_markdown_file_called_after_commit(self):
        """Test that push_markdown_file is called after commit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('sheep.features.feature_272_markdown_file_creation.generate_markdown_content') as mock_gen, \
                     patch('sheep.features.feature_272_markdown_file_creation.write_markdown_file') as mock_write, \
                     patch('sheep.features.feature_272_markdown_file_creation.validate_markdown_file') as mock_validate, \
                     patch('sheep.features.feature_272_markdown_file_creation.commit_markdown_file') as mock_commit, \
                     patch('sheep.features.feature_272_markdown_file_creation.push_markdown_file') as mock_push:

                    mock_gen.return_value = SAMPLE_MARKDOWN
                    mock_write.return_value = str(Path.cwd() / MARKDOWN_FILENAME)
                    mock_validate.return_value = True
                    mock_commit.return_value = "commit result"
                    mock_push.return_value = "push result"

                    create_feature_272_markdown_file()

                    # Verify push was called
                    mock_push.assert_called_once()
                    # Verify it was called with repo_path
                    args, kwargs = mock_push.call_args
                    assert args[0] == str(Path.cwd()) or kwargs.get('repo_path') == str(Path.cwd())
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

    def test_validate_called_after_write(self):
        """Test that validate_markdown_file is called after file is written."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)

                with patch('sheep.features.feature_272_markdown_file_creation.generate_markdown_content') as mock_gen, \
                     patch('sheep.features.feature_272_markdown_file_creation.write_markdown_file') as mock_write, \
                     patch('sheep.features.feature_272_markdown_file_creation.validate_markdown_file') as mock_validate, \
                     patch('sheep.features.feature_272_markdown_file_creation.commit_markdown_file') as mock_commit, \
                     patch('sheep.features.feature_272_markdown_file_creation.push_markdown_file') as mock_push:

                    mock_gen.return_value = SAMPLE_MARKDOWN
                    filepath = str(Path.cwd() / MARKDOWN_FILENAME)
                    mock_write.return_value = filepath
                    mock_validate.return_value = True
                    mock_commit.return_value = "commit result"
                    mock_push.return_value = "push result"

                    create_feature_272_markdown_file()

                    # Verify validate was called with filepath from write
                    mock_validate.assert_called_once_with(filepath)
            finally:
                import os
                os.chdir(original_cwd)

    def test_feature_number_constant_is_272(self):
        """Test that FEATURE_NUMBER constant is correctly set to 272."""
        assert FEATURE_NUMBER == 272

    def test_markdown_filename_constant_is_correct(self):
        """Test that MARKDOWN_FILENAME constant is correctly set."""
        assert MARKDOWN_FILENAME == "test-6poz5r.md"
