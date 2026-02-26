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

    with patch.dict(os.environ, {k: "" for k in env_vars_to_clear}, clear=False):
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


def test_settings_spec_min_chars_default() -> None:
    """Test that spec_min_chars defaults to 20."""
    from sheep.config.settings import get_settings

    get_settings.cache_clear()
    settings = get_settings()
    assert settings.spec_min_chars == 20


def test_settings_spec_min_entropy_default() -> None:
    """Test that spec_min_entropy defaults to 2.5."""
    from sheep.config.settings import get_settings

    get_settings.cache_clear()
    settings = get_settings()
    assert settings.spec_min_entropy == 2.5


def test_settings_spec_min_chars_env_override() -> None:
    """Test that SHEEP_SPEC_MIN_CHARS env var overrides the default."""
    from sheep.config.settings import get_settings

    get_settings.cache_clear()
    with patch.dict(os.environ, {"SHEEP_SPEC_MIN_CHARS": "50"}):
        get_settings.cache_clear()
        settings = get_settings()
        assert settings.spec_min_chars == 50
    get_settings.cache_clear()


def test_settings_spec_min_entropy_env_override() -> None:
    """Test that SHEEP_SPEC_MIN_ENTROPY env var overrides the default."""
    from sheep.config.settings import get_settings

    get_settings.cache_clear()
    with patch.dict(os.environ, {"SHEEP_SPEC_MIN_ENTROPY": "3.0"}):
        get_settings.cache_clear()
        settings = get_settings()
        assert settings.spec_min_entropy == 3.0
    get_settings.cache_clear()
