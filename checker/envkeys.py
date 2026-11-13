#!/usr/bin/env python3
"""Dead-simple API-key handling for a fresh clone of the checker.

Two keys are involved:
  NEURONPEDIA_API_KEY  - scores activations (score.py)
  ANTHROPIC_API_KEY    - generates prompts, mode (a) (generate.py)

Resolution order for both: the real process environment first, then a
`.env` file next to these scripts (or in the current working directory
if that is a different folder). Copy `.env.example` to `.env` and paste
the keys; that is all a new user has to do.

If a key is still missing and the program is running in an interactive
terminal, require_key() offers to take the key by a hidden paste prompt
right there, and optionally saves it into the checker folder's `.env`
(0600) so it only has to be pasted once.

Keys are NEVER printed, logged, or written anywhere except a `.env`
the user explicitly approved saving to.
"""
import getpass
import os
import sys

CHECKER_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILENAME = ".env"

_loaded = False


def _candidate_env_files():
    paths = [os.path.join(CHECKER_DIR, ENV_FILENAME)]
    cwd_path = os.path.join(os.getcwd(), ENV_FILENAME)
    if cwd_path != paths[0]:
        paths.append(cwd_path)
    return paths


def _parse_env_file(path):
    """Parse one .env file into {name: value}; tolerant of quotes,
    surrounding spaces, `export ` prefixes, and comment lines."""
    pairs = {}
    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError:
        return pairs
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        name, _, value = line.partition("=")
        name = name.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if name:
            pairs[name] = value
    return pairs


def load_dotenv():
    """Load .env entries into os.environ for keys not already set.

    The real environment always wins: a variable that is already set
    (even to an empty string is treated as unset by get_key) is never
    overwritten by a file value. Idempotent.
    """
    global _loaded
    if _loaded:
        return
    _loaded = True
    for path in _candidate_env_files():
        for name, value in _parse_env_file(path).items():
            if name not in os.environ:
                os.environ[name] = value


def get_key(name):
    """The key's value from the environment or a .env file, else None."""
    load_dotenv()
    value = os.environ.get(name)
    return value if value else None


def _save_to_dotenv(name, value):
    """Append or update `name` in the checker folder's .env (0600)."""
    path = os.path.join(CHECKER_DIR, ENV_FILENAME)
    lines = []
    if os.path.exists(path):
        with open(path) as f:
            lines = f.read().splitlines()
    found = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("export "):
            stripped = stripped[len("export "):].lstrip()
        if stripped.startswith(name + "="):
            lines[i] = f"{name}={value}"
            found = True
            break
    if not found:
        lines.append(f"{name}={value}")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(path, 0o600)


def require_key(name, what_for, where_to_get):
    """Return the key for `name`, prompting interactively if needed.

    If the key is already available (environment or .env), return it.
    If it is missing and stdin is a TTY, explain what it is for, take
    the key via a hidden getpass prompt, and offer to save it to the
    checker folder's .env for next time. If it is missing and stdin is
    not a TTY, return None so the caller can print setup instructions
    (see `where_to_get`) instead of hanging a scripted run.
    """
    key = get_key(name)
    if key:
        return key
    if not (sys.stdin and sys.stdin.isatty()):
        return None
    try:
        print(f"{name} is not set. It is needed {what_for}.")
        print(f"You can get one at {where_to_get}.")
        answer = getpass.getpass(
            f"Paste your {name} (input hidden, Enter to skip): "
        )
    except (EOFError, KeyboardInterrupt):
        return None
    answer = (answer or "").strip()
    if not answer:
        return None
    os.environ[name] = answer
    try:
        save = input("Save it to .env in this folder for next time? [y/N] ")
    except (EOFError, KeyboardInterrupt):
        save = ""
    if save.strip().lower() in ("y", "yes"):
        _save_to_dotenv(name, answer)
    return answer
