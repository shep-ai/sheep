"""LLM configuration and factory."""

from crewai import LLM

from sheep.config.settings import Settings, get_settings


def create_llm(
    model: str | None = None,
    temperature: float = 0.7,
    settings: Settings | None = None,
) -> LLM:
    """
    Create an LLM instance with the specified model.

    Args:
        model: Model identifier (e.g., "openai/gpt-4o", "anthropic/claude-3-5-sonnet").
               If None, uses the default model from settings.
        temperature: Sampling temperature (0.0 to 1.0).
        settings: Optional settings instance. Uses global settings if not provided.

    Returns:
        Configured LLM instance.

    Example:
        >>> llm = create_llm("anthropic/claude-3-5-sonnet-20241022", temperature=0.3)
        >>> llm = create_llm()  # Uses default model
    """
    if settings is None:
        settings = get_settings()

    model = model or settings.default_model

    # Build LLM configuration
    llm_config: dict = {
        "model": model,
        "temperature": temperature,
    }

    # Add API keys based on provider
    provider = model.split("/")[0].lower() if "/" in model else "openai"

    if provider == "openai" and settings.llm.openai_api_key:
        llm_config["api_key"] = settings.llm.openai_api_key.get_secret_value()
    elif provider == "anthropic" and settings.llm.anthropic_api_key:
        llm_config["api_key"] = settings.llm.anthropic_api_key.get_secret_value()
    elif provider in ("google", "gemini") and settings.llm.google_api_key:
        llm_config["api_key"] = settings.llm.google_api_key.get_secret_value()
    elif provider == "cursor" and settings.llm.cursor_api_key:
        llm_config["api_key"] = settings.llm.cursor_api_key.get_secret_value()
        llm_config["base_url"] = settings.llm.cursor_api_base

    return LLM(**llm_config)


def get_fast_llm(settings: Settings | None = None) -> LLM:
    """Get LLM configured for fast/cheap operations."""
    if settings is None:
        settings = get_settings()
    return create_llm(model=settings.fast_model, temperature=0.3, settings=settings)


def get_reasoning_llm(settings: Settings | None = None) -> LLM:
    """Get LLM configured for complex reasoning tasks."""
    if settings is None:
        settings = get_settings()
    return create_llm(model=settings.reasoning_model, temperature=0.2, settings=settings)
