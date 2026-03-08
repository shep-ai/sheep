"""Utility functions for joke operations."""

import random
from pathlib import Path


def get_random_joke(repo_root: Path | None = None) -> str:
    """Get a random joke from the available joke files.

    Args:
        repo_root: Root directory of the repository. If None, uses the current working directory.

    Returns:
        A random joke as a string.
    """
    if repo_root is None:
        repo_root = Path.cwd()

    repo_root = Path(repo_root)

    # Collect all jokes from joke files
    jokes = []
    for joke_file in sorted(repo_root.glob("JOKE*.md")):
        content = joke_file.read_text(encoding="utf-8").strip()
        if content:
            jokes.append(content)

    if not jokes:
        return "# Random Joke\n\nNo jokes found!"

    # Select a random joke
    selected_joke = random.choice(jokes)

    return selected_joke
