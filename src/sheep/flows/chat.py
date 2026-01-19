"""Chat Flow - General Q&A with web search and code exploration."""

import uuid
from pathlib import Path
from typing import Any

from crewai import Crew, Task
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel, Field

from sheep.agents import create_chat_agent
from sheep.config.settings import get_settings
from sheep.observability import trace_flow
from sheep.observability.logging import AgentLogger, get_logger

_logger = get_logger(__name__)


class ChatState(BaseModel):
    """State for the chat flow."""

    # Input
    question: str = Field(default="", description="Question to answer")
    context_path: str | None = Field(
        default=None,
        description="Optional path to a codebase or directory for context",
    )

    # Output
    answer: str | None = Field(default=None, description="Answer to the question")
    sources: list[str] = Field(
        default_factory=list,
        description="Sources used to answer the question",
    )
    error: str | None = Field(default=None, description="Error message if any")
    final_status: str = Field(default="pending", description="Final status of the flow")


class ChatFlow(Flow[ChatState]):
    """
    Flow for answering general questions using chat agent.

    The agent has access to:
    - Web search (DuckDuckGo)
    - Web fetch (retrieve content from URLs)
    - File operations (read, search)
    - Git operations (log, status, diff)
    - Shell commands

    Example:
        >>> flow = ChatFlow()
        >>> result = flow.kickoff(
        ...     question="How do I implement OAuth2 in FastAPI?",
        ... )
        >>> print(result.answer)
    """

    def __init__(self, verbose: bool | None = None):
        super().__init__()
        settings = get_settings()
        self.verbose = verbose if verbose is not None else settings.verbose
        self.flow_logger = AgentLogger("chat")

    @start()
    def answer_question(self) -> str:
        """Answer the user's question using the chat agent."""
        self.flow_logger.action("Answering question")

        state = self.state

        # Validate context path if provided
        if state.context_path:
            context_path = Path(state.context_path).resolve()
            if not context_path.exists():
                state.error = f"Context path does not exist: {state.context_path}"
                state.final_status = "error"
                return "error"

        # Create chat agent
        chat_agent = create_chat_agent(verbose=self.verbose)

        # Build task description with optional context
        task_description = f"""
        Answer the following question comprehensively and accurately:

        {state.question}
        """

        if state.context_path:
            task_description += f"""

        You can explore the codebase at: {state.context_path}
        Use file_read, file_search, and directory_tree tools to understand the code.
        """

        task_description += """

        Guidelines:
        1. IMPORTANT: If you know the official documentation URL for the topic, use web_fetch
           to directly retrieve it instead of web_search. For example:
           - Python docs: https://docs.python.org/3/...
           - FastAPI docs: https://fastapi.tiangolo.com/...
           - React docs: https://react.dev/...
        2. Only use web_search when you need to discover new URLs or need multiple perspectives
        3. If web_search is rate-limited, adapt and use web_fetch with known documentation URLs
        4. If a codebase path is provided, explore it to understand implementation details
        5. Cite your sources (URLs, file paths, commands run)
        6. Provide practical examples when applicable
        7. If you're not sure, say so - don't make up information
        8. Structure your answer clearly with sections if needed
        """

        answer_task = Task(
            description=task_description,
            expected_output="""
            A comprehensive answer that includes:
            1. Direct answer to the question
            2. Relevant details and explanation
            3. Practical examples if applicable
            4. Sources cited (URLs, file paths, etc.)
            5. Any caveats or additional considerations
            """,
            agent=chat_agent,
        )

        crew = Crew(
            agents=[chat_agent],
            tasks=[answer_task],
            verbose=self.verbose,
        )

        try:
            # Get Langfuse client
            from sheep.observability.langfuse_client import get_langfuse
            langfuse = get_langfuse()

            # Wrap crew execution with Langfuse span as per official docs
            if langfuse:
                with langfuse.start_as_current_observation(as_type="span", name="chat-crew-execution"):
                    result = crew.kickoff()
            else:
                result = crew.kickoff()

            state.answer = str(result)
            state.final_status = "completed"
            self.flow_logger.result("Question answered successfully")
            return "success"

        except Exception as e:
            state.error = f"Failed to answer question: {e}"
            state.final_status = "error"
            self.flow_logger.error(str(e))
            return "error"


def run_chat(
    question: str,
    context_path: str | None = None,
    verbose: bool = False,
    session_id: str | None = None,
    user_id: str | None = None,
) -> ChatState:
    """
    Run the chat flow to answer a question.

    Args:
        question: Question to answer.
        context_path: Optional path to a codebase or directory for context.
        verbose: Enable verbose output.
        session_id: Optional session ID for grouping related queries.
        user_id: Optional user ID for tracking user-specific queries.

    Returns:
        Final state of the flow execution.

    Example:
        >>> result = run_chat(
        ...     question="How do I implement OAuth2 in FastAPI?",
        ...     session_id="user-session-123",
        ... )
        >>> print(result.answer)
    """
    flow = ChatFlow(verbose=verbose)

    # Generate session_id if not provided
    if session_id is None:
        session_id = f"sheep-chat-{uuid.uuid4().hex[:8]}"

    # Prepare input
    input_data = {
        "question": question,
        "context_path": context_path,
    }

    # Run flow with Langfuse tracing
    with trace_flow(
        "chat",
        metadata={
            "question": question[:100],
            "has_context": context_path is not None,
        },
        session_id=session_id,
        user_id=user_id,
    ):
        # Run the flow - OpenInference will capture detailed traces
        flow.kickoff(inputs=input_data)

    return flow.state
