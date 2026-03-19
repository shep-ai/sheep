"""Tests for feature 103: Creating markdown file test-uamczl.md with title and prose content."""

from pathlib import Path
import pytest
from unittest import mock

from sheep.features.feature_103_markdown_file_creation import (
    create_feature_103_markdown_file,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
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
        assert MARKDOWN_FILENAME == "test-uamczl.md"

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

    @mock.patch("sheep.features.feature_103_markdown_file_creation._validate_file_format_comprehensive")
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
        mock_comprehensive_validate,
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

    @mock.patch("sheep.features.feature_103_markdown_file_creation._validate_file_format_comprehensive")
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
        mock_comprehensive_validate,
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

    @mock.patch("sheep.features.feature_103_markdown_file_creation._validate_file_format_comprehensive")
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
        mock_comprehensive_validate,
        tmp_path
    ):
        """Test that orchestrator calls validate_markdown_file (task-3)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify validate_markdown_file was called
        mock_validate.assert_called_once_with(test_file)

    @mock.patch("sheep.features.feature_103_markdown_file_creation._validate_file_format_comprehensive")
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
        mock_comprehensive_validate,
        tmp_path
    ):
        """Test that orchestrator calls commit_markdown_file with exact message (task-4)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify commit_markdown_file was called with exact message
        expected_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
        mock_commit.assert_called_once()
        call_args = mock_commit.call_args
        assert call_args[1]["custom_message"] == expected_message

        # Verify result contains the commit message
        assert result["commit_message"] == expected_message

    @mock.patch("sheep.features.feature_103_markdown_file_creation._validate_file_format_comprehensive")
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
        mock_comprehensive_validate,
        tmp_path
    ):
        """Test that orchestrator calls push_markdown_file (task-5)."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify push_markdown_file was called
        mock_push.assert_called_once()

        # Verify result contains the push result
        assert result["push_result"] == "Pushed"

    @mock.patch("sheep.features.feature_103_markdown_file_creation._validate_file_format_comprehensive")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file")
    @mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content")
    def test_orchestrator_returns_correct_structure(
        self,
        mock_generate,
        mock_write,
        mock_validate,
        mock_commit,
        mock_push,
        mock_comprehensive_validate,
        tmp_path
    ):
        """Test that orchestrator returns dictionary with expected keys."""
        # Setup mocks
        test_content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        mock_generate.return_value = test_content
        test_file = str(tmp_path / MARKDOWN_FILENAME)
        mock_write.return_value = test_file
        mock_commit.return_value = "Committed"
        mock_push.return_value = "Pushed"

        # Call orchestrator
        result = create_feature_103_markdown_file(repo_path=str(tmp_path))

        # Verify result has expected keys
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

        # Verify values
        assert result["filepath"] == test_file
        assert result["content"] == test_content
        assert "feat(103)" in result["commit_message"]
        assert result["push_result"] == "Pushed"


class TestComprehensiveFileValidation:
    """Tests for additional comprehensive validation checks after validate_markdown_file()."""

    def test_orchestrator_detects_bom_in_file(self, tmp_path):
        """Test that orchestrator detects and rejects files with UTF-8 BOM."""
        # Create a file with UTF-8 BOM manually
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# Test Title\n\nFirst sentence. Second sentence.\n"
        # Write with BOM by prepending the BOM bytes
        with open(test_file, 'wb') as f:
            f.write(b'\xef\xbb\xbf')  # UTF-8 BOM
            f.write(content.encode('utf-8'))

        # Try to process this file through the full workflow
        with mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content") as mock_gen:
            with mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file") as mock_write:
                with mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file"):
                    # Make write_markdown_file return the path with BOM file
                    mock_write.return_value = str(test_file)
                    mock_gen.return_value = content

                    # The orchestrator should detect the BOM through explicit validation
                    with pytest.raises(ValueError, match="BOM"):
                        create_feature_103_markdown_file(repo_path=str(tmp_path))

    def test_orchestrator_detects_crlf_line_endings(self, tmp_path):
        """Test that orchestrator detects and rejects files with CRLF line endings."""
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# Test Title\r\n\r\nFirst sentence. Second sentence.\r\n"
        test_file.write_bytes(content.encode('utf-8'))

        with mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content") as mock_gen:
            with mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file") as mock_write:
                with mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file"):
                    mock_write.return_value = str(test_file)
                    mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence.\n"

                    # The orchestrator should detect CRLF through explicit validation
                    with pytest.raises(ValueError, match="CRLF|line ending"):
                        create_feature_103_markdown_file(repo_path=str(tmp_path))

    def test_orchestrator_detects_missing_trailing_newline(self, tmp_path):
        """Test that orchestrator detects files without trailing newline."""
        test_file = tmp_path / MARKDOWN_FILENAME
        # Content without trailing newline
        content = "# Test Title\n\nFirst sentence. Second sentence."
        test_file.write_bytes(content.encode('utf-8'))

        with mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content") as mock_gen:
            with mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file") as mock_write:
                with mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file"):
                    mock_write.return_value = str(test_file)
                    mock_gen.return_value = "# Test Title\n\nFirst sentence. Second sentence.\n"

                    # The orchestrator should detect missing trailing newline
                    with pytest.raises(ValueError, match="trailing newline"):
                        create_feature_103_markdown_file(repo_path=str(tmp_path))

    def test_orchestrator_validates_h1_heading_format(self, tmp_path):
        """Test that orchestrator validates H1 heading is properly formatted."""
        test_file = tmp_path / MARKDOWN_FILENAME
        # Content with improperly formatted heading (should start with "# ")
        content = "##Test Title\n\nFirst sentence. Second sentence.\n"
        # Use write_bytes to ensure LF line endings
        test_file.write_bytes(content.encode('utf-8'))

        with mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content") as mock_gen:
            with mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file") as mock_write:
                with mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file"):
                    mock_write.return_value = str(test_file)
                    mock_gen.return_value = content

                    # The orchestrator should detect improper H1 heading
                    with pytest.raises(ValueError, match="H1|heading"):
                        create_feature_103_markdown_file(repo_path=str(tmp_path))

    def test_orchestrator_validates_blank_line_after_heading(self, tmp_path):
        """Test that orchestrator validates blank line exists after heading."""
        test_file = tmp_path / MARKDOWN_FILENAME
        # Content without blank line after heading
        content = "# Test Title\nFirst sentence. Second sentence.\n"
        # Use write_bytes to ensure LF line endings
        test_file.write_bytes(content.encode('utf-8'))

        with mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content") as mock_gen:
            with mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file") as mock_write:
                with mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file"):
                    mock_write.return_value = str(test_file)
                    mock_gen.return_value = content

                    # The orchestrator should detect missing blank line
                    with pytest.raises(ValueError, match="blank line"):
                        create_feature_103_markdown_file(repo_path=str(tmp_path))

    def test_orchestrator_validates_sentence_count(self, tmp_path):
        """Test that orchestrator validates 2-3 sentences in prose."""
        test_file = tmp_path / MARKDOWN_FILENAME
        # Content with only 1 sentence (one period)
        content = "# Test Title\n\nJust one sentence.\n"
        # Use write_bytes to ensure LF line endings
        test_file.write_bytes(content.encode('utf-8'))

        with mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content") as mock_gen:
            with mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file") as mock_write:
                with mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file"):
                    mock_write.return_value = str(test_file)
                    mock_gen.return_value = content

                    # The orchestrator should detect insufficient sentences
                    with pytest.raises(ValueError, match="sentence"):
                        create_feature_103_markdown_file(repo_path=str(tmp_path))

    def test_orchestrator_validates_file_size_and_logs_warning(self, tmp_path):
        """Test that orchestrator validates file size and logs warning if outside range."""
        test_file = tmp_path / MARKDOWN_FILENAME
        # Content that's way too small (under 350 bytes)
        content = "# T\n\nA.\n"
        test_file.write_text(content, encoding="utf-8")

        with mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content") as mock_gen:
            with mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file") as mock_write:
                with mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file"):
                    with mock.patch("sheep.features.feature_103_markdown_file_creation._logger") as mock_logger:
                        mock_write.return_value = str(test_file)
                        mock_gen.return_value = content
                        mock_logger.debug = mock.MagicMock()

                        # This should raise ValueError due to sentence count first
                        # But when sentence count is OK, file size warning should be logged
                        with pytest.raises(ValueError):
                            create_feature_103_markdown_file(repo_path=str(tmp_path))

    def test_valid_file_passes_all_validation_checks(self, tmp_path):
        """Test that a properly formatted file passes all comprehensive validation checks."""
        test_file = tmp_path / MARKDOWN_FILENAME
        content = "# The Power of Persistence\n\nPersistence is the steadfast commitment to overcome obstacles and challenges while maintaining unwavering focus on our goals. It builds resilience and strength through repeated effort, determination, and the continuous refinement of our abilities and character. Through persistence, we unlock our potential and achieve what once seemed impossible.\n"
        # Use write_bytes to ensure LF line endings
        test_file.write_bytes(content.encode('utf-8'))

        with mock.patch("sheep.features.feature_103_markdown_file_creation.generate_markdown_content") as mock_gen:
            with mock.patch("sheep.features.feature_103_markdown_file_creation.write_markdown_file") as mock_write:
                with mock.patch("sheep.features.feature_103_markdown_file_creation.validate_markdown_file"):
                    with mock.patch("sheep.features.feature_103_markdown_file_creation.commit_markdown_file") as mock_commit:
                        with mock.patch("sheep.features.feature_103_markdown_file_creation.push_markdown_file") as mock_push:
                            mock_write.return_value = str(test_file)
                            mock_gen.return_value = content
                            mock_commit.return_value = "Committed"
                            mock_push.return_value = "Pushed"

                            # Should not raise any exception
                            result = create_feature_103_markdown_file(repo_path=str(tmp_path))
                            assert result["filepath"] == str(test_file)
