"""Application settings using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """LLM provider configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # OpenAI
    openai_api_key: SecretStr | None = Field(default=None, alias="OPENAI_API_KEY")

    # Anthropic
    anthropic_api_key: SecretStr | None = Field(default=None, alias="ANTHROPIC_API_KEY")

    # Google
    google_api_key: SecretStr | None = Field(default=None, alias="GOOGLE_API_KEY")

    # Cursor
    cursor_api_key: SecretStr | None = Field(default=None, alias="CURSOR_API_KEY")
    cursor_api_base: str = Field(default="https://api.cursor.sh/v1", alias="CURSOR_API_BASE")

    def get_available_providers(self) -> list[str]:
        """Return list of configured providers."""
        providers = []
        if self.openai_api_key:
            providers.append("openai")
        if self.anthropic_api_key:
            providers.append("anthropic")
        if self.google_api_key:
            providers.append("google")
        if self.cursor_api_key:
            providers.append("cursor")
        return providers


class LangfuseSettings(BaseSettings):
    """Langfuse observability configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    public_key: SecretStr | None = Field(default=None, alias="LANGFUSE_PUBLIC_KEY")
    secret_key: SecretStr | None = Field(default=None, alias="LANGFUSE_SECRET_KEY")
    # Support both LANGFUSE_BASE_URL (official) and LANGFUSE_HOST (legacy)
    host: str = Field(
        default="https://cloud.langfuse.com",
        validation_alias="LANGFUSE_BASE_URL",
        alias="LANGFUSE_HOST",
    )
    enabled: bool = Field(default=True, alias="LANGFUSE_ENABLED")
    # Control OpenInference tracing
    openlit_enabled: bool = Field(default=False, alias="LANGFUSE_OPENLIT_ENABLED")

    @property
    def is_configured(self) -> bool:
        """Check if Langfuse is properly configured."""
        return bool(self.public_key and self.secret_key and self.enabled)


class GitSettings(BaseSettings):
    """Git configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    remote: str = Field(default="origin", alias="SHEEP_GIT_REMOTE")
    branch_prefix: str = Field(default="sheep/", alias="SHEEP_BRANCH_PREFIX")


class Settings(BaseSettings):
    """Main application settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Model configuration
    default_model: str = Field(default="openai/gpt-4o", alias="SHEEP_DEFAULT_MODEL")
    fast_model: str = Field(default="openai/gpt-4o-mini", alias="SHEEP_FAST_MODEL")
    reasoning_model: str = Field(
        default="anthropic/claude-3-5-sonnet-20241022", alias="SHEEP_REASONING_MODEL"
    )

    # Execution settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", alias="SHEEP_LOG_LEVEL"
    )
    verbose: bool = Field(default=False, alias="SHEEP_VERBOSE")
    max_iterations: int = Field(default=25, alias="SHEEP_MAX_ITERATIONS")

    # Sub-configurations
    llm: LLMSettings = Field(default_factory=LLMSettings)
    langfuse: LangfuseSettings = Field(default_factory=LangfuseSettings)
    git: GitSettings = Field(default_factory=GitSettings)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
