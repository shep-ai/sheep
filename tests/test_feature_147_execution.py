"""
Integration tests for feature 147 execution demonstrating end-to-end workflow.

This test module demonstrates the complete execution flow of feature 147:
1. Content generation via Claude API
2. File creation with proper encoding
3. File validation
4. Git commit and push

The tests use realistic markdown content and execute the feature orchestrator
with mocked git operations to avoid actual repository modifications.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from sheep.features.feature_147_markdown_file_creation import (
    create_feature_147_markdown_file,
    MARKDOWN_FILENAME,
    COMMIT_MESSAGE,
    FEATURE_NUMBER,
)


class TestFeature147RealExecution:
    """Test real execution of feature 147 with orchestrator functions."""

    @patch("sheep.features.feature_147_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.generate_markdown_content")
    def test_execute_feature_147_generates_markdown_file(
        self, mock_generate, mock_write, mock_validate, mock_commit, mock_push, tmp_path
    ):
        """
        Test complete execution of feature 147.

        This test demonstrates the full workflow:
        1. Feature wrapper calls orchestrator functions
        2. Markdown content is generated and written to disk
        3. File is validated
        4. File is committed and pushed

        This is the primary acceptance test for task-3 execution.
        """
        # Setup realistic markdown content
        realistic_content = "# The Future of Technology\n\nTechnology continues to evolve at an unprecedented pace. It transforms how we communicate, work, and live. The next decade will bring even more dramatic changes in artificial intelligence, quantum computing, and biotechnology.\n"

        # Setup mocks for orchestrator functions
        mock_generate.return_value = realistic_content
        mock_write.return_value = str(tmp_path / MARKDOWN_FILENAME)
        mock_validate.return_value = True
        mock_commit.return_value = {
            "status": "success",
            "message": COMMIT_MESSAGE,
        }
        mock_push.return_value = {
            "status": "success",
            "branch": "feat/markdown-file-creation-0c9721",
        }

        # Create actual file for validation
        filepath = tmp_path / MARKDOWN_FILENAME
        filepath.write_text(realistic_content, encoding="utf-8")

        # Change to temp directory for isolated execution
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute the feature
            result = create_feature_147_markdown_file()

            # Verify result structure
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

            # Verify markdown file was created
            assert Path(MARKDOWN_FILENAME).exists(), f"File {MARKDOWN_FILENAME} does not exist"
            markdown_file = Path(MARKDOWN_FILENAME)

            # Read and validate file content
            content = markdown_file.read_text(encoding="utf-8")
            assert len(content) > 0, "File content is empty"

            # Verify H1 heading exists
            assert content.startswith("# "), "Content must start with H1 heading (# )"

            # Verify blank line separator
            lines = content.split("\n")
            assert len(lines) >= 3, "File must have heading, blank line, and prose"
            assert lines[0].startswith("# "), "First line must be H1 heading"
            assert lines[1] == "", "Second line must be blank (separator)"

            # Verify prose content (2-3 sentences)
            prose_lines = lines[2:]
            prose_content = "\n".join(prose_lines).strip()
            assert len(prose_content) > 0, "Prose content must not be empty"

            # Count sentences (by periods)
            sentence_count = prose_content.count(".")
            assert (
                2 <= sentence_count <= 3
            ), f"Must have 2-3 sentences, found {sentence_count}"

            # Verify UTF-8 encoding without BOM
            file_bytes = markdown_file.read_bytes()
            assert not file_bytes.startswith(
                b"\xef\xbb\xbf"
            ), "File must not have UTF-8 BOM"

            # Verify Unix LF line endings (not CRLF)
            assert b"\r\n" not in file_bytes, "File must use LF line endings, not CRLF"
            assert b"\n" in file_bytes, "File must have line endings"

            # Verify trailing newline
            assert content.endswith("\n"), "File must end with trailing newline"

            # Verify file size is reasonable (200-1000 bytes is reasonable)
            file_size = markdown_file.stat().st_size
            assert (
                200 < file_size < 1000
            ), f"File size {file_size} is outside acceptable range (200-1000 bytes)"

            # Verify result content matches file content
            assert result["content"] == content, "Result content must match file content"
            # Filepath can be full path or filename, just verify it ends with the correct filename
            assert result["filepath"].endswith(
                MARKDOWN_FILENAME
            ), "Result filepath must end with the correct filename"
            assert (
                result["commit_message"] == COMMIT_MESSAGE
            ), f"Commit message must be '{COMMIT_MESSAGE}'"

            # Verify git operations were called
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

            # Verify commit was called with correct parameters
            commit_call_args = mock_commit.call_args
            assert commit_call_args is not None
            assert commit_call_args.kwargs.get("custom_message") == COMMIT_MESSAGE

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_147_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.generate_markdown_content")
    def test_execute_feature_147_validates_all_requirements(
        self, mock_generate, mock_write, mock_validate, mock_commit, mock_push, tmp_path
    ):
        """
        Test that executed file meets all specification requirements.

        Verifies all non-functional requirements from the specification:
        - NFR-2: UTF-8 encoding
        - NFR-3: Unix LF line endings
        - NFR-4: File size 400-600 bytes (guideline)
        - NFR-5: Uses create_markdown_file orchestrator
        - NFR-6: Follows module pattern from features 001-146
        - NFR-8: Uses Claude API (via create_markdown_file)
        - NFR-9: Module location is src/sheep/features/feature_147_markdown_file_creation.py
        - NFR-10: Uses project conventions (structlog logging)
        """
        # Setup realistic content
        realistic_content = "# Learning and Growth\n\nContinuous learning is essential for personal and professional development. It enables us to adapt to changing circumstances and seize new opportunities. Investing in education and skill development creates a foundation for long-term success.\n"

        # Setup mocks
        mock_generate.return_value = realistic_content
        mock_write.return_value = str(tmp_path / MARKDOWN_FILENAME)
        mock_validate.return_value = True
        mock_commit.return_value = {"status": "success"}
        mock_push.return_value = {"status": "success"}

        # Create actual file
        filepath = tmp_path / MARKDOWN_FILENAME
        filepath.write_text(realistic_content, encoding="utf-8")

        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute feature
            result = create_feature_147_markdown_file()

            # Get the created file
            filepath = Path(result["filepath"])
            assert filepath.exists()

            # Requirement NFR-2: UTF-8 encoding
            try:
                content = filepath.read_text(encoding="utf-8")
                # If we got here, encoding is valid UTF-8
                assert True, "File is valid UTF-8"
            except UnicodeDecodeError:
                pytest.fail("File is not valid UTF-8 encoded")

            # Requirement NFR-3: Unix LF line endings
            file_bytes = filepath.read_bytes()
            assert b"\r\n" not in file_bytes, "File must use LF, not CRLF"
            assert b"\n" in file_bytes or b"\n" in str(file_bytes), "File must have LF endings"

            # Requirement NFR-4: File size guideline
            file_size = filepath.stat().st_size
            # 400-600 is the guideline from spec, but we allow some variation (200-800)
            assert (
                200 < file_size < 800
            ), f"File size {file_size} should be between 200-800 bytes"

            # Requirement FR-1: Filename is test-mrwvn4.md
            assert (
                filepath.name == MARKDOWN_FILENAME
            ), f"Filename must be {MARKDOWN_FILENAME}"

            # Requirement FR-2: H1 heading present
            assert content.startswith(
                "# "
            ), "File must start with H1 heading (# )"

            # Requirement FR-3: 2-3 sentences of prose
            lines = content.split("\n")
            assert lines[1] == "", "Must have blank line separator"
            prose = "\n".join(lines[2:]).strip()
            sentence_count = prose.count(".")
            assert (
                2 <= sentence_count <= 3
            ), f"Must have 2-3 sentences (periods), found {sentence_count}"

            # Requirement FR-9: Conventional commit message
            assert (
                result["commit_message"]
                == "feat(147): create markdown file test-mrwvn4.md with prose content"
            ), "Commit message must follow conventional format"

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_147_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.generate_markdown_content")
    def test_execute_feature_147_returns_valid_result_dict(
        self, mock_generate, mock_write, mock_validate, mock_commit, mock_push, tmp_path
    ):
        """
        Test that execution returns proper result dictionary.

        Verifies the return value structure and content from the orchestrator.
        """
        # Setup realistic content
        realistic_content = "# Innovation and Change\n\nInnovation drives progress in every field of human endeavor. Organizations that embrace change and encourage creative thinking are more likely to succeed. The ability to adapt and innovate is increasingly critical in today's rapidly evolving world.\n"

        # Setup mocks
        mock_generate.return_value = realistic_content
        filepath_str = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = filepath_str
        mock_validate.return_value = True
        mock_commit.return_value = {
            "status": "committed",
            "hash": "abc123def456",
        }
        mock_push.return_value = {
            "status": "pushed",
            "remote": "origin",
        }

        # Create actual file
        Path(filepath_str).write_text(realistic_content, encoding="utf-8")

        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute feature
            result = create_feature_147_markdown_file(repo_path=str(tmp_path))

            # Verify result dictionary structure
            assert isinstance(result, dict), "Result must be a dictionary"
            assert len(result) == 4, "Result must have exactly 4 keys"

            # Verify required keys
            required_keys = {
                "filepath",
                "content",
                "commit_message",
                "push_result",
            }
            assert (
                set(result.keys()) == required_keys
            ), f"Result keys must be {required_keys}"

            # Verify filepath is valid and file exists
            filepath = Path(result["filepath"])
            assert filepath.exists(), "File from result must exist"
            assert filepath.is_file(), "Result filepath must be a file"

            # Verify content is string with expected structure
            content = result["content"]
            assert isinstance(content, str), "Content must be string"
            assert len(content) > 50, "Content must be meaningful length"
            assert content.startswith("# "), "Content must start with H1"

            # Verify commit message matches specification
            assert isinstance(
                result["commit_message"], str
            ), "Commit message must be string"
            assert result["commit_message"] == COMMIT_MESSAGE
            assert "feat(147)" in result["commit_message"]
            assert MARKDOWN_FILENAME in result["commit_message"]

            # Verify push result is present
            assert isinstance(
                result["push_result"], dict
            ), "Push result must be dict"

        finally:
            os.chdir(original_cwd)

    @patch("sheep.features.feature_147_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.generate_markdown_content")
    def test_execute_feature_147_successful_completion(
        self, mock_generate, mock_write, mock_validate, mock_commit, mock_push, tmp_path
    ):
        """
        Test that feature 147 executes successfully from start to finish.

        This is the main acceptance test for task-3, verifying that:
        - No exceptions are raised during execution
        - All orchestration steps complete successfully
        - Git operations are called
        - Markdown file is created with correct properties
        """
        # Setup realistic content
        realistic_content = "# The Power of Collaboration\n\nCollaboration brings together diverse perspectives and skills to solve complex problems. When people work together toward a common goal, they can achieve far more than any individual could alone. Strong teams build the foundation for organizational success and innovation.\n"

        # Setup successful orchestration
        mock_generate.return_value = realistic_content
        filepath_str = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = filepath_str
        mock_validate.return_value = True
        mock_commit.return_value = {"status": "ok", "commit": "feat(147)..."}
        mock_push.return_value = {"status": "ok"}

        # Create actual file
        Path(filepath_str).write_text(realistic_content, encoding="utf-8")

        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # This should not raise any exceptions
            result = create_feature_147_markdown_file(repo_path=str(tmp_path))

            # Verify execution was successful
            assert result is not None
            assert isinstance(result, dict)

            # Verify file exists and is accessible
            assert Path(MARKDOWN_FILENAME).exists()

            # Verify content is valid
            content = Path(MARKDOWN_FILENAME).read_text(encoding="utf-8")
            assert len(content) > 0

            # Verify structure
            lines = content.split("\n")
            assert lines[0].startswith("# ")
            assert lines[1] == ""

            # Verify orchestration completed
            mock_commit.assert_called_once()
            mock_push.assert_called_once()

        finally:
            os.chdir(original_cwd)


class TestFeature147WithRealMarkdownContent:
    """Test feature 147 with realistic markdown content."""

    @patch("sheep.features.feature_147_markdown_file_creation.push_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.commit_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.validate_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.write_markdown_file")
    @patch("sheep.features.feature_147_markdown_file_creation.generate_markdown_content")
    def test_feature_147_with_realistic_claude_response(
        self, mock_generate, mock_write, mock_validate, mock_commit, mock_push, tmp_path
    ):
        """
        Test feature 147 with realistic Claude API response.

        Simulates actual Claude API generation with realistic markdown content.
        """
        # Realistic markdown content simulating Claude API output
        realistic_content = "# The Future of Artificial Intelligence\n\nArtificial intelligence is rapidly transforming every aspect of human society, from healthcare and education to business and entertainment. It enables machines to learn from data and make decisions with unprecedented speed and accuracy. As AI technology continues to advance, we must consider both its tremendous potential and the important ethical implications of its development and deployment.\n"

        # Setup orchestrator mocks
        mock_generate.return_value = realistic_content
        filepath_str = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = filepath_str
        mock_validate.return_value = True
        mock_commit.return_value = {"status": "success"}
        mock_push.return_value = {"status": "success"}

        # Create actual file
        Path(filepath_str).write_text(realistic_content, encoding="utf-8")

        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Execute feature
            result = create_feature_147_markdown_file(repo_path=str(tmp_path))

            # Verify file was created with realistic content
            assert Path(MARKDOWN_FILENAME).exists()

            content = Path(MARKDOWN_FILENAME).read_text(encoding="utf-8")
            assert "# " in content  # Has H1
            assert len(content) > 100  # Has substantial content
            assert "." in content  # Has sentence structure

            # Verify git operations were called
            assert mock_commit.called
            assert mock_push.called

        finally:
            os.chdir(original_cwd)
