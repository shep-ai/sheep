"""Tests for feature 245 module structure and imports."""

import sys
from pathlib import Path


class TestFeature245ModuleStructure:
    """Tests for task-1: Create feature module skeleton with proper structure."""

    def test_module_file_exists(self):
        """Test that src/sheep/feature_245_markdown_file_creation.py exists."""
        module_path = Path("src/sheep/feature_245_markdown_file_creation.py")
        assert module_path.exists(), f"Module file does not exist: {module_path}"

    def test_module_is_importable(self):
        """Test that the module can be imported without errors."""
        # Add src directory to path for import
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            # Import the module
            from sheep.feature_245_markdown_file_creation import (
                FEATURE_NUMBER,
                FILENAME,
            )

            assert FEATURE_NUMBER == 245
            assert FILENAME == "test-nxclc0.md"
        finally:
            # Clean up sys.path
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_feature_number_constant(self):
        """Test that FEATURE_NUMBER constant is 245."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import FEATURE_NUMBER

            assert FEATURE_NUMBER == 245
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_filename_constant(self):
        """Test that FILENAME constant is 'test-nxclc0.md'."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import FILENAME

            assert FILENAME == "test-nxclc0.md"
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_module_has_required_imports(self):
        """Test that module imports required functions from content_generators."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            # Try to import the module - this will fail if imports are missing
            import sheep.feature_245_markdown_file_creation as module

            # Check that required functions are available
            assert hasattr(module, "generate_markdown_content")
            assert hasattr(module, "write_markdown_file")
            assert hasattr(module, "commit_markdown_file")
            assert hasattr(module, "push_markdown_file")
            assert hasattr(module, "validate_markdown_file")
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_module_has_logger(self):
        """Test that module has logger initialized via get_logger()."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            import sheep.feature_245_markdown_file_creation as module

            assert hasattr(module, "_logger")
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_module_has_docstring(self):
        """Test that module has a docstring explaining the feature."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            import sheep.feature_245_markdown_file_creation as module

            assert module.__doc__ is not None
            assert "Feature 245" in module.__doc__
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))


class TestFeature245TaskFunctionSignatures:
    """Tests for task function definitions."""

    def test_task_2_function_exists(self):
        """Test that task_2_generate_markdown_content function exists."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import (
                task_2_generate_markdown_content,
            )

            assert callable(task_2_generate_markdown_content)
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_task_3_function_exists(self):
        """Test that task_3_write_markdown_file_to_disk function exists."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import (
                task_3_write_markdown_file_to_disk,
            )

            assert callable(task_3_write_markdown_file_to_disk)
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_task_4_function_exists(self):
        """Test that task_4_commit_markdown_file function exists."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import (
                task_4_commit_markdown_file,
            )

            assert callable(task_4_commit_markdown_file)
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_task_5_function_exists(self):
        """Test that task_5_push_markdown_file function exists."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import (
                task_5_push_markdown_file,
            )

            assert callable(task_5_push_markdown_file)
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_function_exists(self):
        """Test that main() function exists and is callable."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            assert callable(main)
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))
