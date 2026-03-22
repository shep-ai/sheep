"""Tests for feature 168: Creating markdown file test-oyiqcz.md with title and prose content."""

import inspect
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestFeature168MarkdownFileCreation:
    """Tests for feature 168 markdown file creation with retry logic."""

    def test_module_imports(self):
        """Test that the feature module can be imported."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        assert callable(create_feature_168_markdown_file)

    def test_function_signature(self):
        """Test that the function has the correct signature."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        sig = inspect.signature(create_feature_168_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None

    def test_feature_constants(self):
        """Test that feature constants are defined correctly."""
        from sheep.features.feature_168_markdown_file_creation import (
            COMMIT_MESSAGE,
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
        )

        assert FEATURE_NUMBER == 168
        assert MARKDOWN_FILENAME == "test-oyiqcz.md"
        assert (
            COMMIT_MESSAGE
            == "feat(168): Create markdown file test-oyiqcz.md with prose content"
        )

    @patch("sheep.features.feature_168_markdown_file_creation.Path")
    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_orchestration_calls_all_steps(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        mock_path,
    ):
        """Test that the orchestration calls all steps in the correct order."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-oyiqcz.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed successfully"
        mock_push.return_value = "Pushed successfully"

        # Mock Path.stat() to return a file size in valid range
        mock_file_stat = MagicMock()
        mock_file_stat.st_size = 400  # Within 300-600 range
        mock_path.return_value.stat.return_value = mock_file_stat

        # Call the function
        result = create_feature_168_markdown_file("/test/repo")

        # Verify all functions were called
        mock_generate.assert_called_once()
        mock_write.assert_called_once_with(mock_content, "test-oyiqcz.md")
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

        # Verify the return value structure
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_168_markdown_file_creation.Path")
    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_returns_correct_dict_structure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        mock_path,
    ):
        """Test that the function returns the correct dictionary structure."""
        from sheep.features.feature_168_markdown_file_creation import (
            COMMIT_MESSAGE,
            create_feature_168_markdown_file,
        )

        # Setup mock returns
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third.\n"
        mock_filepath = "/repo/test-oyiqcz.md"
        mock_generate.return_value = mock_content
        mock_write.return_value = mock_filepath
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Mock Path.stat() to return a file size in valid range
        mock_file_stat = MagicMock()
        mock_file_stat.st_size = 400  # Within 300-600 range
        mock_path.return_value.stat.return_value = mock_file_stat

        # Call the function
        result = create_feature_168_markdown_file()

        # Verify all required keys are present
        assert result["filepath"] == mock_filepath
        assert result["content"] == mock_content
        assert result["commit_message"] == COMMIT_MESSAGE
        assert result["push_result"] == "Pushed"

    @patch("sheep.features.feature_168_markdown_file_creation.Path")
    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_uses_exact_commit_message(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        mock_path,
    ):
        """Test that the exact commit message from spec is used."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-oyiqcz.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Mock Path.stat() to return a file size in valid range
        mock_file_stat = MagicMock()
        mock_file_stat.st_size = 400  # Within 300-600 range
        mock_path.return_value.stat.return_value = mock_file_stat

        # Call the function
        create_feature_168_markdown_file()

        # Verify the commit message is exactly as specified
        call_args = mock_commit.call_args
        assert call_args is not None
        assert (
            call_args.kwargs["custom_message"]
            == "feat(168): Create markdown file test-oyiqcz.md with prose content"
        )

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_repo_path_defaults_to_cwd(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that repo_path defaults to current working directory."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-oyiqcz.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Create a real temporary file to satisfy the stat() call
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
            f.write(b"# Test\n\nSentence. Sentence. Sentence.\n" + b"x" * 350)

        try:
            mock_write.return_value = temp_file

            # Call without repo_path
            create_feature_168_markdown_file()

            # Verify commit was called with str(Path.cwd())
            call_args = mock_commit.call_args
            assert call_args is not None
            assert call_args[0][2] == str(Path.cwd())
        finally:
            Path(temp_file).unlink(missing_ok=True)


class TestRetryLogic:
    """Tests for the retry logic on content generation failure."""

    @patch("sheep.features.feature_168_markdown_file_creation.Path")
    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_retries_on_content_validation_failure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        mock_path,
    ):
        """Test that content generation is retried on validation failure."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mocks: fail on attempt 1, succeed on attempt 2
        valid_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.side_effect = [
            ValueError("Content validation failed"),  # Attempt 1: fails
            valid_content,  # Attempt 2: succeeds
        ]
        mock_write.return_value = "/repo/test-oyiqcz.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Mock Path.stat() to return a file size in valid range
        mock_file_stat = MagicMock()
        mock_file_stat.st_size = 400  # Within 300-600 range
        mock_path.return_value.stat.return_value = mock_file_stat

        # Call the function
        result = create_feature_168_markdown_file()

        # Verify generate was called twice
        assert mock_generate.call_count == 2

        # Verify the successful content was used
        assert result["content"] == valid_content

        # Verify other steps were called
        mock_write.assert_called_once()
        mock_validate.assert_called_once()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_retries_up_to_two_times(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that retries are limited to 2 (3 total attempts)."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mocks: fail on all attempts
        mock_generate.side_effect = ValueError("Content validation failed")

        # Call the function and expect exception
        with pytest.raises(ValueError):
            create_feature_168_markdown_file()

        # Verify generate was called exactly 3 times (1 initial + 2 retries)
        assert mock_generate.call_count == 3

        # Verify subsequent steps were not called
        mock_write.assert_not_called()
        mock_validate.assert_not_called()
        mock_commit.assert_not_called()
        mock_push.assert_not_called()

    @patch("sheep.features.feature_168_markdown_file_creation.Path")
    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_succeeds_on_first_attempt(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        mock_path,
    ):
        """Test that no retry happens if first attempt succeeds."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mocks: succeed on first attempt
        valid_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = valid_content
        mock_write.return_value = "/repo/test-oyiqcz.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Mock Path.stat() to return a file size in valid range
        mock_file_stat = MagicMock()
        mock_file_stat.st_size = 400  # Within 300-600 range
        mock_path.return_value.stat.return_value = mock_file_stat

        # Call the function
        create_feature_168_markdown_file()

        # Verify generate was called only once
        assert mock_generate.call_count == 1


class TestFileSizeValidation:
    """Tests for file size validation (300-600 bytes)."""

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_validates_file_size_in_valid_range(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path,
    ):
        """Test that file with valid size (300-600 bytes) passes validation."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Create a real file with valid size (300-600 bytes)
        test_file = tmp_path / "test-oyiqcz.md"
        valid_content = (
            "# The Power of Persistence\n\n"
            "Persistence is the steadfast commitment to overcome obstacles and challenges in pursuit of goals. "
            "It builds resilience and strength through repeated effort, determination, and continuous practice. "
            "Through persistence, we unlock potential and achieve what once seemed impossible to reach or attain.\n"
        )
        test_file.write_text(valid_content, encoding="utf-8")
        file_size = test_file.stat().st_size
        assert 300 <= file_size <= 600

        # Setup mocks
        mock_generate.return_value = valid_content
        mock_write.return_value = str(test_file)
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Call the function
            result = create_feature_168_markdown_file()

            # Verify the function succeeded
            assert result["content"] == valid_content
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_rejects_file_too_small(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path,
    ):
        """Test that file smaller than 300 bytes is rejected."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Create a real file that's too small
        test_file = tmp_path / "test-oyiqcz.md"
        small_content = "# Short\n\nToo short.\n"  # Less than 300 bytes
        test_file.write_text(small_content, encoding="utf-8")
        file_size = test_file.stat().st_size
        assert file_size < 300

        # Setup mocks
        mock_generate.return_value = small_content
        mock_write.return_value = str(test_file)

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Call the function and expect exception
            with pytest.raises(ValueError, match="outside 300-600 range"):
                create_feature_168_markdown_file()

            # Verify file was deleted
            assert not test_file.exists()

            # Verify subsequent steps were not called
            mock_validate.assert_not_called()
            mock_commit.assert_not_called()
            mock_push.assert_not_called()

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_rejects_file_too_large(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path,
    ):
        """Test that file larger than 600 bytes is rejected."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Create a real file that's too large
        test_file = tmp_path / "test-oyiqcz.md"
        large_content = (
            "# The Power of Persistence\n\n"
            + "This is a very long content. " * 50  # Much longer than 600 bytes
        )
        test_file.write_text(large_content, encoding="utf-8")
        file_size = test_file.stat().st_size
        assert file_size > 600

        # Setup mocks
        mock_generate.return_value = large_content
        mock_write.return_value = str(test_file)

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Call the function and expect exception
            with pytest.raises(ValueError, match="outside 300-600 range"):
                create_feature_168_markdown_file()

            # Verify file was deleted
            assert not test_file.exists()

            # Verify subsequent steps were not called
            mock_validate.assert_not_called()
            mock_commit.assert_not_called()
            mock_push.assert_not_called()

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_file_deleted_on_size_validation_failure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path,
    ):
        """Test that file is deleted if size validation fails."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Create a real file with invalid size
        test_file = tmp_path / "test-oyiqcz.md"
        oversized_content = "# Title\n\n" + "x" * 1000  # Much larger than 600 bytes
        test_file.write_text(oversized_content, encoding="utf-8")
        assert test_file.exists()

        # Setup mocks
        mock_generate.return_value = oversized_content
        mock_write.return_value = str(test_file)

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Call the function and expect exception
            with pytest.raises(ValueError):
                create_feature_168_markdown_file()

            # Verify file was deleted
            assert not test_file.exists()

        finally:
            os.chdir(original_cwd)


class TestErrorHandling:
    """Tests for error handling and exception propagation."""

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_handles_exception_in_write(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
    ):
        """Test that exceptions in write step are properly raised."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mocks
        mock_generate.return_value = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_write.side_effect = IOError("Failed to write file")

        # Verify exception is raised
        with pytest.raises(IOError):
            create_feature_168_markdown_file()

        # Verify subsequent steps were not called
        mock_validate.assert_not_called()
        mock_commit.assert_not_called()
        mock_push.assert_not_called()

    @patch("sheep.features.feature_168_markdown_file_creation.Path")
    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_handles_exception_in_commit(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        mock_path,
    ):
        """Test that exceptions in commit step are properly raised."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-oyiqcz.md"
        mock_validate.return_value = True
        mock_commit.side_effect = Exception("Git commit failed")

        # Mock Path.stat() to return a file size in valid range
        mock_file_stat = MagicMock()
        mock_file_stat.st_size = 400  # Within 300-600 range
        mock_path.return_value.stat.return_value = mock_file_stat

        # Verify exception is raised
        with pytest.raises(Exception, match="Git commit failed"):
            create_feature_168_markdown_file()

        # Verify push was not called
        mock_push.assert_not_called()

    @patch("sheep.features.feature_168_markdown_file_creation.Path")
    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_handles_exception_in_push(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        mock_path,
    ):
        """Test that exceptions in push step are properly raised."""
        from sheep.features.feature_168_markdown_file_creation import (
            create_feature_168_markdown_file,
        )

        # Setup mocks
        mock_content = "# Test\n\nSentence. Sentence. Sentence.\n"
        mock_generate.return_value = mock_content
        mock_write.return_value = "/repo/test-oyiqcz.md"
        mock_validate.return_value = True
        mock_commit.return_value = "Committed"
        mock_push.side_effect = Exception("Git push failed")

        # Mock Path.stat() to return a file size in valid range
        mock_file_stat = MagicMock()
        mock_file_stat.st_size = 400  # Within 300-600 range
        mock_path.return_value.stat.return_value = mock_file_stat

        # Verify exception is raised
        with pytest.raises(Exception, match="Git push failed"):
            create_feature_168_markdown_file()


class TestFileCreation:
    """Integration tests for actual file creation."""

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-oyiqcz.md"

        # Create the file with H1 heading
        content = (
            "# The Power of Persistence\n\n"
            "First sentence. Second sentence. Third sentence.\n"
        )
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_size_is_in_specification_range(self, tmp_path):
        """Test that file size is within 300-600 bytes."""
        test_file = tmp_path / "test-oyiqcz.md"

        content = (
            "# The Power of Persistence\n\n"
            "Persistence is the steadfast commitment to overcome obstacles and challenges. "
            "It builds resilience and strength through repeated effort, determination, and "
            "the continuous refinement of our abilities and character. Through persistence, "
            "we unlock our potential and achieve what once seemed impossible.\n"
        )
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = test_file.stat().st_size
        assert 300 <= file_size <= 600

    def test_file_uses_utf8_encoding(self, tmp_path):
        """Test that file is UTF-8 encoded without BOM."""
        test_file = tmp_path / "test-oyiqcz.md"

        content = (
            "# The Power of Persistence\n\n"
            "Persistence is steadfast commitment. It builds resilience. "
            "Through persistence, we unlock potential.\n"
        )
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no BOM
        binary_content = test_file.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Verify can be decoded as UTF-8
        decoded = binary_content.decode("utf-8")
        assert decoded == content

    def test_file_uses_lf_line_endings(self, tmp_path):
        """Test that file uses LF line endings, not CRLF."""
        test_file = tmp_path / "test-oyiqcz.md"

        content = (
            "# The Power of Persistence\n\n"
            "Persistence is steadfast. It builds resilience. "
            "Through persistence, we unlock potential.\n"
        )
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Read as binary and verify no CRLF
        binary_content = test_file.read_bytes()
        assert b"\r\n" not in binary_content
        assert b"\n" in binary_content

    def test_file_ends_with_newline(self, tmp_path):
        """Test that file ends with a trailing newline (Unix convention)."""
        test_file = tmp_path / "test-oyiqcz.md"

        content = (
            "# The Power of Persistence\n\n"
            "Persistence is steadfast. It builds resilience. "
            "Through persistence, we unlock potential.\n"
        )
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        assert text_content.endswith("\n")


class TestEndToEndIntegration:
    """End-to-end integration tests for feature 168."""

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_e2e_creates_markdown_file_with_valid_format(
        self, mock_generate, mock_commit, mock_push, tmp_path
    ):
        """Test end-to-end creation of markdown file with valid format."""
        from sheep.features.feature_168_markdown_file_creation import (
            MARKDOWN_FILENAME,
            create_feature_168_markdown_file,
        )

        # Setup mocks with content that will be 300-600 bytes (need ~100+ more chars)
        mock_content = (
            "# Technology and Innovation\n\n"
            "Technology continues to drive innovation across industries, sectors, and markets worldwide. "
            "It enables faster communication, collaboration, and coordination among teams and organizations globally. "
            "These advances fundamentally transform and shape how we work, live, and interact in the modern world.\n"
        )
        mock_generate.return_value = mock_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute the feature
            result = create_feature_168_markdown_file()

            # Verify file was created
            file_path_obj = Path(MARKDOWN_FILENAME)
            assert file_path_obj.exists()
            file_content = file_path_obj.read_text(encoding="utf-8")

            # Verify H1 heading
            assert file_content.startswith("# ")

            # Verify prose content
            lines = file_content.split("\n")
            assert len(lines) >= 3
            assert lines[1] == ""  # Blank line separator

            # Verify sentence count (2-3 sentences)
            prose = "\n".join(lines[2:]).strip()
            sentence_count = prose.count(".")
            assert 2 <= sentence_count <= 3

            # Verify file encoding and line endings
            file_bytes = file_path_obj.read_bytes()
            assert not file_bytes.startswith(b"\xef\xbb\xbf")  # No UTF-8 BOM
            assert b"\r\n" not in file_bytes  # No CRLF
            assert b"\n" in file_bytes  # Has LF

            # Verify file size
            file_size = file_path_obj.stat().st_size
            assert 300 <= file_size <= 600

            # Verify result structure
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

            # Verify git operations were called
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_168_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_168_markdown_file_creation.generate_markdown_content")
    def test_e2e_uses_correct_filename_and_message(
        self, mock_generate, mock_commit, mock_push, tmp_path
    ):
        """Test that file is created with correct name and commit message."""
        from sheep.features.feature_168_markdown_file_creation import (
            COMMIT_MESSAGE,
            MARKDOWN_FILENAME,
            create_feature_168_markdown_file,
        )

        # Setup mocks with content that will be 300-600 bytes (need ~50+ more chars)
        mock_content = (
            "# Digital Transformation\n\n"
            "Digital transformation fundamentally reshapes business processes, operations, and strategies. "
            "It requires strategic planning, significant investment, organizational alignment, and change management. "
            "Success comes from embracing change, innovation, technology, and continuous improvement mindset.\n"
        )
        mock_generate.return_value = mock_content
        mock_commit.return_value = {"status": "committed"}
        mock_push.return_value = {"status": "pushed"}

        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute the feature
            result = create_feature_168_markdown_file()

            # Verify exact filename
            assert MARKDOWN_FILENAME == "test-oyiqcz.md"
            file_path_obj = Path(MARKDOWN_FILENAME)
            assert file_path_obj.exists()

            # Verify exact commit message
            assert (
                COMMIT_MESSAGE
                == "feat(168): Create markdown file test-oyiqcz.md with prose content"
            )
            assert result["commit_message"] == COMMIT_MESSAGE

            # Verify commit was called with correct message
            mock_commit.assert_called_once()
            call_args = mock_commit.call_args
            assert (
                call_args.kwargs["custom_message"]
                == "feat(168): Create markdown file test-oyiqcz.md with prose content"
            )

        finally:
            os.chdir(original_cwd)
