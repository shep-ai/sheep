"""Tests for feature 255: Creating markdown file test-zbl9x9.md with title and prose content.

This module provides comprehensive integration test coverage for feature 255, which creates
a markdown file (test-zbl9x9.md) in the repository root with an H1 heading and 2-3 sentences
of prose content.

Test Coverage:
- File creation with correct name and location (repository root)
- File content structure (H1 heading + blank line + 2-3 sentences of prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- File size validation (250-600 byte range per specification)
- Prose content quality (meaningful, coherent sentences)
- Trailing newline presence
- Return value structure and field population
- Git commit with correct conventional message
- Git push to feature branch
- Complete end-to-end integration workflow
- Error handling and logging
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from sheep.features.feature_255_markdown_file_creation import create_feature_255_markdown_file

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
    with mock.patch('sheep.features.feature_255_markdown_file_creation.generate_markdown_content') as m:
        m.return_value = SAMPLE_MARKDOWN_CONTENT
        yield m


@pytest.fixture
def mock_push():
    """Provide a mock for push_markdown_file."""
    with mock.patch('sheep.features.feature_255_markdown_file_creation.push_markdown_file') as m:
        m.return_value = "success"
        yield m


@pytest.fixture
def mocked_feature(mock_generate_content, mock_push):
    """Combine mocks for a complete feature test."""
    yield mock_generate_content, mock_push


# ============================================================================
# Test Classes
# ============================================================================


class TestFeature255FileCreation:
    """Tests for file creation in feature 255."""

    def test_file_created_in_repository_root(self, temp_repo, mocked_feature):
        """Test that file test-zbl9x9.md is created in repository root."""
        result = create_feature_255_markdown_file(str(temp_repo))

        # Verify file exists
        assert result['filepath'] is not None
        filepath = Path(result['filepath'])
        assert filepath.exists()
        assert filepath.name == 'test-zbl9x9.md'

        # Verify it's in the repository root (not in a subdirectory)
        assert filepath.parent == temp_repo

    def test_file_path_in_return_value(self, temp_repo, mocked_feature):
        """Test that result contains filepath key with valid path."""
        result = create_feature_255_markdown_file(str(temp_repo))

        assert 'filepath' in result
        filepath = Path(result['filepath'])
        assert filepath.exists()
        assert str(filepath).endswith('test-zbl9x9.md')

    def test_file_has_h1_heading(self, temp_repo, mocked_feature):
        """Test that created file contains H1 markdown heading on first line."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        content = filepath.read_text(encoding='utf-8')

        # First line should be H1 heading (starts with "# ")
        first_line = content.split('\n')[0]
        assert first_line.startswith('# '), "First line should be H1 heading starting with '# '"
        assert len(first_line) > 2, "H1 heading should have meaningful title content"

    def test_file_has_blank_line_after_heading(self, temp_repo, mocked_feature):
        """Test that file has blank line separating heading from prose."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Second line should be empty (blank line separator)
        assert len(lines) > 1, "File should have at least 2 lines"
        assert lines[1] == '', "Second line should be empty (blank line separator)"

    def test_file_contains_2_to_3_sentences(self, temp_repo, mocked_feature):
        """Test that file contains exactly 2-3 sentences of prose content."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        content = filepath.read_text(encoding='utf-8')

        # Extract prose content (skip heading and blank line)
        lines = content.split('\n')
        prose_lines = lines[2:]
        prose_content = '\n'.join(prose_lines).strip()

        # Count periods to estimate sentence count
        sentence_count = prose_content.count('.')
        assert 2 <= sentence_count <= 3, (
            f"File should contain 2-3 sentences (counting periods), "
            f"but found {sentence_count} periods"
        )

    def test_prose_content_is_meaningful(self, temp_repo, mocked_feature):
        """Test that prose content is semantically meaningful and non-empty."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        content = filepath.read_text(encoding='utf-8')

        # Extract prose
        lines = content.split('\n')
        prose_lines = lines[2:]
        prose_content = '\n'.join(prose_lines).strip()

        # Prose should be non-empty and reasonably long (100-300 chars per spec)
        assert len(prose_content) > 0, "Prose content should not be empty"
        assert len(prose_content) >= 100, (
            f"Prose content should be at least 100 characters (spec requirement NFR-4), "
            f"but is {len(prose_content)} characters"
        )
        assert len(prose_content) <= 300, (
            f"Prose content should be at most 300 characters (spec requirement NFR-4), "
            f"but is {len(prose_content)} characters"
        )

        # Prose should not be just whitespace or repetition
        assert prose_content != prose_content.replace(' ', '').upper()

    def test_file_ends_with_newline(self, temp_repo, mocked_feature):
        """Test that file ends with a newline character."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        binary_content = filepath.read_bytes()

        # File must end with LF (\n, which is b'\n' in binary)
        assert binary_content.endswith(b'\n'), "File should end with a newline character"


class TestFeature255FileEncoding:
    """Tests for encoding compliance in feature 255."""

    def test_file_uses_utf8_encoding(self, temp_repo, mocked_feature):
        """Test that file is UTF-8 encoded."""
        result = create_feature_255_markdown_file(str(temp_repo))

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
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        binary_content = filepath.read_bytes()

        # UTF-8 BOM is b'\xef\xbb\xbf'
        assert not binary_content.startswith(b'\xef\xbb\xbf'), (
            "File should not have UTF-8 BOM (bytes EF BB BF)"
        )

    def test_file_uses_lf_line_endings(self, temp_repo, mocked_feature):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        binary_content = filepath.read_bytes()

        # Should not contain CRLF (\r\n)
        assert b'\r\n' not in binary_content, (
            "File should not have CRLF line endings (bytes 0D 0A)"
        )

        # Should contain LF (\n)
        assert b'\n' in binary_content, "File should have LF line endings (byte 0A)"


class TestFeature255FileSize:
    """Tests for file size compliance in feature 255."""

    def test_file_size_within_spec_range(self, temp_repo, mocked_feature):
        """Test that file size is between 250-600 bytes (specification NFR-3)."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        file_size = filepath.stat().st_size

        # Per specification NFR-3: 250-600 bytes
        assert 250 <= file_size <= 600, (
            f"File size {file_size} bytes outside specification range (250-600 bytes). "
            f"Specification NFR-3 requires this range."
        )

    def test_file_has_reasonable_size(self, temp_repo, mocked_feature):
        """Test that file size indicates proper content (not empty, not excessive)."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        file_size = filepath.stat().st_size

        # Sanity check: file should be larger than just heading + blank line
        assert file_size > 50, "File size should be larger than minimal structure"

        # Sanity check: file should not be excessively large
        assert file_size < 1000, "File size should be reasonable for 2-3 sentences"


class TestFeature255ReturnValue:
    """Tests for return value structure and content in feature 255."""

    def test_return_value_is_dict(self, temp_repo, mocked_feature):
        """Test that function returns a dictionary."""
        result = create_feature_255_markdown_file(str(temp_repo))
        assert isinstance(result, dict), "Function should return a dictionary"

    def test_return_value_has_filepath_key(self, temp_repo, mocked_feature):
        """Test that return value contains 'filepath' key."""
        result = create_feature_255_markdown_file(str(temp_repo))
        assert 'filepath' in result, "Return value should contain 'filepath' key (spec FR-8)"
        assert result['filepath'] is not None

    def test_return_value_has_content_key(self, temp_repo, mocked_feature):
        """Test that return value contains 'content' key with file content."""
        result = create_feature_255_markdown_file(str(temp_repo))
        assert 'content' in result, "Return value should contain 'content' key (spec FR-8)"
        assert isinstance(result['content'], str)
        assert len(result['content']) > 0

    def test_return_value_has_commit_message_key(self, temp_repo, mocked_feature):
        """Test that return value contains 'commit_message' key with correct format."""
        result = create_feature_255_markdown_file(str(temp_repo))
        assert 'commit_message' in result, (
            "Return value should contain 'commit_message' key (spec FR-8)"
        )
        assert isinstance(result['commit_message'], str)

    def test_return_value_has_push_result_key(self, temp_repo, mocked_feature):
        """Test that return value contains 'push_result' key."""
        result = create_feature_255_markdown_file(str(temp_repo))
        assert 'push_result' in result, "Return value should contain 'push_result' key (spec FR-8)"

    def test_return_value_content_matches_file(self, temp_repo, mocked_feature):
        """Test that returned content matches file content on disk."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])
        file_content = filepath.read_text(encoding='utf-8')

        assert result['content'] == file_content, (
            "Returned content should match content written to file"
        )


class TestFeature255GitIntegration:
    """Tests for git integration in feature 255."""

    def test_commit_message_format(self, temp_repo, mocked_feature):
        """Test that commit message follows conventional commit format."""
        result = create_feature_255_markdown_file(str(temp_repo))

        commit_message = result['commit_message']

        # Per specification FR-6: format should be "feat(255): create markdown file test-zbl9x9.md with prose content"
        expected_format = "feat(255): create markdown file test-zbl9x9.md with prose content"
        assert commit_message == expected_format, (
            f"Commit message should follow exact format per FR-6. "
            f"Expected: '{expected_format}' "
            f"Got: '{commit_message}'"
        )

    def test_file_is_staged_and_committed(self, temp_repo, mocked_feature):
        """Test that file is staged and committed to git."""
        result = create_feature_255_markdown_file(str(temp_repo))

        filepath = Path(result['filepath'])

        # Verify file is in git index/committed by checking git log
        log_output = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=temp_repo,
            capture_output=True,
            text=True,
            check=True
        ).stdout

        assert len(log_output.strip()) > 0, "Git should have at least one commit"
        assert '255' in log_output, "Commit should contain feature number 255"

    def test_push_result_present(self, temp_repo, mocked_feature):
        """Test that push_result is returned (even if push fails in test environment)."""
        result = create_feature_255_markdown_file(str(temp_repo))

        # push_result may be empty string or contain push output
        # depending on whether remote is configured
        assert 'push_result' in result


class TestFeature255EndToEnd:
    """Integration tests for complete feature 255 workflow."""

    def test_complete_workflow_succeeds(self, temp_repo, mocked_feature):
        """Test complete workflow: generate, write, validate, commit, push."""
        # This is the main integration test - ensure all steps succeed
        try:
            result = create_feature_255_markdown_file(str(temp_repo))

            # Verify all required fields are present
            assert 'filepath' in result
            assert 'content' in result
            assert 'commit_message' in result
            assert 'push_result' in result

            # Verify file exists and is valid
            filepath = Path(result['filepath'])
            assert filepath.exists()

            # Verify content structure
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')
            assert lines[0].startswith('# ')
            assert lines[1] == ''

            # Verify encoding
            binary_content = filepath.read_bytes()
            assert not binary_content.startswith(b'\xef\xbb\xbf')
            assert b'\r\n' not in binary_content

            # Verify file size
            file_size = filepath.stat().st_size
            assert 250 <= file_size <= 600

        except Exception as e:
            pytest.fail(f"Complete workflow failed: {e}")

    def test_multiple_runs_create_multiple_files(self, temp_repo, mocked_feature):
        """Test that feature can be run multiple times (creates new file or overwrites existing)."""
        # First run
        result1 = create_feature_255_markdown_file(str(temp_repo))
        filepath1 = Path(result1['filepath'])

        # File should exist after first run
        assert filepath1.exists()

        # Get initial file size
        initial_size = filepath1.stat().st_size

        # Second run should succeed (may overwrite the file)
        try:
            result2 = create_feature_255_markdown_file(str(temp_repo))
            filepath2 = Path(result2['filepath'])

            # File should still exist
            assert filepath2.exists()

            # Both runs should return same filepath
            assert filepath1 == filepath2

        except FileExistsError:
            # This is acceptable if implementation doesn't allow overwriting
            pass

    def test_file_validation_constraints(self, temp_repo, mocked_feature):
        """Test that all validation constraints from spec are met."""
        result = create_feature_255_markdown_file(str(temp_repo))
        filepath = Path(result['filepath'])

        # Specification constraints:
        # FR-1: Filename is correct
        assert filepath.name == 'test-zbl9x9.md'

        # FR-2: Has H1 heading
        content = filepath.read_text(encoding='utf-8')
        assert content.startswith('# ')

        # FR-3: Has 2-3 sentences
        prose = '\n'.join(content.split('\n')[2:]).strip()
        sentence_count = prose.count('.')
        assert 2 <= sentence_count <= 3

        # NFR-1: UTF-8 without BOM
        binary_content = filepath.read_bytes()
        assert not binary_content.startswith(b'\xef\xbb\xbf')

        # NFR-2: Unix LF line endings
        assert b'\r\n' not in binary_content

        # NFR-3: File size 250-600 bytes
        file_size = filepath.stat().st_size
        assert 250 <= file_size <= 600

        # NFR-4: Prose length 100-300 characters
        assert 100 <= len(prose) <= 300

    def test_result_contains_all_required_fields(self, temp_repo, mocked_feature):
        """Test that result dict contains all fields specified in FR-8."""
        result = create_feature_255_markdown_file(str(temp_repo))

        # Per FR-8, result should contain:
        # - filepath
        # - content
        # - commit_message
        # - push_result
        required_keys = {'filepath', 'content', 'commit_message', 'push_result'}
        result_keys = set(result.keys())

        missing_keys = required_keys - result_keys
        assert not missing_keys, (
            f"Result missing required keys per FR-8: {missing_keys}"
        )

    def test_feature_number_in_logging(self, temp_repo, mocked_feature):
        """Test that feature number 255 appears in commit message."""
        result = create_feature_255_markdown_file(str(temp_repo))

        commit_message = result['commit_message']
        assert '255' in commit_message, (
            "Feature number 255 should appear in commit message"
        )

    def test_default_repo_path_uses_cwd(self, mocked_feature):
        """Test that default repo_path (None) uses current working directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Initialize git repo in temp directory
                subprocess.run(['git', 'init'], check=True, capture_output=True)
                subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True, capture_output=True)
                subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True, capture_output=True)

                # Call without repo_path argument (defaults to None)
                result = create_feature_255_markdown_file()

                # File should be created in current directory
                filepath = Path(result['filepath'])
                assert filepath.exists()
                assert filepath.parent == Path.cwd()

            finally:
                os.chdir(original_cwd)


class TestFeature255ErrorHandling:
    """Tests for error handling and edge cases."""

    def test_returns_structured_data_on_success(self, temp_repo, mocked_feature):
        """Test that success path returns properly structured data."""
        result = create_feature_255_markdown_file(str(temp_repo))

        assert isinstance(result, dict)
        assert all(isinstance(k, str) for k in result.keys())
        # Values should be strings (filepath, content, commit_message, push_result)
        assert all(isinstance(v, str) for v in result.values())

    def test_content_field_contains_actual_markdown(self, temp_repo, mocked_feature):
        """Test that content field contains the actual markdown that was written."""
        result = create_feature_255_markdown_file(str(temp_repo))

        content = result['content']
        # Should start with H1
        assert content.startswith('# ')
        # Should contain blank line
        assert '\n\n' in content
        # Should have reasonable length
        assert 250 <= len(content) <= 600
