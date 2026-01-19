"""Sheep CLI - Command line interface for the agentic platform."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from sheep import __version__
from sheep.config.settings import get_settings
from sheep.observability import init_observability, setup_logging

app = typer.Typer(
    name="sheep",
    help="🐑 Sheep - An agentic platform for automated code implementation",
    add_completion=False,
)

console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"[bold]Sheep[/bold] version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Sheep - An agentic platform for automated code implementation."""
    setup_logging()
    init_observability()


@app.command()
def implement(
    repo_path: Path = typer.Argument(
        ...,
        help="Path to the git repository",
        exists=True,
        dir_okay=True,
        file_okay=False,
    ),
    issue: str = typer.Option(
        ...,
        "--issue",
        "-i",
        help="Description of the feature, bug, or task to implement",
    ),
    branch: Optional[str] = typer.Option(
        None,
        "--branch",
        "-b",
        help="Branch name to create (auto-generated if not provided)",
    ),
    worktree: bool = typer.Option(
        False,
        "--worktree",
        "-w",
        help="Use git worktree for isolated development",
    ),
    no_push: bool = typer.Option(
        False,
        "--no-push",
        help="Don't push changes after commit",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-V",
        help="Enable verbose output",
    ),
) -> None:
    """
    Implement a feature, fix a bug, or complete a task.

    This command will:
    1. Create a new branch (optionally in a worktree)
    2. Research the codebase to understand the implementation needs
    3. Implement the required changes
    4. Review the changes for quality
    5. Commit and push the changes

    Example:
        sheep implement /path/to/repo -i "Add user authentication"
        sheep implement . -i "Fix login bug" -b "fix/login-bug" --no-push
    """
    from sheep.flows import run_code_implementation

    console.print(
        Panel(
            f"[bold]Issue:[/bold] {issue}\n"
            f"[bold]Repository:[/bold] {repo_path.resolve()}\n"
            f"[bold]Branch:[/bold] {branch or '(auto-generated)'}\n"
            f"[bold]Worktree:[/bold] {worktree}\n"
            f"[bold]Auto-push:[/bold] {not no_push}",
            title="🐑 Sheep - Code Implementation",
            expand=False,
        )
    )

    result = run_code_implementation(
        repo_path=str(repo_path.resolve()),
        issue_description=issue,
        branch_name=branch,
        use_worktree=worktree,
        auto_push=not no_push,
        verbose=verbose,
    )

    # Display results
    if result.final_status == "completed":
        console.print("\n[bold green]✓ Implementation completed successfully![/bold green]\n")

        table = Table(title="Summary")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Branch", result.branch_name or "N/A")
        table.add_row("Working Path", result.working_path or "N/A")
        table.add_row("Pushed", "Yes" if result.pushed else "No")
        table.add_row("Review Iterations", str(result.review_iterations))

        console.print(table)

        if result.changes_made:
            console.print("\n[bold]Changes Made:[/bold]")
            console.print(result.changes_made[:1000])

    else:
        console.print(f"\n[bold red]✗ Implementation failed: {result.error}[/bold red]")
        raise typer.Exit(1)


@app.command()
def config() -> None:
    """Show current configuration and available LLM providers."""
    settings = get_settings()

    console.print(Panel("[bold]Sheep Configuration[/bold]", expand=False))

    # LLM Providers
    providers_table = Table(title="LLM Providers")
    providers_table.add_column("Provider", style="cyan")
    providers_table.add_column("Status", style="green")

    providers = settings.llm.get_available_providers()

    for provider in ["openai", "anthropic", "google", "cursor"]:
        status = "✓ Configured" if provider in providers else "✗ Not configured"
        style = "green" if provider in providers else "red"
        providers_table.add_row(provider.capitalize(), f"[{style}]{status}[/{style}]")

    console.print(providers_table)

    # Model Configuration
    models_table = Table(title="Model Configuration")
    models_table.add_column("Type", style="cyan")
    models_table.add_column("Model", style="yellow")

    models_table.add_row("Default", settings.default_model)
    models_table.add_row("Fast", settings.fast_model)
    models_table.add_row("Reasoning", settings.reasoning_model)

    console.print(models_table)

    # Observability
    obs_table = Table(title="Observability")
    obs_table.add_column("Setting", style="cyan")
    obs_table.add_column("Value", style="yellow")

    langfuse_status = "Enabled" if settings.langfuse.is_configured else "Disabled"
    obs_table.add_row("Langfuse", langfuse_status)
    obs_table.add_row("Log Level", settings.log_level)
    obs_table.add_row("Verbose", str(settings.verbose))

    console.print(obs_table)


@app.command()
def init(
    path: Path = typer.Argument(
        ".",
        help="Path where to initialize the project",
    ),
) -> None:
    """Initialize Sheep configuration in a directory."""
    import shutil

    path = path.resolve()

    # Copy .env.example to .env if it doesn't exist
    env_example = Path(__file__).parent.parent.parent.parent / ".env.example"
    env_target = path / ".env"

    if env_target.exists():
        console.print("[yellow]⚠ .env file already exists, skipping...[/yellow]")
    else:
        if env_example.exists():
            shutil.copy(env_example, env_target)
            console.print(f"[green]✓ Created .env file at {env_target}[/green]")
        else:
            # Create a minimal .env
            env_target.write_text(
                """# Sheep Configuration
# Add your API keys here

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=

SHEEP_DEFAULT_MODEL=openai/gpt-4o
"""
            )
            console.print(f"[green]✓ Created minimal .env file at {env_target}[/green]")

    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Edit .env and add your API keys")
    console.print("2. Run: sheep config")
    console.print("3. Run: sheep implement <repo-path> -i '<issue>'")


if __name__ == "__main__":
    app()
