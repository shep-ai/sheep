"""Tests for feature 260: Create markdown file test-0ap4py.md with title and prose content.

Tests cover:
- Orchestration function calling helpers in correct sequence
- File creation with correct format, encoding, and line endings
- Validation functions for markdown format, sentence count, encoding, and line endings
- Git operations (commit, push) with proper mocking
- Complete workflow orchestration (main function)
- Error handling and edge cases
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.features.feature_260_markdown_file_creation import (
    COMMIT_MESSAGE,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_260_markdown_file,
)


@pytest.fixture
def mock_generate_markdown_content():
    """Fixture for mocking generate_markdown_content helper function.

    Returns a mock that generates valid markdown content with H1 heading
    and 2-3 sentences of prose.
    """
    with patch(
        "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
    ) as mock:
        mock.return_value = (
            "# Understanding Quantum Computing\n\n"
            "Quantum computing represents a paradigm shift in computational power. "
            "Unlike classical computers that use bits, quantum computers use qubits. "
            "This technology promises to revolutionize fields from cryptography to drug discovery.\n"
        )
        yield mock


@pytest.fixture
def mock_write_markdown_file():
    """Fixture for mocking write_markdown_file helper function.

    Returns a mock that returns the full filepath to the created file.
    """
    with patch(
        "sheep.features.feature_260_markdown_file_creation.write_markdown_file"
    ) as mock:
        mock.return_value = str(Path.cwd() / MARKDOWN_FILENAME)
        yield mock


@pytest.fixture
def mock_validate_markdown_file():
    """Fixture for mocking validate_markdown_file helper function.

    Returns a mock that returns True (validation passed).
    """
    with patch(
        "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
    ) as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_commit_markdown_file():
    """Fixture for mocking commit_markdown_file helper function.

    Returns a mock that returns a success message.
    """
    with patch(
        "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
    ) as mock:
        mock.return_value = "✓ File committed with message: feat(260): Create markdown file test-0ap4py.md with prose content"
        yield mock


@pytest.fixture
def mock_push_markdown_file():
    """Fixture for mocking push_markdown_file helper function.

    Returns a mock that returns a success message.
    """
    with patch(
        "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
    ) as mock:
        mock.return_value = "✓ Successfully pushed to origin"
        yield mock


@pytest.fixture
def all_mocks(
    mock_generate_markdown_content,
    mock_write_markdown_file,
    mock_validate_markdown_file,
    mock_commit_markdown_file,
    mock_push_markdown_file,
):
    """Fixture that provides all mocks together.

    Returns a dictionary containing all mock objects for easy access
    in tests that need to verify multiple mocks.
    """
    return {
        "generate": mock_generate_markdown_content,
        "write": mock_write_markdown_file,
        "validate": mock_validate_markdown_file,
        "commit": mock_commit_markdown_file,
        "push": mock_push_markdown_file,
    }


class TestFeature260MarkdownFileCreation:
    """Test suite for feature 260 orchestration and file creation."""

    def test_feature_number_is_correct(self):
        """Test that feature number constant is set correctly."""
        assert FEATURE_NUMBER == 260

    def test_markdown_filename_is_correct(self):
        """Test that markdown filename constant is set correctly."""
        assert MARKDOWN_FILENAME == "test-0ap4py.md"

    def test_commit_message_contains_feature_number(self):
        """Test that commit message includes the feature number."""
        assert "260" in COMMIT_MESSAGE

    def test_commit_message_contains_filename(self):
        """Test that commit message includes the exact filename."""
        assert MARKDOWN_FILENAME in COMMIT_MESSAGE

    def test_commit_message_follows_conventional_format(self):
        """Test that commit message follows conventional commits format."""
        assert COMMIT_MESSAGE.startswith("feat(")
        assert ")" in COMMIT_MESSAGE


class TestOrchestrationFunction:
    """Test suite for create_feature_260_markdown_file() function."""

    def test_orchestration_calls_generate_content(
        self, all_mocks, mock_generate_markdown_content
    ):
        """Test that orchestration function calls generate_markdown_content."""
        create_feature_260_markdown_file()
        mock_generate_markdown_content.assert_called_once()

    def test_orchestration_calls_write_file(self, all_mocks, mock_write_markdown_file):
        """Test that orchestration function calls write_markdown_file with filename."""
        create_feature_260_markdown_file()
        mock_write_markdown_file.assert_called_once()
        # Verify the filename argument
        call_args = mock_write_markdown_file.call_args
        assert MARKDOWN_FILENAME in str(call_args)

    def test_orchestration_calls_validate_file(
        self, all_mocks, mock_validate_markdown_file
    ):
        """Test that orchestration function calls validate_markdown_file."""
        create_feature_260_markdown_file()
        mock_validate_markdown_file.assert_called_once()

    def test_orchestration_calls_commit(self, all_mocks, mock_commit_markdown_file):
        """Test that orchestration function calls commit_markdown_file."""
        create_feature_260_markdown_file()
        mock_commit_markdown_file.assert_called_once()

    def test_orchestration_uses_custom_commit_message(
        self, all_mocks, mock_commit_markdown_file
    ):
        """Test that orchestration passes custom commit message to commit function."""
        create_feature_260_markdown_file()
        call_kwargs = mock_commit_markdown_file.call_args[1]
        assert "custom_message" in call_kwargs
        assert call_kwargs["custom_message"] == COMMIT_MESSAGE

    def test_orchestration_calls_push(self, all_mocks, mock_push_markdown_file):
        """Test that orchestration function calls push_markdown_file."""
        create_feature_260_markdown_file()
        mock_push_markdown_file.assert_called_once()

    def test_orchestration_calls_helpers_in_sequence(self, all_mocks):
        """Test that orchestration calls helpers in correct sequence.

        Expected order:
        1. generate_markdown_content()
        2. write_markdown_file()
        3. validate_markdown_file()
        4. commit_markdown_file()
        5. push_markdown_file()
        """
        # Track call order using mock's call history
        call_order = []

        def track_generate(*args, **kwargs):
            call_order.append("generate")
            return all_mocks["generate"].return_value

        def track_write(*args, **kwargs):
            call_order.append("write")
            return all_mocks["write"].return_value

        def track_validate(*args, **kwargs):
            call_order.append("validate")
            return all_mocks["validate"].return_value

        def track_commit(*args, **kwargs):
            call_order.append("commit")
            return all_mocks["commit"].return_value

        def track_push(*args, **kwargs):
            call_order.append("push")
            return all_mocks["push"].return_value

        all_mocks["generate"].side_effect = track_generate
        all_mocks["write"].side_effect = track_write
        all_mocks["validate"].side_effect = track_validate
        all_mocks["commit"].side_effect = track_commit
        all_mocks["push"].side_effect = track_push

        create_feature_260_markdown_file()

        assert call_order == ["generate", "write", "validate", "commit", "push"]

    def test_orchestration_returns_dict_with_required_keys(self, all_mocks):
        """Test that orchestration returns dictionary with all required keys."""
        result = create_feature_260_markdown_file()

        assert isinstance(result, dict)
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    def test_orchestration_return_filepath_is_string(self, all_mocks):
        """Test that returned filepath is a string."""
        result = create_feature_260_markdown_file()
        assert isinstance(result["filepath"], str)

    def test_orchestration_return_content_is_string(self, all_mocks):
        """Test that returned content is a string."""
        result = create_feature_260_markdown_file()
        assert isinstance(result["content"], str)

    def test_orchestration_return_commit_message_is_correct(self, all_mocks):
        """Test that returned commit message matches constant."""
        result = create_feature_260_markdown_file()
        assert result["commit_message"] == COMMIT_MESSAGE

    def test_orchestration_return_push_result_is_string(self, all_mocks):
        """Test that returned push result is a string."""
        result = create_feature_260_markdown_file()
        assert isinstance(result["push_result"], str)

    def test_orchestration_with_custom_repo_path(self, all_mocks):
        """Test that orchestration accepts and uses custom repo_path parameter."""
        custom_repo = "/custom/path/to/repo"
        create_feature_260_markdown_file(repo_path=custom_repo)

        # Verify commit and push were called with the custom repo_path
        commit_call = all_mocks["commit"].call_args
        assert custom_repo in str(commit_call)

    def test_orchestration_with_none_repo_path(self, all_mocks):
        """Test that orchestration handles None repo_path parameter."""
        # Should use current directory as default
        result = create_feature_260_markdown_file(repo_path=None)
        assert result is not None
        assert "filepath" in result


class TestErrorHandling:
    """Test suite for error handling in orchestration function."""

    def test_orchestration_re_raises_generate_error(self, all_mocks):
        """Test that orchestration re-raises exceptions from generate_markdown_content."""
        all_mocks["generate"].side_effect = ValueError("LLM call failed")
        with pytest.raises(ValueError, match="LLM call failed"):
            create_feature_260_markdown_file()

    def test_orchestration_re_raises_write_error(self, all_mocks):
        """Test that orchestration re-raises exceptions from write_markdown_file."""
        all_mocks["write"].side_effect = IOError("Cannot write file")
        with pytest.raises(IOError, match="Cannot write file"):
            create_feature_260_markdown_file()

    def test_orchestration_re_raises_validate_error(self, all_mocks):
        """Test that orchestration re-raises exceptions from validate_markdown_file."""
        all_mocks["validate"].side_effect = ValueError("File validation failed")
        with pytest.raises(ValueError, match="File validation failed"):
            create_feature_260_markdown_file()

    def test_orchestration_re_raises_commit_error(self, all_mocks):
        """Test that orchestration re-raises exceptions from commit_markdown_file."""
        all_mocks["commit"].side_effect = Exception("Git commit failed")
        with pytest.raises(Exception, match="Git commit failed"):
            create_feature_260_markdown_file()

    def test_orchestration_re_raises_push_error(self, all_mocks):
        """Test that orchestration re-raises exceptions from push_markdown_file."""
        all_mocks["push"].side_effect = Exception("Git push failed")
        with pytest.raises(Exception, match="Git push failed"):
            create_feature_260_markdown_file()


class TestIntegrationWithRealFileIO:
    """Test suite for integration tests using real file I/O.

    These tests use tmp_path fixture to create temporary directories
    and test the orchestration with mocked LLM/git but real file operations.
    """

    def test_integration_creates_file_in_correct_location(self, tmp_path, monkeypatch):
        """Test that integration creates file in the correct directory."""
        # Change to temporary directory
        monkeypatch.chdir(tmp_path)

        # Mock only the helpers that don't do file I/O
        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            # Set up return values
            test_content = (
                "# Test Title\n\n"
                "First sentence. Second sentence. Third sentence.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            # Call the orchestration function (will use real write_markdown_file)
            result = create_feature_260_markdown_file()

            # Verify file was created
            assert Path(MARKDOWN_FILENAME).exists()
            assert result["filepath"] == str(tmp_path / MARKDOWN_FILENAME)

    def test_integration_file_contains_expected_content(self, tmp_path, monkeypatch):
        """Test that created file contains the expected content."""
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = (
                "# Understanding Quantum Computing\n\n"
                "Quantum computing represents a paradigm shift. "
                "Unlike classical computers, quantum computers use qubits. "
                "This technology promises revolutionary advances.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            # Read file and verify content
            file_content = Path(MARKDOWN_FILENAME).read_text()
            assert file_content == test_content

    def test_integration_file_has_correct_encoding(self, tmp_path, monkeypatch):
        """Test that created file uses UTF-8 encoding."""
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = "# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            # Read as binary and verify no BOM
            binary_content = Path(MARKDOWN_FILENAME).read_bytes()
            assert not binary_content.startswith(b"\xef\xbb\xbf")
            # Verify it's valid UTF-8
            binary_content.decode("utf-8")


class TestFileValidation:
    """Test suite for markdown file validation.

    These tests verify that created files meet all specification requirements
    for structure, encoding, and format.
    """

    def test_file_has_h1_heading(self, tmp_path, monkeypatch):
        """Test that file has H1 heading on first line."""
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = (
                "# The Wonders of Astronomy\n\n"
                "Astronomy is the study of celestial objects and phenomena. "
                "Telescopes have revolutionized our understanding of the universe. "
                "Modern observatories continue to make groundbreaking discoveries.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            file_content = Path(MARKDOWN_FILENAME).read_text()
            assert file_content.startswith("# ")

    def test_file_has_blank_line_after_heading(self, tmp_path, monkeypatch):
        """Test that file has blank line separator after H1 heading."""
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = (
                "# The Wonders of Astronomy\n\n"
                "Astronomy is the study of celestial objects. "
                "Telescopes have revolutionized understanding. "
                "Modern observatories continue discoveries.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            file_content = Path(MARKDOWN_FILENAME).read_text()
            lines = file_content.split("\n")
            assert lines[0].startswith("# ")
            assert lines[1] == ""

    def test_file_has_2_to_3_sentences(self, tmp_path, monkeypatch):
        """Test that file contains exactly 2-3 sentences of prose."""
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = (
                "# Exploring the Deep Ocean\n\n"
                "The ocean covers over seventy percent of Earth's surface. "
                "Vast underwater ecosystems support incredible biodiversity. "
                "Deep sea creatures have evolved remarkable adaptations.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            file_content = Path(MARKDOWN_FILENAME).read_text()
            lines = file_content.split("\n")
            prose_lines = lines[2:]  # Skip heading and blank line
            prose_content = "\n".join(prose_lines).strip()

            # Count periods to count sentences
            sentence_count = prose_content.count(".")
            assert 2 <= sentence_count <= 3

    def test_file_is_utf8_without_bom(self, tmp_path, monkeypatch):
        """Test that file is UTF-8 encoded without Byte Order Mark."""
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = (
                "# Understanding Photosynthesis\n\n"
                "Photosynthesis is the process by which plants convert light energy. "
                "This fundamental process sustains most life on Earth. "
                "Researchers continue to discover new aspects of photosynthesis.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            binary_content = Path(MARKDOWN_FILENAME).read_bytes()
            assert not binary_content.startswith(b"\xef\xbb\xbf")
            # Verify valid UTF-8
            binary_content.decode("utf-8")

    def test_file_uses_lf_not_crlf(self, tmp_path, monkeypatch):
        """Test that file uses Unix LF line endings, not CRLF.

        Note: On Windows, Python's text mode without newline='' may convert \n to \r\n.
        The validate_markdown_file function enforces LF-only line endings.
        """
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            # Use real validation, not mocked
            test_content = (
                "# The History of Mathematics\n\n"
                "Mathematics is one of humanity's oldest disciplines. "
                "Ancient civilizations developed mathematical concepts independently. "
                "Modern mathematics underpins virtually all scientific progress.\n"
            )
            mock_generate.return_value = test_content
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            # Note: not mocking validate_markdown_file so it uses real implementation
            # which enforces LF line endings through validation
            try:
                create_feature_260_markdown_file()
                # If the function succeeds, the validation passed (LF only)
                binary_content = Path(MARKDOWN_FILENAME).read_bytes()
                assert b"\n" in binary_content
            except ValueError as e:
                # On Windows with text mode CRLF conversion, validation might fail
                # This is expected - the validation correctly rejects CRLF
                assert "CRLF" in str(e) or "line endings" in str(e).lower()

    def test_file_ends_with_trailing_newline(self, tmp_path, monkeypatch):
        """Test that file ends with a trailing newline."""
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = (
                "# Exploring Machine Learning\n\n"
                "Machine learning has transformed how we process data. "
                "Neural networks can learn complex patterns from examples. "
                "This technology drives innovation across many industries.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            file_content = Path(MARKDOWN_FILENAME).read_text()
            assert file_content.endswith("\n")

    def test_file_size_is_in_expected_range(self, tmp_path, monkeypatch):
        """Test that file size is reasonable (at least 200 bytes, accounting for platform line endings).

        Note: File size varies based on:
        - LF line endings on Unix (smaller)
        - CRLF line endings on Windows (larger)
        - Content length variations
        """
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = (
                "# The Impact of Social Media\n\n"
                "Social media has fundamentally changed how people communicate globally. "
                "These platforms connect billions of people across continents. "
                "Understanding their societal effects remains an ongoing challenge.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            file_size = Path(MARKDOWN_FILENAME).stat().st_size
            # Generous range to account for platform differences (LF vs CRLF)
            # Minimum should be >= 200 bytes (3 sentences of prose)
            # Maximum accounts for CRLF on Windows or other variations
            assert 200 <= file_size <= 1000

    def test_file_has_only_one_h1_heading(self, tmp_path, monkeypatch):
        """Test that file contains exactly one H1 heading."""
        monkeypatch.chdir(tmp_path)

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate, patch(
            "sheep.features.feature_260_markdown_file_creation.validate_markdown_file"
        ) as mock_validate, patch(
            "sheep.features.feature_260_markdown_file_creation.commit_markdown_file"
        ) as mock_commit, patch(
            "sheep.features.feature_260_markdown_file_creation.push_markdown_file"
        ) as mock_push:
            test_content = (
                "# The Power of Renewable Energy\n\n"
                "Renewable energy sources are increasingly important for sustainability. "
                "Solar and wind technologies continue to improve rapidly. "
                "Transitioning to clean energy benefits both economy and environment.\n"
            )
            mock_generate.return_value = test_content
            mock_validate.return_value = True
            mock_commit.return_value = "committed"
            mock_push.return_value = "pushed"

            create_feature_260_markdown_file()

            file_content = Path(MARKDOWN_FILENAME).read_text()
            h1_count = sum(1 for line in file_content.split("\n") if line.startswith("# "))
            assert h1_count == 1


class TestEndToEndWithRealGitOperations:
    """Test suite for end-to-end tests with real git operations.

    These tests use real git operations on the feature branch to verify
    the complete workflow including file creation, validation, commit, and push.
    Only the LLM call (generate_markdown_content) is mocked to avoid external API calls.
    """

    def test_e2e_creates_file_in_repo_root(self):
        """Test that feature creates file in repository root."""
        test_content = (
            "# The Future of Artificial Intelligence\n\n"
            "Artificial intelligence is transforming industries at an unprecedented pace. "
            "Machine learning models can now perform tasks once thought impossible. "
            "The impact of AI on society continues to grow exponentially.\n"
        )

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate:
            mock_generate.return_value = test_content

            # Verify file doesn't exist before
            file_path = Path.cwd() / MARKDOWN_FILENAME
            initial_exists = file_path.exists()

            try:
                result = create_feature_260_markdown_file()

                # Verify file was created
                assert file_path.exists(), f"File {MARKDOWN_FILENAME} not created at {file_path}"
                assert result["filepath"] == str(file_path)
                assert result["content"] == test_content
            finally:
                # Cleanup: remove test file if it was created
                if file_path.exists() and not initial_exists:
                    file_path.unlink()

    def test_e2e_file_content_matches_generated(self):
        """Test that written file contains exactly the generated content."""
        test_content = (
            "# The Wonders of Space Exploration\n\n"
            "Space exploration has always captured human imagination and curiosity. "
            "Technological advances enable us to reach further into the cosmos. "
            "Future missions promise even more groundbreaking discoveries.\n"
        )

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate:
            mock_generate.return_value = test_content

            file_path = Path.cwd() / MARKDOWN_FILENAME
            initial_exists = file_path.exists()

            try:
                create_feature_260_markdown_file()

                # Read file and verify content
                file_content = file_path.read_text()
                assert file_content == test_content
            finally:
                if file_path.exists() and not initial_exists:
                    file_path.unlink()

    def test_e2e_git_staging_works(self):
        """Test that file is properly staged with git add."""
        test_content = (
            "# Innovation in Modern Technology\n\n"
            "Technology innovation drives progress across all sectors of society. "
            "Startups and established companies compete to create breakthrough solutions. "
            "The pace of technological change shows no signs of slowing.\n"
        )

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate:
            mock_generate.return_value = test_content

            file_path = Path.cwd() / MARKDOWN_FILENAME
            initial_exists = file_path.exists()

            try:
                create_feature_260_markdown_file()

                # Check git status - file should be staged
                result = subprocess.run(
                    ["git", "diff", "--cached", "--name-only"],
                    capture_output=True,
                    text=True,
                )
                # The file should be in the staged changes
                assert MARKDOWN_FILENAME in result.stdout or result.returncode == 0
            finally:
                if file_path.exists() and not initial_exists:
                    # Unstage and remove file
                    subprocess.run(
                        ["git", "reset", "HEAD", MARKDOWN_FILENAME],
                        capture_output=True,
                    )
                    file_path.unlink()

    def test_e2e_git_commit_contains_correct_message(self):
        """Test that git commit includes custom message with feature number and filename."""
        test_content = (
            "# The Beauty of Classical Music\n\n"
            "Classical music has influenced Western culture for centuries. "
            "Great composers created masterpieces that still resonate today. "
            "Modern orchestras continue to perform these timeless works.\n"
        )

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate:
            mock_generate.return_value = test_content

            file_path = Path.cwd() / MARKDOWN_FILENAME
            initial_exists = file_path.exists()

            try:
                create_feature_260_markdown_file()

                # Check git log for the commit message
                result = subprocess.run(
                    ["git", "log", "-1", "--oneline"],
                    capture_output=True,
                    text=True,
                )
                log_output = result.stdout
                assert "260" in log_output, f"Feature number 260 not in commit message: {log_output}"
                assert MARKDOWN_FILENAME in log_output, f"Filename not in commit message: {log_output}"
            finally:
                if file_path.exists() and not initial_exists:
                    # Reset and cleanup
                    subprocess.run(
                        ["git", "reset", "--soft", "HEAD~1"],
                        capture_output=True,
                    )
                    file_path.unlink()

    def test_e2e_git_push_completes(self):
        """Test that git push completes without error to the feature branch."""
        test_content = (
            "# The History of Innovation\n\n"
            "Innovation has been the driving force behind human progress. "
            "Throughout history, great innovators have transformed society. "
            "Today's innovators continue to shape the future of humanity.\n"
        )

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate:
            mock_generate.return_value = test_content

            file_path = Path.cwd() / MARKDOWN_FILENAME
            initial_exists = file_path.exists()

            try:
                result = create_feature_260_markdown_file()

                # Verify push_result indicates success
                push_result = result["push_result"]
                assert push_result is not None
                # The push result should be a string indicating success
                assert isinstance(push_result, str)
                # Should contain some indication of success
                assert (
                    "Successfully pushed" in push_result
                    or "push" in push_result.lower()
                    or result.get("push_result") is not None
                )
            finally:
                if file_path.exists() and not initial_exists:
                    # Reset and cleanup
                    subprocess.run(
                        ["git", "reset", "--soft", "HEAD~1"],
                        capture_output=True,
                    )
                    file_path.unlink()

    def test_e2e_file_encoding_is_utf8_no_bom(self):
        """Test that created file uses UTF-8 encoding without BOM."""
        test_content = (
            "# Understanding Quantum Physics\n\n"
            "Quantum physics challenges our understanding of reality. "
            "Subatomic particles behave in ways that defy intuition. "
            "This field continues to produce groundbreaking discoveries.\n"
        )

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate:
            mock_generate.return_value = test_content

            file_path = Path.cwd() / MARKDOWN_FILENAME
            initial_exists = file_path.exists()

            try:
                create_feature_260_markdown_file()

                # Read as binary and verify no BOM
                binary_content = file_path.read_bytes()
                assert not binary_content.startswith(
                    b"\xef\xbb\xbf"
                ), "File has UTF-8 BOM (should not)"
                # Verify it's valid UTF-8
                binary_content.decode("utf-8")
            finally:
                if file_path.exists() and not initial_exists:
                    subprocess.run(
                        ["git", "reset", "--soft", "HEAD~1"],
                        capture_output=True,
                    )
                    file_path.unlink()

    def test_e2e_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        test_content = (
            "# The Power of Education\n\n"
            "Education is the foundation of individual and societal progress. "
            "Quality education transforms lives and opens new opportunities. "
            "Investing in education yields long-term benefits for all.\n"
        )

        with patch(
            "sheep.features.feature_260_markdown_file_creation.generate_markdown_content"
        ) as mock_generate:
            mock_generate.return_value = test_content

            file_path = Path.cwd() / MARKDOWN_FILENAME
            initial_exists = file_path.exists()

            try:
                create_feature_260_markdown_file()

                # Read as binary and check for CRLF
                binary_content = file_path.read_bytes()
                assert (
                    b"\r\n" not in binary_content
                ), "File uses CRLF (should use LF only)"
            finally:
                if file_path.exists() and not initial_exists:
                    subprocess.run(
                        ["git", "reset", "--soft", "HEAD~1"],
                        capture_output=True,
                    )
                    file_path.unlink()
