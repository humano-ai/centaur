"""Jenkins HTTP client for jenkins.humano.ai."""

import os
import re

import httpx

from centaur_sdk import secret

BASE_URL = os.getenv("JENKINS_URL", "https://jenkins.humano.ai").rstrip("/")
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


class JenkinsClient:
    def __init__(self, timeout: float = 60.0):
        self._http = httpx.Client(
            base_url=BASE_URL,
            timeout=timeout,
            headers={"Authorization": f"Basic {secret('JENKINS_AUTH')}"},
            follow_redirects=True,
        )

    def build(self, job: str, number: str = "lastBuild") -> dict:
        """Build result, building flag, and the revision/branch it actually built."""
        resp = self._http.get(f"/job/{job}/{number}/api/json")
        resp.raise_for_status()
        data = httpx.Response(200, text=_CONTROL_CHARS.sub("", resp.text)).json()
        revision = next((a["lastBuiltRevision"] for a in data.get("actions", []) if a and "lastBuiltRevision" in a), {})
        return {
            "number": data.get("number"),
            "result": data.get("result"),
            "building": data.get("building"),
            "url": data.get("url"),
            "sha": revision.get("SHA1"),
            "branch": (revision.get("branch") or [{}])[0].get("name"),
        }

    def builds(self, job: str, limit: int = 10) -> list[dict]:
        """Recent builds with their built sha and branch."""
        resp = self._http.get(f"/job/{job}/api/json", params={"tree": f"builds[number]{{0,{limit}}}"})
        resp.raise_for_status()
        return [self.build(job, str(b["number"])) for b in resp.json().get("builds", [])]

    def console(self, job: str, number: str = "lastBuild") -> str:
        """Full console text of a build."""
        resp = self._http.get(f"/job/{job}/{number}/consoleText")
        resp.raise_for_status()
        return resp.text

    def close(self) -> None:
        self._http.close()


def _client() -> JenkinsClient:
    return JenkinsClient()
