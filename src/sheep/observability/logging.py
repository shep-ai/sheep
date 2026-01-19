"""Structured logging configuration."""

import logging
import sys
from typing import Any

import structlog
from rich.console import Console

from sheep.config.settings import get_settings

_console = Console()


def setup_logging(log_level: str | None = None) -> None:
    """
    Configure structured logging for the application.

    Args:
        log_level: Optional override for log level. Uses settings if not provided.
    """
    settings = get_settings()
    level = log_level or settings.log_level

    # Convert log level string to logging level constant
    log_level_int = getattr(logging, level.upper(), logging.INFO)

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(colors=True),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level_int),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (typically module name).

    Returns:
        Configured structlog logger.
    """
    return structlog.get_logger(name)


class AgentLogger:
    """Logger wrapper for agent execution with rich output."""

    def __init__(self, agent_name: str, flow_id: str | None = None):
        self.agent_name = agent_name
        self.flow_id = flow_id
        self._logger = get_logger(f"agent.{agent_name}")

    def thinking(self, message: str, **kwargs: Any) -> None:
        """Log agent thinking/reasoning."""
        _console.print(f"[dim cyan][{self.agent_name}][/dim cyan] [dim]{message}[/dim]")
        self._logger.debug("thinking", message=message, **kwargs)

    def action(self, action: str, **kwargs: Any) -> None:
        """Log agent action."""
        _console.print(f"[cyan][{self.agent_name}][/cyan] [bold]{action}[/bold]")
        self._logger.info("action", action=action, **kwargs)

    def tool_call(self, tool: str, **kwargs: Any) -> None:
        """Log tool invocation."""
        _console.print(f"[cyan][{self.agent_name}][/cyan] [yellow]Tool:[/yellow] {tool}")
        self._logger.info("tool_call", tool=tool, **kwargs)

    def result(self, result: str, **kwargs: Any) -> None:
        """Log agent result."""
        _console.print(f"[cyan][{self.agent_name}][/cyan] [green]Result:[/green] {result[:200]}...")
        self._logger.info("result", result=result[:500], **kwargs)

    def error(self, error: str, **kwargs: Any) -> None:
        """Log agent error."""
        _console.print(f"[cyan][{self.agent_name}][/cyan] [red]Error:[/red] {error}")
        self._logger.error("error", error=error, **kwargs)
