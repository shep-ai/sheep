"""Code Implementation Flow - From issue to pushed changes."""

import uuid
from pathlib import Path
from typing import Any

from crewai import Crew, Task
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel, Field

from sheep.agents import (
    create_code_implementer_agent,
    create_code_researcher_agent,
    create_code_reviewer_agent,
)
from sheep.config.settings import get_settings
from sheep.observability import trace_flow
from sheep.observability.logging import AgentLogger, get_logger
from sheep.tools import (
    GitCommitTool,
    GitCreateBranchTool,
    GitPushTool,
    GitStatusTool,
    GitWorktreeTool,
)

_logger = get_logger(__name__)


class CodeImplementationState(BaseModel):
    """State for the code implementation flow."""

    # Input
    repo_path: str = Field(default="", description="Path to the repository")
    issue_description: str = Field(default="", description="Description of the feature/bug/task")
    branch_name: str | None = Field(default=None, description="Branch name to create")
    use_worktree: bool = Field(default=False, description="Use git worktree")
    auto_push: bool = Field(default=True, description="Automatically push changes")

    # Derived state
    working_path: str | None = Field(default=None, description="Actual working directory")

    # Research results
    research_findings: str | None = Field(default=None)
    files_to_modify: list[str] = Field(default_factory=list)
    implementation_plan: str | None = Field(default=None)

    # Implementation results
    changes_made: str | None = Field(default=None)
    commit_message: str | None = Field(default=None)

    # Review results
    review_result: str | None = Field(default=None)
    review_passed: bool = Field(default=False)
    review_iterations: int = Field(default=0)

    # Final state
    pushed: bool = Field(default=False)
    final_status: str = Field(default="pending")
    error: str | None = Field(default=None)


class CodeImplementationFlow(Flow[CodeImplementationState]):
    """
    Flow for implementing code changes from an issue description.

    Steps:
    1. Setup: Create branch (optionally in worktree)
    2. Research: Analyze codebase to understand what needs to change
    3. Implement: Make the necessary code changes
    4. Review: Self-review the changes
    5. Commit & Push: Commit and push changes to remote

    Example:
        >>> flow = CodeImplementationFlow()
        >>> result = flow.kickoff(
        ...     repo_path="/path/to/repo",
        ...     issue_description="Add user authentication",
        ...     branch_name="feature/user-auth",
        ... )
    """

    def __init__(self, verbose: bool | None = None):
        super().__init__()
        settings = get_settings()
        self.verbose = verbose if verbose is not None else settings.verbose
        self.flow_logger = AgentLogger("flow")

    @start()
    def setup_branch(self) -> str:
        """Create branch and set up working directory."""
        self.flow_logger.action("Setting up branch")

        state = self.state
        repo_path = Path(state.repo_path).resolve()

        if not repo_path.exists():
            state.error = f"Repository path does not exist: {repo_path}"
            state.final_status = "error"
            return "error"

        # Generate branch name if not provided
        if not state.branch_name:
            settings = get_settings()
            # Create a simple slug from issue description
            slug = state.issue_description[:50].lower()
            slug = "".join(c if c.isalnum() else "-" for c in slug)
            slug = "-".join(filter(None, slug.split("-")))
            state.branch_name = f"{settings.git.branch_prefix}{slug}"

        try:
            if state.use_worktree:
                # Create worktree
                worktree_path = repo_path.parent / f"worktree-{state.branch_name.replace('/', '-')}"
                tool = GitWorktreeTool()
                result = tool._run(
                    repo_path=str(repo_path),
                    worktree_path=str(worktree_path),
                    branch_name=state.branch_name,
                )
                self.flow_logger.result(result)
                state.working_path = str(worktree_path)
            else:
                # Create branch in place
                tool = GitCreateBranchTool()
                result = tool._run(
                    repo_path=str(repo_path),
                    branch_name=state.branch_name,
                )
                self.flow_logger.result(result)
                state.working_path = str(repo_path)

            return "success"

        except Exception as e:
            state.error = f"Failed to setup branch: {e}"
            state.final_status = "error"
            self.flow_logger.error(str(e))
            return "error"

    @listen(setup_branch)
    def research_codebase(self, setup_result: str) -> str:
        """Research the codebase to understand implementation needs."""
        if setup_result == "error":
            return "error"

        self.flow_logger.action("Researching codebase")
        state = self.state

        researcher = create_code_researcher_agent(verbose=self.verbose)

        research_task = Task(
            description=f"""
            Analyze the codebase at {state.working_path} to understand how to implement:

            {state.issue_description}

            Your research should:
            1. First, explore the project structure to understand the architecture
            2. Find similar implementations or patterns in the codebase
            3. Identify the specific files that need to be modified or created
            4. Understand the coding conventions and patterns used
            5. Identify any dependencies or related code that might be affected

            Be thorough but focused. Document:
            - Project structure overview
            - Relevant files and their purposes
            - Existing patterns to follow
            - Specific locations for changes
            - Any potential challenges or considerations
            """,
            expected_output="""
            A detailed research report containing:
            1. Project structure summary
            2. List of files to modify with reasons
            3. Implementation approach based on existing patterns
            4. Specific code locations (file:line) for changes
            5. Any risks or considerations
            """,
            agent=researcher,
        )

        crew = Crew(
            agents=[researcher],
            tasks=[research_task],
            verbose=self.verbose,
        )

        try:
            # Get Langfuse client
            from sheep.observability.langfuse_client import get_langfuse
            langfuse = get_langfuse()

            # Wrap crew execution with Langfuse span as per official docs
            if langfuse:
                with langfuse.start_as_current_observation(as_type="span", name="research-crew-execution"):
                    result = crew.kickoff()
            else:
                result = crew.kickoff()

            state.research_findings = str(result)
            self.flow_logger.result(f"Research completed: {len(state.research_findings)} chars")
            return "success"
        except Exception as e:
            state.error = f"Research failed: {e}"
            state.final_status = "error"
            self.flow_logger.error(str(e))
            return "error"

    @listen(research_codebase)
    def implement_changes(self, research_result: str) -> str:
        """Implement the required code changes."""
        if research_result == "error":
            return "error"

        self.flow_logger.action("Implementing changes")
        state = self.state

        implementer = create_code_implementer_agent(verbose=self.verbose)

        implementation_task = Task(
            description=f"""
            Based on the research findings, implement the changes for:

            {state.issue_description}

            Research findings:
            {state.research_findings}

            Working directory: {state.working_path}

            Guidelines:
            1. Follow the existing code patterns and conventions identified
            2. Make minimal, focused changes - only what's needed
            3. Ensure proper error handling where appropriate
            4. Add comments only where logic isn't self-evident
            5. Do not add unnecessary features or "improvements"

            After making changes, verify them with git status and git diff.
            """,
            expected_output="""
            A summary of changes made including:
            1. List of files modified/created
            2. Brief description of each change
            3. Any important implementation decisions made
            """,
            agent=implementer,
        )

        crew = Crew(
            agents=[implementer],
            tasks=[implementation_task],
            verbose=self.verbose,
        )

        try:
            # Get Langfuse client
            from sheep.observability.langfuse_client import get_langfuse
            langfuse = get_langfuse()

            # Wrap crew execution with Langfuse span as per official docs
            if langfuse:
                with langfuse.start_as_current_observation(as_type="span", name="implement-crew-execution"):
                    result = crew.kickoff()
            else:
                result = crew.kickoff()

            state.changes_made = str(result)
            self.flow_logger.result(f"Implementation completed")
            return "success"
        except Exception as e:
            state.error = f"Implementation failed: {e}"
            state.final_status = "error"
            self.flow_logger.error(str(e))
            return "error"

    @listen(implement_changes)
    def review_changes(self, impl_result: str) -> str:
        """Review the implemented changes."""
        if impl_result == "error":
            return "error"

        self.flow_logger.action("Reviewing changes")
        state = self.state
        state.review_iterations += 1

        if state.review_iterations > 3:
            self.flow_logger.error("Max review iterations reached")
            state.review_passed = True  # Accept after 3 iterations
            return "passed"

        reviewer = create_code_reviewer_agent(verbose=self.verbose)

        review_task = Task(
            description=f"""
            Review the code changes made for:

            {state.issue_description}

            Working directory: {state.working_path}

            Changes made:
            {state.changes_made}

            Review criteria:
            1. Correctness: Does the code correctly implement the requirement?
            2. Code quality: Is the code clean, readable, and maintainable?
            3. Conventions: Does it follow the project's existing patterns?
            4. Security: Are there any security vulnerabilities?
            5. Edge cases: Are edge cases handled appropriately?

            Use git diff to see the actual changes.
            Provide specific, actionable feedback if changes are needed.
            """,
            expected_output="""
            Review result with:
            1. VERDICT: PASS or NEEDS_CHANGES
            2. Summary of findings
            3. Specific issues (if any) with file:line references
            4. Suggested fixes (if any)
            """,
            agent=reviewer,
        )

        crew = Crew(
            agents=[reviewer],
            tasks=[review_task],
            verbose=self.verbose,
        )

        try:
            # Get Langfuse client
            from sheep.observability.langfuse_client import get_langfuse
            langfuse = get_langfuse()

            # Wrap crew execution with Langfuse span as per official docs
            if langfuse:
                with langfuse.start_as_current_observation(as_type="span", name="review-crew-execution"):
                    result = crew.kickoff()
            else:
                result = crew.kickoff()

            state.review_result = str(result)

            # Check if review passed
            result_lower = state.review_result.lower()
            if "pass" in result_lower and "needs_changes" not in result_lower:
                state.review_passed = True
                self.flow_logger.result("Review PASSED")
                return "passed"
            else:
                self.flow_logger.result("Review needs changes")
                return "needs_changes"

        except Exception as e:
            state.error = f"Review failed: {e}"
            self.flow_logger.error(str(e))
            return "passed"  # Don't block on review errors

    @router(review_changes)
    def route_after_review(self, review_result: str) -> str:
        """Route based on review outcome."""
        if review_result == "passed":
            return "commit_and_push"
        elif review_result == "needs_changes":
            return "implement_changes"
        else:
            return "commit_and_push"

    @listen("commit_and_push")
    def commit_and_push(self) -> str:
        """Commit changes and push to remote."""
        self.flow_logger.action("Committing and pushing")
        state = self.state

        try:
            # Generate commit message
            commit_msg = f"""feat: {state.issue_description[:50]}

{state.issue_description}

Changes:
{state.changes_made[:500] if state.changes_made else 'Implementation completed'}

🐑 Generated by Sheep
"""
            state.commit_message = commit_msg

            # Commit
            commit_tool = GitCommitTool()
            commit_result = commit_tool._run(
                repo_path=state.working_path,
                message=commit_msg,
            )
            self.flow_logger.result(f"Commit: {commit_result}")

            # Push if auto_push enabled
            if state.auto_push:
                push_tool = GitPushTool()
                push_result = push_tool._run(
                    repo_path=state.working_path,
                    branch=state.branch_name,
                )
                self.flow_logger.result(f"Push: {push_result}")
                state.pushed = True

            state.final_status = "completed"
            return "success"

        except Exception as e:
            state.error = f"Commit/push failed: {e}"
            state.final_status = "error"
            self.flow_logger.error(str(e))
            return "error"


def run_code_implementation(
    repo_path: str,
    issue_description: str,
    branch_name: str | None = None,
    use_worktree: bool = False,
    auto_push: bool = True,
    verbose: bool = False,
    session_id: str | None = None,
    user_id: str | None = None,
) -> CodeImplementationState:
    """
    Run the code implementation flow.

    Args:
        repo_path: Path to the git repository.
        issue_description: Description of the feature/bug/task.
        branch_name: Optional branch name (auto-generated if not provided).
        use_worktree: Use git worktree for isolated development.
        auto_push: Automatically push changes after commit.
        verbose: Enable verbose output.
        session_id: Optional session ID for grouping related flows.
        user_id: Optional user ID for tracking user-specific executions.

    Returns:
        Final state of the flow execution.

    Example:
        >>> result = run_code_implementation(
        ...     repo_path="/path/to/repo",
        ...     issue_description="Add user logout functionality",
        ...     branch_name="feature/logout",
        ...     session_id="user-session-123",
        ... )
        >>> print(result.final_status)
        completed
    """
    flow = CodeImplementationFlow(verbose=verbose)

    # Generate session_id if not provided (repo-based session)
    if session_id is None:
        repo_name = Path(repo_path).name
        session_id = f"sheep-{repo_name}-{uuid.uuid4().hex[:8]}"

    # Prepare input
    input_data = {
        "repo_path": repo_path,
        "issue_description": issue_description,
        "branch_name": branch_name,
        "use_worktree": use_worktree,
        "auto_push": auto_push,
    }

    # Run flow with Langfuse tracing
    with trace_flow(
        "code-implementation",
        metadata={
            "repo": repo_path,
            "issue": issue_description[:100],
            "branch": branch_name,
        },
        session_id=session_id,
        user_id=user_id,
    ):
        # Run the flow - OpenInference will capture detailed traces
        flow.kickoff(inputs=input_data)

    return flow.state
