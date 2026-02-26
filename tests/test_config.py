"""Tests for configuration module."""

import os
from unittest.mock import patch


def test_settings_defaults():
    """Test that settings have sensible defaults."""
    # Clear any existing environment variables that might affect the test
    env_vars_to_clear = [
        "SHEEP_DEFAULT_MODEL",
        "SHEEP_FAST_MODEL",
        "SHEEP_REASONING_MODEL",
        "SHEEP_LOG_LEVEL",
    ]

    with patch.dict(os.environ, dict.fromkeys(env_vars_to_clear, ""), clear=False):
        # Need to clear the lru_cache to get fresh settings
        from sheep.config.settings import get_settings

        get_settings.cache_clear()
        settings = get_settings()

        assert settings.default_model == "openai/gpt-4o"
        assert settings.fast_model == "openai/gpt-4o-mini"
        assert settings.log_level == "INFO"
        assert settings.max_iterations == 25


def test_llm_settings_providers():
    """Test that LLM settings correctly identify available providers."""
    from sheep.config.settings import LLMSettings

    # No providers configured
    settings = LLMSettings()
    assert settings.get_available_providers() == []


def test_langfuse_settings_configured():
    """Test Langfuse configuration detection."""
    from sheep.config.settings import LangfuseSettings

    # Not configured
    settings = LangfuseSettings()
    assert not settings.is_configured

    # Partially configured
    settings = LangfuseSettings(public_key="pk-test")  # type: ignore
    assert not settings.is_configured
