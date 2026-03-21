"""Phase 1 tests for feature 145: Module creation and foundation."""

import pytest


class TestFeature145Phase1ModuleCreation:
    """Tests for feature 145 phase 1: module creation with metadata and imports."""

    def test_module_can_be_imported(self):
        """Test that the feature module can be imported without errors."""
        from sheep.features.feature_145_markdown_file_creation import (
            FEATURE_NUMBER,
            MARKDOWN_FILENAME,
            COMMIT_MESSAGE,
        )

        # Just verify the constants exist
        assert FEATURE_NUMBER is not None
        assert MARKDOWN_FILENAME is not None
        assert COMMIT_MESSAGE is not None

    def test_feature_number_constant(self):
        """Test that FEATURE_NUMBER is set to 145."""
        from sheep.features.feature_145_markdown_file_creation import (
            FEATURE_NUMBER,
        )

        assert FEATURE_NUMBER == 145

    def test_markdown_filename_constant(self):
        """Test that MARKDOWN_FILENAME is set to 'test-rtj7cz.md'."""
        from sheep.features.feature_145_markdown_file_creation import (
            MARKDOWN_FILENAME,
        )

        assert MARKDOWN_FILENAME == "test-rtj7cz.md"

    def test_commit_message_contains_feature_number(self):
        """Test that COMMIT_MESSAGE contains 'feat(145)'."""
        from sheep.features.feature_145_markdown_file_creation import (
            COMMIT_MESSAGE,
        )

        assert "feat(145)" in COMMIT_MESSAGE

    def test_commit_message_contains_filename(self):
        """Test that COMMIT_MESSAGE contains the filename."""
        from sheep.features.feature_145_markdown_file_creation import (
            COMMIT_MESSAGE,
            MARKDOWN_FILENAME,
        )

        assert MARKDOWN_FILENAME in COMMIT_MESSAGE

    def test_all_required_imports_available(self):
        """Test that all required imports are available from the module."""
        from sheep.features import feature_145_markdown_file_creation

        # Check that logger is available
        assert hasattr(feature_145_markdown_file_creation, "_logger")

        # Check that all content generator utilities are imported
        # We'll just verify the module can be imported with these
        import inspect

        source = inspect.getsource(feature_145_markdown_file_creation)
        assert "from sheep.content_generators import" in source
        assert "from sheep.observability.logging import" in source
        assert "from pathlib import Path" in source

    def test_commit_message_format(self):
        """Test that COMMIT_MESSAGE follows conventional commit format."""
        from sheep.features.feature_145_markdown_file_creation import (
            COMMIT_MESSAGE,
        )

        # Should be in format: feat(145): create markdown file test-rtj7cz.md with prose content
        assert COMMIT_MESSAGE.startswith("feat(145):")
        assert "test-rtj7cz.md" in COMMIT_MESSAGE
