"""GitHub access is used through git and gh directly; this module only declares the secret."""


class GitHubClient:
    pass


def _client() -> GitHubClient:
    return GitHubClient()
