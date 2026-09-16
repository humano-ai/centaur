"""CLI for Trustroot deployment diagnostics (read-only)."""

import json

import typer

app = typer.Typer(name="trustroot", help="Container status and logs for the Trustroot deployment.")


@app.command("ps")
def ps():
    """List trustroot containers with state and health."""
    from .client import _client

    for c in _client().ps():
        print(f"{c['name']:<28} {c['state']:<10} {c['status']}")


@app.command("logs")
def logs(service: str, tail: int = 200):
    """Print recent logs for one service: backend, frontend, worker, ai_gateway, eval_server."""
    from .client import _client

    print(_client().logs(service, tail))


@app.command("health")
def health():
    """Check that diagnostics access works."""
    from .client import _client

    try:
        print(json.dumps({"ok": True, "containers": len(_client().ps())}))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        raise typer.Exit(1) from exc
