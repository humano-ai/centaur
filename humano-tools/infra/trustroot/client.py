"""Read-only diagnostics client for the Trustroot deployment."""

import httpx

from centaur_sdk import secret

BASE_URL = "https://trustroot.136.85.41.115.sslip.io/_diag"


class TrustrootDiagClient:
    def __init__(self, timeout: float = 30.0):
        self._http = httpx.Client(
            base_url=BASE_URL,
            timeout=timeout,
            headers={"Authorization": f"Bearer {secret('TRUSTROOT_DIAG_TOKEN')}"},
            verify=False,  # sslip.io cert is issued for the bare IP host
        )

    def ps(self) -> list[dict]:
        """Every trustroot container with its state and health."""
        resp = self._http.get("/ps")
        resp.raise_for_status()
        return resp.json()

    def logs(self, service: str, tail: int = 200) -> str:
        """Recent stdout/stderr for one service (backend, frontend, worker, …)."""
        resp = self._http.get("/logs", params={"service": service, "tail": tail})
        resp.raise_for_status()
        return resp.text

    def close(self) -> None:
        self._http.close()


def _client() -> TrustrootDiagClient:
    return TrustrootDiagClient()
