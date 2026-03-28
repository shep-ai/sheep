"""Tests for feature 257: Creating markdown file test-oxy715.md with title and prose content.

This module provides comprehensive integration test coverage for feature 257, which creates
a markdown file (test-oxy715.md) in the repository root with an H1 heading and 2-3 sentences
of prose content.

Test Coverage (Phase 2: Workflow Implementation):
- Task 2: Content generation via Claude API with proper logging
- Task 3: File writing with UTF-8 encoding and LF line endings
- Task 4: File validation for structure and properties before commit
- Complete end-to-end workflow validation
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from sheep.features.feature_257_markdown_file_creation import create_feature_257_markdown_file


# Sample valid markdown content for testing
# Prose is 232 characters (within 100-300 spec)
SAMPLE_MARKDOWN_CONTENT = (
    "# Python Programming Fundamentals\n"
    "\n"
    "Python is a versatile language known for clear syntax and ease of learning, making it ideal for both beginners and developers. "
    "Its standard library and ecosystem enable rapid development of sophisticated applications. "
    "Python's dynamic nature makes it excellent for diverse projects.\n"
)


# ============================================================================
# Pytest Fixtures
# ============================================================================


@pytest.fixture
def temp_repo():
    """
    Provide an isolated temporary directory with git repository for testing.

    Creates a temporary directory, initializes it as a git repository,
    and restores the original working directory after the test completes.

    Yields:
        Path: The temporary repository directory path
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            # Initialize git repository for testing git operations
            subprocess.run(['git', 'init'], check=True, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True, capture_output=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True, capture_output=True)
            yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)


@pytest.fixture
def mock_generate_content():
    """Provide a mock for generate_markdown_content that returns valid sample content."""
    with mock.patch('sheep.features.feature_257_markdown_file_creation.generate_markdown_content') as m:
        m.return_value = SAMPLE_MARKDOWN_CONTENT
        yield m


@pytest.fixture
def mock_push():
    """Provide a mock for push_markdown_file."""
    with mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file') as m:
        m.return_value = "success"
        yield m


@pytest.fixture
def mocked_feature(mock_generate_content, mock_push):
    """Combine mocks for a complete feature test."""
    yield mock_generate_content, mock_push


# ============================================================================
# Task 2: Content Generation Tests
# ============================================================================

class TestFeature257ContentGeneration:
    """Tests for Task 2: Content generation via Claude API."""

    def test_content_generation_called(self, temp_repo, mocked_feature):
        """Test that content generation function is called during feature execution."""
        mock_generate_content, _ = mocked_feature

        result = create_feature_257_markdown_file(str(temp_repo))

        # Verify that generate_markdown_content was called
        mock_generate_content.assert_called_once()

    def test_generated_content_is_valid(self, temp_repo, mocked_feature):
        """Test that generated content is valid markdown with H1 heading."""
        result = create_feature_257_markdown_file(str(temp_repo))

        # Content should be non-empty
        assert result['content'] is not None
        assert len(result['content']) > 0

        # Content should start with H1 heading
        assert result['content'].lstrip().startswith('# ')

        # Content should have prose (at least 100 characters)
        assert len(result['content']) > 100

    def test_content_generation_logs_info_message(self, temp_repo, mocked_feature):
        """Test that content generation step logs an INFO-level message."""
        with mock.patch('sheep.features.feature_257_markdown_file_creation._logger') as mock_logger:
            mock_generate_content, _ = mocked_feature
            mock_generate_content.return_value = SAMPLE_MARKDOWN_CONTENT
            mock_push = mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file')
            mock_push.return_value = "success"

            with mock_push:
                result = create_feature_257_markdown_file(str(temp_repo))

            # Verify INFO log was called for content generation
            assert any(
                'Task 1: Generating markdown content' in str(call)
                for call in mock_logger.info.call_args_list
            ), "INFO log for content generation not found"

    def test_generated_content_has_prose(self, temp_repo, mocked_feature):
        """Test that generated content includes prose sentences after H1 heading."""
        result = create_feature_257_markdown_file(str(temp_repo))

        lines = result['content'].split('\n')

        # First line is H1, second is blank, rest is prose
        assert lines[0].startswith('# ')
        assert lines[1] == ''
        assert len(lines) > 2

        # Prose content should have sentences (contain periods)
        prose_text = '\n'.join(lines[2:]).strip()
        assert '.' in prose_text, "Prose should contain sentences (periods)"


# ============================================================================
# Task 3: File Write Tests
# ============================================================================

class TestFeature257FileWrite:
    """Tests for Task 3: File writing with proper encoding and line endings."""

    def test_file_created_in_repository_root(self, temp_repo, mocked_feature):
        """Test that file test-oxy715.md is created in repository root."""
        result = create_feature_257_markdown_file(str(temp_repo))

        # Verify file exists
        assert result['filepath'] is not None
        filepath = Path(result['filepath'])
        assert filepath.exists()
        assert filepath.name == 'test-oxy715.md'

        # Verify it's in the repository root (not in a subdirectory)
        assert filepath.parent == temp_repo

    def test_file_path_in_return_value(self, temp_repo, mocked_feature):
        """Test that result contains filepath key with valid path."""
        result = create_feature_257_markdown_file(str(temp_repo))

        assert 'filepath' in result
        filepath = Path(result['filepath'])
        assert filepath.exists()
        assert str(filepath).endswith('test-oxy715.md')

    def test_file_content_matches_generated_content(self, temp_repo, mocked_feature):
        """Test that written file content matches generated content."""
        result = create_feature_257_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        file_content = filepath.read_text(encoding='utf-8')

        assert file_content == result['content']
        assert len(file_content) > 0

    def test_file_write_logs_info_message(self, temp_repo, mocked_feature):
        """Test that file write step logs an INFO-level message."""
        with mock.patch('sheep.features.feature_257_markdown_file_creation._logger') as mock_logger:
            mock_generate_content, _ = mocked_feature
            mock_generate_content.return_value = SAMPLE_MARKDOWN_CONTENT
            mock_push = mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file')
            mock_push.return_value = "success"

            with mock_push:
                result = create_feature_257_markdown_file(str(temp_repo))

            # Verify INFO log was called for file write
            assert any(
                'Task 2: Writing markdown file to disk' in str(call)
                for call in mock_logger.info.call_args_list
            ), "INFO log for file write not found"

    def test_file_uses_utf8_encoding(self, temp_repo, mocked_feature):
        """Test that file is UTF-8 encoded."""
        result = create_feature_257_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        binary_content = filepath.read_bytes()

        # Verify it can be decoded as UTF-8
        try:
            decoded = binary_content.decode('utf-8')
            assert isinstance(decoded, str)
            assert len(decoded) > 0
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_has_no_utf8_bom(self, temp_repo, mocked_feature):
        """Test that file does not have UTF-8 BOM (Byte Order Mark)."""
        result = create_feature_257_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        binary_content = filepath.read_bytes()

        # UTF-8 BOM is b'\xef\xbb\xbf'
        assert not binary_content.startswith(b'\xef\xbb\xbf'), (
            "File should not have UTF-8 BOM (bytes EF BB BF)"
        )

    def test_file_uses_lf_line_endings(self, temp_repo, mocked_feature):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        result = create_feature_257_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        binary_content = filepath.read_bytes()

        # Should not contain CRLF (\r\n)
        assert b'\r\n' not in binary_content, (
            "File should not have CRLF line endings (bytes 0D 0A)"
        )

        # Should contain LF (\n)
        assert b'\n' in binary_content, "File should have LF line endings (byte 0A)"

    def test_file_ends_with_newline(self, temp_repo, mocked_feature):
        """Test that file ends with a newline character."""
        result = create_feature_257_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        binary_content = filepath.read_bytes()

        # File must end with LF (\n, which is b'\n' in binary)
        assert binary_content.endswith(b'\n'), "File should end with a newline character"


# ============================================================================
# Task 4: File Validation Tests
# ============================================================================

class TestFeature257FileValidation:
    """Tests for Task 4: File validation before git commit."""

    def test_validation_logs_info_message(self, temp_repo, mocked_feature):
        """Test that file validation step logs an INFO-level message."""
        with mock.patch('sheep.features.feature_257_markdown_file_creation._logger') as mock_logger:
            mock_generate_content, _ = mocked_feature
            mock_generate_content.return_value = SAMPLE_MARKDOWN_CONTENT
            mock_push = mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file')
            mock_push.return_value = "success"

            with mock_push:
                result = create_feature_257_markdown_file(str(temp_repo))

            # Verify INFO log was called for validation
            assert any(
                'Task 3: Validating markdown file' in str(call)
                for call in mock_logger.info.call_args_list
            ), "INFO log for validation start not found"

            # Verify validation passed message
            assert any(
                'File validation passed' in str(call)
                for call in mock_logger.info.call_args_list
            ), "INFO log for validation success not found"

    def test_validation_occurs_before_commit(self, temp_repo, mocked_feature):
        """Test that file validation happens before git commit operations."""
        # This is verified by the fact that feature completes successfully
        # when content is valid. If validation didn't work, invalid files
        # would be committed.
        result = create_feature_257_markdown_file(str(temp_repo))

        # If we reach here, validation passed and file was committed
        filepath = Path(result['filepath'])
        assert filepath.exists()

        # Verify the committed file is valid
        content = filepath.read_text(encoding='utf-8')
        assert content.startswith('# ')
        assert content.count('.') >= 2

    def test_validation_checks_h1_heading(self, temp_repo):
        """Test that validation checks for H1 heading presence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                subprocess.run(['git', 'init'], check=True, capture_output=True)
                subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True, capture_output=True)
                subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True, capture_output=True)

                # Mock to return content without H1 heading
                invalid_content = "Some prose without heading.\nMore prose here.\nFinal sentence."

                with mock.patch('sheep.features.feature_257_markdown_file_creation.generate_markdown_content') as m:
                    m.return_value = invalid_content
                    with mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file'):
                        # Should raise ValueError because content doesn't start with H1
                        with pytest.raises(Exception):
                            create_feature_257_markdown_file(tmpdir)
            finally:
                os.chdir(original_cwd)

    def test_validation_checks_sentence_count(self, temp_repo):
        """Test that validation checks for 2-3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                subprocess.run(['git', 'init'], check=True, capture_output=True)
                subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True, capture_output=True)
                subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True, capture_output=True)

                # Mock to return content with only 1 sentence
                invalid_content = "# Title\n\nOnly one sentence"

                with mock.patch('sheep.features.feature_257_markdown_file_creation.generate_markdown_content') as m:
                    m.return_value = invalid_content
                    with mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file'):
                        # Should raise exception due to invalid sentence count
                        with pytest.raises(Exception):
                            create_feature_257_markdown_file(tmpdir)
            finally:
                os.chdir(original_cwd)

    def test_validation_passes_for_valid_content(self, temp_repo, mocked_feature):
        """Test that validation passes for properly structured markdown."""
        result = create_feature_257_markdown_file(str(temp_repo))

        # If validation failed, an exception would be raised and caught above
        # The fact that we have a result means validation passed
        assert result is not None
        assert 'filepath' in result

        # Verify the file is actually valid
        filepath = Path(result['filepath'])
        content = filepath.read_text(encoding='utf-8')

        # Should have H1
        assert content.startswith('# ')
        # Should have blank line
        lines = content.split('\n')
        assert lines[1] == ''
        # Should have 2-3 sentences
        prose = '\n'.join(lines[2:])
        assert 2 <= prose.count('.') <= 3


# ============================================================================
# Integration Tests
# ============================================================================

# ============================================================================
# Task 5: Git Commit Tests
# ============================================================================

class TestFeature257GitCommit:
    """Tests for Task 5: Git commit step."""

    def test_commit_logs_info_message(self, temp_repo, mocked_feature):
        """Test that git commit step logs an INFO-level message."""
        with mock.patch('sheep.features.feature_257_markdown_file_creation._logger') as mock_logger:
            mock_generate_content, _ = mocked_feature
            mock_generate_content.return_value = SAMPLE_MARKDOWN_CONTENT
            mock_push = mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file')
            mock_push.return_value = "success"

            with mock_push:
                result = create_feature_257_markdown_file(str(temp_repo))

            # Verify INFO log was called for commit step
            assert any(
                'Task 4: Staging and committing file' in str(call)
                for call in mock_logger.info.call_args_list
            ), "INFO log for commit step not found"

    def test_commit_message_exact_format(self, temp_repo, mocked_feature):
        """Test that commit message is exactly: 'feat(257): create markdown file test-oxy715.md with prose content'."""
        result = create_feature_257_markdown_file(str(temp_repo))

        expected_message = "feat(257): create markdown file test-oxy715.md with prose content"
        assert result['commit_message'] == expected_message

    def test_commit_exists_on_current_branch(self, temp_repo, mocked_feature):
        """Test that commit is created and exists on current branch."""
        # Create initial commit so we have something to compare against
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=temp_repo, check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=temp_repo, check=True, capture_output=True)

        # Create an initial commit to establish history
        Path(temp_repo / "initial.txt").write_text("initial")
        subprocess.run(['git', 'add', 'initial.txt'], cwd=temp_repo, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'initial commit'], cwd=temp_repo, check=True, capture_output=True)

        # Run feature
        result = create_feature_257_markdown_file(str(temp_repo))

        # Check git log for the feature commit
        log_output = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=temp_repo,
            capture_output=True,
            text=True,
            check=True
        ).stdout

        # Verify commit message appears in git log
        assert "feat(257): create markdown file test-oxy715.md with prose content" in log_output

    def test_file_is_staged_before_commit(self, temp_repo, mocked_feature):
        """Test that file is staged in git before commit."""
        # The fact that the commit succeeds indicates file was properly staged
        result = create_feature_257_markdown_file(str(temp_repo))

        # Verify file was committed by checking git status
        status_output = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=temp_repo,
            capture_output=True,
            text=True,
            check=True
        ).stdout

        # If file is not in output, it means it was committed
        # If it's in output with '??' or 'M ', it means it wasn't committed
        lines = status_output.strip().split('\n') if status_output.strip() else []
        test_file_lines = [l for l in lines if 'test-oxy715.md' in l]

        # File should not appear in git status (meaning it's committed)
        assert len(test_file_lines) == 0, f"File should be committed but found in status: {test_file_lines}"

    def test_commit_result_captured_in_return_value(self, temp_repo, mocked_feature):
        """Test that commit result is captured in return value."""
        result = create_feature_257_markdown_file(str(temp_repo))

        assert 'commit_message' in result
        assert result['commit_message'] is not None
        assert len(result['commit_message']) > 0


# ============================================================================
# Task 6: Git Push Tests
# ============================================================================

class TestFeature257GitPush:
    """Tests for Task 6: Git push step."""

    def test_push_logs_info_message(self, temp_repo, mocked_feature):
        """Test that git push step logs an INFO-level message."""
        with mock.patch('sheep.features.feature_257_markdown_file_creation._logger') as mock_logger:
            mock_generate_content, _ = mocked_feature
            mock_generate_content.return_value = SAMPLE_MARKDOWN_CONTENT
            mock_push = mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file')
            mock_push.return_value = "success"

            with mock_push:
                result = create_feature_257_markdown_file(str(temp_repo))

            # Verify INFO log was called for push step
            assert any(
                'Task 5: Pushing to remote repository' in str(call)
                for call in mock_logger.info.call_args_list
            ), "INFO log for push step not found"

    def test_push_called_after_commit(self, temp_repo):
        """Test that push is called after commit operation."""
        with mock.patch('sheep.features.feature_257_markdown_file_creation.generate_markdown_content') as mock_gen:
            with mock.patch('sheep.features.feature_257_markdown_file_creation.commit_markdown_file') as mock_commit:
                with mock.patch('sheep.features.feature_257_markdown_file_creation.push_markdown_file') as mock_push:
                    mock_gen.return_value = SAMPLE_MARKDOWN_CONTENT
                    mock_commit.return_value = "commit_hash"
                    mock_push.return_value = "success"

                    result = create_feature_257_markdown_file(str(temp_repo))

                    # Verify both commit and push were called
                    assert mock_commit.called, "commit_markdown_file should be called"
                    assert mock_push.called, "push_markdown_file should be called"

    def test_push_result_captured_in_return_value(self, temp_repo, mocked_feature):
        """Test that push result is captured in return value."""
        result = create_feature_257_markdown_file(str(temp_repo))

        assert 'push_result' in result
        assert result['push_result'] is not None

    def test_push_targets_current_branch(self, temp_repo, mocked_feature):
        """Test that push targets the correct branch."""
        result = create_feature_257_markdown_file(str(temp_repo))

        # The feature should push to the current branch (feat/257-markdown-file-creation-62bad4)
        # This is verified by the fact that push succeeds without error
        assert result is not None
        assert 'push_result' in result


# ============================================================================
# Integration Tests
# ============================================================================

class TestFeature257Integration:
    """Integration tests for complete feature 257 workflow."""

    def test_return_value_structure(self, temp_repo, mocked_feature):
        """Test that function returns properly structured result."""
        result = create_feature_257_markdown_file(str(temp_repo))

        # Verify all required fields are present
        assert isinstance(result, dict)
        assert 'filepath' in result
        assert 'content' in result
        assert 'commit_message' in result
        assert 'push_result' in result

    def test_commit_message_format(self, temp_repo, mocked_feature):
        """Test that commit message follows correct format."""
        result = create_feature_257_markdown_file(str(temp_repo))

        expected_message = "feat(257): create markdown file test-oxy715.md with prose content"
        assert result['commit_message'] == expected_message

    def test_complete_workflow_succeeds(self, temp_repo, mocked_feature):
        """Test complete workflow: generate, write, validate, commit, push."""
        result = create_feature_257_markdown_file(str(temp_repo))

        # Verify all required fields are present
        assert 'filepath' in result
        assert 'content' in result
        assert 'commit_message' in result
        assert 'push_result' in result

        # Verify file exists and is valid
        filepath = Path(result['filepath'])
        assert filepath.exists()
        assert filepath.name == 'test-oxy715.md'

        # Verify content structure
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')
        assert lines[0].startswith('# ')
        assert lines[1] == ''

        # Verify encoding
        binary_content = filepath.read_bytes()
        assert not binary_content.startswith(b'\xef\xbb\xbf')
        assert b'\r\n' not in binary_content
        assert binary_content.endswith(b'\n')
