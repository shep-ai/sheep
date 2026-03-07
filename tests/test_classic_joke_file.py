import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CLASSIC_JOKE_FILE = REPO_ROOT / "CLASSIC_JOKE.md"


def test_file_exists():
    assert CLASSIC_JOKE_FILE.exists(), f"{CLASSIC_JOKE_FILE} does not exist"


def test_starts_with_joke_heading():
    content = CLASSIC_JOKE_FILE.read_text(encoding="utf-8")
    assert content.startswith("# Joke\n"), "File must start with '# Joke' heading"


def test_contains_bold_question():
    content = CLASSIC_JOKE_FILE.read_text(encoding="utf-8")
    assert re.search(r"\*\*Q:\*\* .+", content), "File must contain a **Q:** line"


def test_contains_bold_answer():
    content = CLASSIC_JOKE_FILE.read_text(encoding="utf-8")
    assert re.search(r"\*\*A:\*\* .+", content), "File must contain an **A:** line"


def test_ends_with_horizontal_rule():
    content = CLASSIC_JOKE_FILE.read_text(encoding="utf-8")
    assert content.endswith("---\n"), "File must end with '---' followed by a newline"
