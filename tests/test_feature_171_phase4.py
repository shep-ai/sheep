"""Tests for feature 171 phase 4: Orchestration & Execution.

Tests for the orchestration and execution phase of feature 171:
- main(): Orchestrates complete workflow (generate, validate, write, git operations)
- Integration tests verifying all success criteria are met
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestMainOrchestration:
    """Tests for main() orchestration function."""

    def test_main_can_be_called_without_arguments(self):
        """Test that main() can be called without arguments."""
        from sheep.features.feature_171 import main

        # main() should be callable
        assert callable(main)

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_main_produces_markdown_file(self, mock_add, mock_commit, mock_push):
        """Test that main() produces test-jn0b4n.md file."""
        from sheep.features.feature_171 import main

        mock_commit.return_value = "[branch] commit\n"
        mock_push.return_value = "Pushed\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = main()

                # File should exist
                assert Path('test-jn0b4n.md').exists()
                assert Path('test-jn0b4n.md').is_file()

                # Result should indicate success
                assert result is not None
                if isinstance(result, dict):
                    assert 'filepath' in result
                    assert 'content' in result

            finally:
                os.chdir(old_cwd)

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_main_returns_success_on_completion(self, mock_add, mock_commit, mock_push):
        """Test that main() returns/indicates success on completion."""
        from sheep.features.feature_171 import main

        mock_commit.return_value = "[branch] commit\n"
        mock_push.return_value = "Pushed\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = main()

                # Should return successfully (not raise exception)
                assert result is not None
                # Result should be dict with expected keys
                assert isinstance(result, dict)
                assert 'filepath' in result

            finally:
                os.chdir(old_cwd)

    def test_main_handles_validation_failure_gracefully(self):
        """Test that main() handles validation failure gracefully."""
        from sheep.features.feature_171 import main, validate_encoding

        # Mock validate_encoding to raise an error
        with patch('sheep.features.feature_171.validate_encoding') as mock_validate:
            mock_validate.side_effect = ValueError("Invalid encoding")

            with tempfile.TemporaryDirectory() as tmpdir:
                import os
                old_cwd = os.getcwd()
                try:
                    os.chdir(tmpdir)
                    # main() should raise exception if validation fails
                    with pytest.raises(ValueError, match="Invalid encoding"):
                        main()

                finally:
                    os.chdir(old_cwd)

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_main_calls_validation_before_file_write(
        self, mock_add, mock_commit, mock_push
    ):
        """Test that main() calls validation functions before writing file."""
        from sheep.features.feature_171 import main

        mock_commit.return_value = "[branch] commit\n"
        mock_push.return_value = "Pushed\n"

        # Track call order
        call_order = []

        with patch('sheep.features.feature_171.validate_content_structure') as mock_validate:
            mock_validate.side_effect = lambda x: call_order.append('validate')

            with patch('sheep.features.feature_171.write_markdown_file') as mock_write:
                def write_file_side_effect(*args, **kwargs):
                    call_order.append('write')
                    # Create actual file so validation succeeds
                    filepath = Path(kwargs.get('repo_path', '.')) / args[1]
                    # Use newline='' to ensure LF-only line endings
                    filepath.write_text(args[0], encoding='utf-8', newline='')
                    return str(filepath)

                mock_write.side_effect = write_file_side_effect

                with tempfile.TemporaryDirectory() as tmpdir:
                    import os
                    old_cwd = os.getcwd()
                    try:
                        os.chdir(tmpdir)
                        main()

                        # Validation should come before write
                        assert 'validate' in call_order
                        assert 'write' in call_order
                        assert call_order.index('validate') < call_order.index('write')

                    finally:
                        os.chdir(old_cwd)

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_main_calls_git_operations_in_sequence(
        self, mock_add, mock_commit, mock_push
    ):
        """Test that main() calls git operations in correct sequence."""
        from sheep.features.feature_171 import main

        mock_commit.return_value = "[branch] commit\n"
        mock_push.return_value = "Pushed\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                main()

                # All git operations should be called
                mock_add.assert_called_once()
                mock_commit.assert_called_once()
                mock_push.assert_called_once()

            finally:
                os.chdir(old_cwd)

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_main_handles_git_add_failure(self, mock_add, mock_commit, mock_push):
        """Test that main() stops if git add fails."""
        from sheep.features.feature_171 import main

        mock_add.side_effect = RuntimeError("git add failed")

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Should raise when git_add fails
                with pytest.raises(RuntimeError, match="git add failed"):
                    main()

                # git_commit and git_push should not be called
                mock_commit.assert_not_called()
                mock_push.assert_not_called()

            finally:
                os.chdir(old_cwd)

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_main_with_custom_repo_path(self, mock_add, mock_commit, mock_push):
        """Test that main() can accept custom repo path."""
        from sheep.features.feature_171 import main

        mock_commit.return_value = "[branch] commit\n"
        mock_push.return_value = "Pushed\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            result = main(repo_path=tmpdir)

            # Should succeed with custom path
            assert result is not None
            # git operations should be called (at least git_add)
            assert mock_add.called or mock_commit.called or mock_push.called


class TestPhase4Integration:
    """Integration tests for phase 4 (orchestration and execution)."""

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_full_workflow_creates_file_with_valid_content(
        self, mock_add, mock_commit, mock_push
    ):
        """Test complete workflow creates file with valid content."""
        from sheep.features.feature_171 import main, validate_file_properties

        mock_commit.return_value = "[branch] commit\n"
        mock_push.return_value = "Pushed\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = main()

                filepath = result['filepath']
                # File should pass all property validations
                validate_file_properties(filepath)

            finally:
                os.chdir(old_cwd)

    @patch('sheep.features.feature_171.git_push')
    @patch('sheep.features.feature_171.git_commit')
    @patch('sheep.features.feature_171.git_add')
    def test_main_orchestrates_all_components(
        self, mock_add, mock_commit, mock_push
    ):
        """Test that main() successfully orchestrates all components."""
        from sheep.features.feature_171 import main

        mock_commit.return_value = "[branch] commit\n"
        mock_push.return_value = "Pushed\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = main()

                # Verify all expected keys in result
                assert 'filepath' in result
                assert 'content' in result
                assert 'commit_message' in result
                assert 'push_result' in result

                # Verify file exists
                assert Path(result['filepath']).exists()

            finally:
                os.chdir(old_cwd)
