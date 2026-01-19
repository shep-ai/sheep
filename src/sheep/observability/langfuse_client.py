"""Langfuse integration for observability."""

from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Generator, TypeVar

from langfuse import Langfuse

from sheep.config.settings import get_settings
from sheep.observability.logging import get_logger

_langfuse_client: Langfuse | None = None
_logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def init_observability() -> Langfuse | None:
    """
    Initialize observability (Langfuse client).

    Returns:
        Langfuse client if configured, None otherwise.
    """
    global _langfuse_client

    settings = get_settings()

    if not settings.langfuse.is_configured:
        _logger.info("Langfuse not configured, observability disabled")
        return None

    try:
        _langfuse_client = Langfuse(
            public_key=settings.langfuse.public_key.get_secret_value(),
            secret_key=settings.langfuse.secret_key.get_secret_value(),
            host=settings.langfuse.host,
        )
        _logger.info("Langfuse initialized", host=settings.langfuse.host)
        return _langfuse_client
    except Exception as e:
        _logger.warning("Failed to initialize Langfuse", error=str(e))
        return None


def get_langfuse() -> Langfuse | None:
    """Get the Langfuse client instance."""
    return _langfuse_client


@contextmanager
def trace_flow(
    name: str,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
    session_id: str | None = None,
    user_id: str | None = None,
) -> Generator[Any, None, None]:
    """
    Context manager for tracing a flow execution.

    Args:
        name: Name of the flow.
        metadata: Optional metadata to attach to the trace.
        tags: Optional tags for filtering.
        session_id: Optional session ID to group related traces.
        user_id: Optional user ID to track user-specific executions.

    Yields:
        Langfuse trace object if configured, None otherwise.

    Example:
        >>> with trace_flow(
        ...     "code-implementation",
        ...     metadata={"repo": "/path"},
        ...     session_id="user-123-session-456",
        ...     user_id="user-123",
        ... ) as trace:
        ...     # Flow execution here
        ...     pass
    """
    client = get_langfuse()
    if client is None:
        yield None
        return

    trace = client.trace(
        name=name,
        metadata=metadata or {},
        tags=tags or [],
        session_id=session_id,
        user_id=user_id,
    )
    try:
        yield trace
    except Exception as e:
        trace.update(metadata={"error": str(e), "status": "error"})
        raise
    finally:
        client.flush()


@contextmanager
def trace_agent(
    name: str,
    parent_trace: Any = None,
    metadata: dict[str, Any] | None = None,
) -> Generator[Any, None, None]:
    """
    Context manager for tracing an agent execution.

    Args:
        name: Name of the agent.
        parent_trace: Parent trace object for nesting.
        metadata: Optional metadata.

    Yields:
        Langfuse span object if configured, None otherwise.
    """
    client = get_langfuse()
    if client is None or parent_trace is None:
        yield None
        return

    span = parent_trace.span(
        name=f"agent:{name}",
        metadata=metadata or {},
    )
    try:
        yield span
    except Exception as e:
        span.update(metadata={"error": str(e), "status": "error"})
        raise
    finally:
        span.end()


def trace_tool(tool_name: str) -> Callable[[F], F]:
    """
    Decorator to trace tool executions.

    Args:
        tool_name: Name of the tool being traced.

    Returns:
        Decorated function with tracing.
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            client = get_langfuse()
            if client is None:
                return func(*args, **kwargs)

            generation = client.generation(
                name=f"tool:{tool_name}",
                input={"args": str(args), "kwargs": str(kwargs)},
            )
            try:
                result = func(*args, **kwargs)
                generation.end(output=str(result)[:1000])
                return result
            except Exception as e:
                generation.end(metadata={"error": str(e)})
                raise

        return wrapper  # type: ignore

    return decorator
