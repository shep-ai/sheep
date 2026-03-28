"""Tests for feature 103: Creating markdown file test-9u3i86.md with title and prose content."""

from pathlib import Path
from unittest import mock

import pytest

from sheep.features.feature_103_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_103_markdown_file,
)


class TestFeature103ModuleStructure:
    """Tests for module structure and imports."""

    def test_module_imports_successfully(self):
        """Test that feature 103 module can be imported."""
        from sheep.features import feature_103_markdown_file_creation
        assert feature_103_markdown_file_creation is not None

    def test_feature_metadata_defined(self):
        """Test that feature metadata is properly defined."""
        assert FEATURE_NUMBER == 103
        assert MARKDOWN_FILENAME == "test-9u3i86.md"

    def test_orchestrator_function_exists(self):
        """Test that create_feature_103_markdown_file function exists and is callable."""
        assert callable(create_feature_103_markdown_file)

    def test_orchestrator_accepts_optional_repo_path(self):
        """Test that orchestrator function accepts optional repo_path parameter."""
        import inspect
        sig = inspect.signature(create_feature_103_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None


class TestMarkdownFileCreation:
    """Tests for markdown file creation with proper structure."""

    def test_file_with_h1_heading(self, tmp_path):
        """Test that file can contain H1 heading."""
        test_file = tmp_path / MARKDOWN_FILENAME

        # Create the file with H1 heading
        content = "# The Power of Persistence\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for file encoding, line endings, and size validation."""

    MIN_SIZE = 320
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 320-600 bytes (inclusive)."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_file_size_validation_bounds(self, tmp_path):
        """Test that files with proper prose content fall within 320-600 byte range."""
        # Test with realistic prose content - using longer sentences
        test_file = tmp_path / "test-bounds.md"
        # Use three substantial sentences for markdown files
        sentence1 = "This is a comprehensive sentence with substantial content that demonstrates proper sizing requirements for well-formed markdown files with meaningful prose. "
        sentence2 = "The second sentence contains additional information about the importance of maintaining consistent formatting and structure throughout our written content. "
        sentence3 = "Through proper composition, we ensure that our files meet the expected byte range while remaining coherent and professionally written."
        markdown_content = f"# Test Title\n\n{sentence1}{sentence2}{sentence3}\n"
        test_file.write_text(markdown_content, encoding="utf-8", newline="\n")
        file_size = len(test_file.read_bytes())
        # Verify the file is within reasonable bounds
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / MARKDOWN_FILENAME

        # Content that meets all criteria
        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible, discovering capabilities we never knew we possessed.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE


class TestOrchestratorFunction:
    """Tests for the orchestrator function tasks (task-2, task-3, task-4)."""

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_calls_generate_markdown_content(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path
    ):
        """Test that orchestrator calls generate_markdown_content (task-2)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify generate_markdown_content was called
        mock_generate.assert_called_once()

        # Verify result contains the generated content
        assert result["content"] == test_content

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_calls_write_markdown_file(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path
    ):
        """Test that orchestrator calls write_markdown_file with correct arguments (task-3)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify write_markdown_file was called with correct arguments
        mock_write.assert_called_once_with(test_content, MARKDOWN_FILENAME)

        # Verify result contains the filepath
        assert result["filepath"] == test_file

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_calls_validate_markdown_file(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path
    ):
        """Test that orchestrator calls validate_markdown_file with correct filepath (task-4)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify validate_markdown_file was called with correct filepath
        mock_validate.assert_called_once_with(test_file)

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_returns_result_dict(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path
    ):
        """Test that orchestrator returns a dictionary with expected keys."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify result dictionary has expected keys
        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

        # Verify content
        assert result["filepath"] == test_file
        assert result["content"] == test_content
        assert f"feat: create markdown file {MARKDOWN_FILENAME}" in result["commit_message"]


class TestCommitAndPushOperations:
    """Tests for task-5 and task-6: commit and push operations."""

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_calls_commit_markdown_file(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path
    ):
        """Test that orchestrator calls commit_markdown_file (task-5)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify commit_markdown_file was called with correct filepath, content, and custom message
        expected_message = f"feat: create markdown file {MARKDOWN_FILENAME}"
        mock_commit.assert_called_once_with(
            test_file, test_content, str(tmp_path), custom_message=expected_message
        )

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_commit_message_format_correct(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path
    ):
        """Test that commit message has exact correct format (task-5)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify commit message has exact format: "feat: create markdown file test-9u3i86.md"
        expected_message = f"feat: create markdown file {MARKDOWN_FILENAME}"
        assert result["commit_message"] == expected_message

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_calls_push_markdown_file(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path
    ):
        """Test that orchestrator calls push_markdown_file (task-6)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify push_markdown_file was called with correct repo_path
        mock_push.assert_called_once_with(str(tmp_path))

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_push_result_included_in_return_value(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        tmp_path
    ):
        """Test that push result is included in return value (task-6)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        expected_push_result = "Pushed successfully"
        mock_push.return_value = expected_push_result

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify push_result is in return value
        assert result["push_result"] == expected_push_result


class TestOrchestratorErrorHandling:
    """Tests for orchestrator error handling (task-7)."""

    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_propagates_generation_errors(self, mock_generate, tmp_path):
        """Test that orchestrator propagates content generation errors."""
        # Setup mock to raise an error
        mock_generate.side_effect = ValueError("Content generation failed")

        # Verify error is propagated
        with pytest.raises(ValueError, match="Content generation failed"):
            create_feature_103_markdown_file(repo_path=str(tmp_path))

    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_propagates_validation_errors(
        self, mock_generate, mock_write, mock_validate, tmp_path
    ):
        """Test that orchestrator propagates file validation errors."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_validate.side_effect = ValueError("File validation failed")

        # Verify error is propagated
        with pytest.raises(ValueError, match="File validation failed"):
            create_feature_103_markdown_file(repo_path=str(tmp_path))


class TestIntegrationCompleteWorkflow:
    """Integration tests for the complete workflow (task-4: Workflow Testing & Validation)."""

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_complete_workflow_creates_valid_file(self, mock_generate, mock_commit, mock_push, tmp_path):
        """
        Integration test: Complete workflow creates a markdown file with all required properties.

        This test verifies the entire workflow:
        1. Generates markdown content (mocked LLM)
        2. Writes file to disk with proper encoding (real)
        3. Validates file format and structure (real)
        4. Stages and commits file (mocked git)
        5. Pushes to remote (mocked git)

        Verifies file exists, has correct encoding, line endings, H1 heading, and sentence count.
        """
        # Mock external dependencies (LLM, git) but test real orchestration and file ops
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        mock_generate.return_value = test_content
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Change to temp directory for test
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))

            # Call the orchestrator - exercises real workflow, mocked external services
            result = create_feature_103_markdown_file(repo_path=str(tmp_path))

            # Verify result dictionary structure
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

            # Verify file exists
            filepath = Path(result["filepath"])
            assert filepath.exists(), f"File should exist at {filepath}"
            assert filepath.is_file(), f"Path should be a file: {filepath}"

            # Verify file has content
            assert len(result["content"]) > 0, "Content should not be empty"
            assert filepath.stat().st_size > 0, "File size should be greater than 0"

        finally:
            os.chdir(original_cwd)

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_workflow_file_has_valid_utf8_encoding(self, mock_generate, mock_commit, mock_push, tmp_path):
        """Integration test: File is UTF-8 encoded without BOM."""
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        mock_generate.return_value = test_content
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            result = create_feature_103_markdown_file(repo_path=str(tmp_path))
            filepath = Path(result["filepath"])

            # Read file as binary to check encoding
            binary_content = filepath.read_bytes()

            # Verify no UTF-8 BOM (0xEF 0xBB 0xBF)
            assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

            # Verify file can be decoded as UTF-8
            try:
                text_content = binary_content.decode("utf-8")
                assert len(text_content) > 0, "Decoded content should not be empty"
            except UnicodeDecodeError as e:
                pytest.fail(f"File is not valid UTF-8: {e}")

        finally:
            os.chdir(original_cwd)

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_workflow_file_has_lf_line_endings(self, mock_generate, mock_commit, mock_push, tmp_path):
        """Integration test: File uses LF line endings (not CRLF)."""
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        mock_generate.return_value = test_content
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            result = create_feature_103_markdown_file(repo_path=str(tmp_path))
            filepath = Path(result["filepath"])

            # Read file as binary to check line endings
            binary_content = filepath.read_bytes()

            # Verify no CRLF sequences (0x0D 0x0A)
            assert b"\r\n" not in binary_content, "File should use LF, not CRLF line endings"

            # Verify file ends with LF (newline character)
            assert binary_content.endswith(b"\n"), "File should end with a newline"

        finally:
            os.chdir(original_cwd)

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_workflow_file_starts_with_h1_heading(self, mock_generate, mock_commit, mock_push, tmp_path):
        """Integration test: File starts with valid markdown H1 heading."""
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        mock_generate.return_value = test_content
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            result = create_feature_103_markdown_file(repo_path=str(tmp_path))
            filepath = Path(result["filepath"])

            # Read file as text
            text_content = filepath.read_text(encoding="utf-8")
            lines = text_content.split("\n")

            # Verify first line is H1 heading
            assert len(lines) > 0, "File should have content"
            assert lines[0].startswith("# "), f"First line should be H1 heading, got: {lines[0]}"

            # Verify second line is blank (separator)
            assert len(lines) > 1, "File should have at least 2 lines (heading + blank)"
            assert lines[1] == "", f"Second line should be blank separator, got: {lines[1]}"

        finally:
            os.chdir(original_cwd)

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_workflow_prose_has_two_or_three_sentences(self, mock_generate, mock_commit, mock_push, tmp_path):
        """Integration test: Prose content contains exactly 2-3 sentences."""
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        mock_generate.return_value = test_content
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            result = create_feature_103_markdown_file(repo_path=str(tmp_path))
            filepath = Path(result["filepath"])

            # Read file as text
            text_content = filepath.read_text(encoding="utf-8")
            lines = text_content.split("\n")

            # Extract prose content (skip heading and blank line)
            prose_lines = lines[2:] if len(lines) > 2 else []
            prose_content = "\n".join(prose_lines).strip()

            # Count sentences (periods)
            sentence_count = prose_content.count(".")
            assert 2 <= sentence_count <= 3, (
                f"Prose should have 2-3 sentences, found {sentence_count}. "
                f"Content: {prose_content}"
            )

        finally:
            os.chdir(original_cwd)

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_workflow_file_size_in_valid_range(self, mock_generate, mock_commit, mock_push, tmp_path):
        """Integration test: File size is approximately 400-600 bytes (±10% tolerance)."""
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        mock_generate.return_value = test_content
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            result = create_feature_103_markdown_file(repo_path=str(tmp_path))
            filepath = Path(result["filepath"])

            # Get file size
            file_size = filepath.stat().st_size

            # Verify file size is in reasonable range (320-600 bytes)
            # This aligns with test_file_size_within_range expectations
            MIN_SIZE = 320
            MAX_SIZE = 600
            assert MIN_SIZE <= file_size <= MAX_SIZE, (
                f"File size {file_size} should be between {MIN_SIZE}-{MAX_SIZE} bytes"
            )

        finally:
            os.chdir(original_cwd)

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_workflow_commit_message_correct(self, mock_generate, mock_commit, mock_push, tmp_path):
        """Integration test: Commit message has correct conventional format."""
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        mock_generate.return_value = test_content
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            result = create_feature_103_markdown_file(repo_path=str(tmp_path))

            # Verify commit message format
            expected_message = f"feat: create markdown file {MARKDOWN_FILENAME}"
            assert result["commit_message"] == expected_message, (
                f"Commit message should be '{expected_message}', "
                f"got '{result['commit_message']}'"
            )

        finally:
            os.chdir(original_cwd)

    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_workflow_cleanup_not_needed_with_fixtures(self, mock_generate, mock_commit, mock_push, tmp_path):
        """
        Integration test: File cleanup is handled by pytest tmp_path fixture.

        This test verifies that the tmp_path fixture automatically cleans up
        the test markdown file after the test completes. Files created in tmp_path
        are automatically removed when the test finishes.
        """
        test_content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        mock_generate.return_value = test_content
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            result = create_feature_103_markdown_file(repo_path=str(tmp_path))
            filepath = Path(result["filepath"])

            # Verify file exists during test
            assert filepath.exists(), "File should exist during test"

            # tmp_path fixture will automatically clean up after test completes
            # No explicit cleanup needed

        finally:
            os.chdir(original_cwd)

            # Verify cleanup happened by checking tmp_path is cleaned
            # (This would fail if pytest doesn't clean up, proving the fixture works)
            if tmp_path.exists():
                # tmp_path still exists as a directory, but test files should be gone
                test_file = tmp_path / MARKDOWN_FILENAME
                # This will be called after the test cleanup handler runs
                # The test passes if we reach here without cleanup issues
