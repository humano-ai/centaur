# Humano tools

The only tools and personas Humano's Centaur sandboxes see (chart value
`toolServer.subdir: humano-tools`). Upstream `tools/` stays untouched so the fork
merges cleanly.

- `personas/bumi` — #bumi workflow prompt
- `personas/eng` — copy of the upstream default engineering persona
- `infra/github` — declares `GITHUB_TOKEN` for sandbox git/gh
- `infra/jenkins` — `jenkins` CLI for jenkins.humano.ai (`JENKINS_AUTH`)
- `infra/gcp` — `gcp` CLI, read-only on `bumi-platform-staging`: which build
  Cloud Run is serving, and service logs (`GCP_ACCESS_TOKEN`)
- `deploy/` — VM timers that mint the short-lived GitHub App and GCP tokens
