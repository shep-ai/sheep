"""General-purpose agents for Q&A and chat workflows."""

from crewai import LLM, Agent

from sheep.config.llm import get_reasoning_llm
from sheep.tools import (
    DirectoryTreeTool,
    FileReadTool,
    FileSearchTool,
    GitDiffTool,
    GitLogTool,
    GitStatusTool,
    ShellCommandTool,
    WebFetchTool,
    WebSearchTool,
)


def create_chat_agent(
    llm: LLM | None = None,
    verbose: bool = False,
) -> Agent:
    """
    Create an agent specialized in answering general questions.

    This agent excels at:
    - Answering questions about code, technology, and best practices
    - Searching the web for up-to-date information
    - Exploring codebases to understand implementation details
    - Running commands to gather information
    - Providing detailed, accurate answers with sources

    Args:
        llm: Optional LLM instance. Uses reasoning model by default.
        verbose: Enable verbose output.

    Returns:
        Configured Agent instance.
    """
    if llm is None:
        llm = get_reasoning_llm()

    return Agent(
        role="Senior Software Engineer & Technical Advisor",
        goal=(
            "Provide accurate, helpful answers to technical questions by leveraging "
            "code exploration, web search, and command-line tools. Always cite sources "
            "and provide practical, actionable information."
        ),
        backstory=(
            "You are an experienced software engineer and technical advisor with deep "
            "expertise across multiple domains. You excel at finding information quickly, "
            "whether it's in codebases, documentation, or online resources. You have a "
            "methodical approach: first understanding the question, then gathering relevant "
            "information using all available tools, and finally synthesizing it into a clear, "
            "comprehensive answer. You always cite your sources and prefer showing practical "
            "examples. When exploring code, you start with high-level structure and drill "
            "down as needed. When searching the web, you are smart about it: if you know "
            "the official documentation URL for a topic, you use web_fetch to directly "
            "retrieve it instead of searching. For example, for Python asyncio questions, "
            "you fetch https://docs.python.org/3/library/asyncio.html directly. You only "
            "use web_search when you need to discover new URLs or get multiple perspectives. "
            "If web_search is rate-limited, you adapt and use your knowledge to provide "
            "accurate answers based on well-known documentation sources."
        ),
        llm=llm,
        tools=[
            # Code exploration tools
            DirectoryTreeTool(),
            FileReadTool(),
            FileSearchTool(),
            # Git tools for understanding history
            GitLogTool(),
            GitStatusTool(),
            GitDiffTool(),
            # Web tools for research
            WebSearchTool(),
            WebFetchTool(),
            # Shell for running commands
            ShellCommandTool(),
        ],
        verbose=verbose,
        allow_delegation=False,
        max_iter=25,
    )
