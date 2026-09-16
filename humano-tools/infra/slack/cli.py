"""CLI for posting Slack messages and uploading evidence files."""

import json

import typer

app = typer.Typer(name="slack-post", help="Post messages and upload files to Slack.")


@app.command("health")
def health():
    """Check that the sandbox's Slack credential works."""
    from .client import SlackClient

    client = SlackClient()
    try:
        print(json.dumps(client._call("auth.test"), indent=2))
    finally:
        client.close()


@app.command("message")
def message(channel: str, text: str, thread_ts: str = typer.Option(None, "--thread-ts")):
    """Post a message, optionally into a thread."""
    from .client import _client

    print(json.dumps(_client().post(channel, text, thread_ts), indent=2, default=str))


@app.command("upload")
def upload(
    channel: str,
    path: str,
    title: str = typer.Option(None, "--title"),
    thread_ts: str = typer.Option(None, "--thread-ts"),
):
    """Upload a file (screenshot, log, evidence) to a channel or thread."""
    from .client import _client

    print(json.dumps(_client().upload(channel, path, title, thread_ts), indent=2, default=str))
