#!/bin/bash
# Mints a humano-foundry GitHub App installation token (valid 1h) and stores it
# as the Console value of the sandbox GITHUB_TOKEN secret. Run every 20 min.
set -euo pipefail
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
APP_ID=4703056
INSTALLATION_ID=156219131
KEY=/etc/foundry/github-app.pem
b64() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }
now=$(date +%s)
h=$(printf '{"alg":"RS256","typ":"JWT"}' | b64)
p=$(printf '{"iat":%d,"exp":%d,"iss":"%s"}' $((now - 60)) $((now + 540)) "$APP_ID" | b64)
jwt="$h.$p.$(printf '%s.%s' "$h" "$p" | openssl dgst -sha256 -sign "$KEY" | b64)"
token=$(curl -fsS -X POST "https://api.github.com/app/installations/$INSTALLATION_ID/access_tokens" \
  -H "Authorization: Bearer $jwt" -H "Accept: application/vnd.github+json" | jq -r .token)
[[ "$token" == ghs_* ]] || { echo "failed to mint installation token" >&2; exit 1; }
api_key=$(kubectl -n centaur get secret centaur-infra-env -o jsonpath='{.data.IRON_CONTROL_INITIAL_API_KEY}' | base64 -d)
body=$(jq -cn --arg t "$token" '{data:{name:"GITHUB_TOKEN", kind:"custom", labels:{"managed-by":"foundry"},
  replace_config:{proxy_value:"GITHUB_TOKEN", match_headers:["Authorization"]},
  source:{source_type:"control_plane", secret:$t},
  rules:[{host:"github.com"},{host:"api.github.com"},{host:"uploads.github.com"}]}}')
kubectl -n centaur exec -i deploy/centaur-centaur-api-rs -- curl -fsS -X PUT \
  http://centaur-centaur-console:3000/api/v1/static_secrets/tool-github-github-token \
  -H "authorization: Bearer $api_key" -H 'content-type: application/json' --data-binary @- <<<"$body" \
  | jq -r '"updated \(.data.foreign_id) source=\(.data.source.source_type)"'
