"""Slack client for posting messages and uploading files into a thread."""

import json
import pathlib

import httpx

from centaur_sdk import secret

BASE_URL = "https://slack.com/api"


class SlackClient:
    def __init__(self, timeout: float = 60.0):
        self._token = secret("SLACK_BOT_TOKEN")
        self._http = httpx.Client(
            base_url=BASE_URL,
            timeout=timeout,
            headers={"Authorization": f"Bearer {self._token}"},
        )

    # Slack's Web API takes form-encoded parameters. JSON bodies are accepted
    # only by a few methods, and the upload endpoints reject them with
    # invalid_arguments, so every call here posts a form.
    def _call(self, method: str, **payload) -> dict:
        form = {k: v for k, v in payload.items() if v is not None}
        resp = self._http.post(f"/{method}", data=form)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            raise RuntimeError(f"slack {method} failed: {data.get('error')}")
        return data

    def _get(self, method: str, **params) -> dict:
        resp = self._http.get(f"/{method}", params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            raise RuntimeError(f"slack {method} failed: {data.get('error')}")
        return data

    def post(self, channel: str, text: str, thread_ts: str | None = None) -> dict:
        """Post a message, optionally as a reply in a thread."""
        return self._call("chat.postMessage", channel=channel, text=text, thread_ts=thread_ts)

    def thread(self, channel: str, thread_ts: str, limit: int = 200) -> list[dict]:
        """Every message in a thread, oldest first — the task usually lives here."""
        data = self._get("conversations.replies", channel=channel, ts=thread_ts, limit=limit)
        return data.get("messages", [])

    def history(self, channel: str, limit: int = 50) -> list[dict]:
        """Recent top-level messages in a channel."""
        return self._get("conversations.history", channel=channel, limit=limit).get("messages", [])

    def user(self, user_id: str) -> dict:
        """Display name and email for a Slack user id, to resolve <@U…> mentions."""
        profile = self._get("users.info", user=user_id).get("user", {})
        return {
            "id": profile.get("id"),
            "name": profile.get("profile", {}).get("real_name") or profile.get("name"),
            "email": profile.get("profile", {}).get("email"),
        }

    def upload(self, channel: str, path: str, title: str | None = None, thread_ts: str | None = None) -> dict:
        """Upload a file to a channel or thread via Slack's external-upload flow."""
        file = pathlib.Path(path)
        body = file.read_bytes()
        ticket = self._call("files.getUploadURLExternal", filename=file.name, length=len(body))
        # The signed upload URL carries its own credentials: sending the bot
        # token there fails, so this PUT uses a bare client.
        with httpx.Client(timeout=self._http.timeout) as anon:
            anon.post(ticket["upload_url"], files={"file": (file.name, body)}).raise_for_status()
        return self._call(
            "files.completeUploadExternal",
            files=json.dumps([{"id": ticket["file_id"], "title": title or file.name}]),
            channel_id=channel,
            thread_ts=thread_ts,
        )

    def close(self) -> None:
        self._http.close()


def _client() -> SlackClient:
    return SlackClient()
