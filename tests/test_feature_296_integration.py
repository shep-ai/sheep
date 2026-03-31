"""Integration tests for feature 296: Testing actual markdown file creation with mocked LLM.

This test module validates the complete feature execution:
- File creation with actual I/O (not mocked)
- Content generation with mocked LLM API
- Git operations with real subprocess calls
- File validation with actual file properties checks
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_296_markdown_file_creation import (
    create_test_v4dx46_markdown_file,
    main,
)


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary git repository for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    # Initialize git repo
    subprocess.run(
        ["git", "init"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )

    # Configure git user (required for commits)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_path,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_path,
        capture_output=True,
        check=True,
    )

    # Create a feature branch
    subprocess.run(
        ["git", "checkout", "-b", "feat/296-markdown-file-creation-67ee89"],
        cwd=repo_path,
        capture_output=True,
        check=True,
    )

    # Create initial commit on the branch
    initial_file = repo_path / "README.md"
    initial_file.write_text("# Test Repo\n")
    subprocess.run(
        ["git", "add", "."],
        cwd=repo_path,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "initial commit"],
        cwd=repo_path,
        capture_output=True,
        check=True,
    )

    return str(repo_path)


class TestFeatureExecution:
    """Integration tests for feature 296 execution."""

    def test_create_markdown_file_execution_success(self, temp_repo, monkeypatch):
        """Test that feature execution creates markdown file successfully."""
        # Mock the LLM API to return valid markdown content
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        # Change to temp repo directory so file is written there
        monkeypatch.chdir(temp_repo)

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.return_value = {"content": mock_content}
            mock_llm.return_value = mock_llm_instance

            # Execute feature
            result = create_test_v4dx46_markdown_file(repo_path=temp_repo)

            # Verify result dict structure
            assert isinstance(result, dict)
            assert "filepath" in result
            assert "content" in result
            assert "commit_message" in result
            assert "push_result" in result

            # Verify file was created
            file_path = Path(result["filepath"])
            assert file_path.exists()
            assert file_path.name == "test-v4dx46.md"

            # Verify file is in repo root
            assert file_path.parent == Path(temp_repo)

    def test_created_file_has_correct_encoding(self, temp_repo):
        """Test that created file uses UTF-8 encoding without BOM."""
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.return_value = {"content": mock_content}
            mock_llm.return_value = mock_llm_instance

            result = create_test_v4dx46_markdown_file(repo_path=temp_repo)

            file_path = Path(result["filepath"])
            binary_content = file_path.read_bytes()

            # Check for UTF-8 BOM (should not be present)
            assert not binary_content.startswith(b"\xef\xbb\xbf")

            # Verify can be decoded as UTF-8
            text_content = file_path.read_text(encoding="utf-8")
            assert text_content == mock_content

    def test_created_file_has_lf_line_endings(self, temp_repo):
        """Test that created file uses LF line endings."""
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.return_value = {"content": mock_content}
            mock_llm.return_value = mock_llm_instance

            result = create_test_v4dx46_markdown_file(repo_path=temp_repo)

            file_path = Path(result["filepath"])
            binary_content = file_path.read_bytes()

            # Check for CRLF (should not be present)
            assert b"\r\n" not in binary_content
            # Check for LF (should be present)
            assert b"\n" in binary_content

    def test_created_file_has_correct_structure(self, temp_repo):
        """Test that created file has correct markdown structure."""
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.return_value = {"content": mock_content}
            mock_llm.return_value = mock_llm_instance

            result = create_test_v4dx46_markdown_file(repo_path=temp_repo)

            file_path = Path(result["filepath"])
            text_content = file_path.read_text(encoding="utf-8")
            lines = text_content.split("\n")

            # Check H1 heading
            assert lines[0].startswith("# ")
            # Check blank line
            assert lines[1] == ""
            # Check prose content
            prose = "\n".join(lines[2:]).strip()
            assert len(prose) > 0

    def test_created_file_size_within_range(self, temp_repo):
        """Test that created file size is between 400-600 bytes."""
        mock_content = "# The Evolution of Software Development Practices\n\nSoftware development has undergone significant transformation over the past several decades, from early mainframe-based systems to modern cloud-native architectures and microservices. The adoption of agile methodologies, continuous integration and deployment practices, and automated testing has fundamentally changed how teams collaborate and deliver value to users. These evolutionary changes reflect the industry's commitment to improving code quality, reducing time-to-market, and creating more resilient and maintainable systems.\n"

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.return_value = {"content": mock_content}
            mock_llm.return_value = mock_llm_instance

            result = create_test_v4dx46_markdown_file(repo_path=temp_repo)

            file_path = Path(result["filepath"])
            file_size = len(file_path.read_bytes())

            assert 400 <= file_size <= 600

    def test_main_returns_zero_on_success(self, temp_repo, monkeypatch):
        """Test that main() returns 0 on successful execution."""
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        # Change to temp repo directory
        monkeypatch.chdir(temp_repo)

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.return_value = {"content": mock_content}
            mock_llm.return_value = mock_llm_instance

            result = main()

            assert result == 0
            assert isinstance(result, int)

    def test_main_returns_one_on_failure(self, temp_repo, monkeypatch):
        """Test that main() returns 1 on failure."""
        # Change to temp repo directory
        monkeypatch.chdir(temp_repo)

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.side_effect = Exception("LLM API failed")
            mock_llm.return_value = mock_llm_instance

            result = main()

            assert result == 1
            assert isinstance(result, int)

    def test_git_commit_message_is_correct(self, temp_repo):
        """Test that git commit message follows conventional commit format."""
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.return_value = {"content": mock_content}
            mock_llm.return_value = mock_llm_instance

            result = create_test_v4dx46_markdown_file(repo_path=temp_repo)

            # Verify commit message format
            commit_message = result["commit_message"]
            assert "feat(296):" in commit_message
            assert "create markdown file test-v4dx46.md with prose content" in commit_message

    def test_feature_execution_no_unhandled_exceptions(self, temp_repo):
        """Test that feature execution completes without unhandled exceptions."""
        mock_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"

        with patch("sheep.content_generators.get_reasoning_llm") as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm_instance.call.return_value = {"content": mock_content}
            mock_llm.return_value = mock_llm_instance

            # Should not raise any exception
            try:
                result = create_test_v4dx46_markdown_file(repo_path=temp_repo)
                assert result is not None
                assert isinstance(result, dict)
            except Exception as e:
                pytest.fail(f"Feature execution raised unexpected exception: {e}")
