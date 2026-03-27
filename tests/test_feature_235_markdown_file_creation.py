"""Tests for feature 235: markdown file creation."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from sheep.feature_235_markdown_file_creation import (
    create_markdown_file_235,
    FILENAME,
    FEATURE_NUMBER,
)


@pytest.fixture
def cleanup_test_file():
    """Clean up test file after each test."""
    yield
    # Cleanup after test
    test_file = Path(FILENAME)
    if test_file.exists():
        test_file.unlink()


class TestFeature235ModuleStructure:
    """Test that the feature module has the correct structure."""

    def test_filename_constant_is_correct(self):
        """Test that FILENAME constant is set to test-2k7sog.md."""
        assert FILENAME == "test-2k7sog.md"

    def test_feature_number_constant_is_correct(self):
        """Test that FEATURE_NUMBER constant is set to 235."""
        assert FEATURE_NUMBER == 235

    def test_create_markdown_file_235_function_exists(self):
        """Test that create_markdown_file_235 function exists and is callable."""
        assert callable(create_markdown_file_235)


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_orchestrates_all_steps(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that create_markdown_file_235 orchestrates all required steps."""
    # Setup mocks
    test_content = "# Test Topic\n\nTest sentence one. Test sentence two."
    test_filepath = str(Path(FILENAME).absolute())
    test_commit_msg = "feat(235): Create markdown file test-2k7sog.md with prose content"
    test_push_result = "Pushed to origin"

    mock_generate.return_value = test_content
    mock_write.return_value = test_filepath
    mock_validate.return_value = True
    mock_commit.return_value = "Commit successful"
    mock_push.return_value = test_push_result

    # Execute
    result = create_markdown_file_235()

    # Verify all helpers were called in correct order
    mock_generate.assert_called_once()
    mock_write.assert_called_once_with(test_content, FILENAME)
    mock_validate.assert_called_once_with(test_filepath)
    mock_commit.assert_called_once()
    mock_push.assert_called_once()

    # Verify result structure
    assert isinstance(result, dict)
    assert "filepath" in result
    assert "content" in result
    assert "commit_message" in result
    assert "push_result" in result

    # Verify result values
    assert result["filepath"] == test_filepath
    assert result["content"] == test_content
    assert result["commit_message"] == test_commit_msg
    assert result["push_result"] == test_push_result


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_returns_dict_with_correct_keys(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that function returns dictionary with all required keys."""
    # Setup mocks
    mock_generate.return_value = "# Test\n\nTest. Test."
    mock_write.return_value = "/path/to/test-2k7sog.md"
    mock_push.return_value = "Pushed"
    mock_commit.return_value = "Committed"

    # Execute
    result = create_markdown_file_235()

    # Verify dictionary structure
    expected_keys = {"filepath", "content", "commit_message", "push_result"}
    assert set(result.keys()) == expected_keys


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_commit_message_includes_feature_number(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that commit message includes feature number 235."""
    # Setup mocks
    mock_generate.return_value = "# Test\n\nTest. Test."
    mock_write.return_value = "/path/to/test-2k7sog.md"
    mock_push.return_value = "Pushed"

    # Execute
    result = create_markdown_file_235()

    # Verify commit message
    assert "235" in result["commit_message"]
    assert "feat(235)" in result["commit_message"]
    assert FILENAME in result["commit_message"]


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_handles_generation_failure(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that function propagates generation failures."""
    # Setup mock to raise exception
    mock_generate.side_effect = ValueError("LLM API failed")

    # Execute and verify exception is raised
    with pytest.raises(ValueError, match="LLM API failed"):
        create_markdown_file_235()


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_handles_write_failure(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that function propagates write failures."""
    # Setup mocks
    mock_generate.return_value = "# Test\n\nTest. Test."
    mock_write.side_effect = IOError("Cannot write file")

    # Execute and verify exception is raised
    with pytest.raises(IOError, match="Cannot write file"):
        create_markdown_file_235()

    # Verify write was called (generation completed)
    mock_generate.assert_called_once()
    mock_write.assert_called_once()


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_handles_validation_failure(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that function propagates validation failures."""
    # Setup mocks
    mock_generate.return_value = "# Test\n\nTest. Test."
    mock_write.return_value = "/path/to/test-2k7sog.md"
    mock_validate.side_effect = ValueError("File validation failed: invalid encoding")

    # Execute and verify exception is raised
    with pytest.raises(ValueError, match="File validation failed"):
        create_markdown_file_235()

    # Verify earlier steps were called
    mock_generate.assert_called_once()
    mock_write.assert_called_once()
    mock_validate.assert_called_once()


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_handles_commit_failure(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that function propagates commit failures."""
    # Setup mocks
    mock_generate.return_value = "# Test\n\nTest. Test."
    mock_write.return_value = "/path/to/test-2k7sog.md"
    mock_validate.return_value = True
    mock_commit.side_effect = Exception("Git commit failed: user.name not set")

    # Execute and verify exception is raised
    with pytest.raises(Exception, match="Git commit failed"):
        create_markdown_file_235()

    # Verify earlier steps were called
    mock_generate.assert_called_once()
    mock_write.assert_called_once()
    mock_validate.assert_called_once()


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_handles_push_failure(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that function propagates push failures."""
    # Setup mocks
    mock_generate.return_value = "# Test\n\nTest. Test."
    mock_write.return_value = "/path/to/test-2k7sog.md"
    mock_validate.return_value = True
    mock_commit.return_value = "Committed"
    mock_push.side_effect = Exception("Git push failed: network error")

    # Execute and verify exception is raised
    with pytest.raises(Exception, match="Git push failed"):
        create_markdown_file_235()

    # Verify all steps up to push were called
    mock_generate.assert_called_once()
    mock_write.assert_called_once()
    mock_validate.assert_called_once()
    mock_commit.assert_called_once()


@patch("sheep.feature_235_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_235_markdown_file_creation.write_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.validate_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.commit_markdown_file")
@patch("sheep.feature_235_markdown_file_creation.push_markdown_file")
def test_create_markdown_file_235_commit_uses_custom_message(
    mock_push,
    mock_commit,
    mock_validate,
    mock_write,
    mock_generate,
    cleanup_test_file,
):
    """Test that create_markdown_file_235 passes custom commit message to commit helper."""
    # Setup mocks
    mock_generate.return_value = "# Test\n\nTest. Test."
    mock_write.return_value = "/path/to/test-2k7sog.md"
    mock_push.return_value = "Pushed"

    # Execute
    create_markdown_file_235()

    # Verify commit was called with custom_message parameter
    mock_commit.assert_called_once()
    call_kwargs = mock_commit.call_args[1]
    assert "custom_message" in call_kwargs
    assert call_kwargs["custom_message"] == f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with prose content"
