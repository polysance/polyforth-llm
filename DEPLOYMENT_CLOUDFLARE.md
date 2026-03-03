# Cloudflare Tunnel Deployment (Debian + KDE)

This guide deploys a public test endpoint for `cartheur.ai` using your local host and Cloudflare Tunnel.

Recommended first target:

- `beta.cartheur.ai` (staging)

## 1) Prerequisites

1. Cloudflare-managed domain (`cartheur.ai`) in your account.
2. Local project ready with index built (`python scripts/build_index.py`).
3. `.env` configured (model endpoint/key/source path).

## 2) Install system packages

```bash
sudo apt update
sudo apt install -y curl gnupg2 ca-certificates lsb-release debian-keyring debian-archive-keyring
```

## 3) Install Caddy (reverse proxy)

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install -y caddy
```

## 4) Install cloudflared

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloudflare-main.gpg
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared bookworm main' | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update
sudo apt install -y cloudflared
```

## 5) Create app service user

```bash
sudo useradd --system --create-home --shell /usr/sbin/nologin polyforth || true
sudo chown -R polyforth:polyforth /home/cartheur/ame/aiventure/aiventure-github/polysance/polyforth-llm
```

## 6) Configure app environment

Create runtime env file:

```bash
sudo tee /etc/polyforth-llm.env >/dev/null <<'EOF'
SOURCE_PATH=/home/cartheur/ame/aiventure/aiventure-github/polysance/polyforth-llm/data/polyForth-llm.docx
INDEX_DIR=/home/cartheur/ame/aiventure/aiventure-github/polysance/polyforth-llm/index
EMBEDDING_MODEL=/home/cartheur/ame/aiventure/aiventure-github/polysance/polyforth-llm/models/all-MiniLM-L6-v2
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=replace-me
LLM_MODEL=gpt-4o-mini
APP_API_KEY=replace-with-long-random-secret
EOF
```

Protect file:

```bash
sudo chmod 600 /etc/polyforth-llm.env
```

## 7) Create app systemd service

```bash
sudo tee /etc/systemd/system/polyforth-api.service >/dev/null <<'EOF'
[Unit]
Description=polyforth-llm API
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=polyforth
Group=polyforth
WorkingDirectory=/home/cartheur/ame/aiventure/aiventure-github/polysance/polyforth-llm
EnvironmentFile=/etc/polyforth-llm.env
ExecStart=/home/cartheur/ame/aiventure/aiventure-github/polysance/polyforth-llm/.venv/bin/python scripts/serve_api.py
Restart=always
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=false

[Install]
WantedBy=multi-user.target
EOF
```

Start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now polyforth-api
sudo systemctl status polyforth-api
```

## 8) Configure Caddy (localhost reverse proxy)

```bash
sudo tee /etc/caddy/Caddyfile >/dev/null <<'EOF'
:8080 {
    encode zstd gzip
    request_body {
        max_size 1MB
    }
    reverse_proxy 127.0.0.1:8000
}
EOF
sudo systemctl reload caddy
```

## 9) Create Cloudflare tunnel

Login:

```bash
cloudflared tunnel login
```

Create tunnel:

```bash
cloudflared tunnel create polyforth-beta
```

Create tunnel config:

```bash
sudo mkdir -p /etc/cloudflared
sudo tee /etc/cloudflared/config.yml >/dev/null <<'EOF'
tunnel: polyforth-beta
credentials-file: /home/cartheur/.cloudflared/<TUNNEL-UUID>.json
ingress:
  - hostname: beta.cartheur.ai
    service: http://127.0.0.1:8080
  - service: http_status:404
EOF
```

Route DNS:

```bash
cloudflared tunnel route dns polyforth-beta beta.cartheur.ai
```

Install/start tunnel service:

```bash
sudo cloudflared service install
sudo systemctl enable --now cloudflared
sudo systemctl status cloudflared
```

## 10) Validate endpoint

Health:

```bash
curl -s https://beta.cartheur.ai/health
```

Teach endpoint (requires API key):

```bash
curl -s -X POST https://beta.cartheur.ai/teach \
  -H "Content-Type: application/json" \
  -H "X-API-Key: replace-with-long-random-secret" \
  -d '{"question":"What is stack effect notation?"}'
```

## 11) Security controls (recommended)

1. Keep API bound to `127.0.0.1` only.
2. Use Cloudflare Access allowlist for early testers.
3. Keep `/etc/polyforth-llm.env` root-readable only.
4. Enable Cloudflare rate limiting on `/teach`.
5. Keep logs:
   - `journalctl -u polyforth-api -f`
   - `journalctl -u cloudflared -f`

## 12) Upgrade to main domain later

After stable testing on `beta.cartheur.ai`, repeat ingress route for production hostname and keep staging live for safe changes.
