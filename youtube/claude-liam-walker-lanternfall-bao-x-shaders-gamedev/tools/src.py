"""The film's game source, read from git at the film's source revision (FILM-SOURCE-REVISION.txt), never from the
working tree: a later uncommitted edit under godot/ cannot leak into a code panel or a hash.

    from src import text, excerpt, blob, inventory, SHA
"""
import subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()


def blob(path: str) -> bytes:
    """Bytes of godot/<path> at the film revision."""
    return subprocess.run(["git", "-C", str(REPO), "show", f"{SHA}:godot/{path}"], capture_output=True, check=True).stdout


def text(path: str) -> str:
    return blob(path).decode("utf-8")


def excerpt(path: str, a: int, b: int) -> str:
    return "\n".join(text(path).splitlines()[a - 1:b])


def inventory() -> list:
    """Every file under godot/ at the film revision (what `git archive SHA godot` writes), minus .uid files."""
    out = subprocess.run(["git", "-C", str(REPO), "ls-tree", "-r", "--name-only", SHA, "godot"],
                         capture_output=True, text=True, check=True).stdout.split("\n")
    return sorted(p[len("godot/"):] for p in out if p and not p.endswith(".uid"))


def repo_text(path: str, rev: str = None) -> str:
    """A repository document (not game source) at a given revision, default the film revision."""
    return subprocess.run(["git", "-C", str(REPO), "show", f"{rev or SHA}:{path}"], capture_output=True, text=True,
                          check=True).stdout
