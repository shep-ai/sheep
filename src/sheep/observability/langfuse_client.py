"""Langfuse integration for observability."""

import base64
import os
from typing import Any

from langfuse import get_client

from sheep.config.settings import get_settings
from sheep.observability.logging import get_logger

_instrumented = False
_logger = get_logger(__name__)


def init_observability() -> None:
    """
    Initialize Langfuse observability following official CrewAI integration guide.

    See: https://langfuse.com/integrations/frameworks/crewai
    """
    global _instrumented

    # Only instrument once
    if _instrumented:
        return

    settings = get_settings()

    if not settings.langfuse.is_configured:
        _logger.info("Langfuse not configured, observability disabled")
        return

    # Optional: Verify authentication
    try:
        os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse.public_key.get_secret_value()
        os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse.secret_key.get_secret_value()
        os.environ["LANGFUSE_BASE_URL"] = settings.langfuse.host

        client = get_client()
        if not client.auth_check():
            _logger.warning("Langfuse authentication failed")
            return

        _logger.info("Langfuse authenticated", host=settings.langfuse.host)
    except Exception as e:
        _logger.warning("Failed to authenticate with Langfuse", error=str(e))
        return

    # Enable OpenInference CrewAI instrumentation if configured
    if not settings.langfuse.openlit_enabled:
        _logger.info("OpenInference tracing disabled (set LANGFUSE_OPENLIT_ENABLED=true to enable)")
        return

    try:
        from openinference.instrumentation.crewai import CrewAIInstrumentor

        # Configure OTLP endpoint with Basic Auth
        endpoint = f"{settings.langfuse.host}/api/public/otel/v1/traces"
        credentials = f"{settings.langfuse.public_key.get_secret_value()}:{settings.langfuse.secret_key.get_secret_value()}"
        auth_string = base64.b64encode(credentials.encode()).decode()

        # Set OTLP environment variables (official method)
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = endpoint
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_string}"
        os.environ["OTEL_TRACES_EXPORTER"] = "otlp"
        os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"
        os.environ["OTEL_SERVICE_NAME"] = "sheep-agents"

        # Set resource attributes including default model
        os.environ["OTEL_RESOURCE_ATTRIBUTES"] = (
            f"service.name=sheep-agents,"
            f"deployment.environment=local,"
            f"gen_ai.request.model={settings.default_model},"
            f"llm.model={settings.default_model}"
        )

        # Instrument CrewAI - this is all we need!
        CrewAIInstrumentor().instrument(skip_dep_check=True)

        _instrumented = True
        _logger.info("OpenInference CrewAI instrumentation enabled", endpoint=endpoint)

    except ImportError as e:
        _logger.warning(
            f"OpenInference not installed: {e.name}\n"
            "Install with: pip install openinference-instrumentation-crewai"
        )
    except Exception as e:
        _logger.warning("Failed to initialize OpenInference", error=str(e))


