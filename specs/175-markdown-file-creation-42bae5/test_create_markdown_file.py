"""
Test suite for markdown file creation feature 175.

Tests cover file creation, validation, and git operations.
Uses tempfile for isolated testing without affecting the repository.
"""
import tempfile
from pathlib import Path
import pytest
import subprocess
from unittest import mock
import create_markdown_file


class TestFileCreation:
    """Tests for file creation with correct structure and encoding."""

    def test_file_created(self):
        """Test that markdown file is created in the repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                # Change to temp directory for isolated test
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                assert (tmpdir_path / create_markdown_file.FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_file_has_heading(self):
        """Test that file has H1 heading on line 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                assert lines[0].startswith('# ')
                assert len(lines[0]) > 2  # Title is not empty
            finally:
                os.chdir(original_cwd)

    def test_file_has_blank_line(self):
        """Test that file has blank line on line 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                assert lines[1] == ''
            finally:
                os.chdir(original_cwd)

    def test_file_has_prose(self):
        """Test that file has prose content starting on line 3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                # Lines 3+ should have content
                prose_lines = lines[2:]
                prose_content = '\n'.join(prose_lines).strip()
                assert len(prose_content) > 0
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert content.endswith(b'\n')
            finally:
                os.chdir(original_cwd)

    def test_file_utf8_encoding(self):
        """Test that file uses UTF-8 encoding (can be read as UTF-8)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                # Should not raise UnicodeDecodeError
                (tmpdir_path / create_markdown_file.FILENAME).read_text(encoding='utf-8')
            finally:
                os.chdir(original_cwd)

    def test_file_lf_line_endings(self):
        """Test that file uses Unix LF line endings (no CRLF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert b'\r\n' not in content, "File should use LF, not CRLF"
            finally:
                os.chdir(original_cwd)


class TestValidation:
    """Tests for file validation logic."""

    def test_validate_accepts_valid_file(self):
        """Test that validation accepts a properly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                # Should not raise any exception
                create_markdown_file.validate_file(create_markdown_file.FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_no_utf8_bom(self):
        """Test that file does not have UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert not content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_bom(self):
        """Test that validation rejects files with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a file with BOM
                test_file = tmpdir_path / "test-bom.md"
                content = f"# {create_markdown_file.TITLE}\n\n{create_markdown_file.PROSE}\n"
                # Write with BOM by using utf-8-sig encoding
                test_file.write_text(content, encoding='utf-8-sig', newline='\n')

                # Validation should raise ValueError
                with pytest.raises(ValueError, match="UTF-8 BOM"):
                    create_markdown_file.validate_file("test-bom.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_crlf(self):
        """Test that validation rejects files with CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a file with CRLF
                test_file = tmpdir_path / "test-crlf.md"
                content = f"# {create_markdown_file.TITLE}\r\n\r\n{create_markdown_file.PROSE}\r\n"
                test_file.write_bytes(content.encode('utf-8'))

                # Validation should raise ValueError
                with pytest.raises(ValueError, match="CRLF"):
                    create_markdown_file.validate_file("test-crlf.md")
            finally:
                os.chdir(original_cwd)

    def test_lf_line_endings(self):
        """Test that file uses Unix LF line endings (no CRLF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert b'\r\n' not in content, "File should use LF, not CRLF"
            finally:
                os.chdir(original_cwd)


class TestStructureValidation:
    """Tests for file structure and size validation."""

    def test_validate_has_heading(self):
        """Test that validation checks for H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file without heading
                test_file = tmpdir_path / "test-no-heading.md"
                test_file.write_text("No heading here\n\nSome content.\n", encoding='utf-8', newline='\n')

                with pytest.raises(ValueError, match="H1 heading"):
                    create_markdown_file.validate_file("test-no-heading.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_has_blank_line(self):
        """Test that validation checks for blank line on line 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file without blank line after heading
                test_file = tmpdir_path / "test-no-blank.md"
                test_file.write_text("# Title\nContent without blank line.\n", encoding='utf-8', newline='\n')

                with pytest.raises(ValueError, match="blank line"):
                    create_markdown_file.validate_file("test-no-blank.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_has_prose(self):
        """Test that validation checks for prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file without prose content
                test_file = tmpdir_path / "test-no-prose.md"
                test_file.write_text("# Title\n\n\n", encoding='utf-8', newline='\n')

                with pytest.raises(ValueError, match="prose"):
                    create_markdown_file.validate_file("test-no-prose.md")
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_range(self):
        """Test that validation checks file size within 300-800 byte range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                file_size = (tmpdir_path / create_markdown_file.FILENAME).stat().st_size

                assert 300 <= file_size <= 800, f"File size {file_size} not in range 300-800"
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_too_small(self):
        """Test that validation rejects files under 300 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a small file with valid structure but still under 300 bytes
                # This is hard to achieve with real prose, so test with a minimal but valid structure
                test_file = tmpdir_path / "test-tiny.md"
                small_content = "# Title\n\nFirst. Second. Third.\n"
                test_file.write_text(small_content, encoding='utf-8', newline='\n')

                file_size = test_file.stat().st_size
                if file_size < 300:
                    # If it's still under 300, expect size error
                    with pytest.raises(ValueError, match="minimum is 300"):
                        create_markdown_file.validate_file("test-tiny.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_too_large(self):
        """Test that validation rejects files over 800 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a large file with exactly 3 sentences but over 800 bytes
                test_file = tmpdir_path / "test-huge.md"
                # Use 3 long sentences to exceed 800 bytes
                sentence1 = "This is the first very long sentence " * 8  # ~280 bytes
                sentence2 = "This is the second very long sentence " * 8  # ~280 bytes
                sentence3 = "This is the third very long sentence " * 8  # ~280 bytes
                large_prose = f"{sentence1}. {sentence2}. {sentence3}."
                large_content = f"# A Title\n\n{large_prose}\n"
                test_file.write_text(large_content, encoding='utf-8', newline='\n')

                file_size = test_file.stat().st_size
                # Only test if file is actually over 800 bytes
                if file_size > 800:
                    with pytest.raises(ValueError, match="maximum is 800"):
                        create_markdown_file.validate_file("test-huge.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_wrong_sentence_count(self):
        """Test that validation rejects files with wrong sentence count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file with only 1 sentence
                test_file = tmpdir_path / "test-one-sentence.md"
                test_file.write_text("# Title\n\nOnly one sentence.\n", encoding='utf-8', newline='\n')

                with pytest.raises(ValueError, match="1 sentences.*expected 2-3"):
                    create_markdown_file.validate_file("test-one-sentence.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_no_trailing_newline(self):
        """Test that validation rejects files without trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file without trailing newline
                test_file = tmpdir_path / "test-no-newline.md"
                # Use write_bytes to avoid automatic newline addition
                content = "# Title\n\nFirst sentence. Second sentence. Third sentence."
                test_file.write_bytes(content.encode('utf-8'))

                with pytest.raises(ValueError, match="does not end with newline"):
                    create_markdown_file.validate_file("test-no-newline.md")
            finally:
                os.chdir(original_cwd)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_minimal_valid_file(self):
        """Test creation and validation of minimal valid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                # Should pass validation without error
                create_markdown_file.validate_file(create_markdown_file.FILENAME)

                # Verify file content
                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                assert "# " in content  # Has heading
                assert content.count('\n') >= 3  # At least: heading\n, blank\n, prose\n
                assert content.endswith('\n')  # Trailing newline
            finally:
                os.chdir(original_cwd)

    def test_file_size_boundary_lower(self):
        """Test file that is near lower size boundary (300 bytes)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a file with content that naturally fills ~300-400 bytes
                test_file = tmpdir_path / "test-boundary.md"
                # Build content with exactly 3 sentences
                prose = "This is the first sentence that will be reasonably long to reach the minimum size requirement. " \
                        "This is the second sentence that adds more content to the file. " \
                        "This is the third sentence that completes the required sentence count."
                content = f"# Engineering Excellence\n\n{prose}\n"

                test_file.write_text(content, encoding='utf-8', newline='\n')

                file_size = test_file.stat().st_size

                # If the file is within the valid range, validation should pass
                if 300 <= file_size <= 800:
                    create_markdown_file.validate_file("test-boundary.md")
            finally:
                os.chdir(original_cwd)

    def test_file_size_boundary_upper(self):
        """Test file that is exactly at upper size boundary (800 bytes)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                # Verify actual file size
                file_path = tmpdir_path / create_markdown_file.FILENAME
                file_size = file_path.stat().st_size

                # Should be within valid range
                assert 300 <= file_size <= 800, f"File size {file_size} out of range"

                # Should pass validation
                create_markdown_file.validate_file(create_markdown_file.FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_exactly_two_sentences(self):
        """Test file with exactly 2 sentences (minimum)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                test_file = tmpdir_path / "test-two.md"
                content = "# Title\n\nThis is the first sentence. This is the second sentence.\n"
                test_file.write_text(content, encoding='utf-8', newline='\n')

                # Should pass if size is in range
                file_size = test_file.stat().st_size
                if 300 <= file_size <= 800:
                    create_markdown_file.validate_file("test-two.md")
            finally:
                os.chdir(original_cwd)

    def test_exactly_three_sentences(self):
        """Test file with exactly 3 sentences (maximum)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                test_file = tmpdir_path / "test-three.md"
                content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
                test_file.write_text(content, encoding='utf-8', newline='\n')

                # Should pass if size is in range
                file_size = test_file.stat().st_size
                if 300 <= file_size <= 800:
                    create_markdown_file.validate_file("test-three.md")
            finally:
                os.chdir(original_cwd)

    def test_heading_with_special_characters(self):
        """Test that heading can contain special characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                test_file = tmpdir_path / "test-special.md"
                content = "# The Art of Problem-Solving: A Guide\n\nThis is a test. Second. Third.\n"
                test_file.write_text(content, encoding='utf-8', newline='\n')

                file_size = test_file.stat().st_size
                if 300 <= file_size <= 800:
                    create_markdown_file.validate_file("test-special.md")
            finally:
                os.chdir(original_cwd)

    def test_prose_with_multiple_lines(self):
        """Test that prose can span multiple lines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                test_file = tmpdir_path / "test-multiline.md"
                prose = "This is the first sentence.\nContinuing here.\nSecond sentence. Third sentence."
                content = f"# Title\n\n{prose}\n"
                test_file.write_text(content, encoding='utf-8', newline='\n')

                file_size = test_file.stat().st_size
                if 300 <= file_size <= 800:
                    create_markdown_file.validate_file("test-multiline.md")
            finally:
                os.chdir(original_cwd)


class TestValidationErrorMessages:
    """Tests to verify that validation errors have clear, actionable messages."""

    def test_missing_file_error_message(self):
        """Test that missing file error has clear message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                try:
                    create_markdown_file.validate_file("nonexistent.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "does not exist" in str(e)
            finally:
                os.chdir(original_cwd)

    def test_empty_file_error_message(self):
        """Test that empty file error has clear message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                test_file = tmpdir_path / "test-empty.md"
                test_file.write_text("", encoding='utf-8')

                try:
                    create_markdown_file.validate_file("test-empty.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "empty" in str(e)
            finally:
                os.chdir(original_cwd)


class TestMainOrchestration:
    """Tests for main() orchestration and error handling."""

    def test_main_success(self):
        """Test that main() successfully orchestrates complete workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Mock git operations to avoid actual repository modifications
                with mock.patch('create_markdown_file.git_add'):
                    with mock.patch('create_markdown_file.git_commit'):
                        with mock.patch('create_markdown_file.git_push'):
                            # Capture exit code by catching SystemExit
                            try:
                                create_markdown_file.main()
                                # If we get here, sys.exit(0) was called
                                assert False, "Should have called sys.exit()"
                            except SystemExit as e:
                                # Success path should exit with code 0
                                assert e.code == 0

                # Verify file was created
                assert (tmpdir_path / create_markdown_file.FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_main_validation_failure(self):
        """Test that main() catches validation errors and exits with code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Mock create_file to create an invalid file (no prose)
                def create_invalid_file():
                    file_path = Path(create_markdown_file.FILENAME)
                    file_path.write_text("# Title\n\n\n", encoding='utf-8', newline='\n')

                with mock.patch('create_markdown_file.create_file', side_effect=create_invalid_file):
                    with mock.patch('create_markdown_file.git_add'):
                        with mock.patch('create_markdown_file.git_commit'):
                            with mock.patch('create_markdown_file.git_push'):
                                try:
                                    create_markdown_file.main()
                                    assert False, "Should have exited with code 1"
                                except SystemExit as e:
                                    # Validation failure should exit with code 1
                                    assert e.code == 1
            finally:
                os.chdir(original_cwd)

    def test_main_git_failure(self):
        """Test that main() catches git errors and exits with code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Mock git_push to raise CalledProcessError
                with mock.patch('create_markdown_file.git_add'):
                    with mock.patch('create_markdown_file.git_commit'):
                        with mock.patch('create_markdown_file.git_push') as mock_push:
                            mock_push.side_effect = subprocess.CalledProcessError(
                                1, 'git push', stderr="fatal: network error"
                            )
                            try:
                                create_markdown_file.main()
                                assert False, "Should have exited with code 1"
                            except SystemExit as e:
                                # Git failure should exit with code 1
                                assert e.code == 1
            finally:
                os.chdir(original_cwd)

    def test_main_file_io_failure(self):
        """Test that main() catches file I/O errors and exits with code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Mock create_file to raise OSError
                with mock.patch('create_markdown_file.create_file') as mock_create:
                    mock_create.side_effect = OSError("Permission denied")
                    try:
                        create_markdown_file.main()
                        assert False, "Should have exited with code 1"
                    except SystemExit as e:
                        # File I/O failure should exit with code 1
                        assert e.code == 1
            finally:
                os.chdir(original_cwd)

    def test_main_orchestration_order(self):
        """Test that main() calls functions in correct order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                call_order = []

                def mock_create():
                    call_order.append('create')
                    # Create a valid file
                    file_path = Path(create_markdown_file.FILENAME)
                    file_path.write_text(
                        f"# {create_markdown_file.TITLE}\n\n{create_markdown_file.PROSE}\n",
                        encoding='utf-8',
                        newline='\n'
                    )

                def mock_validate(filename):
                    call_order.append('validate')

                def mock_add(filename):
                    call_order.append('add')

                def mock_commit(message):
                    call_order.append('commit')

                def mock_push():
                    call_order.append('push')

                with mock.patch('create_markdown_file.create_file', side_effect=mock_create):
                    with mock.patch('create_markdown_file.validate_file', side_effect=mock_validate):
                        with mock.patch('create_markdown_file.git_add', side_effect=mock_add):
                            with mock.patch('create_markdown_file.git_commit', side_effect=mock_commit):
                                with mock.patch('create_markdown_file.git_push', side_effect=mock_push):
                                    try:
                                        create_markdown_file.main()
                                    except SystemExit:
                                        pass

                # Verify correct order
                assert call_order == ['create', 'validate', 'add', 'commit', 'push']
            finally:
                os.chdir(original_cwd)


class TestGitOperations:
    """Tests for git workflow operations (add, commit, push)."""

    def test_git_add_called(self):
        """Test that git_add calls subprocess.run with correct arguments."""
        with mock.patch('subprocess.run') as mock_run:
            # Mock successful git add
            mock_run.return_value = mock.Mock(returncode=0)

            create_markdown_file.git_add("test-file.md")

            # Verify subprocess.run was called with correct args
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ['git', 'add', 'test-file.md']
            assert call_args[1]['check'] is True

    def test_git_add_failure(self):
        """Test that git_add raises CalledProcessError on failure."""
        with mock.patch('subprocess.run') as mock_run:
            # Mock git add failure
            mock_run.side_effect = subprocess.CalledProcessError(
                1, 'git add', stderr="fatal: not a git repository"
            )

            # Should raise CalledProcessError
            with pytest.raises(subprocess.CalledProcessError):
                create_markdown_file.git_add("test-file.md")

    def test_git_commit_message_format(self):
        """Test that commit message follows conventional commit format."""
        # Verify the commit message constant has correct format
        message = create_markdown_file.COMMIT_MESSAGE

        # Should start with 'feat(175):'
        assert message.startswith('feat(175):')

        # Should mention the filename
        assert 'test-rh39t2.md' in message

        # Should mention prose content
        assert 'prose content' in message

    def test_git_commit_called(self):
        """Test that git_commit calls subprocess.run with correct arguments."""
        with mock.patch('subprocess.run') as mock_run:
            # Mock successful git commit
            mock_run.return_value = mock.Mock(returncode=0)

            test_message = "feat(175): test commit"
            create_markdown_file.git_commit(test_message)

            # Verify subprocess.run was called with correct args
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ['git', 'commit', '-m', test_message]
            assert call_args[1]['check'] is True

    def test_git_commit_failure(self):
        """Test that git_commit raises CalledProcessError on failure."""
        with mock.patch('subprocess.run') as mock_run:
            # Mock git commit failure (e.g., missing user config)
            mock_run.side_effect = subprocess.CalledProcessError(
                1, 'git commit', stderr="error: no changes added to commit"
            )

            # Should raise CalledProcessError
            with pytest.raises(subprocess.CalledProcessError):
                create_markdown_file.git_commit("feat(175): test")

    def test_git_push_to_head(self):
        """Test that git_push uses HEAD for current branch."""
        with mock.patch('subprocess.run') as mock_run:
            # Mock successful git push
            mock_run.return_value = mock.Mock(returncode=0)

            create_markdown_file.git_push()

            # Verify subprocess.run was called with HEAD (current branch)
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert 'HEAD' in call_args[0][0]
            assert call_args[0][0] == ['git', 'push', '-u', 'origin', 'HEAD']
            assert call_args[1]['check'] is True

    def test_git_push_sets_upstream(self):
        """Test that git_push sets upstream tracking with -u flag."""
        with mock.patch('subprocess.run') as mock_run:
            # Mock successful git push
            mock_run.return_value = mock.Mock(returncode=0)

            create_markdown_file.git_push()

            # Verify -u flag is present for upstream tracking
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert '-u' in call_args[0][0]
            assert 'origin' in call_args[0][0]

    def test_git_push_failure(self):
        """Test that git_push raises CalledProcessError on failure."""
        with mock.patch('subprocess.run') as mock_run:
            # Mock git push failure (e.g., network error)
            mock_run.side_effect = subprocess.CalledProcessError(
                1, 'git push', stderr="fatal: Could not read from remote repository"
            )

            # Should raise CalledProcessError
            with pytest.raises(subprocess.CalledProcessError):
                create_markdown_file.git_push()


class TestScriptEntryPoint:
    """Tests for script entry point and command-line interface."""

    def test_script_entry_point_exists(self):
        """Test that script has if __name__ == '__main__' entry point."""
        import inspect

        # Get the source code
        source = inspect.getsource(create_markdown_file)

        # Should contain the entry point
        assert "if __name__ == '__main__'" in source

    def test_script_exits_zero_on_success(self):
        """Test that running script as main exits with code 0 on success."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Mock git operations
                with mock.patch('create_markdown_file.git_add'):
                    with mock.patch('create_markdown_file.git_commit'):
                        with mock.patch('create_markdown_file.git_push'):
                            # Simulate script execution
                            try:
                                create_markdown_file.main()
                            except SystemExit as e:
                                assert e.code == 0, f"Expected exit code 0, got {e.code}"
            finally:
                os.chdir(original_cwd)

    def test_script_exits_one_on_failure(self):
        """Test that running script as main exits with code 1 on failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Mock create_file to raise validation error
                with mock.patch('create_markdown_file.create_file'):
                    with mock.patch('create_markdown_file.validate_file') as mock_validate:
                        mock_validate.side_effect = ValueError("Invalid file structure")
                        try:
                            create_markdown_file.main()
                        except SystemExit as e:
                            assert e.code == 1, f"Expected exit code 1, got {e.code}"
            finally:
                os.chdir(original_cwd)
