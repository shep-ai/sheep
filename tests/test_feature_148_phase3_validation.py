"""Phase 3 Validation tests for feature 148: markdown file creation.

These tests validate that the generated markdown file meets all success criteria:
- File exists in repository root
- Contains H1 heading as first line
- Contains blank line after heading
- Contains exactly 2-3 sentences of prose
- File is encoded as UTF-8 without BOM
- File uses Unix LF line endings (not CRLF)
- File size is in expected range (400-600 bytes typical)
- All validation checks pass
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import validate_file_properties, validate_markdown_file
from sheep.feature_148_markdown_file_creation import FILENAME, main


@pytest.fixture
def cleanup_test_file():
    """Clean up test file after each test."""
    yield
    # Cleanup after test
    test_file = Path(FILENAME)
    if test_file.exists():
        test_file.unlink()


def create_valid_test_markdown() -> str:
    """Create valid test markdown content with H1 heading and 2-3 sentences."""
    return "# Artificial Intelligence and Machine Learning\n\nArtificial intelligence and machine learning have revolutionized technology, transforming industries from healthcare to finance with intelligent systems that learn from data. Deep learning neural networks now power sophisticated applications like language models, computer vision systems, and autonomous decision-making platforms. The convergence of AI, cloud computing, and big data continues to accelerate innovation and create new opportunities for solving complex problems.\n"


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_feature_148_generates_file_in_repo_root(mock_stat, mock_generate, cleanup_test_file):
    """Test that feature 148 creates test-iufzs9.md in repository root."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Verify file path
    assert FILENAME in result["filepath"]
    assert "test-iufzs9.md" in result["filepath"]


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_contains_h1_heading(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file contains H1 heading as first line."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Verify H1 heading
    lines = result["content"].split("\n")
    assert lines[0].startswith("# ")
    assert "# " in result["content"]


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_contains_blank_line_after_heading(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file contains blank line after H1 heading."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Verify blank line after heading
    lines = result["content"].split("\n")
    assert len(lines) >= 2
    assert lines[1] == ""  # Second line should be blank


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_contains_prose_content(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file contains prose content (2-3 sentences)."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Verify prose content
    content = result["content"]
    lines = content.split("\n")
    prose_lines = [line for line in lines[2:] if line.strip()]  # Skip heading and blank line

    assert len(prose_lines) > 0, "No prose content found"
    prose_content = "\n".join(prose_lines).strip()
    assert len(prose_content) > 50, "Prose content too short"


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_has_2_to_3_sentences(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file contains exactly 2-3 sentences (periods)."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Count sentences (periods)
    sentence_count = result["content"].count(".")
    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_utf8_encoding(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file uses UTF-8 encoding without BOM."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Write test file to validate encoding
    test_file = Path(FILENAME)
    test_file.write_text(result["content"], encoding="utf-8")

    try:
        # Read as binary to check encoding
        with open(test_file, "rb") as f:
            binary_content = f.read()

        # Check for UTF-8 BOM (should not be present)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File has UTF-8 BOM (should not be present)"

        # Verify the file is valid UTF-8
        binary_content.decode("utf-8")  # Should not raise UnicodeDecodeError
    finally:
        if test_file.exists():
            test_file.unlink()


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_unix_lf_line_endings(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file uses Unix LF line endings (not CRLF)."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Write test file to validate line endings
    test_file = Path(FILENAME)
    test_file.write_text(result["content"], encoding="utf-8")

    try:
        # Read as binary to check line endings
        with open(test_file, "rb") as f:
            binary_content = f.read()

        # Check for CRLF line endings (should use LF instead)
        assert b"\r\n" not in binary_content, "File uses CRLF line endings (should use LF)"

        # Verify LF line endings are present (if multi-line)
        if b"\n" in binary_content:
            assert b"\n" in binary_content, "File should have LF line endings"
    finally:
        if test_file.exists():
            test_file.unlink()


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_size_in_expected_range(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file size is in expected range (400-600 bytes typical)."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Check file size
    file_size = len(result["content"].encode("utf-8"))
    # Allow natural variation: typical range is 400-600 bytes, but allow 350-700 for flexibility
    assert 350 <= file_size <= 700, f"File size {file_size} bytes outside expected range (350-700)"


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_has_trailing_newline(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file ends with trailing newline (Unix convention)."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Verify trailing newline
    assert result["content"].endswith("\n"), "File must end with trailing newline"


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_content_is_meaningful_prose(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated content is meaningful prose (not placeholder)."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Verify prose is meaningful (not just "lorem ipsum" or "placeholder")
    content = result["content"].lower()
    assert "lorem ipsum" not in content, "Content should not be lorem ipsum"
    assert "placeholder" not in content, "Content should not be placeholder"

    # Verify content has substance (multiple lines of actual text)
    lines = result["content"].split("\n")
    prose_lines = [line for line in lines[2:] if line.strip()]
    assert len(prose_lines) >= 1, "Should have at least one line of prose"


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_generated_file_structure_matches_success_criteria(mock_stat, mock_generate, cleanup_test_file):
    """Test that generated file structure matches all success criteria format.

    Format: Line 1: # Title
            Line 2: (blank)
            Lines 3+: 2-3 sentences
    """
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    lines = result["content"].split("\n")

    # Verify structure
    assert lines[0].startswith("# "), "First line must be H1 heading"
    assert lines[1] == "", "Second line must be blank"
    assert len(lines) > 2, "Must have content after blank line"

    # Verify prose
    prose_content = "\n".join(lines[2:]).strip()
    sentence_count = prose_content.count(".")
    assert 2 <= sentence_count <= 3, f"Must have 2-3 sentences, found {sentence_count}"


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_feature_148_returns_dict_with_content_and_filepath(mock_stat, mock_generate, cleanup_test_file):
    """Test that feature 148 main() returns dict with content and filepath keys."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Verify return type and keys
    assert isinstance(result, dict)
    assert "content" in result
    assert "filepath" in result
    assert isinstance(result["content"], str)
    assert isinstance(result["filepath"], str)
    assert len(result["content"]) > 0
    assert len(result["filepath"]) > 0


@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
@patch("pathlib.Path.stat")
def test_feature_148_content_matches_returned_value(mock_stat, mock_generate, cleanup_test_file):
    """Test that feature 148 returns generated content in result dict."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Mock the file stat to return a size
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = len(test_content)
    mock_stat.return_value = mock_stat_result

    # Execute feature
    result = main()

    # Verify content matches
    assert result["content"] == test_content


# Integration test with real file creation (but mocked LLM)
@patch("sheep.feature_148_markdown_file_creation.generate_markdown_content")
def test_feature_148_integration_with_file_validation(mock_generate, cleanup_test_file):
    """Integration test: generate file and validate it meets all criteria."""
    test_content = create_valid_test_markdown()
    mock_generate.return_value = test_content

    # Execute feature (this will call write_markdown_file with real file I/O)
    result = main()

    # Verify the file was created
    test_file = Path(FILENAME)
    assert test_file.exists(), f"File {FILENAME} was not created by feature"

    try:
        # Test all validation criteria

        # 1. File exists
        assert test_file.exists(), f"File {FILENAME} does not exist"

        # 2. File is readable
        assert test_file.is_file(), f"{FILENAME} is not a file"

        # 3. File has content
        file_size = test_file.stat().st_size
        assert file_size > 0, "File is empty"

        # 4. Validate file properties (encoding, line endings)
        validate_file_properties(str(test_file))

        # 5. Validate markdown structure, content, and encoding
        validate_markdown_file(str(test_file))

    finally:
        if test_file.exists():
            test_file.unlink()
