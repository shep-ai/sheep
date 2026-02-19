"""Tests for fast mode feature — state, routing, flow behavior, and CLI integration."""

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from sheep.cli import app
from sheep.flows.code_implementation import CodeImplementationFlow, CodeImplementationState

# ── State tests ──────────────────────────────────────────────────────────────


class TestCodeImplementationStateFastMode:
    """Tests for fast_mode field on CodeImplementationState."""

    def test_fast_mode_defaults_to_false(self):
        state = CodeImplementationState()
        assert state.fast_mode is False

    def test_fast_mode_can_be_set_true(self):
        state = CodeImplementationState(fast_mode=True)
        assert state.fast_mode is True

    def test_fast_mode_does_not_affect_other_defaults(self):
        state = CodeImplementationState(fast_mode=True)
        assert state.use_worktree is False
        assert state.auto_push is True
        assert state.repo_path == ""
        assert state.final_status == "pending"


# ── Router tests ─────────────────────────────────────────────────────────────


class TestRouteAfterSetup:
    """Tests for the route_after_setup router."""

    @pytest.fixture()
    def flow(self):
        with patch("sheep.flows.code_implementation.get_settings") as mock_settings:
            settings = MagicMock()
            settings.verbose = False
            mock_settings.return_value = settings
            return CodeImplementationFlow(verbose=False)

    def test_routes_to_research_when_not_fast(self, flow):
        flow.state.fast_mode = False
        result = flow.route_after_setup("success")
        assert result == "research_codebase"

    def test_routes_to_implement_when_fast(self, flow):
        flow.state.fast_mode = True
        result = flow.route_after_setup("success")
        assert result == "implement_changes"

    def test_routes_to_error_on_error(self, flow):
        flow.state.fast_mode = False
        result = flow.route_after_setup("error")
        assert result == "error"

    def test_routes_to_error_on_error_even_in_fast_mode(self, flow):
        flow.state.fast_mode = True
        result = flow.route_after_setup("error")
        assert result == "error"


class TestRouteAfterImplementation:
    """Tests for the route_after_implementation router."""

    @pytest.fixture()
    def flow(self):
        with patch("sheep.flows.code_implementation.get_settings") as mock_settings:
            settings = MagicMock()
            settings.verbose = False
            mock_settings.return_value = settings
            return CodeImplementationFlow(verbose=False)

    def test_routes_to_review_when_not_fast(self, flow):
        flow.state.fast_mode = False
        result = flow.route_after_implementation("success")
        assert result == "review_changes"

    def test_routes_to_commit_when_fast(self, flow):
        flow.state.fast_mode = True
        result = flow.route_after_implementation("success")
        assert result == "commit_and_push"

    def test_routes_to_error_on_error(self, flow):
        flow.state.fast_mode = False
        result = flow.route_after_implementation("error")
        assert result == "error"

    def test_routes_to_error_on_error_even_in_fast_mode(self, flow):
        flow.state.fast_mode = True
        result = flow.route_after_implementation("error")
        assert result == "error"


# ── Existing route_after_review unchanged ────────────────────────────────────


class TestRouteAfterReviewUnchanged:
    """Verify existing route_after_review behavior is preserved."""

    @pytest.fixture()
    def flow(self):
        with patch("sheep.flows.code_implementation.get_settings") as mock_settings:
            settings = MagicMock()
            settings.verbose = False
            mock_settings.return_value = settings
            return CodeImplementationFlow(verbose=False)

    def test_passed_routes_to_commit(self, flow):
        result = flow.route_after_review("passed")
        assert result == "commit_and_push"

    def test_needs_changes_routes_to_implement(self, flow):
        result = flow.route_after_review("needs_changes")
        assert result == "implement_changes"

    def test_unknown_routes_to_commit(self, flow):
        result = flow.route_after_review("something_else")
        assert result == "commit_and_push"


# ── LLM override tests ──────────────────────────────────────────────────────


class TestImplementChangesLLMOverride:
    """Tests for fast LLM usage in implement_changes."""

    @pytest.fixture()
    def flow(self):
        with patch("sheep.flows.code_implementation.get_settings") as mock_settings:
            settings = MagicMock()
            settings.verbose = False
            mock_settings.return_value = settings
            return CodeImplementationFlow(verbose=False)

    @patch("sheep.flows.code_implementation.Task")
    @patch("sheep.flows.code_implementation.Crew")
    @patch("sheep.flows.code_implementation.get_fast_llm")
    @patch("sheep.flows.code_implementation.create_code_implementer_agent")
    def test_fast_mode_uses_fast_llm(
        self, mock_create_agent, mock_get_fast_llm, mock_crew, mock_task, flow
    ):
        mock_agent = MagicMock()
        mock_create_agent.return_value = mock_agent
        mock_fast_llm = MagicMock()
        mock_get_fast_llm.return_value = mock_fast_llm
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "changes done"
        mock_crew.return_value = mock_crew_instance

        flow.state.fast_mode = True
        flow.state.working_path = "/tmp/repo"
        flow.state.issue_description = "Add a button"

        flow.implement_changes("success")

        mock_get_fast_llm.assert_called_once()
        mock_create_agent.assert_called_once_with(llm=mock_fast_llm, verbose=False)

    @patch("sheep.flows.code_implementation.Task")
    @patch("sheep.flows.code_implementation.Crew")
    @patch("sheep.flows.code_implementation.create_code_implementer_agent")
    def test_normal_mode_uses_default_llm(self, mock_create_agent, mock_crew, mock_task, flow):
        mock_agent = MagicMock()
        mock_create_agent.return_value = mock_agent
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "changes done"
        mock_crew.return_value = mock_crew_instance

        flow.state.fast_mode = False
        flow.state.working_path = "/tmp/repo"
        flow.state.issue_description = "Add a button"
        flow.state.research_findings = "Found patterns in codebase"

        flow.implement_changes("success")

        mock_create_agent.assert_called_once_with(verbose=False)


# ── Task description tests ───────────────────────────────────────────────────


class TestImplementChangesTaskDescription:
    """Tests for task description in fast vs normal mode."""

    @pytest.fixture()
    def flow(self):
        with patch("sheep.flows.code_implementation.get_settings") as mock_settings:
            settings = MagicMock()
            settings.verbose = False
            mock_settings.return_value = settings
            return CodeImplementationFlow(verbose=False)

    @patch("sheep.flows.code_implementation.Task")
    @patch("sheep.flows.code_implementation.Crew")
    @patch("sheep.flows.code_implementation.get_fast_llm")
    @patch("sheep.flows.code_implementation.create_code_implementer_agent")
    def test_fast_mode_description_does_not_contain_none(
        self, mock_create_agent, mock_get_fast_llm, mock_crew, mock_task, flow
    ):
        mock_create_agent.return_value = MagicMock()
        mock_get_fast_llm.return_value = MagicMock()
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "changes done"
        mock_crew.return_value = mock_crew_instance

        flow.state.fast_mode = True
        flow.state.working_path = "/tmp/repo"
        flow.state.issue_description = "Add a button"
        flow.state.research_findings = None

        flow.implement_changes("success")

        # Get the description passed to Task constructor
        task_call_kwargs = mock_task.call_args.kwargs
        description = task_call_kwargs["description"]
        assert "None" not in description
        assert "explore" in description.lower() or "codebase" in description.lower()

    @patch("sheep.flows.code_implementation.Task")
    @patch("sheep.flows.code_implementation.Crew")
    @patch("sheep.flows.code_implementation.create_code_implementer_agent")
    def test_normal_mode_includes_research_findings(
        self, mock_create_agent, mock_crew, mock_task, flow
    ):
        mock_create_agent.return_value = MagicMock()
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "changes done"
        mock_crew.return_value = mock_crew_instance

        flow.state.fast_mode = False
        flow.state.working_path = "/tmp/repo"
        flow.state.issue_description = "Add a button"
        flow.state.research_findings = "Found patterns in codebase"

        flow.implement_changes("success")

        task_call_kwargs = mock_task.call_args.kwargs
        description = task_call_kwargs["description"]
        assert "Found patterns in codebase" in description


# ── CLI integration tests ────────────────────────────────────────────────────

runner = CliRunner()


class TestCLIFastFlag:
    """Tests for --fast/-f CLI flag and panel display."""

    @patch("sheep.flows.run_code_implementation")
    def test_fast_flag_passed_to_flow(self, mock_run, tmp_path):
        mock_state = MagicMock()
        mock_state.final_status = "completed"
        mock_state.branch_name = "feat/test"
        mock_state.working_path = str(tmp_path)
        mock_state.pushed = False
        mock_state.review_iterations = 0
        mock_state.changes_made = "test changes"
        mock_run.return_value = mock_state

        result = runner.invoke(app, [
            "implement", str(tmp_path), "-i", "test issue", "--fast",
        ])

        assert result.exit_code == 0
        mock_run.assert_called_once()
        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["fast_mode"] is True

    @patch("sheep.flows.run_code_implementation")
    def test_short_flag_f_passed_to_flow(self, mock_run, tmp_path):
        mock_state = MagicMock()
        mock_state.final_status = "completed"
        mock_state.branch_name = "feat/test"
        mock_state.working_path = str(tmp_path)
        mock_state.pushed = False
        mock_state.review_iterations = 0
        mock_state.changes_made = "test changes"
        mock_run.return_value = mock_state

        result = runner.invoke(app, [
            "implement", str(tmp_path), "-i", "test issue", "-f",
        ])

        assert result.exit_code == 0
        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["fast_mode"] is True

    @patch("sheep.flows.run_code_implementation")
    def test_no_fast_flag_defaults_to_false(self, mock_run, tmp_path):
        mock_state = MagicMock()
        mock_state.final_status = "completed"
        mock_state.branch_name = "feat/test"
        mock_state.working_path = str(tmp_path)
        mock_state.pushed = False
        mock_state.review_iterations = 0
        mock_state.changes_made = "test changes"
        mock_run.return_value = mock_state

        result = runner.invoke(app, [
            "implement", str(tmp_path), "-i", "test issue",
        ])

        assert result.exit_code == 0
        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["fast_mode"] is False

    @patch("sheep.flows.run_code_implementation")
    def test_panel_shows_mode_fast(self, mock_run, tmp_path):
        mock_state = MagicMock()
        mock_state.final_status = "completed"
        mock_state.branch_name = "feat/test"
        mock_state.working_path = str(tmp_path)
        mock_state.pushed = False
        mock_state.review_iterations = 0
        mock_state.changes_made = "test changes"
        mock_run.return_value = mock_state

        result = runner.invoke(app, [
            "implement", str(tmp_path), "-i", "test issue", "--fast",
        ])

        assert result.exit_code == 0
        assert "Mode" in result.output
        assert "Fast" in result.output

    @patch("sheep.flows.run_code_implementation")
    def test_panel_shows_mode_normal(self, mock_run, tmp_path):
        mock_state = MagicMock()
        mock_state.final_status = "completed"
        mock_state.branch_name = "feat/test"
        mock_state.working_path = str(tmp_path)
        mock_state.pushed = False
        mock_state.review_iterations = 0
        mock_state.changes_made = "test changes"
        mock_run.return_value = mock_state

        result = runner.invoke(app, [
            "implement", str(tmp_path), "-i", "test issue",
        ])

        assert result.exit_code == 0
        assert "Mode" in result.output
        assert "Normal" in result.output


class TestRunCodeImplementationFastMode:
    """Tests for run_code_implementation accepting fast_mode parameter."""

    @patch("sheep.flows.code_implementation.CodeImplementationFlow")
    def test_fast_mode_included_in_input_data(self, mock_flow_class):
        mock_flow = MagicMock()
        mock_flow.state = CodeImplementationState(
            final_status="completed",
            repo_path="/tmp/repo",
        )
        mock_flow_class.return_value = mock_flow

        from sheep.flows.code_implementation import run_code_implementation

        run_code_implementation(
            repo_path="/tmp/repo",
            issue_description="test",
            fast_mode=True,
        )

        mock_flow.kickoff.assert_called_once()
        input_data = mock_flow.kickoff.call_args.kwargs["inputs"]
        assert input_data["fast_mode"] is True

    @patch("sheep.flows.code_implementation.CodeImplementationFlow")
    def test_fast_mode_defaults_to_false_in_input_data(self, mock_flow_class):
        mock_flow = MagicMock()
        mock_flow.state = CodeImplementationState(
            final_status="completed",
            repo_path="/tmp/repo",
        )
        mock_flow_class.return_value = mock_flow

        from sheep.flows.code_implementation import run_code_implementation

        run_code_implementation(
            repo_path="/tmp/repo",
            issue_description="test",
        )

        input_data = mock_flow.kickoff.call_args.kwargs["inputs"]
        assert input_data["fast_mode"] is False
