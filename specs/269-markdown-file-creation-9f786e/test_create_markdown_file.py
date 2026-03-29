"""
Comprehensive test suite for markdown file creation with Claude API content generation.

This module provides comprehensive test coverage for feature 269, which creates
a markdown file (test-hb8tyt.md) with auto-generated content from Claude API,
proper structure, encoding, and line endings.

Test Coverage:
- Content generation (Claude API) with mocking
- File creation with correct structure (H1 heading + blank line + prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- File size validation (400-600 byte range, tolerance 300-800)
- Prose content validation (2-3 sentences)
- Trailing newline validation
- Validation function behavior (success and failure paths)
- Integration tests (complete workflow)
- Error handling and informative error messages

The test suite uses pytest fixtures, mocks, and helper functions to create
isolated test environments and comprehensive validation testing.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Import the functions from the script
script_path = Path(__file__).parent / "create_markdown_file.py"
sys.path.insert(0, str(Path(__file__).parent))
from create_markdown_file import (
    create_file,
    generate_content,
    git_operations,
    validate_file,
)

# ============================================================================
# Pytest Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """
    Provide an isolated temporary directory for test file creation.

    Yields a temporary directory path and restores the original working
    directory after the test completes. This fixture ensures tests don't
    interfere with the repository state or each other.

    Yields:
        Path: The temporary directory path
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)


@pytest.fixture
def mock_claude_response():
    """
    Provide a mock Claude API response for testing content generation.

    Returns:
        dict: Mock response object with generated content
    """
    return {
        "content": [
            {
                "type": "text",
                "text": "The Power of Iteration\n\nIteration is a fundamental principle in software development that drives improvement through repeated cycles of design, implementation, and refinement. Each iteration builds upon the previous one, incorporating feedback and lessons learned to refine approaches and achieve better outcomes. By embracing iterative processes, teams can adapt to changing requirements and deliver increasingly valuable solutions with greater confidence and quality."
            }
        ]
    }


@pytest.fixture
def sample_markdown():
    """
    Provide a sample valid markdown file content for testing.

    Returns:
        dict: Dictionary with 'content' and 'filename' keys containing valid markdown
    """
    content = (
        "# Sample Title\n"
        "\n"
        "First sentence of the prose content here. "
        "Second sentence explaining the topic more thoroughly. "
        "Third sentence concluding the thought.\n"
    )
    return {"content": content, "filename": "sample.md"}


# ============================================================================
# Helper Functions
# ============================================================================


def create_invalid_file(temp_dir, invalid_type="missing_heading"):
    """
    Create a markdown file with specific validation errors for testing.

    This helper function creates test files with various structural issues
    to verify that the validate_file() function correctly rejects invalid files.

    Args:
        temp_dir (Path): The temporary directory where file will be created
        invalid_type (str): Type of invalid file to create. Options:
            - 'missing_heading': No H1 heading
            - 'missing_blank_line': No blank line after heading
            - 'empty_prose': Blank line + heading but no prose content
            - 'too_small': File size under 300 bytes
            - 'too_large': File size over 800 bytes
            - 'with_crlf': Windows-style line endings
            - 'with_bom': UTF-8 BOM encoding

    Returns:
        Path: Path to the created invalid file

    Raises:
        ValueError: If invalid_type is not recognized
    """
    filepath = temp_dir / "invalid_test.md"

    if invalid_type == "missing_heading":
        content = "## Wrong Level\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "missing_blank_line":
        prose = "This is prose content that should have a blank line before it. " * 5
        content = f"# Title\n{prose}\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "empty_prose":
        # Create a file with proper heading and blank line but only whitespace for prose
        # Ensure file is large enough to pass size check (>300 bytes)
        content = "# Title\n\n" + " " * 300 + "\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "too_small":
        content = "# T\n\nS.\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "too_large":
        prose = "This is a sentence. " * 60
        content = f"# Title\n\n{prose}\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "with_crlf":
        content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
        filepath.write_bytes(content.encode('utf-8'))

    elif invalid_type == "with_bom":
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        # Write with BOM using utf-8-sig encoding
        filepath.write_bytes(content.encode('utf-8-sig'))

    else:
        raise ValueError(f"Unknown invalid_type: {invalid_type}")

    return filepath


# ============================================================================
# Test Classes
# ============================================================================


class TestGenerateContent:
    """Tests for generate_content() function."""

    def test_generate_content_returns_tuple(self):
        """Test that generate_content() returns a tuple of (title, prose)."""
        with mock.patch("create_markdown_file.Anthropic") as mock_anthropic:
            # Mock the Claude API response
            mock_client = mock.Mock()
            mock_anthropic.return_value = mock_client

            mock_response = mock.Mock()
            mock_response.content = [
                mock.Mock(
                    text="The Power of Iteration\n\nIteration is a fundamental principle. Each iteration builds upon the previous one. By embracing iterative processes, teams adapt to changing requirements."
                )
            ]
            mock_client.messages.create.return_value = mock_response

            with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
                result = generate_content()

                assert isinstance(result, tuple), "generate_content() should return a tuple"
                assert len(result) == 2, "Tuple should have 2 elements (title, prose)"
                title, prose = result
                assert isinstance(title, str), "Title should be a string"
                assert isinstance(prose, str), "Prose should be a string"

    def test_generated_title_is_single_phrase(self):
        """Test that generated title is 1-5 words suitable for H1 heading."""
        with mock.patch("create_markdown_file.Anthropic") as mock_anthropic:
            mock_client = mock.Mock()
            mock_anthropic.return_value = mock_client

            mock_response = mock.Mock()
            mock_response.content = [
                mock.Mock(
                    text="The Power of Iteration\n\nIteration is fundamental. Each iteration builds. By embracing iterative processes, teams adapt."
                )
            ]
            mock_client.messages.create.return_value = mock_response

            with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
                title, prose = generate_content()

                # Title should be short (1-5 words)
                word_count = len(title.split())
                assert 1 <= word_count <= 5, f"Title should be 1-5 words, got {word_count}: '{title}'"

    def test_generated_prose_has_sentences(self):
        """Test that generated prose contains multiple sentences."""
        with mock.patch("create_markdown_file.Anthropic") as mock_anthropic:
            mock_client = mock.Mock()
            mock_anthropic.return_value = mock_client

            mock_response = mock.Mock()
            mock_response.content = [
                mock.Mock(
                    text="The Power of Iteration\n\nIteration is fundamental principle in software development. Each iteration builds upon previous one with feedback. By embracing iterative processes, teams adapt to changing requirements effectively."
                )
            ]
            mock_client.messages.create.return_value = mock_response

            with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
                title, prose = generate_content()

                # Prose should contain periods (sentences)
                period_count = prose.count('.')
                assert period_count >= 2, f"Prose should contain at least 2 sentences, found {period_count}"

    def test_generate_content_handles_missing_api_key(self):
        """Test that generate_content() provides clear error if ANTHROPIC_API_KEY not set."""
        # Save original API key if it exists
        original_key = os.environ.pop("ANTHROPIC_API_KEY", None)

        try:
            # Verify API key is not set
            assert "ANTHROPIC_API_KEY" not in os.environ

            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                generate_content()

        finally:
            # Restore original API key if it was set
            if original_key:
                os.environ["ANTHROPIC_API_KEY"] = original_key

    def test_generate_content_calls_claude_api(self):
        """Test that generate_content() actually calls Claude API with correct parameters."""
        with mock.patch("create_markdown_file.Anthropic") as mock_anthropic:
            mock_client = mock.Mock()
            mock_anthropic.return_value = mock_client

            mock_response = mock.Mock()
            mock_response.content = [
                mock.Mock(
                    text="Test Title\n\nFirst sentence. Second sentence. Third sentence."
                )
            ]
            mock_client.messages.create.return_value = mock_response

            # Mock the API key
            with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
                title, prose = generate_content()

                # Verify Claude API was called
                mock_client.messages.create.assert_called_once()

                # Verify the call includes required parameters
                call_args = mock_client.messages.create.call_args
                assert call_args[1]["model"] == "claude-3-5-sonnet-20241022"
                assert call_args[1]["max_tokens"] == 300
                assert "messages" in call_args[1]


class TestCreateFile:
    """Tests for create_file() function."""

    def test_creates_file_at_repository_root(self, temp_dir):
        """Test that create_file() creates test-hb8tyt.md in the repository root."""
        filepath = create_file("Test Title", "First sentence. Second sentence. Third sentence.")

        assert filepath.exists(), "File should be created"
        assert filepath.name == "test-hb8tyt.md", "File should be named test-hb8tyt.md"

    def test_file_contains_h1_heading(self, temp_dir):
        """Test that file contains H1 markdown heading on first line."""
        create_file("Test Title", "First sentence. Second sentence. Third sentence.")

        content = Path("test-hb8tyt.md").read_text(encoding='utf-8')
        assert content.startswith("# "), "File should start with H1 heading"
        assert "Test Title" in content, "File should contain the title"

    def test_file_contains_prose_content(self, temp_dir):
        """Test that file contains the provided prose content."""
        prose = "First sentence. Second sentence. Third sentence."
        create_file("Test Title", prose)

        content = Path("test-hb8tyt.md").read_text(encoding='utf-8')
        assert prose in content, "File should contain the provided prose"

    def test_file_uses_utf8_encoding(self, temp_dir):
        """Test that file is UTF-8 encoded."""
        create_file("Test Title", "First sentence. Second sentence. Third sentence.")

        # Read as binary
        binary_content = Path("test-hb8tyt.md").read_bytes()

        # Verify it can be decoded as UTF-8
        try:
            decoded = binary_content.decode('utf-8')
            assert isinstance(decoded, str)
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    def test_file_has_no_utf8_bom(self, temp_dir):
        """Test that file does not have UTF-8 BOM (Byte Order Mark)."""
        create_file("Test Title", "First sentence. Second sentence. Third sentence.")

        binary_content = Path("test-hb8tyt.md").read_bytes()
        # UTF-8 BOM is b'\xef\xbb\xbf'
        assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"

    def test_file_uses_lf_line_endings(self, temp_dir):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        create_file("Test Title", "First sentence. Second sentence. Third sentence.")

        binary_content = Path("test-hb8tyt.md").read_bytes()
        # Should not contain CRLF (\r\n)
        assert b'\r\n' not in binary_content, "File should not have CRLF line endings"
        # Should contain LF (\n)
        assert b'\n' in binary_content, "File should have LF line endings"

    def test_file_size_in_typical_range(self, temp_dir):
        """Test that file size is approximately 400-600 bytes."""
        # Create prose that results in ~500 byte file
        prose = "Iteration is a fundamental principle in software development that drives improvement and excellence through repeated cycles. Each iteration builds upon the previous one, incorporating valuable feedback and lessons learned to refine approaches. By embracing iterative processes, teams can adapt to changing requirements and deliver increasingly valuable solutions with greater confidence."
        create_file("Test Title", prose)

        file_size = Path("test-hb8tyt.md").stat().st_size
        # Soft guideline: typically 400-600 bytes
        # We tolerate a range of 300-800 bytes for flexibility
        assert 300 < file_size < 800, (
            f"File size {file_size} bytes outside typical range (300-800). "
            f"Expected 400-600 as soft guideline."
        )

    def test_file_contains_blank_line_after_heading(self, temp_dir):
        """Test that file has blank line separating heading from prose."""
        create_file("Test Title", "First sentence. Second sentence. Third sentence.")

        content = Path("test-hb8tyt.md").read_text(encoding='utf-8')
        # Should contain double newline (blank line)
        assert '\n\n' in content, "File should contain blank line after heading"

    def test_returns_path_object(self, temp_dir):
        """Test that create_file() returns a Path object."""
        result = create_file("Test Title", "First sentence. Second sentence. Third sentence.")

        assert isinstance(result, Path), "Return value should be a Path object"
        assert result.name == "test-hb8tyt.md", "Path should point to test-hb8tyt.md"

    def test_file_ends_with_newline(self, temp_dir):
        """Test that file ends with a newline character."""
        create_file("Test Title", "First sentence. Second sentence. Third sentence.")

        binary_content = Path("test-hb8tyt.md").read_bytes()
        # File must end with LF (\n, which is b'\n' in binary)
        assert binary_content.endswith(b'\n'), "File should end with a newline character"


class TestValidateFile:
    """Tests for validate_file() function."""

    def test_validates_correctly_created_file(self, temp_dir):
        """Test that validate_file() passes for a correctly created file."""
        prose = "Iteration is a fundamental principle in software development that drives improvement and excellence. Each iteration builds upon the previous one, incorporating feedback and lessons learned. By embracing iterative processes, teams adapt to changing requirements and deliver valuable solutions."
        filepath = create_file("Test Title", prose)

        result = validate_file(filepath)
        assert result is True, "Validation should pass for correctly created file"

    def test_rejects_missing_file(self):
        """Test that validate_file() raises error for non-existent file."""
        nonexistent_path = Path("nonexistent.md")

        with pytest.raises(AssertionError, match="does not exist"):
            validate_file(nonexistent_path)

    def test_rejects_file_too_small(self, temp_dir):
        """Test that validate_file() rejects file smaller than 300 bytes."""
        path = Path("test-hb8tyt.md")
        # Create very small file
        content = "# Title\n\nSmall.\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="outside typical range"):
            validate_file(path)

    def test_rejects_file_too_large(self, temp_dir):
        """Test that validate_file() rejects file larger than 800 bytes."""
        path = Path("test-hb8tyt.md")
        # Create very large file
        large_prose = "This is a sentence. " * 50  # Creates very long content
        content = f"# Title\n\n{large_prose}\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="outside typical range"):
            validate_file(path)

    def test_rejects_missing_h1_heading(self, temp_dir):
        """Test that validate_file() rejects file without H1 heading."""
        path = Path("test-hb8tyt.md")
        # No heading
        content = "## Second Level\n\nFirst sentence. Second sentence. Third sentence.\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="H1 heading"):
            validate_file(path)

    def test_rejects_missing_blank_line(self, temp_dir):
        """Test that validate_file() rejects file without blank line after heading."""
        path = Path("test-hb8tyt.md")
        # No blank line between heading and prose
        prose = "Artificial intelligence is transforming industries. Machine learning models are becoming sophisticated. Organizations are leveraging technologies. The integration of AI systems has become standard practice."
        content = f"# Title\n{prose}\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="blank line"):
            validate_file(path)

    def test_rejects_empty_prose(self, temp_dir):
        """Test that validate_file() rejects file with no prose content."""
        path = Path("test-hb8tyt.md")
        # Test with proper structure but prose is just whitespace
        content = "# Title\n\n" + " " * 300 + "\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="prose"):
            validate_file(path)

    def test_rejects_file_with_bom(self, temp_dir):
        """Test that validate_file() rejects file with UTF-8 BOM."""
        path = Path("test-hb8tyt.md")
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        path.write_bytes(content.encode('utf-8-sig'))

        with pytest.raises(AssertionError, match="BOM"):
            validate_file(path)

    def test_rejects_file_with_crlf(self, temp_dir):
        """Test that validate_file() rejects file with Windows CRLF line endings."""
        path = Path("test-hb8tyt.md")
        content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
        path.write_bytes(content.encode('utf-8'))

        with pytest.raises(AssertionError, match="Unix LF"):
            validate_file(path)


class TestIntegration:
    """Integration tests for content generation, file creation, and validation."""

    def test_generate_create_validate_workflow(self, temp_dir):
        """Test complete workflow: generate content, create file, and validate it."""
        with mock.patch("create_markdown_file.Anthropic") as mock_anthropic:
            # Mock Claude API
            mock_client = mock.Mock()
            mock_anthropic.return_value = mock_client

            mock_response = mock.Mock()
            mock_response.content = [
                mock.Mock(
                    text="The Power of Iteration\n\nIteration is a fundamental principle in software development that drives improvement and excellence through repeated cycles of design and refinement. Each iteration builds upon the previous one, incorporating valuable feedback and lessons learned. By embracing iterative processes, teams adapt to changing requirements and deliver increasingly valuable solutions."
                )
            ]
            mock_client.messages.create.return_value = mock_response

            with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
                # Generate content
                title, prose = generate_content()
                assert title, "Should generate title"
                assert prose, "Should generate prose"

                # Create file
                filepath = create_file(title, prose)
                assert filepath.exists(), "File should exist"

                # Validate file
                result = validate_file(filepath)
                assert result is True, "Validation should pass"

    def test_multiple_validations_pass(self, temp_dir):
        """Test that a created file passes validation multiple times."""
        prose = "Iteration is a fundamental principle in software development that drives improvement and excellence through repeated cycles of design, implementation, and refinement. Each iteration builds upon the previous one, incorporating valuable feedback and lessons learned to refine approaches. By embracing iterative processes, teams can adapt to changing requirements and deliver increasingly valuable solutions with greater confidence and quality."
        filepath = create_file("Test Title", prose)

        # Validate multiple times
        for i in range(3):
            result = validate_file(filepath)
            assert result is True, f"Validation failed on attempt {i+1}"

    def test_git_operations_called_with_correct_parameters(self, temp_dir):
        """Test that git operations are called with correct parameters."""
        # Create a valid file first
        prose = "Iteration is a fundamental principle in software development that drives improvement and excellence through repeated cycles of design, implementation, and refinement. Each iteration builds upon the previous one, incorporating valuable feedback and lessons learned to refine approaches. By embracing iterative processes, teams can adapt to changing requirements and deliver increasingly valuable solutions with greater confidence and quality."
        create_file("Test Title", prose)
        validate_file(Path("test-hb8tyt.md"))

        # Mock subprocess.run to verify git commands
        with mock.patch('subprocess.run') as mock_run:
            git_operations()

            # Verify subprocess.run was called 3 times (add, commit, push)
            assert mock_run.call_count == 3, "Expected 3 git commands (add, commit, push)"

            # Verify the commands are correct
            calls = mock_run.call_args_list

            # Check git add command
            assert calls[0][0][0] == ['git', 'add', 'test-hb8tyt.md'], "First call should be git add"
            assert calls[0][1] == {'check': True}, "Should use check=True"

            # Check git commit command
            assert calls[1][0][0][0:2] == ['git', 'commit'], "Second call should be git commit"
            assert calls[1][1] == {'check': True}, "Should use check=True"

            # Check git push command
            assert calls[2][0][0] == ['git', 'push', '-u', 'origin', 'HEAD'], "Third call should be git push"
            assert calls[2][1] == {'check': True}, "Should use check=True"

    def test_validation_errors_are_descriptive(self, temp_dir):
        """Test that validation error messages are clear and actionable."""
        path = Path("test-hb8tyt.md")
        content = "Some content without heading\n\nMore content.\n"
        path.write_bytes(content.encode('utf-8'))

        try:
            validate_file(path)
            pytest.fail("Should have raised AssertionError")
        except AssertionError as e:
            # Error message should be descriptive
            assert len(str(e)) > 10, "Error message should be descriptive"
            assert "H1" in str(e) or "heading" in str(e), "Error should mention heading requirement"
