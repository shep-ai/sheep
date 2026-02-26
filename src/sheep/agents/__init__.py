"""Agent definitions for Sheep."""

from sheep.agents.code_agents import (
    create_code_implementer_agent,
    create_code_researcher_agent,
    create_code_reviewer_agent,
)
from sheep.agents.general_agents import (
    create_chat_agent,
)

__all__ = [
    "create_code_researcher_agent",
    "create_code_implementer_agent",
    "create_code_reviewer_agent",
    "create_chat_agent",
]
