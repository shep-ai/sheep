"""Tests for git integration (phase 3) for feature 076."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest


class TestStageFile:
    """Tests for git add (staging) operation."""

    def test_stage_file_runs_git_add_command(self):
        """Test that stage_file runs git add with correct arguments."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.stage_file("test-3nslmx.md")

            # Verify git add was called with correct arguments
            mock_run.assert_called_once_with(
                ["git", "add", "test-3nslmx.md"],
                check=True
            )

    def test_stage_file_uses_check_true(self):
        """Test that stage_file uses check=True for error handling."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.stage_file("test-3nslmx.md")

            # Verify check=True is used
            call_kwargs = mock_run.call_args[1]
            assert call_kwargs['check'] is True

    def test_stage_file_raises_on_git_error(self):
        """Test that stage_file raises when git add fails."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            # Simulate git error
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ['git', 'add', 'test-3nslmx.md']
            )

            with pytest.raises(subprocess.CalledProcessError):
                create_test_3nslmx.stage_file("test-3nslmx.md")

    def test_stage_file_prints_status_message(self):
        """Test that stage_file prints status message."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch('builtins.print') as mock_print:
                create_test_3nslmx.stage_file("test-3nslmx.md")

                # Verify print was called
                assert mock_print.called


class TestCommitFile:
    """Tests for git commit operation."""

    def test_commit_file_runs_git_commit_command(self):
        """Test that commit_file runs git commit with correct arguments."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.commit_file("test-3nslmx.md")

            # Verify git commit was called
            call_args = mock_run.call_args[0][0]
            assert call_args[0] == "git"
            assert call_args[1] == "commit"

    def test_commit_file_uses_no_verify_flag(self):
        """Test that commit_file uses --no-verify flag."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.commit_file("test-3nslmx.md")

            # Verify --no-verify flag is used
            call_args = mock_run.call_args[0][0]
            assert "--no-verify" in call_args

    def test_commit_file_uses_conventional_message_format(self):
        """Test that commit message follows conventional format."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.commit_file("test-3nslmx.md")

            # Verify conventional commit format
            call_args = mock_run.call_args[0][0]
            message_index = call_args.index('-m') + 1
            message = call_args[message_index]

            # Should start with feat(076):
            assert message.startswith("feat(076):")
            # Should mention the file
            assert "test-3nslmx.md" in message

    def test_commit_file_uses_check_true(self):
        """Test that commit_file uses check=True for error handling."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.commit_file("test-3nslmx.md")

            # Verify check=True is used
            call_kwargs = mock_run.call_args[1]
            assert call_kwargs['check'] is True

    def test_commit_file_raises_on_git_error(self):
        """Test that commit_file raises when git commit fails."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            # Simulate git error
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ['git', 'commit']
            )

            with pytest.raises(subprocess.CalledProcessError):
                create_test_3nslmx.commit_file("test-3nslmx.md")

    def test_commit_file_prints_status_message(self):
        """Test that commit_file prints status message."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch('builtins.print') as mock_print:
                create_test_3nslmx.commit_file("test-3nslmx.md")

                # Verify print was called
                assert mock_print.called


class TestPushCommit:
    """Tests for git push operation."""

    def test_push_commit_runs_git_push_command(self):
        """Test that push_commit runs git push with correct arguments."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.push_commit()

            # Verify git push was called
            call_args = mock_run.call_args[0][0]
            assert call_args[0] == "git"
            assert call_args[1] == "push"

    def test_push_commit_uses_upstream_flag(self):
        """Test that push_commit uses -u flag for upstream tracking."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.push_commit()

            # Verify -u flag is used
            call_args = mock_run.call_args[0][0]
            assert "-u" in call_args

    def test_push_commit_pushes_to_origin(self):
        """Test that push_commit pushes to origin."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.push_commit()

            # Verify origin is specified
            call_args = mock_run.call_args[0][0]
            assert "origin" in call_args

    def test_push_commit_pushes_current_branch(self):
        """Test that push_commit pushes current branch (HEAD)."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.push_commit()

            # Verify HEAD is specified
            call_args = mock_run.call_args[0][0]
            assert "HEAD" in call_args

    def test_push_commit_uses_check_true(self):
        """Test that push_commit uses check=True for error handling."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            create_test_3nslmx.push_commit()

            # Verify check=True is used
            call_kwargs = mock_run.call_args[1]
            assert call_kwargs['check'] is True

    def test_push_commit_raises_on_git_error(self):
        """Test that push_commit raises when git push fails."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            # Simulate git error
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ['git', 'push']
            )

            with pytest.raises(subprocess.CalledProcessError):
                create_test_3nslmx.push_commit()

    def test_push_commit_prints_status_message(self):
        """Test that push_commit prints status message."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch('builtins.print') as mock_print:
                create_test_3nslmx.push_commit()

                # Verify print was called
                assert mock_print.called


class TestGitWorkflow:
    """Tests for complete git workflow (add, commit, push)."""

    def test_git_workflow_calls_stage_commit_push_in_order(self):
        """Test that git_workflow calls functions in correct order."""
        import create_test_3nslmx

        with patch.object(create_test_3nslmx, 'stage_file') as mock_stage:
            with patch.object(create_test_3nslmx, 'commit_file') as mock_commit:
                with patch.object(create_test_3nslmx, 'push_commit') as mock_push:
                    create_test_3nslmx.git_workflow("test-3nslmx.md")

                    # Verify all three were called
                    assert mock_stage.called
                    assert mock_commit.called
                    assert mock_push.called

                    # Verify call order by checking call args
                    assert mock_stage.call_count == 1
                    assert mock_commit.call_count == 1
                    assert mock_push.call_count == 1

    def test_git_workflow_returns_0_on_success(self):
        """Test that git_workflow returns 0 on success."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = create_test_3nslmx.git_workflow("test-3nslmx.md")
            assert result == 0

    def test_git_workflow_returns_1_on_stage_failure(self):
        """Test that git_workflow returns 1 if stage_file fails."""
        import create_test_3nslmx

        with patch.object(create_test_3nslmx, 'stage_file') as mock_stage:
            mock_stage.side_effect = subprocess.CalledProcessError(1, ['git', 'add'])

            result = create_test_3nslmx.git_workflow("test-3nslmx.md")
            assert result == 1

    def test_git_workflow_returns_1_on_commit_failure(self):
        """Test that git_workflow returns 1 if commit_file fails."""
        import create_test_3nslmx

        with patch.object(create_test_3nslmx, 'stage_file'):
            with patch.object(create_test_3nslmx, 'commit_file') as mock_commit:
                mock_commit.side_effect = subprocess.CalledProcessError(1, ['git', 'commit'])

                result = create_test_3nslmx.git_workflow("test-3nslmx.md")
                assert result == 1

    def test_git_workflow_returns_1_on_push_failure(self):
        """Test that git_workflow returns 1 if push_commit fails."""
        import create_test_3nslmx

        with patch.object(create_test_3nslmx, 'stage_file'):
            with patch.object(create_test_3nslmx, 'commit_file'):
                with patch.object(create_test_3nslmx, 'push_commit') as mock_push:
                    mock_push.side_effect = subprocess.CalledProcessError(1, ['git', 'push'])

                    result = create_test_3nslmx.git_workflow("test-3nslmx.md")
                    assert result == 1


class TestPhase3MainFunction:
    """Tests for phase 3 main execution."""

    def test_main_phase3_executes_git_workflow(self):
        """Test that main_phase3 executes git workflow."""
        import create_test_3nslmx

        with patch.object(create_test_3nslmx, 'git_workflow') as mock_workflow:
            mock_workflow.return_value = 0
            result = create_test_3nslmx.main_phase3()
            assert result == 0
            assert mock_workflow.called

    def test_main_phase3_returns_0_on_success(self):
        """Test that main_phase3 returns 0 on success."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = create_test_3nslmx.main_phase3()
            assert result == 0

    def test_main_phase3_returns_1_on_error(self):
        """Test that main_phase3 returns 1 on error."""
        import create_test_3nslmx

        with patch.object(create_test_3nslmx, 'git_workflow') as mock_workflow:
            mock_workflow.side_effect = Exception("Test error")
            result = create_test_3nslmx.main_phase3()
            assert result == 1

    def test_main_phase3_prints_completion_message(self):
        """Test that main_phase3 prints completion message on success."""
        import create_test_3nslmx

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch('builtins.print') as mock_print:
                create_test_3nslmx.main_phase3()

                # Verify print was called with completion message
                assert mock_print.called
