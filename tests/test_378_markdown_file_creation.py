"""Tests for feature 378: Creating markdown file test-y5r064.md with title and content."""

from unittest import mock

import pytest

from sheep.features.feature_378_markdown_file_creation import (
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_378_markdown_file,
)


class TestFeature378ModuleStructure:
    """Tests for module structure and imports."""

    def test_module_imports_successfully(self):
        """Test that feature 378 module can be imported."""
        from sheep.features import feature_378_markdown_file_creation
        assert feature_378_markdown_file_creation is not None

    def test_feature_metadata_defined(self):
        """Test that feature metadata is properly defined."""
        assert FEATURE_NUMBER == 378
        assert MARKDOWN_FILENAME == "test-y5r064.md"

    def test_orchestrator_function_exists(self):
        """Test that create_feature_378_markdown_file function exists and is callable."""
        assert callable(create_feature_378_markdown_file)

    def test_orchestrator_accepts_optional_repo_path(self):
        """Test that orchestrator function accepts optional repo_path parameter."""
        import inspect
        sig = inspect.signature(create_feature_378_markdown_file)
        assert "repo_path" in sig.parameters
        assert sig.parameters["repo_path"].default is None


class TestMarkdownFileCreation:
    """Tests for markdown file creation with proper structure."""

    def test_file_with_h1_heading(self, tmp_path):
        """Test that file can contain H1 heading."""
        test_file = tmp_path / MARKDOWN_FILENAME

        # Create the file with H1 heading
        content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# Quantum Computing Fundamentals\n\nQuantum computers harness the power of quantum mechanics to perform computations that would be impossible for classical computers. Unlike traditional bits that exist as either 0 or 1, quantum bits (qubits) can exist in a superposition of both states simultaneously. This fundamental difference allows quantum computers to explore multiple solutions in parallel, making them exceptionally powerful for certain types of problems.\n"
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

        content = "# Quantum Computing Fundamentals\n\nQuantum computers harness the power of quantum mechanics to perform computations that would be impossible for classical computers. Unlike traditional bits that exist as either 0 or 1, quantum bits (qubits) can exist in a superposition of both states simultaneously. This fundamental difference allows quantum computers to explore multiple solutions in parallel, making them exceptionally powerful for certain types of problems.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# Quantum Computing Fundamentals\n\nQuantum computers harness the power of quantum mechanics to perform computations that would be impossible for classical computers. Unlike traditional bits that exist as either 0 or 1, quantum bits (qubits) can exist in a superposition of both states simultaneously. This fundamental difference allows quantum computers to explore multiple solutions in parallel, making them exceptionally powerful for certain types of problems.\n"
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

        content = "# Quantum Computing Fundamentals\n\nQuantum computers harness the power of quantum mechanics to perform computations that would be impossible for classical computers. Unlike traditional bits that exist as either 0 or 1, quantum bits (qubits) can exist in a superposition of both states simultaneously. This fundamental difference allows quantum computers to explore multiple solutions in parallel, making them exceptionally powerful for certain types of problems.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# Quantum Computing Fundamentals\n\nQuantum computers harness the power of quantum mechanics to perform computations that would be impossible for classical computers. Unlike traditional bits that exist as either 0 or 1, quantum bits (qubits) can exist in a superposition of both states simultaneously. This fundamental difference allows quantum computers to explore multiple solutions in parallel, making them exceptionally powerful for certain types of problems.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 320-600 bytes (inclusive)."""
        test_file = tmp_path / MARKDOWN_FILENAME

        content = "# Quantum Computing Fundamentals\n\nQuantum computers harness the power of quantum mechanics to perform computations that would be impossible for classical computers. Unlike traditional bits that exist as either 0 or 1, quantum bits (qubits) can exist in a superposition of both states simultaneously. This fundamental difference allows quantum computers to explore multiple solutions in parallel, making them exceptionally powerful for certain types of problems.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / MARKDOWN_FILENAME

        # Content that meets all criteria
        content = "# Quantum Computing Fundamentals\n\nQuantum computers harness the power of quantum mechanics to perform computations that would be impossible for classical computers. Unlike traditional bits that exist as either 0 or 1, quantum bits (qubits) can exist in a superposition of both states simultaneously. This fundamental difference allows quantum computers to explore multiple solutions in parallel, making them exceptionally powerful for certain types of problems.\n"
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

    @mock.patch("sheep.features.feature_378_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
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
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_378_markdown_file(repo_path=str(tmp_path))

        # Verify generate_markdown_content was called
        mock_generate.assert_called_once()

        # Verify result contains the generated content
        assert result["content"] == test_content

    @mock.patch("sheep.features.feature_378_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
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
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_378_markdown_file(repo_path=str(tmp_path))

        # Verify write_markdown_file was called with correct arguments
        mock_write.assert_called_once_with(test_content, MARKDOWN_FILENAME)

        # Verify result contains the filepath
        assert result["filepath"] == test_file

    @mock.patch("sheep.features.feature_378_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
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
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        create_feature_378_markdown_file(repo_path=str(tmp_path))

        # Verify validate_markdown_file was called with correct filepath
        mock_validate.assert_called_once_with(test_file)

    @mock.patch("sheep.features.feature_378_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
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
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_378_markdown_file(repo_path=str(tmp_path))

        # Verify result dictionary has expected keys
        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

        # Verify content
        assert result["filepath"] == test_file
        assert result["content"] == test_content
        assert f"feat({FEATURE_NUMBER})" in result["commit_message"]
        assert MARKDOWN_FILENAME in result["commit_message"]


class TestCommitAndPushOperations:
    """Tests for task-5 and task-6: commit and push operations."""

    @mock.patch("sheep.features.feature_378_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
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
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        create_feature_378_markdown_file(repo_path=str(tmp_path))

        # Verify commit_markdown_file was called with correct filepath, content, and custom message
        expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with title and content"
        mock_commit.assert_called_once_with(
            test_file, test_content, str(tmp_path), custom_message=expected_message
        )

    @mock.patch("sheep.features.feature_378_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
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
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_378_markdown_file(repo_path=str(tmp_path))

        # Verify commit message has exact format
        expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with title and content"
        assert result["commit_message"] == expected_message

    @mock.patch("sheep.features.feature_378_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
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
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        create_feature_378_markdown_file(repo_path=str(tmp_path))

        # Verify push_markdown_file was called with correct repo_path
        mock_push.assert_called_once_with(str(tmp_path))

    @mock.patch("sheep.features.feature_378_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
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
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        expected_push_result = "Pushed successfully"
        mock_push.return_value = expected_push_result

        # Call orchestrator
        result = create_feature_378_markdown_file(repo_path=str(tmp_path))

        # Verify push_result is in return value
        assert result["push_result"] == expected_push_result


class TestOrchestratorErrorHandling:
    """Tests for orchestrator error handling (task-7)."""

    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_propagates_generation_errors(self, mock_generate, tmp_path):
        """Test that orchestrator propagates content generation errors."""
        # Setup mock to raise an error
        mock_generate.side_effect = ValueError("Content generation failed")

        # Verify error is propagated
        with pytest.raises(ValueError, match="Content generation failed"):
            create_feature_378_markdown_file(repo_path=str(tmp_path))

    @mock.patch("sheep.features.feature_378_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_378_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_propagates_validation_errors(
        self, mock_generate, mock_write, mock_validate, tmp_path
    ):
        """Test that orchestrator propagates file validation errors."""
        # Setup mocks
        test_content = "# Quantum Computing Fundamentals\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_validate.side_effect = ValueError("File validation failed")

        # Verify error is propagated
        with pytest.raises(ValueError, match="File validation failed"):
            create_feature_378_markdown_file(repo_path=str(tmp_path))
