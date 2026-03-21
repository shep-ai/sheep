"""Tests for feature 148: markdown file creation."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock

from sheep.feature_148_markdown_file_creation import (
    task_2_generate_markdown_content,
    task_3_write_markdown_file_to_disk,
    main,
    FILENAME,
)


@pytest.fixture
def cleanup_test_file():
    """Clean up test file after each test."""
    yield
    # Cleanup after test
    test_file = Path(FILENAME)
    if test_file.exists():
        test_file.unlink()


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
def test_task_2_generates_markdown_content(mock_generate, cleanup_test_file):
    """Test task_2 calls generate_markdown_content and returns a string."""
    mock_content = "# Test Heading\n\nThis is a test sentence. This is another sentence."
    mock_generate.return_value = mock_content

    result = task_2_generate_markdown_content()

    assert isinstance(result, str)
    assert len(result) > 0
    assert "# " in result  # Contains H1 heading
    assert result == mock_content
    mock_generate.assert_called_once()


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
def test_task_2_returns_string_with_h1_heading(mock_generate, cleanup_test_file):
    """Test task_2 returns content starting with H1 heading."""
    mock_content = "# Example Topic\n\nThis is the first sentence. This is the second sentence."
    mock_generate.return_value = mock_content

    result = task_2_generate_markdown_content()

    assert result.startswith("# ")


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
def test_task_2_contains_sentences(mock_generate, cleanup_test_file):
    """Test task_2 returns content with sentences (contains periods)."""
    mock_content = "# Topic\n\nFirst sentence. Second sentence. Third sentence."
    mock_generate.return_value = mock_content

    result = task_2_generate_markdown_content()

    # Check for at least 2 periods (sentences)
    assert result.count(".") >= 2


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
def test_task_2_error_handling(mock_generate, cleanup_test_file):
    """Test task_2 propagates exceptions."""
    mock_generate.side_effect = ValueError("LLM failed")

    with pytest.raises(ValueError, match="LLM failed"):
        task_2_generate_markdown_content()


@patch("pathlib.Path.stat")
@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_task_3_writes_file_to_disk(mock_write, mock_stat, cleanup_test_file):
    """Test task_3 calls write_markdown_file and returns filepath."""
    test_content = "# Test\n\nTest content."
    mock_filepath = str(Path(FILENAME).absolute())
    mock_write.return_value = mock_filepath

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    result = task_3_write_markdown_file_to_disk(test_content)

    assert isinstance(result, str)
    assert FILENAME in result
    mock_write.assert_called_once_with(test_content, FILENAME)


@patch("pathlib.Path.stat")
@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_task_3_returns_filepath_with_correct_filename(mock_write, mock_stat, cleanup_test_file):
    """Test task_3 returns filepath containing the correct filename."""
    test_content = "# Topic\n\nSentence one. Sentence two."
    mock_filepath = str(Path(FILENAME).absolute())
    mock_write.return_value = mock_filepath

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    result = task_3_write_markdown_file_to_disk(test_content)

    assert FILENAME in result


@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_task_3_error_handling(mock_write, cleanup_test_file):
    """Test task_3 propagates exceptions."""
    mock_write.side_effect = IOError("File write failed")
    test_content = "# Test\n\nContent."

    with pytest.raises(IOError, match="File write failed"):
        task_3_write_markdown_file_to_disk(test_content)


@patch("pathlib.Path.stat")
@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_main_orchestrates_tasks(mock_write, mock_generate, mock_stat, cleanup_test_file):
    """Test main() orchestrates task_2 and task_3 in sequence."""
    mock_content = "# Test Topic\n\nFirst sentence. Second sentence."
    mock_filepath = str(Path(FILENAME).absolute())
    mock_generate.return_value = mock_content
    mock_write.return_value = mock_filepath

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(mock_content)
    mock_stat.return_value = mock_stat_result

    result = main()

    assert isinstance(result, dict)
    assert "content" in result
    assert "filepath" in result
    assert result["content"] == mock_content
    assert result["filepath"] == mock_filepath
    mock_generate.assert_called_once()
    mock_write.assert_called_once_with(mock_content, FILENAME)


@patch("pathlib.Path.stat")
@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_main_returns_dict_with_correct_keys(mock_write, mock_generate, mock_stat, cleanup_test_file):
    """Test main() returns dict with content and filepath keys."""
    mock_content = "# Example\n\nContent here. More content."
    mock_filepath = str(Path(FILENAME).absolute())
    mock_generate.return_value = mock_content
    mock_write.return_value = mock_filepath

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(mock_content)
    mock_stat.return_value = mock_stat_result

    result = main()

    assert set(result.keys()) == {"content", "filepath"}


@patch("pathlib.Path.stat")
@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_main_returns_non_empty_content(mock_write, mock_generate, mock_stat, cleanup_test_file):
    """Test main() returns non-empty content string."""
    mock_content = "# Title\n\nSentence one. Sentence two. Sentence three."
    mock_filepath = str(Path(FILENAME).absolute())
    mock_generate.return_value = mock_content
    mock_write.return_value = mock_filepath

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(mock_content)
    mock_stat.return_value = mock_stat_result

    result = main()

    assert result["content"]
    assert len(result["content"]) > 0


@patch("pathlib.Path.stat")
@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_main_returns_filepath_with_correct_filename(mock_write, mock_generate, mock_stat, cleanup_test_file):
    """Test main() returns filepath ending with correct filename."""
    mock_content = "# Test\n\nTest."
    mock_filepath = str(Path(FILENAME).absolute())
    mock_generate.return_value = mock_content
    mock_write.return_value = mock_filepath

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(mock_content)
    mock_stat.return_value = mock_stat_result

    result = main()

    assert result["filepath"].endswith(FILENAME)


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_main_error_in_task_2_propagates(mock_write, mock_generate, cleanup_test_file):
    """Test main() propagates exceptions from task_2."""
    mock_generate.side_effect = ValueError("Generation failed")

    with pytest.raises(ValueError, match="Generation failed"):
        main()


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("sheep.feature_148_markdown_file_creation.write_markdown_file")
def test_main_error_in_task_3_propagates(mock_write, mock_generate, cleanup_test_file):
    """Test main() propagates exceptions from task_3."""
    mock_content = "# Test\n\nContent."
    mock_generate.return_value = mock_content
    mock_write.side_effect = IOError("Write failed")

    with pytest.raises(IOError, match="Write failed"):
        main()
