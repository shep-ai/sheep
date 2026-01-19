# Sheep

An agentic platform for automated code implementation using CrewAI.

## Overview

Sheep is a modular, observable agentic platform that automates software development tasks. Given a repository and a task description, Sheep will:

1. **Create a branch** - Set up an isolated workspace (optionally using git worktrees)
2. **Research** - Analyze the codebase to understand architecture and patterns
3. **Implement** - Make the necessary code changes following existing conventions
4. **Review** - Self-review changes for quality and correctness
5. **Push** - Commit and push changes to the remote repository

## Features

- **Multi-LLM Support** - Works with OpenAI, Anthropic (Claude), Google (Gemini), and Cursor API
- **Observable Execution** - Full tracing via Langfuse with execution graphs, metrics, and logs
- **Modular Architecture** - Separation of flows (structure) and crews (intelligence)
- **Git Integration** - Full git support including worktrees for parallel development
- **Extensible** - Easy to add new agents, tools, and flows

## Installation

```bash
# Clone the repository
git clone <repo-url> sheep
cd sheep

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:

```bash
# Required: At least one LLM provider
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...
# or
GOOGLE_API_KEY=...

# Optional: Observability with Langfuse
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
```

3. Verify configuration:

```bash
sheep config
```

## Usage

### CLI

```bash
# Basic usage - implement a feature
sheep implement /path/to/repo -i "Add user authentication with JWT tokens"

# Specify branch name
sheep implement /path/to/repo -i "Fix login bug" -b "fix/login-bug"

# Use worktree for isolated development
sheep implement /path/to/repo -i "Refactor database layer" --worktree

# Don't auto-push (just commit locally)
sheep implement /path/to/repo -i "Add tests" --no-push

# Verbose output
sheep implement /path/to/repo -i "Add feature" -V
```

### Python API

```python
from sheep.flows import run_code_implementation

result = run_code_implementation(
    repo_path="/path/to/repo",
    issue_description="Add user logout functionality",
    branch_name="feature/logout",
    use_worktree=False,
    auto_push=True,
    verbose=True,
)

print(f"Status: {result.final_status}")
print(f"Branch: {result.branch_name}")
print(f"Changes: {result.changes_made}")
```

## Architecture

```
sheep/
├── src/sheep/
│   ├── agents/          # Agent definitions
│   │   └── code_agents.py   # Research, Implementation, Review agents
│   ├── config/          # Configuration management
│   │   ├── settings.py      # Pydantic settings
│   │   └── llm.py           # LLM factory
│   ├── flows/           # Flow definitions (orchestration)
│   │   └── code_implementation.py  # Main implementation flow
│   ├── observability/   # Logging and tracing
│   │   ├── logging.py       # Structured logging
│   │   └── langfuse_client.py  # Langfuse integration
│   ├── tools/           # Agent tools
│   │   ├── git_tools.py     # Git operations
│   │   └── file_tools.py    # File operations
│   └── cli.py           # CLI entry point
```

### Design Principles

1. **Separation of Structure and Intelligence**
   - Flows define the execution structure and control paths
   - Crews provide autonomous AI decision-making
   - Each crew is a specialized unit invoked at specific flow steps

2. **Task-First Design**
   - 80% of effort goes into well-designed tasks
   - 20% into agent configuration
   - Well-crafted tasks elevate agent performance

3. **Specialized Agents**
   - Each agent has a focused role and expertise
   - Clear roles, goals, and backstories
   - Complementary skills for collaboration

## Observability

Sheep integrates with [Langfuse](https://langfuse.com) for comprehensive observability:

- **Execution Traces** - Full trace of agent decisions and actions
- **Metrics** - Token usage, latency, cost tracking
- **Execution Graphs** - Visual representation of flow execution
- **Error Tracking** - Detailed error context and stack traces

### Setting up Langfuse

1. Create a free account at [cloud.langfuse.com](https://cloud.langfuse.com)
2. Create a project and get your API keys
3. Add keys to `.env`:

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Adding New Flows

Create a new flow by extending the base Flow class:

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class MyFlowState(BaseModel):
    input_data: str
    result: str | None = None

class MyFlow(Flow[MyFlowState]):
    @start()
    def step_one(self) -> str:
        # First step logic
        return "continue"

    @listen(step_one)
    def step_two(self, prev_result: str) -> str:
        # Second step logic
        self.state.result = "Done!"
        return "complete"
```

## Adding New Agents

Create specialized agents for your use case:

```python
from crewai import Agent
from sheep.config.llm import get_reasoning_llm

def create_my_agent(verbose: bool = False) -> Agent:
    return Agent(
        role="My Specialist",
        goal="Accomplish specific tasks",
        backstory="Expert in domain X with years of experience...",
        llm=get_reasoning_llm(),
        tools=[...],
        verbose=verbose,
    )
```

## Model Configuration

Configure which models to use for different tasks:

```bash
# .env

# Default model for general tasks
SHEEP_DEFAULT_MODEL=openai/gpt-4o

# Fast model for research and simple tasks
SHEEP_FAST_MODEL=openai/gpt-4o-mini

# Reasoning model for complex implementation
SHEEP_REASONING_MODEL=anthropic/claude-3-5-sonnet-20241022
```

Supported model formats:
- OpenAI: `openai/gpt-4o`, `openai/gpt-4o-mini`
- Anthropic: `anthropic/claude-3-5-sonnet-20241022`, `anthropic/claude-3-opus`
- Google: `gemini/gemini-2.0-flash`, `gemini/gemini-1.5-pro`

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/

# Run type checking
mypy src/
```

## Roadmap

- [ ] Web UI for execution monitoring
- [ ] Support for more observability platforms (DataDog, OpenLIT)
- [ ] Parallel agent execution with thread pools
- [ ] Integration with issue trackers (GitHub, Jira)
- [ ] Custom tool marketplace
- [ ] Multi-repo support

## License

MIT
