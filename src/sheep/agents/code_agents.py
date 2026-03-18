"""Code-related agents for implementation workflows."""

from crewai import LLM, Agent

from sheep.config.llm import get_fast_llm, get_reasoning_llm
from sheep.tools import (
    DirectoryTreeTool,
    FileReadTool,
    FileSearchTool,
    FileWriteTool,
    GitDiffTool,
    GitLogTool,
    GitStatusTool,
)


def create_code_researcher_agent(
    llm: LLM | None = None,
    verbose: bool = False,
) -> Agent:
    """
    Create an agent specialized in researching codebases.

    This agent excels at:
    - Understanding project structure and architecture
    - Finding relevant code sections for a given task
    - Identifying patterns and conventions used in the codebase
    - Tracing code paths and dependencies

    Args:
        llm: Optional LLM instance. Uses fast model by default.
        verbose: Enable verbose output.

    Returns:
        Configured Agent instance.
    """
    if llm is None:
        llm = get_fast_llm()

    return Agent(
        role="Senior Code Researcher",
        goal=(
            "Thoroughly analyze codebases to understand architecture, patterns, "
            "and identify the exact locations and approach needed to implement features or fix bugs."
        ),
        backstory=(
            "You are an expert software architect with decades of experience across "
            "multiple programming languages and paradigms. You have an exceptional ability "
            "to quickly understand unfamiliar codebases, identify design patterns, and "
            "trace code paths. You approach each codebase methodically: first understanding "
            "the overall structure, then diving into relevant areas. You always document "
            "your findings clearly, including file paths and line numbers."
        ),
        llm=llm,
        tools=[
            DirectoryTreeTool(),
            FileReadTool(),
            FileSearchTool(),
            GitLogTool(),
        ],
        verbose=verbose,
        allow_delegation=False,
        max_iter=15,
    )


def create_code_implementer_agent(
    llm: LLM | None = None,
    verbose: bool = False,
) -> Agent:
    """
    Create an agent specialized in implementing code changes.

    This agent excels at:
    - Writing clean, idiomatic code following project conventions
    - Making precise, minimal changes to achieve goals
    - Creating new files when needed
    - Handling edge cases and error conditions

    Args:
        llm: Optional LLM instance. Uses reasoning model by default.
        verbose: Enable verbose output.

    Returns:
        Configured Agent instance.
    """
    if llm is None:
        llm = get_reasoning_llm()

    return Agent(
        role="Senior Software Engineer",
        goal=(
            "Implement code changes precisely and correctly, following the project's "
            "existing patterns and conventions while ensuring code quality and correctness."
        ),
        backstory=(
            "You are a highly skilled software engineer with deep expertise in writing "
            "production-quality code. You take pride in clean, maintainable code that "
            "follows established patterns. You understand that good code changes are "
            "minimal and focused - you make exactly the changes needed, no more, no less. "
            "You always consider edge cases, error handling, and testability. When making "
            "changes, you preserve the existing style and conventions of the codebase."
        ),
        llm=llm,
        tools=[
            FileReadTool(),
            FileWriteTool(),
            FileSearchTool(),
            GitStatusTool(),
            GitDiffTool(),
        ],
        verbose=verbose,
        allow_delegation=False,
        max_iter=20,
    )


def create_code_reviewer_agent(
    llm: LLM | None = None,
    verbose: bool = False,
) -> Agent:
    """
    Create an agent specialized in reviewing code changes.

    This agent excels at:
    - Identifying bugs and potential issues
    - Checking for security vulnerabilities
    - Ensuring code follows project conventions
    - Suggesting improvements

    Args:
        llm: Optional LLM instance. Uses reasoning model by default.
        verbose: Enable verbose output.

    Returns:
        Configured Agent instance.
    """
    if llm is None:
        llm = get_reasoning_llm()

    return Agent(
        role="Senior Code Reviewer",
        goal=(
            "Review code changes thoroughly to ensure correctness, security, "
            "and adherence to best practices and project conventions."
        ),
        backstory=(
            "You are a meticulous code reviewer with extensive experience in identifying "
            "bugs, security vulnerabilities, and code quality issues. You have a keen eye "
            "for detail and can spot subtle issues that others miss. You review code not "
            "just for correctness, but also for maintainability, performance, and security. "
            "Your feedback is always constructive and specific, with concrete suggestions "
            "for improvement."
        ),
        llm=llm,
        tools=[
            FileReadTool(),
            FileSearchTool(),
            GitDiffTool(),
            GitStatusTool(),
        ],
        verbose=verbose,
        allow_delegation=False,
        max_iter=10,
    )
