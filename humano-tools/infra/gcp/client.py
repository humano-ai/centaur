"""Read-only client for bumi staging on GCP: Cloud Run, Artifact Registry, Logging."""

import os
import re
from datetime import datetime, timedelta, timezone

import httpx

from centaur_sdk import secret

PROJECT = os.getenv("GCP_PROJECT", "bumi-platform-staging")
REGION = os.getenv("GCP_REGION", "asia-southeast1")
REPOSITORY = os.getenv("GCP_AR_REPOSITORY", "bumi")

RUN = f"https://run.googleapis.com/v2/projects/{PROJECT}/locations/{REGION}"
AR = f"https://artifactregistry.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/repositories/{REPOSITORY}"
REGISTRY = f"https://{REGION}-docker.pkg.dev/v2/{PROJECT}/{REPOSITORY}"
LOGGING = "https://logging.googleapis.com/v2/entries:list"

# Jenkins tags staging images `staging-<first 12 chars of the git sha>`.
_TAG_SHA = re.compile(r":staging-([0-9a-f]{7,40})$")
_INDEX_TYPES = (
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
)
_MANIFEST_ACCEPT = ", ".join(
    _INDEX_TYPES
    + (
        "application/vnd.oci.image.manifest.v1+json",
        "application/vnd.docker.distribution.manifest.v2+json",
    )
)


class GcpClient:
    def __init__(self, timeout: float = 60.0):
        self._http = httpx.Client(
            timeout=timeout,
            headers={"Authorization": f"Bearer {secret('GCP_ACCESS_TOKEN')}"},
        )

    def _get(self, url: str, **kwargs) -> httpx.Response:
        resp = self._http.get(url, **kwargs)
        resp.raise_for_status()
        return resp

    def services(self) -> list[dict]:
        """Every Cloud Run service in the project with its configured image."""
        resp = self._get(f"{RUN}/services")
        return [self._summarise(s) for s in resp.json().get("services", [])]

    def served(self, service: str) -> dict:
        """Prove which build is actually serving traffic for one service.

        The service template names an image by tag (`staging-<sha>`); what runs
        is the revision's pinned digest. Jenkins pushes multi-arch OCI indexes,
        so the tag resolves to an *index* digest while the revision runs the
        linux/amd64 child — the two digests legitimately differ. A revision
        counts as serving the tagged build when its digest is the tag's digest
        or one of that index's children.
        """
        svc = self._get(f"{RUN}/services/{service}").json()
        summary = self._summarise(svc)
        tag = summary["image"].rsplit(":", 1)[-1] if ":" in summary["image"] else None
        tag_digests = self._tag_digests(service, tag) if tag else set()

        revisions = []
        for rev_name, percent in summary["traffic"]:
            rev = self._get(f"{RUN}/services/{service}/revisions/{rev_name}").json()
            image = rev["containers"][0]["image"]
            digest = image.split("@", 1)[1] if "@" in image else None
            revisions.append(
                {
                    "revision": rev_name,
                    "percent": percent,
                    "digest": digest,
                    "created": rev.get("createTime"),
                    "matches_tag": digest in tag_digests if digest else False,
                }
            )

        serving = [r for r in revisions if r["percent"]]
        summary["revisions"] = revisions
        summary["verified"] = bool(serving) and all(r["matches_tag"] for r in serving)
        return summary

    def logs(self, service: str, since: str = "1h", severity: str = "DEFAULT", limit: int = 50) -> list[dict]:
        """Recent log entries for a service, newest first."""
        start = datetime.now(timezone.utc) - _parse_duration(since)
        flt = " AND ".join(
            [
                'resource.type="cloud_run_revision"',
                f'resource.labels.service_name="{service}"',
                f'severity>="{severity.upper()}"',
                f'timestamp>="{start.strftime("%Y-%m-%dT%H:%M:%SZ")}"',
            ]
        )
        resp = self._http.post(
            LOGGING,
            json={
                "resourceNames": [f"projects/{PROJECT}"],
                "filter": flt,
                "orderBy": "timestamp desc",
                "pageSize": limit,
            },
        )
        resp.raise_for_status()
        return [
            {
                "time": e.get("timestamp"),
                "severity": e.get("severity", "DEFAULT"),
                "revision": e.get("resource", {}).get("labels", {}).get("revision_name"),
                "message": _message(e),
            }
            for e in resp.json().get("entries", [])
        ]

    def _summarise(self, svc: dict) -> dict:
        image = svc["template"]["containers"][0]["image"]
        latest = svc.get("latestReadyRevision", "").rsplit("/", 1)[-1]
        traffic = [
            (t.get("revision") or latest, t.get("percent", 0))
            for t in svc.get("trafficStatuses", [])
            if t.get("percent")
        ]
        match = _TAG_SHA.search(image)
        return {
            "service": svc["name"].rsplit("/", 1)[-1],
            "image": image,
            "sha": match.group(1) if match else None,
            "latest_ready": latest,
            "ready": svc.get("terminalCondition", {}).get("state") == "CONDITION_SUCCEEDED",
            "traffic": traffic,
        }

    def _tag_digests(self, service: str, tag: str) -> set[str]:
        """The tag's own digest plus, for an index, every child manifest digest."""
        resp = self._get(f"{REGISTRY}/{service}/manifests/{tag}", headers={"Accept": _MANIFEST_ACCEPT})
        digests = {resp.headers.get("docker-content-digest")}
        body = resp.json()
        if body.get("mediaType") in _INDEX_TYPES:
            digests.update(m["digest"] for m in body.get("manifests", []))
        return {d for d in digests if d}


def _parse_duration(text: str) -> timedelta:
    match = re.fullmatch(r"(\d+)([smhd])", text.strip())
    if not match:
        raise ValueError(f"duration must look like 30m, 2h or 1d, got {text!r}")
    units = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}
    return timedelta(**{units[match.group(2)]: int(match.group(1))})


def _message(entry: dict) -> str:
    if "textPayload" in entry:
        return entry["textPayload"]
    payload = entry.get("jsonPayload") or {}
    if payload:
        return payload.get("message") or payload.get("msg") or str(payload)
    req = entry.get("httpRequest")
    if req:
        return f'{req.get("requestMethod")} {req.get("status")} {req.get("requestUrl")}'
    return ""
