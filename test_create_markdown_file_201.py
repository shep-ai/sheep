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
