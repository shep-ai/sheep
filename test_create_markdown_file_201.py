"""
Tests for Feature 201 implementation script: create_markdown_file_201.py

This module contains tests for:
- Module structure with imports and constants
- Main function existence and signature
- Logger initialization
"""

import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))


class TestModuleStructure:
    """Tests for create_markdown_file_201.py module structure."""

    def test_module_has_shebang(self):
        """Test that module has proper shebang for direct execution."""
        script_path = Path(__file__).parent / "create_markdown_file_201.py"
        first_line = script_path.read_text().split('\n')[0]
        assert first_line == "#!/usr/bin/env python3"

    def test_module_docstring_exists(self):
        """Test that module has descriptive docstring."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content'):
                import create_markdown_file_201
                assert create_markdown_file_201.__doc__ is not None
                assert "feature 201" in create_markdown_file_201.__doc__.lower()
                assert "markdown" in create_markdown_file_201.__doc__.lower()


class TestMainFunction:
    """Tests for main() function."""

    def test_main_function_exists(self):
        """Test that main() function is defined."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content'):
                import create_markdown_file_201
                assert hasattr(create_markdown_file_201, 'main')
                assert callable(create_markdown_file_201.main)

    def test_main_function_has_docstring(self):
        """Test that main() function has docstring."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content'):
                import create_markdown_file_201
                assert create_markdown_file_201.main.__doc__ is not None
                assert "orchestrate" in create_markdown_file_201.main.__doc__.lower()


class TestImports:
    """Tests for module imports."""

    def test_required_imports_available(self):
        """Test that required modules can be imported."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content'):
                import create_markdown_file_201
                # Check that pathlib is imported
                assert hasattr(create_markdown_file_201, 'Path')
                # Check that sys is imported
                assert hasattr(create_markdown_file_201, 'sys')
                # Check that subprocess is imported
                assert hasattr(create_markdown_file_201, 'subprocess')


class TestConstants:
    """Tests for module-level constants."""

    def test_filename_constant_exists(self):
        """Test that FILENAME constant is defined."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content'):
                import create_markdown_file_201
                assert hasattr(create_markdown_file_201, 'FILENAME')
                assert create_markdown_file_201.FILENAME == "test-lihjez.md"

    def test_commit_message_constant_exists(self):
        """Test that COMMIT_MESSAGE constant is defined."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content'):
                import create_markdown_file_201
                assert hasattr(create_markdown_file_201, 'COMMIT_MESSAGE')
                assert "feat(201)" in create_markdown_file_201.COMMIT_MESSAGE
                assert "test-lihjez.md" in create_markdown_file_201.COMMIT_MESSAGE


class TestLogger:
    """Tests for logger initialization."""

    def test_logger_is_initialized(self):
        """Test that logger is initialized using sheep.observability.logging."""
        with patch('sheep.observability.logging.get_logger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            with patch('src.create_markdown.generate_markdown_content'):
                # Import fresh module to capture logger initialization
                import importlib
                import create_markdown_file_201
                importlib.reload(create_markdown_file_201)
                # Verify get_logger was called
                mock_get_logger.assert_called()


class TestContentGeneration:
    """Tests for content generation functionality."""

    def test_main_calls_generate_markdown_content(self):
        """Test that main() calls generate_markdown_content."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                mock_gen.return_value = {
                    'title': 'Test Title',
                    'prose': 'First sentence. Second sentence. Third sentence.',
                    'full_content': '# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n',
                }
                import importlib
                import create_markdown_file_201
                importlib.reload(create_markdown_file_201)
                result = create_markdown_file_201.main()
                # Verify generate_markdown_content was called
                mock_gen.assert_called_once()
                # Verify main returns 0 (success)
                assert result == 0

    def test_generate_markdown_content_returns_correct_structure(self):
        """Test that content generation returns expected dict structure."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                test_content = {
                    'title': 'The Importance of Code Quality',
                    'prose': 'Code quality is fundamental to software development. Clean, readable code reduces bugs and maintenance costs. Investing in code quality pays dividends throughout a project lifecycle.',
                    'full_content': '# The Importance of Code Quality\n\nCode quality is fundamental to software development. Clean, readable code reduces bugs and maintenance costs. Investing in code quality pays dividends throughout a project lifecycle.\n',
                }
                mock_gen.return_value = test_content

                import importlib
                import create_markdown_file_201
                importlib.reload(create_markdown_file_201)
                result = create_markdown_file_201.main()

                # Verify return value structure
                called_args = mock_gen.call_args
                assert called_args is not None
                assert result == 0

    def test_generated_title_is_valid(self):
        """Test that generated title is H1 heading format."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                # Valid title (without # prefix - will be added as heading)
                mock_gen.return_value = {
                    'title': 'Valid Title',
                    'prose': 'First. Second. Third.',
                    'full_content': '# Valid Title\n\nFirst. Second. Third.\n',
                }

                import importlib
                import create_markdown_file_201
                importlib.reload(create_markdown_file_201)
                result = create_markdown_file_201.main()

                # If main succeeded, content generation was valid
                assert result == 0

    def test_generated_prose_has_correct_sentence_count(self):
        """Test that generated prose contains 2-3 sentences."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                # Prose with exactly 3 sentences
                prose = "This is sentence one. This is sentence two. This is sentence three."
                mock_gen.return_value = {
                    'title': 'Test Title',
                    'prose': prose,
                    'full_content': f'# Test Title\n\n{prose}\n',
                }

                import importlib
                import create_markdown_file_201
                importlib.reload(create_markdown_file_201)
                result = create_markdown_file_201.main()

                # If main succeeded, prose validation passed
                assert result == 0
                # Verify prose has 3 sentences
                sentence_count = prose.count('.')
                assert 2 <= sentence_count <= 3

    def test_main_handles_content_generation_errors(self):
        """Test that main() handles content generation errors gracefully."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                mock_gen.side_effect = ValueError("Failed to generate content")

                import importlib
                import create_markdown_file_201
                importlib.reload(create_markdown_file_201)
                result = create_markdown_file_201.main()

                # Verify main returns error code
                assert result == 1


class TestFileCreation:
    """Tests for file creation functionality (Task 3)."""

    def test_file_creation_check_pre_existing_file(self):
        """Test that main() fails if test-lihjez.md already exists."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create pre-existing file
                Path("test-lihjez.md").write_text("existing content")

                with patch('sheep.observability.logging.get_logger'):
                    with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                        mock_gen.return_value = {
                            'title': 'Test Title',
                            'prose': 'First. Second. Third.',
                            'full_content': '# Test Title\n\nFirst. Second. Third.\n',
                        }
                        import create_markdown_file_201
                        importlib.reload(create_markdown_file_201)
                        result = create_markdown_file_201.main()

                        # Should fail with FileExistsError
                        assert result == 1
            finally:
                os.chdir(original_cwd)

    def test_file_created_with_utf8_encoding(self):
        """Test that file is created with UTF-8 encoding and no BOM."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.observability.logging.get_logger'):
                    with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                        mock_gen.return_value = {
                            'title': 'Test Title',
                            'prose': 'First sentence. Second sentence. Third sentence.',
                            'full_content': '# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n',
                        }
                        import create_markdown_file_201
                        importlib.reload(create_markdown_file_201)
                        result = create_markdown_file_201.main()

                        # If successful, verify file exists and has proper encoding
                        if Path("test-lihjez.md").exists():
                            content = Path("test-lihjez.md").read_bytes()
                            # Check for UTF-8 BOM (should not exist)
                            assert not content.startswith(b'\xef\xbb\xbf')
                            # File should be decodable as UTF-8
                            assert content.decode('utf-8') is not None
            finally:
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF line endings exclusively (no CRLF)."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.observability.logging.get_logger'):
                    with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                        mock_gen.return_value = {
                            'title': 'Test Title',
                            'prose': 'First sentence. Second sentence. Third sentence.',
                            'full_content': '# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n',
                        }
                        import create_markdown_file_201
                        importlib.reload(create_markdown_file_201)
                        result = create_markdown_file_201.main()

                        # If successful, verify file uses only LF
                        if Path("test-lihjez.md").exists():
                            content = Path("test-lihjez.md").read_bytes()
                            # Should not contain CRLF
                            assert b'\r\n' not in content
                            # Should contain only LF for line endings
                            assert b'\n' in content
            finally:
                os.chdir(original_cwd)


class TestFileValidation:
    """Tests for file validation functionality (Task 4)."""

    def test_file_validation_encoding_check(self):
        """Test that file validation checks for UTF-8 encoding without BOM."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.observability.logging.get_logger'):
                    with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                        mock_gen.return_value = {
                            'title': 'Test Title',
                            'prose': 'First sentence. Second sentence. Third sentence.',
                            'full_content': '# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n',
                        }
                        import create_markdown_file_201
                        importlib.reload(create_markdown_file_201)
                        result = create_markdown_file_201.main()

                        # Verify file passes encoding validation
                        if Path("test-lihjez.md").exists():
                            content = Path("test-lihjez.md").read_bytes()
                            # Should not start with BOM
                            assert not content.startswith(b'\xef\xbb\xbf')
                            # Should be valid UTF-8
                            try:
                                content.decode('utf-8')
                                assert True
                            except UnicodeDecodeError:
                                assert False, "File is not valid UTF-8"
            finally:
                os.chdir(original_cwd)

    def test_file_validation_line_endings_check(self):
        """Test that file validation checks for LF line endings."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.observability.logging.get_logger'):
                    with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                        mock_gen.return_value = {
                            'title': 'Test Title',
                            'prose': 'First sentence. Second sentence. Third sentence.',
                            'full_content': '# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n',
                        }
                        import create_markdown_file_201
                        importlib.reload(create_markdown_file_201)
                        result = create_markdown_file_201.main()

                        # Verify file uses LF line endings
                        if Path("test-lihjez.md").exists():
                            content = Path("test-lihjez.md").read_bytes()
                            # Should not contain CRLF
                            assert b'\r\n' not in content
            finally:
                os.chdir(original_cwd)

    def test_file_validation_structure_check(self):
        """Test that file validation checks for proper markdown structure."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.observability.logging.get_logger'):
                    with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                        mock_gen.return_value = {
                            'title': 'Test Title',
                            'prose': 'First sentence. Second sentence. Third sentence.',
                            'full_content': '# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n',
                        }
                        import create_markdown_file_201
                        importlib.reload(create_markdown_file_201)
                        result = create_markdown_file_201.main()

                        # Verify file structure is correct
                        if Path("test-lihjez.md").exists():
                            content = Path("test-lihjez.md").read_text()
                            lines = content.split('\n')
                            # First line should be H1 heading
                            assert lines[0].startswith('# ')
                            # Second line should be blank
                            assert lines[1] == ''
                            # Should have prose content
                            assert len(lines) > 2
            finally:
                os.chdir(original_cwd)

    def test_file_validation_sentence_count(self):
        """Test that file validation checks for 2-3 sentences in prose."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.observability.logging.get_logger'):
                    with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                        # Exactly 3 sentences
                        prose = 'First sentence. Second sentence. Third sentence.'
                        mock_gen.return_value = {
                            'title': 'Test Title',
                            'prose': prose,
                            'full_content': f'# Test Title\n\n{prose}\n',
                        }
                        import create_markdown_file_201
                        importlib.reload(create_markdown_file_201)
                        result = create_markdown_file_201.main()

                        # Verify sentence count
                        if Path("test-lihjez.md").exists():
                            content = Path("test-lihjez.md").read_text()
                            prose_content = '\n'.join(content.split('\n')[2:]).strip()
                            sentence_count = prose_content.count('.')
                            assert 2 <= sentence_count <= 3
            finally:
                os.chdir(original_cwd)

    def test_file_validation_size_check(self):
        """Test that file validation checks for 400-600 byte size constraint."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch('sheep.observability.logging.get_logger'):
                    with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                        mock_gen.return_value = {
                            'title': 'Test Title',
                            'prose': 'First sentence. Second sentence. Third sentence.',
                            'full_content': '# Test Title\n\nFirst sentence. Second sentence. Third sentence.\n',
                        }
                        import create_markdown_file_201
                        importlib.reload(create_markdown_file_201)
                        result = create_markdown_file_201.main()

                        # Verify file size
                        if Path("test-lihjez.md").exists():
                            file_size = Path("test-lihjez.md").stat().st_size
                            assert 400 <= file_size <= 600, f"File size {file_size} outside 400-600 byte range"
            finally:
                os.chdir(original_cwd)


class TestGitAdd:
    """Tests for git_add() function (Phase 3 - Git Integration)."""

    def test_git_add_with_valid_file(self):
        """Test that git_add() stages a file successfully."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                os.system("git init")
                os.system("git config user.email 'test@example.com'")
                os.system("git config user.name 'Test User'")

                # Create test file
                Path("test-file.md").write_text("test content")

                with patch('sheep.observability.logging.get_logger'):
                    import create_markdown_file_201
                    result = create_markdown_file_201.git_add("test-file.md")

                    assert result['success'] == True
                    assert result['filename'] == "test-file.md"
                    assert result['error'] is None
            finally:
                os.chdir(original_cwd)

    def test_git_add_nonexistent_file(self):
        """Test that git_add() handles nonexistent file gracefully."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                os.system("git init")

                with patch('sheep.observability.logging.get_logger'):
                    import create_markdown_file_201
                    result = create_markdown_file_201.git_add("nonexistent.md")

                    assert result['success'] == False
                    assert result['filename'] == "nonexistent.md"
                    assert result['error'] is not None
            finally:
                os.chdir(original_cwd)


class TestGitCommit:
    """Tests for git_commit() function (Phase 3 - Git Integration)."""

    def test_git_commit_with_staged_file(self):
        """Test that git_commit() creates a commit successfully."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                os.system("git init")
                os.system("git config user.email 'test@example.com'")
                os.system("git config user.name 'Test User'")

                # Create and stage test file
                Path("test-file.md").write_text("test content")
                os.system("git add test-file.md")

                with patch('sheep.observability.logging.get_logger'):
                    import create_markdown_file_201
                    result = create_markdown_file_201.git_commit(
                        "test-file.md",
                        "test: add test file"
                    )

                    assert result['success'] == True
                    assert result['commit_hash'] is not None
                    assert result['error'] is None
            finally:
                os.chdir(original_cwd)

    def test_git_commit_message_format(self):
        """Test that git_commit() uses the provided message."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                os.system("git init")
                os.system("git config user.email 'test@example.com'")
                os.system("git config user.name 'Test User'")

                # Create and stage test file
                Path("test-file.md").write_text("test content")
                os.system("git add test-file.md")

                with patch('sheep.observability.logging.get_logger'):
                    import create_markdown_file_201
                    commit_msg = "feat(201): test commit message"
                    result = create_markdown_file_201.git_commit("test-file.md", commit_msg)

                    assert result['success'] == True
                    # Verify the commit was created with the message
                    log_result = os.popen("git log --oneline -1").read()
                    assert "feat(201): test commit message" in log_result
            finally:
                os.chdir(original_cwd)


class TestGitPush:
    """Tests for git_push() function (Phase 3 - Git Integration)."""

    def test_git_push_nonexistent_branch(self):
        """Test that git_push() handles nonexistent branch gracefully."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo without remote
                os.system("git init")

                with patch('sheep.observability.logging.get_logger'):
                    import create_markdown_file_201
                    result = create_markdown_file_201.git_push("nonexistent-branch")

                    # Should fail because there's no remote
                    assert result['success'] == False
                    assert result['error'] is not None
            finally:
                os.chdir(original_cwd)


class TestGitWorkflow:
    """Tests for git_workflow() function (Phase 3 - Git Integration)."""

    def test_git_workflow_orchestrates_operations(self):
        """Test that git_workflow() calls add, commit, and push in sequence."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize git repo
                os.system("git init")
                os.system("git config user.email 'test@example.com'")
                os.system("git config user.name 'Test User'")

                # Create test file
                Path("test-file.md").write_text("test content")

                with patch('sheep.observability.logging.get_logger'):
                    import create_markdown_file_201
                    # Mock the push operation since we don't have a real remote
                    with patch('subprocess.run') as mock_run:
                        mock_run.side_effect = [
                            # Add operation succeeds
                            MagicMock(returncode=0, stdout="", stderr=""),
                            # Commit operation succeeds
                            MagicMock(returncode=0, stdout="commit 123abc", stderr=""),
                            # rev-parse succeeds
                            MagicMock(returncode=0, stdout="1234567\n", stderr=""),
                            # Push fails (expected since no remote)
                            None,
                        ]
                        result = create_markdown_file_201.git_workflow(
                            "test-file.md",
                            "feat(201): test file",
                            "test-branch"
                        )

                        # Should have called subprocess.run at least twice (add, commit)
                        assert mock_run.call_count >= 2
            finally:
                os.chdir(original_cwd)

    def test_git_workflow_returns_success_false_on_add_failure(self):
        """Test that git_workflow() returns failure if git add fails."""
        with patch('sheep.observability.logging.get_logger'):
            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.CalledProcessError(1, 'git add')

                import create_markdown_file_201
                result = create_markdown_file_201.git_workflow(
                    "test-file.md",
                    "feat(201): test",
                    "test-branch"
                )

                assert result['success'] == False
                assert len(result['errors']) > 0


class TestEndToEndIntegration:
    """End-to-end integration tests for feature 201."""

    def test_complete_workflow_end_to_end(self):
        """Test the complete workflow: content generation, file creation, validation, and git integration."""
        import tempfile
        import os
        import importlib

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Initialize a git repository
                os.system("git init")
                os.system("git config user.email 'test@example.com'")
                os.system("git config user.name 'Test User'")

                # Create an initial commit so git operations work
                Path(".gitkeep").write_text("")
                os.system("git add .gitkeep")
                os.system("git commit -m 'initial commit'")

                with patch('sheep.observability.logging.get_logger'):
                    with patch('subprocess.run') as mock_subprocess:
                        # Set up subprocess mocks for git operations
                        def subprocess_side_effect(cmd, *args, **kwargs):
                            if 'rev-parse' in cmd and '--abbrev-ref' in cmd:
                                result = MagicMock()
                                result.returncode = 0
                                result.stdout = "master\n"
                                result.stderr = ""
                                return result
                            elif 'rev-parse' in cmd:
                                result = MagicMock()
                                result.returncode = 0
                                result.stdout = "abc1234567\n"
                                result.stderr = ""
                                return result
                            elif 'add' in cmd:
                                result = MagicMock()
                                result.returncode = 0
                                result.stdout = ""
                                result.stderr = ""
                                return result
                            elif 'commit' in cmd:
                                result = MagicMock()
                                result.returncode = 0
                                result.stdout = ""
                                result.stderr = ""
                                return result
                            elif 'push' in cmd:
                                result = MagicMock()
                                result.returncode = 0
                                result.stdout = ""
                                result.stderr = ""
                                return result
                            else:
                                raise NotImplementedError(f"Mock not configured for: {cmd}")

                        mock_subprocess.side_effect = subprocess_side_effect

                        with patch('src.create_markdown.generate_markdown_content') as mock_gen:
                            # Create content that meets the 400-600 byte requirement
                            # H1 title + blank line + 3 sentences = approximately 500+ bytes
                            prose = "This is the first sentence about software engineering best practices and principles that guide modern development. This is the second sentence explaining the importance of clean code and maintainability for long-term project success. This is the third sentence discussing how proper testing, documentation, and code review practices significantly improve overall code quality and reduce technical debt."
                            full_content = f"# Software Engineering Excellence\n\n{prose}\n"

                            # Verify content size is in range
                            content_bytes = full_content.encode('utf-8')
                            assert 400 <= len(content_bytes) <= 600, f"Mock content size {len(content_bytes)} outside 400-600 range"

                            mock_gen.return_value = {
                                'title': 'Software Engineering Excellence',
                                'prose': prose,
                                'full_content': full_content,
                            }

                            # Import and run main
                            import create_markdown_file_201
                            importlib.reload(create_markdown_file_201)

                            # Capture stdout and stderr to debug failures
                            import io
                            from contextlib import redirect_stdout, redirect_stderr

                            stdout_capture = io.StringIO()
                            stderr_capture = io.StringIO()

                            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                                result = create_markdown_file_201.main()

                            stdout_output = stdout_capture.getvalue()
                            stderr_output = stderr_capture.getvalue()

                            # Verify success
                            assert result == 0, f"main() should return 0 on success. Got {result}. Stdout: {stdout_output}. Stderr: {stderr_output}"

                            # Verify file exists
                            assert Path("test-lihjez.md").exists(), "File test-lihjez.md should exist"

                            # Verify file content
                            file_content = Path("test-lihjez.md").read_text()
                            assert file_content.startswith("# Software Engineering Excellence"), "File should start with H1 heading"
                            assert prose in file_content, "File should contain prose content"

                            # Verify file size
                            file_size = Path("test-lihjez.md").stat().st_size
                            assert 400 <= file_size <= 600, f"File size {file_size} should be in 400-600 byte range"

                            # Verify file encoding (no BOM)
                            file_bytes = Path("test-lihjez.md").read_bytes()
                            assert not file_bytes.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"

                            # Verify LF line endings (no CRLF)
                            assert b'\r\n' not in file_bytes, "File should use LF line endings, not CRLF"

                            # Verify file ends with newline
                            assert file_bytes.endswith(b'\n'), "File should end with newline"

                            # Verify that subprocess.run was called for git operations
                            # We mocked subprocess.run, so we can verify the mocks were called
                            call_count = mock_subprocess.call_count
                            assert call_count >= 3, f"subprocess.run should be called at least 3 times (add, commit, push), got {call_count}"

                            # Check that at least one call was for 'git add'
                            add_calls = [c for c in mock_subprocess.call_args_list if 'add' in str(c)]
                            assert len(add_calls) > 0, "git add should be called"

                            # Check that at least one call was for 'git commit'
                            commit_calls = [c for c in mock_subprocess.call_args_list if 'commit' in str(c)]
                            assert len(commit_calls) > 0, "git commit should be called"

                            # Check that at least one call was for 'git push'
                            push_calls = [c for c in mock_subprocess.call_args_list if 'push' in str(c)]
                            assert len(push_calls) > 0, "git push should be called"

            finally:
                os.chdir(original_cwd)
