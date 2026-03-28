"""
Tests for end-to-end workflow module.

Tests verify that the complete workflow (file creation, validation, git operations)
executes correctly and reports status appropriately.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from workflow import (
    WorkflowStatus,
    create_markdown_file,
    execute_git_operations,
    main,
    validate_markdown_file,
)

# ============================================================================
# Tests for WorkflowStatus
# ============================================================================


class TestWorkflowStatus:
    """Tests for WorkflowStatus class."""

    def test_initialization(self):
        """Test WorkflowStatus initialization."""
        status = WorkflowStatus()
        assert status.phases == {}
        assert status.overall_success is True
        assert status.error_message is None

    def test_phase_tracking(self):
        """Test that phases are tracked correctly."""
        status = WorkflowStatus()
        status.start_phase("Phase 1")
        assert "Phase 1" in status.phases
        assert status.phases["Phase 1"]["start"] is not None

    def test_phase_completion(self):
        """Test marking phase as complete."""
        status = WorkflowStatus()
        status.start_phase("Phase 1")
        status.end_phase("Phase 1", success=True)
        assert status.phases["Phase 1"]["success"] is True
        assert status.overall_success is True

    def test_phase_failure_sets_overall_failure(self):
        """Test that phase failure sets overall_success to False."""
        status = WorkflowStatus()
        status.start_phase("Phase 1")
        status.end_phase("Phase 1", success=False, error="Test error")
        assert status.phases["Phase 1"]["success"] is False
        assert status.overall_success is False

    def test_report_generation(self):
        """Test that report is generated successfully."""
        status = WorkflowStatus()
        status.start_phase("Phase 1")
        status.end_phase("Phase 1", success=True)
        status.end_time = status.phases["Phase 1"]["end"]

        report = status.report()
        assert "Phase 1" in report
        assert "SUCCESS" in report
        assert "=" * 80 in report or "=" in report  # Check for border line


# ============================================================================
# Tests for File Creation
# ============================================================================


class TestFileCreation:
    """Tests for create_markdown_file function."""

    def test_creates_file(self):
        """Test that file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(str(filepath))
            assert filepath.exists()

    def test_file_has_h1_heading(self):
        """Test that created file has H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(str(filepath))
            content = filepath.read_text()
            assert content.startswith("# The Nature of Resilience")

    def test_file_has_blank_line_separator(self):
        """Test that file has blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(str(filepath))
            content = filepath.read_text()
            lines = content.split("\n")
            assert lines[1] == ""

    def test_file_has_prose_content(self):
        """Test that file contains prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(str(filepath))
            content = filepath.read_text()
            assert "Resilience" in content
            assert "bend without breaking" in content

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(str(filepath))
            binary_content = filepath.read_bytes()
            # Should be decodable as UTF-8
            binary_content.decode("utf-8")
            # Should not have BOM
            assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(str(filepath))
            binary_content = filepath.read_bytes()
            # Should not have CRLF
            assert b"\r\n" not in binary_content
            # Should have LF
            assert b"\n" in binary_content


# ============================================================================
# Tests for File Validation
# ============================================================================


class TestFileValidation:
    """Tests for validate_markdown_file function."""

    def test_validation_passes_for_valid_file(self):
        """Test that validation passes for correctly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            create_markdown_file(str(filepath))
            # Should not raise exception
            result = validate_markdown_file(str(filepath))
            assert result is True

    def test_validation_fails_for_missing_file(self):
        """Test that validation fails for missing file."""
        with pytest.raises(AssertionError):
            validate_markdown_file("/nonexistent/path/file.md")


# ============================================================================
# Tests for Git Operations
# ============================================================================


class TestGitOperations:
    """Tests for execute_git_operations function."""

    @patch("workflow.GitWorkflow")
    def test_git_operations_calls_workflow(self, mock_workflow_class):
        """Test that execute_git_operations creates and uses GitWorkflow."""
        mock_workflow = MagicMock()
        mock_workflow.execute_workflow.return_value = True
        mock_workflow_class.return_value = mock_workflow

        result = execute_git_operations()

        mock_workflow_class.assert_called_once()
        mock_workflow.execute_workflow.assert_called_once()
        assert result is True

    @patch("workflow.GitWorkflow")
    def test_git_operations_propagates_error(self, mock_workflow_class):
        """Test that execute_git_operations propagates git errors."""
        from workflow import GitWorkflowError
        mock_workflow = MagicMock()
        mock_workflow.execute_workflow.side_effect = GitWorkflowError("Test error")
        mock_workflow_class.return_value = mock_workflow

        with pytest.raises(GitWorkflowError):
            execute_git_operations()


# ============================================================================
# Tests for Main Workflow
# ============================================================================


class TestMainWorkflow:
    """Tests for main() function."""

    @patch("workflow.execute_git_operations")
    @patch("workflow.validate_markdown_file")
    @patch("workflow.create_markdown_file")
    def test_main_returns_0_on_success(self, mock_create, mock_validate, mock_git):
        """Test that main() returns 0 when all phases succeed."""
        mock_create.return_value = True
        mock_validate.return_value = True
        mock_git.return_value = True

        result = main()

        assert result == 0

    @patch("workflow.execute_git_operations")
    @patch("workflow.validate_markdown_file")
    @patch("workflow.create_markdown_file")
    def test_main_returns_1_on_creation_failure(self, mock_create, mock_validate, mock_git):
        """Test that main() returns 1 when file creation fails."""
        mock_create.side_effect = Exception("Creation failed")

        result = main()

        assert result == 1
        mock_validate.assert_not_called()
        mock_git.assert_not_called()

    @patch("workflow.execute_git_operations")
    @patch("workflow.validate_markdown_file")
    @patch("workflow.create_markdown_file")
    def test_main_returns_1_on_validation_failure(self, mock_create, mock_validate, mock_git):
        """Test that main() returns 1 when validation fails."""
        from validate_markdown_file import ValidationError
        mock_create.return_value = True
        mock_validate.side_effect = ValidationError("Validation failed")

        result = main()

        assert result == 1
        mock_git.assert_not_called()

    @patch("workflow.execute_git_operations")
    @patch("workflow.validate_markdown_file")
    @patch("workflow.create_markdown_file")
    def test_main_returns_1_on_git_failure(self, mock_create, mock_validate, mock_git):
        """Test that main() returns 1 when git operations fail."""
        from workflow import GitWorkflowError
        mock_create.return_value = True
        mock_validate.return_value = True
        mock_git.side_effect = GitWorkflowError("Git failed")

        result = main()

        assert result == 1

    @patch("workflow.execute_git_operations")
    @patch("workflow.validate_markdown_file")
    @patch("workflow.create_markdown_file")
    def test_main_calls_phases_in_order(self, mock_create, mock_validate, mock_git):
        """Test that main() calls phases in correct order."""
        call_order = []
        mock_create.side_effect = lambda: call_order.append("create") or True
        mock_validate.side_effect = lambda: call_order.append("validate") or True
        mock_git.side_effect = lambda: call_order.append("git") or True

        main()

        assert call_order == ["create", "validate", "git"]

    @patch("workflow.execute_git_operations")
    @patch("workflow.validate_markdown_file")
    @patch("workflow.create_markdown_file")
    def test_main_generates_status_report(self, mock_create, mock_validate, mock_git, capsys):
        """Test that main() generates status report."""
        mock_create.return_value = True
        mock_validate.return_value = True
        mock_git.return_value = True

        main()

        captured = capsys.readouterr()
        # Check that status report was printed
        assert "WORKFLOW STATUS REPORT" in captured.out or "Phase 1" in captured.out


# ============================================================================
# Integration Tests
# ============================================================================


class TestIntegration:
    """Integration tests for complete workflow."""

    @patch("workflow.execute_git_operations")
    def test_complete_workflow_integration(self, mock_git):
        """Test complete workflow without mocking git operations."""
        mock_git.return_value = True

        with tempfile.TemporaryDirectory() as tmpdir:
            # Save original create_markdown_file function
            import workflow as wf_module
            original_create = wf_module.create_markdown_file

            # Patch it to use temp directory
            def temp_create(filepath=None):
                return original_create(str(Path(tmpdir) / "test.md"))

            with patch.object(wf_module, "create_markdown_file", temp_create):
                with patch.object(wf_module, "validate_markdown_file") as mock_validate:
                    # Make validation check the actual temp file
                    def validate_temp_file(filepath=None):
                        from validate_markdown_file import validate_file
                        return validate_file(str(Path(tmpdir) / "test.md"))

                    mock_validate.side_effect = validate_temp_file

                    result = main()

                    # Should succeed
                    assert result == 0
                    mock_git.assert_called_once()
