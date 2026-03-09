"""Utility for loading and displaying random jokes."""

import random
from pathlib import Path


def load_jokes() -> list[str]:
    """Load all jokes from JOKE*.md files in the project root.

    Returns:
        List of jokes (strings), separated by '---' markers in the files.
    """
    project_root = Path(__file__).parent.parent.parent.parent
    jokes = []

    # Look for JOKE.md, JOKE2.md, JOKE3.md, etc.
    joke_files = sorted(project_root.glob("JOKE*.md"))

    for joke_file in joke_files:
        content = joke_file.read_text()
        # Split by '---' separator
        entries = content.split("---")
        for entry in entries:
            joke = entry.strip()
            if not joke:
                continue
            # Remove markdown header line if it exists
            if joke.startswith("# Joke"):
                lines = joke.split("\n", 1)
                joke = lines[1].strip() if len(lines) > 1 else ""
            # Only include non-empty entries
            if joke:
                jokes.append(joke)

    return jokes


def get_random_joke() -> str:
    """Get a random joke from the loaded jokes.

    Returns:
        A random joke string, or a default message if no jokes are found.
    """
    jokes = load_jokes()
    if not jokes:
        return "No jokes found! Add some JOKE*.md files to the project root."
    return random.choice(jokes)
