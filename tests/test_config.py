"""Tests for configuration module."""

import os
from unittest.mock import patch

import pytest


def test_settings_defaults():
    """Test that settings have sensible defaults."""
    # Clear any existing environment variables that might affect the test
    env_vars_to_clear = [
        "SHEEP_DEFAULT_MODEL",
        "SHEEP_FAST_MODEL",
        "SHEEP_REASONING_MODEL",
        "SHEEP_LOG_LEVEL",
    ]

    with patch.dict(os.environ, {}, clear=False):
        for k in env_vars_to_clear:
            os.environ.pop(k, None)
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

    api_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "CURSOR_API_KEY"]
    # No providers configured
    with patch.dict(os.environ, {}, clear=False):
        for k in api_keys:
            os.environ.pop(k, None)
        settings = LLMSettings()
    assert settings.get_available_providers() == []


def test_langfuse_settings_configured():
    """Test Langfuse configuration detection."""
    from sheep.config.settings import LangfuseSettings

    langfuse_keys = ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_BASE_URL", "LANGFUSE_HOST"]
    with patch.dict(os.environ, {}, clear=False):
        for k in langfuse_keys:
            os.environ.pop(k, None)
        # Not configured
        settings = LangfuseSettings()
        assert not settings.is_configured

        # Partially configured
        settings = LangfuseSettings(public_key="pk-test")  # type: ignore
        assert not settings.is_configured
