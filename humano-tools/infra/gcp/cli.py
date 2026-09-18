"""CLI for bumi staging on GCP (read-only)."""

import json

import typer

from .client import PROJECT, GcpClient

app = typer.Typer(help=f"Read-only view of {PROJECT}: what Cloud Run is serving, and its logs.")


@app.command()
def services(as_json: bool = typer.Option(False, "--json", help="Machine-readable output")):
    """List Cloud Run services with the git sha each is configured to run.

    Examples:
        gcp services
    """
    rows = GcpClient().services()
    if as_json:
        typer.echo(json.dumps(rows, indent=2))
        return
    for r in rows:
        traffic = ", ".join(f"{rev} {pct}%" for rev, pct in r["traffic"])
        typer.echo(f'{r["service"]:<18} sha={r["sha"] or "?":<12}  {"ready" if r["ready"] else "NOT READY"}  {traffic}')


@app.command()
def served(
    service: str = typer.Argument(..., help="Cloud Run service, e.g. bumi-api"),
    as_json: bool = typer.Option(False, "--json", help="Machine-readable output"),
):
    """Prove which build a service is actually serving.

    Checks every revision taking traffic and confirms the digest it runs is the
    image the `staging-<sha>` tag points to. Exit code 0 means verified, 1 means
    the serving revision does NOT match the tag (or the service is not ready).

    Examples:
        gcp served bumi-api
        gcp served bumi-pwa --json
    """
    r = GcpClient().served(service)
    if as_json:
        typer.echo(json.dumps(r, indent=2))
    else:
        typer.echo(f'{r["service"]}: configured sha={r["sha"] or "?"} image={r["image"]}')
        for rev in r["revisions"]:
            mark = "matches tag" if rev["matches_tag"] else "DOES NOT MATCH TAG"
            typer.echo(f'  {rev["revision"]:<24} {rev["percent"]:>3}%  {rev["digest"]}  {mark}  (created {rev["created"]})')
        typer.echo("VERIFIED: serving the tagged build" if r["verified"] else "NOT VERIFIED: see revisions above")
    raise typer.Exit(0 if r["verified"] else 1)


@app.command()
def logs(
    service: str = typer.Argument(..., help="Cloud Run service, e.g. bumi-api"),
    since: str = typer.Option("1h", "--since", help="Look-back window: 30m, 2h, 1d"),
    severity: str = typer.Option("DEFAULT", "--severity", "-s", help="Minimum severity, e.g. WARNING, ERROR"),
    limit: int = typer.Option(50, "--limit", "-n", help="Max entries"),
):
    """Recent log entries for a service, newest first.

    Examples:
        gcp logs bumi-api --severity ERROR --since 2h
        gcp logs bumi-pwa -n 20
    """
    for e in GcpClient().logs(service, since=since, severity=severity, limit=limit):
        typer.echo(f'{e["time"]} {e["severity"]:<8} {e["revision"] or "":<22} {e["message"]}')
