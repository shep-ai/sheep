"""Langfuse integration for observability."""

import os
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Generator, TypeVar

from langfuse import get_client

from sheep.config.settings import get_settings
from sheep.observability.logging import get_logger

_langfuse_client: Any = None
_logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def init_observability() -> Any:
    """
    Initialize observability (Langfuse client and OpenInference for automatic tracing).

    Returns:
        Langfuse client if configured, None otherwise.
    """
    global _langfuse_client

    settings = get_settings()

    if not settings.langfuse.is_configured:
        _logger.info("Langfuse not configured, observability disabled")
        return None

    try:
        # Set environment variables for Langfuse
        os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse.public_key.get_secret_value()
        os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse.secret_key.get_secret_value()
        os.environ["LANGFUSE_BASE_URL"] = settings.langfuse.host

        # Initialize Langfuse client using get_client() as per official docs
        _langfuse_client = get_client()

        # Verify authentication
        if _langfuse_client.auth_check():
            _logger.info("Langfuse client authenticated and ready", host=settings.langfuse.host)
        else:
            _logger.warning("Langfuse authentication failed")
            return None

        # Initialize OpenInference for automatic CrewAI tracing (if enabled)
        if settings.langfuse.openlit_enabled:
            try:
                from openinference.instrumentation.crewai import CrewAIInstrumentor

                # Initialize the CrewAI instrumentor
                # This automatically captures all CrewAI operations including:
                # - Agent iterations
                # - Tool calls
                # - LLM generations
                # - Task executions
                CrewAIInstrumentor().instrument(skip_dep_check=True)

                _logger.info(
                    "OpenInference CrewAI instrumentation enabled - "
                    "detailed traces will appear in Langfuse"
                )
            except ImportError:
                _logger.warning(
                    "OpenInference CrewAI instrumentation not installed.\n"
                    "Install with: pip install openinference-instrumentation-crewai\n"
                    "Or run: pip install -e . to install all dependencies.\n"
                    "Automatic CrewAI tracing will not be available."
                )
            except Exception as e:
                _logger.warning("Failed to initialize OpenInference", error=str(e))
        else:
            _logger.info(
                "OpenInference tracing disabled (set LANGFUSE_OPENLIT_ENABLED=true to enable detailed tracing)"
            )

        return _langfuse_client
    except Exception as e:
        _logger.warning("Failed to initialize Langfuse", error=str(e))
        return None


def get_langfuse() -> Any:
    """Get the Langfuse client instance."""
    return _langfuse_client


class FlowTracer:
    """Helper class to capture flow input/output for tracing."""

    def __init__(self, trace: Any):
        self.trace = trace
        self.input_data: dict[str, Any] | None = None
        self.output_data: Any | None = None

    def set_input(self, input_data: dict[str, Any]) -> None:
        """Set the input data for the trace."""
        self.input_data = input_data
        if self.trace:
            self.trace.update(input=input_data)

    def set_output(self, output_data: Any) -> None:
        """Set the output data for the trace."""
        self.output_data = output_data
        if self.trace:
            # Convert output to dict if it's a Pydantic model
            if hasattr(output_data, "model_dump"):
                output_dict = output_data.model_dump()
            else:
                output_dict = str(output_data)
            self.trace.update(output=output_dict)


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
        Langfuse span object, or None if Langfuse not configured.

    Example:
        >>> with trace_flow(
        ...     "code-implementation",
        ...     metadata={"repo": "/path"},
        ...     session_id="user-123-session-456",
        ...     user_id="user-123",
        ... ) as span:
        ...     # Your flow execution
        ...     pass
    """
    client = get_langfuse()
    if client is None:
        yield None
        return

    # Build attributes
    attributes = metadata or {}
    if session_id:
        attributes["session_id"] = session_id
    if user_id:
        attributes["user_id"] = user_id
    if tags:
        attributes["tags"] = tags

    # Use start_as_current_observation as per Langfuse v3 API
    with client.start_as_current_observation(as_type="span", name=name, metadata=attributes) as span:
        try:
            yield span
        except Exception as e:
            if span:
                span.update(metadata={**attributes, "error": str(e), "status": "error"})
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
