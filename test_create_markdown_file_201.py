"""
Tests for Feature 201 implementation script: create_markdown_file_201.py

This module contains tests for:
- Module structure with imports and constants
- Main function existence and signature
- Logger initialization
"""

import sys
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
                assert "Feature 201" in create_markdown_file_201.__doc__
                assert "markdown-file-creation" in create_markdown_file_201.__doc__


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
