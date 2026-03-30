"""
Comprehensive test suite for feature 282: markdown file creation with content generation.

This module provides comprehensive test coverage for feature 282, which creates
a markdown file (test-9xt2ec.md) with auto-generated content from Claude API,
proper structure, encoding, and line endings.

Test Coverage:
- Orchestration function returns correct result dictionary
- File is created at repository root with correct filename
- Content structure (H1 heading + blank line + prose)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- Prose content validation (2-3 sentences)
- Git integration (commit message format, push result)
- End-to-end integration of the complete workflow
- Error handling for missing API key, git configuration issues

The test suite uses pytest fixtures, mocks, and helper functions to create
isolated test environments and comprehensive validation testing.
"""

import importlib.util
import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import (
    create_markdown_file,
    validate_markdown_file,
    write_markdown_file,
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
def sample_markdown_content():
    """
    Provide sample valid markdown content for testing.

    Returns:
        str: Valid markdown with H1 heading and 2-3 sentences
    """
    return (
        "# The Power of Iteration\n"
        "\n"
        "Iteration is a fundamental principle in software development that drives "
        "improvement through repeated cycles of design and implementation. "
        "Each iteration builds upon the previous one, incorporating feedback and "
        "lessons learned to refine approaches. By embracing iterative processes, "
        "teams can adapt to changing requirements and deliver increasingly valuable solutions.\n"
    )


# ============================================================================
# Test Classes
# ============================================================================


class TestWrapperScript:
    """Unit tests for the wrapper script create_markdown_file.py."""

    def _load_wrapper_module(self):
        """Helper to dynamically load the wrapper module."""
        wrapper_path = Path(__file__).parent / "create_markdown_file.py"
        spec = importlib.util.spec_from_file_location("wrapper_module_test", wrapper_path)
        wrapper_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper_module)
        return wrapper_module

    def test_imports_orchestration_function(self):
        """Test that wrapper script imports orchestration function successfully."""
        wrapper_module = self._load_wrapper_module()

        # Should have main function
        assert hasattr(wrapper_module, "main")
        assert callable(wrapper_module.main)

        # Should have imported create_markdown_file
        assert hasattr(wrapper_module, "create_markdown_file")

    def test_calls_create_markdown_file_with_correct_filename(self, temp_dir):
        """Test that wrapper script calls create_markdown_file with filename='test-9xt2ec.md'."""
        wrapper_module = self._load_wrapper_module()

        # Mock the create_markdown_file in the wrapper module's namespace
        with mock.patch.object(wrapper_module, "create_markdown_file") as mock_create:
            mock_create.return_value = {
                "filepath": str(Path.cwd() / "test-9xt2ec.md"),
                "content": "# Test\n\nSentence one. Sentence two. Sentence three.",
                "commit_message": "feat(282): create markdown file test-9xt2ec.md with title and prose content",
                "push_result": "Success",
            }

            result = wrapper_module.main()

            # Verify create_markdown_file was called with correct filename
            mock_create.assert_called_once()
            call_args = mock_create.call_args
            # Verify "test-9xt2ec.md" is the first positional argument
            assert call_args[0][0] == "test-9xt2ec.md"

    def test_calls_create_markdown_file_with_correct_feature_number(self, temp_dir):
        """Test that wrapper script calls create_markdown_file with feature_number=282."""
        wrapper_module = self._load_wrapper_module()

        # Mock the create_markdown_file in the wrapper module's namespace
        with mock.patch.object(wrapper_module, "create_markdown_file") as mock_create:
            mock_create.return_value = {
                "filepath": str(Path.cwd() / "test-9xt2ec.md"),
                "content": "# Test\n\nSentence one. Sentence two. Sentence three.",
                "commit_message": "feat(282): create markdown file test-9xt2ec.md with title and prose content",
                "push_result": "Success",
            }

            result = wrapper_module.main()

            # Verify create_markdown_file was called with correct feature number
            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args[1]
            assert call_kwargs.get("feature_number") == 282

    def test_handles_orchestration_error_gracefully(self, temp_dir):
        """Test that wrapper script catches exceptions from orchestration function."""
        wrapper_module = self._load_wrapper_module()

        # Mock create_markdown_file to raise an exception
        with mock.patch.object(wrapper_module, "create_markdown_file") as mock_create:
            mock_create.side_effect = ValueError("Test error message")

            # Wrapper should catch and re-raise (but not crash)
            with pytest.raises(ValueError, match="Test error message"):
                wrapper_module.main()

    def test_returns_result_dictionary_on_success(self, temp_dir):
        """Test that wrapper script returns result dictionary from orchestration."""
        wrapper_module = self._load_wrapper_module()

        with mock.patch.object(wrapper_module, "create_markdown_file") as mock_create:
            expected_result = {
                "filepath": str(Path.cwd() / "test-9xt2ec.md"),
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence.",
                "commit_message": "feat(282): create markdown file test-9xt2ec.md with title and prose content",
                "push_result": "Success",
            }
            mock_create.return_value = expected_result

            result = wrapper_module.main()

            assert result == expected_result
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result


class TestCreateMarkdownFileIntegration:
    """Integration tests for the complete markdown file creation workflow."""

    def test_create_markdown_file_returns_result_dictionary(self, temp_dir):
        """Test that create_markdown_file() returns a dictionary with required keys."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            # Mock the LLM response
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool") as mock_commit:
                with mock.patch("sheep.content_generators.GitPushTool") as mock_push:
                    # Mock git tools
                    mock_commit.return_value._run.return_value = "Commit successful"
                    mock_push.return_value._run.return_value = "Push successful"

                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify result is a dictionary with required keys
                    assert isinstance(result, dict)
                    assert "filepath" in result
                    assert "content" in result
                    assert "commit_message" in result
                    assert "push_result" in result

    def test_commit_message_includes_correct_feature_number(self, temp_dir):
        """Test that the commit message includes the feature number (282)."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool") as mock_commit:
                with mock.patch("sheep.content_generators.GitPushTool") as mock_push:
                    mock_commit.return_value._run.return_value = "Commit successful"
                    mock_push.return_value._run.return_value = "Push successful"

                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify feature number in commit message
                    assert "feat(282):" in result["commit_message"]
                    assert "test-9xt2ec.md" in result["commit_message"]

    def test_file_created_at_repository_root(self, temp_dir):
        """Test that the file is created at the repository root (current directory)."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify file exists
                    filepath = Path(result["filepath"])
                    assert filepath.exists()
                    assert filepath.name == "test-9xt2ec.md"

    def test_file_contains_h1_heading(self, temp_dir):
        """Test that created file contains H1 markdown heading."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify file content
                    content = Path(result["filepath"]).read_text(encoding="utf-8")
                    assert content.startswith("# "), "File should start with H1 heading"

    def test_file_uses_utf8_encoding(self, temp_dir):
        """Test that file is UTF-8 encoded without BOM."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify encoding
                    binary_content = Path(result["filepath"]).read_bytes()

                    # Should not have BOM
                    assert not binary_content.startswith(b"\xef\xbb\xbf")

                    # Should be valid UTF-8
                    try:
                        binary_content.decode("utf-8")
                    except UnicodeDecodeError:
                        pytest.fail("File is not valid UTF-8")

    def test_file_uses_lf_line_endings(self, temp_dir):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify line endings
                    binary_content = Path(result["filepath"]).read_bytes()

                    # Should not contain CRLF
                    assert b"\r\n" not in binary_content
                    # Should contain LF
                    assert b"\n" in binary_content

    def test_file_has_blank_line_separator(self, temp_dir):
        """Test that file has blank line separating heading from prose."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    content = Path(result["filepath"]).read_text(encoding="utf-8")
                    # Should have blank line (double newline)
                    assert "\n\n" in content

    def test_file_ends_with_newline(self, temp_dir):
        """Test that file ends with a newline character."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    binary_content = Path(result["filepath"]).read_bytes()
                    assert binary_content.endswith(b"\n")

    def test_result_dictionary_contains_content(self, temp_dir):
        """Test that result dictionary includes the actual content."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            expected_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_response = {"content": expected_content.rstrip("\n")}
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Content in result should match file content
                    assert result["content"]
                    file_content = Path(result["filepath"]).read_text(encoding="utf-8")
                    assert file_content == result["content"]


class TestWriteMarkdownFile:
    """Tests for the write_markdown_file() utility function."""

    def test_write_markdown_file_creates_file(self, temp_dir):
        """Test that write_markdown_file creates a file at the repository root."""
        content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        assert Path(filepath).exists()
        assert Path(filepath).name == "test-9xt2ec.md"

    def test_write_markdown_file_with_utf8_encoding(self, temp_dir):
        """Test that write_markdown_file uses UTF-8 encoding."""
        content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        # Verify it can be decoded as UTF-8
        binary_content = Path(filepath).read_bytes()
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not UTF-8 encoded")

    def test_write_markdown_file_path_traversal_prevention(self, temp_dir):
        """Test that write_markdown_file prevents path traversal attacks."""
        content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"

        # Should reject filenames with path traversal
        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "../../../etc/passwd")

        with pytest.raises(ValueError, match="Invalid filename"):
            write_markdown_file(content, "..\\windows\\system32")


class TestMarkdownValidation:
    """Tests for markdown file validation covering all file properties and constraints."""

    def test_validate_markdown_file_passes_for_valid_file(self, temp_dir, sample_markdown_content):
        """Test that validate_markdown_file passes for correctly formatted files."""
        filepath = write_markdown_file(sample_markdown_content, "test-9xt2ec.md")
        result = validate_markdown_file(filepath)
        assert result is True

    def test_validate_markdown_file_rejects_missing_h1(self, temp_dir):
        """Test that validate_markdown_file rejects file without H1 heading."""
        content = "## Wrong Level\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        with pytest.raises(ValueError, match="H1 heading"):
            validate_markdown_file(filepath)

    def test_validate_markdown_file_rejects_missing_blank_line(self, temp_dir):
        """Test that validate_markdown_file rejects file without blank line."""
        content = "# Title\nNo blank line here. Second sentence. Third sentence.\n"
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        with pytest.raises(ValueError, match="must be blank"):
            validate_markdown_file(filepath)

    def test_validate_markdown_file_rejects_wrong_sentence_count(self, temp_dir):
        """Test that validate_markdown_file rejects file with wrong sentence count."""
        # Only 1 sentence
        content = "# Title\n\nOnly one sentence.\n"
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        with pytest.raises(ValueError, match="2-3 sentences"):
            validate_markdown_file(filepath)

    def test_validate_markdown_file_rejects_crlf_line_endings(self, temp_dir):
        """Test that validate_markdown_file rejects CRLF line endings."""
        content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
        filepath = Path("test-9xt2ec.md")
        filepath.write_bytes(content.encode("utf-8"))

        with pytest.raises(ValueError, match="CRLF"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_rejects_utf8_bom(self, temp_dir):
        """Test that validate_markdown_file rejects UTF-8 BOM."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath = Path("test-9xt2ec.md")
        filepath.write_bytes(content.encode("utf-8-sig"))

        with pytest.raises(ValueError, match="BOM"):
            validate_markdown_file(str(filepath))

    def test_validate_markdown_file_requires_utf8_encoding(self, temp_dir):
        """Test that validate_markdown_file requires UTF-8 encoding."""
        # Valid UTF-8 content should pass
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        # Should be decodable as UTF-8
        try:
            validate_markdown_file(filepath)
        except ValueError:
            pytest.fail("Valid UTF-8 file should pass validation")

    def test_validate_markdown_file_requires_trailing_newline(self, temp_dir):
        """Test that validate_markdown_file requires trailing newline."""
        content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        # File should end with newline
        binary_content = Path(filepath).read_bytes()
        assert binary_content.endswith(b"\n")

        # Should pass validation
        assert validate_markdown_file(filepath) is True

    def test_validate_markdown_file_rejects_file_too_small(self, temp_dir):
        """Test that validate_markdown_file rejects files smaller than 400 bytes."""
        # Create very small markdown file
        content = "# T\n\nA.\n"  # Only ~10 bytes
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        # Should fail validation due to file size
        with pytest.raises(ValueError):
            validate_markdown_file(filepath)

    def test_validate_markdown_file_rejects_file_too_large(self, temp_dir):
        """Test that validate_markdown_file rejects files larger than 600 bytes."""
        # Create large markdown file (>600 bytes)
        long_prose = "This is a very long sentence with many words. " * 20
        content = f"# Long Title\n\n{long_prose}"
        filepath = write_markdown_file(content, "test-9xt2ec.md")

        # Should fail validation due to file size
        with pytest.raises(ValueError):
            validate_markdown_file(filepath)


class TestGitIntegration:
    """Tests for git integration (commit and push)."""

    def test_git_commit_message_format_is_conventional(self, temp_dir):
        """Test that git commit message follows conventional commits format."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool") as mock_commit:
                with mock.patch("sheep.content_generators.GitPushTool") as mock_push:
                    mock_commit.return_value._run.return_value = "Commit successful"
                    mock_push.return_value._run.return_value = "Push successful"

                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify conventional commit format: type(scope): subject
                    msg = result["commit_message"]
                    assert msg.startswith("feat("), "Commit message must start with 'feat('"
                    assert "282" in msg, "Commit message must include feature number 282"
                    assert "test-9xt2ec.md" in msg, "Commit message must include filename"

    def test_git_push_result_is_included_in_response(self, temp_dir):
        """Test that push result is returned in the result dictionary."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool") as mock_push:
                    mock_push.return_value._run.return_value = "Push successful"

                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Push result should be in the response
                    assert result["push_result"] is not None

    def test_git_commit_tool_is_called(self, temp_dir):
        """Test that GitCommitTool is called for commit operation."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool") as mock_commit:
                with mock.patch("sheep.content_generators.GitPushTool") as mock_push:
                    mock_commit.return_value._run.return_value = "Commit successful"
                    mock_push.return_value._run.return_value = "Push successful"

                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify GitCommitTool was instantiated and called
                    mock_commit.assert_called()

    def test_git_push_tool_is_called(self, temp_dir):
        """Test that GitPushTool is called for push operation."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool") as mock_push:
                    mock_push.return_value._run.return_value = "Push successful"

                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify GitPushTool was instantiated and called
                    mock_push.assert_called()

    def test_commit_message_has_exact_expected_format(self, temp_dir):
        """Test that commit message has the exact format specified in requirements."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            mock_response = {
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Verify exact commit message format
                    expected_prefix = "feat(282):"
                    assert result["commit_message"].startswith(expected_prefix)
                    assert "test-9xt2ec.md" in result["commit_message"]


class TestProseContent:
    """Tests for prose content validation."""

    def test_prose_contains_2_to_3_sentences(self, temp_dir):
        """Test that file prose content contains exactly 2-3 sentences."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            # Three sentences (periods)
            mock_response = {
                "content": "# Title\n\nFirst sentence. Second sentence. Third sentence."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    # Extract prose (everything after the blank line)
                    content = Path(result["filepath"]).read_text(encoding="utf-8")
                    lines = content.split("\n")
                    # Prose is from line 2 onwards (after blank line at line 1)
                    prose = "\n".join(lines[2:])

                    # Count periods (sentences)
                    sentence_count = prose.count(".")
                    assert 2 <= sentence_count <= 3, (
                        f"Prose contains {sentence_count} sentences, "
                        f"expected 2-3 sentences"
                    )


class TestFileSizeRequirements:
    """Tests for file size validation."""

    def test_file_size_meets_specification_400_to_600_bytes(self, temp_dir):
        """Test that created file size meets specification of 400-600 bytes."""
        with mock.patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = mock.Mock()
            mock_llm.return_value = mock_llm_instance

            # Content that results in size within 400-600 byte requirement
            mock_response = {
                "content": "# Iteration and Innovation in Software Development\n\nIteration is a fundamental principle in modern software development that drives continuous improvement and excellence through repeated cycles of design, implementation, and refinement. Each iteration builds upon the previous one, incorporating valuable feedback and lessons learned. Teams that embrace iterative processes adapt better to changing requirements and deliver increasingly valuable solutions."
            }
            mock_llm_instance.call.return_value = mock_response

            with mock.patch("sheep.content_generators.GitCommitTool"):
                with mock.patch("sheep.content_generators.GitPushTool"):
                    result = create_markdown_file("test-9xt2ec.md", feature_number=282)

                    file_size = Path(result["filepath"]).stat().st_size
                    # File must be between 400-600 bytes per specification
                    assert 400 <= file_size <= 600, (
                        f"File size {file_size} bytes does not meet specification "
                        f"requirement of 400-600 bytes"
                    )
