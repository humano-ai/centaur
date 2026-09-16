"""Slack client for posting messages and uploading files into a thread."""

import os
import pathlib

import httpx

from centaur_sdk import secret

BASE_URL = "https://slack.com/api"


class SlackClient:
    def __init__(self, timeout: float = 60.0):
        self._http = httpx.Client(
            base_url=BASE_URL,
            timeout=timeout,
            headers={"Authorization": f"Bearer {secret('SLACK_BOT_TOKEN')}"},
        )

    def _call(self, method: str, **payload) -> dict:
        resp = self._http.post(f"/{method}", json=payload)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            raise RuntimeError(f"slack {method} failed: {data.get('error')}")
        return data

    def post(self, channel: str, text: str, thread_ts: str | None = None) -> dict:
        """Post a message, optionally as a reply in a thread."""
        return self._call("chat.postMessage", channel=channel, text=text, thread_ts=thread_ts)

    def upload(self, channel: str, path: str, title: str | None = None, thread_ts: str | None = None) -> dict:
        """Upload a file to a channel or thread via Slack's external-upload flow."""
        file = pathlib.Path(path)
        size = file.stat().st_size
        ticket = self._call("files.getUploadURLExternal", filename=file.name, length=size)
        put = self._http.put(ticket["upload_url"], content=file.read_bytes(), headers={"Authorization": ""})
        put.raise_for_status()
        return self._call(
            "files.completeUploadExternal",
            files=[{"id": ticket["file_id"], "title": title or file.name}],
            channel_id=channel,
            thread_ts=thread_ts,
        )

    def close(self) -> None:
        self._http.close()


def _client() -> SlackClient:
    return SlackClient()
