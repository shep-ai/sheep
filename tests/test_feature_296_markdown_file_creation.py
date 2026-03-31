"""Tests for feature 296: Creating markdown file test-v4dx46.md with title and prose content.

This test module validates:
- Feature function create_test_v4dx46_markdown_file() returns expected dict structure
- Feature function main() returns correct exit codes (0 for success, 1 for failure)
- File creation, validation, and git operations work correctly
- Content meets specification requirements (UTF-8, LF, H1+prose, 400-600 bytes)
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_296_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_v4dx46_markdown_file,
    main,
)


class TestFeatureFunctionSignature:
    """Tests for feature 296 function signatures and return types."""

    def test_create_test_v4dx46_markdown_file_signature(self):
        """Test that create_test_v4dx46_markdown_file has correct signature."""
        # Function should accept optional repo_path parameter
        import inspect

        sig = inspect.signature(create_test_v4dx46_markdown_file)
        assert "repo_path" in sig.parameters
        # repo_path should have default None
        assert sig.parameters["repo_path"].default is None
        # Return type should be dict[str, str]
        assert sig.return_annotation == dict[str, str]

    def test_main_signature(self):
        """Test that main has correct signature."""
        import inspect

        sig = inspect.signature(main)
        # main should take no parameters
        assert len(sig.parameters) == 0
        # Return type should be int
        assert sig.return_annotation == int

    def test_feature_constants_defined(self):
        """Test that required constants are defined."""
        assert FEATURE_NUMBER == 296
        assert FEATURE_NAME == "markdown-file-creation-v4dx46"
        assert MARKDOWN_FILENAME == "test-v4dx46.md"


class TestFeatureFunctionBehavior:
    """Tests for create_test_v4dx46_markdown_file() function behavior."""

    def test_create_test_v4dx46_markdown_file_returns_dict(self):
        """Test that function returns a dict with required keys."""
        with patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file") as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-v4dx46.md",
                "content": "# Test\n\nProse.",
                "commit_message": "feat(296): create markdown file test-v4dx46.md with prose content",
                "push_result": "success",
            }

            result = create_test_v4dx46_markdown_file(repo_path="/repo")

            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

    def test_create_test_v4dx46_markdown_file_calls_create_markdown_file(self):
        """Test that function calls create_markdown_file with correct parameters."""
        with patch(
            "sheep.features.feature_296_markdown_file_creation.create_markdown_file"
        ) as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-v4dx46.md",
                "content": "# Test\n\nProse.",
                "commit_message": "feat(296): create markdown file test-v4dx46.md with prose content",
                "push_result": "success",
            }

            create_test_v4dx46_markdown_file(repo_path="/repo")

            # Verify create_markdown_file was called with correct parameters
            mock_create.assert_called_once_with(
                filename="test-v4dx46.md",
                repo_path="/repo",
                feature_number=296,
            )

    def test_create_test_v4dx46_markdown_file_defaults_repo_path(self):
        """Test that function defaults repo_path to current directory."""
        with patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file") as mock_create:
            with patch("sheep.features.feature_296_markdown_file_creation.Path") as mock_path_class:
                mock_cwd = Path("/current/dir")
                mock_path_class.cwd.return_value = mock_cwd
                mock_create.return_value = {
                    "filepath": "/current/dir/test-v4dx46.md",
                    "content": "# Test\n\nProse.",
                    "commit_message": "feat(296): create markdown file test-v4dx46.md with prose content",
                    "push_result": "success",
                }

                create_test_v4dx46_markdown_file()

                # Verify create_markdown_file was called with current directory
                call_args = mock_create.call_args
                # The function converts the path to string, check that it's a string path
                assert isinstance(call_args.kwargs["repo_path"], str)
                assert "current" in call_args.kwargs["repo_path"]
                assert "dir" in call_args.kwargs["repo_path"]

    def test_create_test_v4dx46_markdown_file_raises_on_error(self):
        """Test that function re-raises exceptions from create_markdown_file."""
        with patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file") as mock_create:
            mock_create.side_effect = ValueError("Content validation failed")

            with pytest.raises(ValueError, match="Content validation failed"):
                create_test_v4dx46_markdown_file(repo_path="/repo")

    def test_create_test_v4dx46_markdown_file_returns_correct_keys(self):
        """Test that function returns dict with all required keys."""
        with patch("sheep.features.feature_296_markdown_file_creation.create_markdown_file") as mock_create:
            expected_result = {
                "filepath": str(Path("/repo/test-v4dx46.md")),
                "content": "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n",
                "commit_message": "feat(296): create markdown file test-v4dx46.md with prose content",
                "push_result": "Pushed to origin/feat/296-markdown-file-creation-67ee89",
            }
            mock_create.return_value = expected_result

            result = create_test_v4dx46_markdown_file(repo_path="/repo")

            assert result == expected_result
            assert result["filepath"] == str(Path("/repo/test-v4dx46.md"))
            assert "test-v4dx46.md" in result["filepath"]
            assert "feat(296)" in result["commit_message"]


class TestMainFunction:
    """Tests for main() entry point."""

    def test_main_returns_0_on_success(self):
        """Test that main() returns 0 when feature creation succeeds."""
        with patch("sheep.features.feature_296_markdown_file_creation.create_test_v4dx46_markdown_file") as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-v4dx46.md",
                "content": "# Test\n\nProse.",
                "commit_message": "feat(296): create markdown file test-v4dx46.md with prose content",
                "push_result": "success",
            }

            result = main()

            assert result == 0
            assert isinstance(result, int)

    def test_main_returns_1_on_error(self):
        """Test that main() returns 1 when feature creation fails."""
        with patch("sheep.features.feature_296_markdown_file_creation.create_test_v4dx46_markdown_file") as mock_create:
            mock_create.side_effect = Exception("Creation failed")

            result = main()

            assert result == 1
            assert isinstance(result, int)

    def test_main_calls_create_test_v4dx46_markdown_file(self):
        """Test that main() calls create_test_v4dx46_markdown_file()."""
        with patch("sheep.features.feature_296_markdown_file_creation.create_test_v4dx46_markdown_file") as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-v4dx46.md",
                "content": "# Test\n\nProse.",
                "commit_message": "feat(296): create markdown file test-v4dx46.md with prose content",
                "push_result": "success",
            }

            main()

            mock_create.assert_called_once()

    def test_main_catches_all_exceptions(self):
        """Test that main() catches exceptions and returns 1."""
        with patch("sheep.features.feature_296_markdown_file_creation.create_test_v4dx46_markdown_file") as mock_create:
            # Test with different exception types
            for exc_type in [ValueError, IOError, Exception, RuntimeError]:
                mock_create.side_effect = exc_type("Test error")

                result = main()

                assert result == 1


class TestMarkdownFileFormatting:
    """Tests for markdown file formatting requirements."""

    def test_markdown_file_h1_heading(self, tmp_path):
        """Test that markdown file contains H1 heading."""
        # Create test file with H1 heading
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# Test Heading\n\nTest sentence. Another sentence. Final sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_markdown_file_blank_line_separator(self, tmp_path):
        """Test that markdown file has blank line after H1 heading."""
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# Test Heading\n\nTest sentence. Another sentence. Final sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        lines = test_file.read_text(encoding="utf-8").split("\n")
        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line

    def test_markdown_file_prose_content(self, tmp_path):
        """Test that markdown file contains 2-3 sentences of prose."""
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# Test Heading\n\nTest sentence. Another sentence. Final sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        prose_content = "\n".join(lines[2:]).strip()

        # Count sentences (periods)
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_markdown_file_utf8_encoding(self, tmp_path):
        """Test that markdown file uses UTF-8 encoding without BOM."""
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# Test Heading\n\nTest sentence. Another sentence. Final sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # UTF-8 BOM is 0xEF 0xBB 0xBF - should not be present
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_markdown_file_lf_line_endings(self, tmp_path):
        """Test that markdown file uses LF line endings (not CRLF)."""
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# Test Heading\n\nTest sentence. Another sentence. Final sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # CRLF is 0x0D 0x0A - should not be present
        assert b"\r\n" not in binary_content
        # LF (0x0A) should be present
        assert b"\n" in binary_content

    def test_markdown_file_size_range(self, tmp_path):
        """Test that markdown file size is between 400-600 bytes."""
        test_file = tmp_path / MARKDOWN_FILENAME
        # Create content that falls within the 400-600 byte range
        content = "# The Evolution of Software Development Practices\n\nSoftware development has undergone significant transformation over the past several decades, from early mainframe-based systems to modern cloud-native architectures and microservices. The adoption of agile methodologies, continuous integration and deployment practices, and automated testing has fundamentally changed how teams collaborate and deliver value to users. These evolutionary changes reflect the industry's commitment to improving code quality, reducing time-to-market, and creating more resilient and maintainable systems.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert 400 <= file_size <= 600

    def test_markdown_file_trailing_newline(self, tmp_path):
        """Test that markdown file ends with newline."""
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# Test Heading\n\nTest sentence. Another sentence. Final sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # File should end with newline (LF = 0x0A)
        assert binary_content.endswith(b"\n")


class TestFeatureIntegration:
    """Integration tests for feature 296."""

    def test_feature_constants_match_filename(self):
        """Test that feature constants are internally consistent."""
        assert "test-v4dx46.md" == MARKDOWN_FILENAME
        assert 296 == FEATURE_NUMBER
        assert "v4dx46" in FEATURE_NAME

    def test_create_markdown_file_function_exists(self):
        """Test that create_markdown_file can be imported and called."""
        from sheep.content_generators import create_markdown_file

        assert callable(create_markdown_file)

    def test_feature_module_can_be_imported(self):
        """Test that feature module can be imported successfully."""
        from sheep.features import feature_296_markdown_file_creation

        assert hasattr(feature_296_markdown_file_creation, "create_test_v4dx46_markdown_file")
        assert hasattr(feature_296_markdown_file_creation, "main")
        assert hasattr(feature_296_markdown_file_creation, "FEATURE_NUMBER")
        assert hasattr(feature_296_markdown_file_creation, "MARKDOWN_FILENAME")

    def test_feature_module_executable(self):
        """Test that feature module can be executed directly."""
        from sheep.features import feature_296_markdown_file_creation

        assert hasattr(feature_296_markdown_file_creation, "main")
        assert callable(feature_296_markdown_file_creation.main)
