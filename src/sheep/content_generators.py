"""Content generation utilities for creating markdown and other content."""

from sheep.config.llm import get_reasoning_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Prompt template for markdown generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following structure:
1. An H1 heading (using #) with a title about any topic you choose
2. A blank line
3. Exactly 2-3 sentences of coherent prose about that topic

Return ONLY the markdown content, no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""


def generate_markdown_content() -> str:
    """
    Generate markdown content with an H1 heading and 2-3 sentences of prose.

    Uses Claude API via CrewAI LLM framework to generate coherent,
    contextually-appropriate prose about any topic.

    Returns:
        String containing valid markdown with H1 heading and prose content.

    Raises:
        ValueError: If generated content doesn't meet format requirements.
        Exception: If LLM API call fails.
    """
    llm = get_reasoning_llm()
    _logger.info("Generating markdown content with reasoning LLM")

    try:
        # Call LLM with the prompt
        response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

        # Extract the response text
        if isinstance(response, dict):
            content = response.get("content", str(response))
        else:
            content = str(response)

        _logger.debug(f"Raw LLM response: {content[:100]}...")

        # Ensure trailing newline (Unix convention)
        if not content.endswith("\n"):
            content = content + "\n"

        # Validate the response format
        _validate_markdown_content(content)

        _logger.info("Markdown content generated successfully")
        return content

    except Exception as e:
        _logger.error(f"Failed to generate markdown content: {e}")
        raise


def _validate_markdown_content(content: str) -> None:
    """
    Validate that generated content meets markdown format requirements.

    Args:
        content: The generated markdown content to validate.

    Raises:
        ValueError: If content doesn't meet format requirements.
    """
    # Check that content is not empty
    if not content or not content.strip():
        raise ValueError("Generated content is empty")

    # Check for H1 heading
    if not content.lstrip().startswith("# "):
        raise ValueError("Content must start with H1 heading (# )")

    # Check that content has reasonable length
    if len(content) < 50:
        raise ValueError("Generated content is too short to be meaningful")

    # Check for sentence structure (count periods)
    sentence_count = content.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"Content should have 2-3 sentences, found {sentence_count}"
        )
