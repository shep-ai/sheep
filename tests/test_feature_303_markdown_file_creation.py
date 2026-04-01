"""Tests for feature 303: Create markdown file test-t4bvyv.md with prose content."""

import os
from unittest.mock import patch

import pytest

from sheep.features.feature_303_markdown_file_creation import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_test_t4bvyv_markdown_file,
)

# Check if ANTHROPIC_API_KEY is set for integration tests
HAS_API_KEY = bool(os.getenv("ANTHROPIC_API_KEY"))


class TestFeature303Module:
    """Tests for feature 303 module structure and metadata."""

    def test_feature_number_is_303(self):
        """Test that FEATURE_NUMBER is 303."""
        assert FEATURE_NUMBER == 303

    def test_markdown_filename_is_correct(self):
        """Test that MARKDOWN_FILENAME is test-t4bvyv.md."""
        assert MARKDOWN_FILENAME == "test-t4bvyv.md"

    def test_feature_name_is_set(self):
        """Test that FEATURE_NAME is set."""
        assert FEATURE_NAME == "markdown-file-creation-67deea"

    def test_create_function_exists(self):
        """Test that create_test_t4bvyv_markdown_file function exists."""
        assert callable(create_test_t4bvyv_markdown_file)


class TestCreateFeature303Function:
    """Tests for create_test_t4bvyv_markdown_file function."""

    def test_function_signature_accepts_repo_path(self):
        """Test that function accepts repo_path parameter."""
        # Function should accept optional repo_path parameter
        # This test verifies the function is callable with this parameter
        assert create_test_t4bvyv_markdown_file.__code__.co_varnames[0] == "repo_path"

    def test_function_returns_dict(self):
        """Test that function would return a dictionary (checking structure)."""
        # Verify the function has the expected return annotation or docstring
        docstring = create_test_t4bvyv_markdown_file.__doc__
        assert "Dictionary containing" in docstring
        assert "filepath" in docstring
        assert "content" in docstring
        assert "commit_message" in docstring
        assert "push_result" in docstring

    def test_function_includes_logging(self):
        """Test that function includes logging implementation."""
        # Check that the module has logger configured
        from sheep.features.feature_303_markdown_file_creation import _logger

        assert _logger is not None

    def test_function_raises_on_failure(self):
        """Test that function documents exception behavior."""
        docstring = create_test_t4bvyv_markdown_file.__doc__
        assert "Raises" in docstring
        assert "ValueError" in docstring
        assert "IOError" in docstring
        assert "Exception" in docstring


class TestFeature303Integration:
    """Integration tests for feature 303 workflow."""

    def test_function_has_complete_docstring(self):
        """Test that function has comprehensive documentation."""
        docstring = create_test_t4bvyv_markdown_file.__doc__
        assert "orchestrates the complete workflow" in docstring.lower()
        assert "generate valid markdown content" in docstring.lower()
        assert "write file to repository root" in docstring.lower()
        assert "validate file meets" in docstring.lower()
        assert "stage and commit" in docstring.lower()
        assert "push to remote" in docstring.lower()

    def test_workflow_steps_in_docstring(self):
        """Test that docstring documents all 5 workflow steps."""
        docstring = create_test_t4bvyv_markdown_file.__doc__
        # Count occurrences of step references
        assert "1." in docstring
        assert "2." in docstring
        assert "3." in docstring
        assert "4." in docstring
        assert "5." in docstring

    def test_module_has_main_block(self):
        """Test that module has __main__ execution block."""
        import inspect

        # Import the module and check its source
        module = __import__(
            "sheep.features.feature_303_markdown_file_creation",
            fromlist=[""],
        )
        source = inspect.getsource(module)
        # Check that the module source includes __main__ execution
        assert 'if __name__ == "__main__"' in source


class TestContentGenerationTask:
    """Tests for task-1: Feature module with wrapper function."""

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_calls_create_markdown_file(self, mock_create):
        """Test that function calls create_markdown_file during workflow."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "pushed",
        }

        create_test_t4bvyv_markdown_file()

        mock_create.assert_called_once()

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_calls_create_markdown_file_with_correct_parameters(
        self, mock_create
    ):
        """Test that create_markdown_file is called with correct parameters."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "pushed",
        }

        create_test_t4bvyv_markdown_file()

        # Verify create_markdown_file was called with correct parameters
        call_args = mock_create.call_args
        assert call_args[1]["filename"] == MARKDOWN_FILENAME
        assert call_args[1]["feature_number"] == FEATURE_NUMBER

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_function_includes_logging(self, mock_create):
        """Test that function includes logging implementation."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Test\n\nThis is a test sentence. Another one. And a third.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "pushed",
        }

        with patch(
            "sheep.features.feature_303_markdown_file_creation._logger"
        ) as mock_logger:
            create_test_t4bvyv_markdown_file()

            # Verify INFO log for task start and completion
            info_calls = list(mock_logger.info.call_args_list)
            assert len(info_calls) > 0


class TestMainEntryPoint:
    """Tests for main() entry point."""

    def test_main_function_exists(self):
        """Test that main() function exists."""
        from sheep.features.feature_303_markdown_file_creation import main

        assert callable(main)

    def test_main_returns_int(self):
        """Test that main() returns an integer."""
        from sheep.features.feature_303_markdown_file_creation import main

        with patch(
            "sheep.features.feature_303_markdown_file_creation.create_test_t4bvyv_markdown_file"
        ) as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-t4bvyv.md",
                "content": "# Test\n\nThis is test. Another test.",
                "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
                "push_result": "pushed",
            }

            result = main()

            assert isinstance(result, int)

    def test_main_returns_zero_on_success(self):
        """Test that main() returns 0 on success."""
        from sheep.features.feature_303_markdown_file_creation import main

        with patch(
            "sheep.features.feature_303_markdown_file_creation.create_test_t4bvyv_markdown_file"
        ) as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-t4bvyv.md",
                "content": "# Test\n\nThis is test. Another test.",
                "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
                "push_result": "pushed",
            }

            result = main()

            assert result == 0

    def test_main_returns_one_on_failure(self):
        """Test that main() returns 1 on failure."""
        from sheep.features.feature_303_markdown_file_creation import main

        with patch(
            "sheep.features.feature_303_markdown_file_creation.create_test_t4bvyv_markdown_file"
        ) as mock_create:
            mock_create.side_effect = RuntimeError("Test error")

            result = main()

            assert result == 1

    def test_main_calls_create_function(self):
        """Test that main() calls create_test_t4bvyv_markdown_file()."""
        from sheep.features.feature_303_markdown_file_creation import main

        with patch(
            "sheep.features.feature_303_markdown_file_creation.create_test_t4bvyv_markdown_file"
        ) as mock_create:
            mock_create.return_value = {
                "filepath": "/repo/test-t4bvyv.md",
                "content": "# Test\n\nThis is test. Another test.",
                "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
                "push_result": "pushed",
            }

            main()

            mock_create.assert_called_once()

    def test_main_handles_exceptions_gracefully(self):
        """Test that main() handles exceptions gracefully."""
        from sheep.features.feature_303_markdown_file_creation import main

        with patch(
            "sheep.features.feature_303_markdown_file_creation.create_test_t4bvyv_markdown_file"
        ) as mock_create:
            mock_create.side_effect = RuntimeError("API error")

            with patch(
                "sheep.features.feature_303_markdown_file_creation._logger"
            ) as mock_logger:
                result = main()

                # Should not raise, but return error code
                assert result == 1
                # Should log the error
                error_calls = list(mock_logger.error.call_args_list)
                assert len(error_calls) > 0


class TestIntegrationTask2ExecutionEndToEnd:
    """Integration tests for task-2: Test feature module execution end-to-end."""

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_function_executes_without_exceptions(self, mock_create):
        """Test that create_test_t4bvyv_markdown_file executes without raising exceptions."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Artificial Intelligence\n\nArtificial intelligence is transforming industries and society. Machine learning models process vast amounts of data to discover patterns. This technology will reshape how we work and solve complex problems.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "pushed to feature branch",
        }

        # Should not raise any exception
        result = create_test_t4bvyv_markdown_file()

        assert result is not None

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_return_value_is_dict(self, mock_create):
        """Test that create_test_t4bvyv_markdown_file returns a dictionary."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Quantum Computing\n\nQuantum computing leverages quantum mechanics for computation. Traditional computers process bits as 0 or 1. Quantum computers use qubits that can be 0, 1, or both simultaneously.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "pushed",
        }

        result = create_test_t4bvyv_markdown_file()

        assert isinstance(result, dict)

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_return_dict_contains_required_keys(self, mock_create):
        """Test that returned dict contains required keys: filepath, content, commit_message, push_result."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Climate Action\n\nClimate change demands urgent action from individuals and nations. Renewable energy sources provide sustainable alternatives. Together we can build a better future for coming generations.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "success",
        }

        result = create_test_t4bvyv_markdown_file()

        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_filepath_is_not_none_and_not_empty(self, mock_create):
        """Test that return value filepath is not None and is non-empty string."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Space Exploration\n\nSpace exploration expands human knowledge and capability. Satellites provide essential services for communications. Future missions will establish permanent settlements on the Moon.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "success",
        }

        result = create_test_t4bvyv_markdown_file()

        assert result["filepath"] is not None
        assert isinstance(result["filepath"], str)
        assert len(result["filepath"]) > 0

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_content_starts_with_h1_heading(self, mock_create):
        """Test that return value content contains H1 markdown heading."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Ocean Conservation\n\nOcean health is crucial for all life on Earth. Plastic pollution threatens marine ecosystems daily. We must implement sustainable practices to protect our oceans.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "success",
        }

        result = create_test_t4bvyv_markdown_file()

        assert "#" in result["content"]
        # Content should start with H1 heading
        lines = result["content"].split("\n")
        assert len(lines) > 0
        assert lines[0].startswith("#")

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_commit_message_contains_feature_number(self, mock_create):
        """Test that return value commit_message contains feature number 303."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Renewable Energy\n\nRenewable energy sources reduce carbon emissions significantly. Solar and wind power are becoming increasingly affordable. Transitioning to clean energy creates jobs and protects the environment.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "success",
        }

        result = create_test_t4bvyv_markdown_file()

        assert "303" in result["commit_message"]
        assert "test-t4bvyv.md" in result["commit_message"]

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_push_result_indicates_success(self, mock_create):
        """Test that return value push_result contains indication of successful push."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Biodiversity\n\nBiodiversity is essential for ecosystem resilience and human survival. Species extinction rates are alarming globally. Conservation efforts must be strengthened to protect all life forms.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "pushed to feature branch",
        }

        result = create_test_t4bvyv_markdown_file()

        # Push result should contain indication of success
        assert result["push_result"] is not None
        assert isinstance(result["push_result"], str)
        assert len(result["push_result"]) > 0

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_logger_contains_info_messages(self, mock_create):
        """Test that logger messages include at least info-level entries for start and completion."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Education Innovation\n\nEducation technology transforms learning experiences for students worldwide. Digital tools enable personalized learning paths. Access to quality education becomes more equitable through innovation.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "success",
        }

        with patch(
            "sheep.features.feature_303_markdown_file_creation._logger"
        ) as mock_logger:
            create_test_t4bvyv_markdown_file()

            # Should have at least info-level logs for start and completion
            info_calls = list(mock_logger.info.call_args_list)
            assert len(info_calls) >= 2


class TestIntegrationTask2FunctionIntegration:
    """Tests for integration between feature module and orchestration function."""

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_calls_create_markdown_file_with_correct_filename(self, mock_create):
        """Test that create_test_t4bvyv_markdown_file calls create_markdown_file with correct filename."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Sustainable Cities\n\nSustainable cities integrate environmental and social considerations. Green infrastructure reduces urban heat. Smart planning creates livable communities for all residents.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "success",
        }

        create_test_t4bvyv_markdown_file()

        # Verify create_markdown_file was called with correct filename
        call_args = mock_create.call_args
        assert call_args[1]["filename"] == MARKDOWN_FILENAME
        assert call_args[1]["filename"] == "test-t4bvyv.md"

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_calls_create_markdown_file_with_feature_number_303(self, mock_create):
        """Test that create_test_t4bvyv_markdown_file calls create_markdown_file with feature_number=303."""
        mock_create.return_value = {
            "filepath": "/repo/test-t4bvyv.md",
            "content": "# Healthcare Innovation\n\nHealthcare innovation improves patient outcomes and quality of life. Telemedicine expands access to medical expertise. Artificial intelligence assists in diagnosis and treatment planning.",
            "commit_message": "feat(303): create markdown file test-t4bvyv.md with prose content",
            "push_result": "success",
        }

        create_test_t4bvyv_markdown_file()

        # Verify create_markdown_file was called with correct feature number
        call_args = mock_create.call_args
        assert call_args[1]["feature_number"] == FEATURE_NUMBER
        assert call_args[1]["feature_number"] == 303

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_exception_propagates_from_orchestration_function(self, mock_create):
        """Test that exceptions from create_markdown_file propagate correctly."""
        mock_create.side_effect = ValueError("Invalid content generated")

        with pytest.raises(ValueError, match="Invalid content generated"):
            create_test_t4bvyv_markdown_file()

    @patch("sheep.features.feature_303_markdown_file_creation.create_markdown_file")
    def test_io_error_from_orchestration_function_propagates(self, mock_create):
        """Test that IOError from create_markdown_file propagates."""
        mock_create.side_effect = OSError("Failed to write file")

        with pytest.raises(OSError, match="Failed to write file"):
            create_test_t4bvyv_markdown_file()


class TestFeature303EndToEndIntegration:
    """End-to-end integration tests for feature 303 (task-6)."""

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_file_is_created_in_repository_root(self):
        """Test that test-t4bvyv.md file is created in repository root."""
        from pathlib import Path

        # Store original path to ensure cleanup
        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        # Clean up before test if file exists from previous run
        if test_file.exists():
            test_file.unlink()

        try:
            # Execute the feature
            result = create_test_t4bvyv_markdown_file()

            # Verify file was created
            assert test_file.exists(), f"File {MARKDOWN_FILENAME} was not created"
            assert result["filepath"] is not None
            # Verify filepath ends with correct filename
            assert MARKDOWN_FILENAME in result["filepath"]
        finally:
            # Cleanup after test
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_file_contains_h1_heading(self):
        """Test that created file contains valid H1 markdown heading."""
        from pathlib import Path

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            # Verify file has H1 heading
            content = result["content"]
            lines = content.split("\n")
            assert len(lines) > 0, "Content is empty"
            assert lines[0].startswith("# "), f"First line is not H1 heading: {lines[0]}"
        finally:
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_file_contains_blank_line_after_h1(self):
        """Test that created file contains blank line immediately after H1 heading."""
        from pathlib import Path

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            # Verify blank line after H1
            content = result["content"]
            lines = content.split("\n")
            assert len(lines) >= 2, "Content has fewer than 2 lines"
            assert lines[0].startswith("# "), "First line is not H1"
            assert lines[1] == "", f"Second line is not blank: '{lines[1]}'"
        finally:
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_file_contains_2_to_3_sentences(self):
        """Test that created file contains exactly 2-3 sentences of prose content."""
        from pathlib import Path

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            # Count sentences (periods) in the prose
            content = result["content"]
            lines = content.split("\n")

            # Prose is lines[2:] (after H1 and blank line)
            prose = "\n".join(lines[2:])
            sentence_count = prose.count(".")

            # Should have 2-3 sentences (periods)
            assert 2 <= sentence_count <= 3, (
                f"Expected 2-3 sentences (periods), got {sentence_count}: {prose}"
            )
        finally:
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_file_is_utf8_encoded_without_bom(self):
        """Test that created file is UTF-8 encoded without BOM (byte order mark)."""
        from pathlib import Path

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            # Verify file bytes don't start with UTF-8 BOM
            file_bytes = test_file.read_bytes()

            # UTF-8 BOM is b'\xef\xbb\xbf'
            assert not file_bytes.startswith(b"\xef\xbb\xbf"), (
                "File contains UTF-8 BOM (should not)"
            )

            # Verify file can be decoded as UTF-8
            try:
                file_bytes.decode("utf-8")
            except UnicodeDecodeError as e:
                pytest.fail(f"File is not valid UTF-8: {e}")
        finally:
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_file_uses_unix_lf_line_endings(self):
        """Test that created file uses Unix LF line endings (no CRLF)."""
        from pathlib import Path

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            # Verify file uses LF not CRLF
            file_bytes = test_file.read_bytes()

            # Check that file doesn't contain CRLF (Windows line ending)
            assert b"\r\n" not in file_bytes, (
                "File contains CRLF line endings (should use LF)"
            )

            # File should contain LF characters for line breaks
            assert b"\n" in file_bytes, "File contains no LF line endings"
        finally:
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_commit_message_format_is_conventional(self):
        """Test that git commit message follows conventional commits format."""
        from pathlib import Path

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            # Verify commit message format
            commit_message = result["commit_message"]
            assert "feat(303)" in commit_message, (
                f"Commit message should contain 'feat(303)': {commit_message}"
            )
            assert "test-t4bvyv.md" in commit_message, (
                f"Commit message should contain filename: {commit_message}"
            )
            assert commit_message == (
                "feat(303): create markdown file test-t4bvyv.md with prose content"
            ), f"Unexpected commit message format: {commit_message}"
        finally:
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_returned_content_is_valid_string(self):
        """Test that returned content is a non-empty string."""
        from pathlib import Path

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            content = result["content"]
            assert isinstance(content, str), "Content should be a string"
            assert len(content) > 0, "Content should not be empty"
            assert len(content) > 100, (
                f"Content seems too short ({len(content)} chars)"
            )
        finally:
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_markdown_file_passes_validation(self):
        """Test that markdown file passes structure validation."""
        from pathlib import Path

        from sheep.content_generators import validate_markdown_file

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            # Validate file using the standard validation function
            try:
                is_valid = validate_markdown_file(test_file)
                assert (
                    is_valid is not False
                ), "File failed markdown structure validation"
            except Exception as e:
                pytest.fail(f"File validation raised exception: {e}")
        finally:
            if test_file.exists():
                test_file.unlink()

    @pytest.mark.skipif(
        not HAS_API_KEY, reason="ANTHROPIC_API_KEY not set - skipping API integration test"
    )
    def test_result_dict_contains_all_required_keys(self):
        """Test that result dictionary contains all required keys."""
        from pathlib import Path

        repo_path = Path.cwd()
        test_file = repo_path / MARKDOWN_FILENAME

        if test_file.exists():
            test_file.unlink()

        try:
            result = create_test_t4bvyv_markdown_file()

            # Verify all required keys exist
            required_keys = ["filepath", "content", "commit_message", "push_result"]
            for key in required_keys:
                assert key in result, f"Result dict missing key: {key}"
                assert result[key] is not None, f"Result[{key}] is None"
        finally:
            if test_file.exists():
                test_file.unlink()
