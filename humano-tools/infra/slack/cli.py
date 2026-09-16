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


@app.command("thread")
def thread(channel: str, thread_ts: str, limit: int = 200):
    """Read a whole Slack thread (oldest first): use it to recover the task."""
    from .client import _client

    messages = _client().thread(channel, thread_ts, limit)
    for m in messages:
        print(json.dumps({"ts": m.get("ts"), "user": m.get("user") or m.get("bot_id"), "text": m.get("text", "")}))


@app.command("history")
def history(channel: str, limit: int = 50):
    """Read recent top-level messages in a channel."""
    from .client import _client

    for m in _client().history(channel, limit):
        print(json.dumps({"ts": m.get("ts"), "user": m.get("user") or m.get("bot_id"), "text": m.get("text", "")}))


@app.command("user")
def user(user_id: str):
    """Resolve a Slack user id to a name and email."""
    from .client import _client

    print(json.dumps(_client().user(user_id), indent=2))
