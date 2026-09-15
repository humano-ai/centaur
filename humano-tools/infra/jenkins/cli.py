"""CLI for Jenkins (jenkins.humano.ai)."""

import json

import typer

app = typer.Typer(name="jenkins", help="Read Jenkins builds and console logs.")


def _print(payload) -> None:
    print(json.dumps(payload, indent=2, default=str))


@app.command("health")
def health():
    """Check connectivity and auth with a read-only call."""
    from .client import _client

    try:
        _print({"ok": True, "tool": "jenkins", "details": _client().builds("bumi", limit=1)})
    except Exception as exc:
        _print({"ok": False, "tool": "jenkins", "error": str(exc)})
        raise typer.Exit(1) from exc


@app.command("build")
def build(job: str, number: str = typer.Argument("lastBuild")):
    """Result, building flag, and the sha/branch a build actually built."""
    from .client import _client

    _print(_client().build(job, number))


@app.command("builds")
def builds(job: str, limit: int = 10):
    """Recent builds with their built sha and branch."""
    from .client import _client

    _print(_client().builds(job, limit))


@app.command("console")
def console(job: str, number: str = typer.Argument("lastBuild"), tail: int = 0):
    """Console text of a build; --tail N prints only the last N lines."""
    from .client import _client

    text = _client().console(job, number)
    print("\n".join(text.splitlines()[-tail:]) if tail else text)
