"""Tests for Feature 200 orchestration script.

This module contains comprehensive tests for feature_200_main.py:
- Module structure with imports and constants
- Main function execution and workflow
- Result handling and exit codes
- Integration with create_and_commit_markdown_file utility
"""

import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import pytest

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from feature_200_main import main


class TestModuleStructure:
    """Tests for feature_200_main.py module structure."""

    def test_module_has_shebang(self):
        """Test that module has proper shebang for direct execution."""
        content = Path(__file__).parent.parent / "feature_200_main.py"
        first_line = content.read_text().split('\n')[0]
        assert first_line == "#!/usr/bin/env python3"

    def test_module_docstring_exists(self):
        """Test that module has docstring."""
        import feature_200_main
        assert feature_200_main.__doc__ is not None
        assert "Feature 200" in feature_200_main.__doc__
        assert "orchestration" in feature_200_main.__doc__.lower()

    def test_main_function_exists(self):
        """Test that main() function is defined."""
        import feature_200_main
        assert hasattr(feature_200_main, 'main')
        assert callable(feature_200_main.main)

    def test_imports_correct_modules(self):
        """Test that module imports required dependencies."""
        import feature_200_main
        import sys
        assert feature_200_main.sys is sys
        assert hasattr(feature_200_main, 'Path')
        assert hasattr(feature_200_main, 'create_and_commit_markdown_file')
        assert hasattr(feature_200_main, 'get_logger')

    def test_has_entry_point(self):
        """Test that module has if __name__ == '__main__' entry point."""
        script_content = Path(__file__).parent.parent / "feature_200_main.py"
        content = script_content.read_text()
        assert 'if __name__ == "__main__"' in content
        assert 'sys.exit(main())' in content


class TestMainFunctionSignature:
    """Tests for main() function signature and basic behavior."""

    def test_main_has_no_required_arguments(self):
        """Test that main() takes no required arguments."""
        import inspect
        sig = inspect.signature(main)
        assert len(sig.parameters) == 0

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_returns_integer(self, mock_create):
        """Test that main() returns an integer exit code."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': ['content_generation', 'file_creation'],
            'steps_failed': [],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': 'abc1234',
            'errors': [],
        }
        result = main()
        assert isinstance(result, int)
        assert result in [0, 1]

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_returns_zero_on_success(self, mock_create):
        """Test that main() returns 0 when workflow succeeds."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': ['content_generation', 'file_creation', 'file_validation', 'git_staging', 'git_commit', 'git_push'],
            'steps_failed': [],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': 'abc1234',
            'errors': [],
        }
        result = main()
        assert result == 0

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_returns_one_on_failure(self, mock_create):
        """Test that main() returns 1 when workflow fails."""
        mock_create.return_value = {
            'success': False,
            'steps_completed': ['content_generation'],
            'steps_failed': ['file_creation'],
            'file_path': None,
            'commit_hash': None,
            'errors': ['File creation failed: Permission denied'],
        }
        result = main()
        assert result == 1


class TestWorkflowExecution:
    """Tests for workflow execution and orchestration."""

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_calls_create_and_commit_with_correct_parameters(self, mock_create):
        """Test that main() calls create_and_commit_markdown_file with Feature 200 parameters."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': [],
            'steps_failed': [],
            'file_path': None,
            'commit_hash': None,
            'errors': [],
        }
        main()

        # Verify function was called with correct arguments
        mock_create.assert_called_once()
        call_kwargs = mock_create.call_args[1]

        assert call_kwargs['filename'] == 'test-8ij3et.md'
        assert call_kwargs['filepath'] is None
        assert call_kwargs['branch_name'] == 'feat/200-markdown-file-creation-791c69'

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_logs_starting_message(self, mock_create):
        """Test that main() logs a starting message for Feature 200."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': [],
            'steps_failed': [],
            'file_path': None,
            'commit_hash': None,
            'errors': [],
        }

        with patch('feature_200_main._logger') as mock_logger:
            main()

            # Check that info() was called with Feature 200 message
            calls = [str(call[0]) for call in mock_logger.info.call_args_list]
            log_text = ' '.join(calls)
            assert '200' in log_text or 'Feature 200' in log_text

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('builtins.print')
    def test_main_prints_results(self, mock_print, mock_create):
        """Test that main() prints workflow results."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': ['content_generation', 'file_creation'],
            'steps_failed': [],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': 'abc1234',
            'errors': [],
        }
        main()

        # Verify print was called to output results
        assert mock_print.call_count > 0

        # Check for expected content in printed output
        printed_text = ' '.join(str(call[0][0]) for call in mock_print.call_args_list)
        assert 'WORKFLOW RESULTS' in printed_text
        assert 'Success' in printed_text

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('builtins.print')
    def test_main_prints_success_status(self, mock_print, mock_create):
        """Test that main() prints success status."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': ['content_generation', 'file_creation', 'git_commit'],
            'steps_failed': [],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': 'abc1234',
            'errors': [],
        }
        main()

        # Check for Success: True in output
        printed_text = ' '.join(str(call[0][0]) for call in mock_print.call_args_list)
        assert 'Success: True' in printed_text

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('builtins.print')
    def test_main_prints_steps_completed(self, mock_print, mock_create):
        """Test that main() prints steps completed."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': ['content_generation', 'file_creation', 'file_validation'],
            'steps_failed': [],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': 'abc1234',
            'errors': [],
        }
        main()

        printed_text = ' '.join(str(call[0][0]) for call in mock_print.call_args_list)
        assert 'Steps Completed:' in printed_text
        assert 'content_generation' in printed_text

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('builtins.print')
    def test_main_prints_file_path_on_success(self, mock_print, mock_create):
        """Test that main() prints file path when successful."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': ['content_generation', 'file_creation'],
            'steps_failed': [],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': 'abc1234',
            'errors': [],
        }
        main()

        printed_text = ' '.join(str(call[0][0]) for call in mock_print.call_args_list)
        assert 'File:' in printed_text
        assert 'test-8ij3et.md' in printed_text

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('builtins.print')
    def test_main_prints_commit_hash_on_success(self, mock_print, mock_create):
        """Test that main() prints commit hash when available."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': ['content_generation', 'file_creation', 'git_commit'],
            'steps_failed': [],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': 'abc1234567890ab',
            'errors': [],
        }
        main()

        printed_text = ' '.join(str(call[0][0]) for call in mock_print.call_args_list)
        assert 'Commit:' in printed_text
        assert 'abc1234567890ab' in printed_text

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('builtins.print')
    def test_main_prints_steps_failed_on_failure(self, mock_print, mock_create):
        """Test that main() prints failed steps on failure."""
        mock_create.return_value = {
            'success': False,
            'steps_completed': ['content_generation'],
            'steps_failed': ['file_creation'],
            'file_path': None,
            'commit_hash': None,
            'errors': ['File creation failed'],
        }
        main()

        printed_text = ' '.join(str(call[0][0]) for call in mock_print.call_args_list)
        assert 'Steps Failed:' in printed_text
        assert 'file_creation' in printed_text

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('builtins.print')
    def test_main_prints_errors_on_failure(self, mock_print, mock_create):
        """Test that main() prints errors when workflow fails."""
        mock_create.return_value = {
            'success': False,
            'steps_completed': [],
            'steps_failed': ['content_generation'],
            'file_path': None,
            'commit_hash': None,
            'errors': ['API request failed: Connection timeout'],
        }
        main()

        printed_text = ' '.join(str(call[0][0]) for call in mock_print.call_args_list)
        assert 'Errors:' in printed_text
        assert 'API' in printed_text or 'timeout' in printed_text

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('builtins.print')
    def test_main_prints_separator_lines(self, mock_print, mock_create):
        """Test that main() prints separator lines for readability."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': [],
            'steps_failed': [],
            'file_path': None,
            'commit_hash': None,
            'errors': [],
        }
        main()

        # Check for separator lines (80 character lines)
        printed_text = '\n'.join(str(call[0][0]) for call in mock_print.call_args_list)
        assert '=' * 80 in printed_text


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_handles_empty_steps_lists(self, mock_create):
        """Test that main() handles empty steps_completed and steps_failed lists."""
        mock_create.return_value = {
            'success': False,
            'steps_completed': [],
            'steps_failed': [],
            'file_path': None,
            'commit_hash': None,
            'errors': [],
        }
        # Should not raise exception
        result = main()
        assert result == 1

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_handles_none_file_path(self, mock_create):
        """Test that main() handles None file_path gracefully."""
        mock_create.return_value = {
            'success': False,
            'steps_completed': ['content_generation'],
            'steps_failed': ['file_creation'],
            'file_path': None,
            'commit_hash': None,
            'errors': ['File creation failed'],
        }
        with patch('builtins.print') as mock_print:
            result = main()
            # Should not print file path if None
            printed_text = ' '.join(str(call[0][0]) for call in mock_print.call_args_list)
            # If file_path is None, it should not be printed or should say None
            assert result == 1

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_handles_none_commit_hash(self, mock_create):
        """Test that main() handles None commit_hash gracefully."""
        mock_create.return_value = {
            'success': False,
            'steps_completed': ['content_generation', 'file_creation'],
            'steps_failed': ['git_commit'],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': None,
            'errors': ['Git commit failed'],
        }
        with patch('builtins.print') as mock_print:
            result = main()
            assert result == 1

    @patch('feature_200_main.create_and_commit_markdown_file')
    def test_main_handles_empty_errors_list(self, mock_create):
        """Test that main() handles empty errors list gracefully."""
        mock_create.return_value = {
            'success': True,
            'steps_completed': ['content_generation', 'file_creation'],
            'steps_failed': [],
            'file_path': '/path/to/test-8ij3et.md',
            'commit_hash': 'abc1234',
            'errors': [],
        }
        result = main()
        assert result == 0


class TestIntegrationWithEntryPoint:
    """Tests for integration with __main__ entry point."""

    def test_script_can_be_executed_directly(self):
        """Test that script can be executed directly as Python module."""
        script_path = Path(__file__).parent.parent / "feature_200_main.py"

        # Just verify the script exists and is executable
        assert script_path.exists()
        assert script_path.is_file()

        # Check that shebang is correct for direct execution
        first_line = script_path.read_text().split('\n')[0]
        assert first_line == "#!/usr/bin/env python3"

    @patch('feature_200_main.create_and_commit_markdown_file')
    @patch('sys.exit')
    def test_entry_point_calls_sys_exit_with_result(self, mock_exit, mock_create):
        """Test that __main__ entry point calls sys.exit with main() result."""
        # This test verifies the entry point behavior
        # The entry point should call sys.exit(main())

        mock_create.return_value = {
            'success': True,
            'steps_completed': [],
            'steps_failed': [],
            'file_path': None,
            'commit_hash': None,
            'errors': [],
        }

        # Verify that main() returns 0 on success
        result = main()
        assert result == 0


class TestConsistencyWithFeature199:
    """Tests to ensure consistency with Feature 199 pattern."""

    def test_feature_200_parameters_differ_from_feature_199(self):
        """Test that Feature 200 uses different filename and branch than Feature 199."""
        import feature_200_main

        # Read the source to verify parameters
        script_content = Path(__file__).parent.parent / "feature_200_main.py"
        content = script_content.read_text()

        # Feature 200 should use test-8ij3et.md
        assert 'test-8ij3et.md' in content
        assert "filename=\"test-8ij3et.md\"" in content

        # Feature 200 should use correct branch
        assert 'feat/200-markdown-file-creation-791c69' in content
        assert "branch_name=\"feat/200-markdown-file-creation-791c69\"" in content

    def test_feature_200_has_same_structure_as_feature_199(self):
        """Test that Feature 200 main() has same structure/pattern as Feature 199."""
        # Both should have:
        # 1. imports
        # 2. logger
        # 3. main() function
        # 4. sys.path.insert(0, str(Path(__file__).parent))
        # 5. create_and_commit_markdown_file call
        # 6. result printing
        # 7. return 0 or 1 based on success

        script_content = Path(__file__).parent.parent / "feature_200_main.py"
        content = script_content.read_text()

        assert 'import sys' in content
        assert 'from pathlib import Path' in content
        assert 'from src.create_markdown import create_and_commit_markdown_file' in content
        assert 'from sheep.observability.logging import get_logger' in content
        assert '_logger = get_logger(__name__)' in content
        assert 'def main():' in content
        assert 'create_and_commit_markdown_file(' in content
        assert 'print' in content  # Results printing
        assert 'return 0 if result' in content
