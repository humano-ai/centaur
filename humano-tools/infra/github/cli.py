"""Health check for sandbox GitHub access."""

import subprocess

import typer

app = typer.Typer(name="github-auth", help="Check that git and gh are authenticated.")


@app.command("health")
def health():
    """Print the authenticated GitHub login."""
    raise typer.Exit(subprocess.call(["gh", "api", "user", "--jq", ".login"]))
