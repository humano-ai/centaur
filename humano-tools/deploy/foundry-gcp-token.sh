#!/bin/bash
# Mints a 1h OAuth token for fyndry-reader@bumi-platform-staging and stores it
# as the Console value of the sandbox GCP_ACCESS_TOKEN secret. Run every 20 min.
#
# Keyless: bumi's org policy forbids service-account keys, so the VM
# authenticates as its own attached service account via the metadata server
# and impersonates fyndry-reader (it holds roles/iam.serviceAccountTokenCreator
# on that one account only).
#
# Read-only is enforced by fyndry-reader's IAM roles alone (run.viewer,
# artifactregistry.reader, logging.viewer). The scope cannot help: Cloud Run's
# v2 API rejects cloud-platform.read-only with "insufficient authentication
# scopes", so the token has to carry the full cloud-platform scope. Never grant
# fyndry-reader a write role — nothing else stands in the way.
set -euo pipefail
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
TARGET=fyndry-reader@bumi-platform-staging.iam.gserviceaccount.com
HOSTS=(run.googleapis.com artifactregistry.googleapis.com logging.googleapis.com asia-southeast1-docker.pkg.dev)

vm_token=$(curl -fsS -H 'Metadata-Flavor: Google' \
  http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token | jq -r .access_token)
token=$(curl -fsS -X POST \
  "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/$TARGET:generateAccessToken" \
  -H "Authorization: Bearer $vm_token" -H 'content-type: application/json' \
  -d '{"scope":["https://www.googleapis.com/auth/cloud-platform"],"lifetime":"3600s"}' | jq -r .accessToken)
[[ "$token" == ya29.* ]] || { echo "failed to mint $TARGET token" >&2; exit 1; }

api_key=$(kubectl -n centaur get secret centaur-infra-env -o jsonpath='{.data.IRON_CONTROL_INITIAL_API_KEY}' | base64 -d)
body=$(jq -cn --arg t "$token" --args '{data:{name:"GCP_ACCESS_TOKEN", kind:"custom", labels:{"managed-by":"foundry"},
  replace_config:{proxy_value:"GCP_ACCESS_TOKEN", match_headers:["Authorization"]},
  source:{source_type:"control_plane", secret:$t},
  rules:[$ARGS.positional[] | {host:.}]}}' "${HOSTS[@]}")
kubectl -n centaur exec -i deploy/centaur-centaur-api-rs -- curl -fsS -X PUT \
  http://centaur-centaur-console:3000/api/v1/static_secrets/tool-gcp-gcp-access-token \
  -H "authorization: Bearer $api_key" -H 'content-type: application/json' --data-binary @- <<<"$body" \
  | jq -r '"updated \(.data.foreign_id) source=\(.data.source.source_type)"'
