"""Tests for feature 208 implementation - File Creation & Validation Framework.

Tests verify that all functions work correctly:
1. create_markdown_file() - creates file with proper encoding
2. Validation functions - verify markdown format, sentence count, encoding, line endings, file size
3. validate_markdown_file() - orchestrates all validation checks
4. Git operations - stages, commits, and pushes file
5. main() - orchestrates complete workflow
"""

import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess


def setup_module():
    """Set up test environment by adding src to path."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


class TestCreateMarkdownFile:
    """Tests for create_markdown_file() function."""

    def test_create_markdown_file_creates_file_at_correct_path(self):
        """Test create_markdown_file creates file with correct filename."""
        from sheep.features.feature_208_markdown_file_creation import (
            create_markdown_file,
            FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock generate_content to return test data
                with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                    mock_gen.return_value = ("Test Title", "First sentence. Second sentence.")

                    # Create file
                    file_path = create_markdown_file()

                    # Verify file exists at expected path
                    assert file_path.exists()
                    assert file_path.name == FILENAME

            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_writes_correct_markdown_format(self):
        """Test create_markdown_file writes markdown with H1, blank line, prose."""
        from sheep.features.feature_208_markdown_file_creation import (
            create_markdown_file,
            FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock generate_content
                with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                    test_title = "Test Title"
                    test_prose = "First sentence. Second sentence."
                    mock_gen.return_value = (test_title, test_prose)

                    # Create file
                    create_markdown_file()

                    # Read and verify content
                    content = Path(FILENAME).read_text(encoding="utf-8")
                    lines = content.split("\n")

                    # Verify H1 title on first line
                    assert lines[0] == f"# {test_title}"

                    # Verify blank line on second line
                    assert lines[1] == ""

                    # Verify prose content after blank line
                    assert test_prose in content

            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_uses_utf8_encoding(self):
        """Test create_markdown_file writes with UTF-8 encoding."""
        from sheep.features.feature_208_markdown_file_creation import (
            create_markdown_file,
            FILENAME,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock generate_content
                with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                    mock_gen.return_value = ("Title", "Sentence. Sentence.")

                    # Create file
                    create_markdown_file()

                    # Verify file has UTF-8 encoding (no BOM)
                    binary_content = Path(FILENAME).read_bytes()
                    assert not binary_content.startswith(b"\xef\xbb\xbf")

            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_on_missing_file(self):
        """Test create_markdown_file raises OSError if file is not created."""
        from sheep.features.feature_208_markdown_file_creation import create_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock generate_content and Path.write_text to simulate failure
                with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                    mock_gen.return_value = ("Title", "Sentence. Sentence.")

                    with patch("sheep.features.feature_208_markdown_file_creation.Path.write_text") as mock_write:
                        # Simulate write failure (file not created)
                        mock_write.return_value = None

                        try:
                            create_markdown_file()
                            assert False, "Should have raised OSError"
                        except OSError as e:
                            assert "not created" in str(e)

            finally:
                os.chdir(original_cwd)


class TestValidationFunctions:
    """Tests for individual validation functions."""

    def test_verify_file_exists_raises_on_missing_file(self):
        """Test verify_file_exists raises FileNotFoundError if file missing."""
        from sheep.features.feature_208_markdown_file_creation import verify_file_exists

        try:
            verify_file_exists("nonexistent.md")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass  # Expected

    def test_validate_markdown_format_passes_valid_format(self):
        """Test validate_markdown_format accepts valid H1 format."""
        from sheep.features.feature_208_markdown_file_creation import validate_markdown_format

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create valid markdown
                Path("test.md").write_text("# Title\n\nContent here.", encoding="utf-8")

                # Should not raise
                validate_markdown_format("test.md")

            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_raises_on_invalid_heading(self):
        """Test validate_markdown_format raises on invalid H1 heading."""
        from sheep.features.feature_208_markdown_file_creation import validate_markdown_format

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create invalid markdown (no H1 heading)
                Path("test.md").write_text("Regular heading\n\nContent here.", encoding="utf-8")

                try:
                    validate_markdown_format("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "H1 heading" in str(e)

            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_raises_on_missing_blank_line(self):
        """Test validate_markdown_format raises if blank line is missing."""
        from sheep.features.feature_208_markdown_file_creation import validate_markdown_format

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create markdown without blank line after heading
                Path("test.md").write_text("# Title\nContent directly here.", encoding="utf-8")

                try:
                    validate_markdown_format("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "blank line" in str(e).lower()

            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_passes_valid_count(self):
        """Test validate_sentence_count accepts 2-3 sentences."""
        from sheep.features.feature_208_markdown_file_creation import validate_sentence_count

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create with 2 sentences
                Path("test.md").write_text("# Title\n\nFirst sentence. Second sentence.", encoding="utf-8")

                # Should not raise
                validate_sentence_count("test.md")

                # Create with 3 sentences
                Path("test.md").write_text("# Title\n\nFirst. Second. Third.", encoding="utf-8")

                # Should not raise
                validate_sentence_count("test.md")

            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_raises_on_invalid_count(self):
        """Test validate_sentence_count raises on wrong sentence count."""
        from sheep.features.feature_208_markdown_file_creation import validate_sentence_count

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create with 1 sentence
                Path("test.md").write_text("# Title\n\nOnly one sentence.", encoding="utf-8")

                try:
                    validate_sentence_count("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "2 or 3 sentences" in str(e)

            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_passes_valid_utf8(self):
        """Test validate_encoding accepts valid UTF-8 without BOM."""
        from sheep.features.feature_208_markdown_file_creation import validate_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create with UTF-8 (no BOM)
                Path("test.md").write_text("# Title\n\nContent.", encoding="utf-8")

                # Should not raise
                validate_encoding("test.md")

            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_raises_on_bom(self):
        """Test validate_encoding raises if UTF-8 BOM is present."""
        from sheep.features.feature_208_markdown_file_creation import validate_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create with UTF-8 BOM
                Path("test.md").write_bytes(b"\xef\xbb\xbf# Title\n\nContent.")

                try:
                    validate_encoding("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "BOM" in str(e)

            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_passes_lf_only(self):
        """Test validate_line_endings accepts Unix LF line endings."""
        from sheep.features.feature_208_markdown_file_creation import validate_line_endings

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create with LF only (Unix)
                Path("test.md").write_bytes(b"# Title\n\nContent.\n")

                # Should not raise
                validate_line_endings("test.md")

            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_raises_on_crlf(self):
        """Test validate_line_endings raises on Windows CRLF."""
        from sheep.features.feature_208_markdown_file_creation import validate_line_endings

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create with CRLF (Windows)
                Path("test.md").write_bytes(b"# Title\r\n\r\nContent.\r\n")

                try:
                    validate_line_endings("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "LF" in str(e)

            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_passes_valid_range(self):
        """Test validate_file_size accepts files within range."""
        from sheep.features.feature_208_markdown_file_creation import validate_file_size

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file within default range (250-600 bytes)
                content = "# Cloud Computing Fundamentals\n\nCloud computing has revolutionized how organizations deploy and manage their infrastructure by providing on-demand access to computing resources over the internet. This technology enables businesses to scale their operations dynamically while reducing capital expenditures on physical servers.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should not raise
                validate_file_size("test.md")

            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_raises_on_small_file(self):
        """Test validate_file_size raises if file is too small."""
        from sheep.features.feature_208_markdown_file_creation import validate_file_size

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create very small file
                Path("test.md").write_text("# T\n\nS.", encoding="utf-8")

                try:
                    validate_file_size("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "too small" in str(e)

            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_raises_on_large_file(self):
        """Test validate_file_size raises if file is too large."""
        from sheep.features.feature_208_markdown_file_creation import validate_file_size

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create very large file (exceed 600 byte default max)
                large_content = "# Title\n\n" + ("A" * 700)
                Path("test.md").write_text(large_content, encoding="utf-8")

                try:
                    validate_file_size("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "too large" in str(e)

            finally:
                os.chdir(original_cwd)


class TestValidateMarkdownFileOrchestrator:
    """Tests for validate_markdown_file() orchestrator."""

    def test_validate_markdown_file_passes_all_checks(self):
        """Test validate_markdown_file passes on valid file."""
        from sheep.features.feature_208_markdown_file_creation import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create valid markdown file with adequate size
                content = "# Cloud Computing Fundamentals\n\nCloud computing has revolutionized how organizations deploy and manage their infrastructure by providing on-demand access to computing resources over the internet. This technology enables businesses to scale their operations dynamically while reducing capital expenditures on physical servers.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should not raise
                validate_markdown_file("test.md")

            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_on_invalid_file(self):
        """Test validate_markdown_file raises on invalid file."""
        from sheep.features.feature_208_markdown_file_creation import validate_markdown_file

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create invalid file (no H1)
                Path("test.md").write_text("No heading here.", encoding="utf-8")

                try:
                    validate_markdown_file("test.md")
                    assert False, "Should have raised ValueError"
                except ValueError:
                    pass  # Expected

            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_fast_on_first_error(self):
        """Test validate_markdown_file stops at first error (fail-fast)."""
        from sheep.features.feature_208_markdown_file_creation import (
            validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Create file that fails at first check (doesn't exist)
                try:
                    validate_markdown_file("nonexistent.md")
                    assert False, "Should have raised FileNotFoundError"
                except FileNotFoundError:
                    pass  # Expected - stopped at first check

            finally:
                os.chdir(original_cwd)


class TestGitOperations:
    """Tests for git operations."""

    def test_git_add_file_calls_subprocess_with_correct_args(self):
        """Test git_add_file executes git add with correct arguments."""
        from sheep.features.feature_208_markdown_file_creation import git_add_file

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_add_file("test-mujic0.md")

            # Verify subprocess.run was called with correct git add command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "add", "test-mujic0.md"]
            assert call_args[1]["check"] is True
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True

    def test_git_commit_calls_subprocess_with_correct_args(self):
        """Test git_commit executes git commit with correct arguments."""
        from sheep.features.feature_208_markdown_file_creation import git_commit

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_commit("feat(208): Create markdown file test-mujic0.md")

            # Verify subprocess.run was called with correct git commit command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0][0:2] == ["git", "commit"]
            assert call_args[0][0][2] == "-m"
            assert call_args[1]["check"] is True

    def test_git_push_calls_subprocess_with_correct_args(self):
        """Test git_push executes git push with correct arguments."""
        from sheep.features.feature_208_markdown_file_creation import git_push

        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            git_push("feat/markdown-file-creation-9f7556")

            # Verify subprocess.run was called with correct git push command
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "push", "-u", "origin", "HEAD"]
            assert call_args[1]["check"] is True

    def test_git_operations_raise_on_subprocess_error(self):
        """Test git operations raise CalledProcessError on failure."""
        from sheep.features.feature_208_markdown_file_creation import (
            git_add_file,
            git_commit,
            git_push,
        )

        # Test git_add_file
        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git add")
            try:
                git_add_file("test.md")
                assert False, "Should have raised CalledProcessError"
            except subprocess.CalledProcessError:
                pass

        # Test git_commit
        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git commit")
            try:
                git_commit("feat: test")
                assert False, "Should have raised CalledProcessError"
            except subprocess.CalledProcessError:
                pass

        # Test git_push
        with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git push")
            try:
                git_push("branch")
                assert False, "Should have raised CalledProcessError"
            except subprocess.CalledProcessError:
                pass


class TestMainOrchestration:
    """Tests for main() orchestration function."""

    def test_main_returns_zero_on_success(self):
        """Test main returns 0 on successful execution."""
        from sheep.features.feature_208_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock git operations
                with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock()

                    # Mock generate_content with long enough content (must be >250 bytes total)
                    with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                        mock_gen.return_value = (
                            "Cloud Computing Fundamentals",
                            "Cloud computing has revolutionized how organizations deploy and manage their infrastructure by providing on-demand access to computing resources over the internet. This technology enables businesses to scale their operations dynamically while reducing capital expenditures on physical servers."
                        )

                        # Execute main
                        exit_code = main()

                        # Verify success
                        assert exit_code == 0

            finally:
                os.chdir(original_cwd)

    def test_main_creates_and_validates_file(self):
        """Test main creates file and validates it successfully."""
        from sheep.features.feature_208_markdown_file_creation import (
            main,
            FILENAME,
            validate_markdown_file,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock only git operations
                with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock()

                    # Mock generate_content with long enough content
                    with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                        mock_gen.return_value = (
                            "Cloud Computing Fundamentals",
                            "Cloud computing has revolutionized how organizations deploy and manage their infrastructure by providing on-demand access to computing resources over the internet. This technology enables businesses to scale their operations dynamically while reducing capital expenditures on physical servers."
                        )

                        # Execute main
                        exit_code = main()

                        # Verify success
                        assert exit_code == 0

                        # Verify file exists
                        assert Path(FILENAME).exists()

                        # Verify file passes validation
                        validate_markdown_file(FILENAME)

            finally:
                os.chdir(original_cwd)

    def test_main_returns_one_on_validation_failure(self):
        """Test main returns 1 if validation fails."""
        from sheep.features.feature_208_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock create_markdown_file to create invalid file
                with patch("sheep.features.feature_208_markdown_file_creation.create_markdown_file") as mock_create:
                    # Create invalid file
                    def create_invalid():
                        Path("test-mujic0.md").write_text("Invalid content")
                        return Path("test-mujic0.md")

                    mock_create.side_effect = create_invalid

                    # Execute main
                    exit_code = main()

                    # Verify failure
                    assert exit_code == 1

            finally:
                os.chdir(original_cwd)

    def test_main_returns_one_on_git_failure(self):
        """Test main returns 1 if git operations fail."""
        from sheep.features.feature_208_markdown_file_creation import main

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Mock generate_content
                with patch("sheep.features.feature_208_markdown_file_creation.generate_content") as mock_gen:
                    mock_gen.return_value = ("Title", "First. Second.")

                    # Mock subprocess.run to fail on git operations
                    with patch("sheep.features.feature_208_markdown_file_creation.subprocess.run") as mock_run:
                        mock_run.side_effect = subprocess.CalledProcessError(1, "git")

                        # Execute main
                        exit_code = main()

                        # Verify failure
                        assert exit_code == 1

            finally:
                os.chdir(original_cwd)
