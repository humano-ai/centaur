# fyndry.ai landing page

Static page, no build step. `index.html` pulls in `style.css`, the SVG marks and
`img/*.jpg` (generated with xAI), and nothing else — open `index.html` directly
to preview it.

## Deploying

It is served by the host Caddy on the `centaur` VM (`humano-foundry`,
`asia-southeast1-a`, 136.85.65.194) out of `/var/www/fyndry`, with automatic TLS
for `fyndry.ai`. `console.fyndry.ai` and `hooks.fyndry.ai` are separate site
blocks in `/etc/caddy/Caddyfile` that proxy into the k3s cluster.

```bash
gcloud --account=foundry-ops@humano-foundry.iam.gserviceaccount.com \
  --project=humano-foundry compute ssh centaur --zone asia-southeast1-a \
  --command 'sudo mkdir -p /var/www/fyndry'

# from this directory
tar cz -C site . | gcloud --account=foundry-ops@humano-foundry.iam.gserviceaccount.com \
  --project=humano-foundry compute ssh centaur --zone asia-southeast1-a \
  --command 'sudo tar xz -C /var/www/fyndry'
```

Caddy serves the files straight off disk, so there is nothing to restart.
