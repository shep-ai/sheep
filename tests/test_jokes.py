"""Tests for joke utilities."""

from sheep.utils import get_random_joke, load_jokes


def test_load_jokes():
    """Test that jokes are loaded correctly."""
    jokes = load_jokes()
    assert isinstance(jokes, list)
    assert len(jokes) > 0
    # All jokes should be non-empty strings
    for joke in jokes:
        assert isinstance(joke, str)
        assert len(joke) > 0
        # Jokes should not start with markdown header
        assert not joke.startswith("# Joke")


def test_get_random_joke():
    """Test that a random joke can be retrieved."""
    joke = get_random_joke()
    assert isinstance(joke, str)
    assert len(joke) > 0
    # The joke should be one of the loaded jokes or an error message
    jokes = load_jokes()
    assert joke in jokes or joke == "No jokes found! Add some JOKE*.md files to the project root."
