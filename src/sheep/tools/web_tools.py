"""Web operation tools for agents."""

import httpx
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


class WebFetchInput(BaseModel):
    """Input for fetching web content."""

    url: str = Field(description="URL to fetch content from")


class WebFetchTool(BaseTool):
    """Fetch content from a web URL."""

    name: str = "web_fetch"
    description: str = (
        "Fetch content from a web URL. Returns the HTML content of the page. "
        "Use this to retrieve documentation, articles, or any web content."
    )
    args_schema: type[BaseModel] = WebFetchInput

    def _run(self, url: str) -> str:
        try:
            # Add timeout and follow redirects
            with httpx.Client(timeout=30.0, follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()

                # Limit output size to avoid overwhelming the agent
                content = response.text
                if len(content) > 100000:
                    content = content[:100000] + "\n... (content truncated)"

                return f"Successfully fetched content from {url}\n\nContent:\n{content}"

        except httpx.HTTPStatusError as e:
            return f"HTTP error occurred: {e.response.status_code} - {e}"
        except httpx.RequestError as e:
            return f"Request error occurred: {e}"
        except Exception as e:
            return f"Error fetching URL: {e}"


class WebSearchInput(BaseModel):
    """Input for web search."""

    query: str = Field(description="Search query to look up")
    max_results: int = Field(
        default=5,
        description="Maximum number of results to return (1-10)",
        ge=1,
        le=10,
    )


class WebSearchTool(BaseTool):
    """Search the web using DuckDuckGo."""

    name: str = "web_search"
    description: str = (
        "Search the web for information using DuckDuckGo. "
        "Returns a list of search results with titles, URLs, and snippets. "
        "Use this to find up-to-date information, documentation, or answers to questions. "
        "Note: If you get a rate limit error, try using web_fetch to directly access "
        "known documentation URLs instead."
    )
    args_schema: type[BaseModel] = WebSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        try:
            import time

            from duckduckgo_search import DDGS

            results = []

            # Retry logic for rate limiting
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Try with increased timeout and proxy settings
                    with DDGS(timeout=20, proxies=None) as ddgs:
                        # Use the text search
                        search_results = list(
                            ddgs.text(
                                query,
                                max_results=max_results,
                            )
                        )

                        for i, result in enumerate(search_results, 1):
                            title = result.get("title", "No title")
                            url = result.get("href", "No URL")
                            snippet = result.get("body", "No description")

                            results.append(f"{i}. **{title}**\n   URL: {url}\n   {snippet}\n")

                    # If we got results, break out of retry loop
                    if results:
                        break

                except Exception as e:
                    error_str = str(e).lower()
                    # Check if it's a rate limit error
                    if "ratelimit" in error_str or "202" in error_str or "429" in error_str:
                        if attempt < max_retries - 1:
                            # Wait before retrying (exponential backoff)
                            wait_time = (attempt + 1) * 3
                            _logger.warning(
                                f"Rate limit hit, waiting {wait_time}s before retry {attempt + 2}/{max_retries}"
                            )
                            time.sleep(wait_time)
                            continue
                        else:
                            return (
                                f"Web search rate limited after {max_retries} attempts. "
                                f"Please try again in a few moments, "
                                f"or use the web_fetch tool to directly access known documentation URLs. "
                                f"For example: web_fetch('https://docs.python.org/...')"
                            )
                    else:
                        # Non-rate-limit error, raise it
                        raise

            if not results:
                return (
                    f"No search results found for: {query}\n\n"
                    f"Tip: If you know the URL of relevant documentation, "
                    f"use the web_fetch tool to retrieve it directly."
                )

            return f"Search results for '{query}':\n\n" + "\n".join(results)

        except ImportError:
            return (
                "Error: duckduckgo-search package not installed. "
                "Install with: pip install duckduckgo-search"
            )
        except Exception as e:
            return (
                f"Error performing web search: {e}\n\n"
                f"Tip: Try using web_fetch to directly access documentation URLs instead, "
                f"for example: web_fetch('https://docs.python.org/3/library/asyncio.html')"
            )


class ShellCommandInput(BaseModel):
    """Input for running shell commands."""

    command: str = Field(description="Shell command to execute")
    working_dir: str | None = Field(
        default=None,
        description="Working directory for the command (defaults to current directory)",
    )


class ShellCommandTool(BaseTool):
    """Execute shell commands safely."""

    name: str = "shell_command"
    description: str = (
        "Execute shell commands safely. Use this for CLI operations, "
        "running build commands, testing, etc. "
        "Commands are executed in a subprocess with a timeout."
    )
    args_schema: type[BaseModel] = ShellCommandInput

    def _run(self, command: str, working_dir: str | None = None) -> str:
        import subprocess
        from pathlib import Path

        try:
            # Validate working directory
            cwd = None
            if working_dir:
                cwd = Path(working_dir)
                if not cwd.exists():
                    return f"Error: Working directory does not exist: {working_dir}"

            # Execute command with timeout
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=cwd,
            )

            output = []
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")

            output.append(f"\nReturn code: {result.returncode}")

            return "\n\n".join(output)

        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after 5 minutes: {command}"
        except Exception as e:
            return f"Error executing command: {e}"
