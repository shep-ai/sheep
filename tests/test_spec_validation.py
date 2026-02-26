"""Tests for spec intake validation — entropy utility and SpecInput model."""

import os
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# compute_shannon_entropy tests
# ---------------------------------------------------------------------------


class TestComputeShannonEntropy:
    """Unit tests for the Shannon entropy helper function."""

    def setup_method(self) -> None:
        from sheep.models.spec import compute_shannon_entropy

        self.entropy = compute_shannon_entropy

    def test_entropy_empty(self) -> None:
        """Empty string returns 0.0 by convention."""
        assert self.entropy("") == 0.0

    def test_entropy_single_char(self) -> None:
        """Single unique character has zero entropy (no uncertainty)."""
        assert self.entropy("a") == 0.0
        assert self.entropy("aaaa") == 0.0

    def test_entropy_two_chars(self) -> None:
        """Two equally-probable characters give entropy of 1.0 bit."""
        assert self.entropy("ab") == pytest.approx(1.0)
        assert self.entropy("aabb") == pytest.approx(1.0)

    def test_entropy_low_gibberish(self) -> None:
        """Gibberish 'gdgd' has low entropy — two equally-probable chars = 1.0 bit, well below 2.5."""
        result = self.entropy("gdgd")
        assert result < 2.5

    def test_entropy_high_real_sentence(self) -> None:
        """A real English sentence with diverse characters has entropy above 2.5."""
        result = self.entropy("Add dark mode to the settings panel")
        assert result > 2.5

    def test_entropy_return_type(self) -> None:
        """Return type is float."""
        result = self.entropy("hello world")
        assert isinstance(result, float)


# ---------------------------------------------------------------------------
# SpecInput model tests
# ---------------------------------------------------------------------------


class TestSpecInput:
    """Unit tests for the SpecInput Pydantic model and its field validator."""

    def setup_method(self) -> None:
        from sheep.config.settings import get_settings

        get_settings.cache_clear()

    def teardown_method(self) -> None:
        from sheep.config.settings import get_settings

        get_settings.cache_clear()

    def test_spec_input_valid(self) -> None:
        """A well-formed description passes validation without error."""
        from sheep.models.spec import SpecInput

        spec = SpecInput(user_query="Add dark mode to the settings panel")
        assert spec.user_query == "Add dark mode to the settings panel"

    def test_spec_input_too_short(self) -> None:
        """Input shorter than the minimum character threshold is rejected."""
        import pydantic

        from sheep.models.spec import SpecInput

        with pytest.raises(pydantic.ValidationError):
            SpecInput(user_query="hi")

    def test_spec_input_low_entropy(self) -> None:
        """Input with Shannon entropy below the threshold is rejected (gibberish)."""
        import pydantic

        from sheep.models.spec import SpecInput

        # "gdgdgdgdgdgd" is long enough but has very low entropy (2 chars)
        with pytest.raises(pydantic.ValidationError):
            SpecInput(user_query="gdgdgdgdgdgdgdgdgdgdgd")

    def test_spec_input_error_code_too_short(self) -> None:
        """ValidationError for short input contains '[input_too_short]' error code."""
        import pydantic

        from sheep.models.spec import SpecInput

        with pytest.raises(pydantic.ValidationError) as exc_info:
            SpecInput(user_query="hi")

        error_messages = [e["msg"] for e in exc_info.value.errors()]
        assert any("[input_too_short]" in msg for msg in error_messages)

    def test_spec_input_error_code_low_entropy(self) -> None:
        """ValidationError for low-entropy input contains '[input_low_entropy]' error code."""
        import pydantic

        from sheep.models.spec import SpecInput

        with pytest.raises(pydantic.ValidationError) as exc_info:
            SpecInput(user_query="gdgdgdgdgdgdgdgdgdgdgd")

        error_messages = [e["msg"] for e in exc_info.value.errors()]
        assert any("[input_low_entropy]" in msg for msg in error_messages)

    def test_spec_input_reads_settings_min_chars(self) -> None:
        """Validator reads min_chars from settings — raising the threshold rejects a longer input."""
        import pydantic

        from sheep.models.spec import SpecInput

        with patch.dict(os.environ, {"SHEEP_SPEC_MIN_CHARS": "200"}):
            from sheep.config.settings import get_settings

            get_settings.cache_clear()

            with pytest.raises(pydantic.ValidationError) as exc_info:
                SpecInput(user_query="Add dark mode to the settings panel")

            error_messages = [e["msg"] for e in exc_info.value.errors()]
            assert any("[input_too_short]" in msg for msg in error_messages)

    def test_spec_input_reads_settings_min_entropy(self) -> None:
        """Validator reads min_entropy from settings — raising the threshold rejects a valid input."""
        import pydantic

        from sheep.models.spec import SpecInput

        # A sentence with entropy ~3.x bits — raising threshold above that rejects it
        with patch.dict(os.environ, {"SHEEP_SPEC_MIN_ENTROPY": "99.0"}):
            from sheep.config.settings import get_settings

            get_settings.cache_clear()

            with pytest.raises(pydantic.ValidationError) as exc_info:
                SpecInput(user_query="Add dark mode to the settings panel")

            error_messages = [e["msg"] for e in exc_info.value.errors()]
            assert any("[input_low_entropy]" in msg for msg in error_messages)


# ---------------------------------------------------------------------------
# CLI implement command tests
# ---------------------------------------------------------------------------


class TestImplementCLI:
    """Tests for the implement CLI command's --force flag and validation loop."""

    def setup_method(self) -> None:
        from sheep.config.settings import get_settings

        get_settings.cache_clear()

    def teardown_method(self) -> None:
        from sheep.config.settings import get_settings

        get_settings.cache_clear()

    def _make_mock_result(self) -> "MagicMock":  # type: ignore[name-defined]
        """Return a mock CodeImplementationState for a successful run."""
        from unittest.mock import MagicMock

        mock_result = MagicMock()
        mock_result.final_status = "completed"
        mock_result.branch_name = "test-branch"
        mock_result.working_path = "/tmp/test"
        mock_result.pushed = False
        mock_result.review_iterations = 1
        mock_result.changes_made = "test changes"
        return mock_result

    def test_implement_force_flag_present(self) -> None:
        """--force / --skip-validation flags appear in --help output."""
        from typer.testing import CliRunner

        from sheep.cli import app

        runner = CliRunner()
        result = runner.invoke(app, ["implement", "--help"])
        assert "--force" in result.output
        assert "--skip-validation" in result.output

    def test_implement_rejects_short_issue(self) -> None:
        """Short input (<20 chars) without --force exits with code 1 (non-interactive)."""
        from typer.testing import CliRunner

        from sheep.cli import app

        runner = CliRunner()
        result = runner.invoke(app, ["implement", ".", "--issue", "hi"])
        assert result.exit_code == 1

    def test_implement_rejects_low_entropy_issue(self) -> None:
        """Low-entropy input without --force exits with code 1 (non-interactive)."""
        from typer.testing import CliRunner

        from sheep.cli import app

        runner = CliRunner()
        result = runner.invoke(app, ["implement", ".", "--issue", "gdgdgdgdgdgdgdgdgdgdgd"])
        assert result.exit_code == 1

    def test_implement_error_panel_content(self) -> None:
        """Error panel for short input names the rule '[input_too_short]'."""
        from typer.testing import CliRunner

        from sheep.cli import app

        runner = CliRunner()
        result = runner.invoke(app, ["implement", ".", "--issue", "hi"])
        assert "input_too_short" in result.output

    def test_implement_error_panel_contains_hint(self) -> None:
        """Error panel contains a hint referencing the minimum character count."""
        from typer.testing import CliRunner

        from sheep.cli import app

        runner = CliRunner()
        result = runner.invoke(app, ["implement", ".", "--issue", "hi"])
        assert "20" in result.output

    def test_implement_valid_passes_through(self) -> None:
        """A valid issue string passes validation and reaches run_code_implementation."""
        from unittest.mock import patch
        from typer.testing import CliRunner

        from sheep.cli import app

        runner = CliRunner()
        with patch("sheep.flows.run_code_implementation", return_value=self._make_mock_result()):
            result = runner.invoke(
                app,
                ["implement", ".", "--issue", "Add dark mode to the settings panel"],
            )
        assert result.exit_code == 0

    def test_implement_force_skips_validation(self) -> None:
        """--force skips validation for invalid input and proceeds to implementation."""
        from unittest.mock import patch
        from typer.testing import CliRunner

        from sheep.cli import app

        runner = CliRunner()
        with patch("sheep.flows.run_code_implementation", return_value=self._make_mock_result()):
            result = runner.invoke(
                app,
                ["implement", ".", "--issue", "hi", "--force"],
            )
        assert result.exit_code == 0

    def test_implement_force_logs_structlog_warning(self) -> None:
        """--force emits a structlog WARNING with event name 'validation_skipped'."""
        from unittest.mock import MagicMock, patch
        from typer.testing import CliRunner

        from sheep.cli import app

        mock_logger = MagicMock()
        runner = CliRunner()
        with patch("sheep.flows.run_code_implementation", return_value=self._make_mock_result()):
            with patch("sheep.cli._logger", mock_logger):
                result = runner.invoke(
                    app,
                    ["implement", ".", "--issue", "hi", "--force"],
                )
        assert result.exit_code == 0
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args
        assert call_args.args[0] == "validation_skipped"
        assert call_args.kwargs.get("rule_skipped") == "all"


# ---------------------------------------------------------------------------
# emit_validation_skipped_event tests
# ---------------------------------------------------------------------------


class TestEmitValidationSkippedEvent:
    """Tests for the Langfuse event emitted on forced validation bypass."""

    def test_emits_trace_when_configured(self) -> None:
        """When Langfuse is configured, trace() is called with name='validation_skipped'."""
        from unittest.mock import MagicMock, patch

        from sheep.observability.langfuse_client import emit_validation_skipped_event

        mock_client = MagicMock()
        mock_settings = MagicMock()
        mock_settings.langfuse.is_configured = True

        with patch("sheep.observability.langfuse_client.get_settings", return_value=mock_settings):
            with patch(
                "sheep.observability.langfuse_client.get_client", return_value=mock_client
            ):
                emit_validation_skipped_event(input_length=5)

        mock_client.create_event.assert_called_once()
        call_kwargs = mock_client.create_event.call_args.kwargs
        assert call_kwargs.get("name") == "validation_skipped"
        assert call_kwargs.get("metadata", {}).get("input_length") == 5

    def test_graceful_skip_when_not_configured(self) -> None:
        """When Langfuse is not configured, get_client is never called."""
        from unittest.mock import MagicMock, patch

        from sheep.observability.langfuse_client import emit_validation_skipped_event

        mock_settings = MagicMock()
        mock_settings.langfuse.is_configured = False

        with patch("sheep.observability.langfuse_client.get_settings", return_value=mock_settings):
            with patch(
                "sheep.observability.langfuse_client.get_client"
            ) as mock_get_client:
                emit_validation_skipped_event(input_length=5)

        mock_get_client.assert_not_called()

    def test_graceful_on_langfuse_error(self) -> None:
        """When get_client() raises, no exception propagates out of the function."""
        from unittest.mock import MagicMock, patch

        from sheep.observability.langfuse_client import emit_validation_skipped_event

        mock_settings = MagicMock()
        mock_settings.langfuse.is_configured = True

        with patch("sheep.observability.langfuse_client.get_settings", return_value=mock_settings):
            with patch(
                "sheep.observability.langfuse_client.get_client",
                side_effect=Exception("connection refused"),
            ):
                # Should not raise
                emit_validation_skipped_event(input_length=5)
