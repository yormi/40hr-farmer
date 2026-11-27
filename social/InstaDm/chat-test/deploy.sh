#!/usr/bin/env bash
# Idempotent: installs Node + Caddy on first run, then syncs code and env, then restarts (server data/ untouched).
set -euo pipefail
HOST=root@172.105.6.173
DOMAIN=172-105-6-173.ip.linodeusercontent.com
NODE_VERSION=22.21.1
cd "$(dirname "$0")"
SECRETS=../../../.secrets

ssh "$HOST" bash -s <<REMOTE
set -euo pipefail
if [ ! -x /opt/node/bin/node ]; then
  cd /tmp
  curl -fsSLO https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz
  curl -fsSL https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt | grep node-v$NODE_VERSION-linux-x64.tar.gz\$ | sha256sum -c -
  mkdir -p /opt/node && tar xzf node-v$NODE_VERSION-linux-x64.tar.gz -C /opt/node --strip-components=1
  ln -sf /opt/node/bin/node /usr/local/bin/node && ln -sf /opt/node/bin/npm /usr/local/bin/npm
fi
command -v caddy >/dev/null || { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq caddy; }
id orisha >/dev/null 2>&1 || useradd --system --home /opt/ig-dm --shell /usr/sbin/nologin orisha
mkdir -p /opt/ig-dm/data && chown -R orisha:orisha /opt/ig-dm
REMOTE

tar czf - server.ts manychat.ts index.html package.json package-lock.json \
  | ssh "$HOST" "tar xzf - -C /opt/ig-dm && chown -R orisha:orisha /opt/ig-dm && cd /opt/ig-dm && su -s /bin/bash orisha -c 'npm ci --omit=dev --silent'"

source "$SECRETS/editor.env"
EDITOR_HASH=$(printf '%s\n' "$EDITOR_PASSWORD" | ssh "$HOST" caddy hash-password)

cat "$SECRETS/anthropic.env" "$SECRETS/manychat.env" | ssh "$HOST" "install -m 600 -o root -g root /dev/stdin /etc/ig-dm.env"

ssh "$HOST" bash -s <<REMOTE
set -euo pipefail
cat > /etc/systemd/system/ig-dm.service <<UNIT
[Unit]
Description=Instagram DM funnel server
After=network-online.target

[Service]
User=orisha
WorkingDirectory=/opt/ig-dm
EnvironmentFile=/etc/ig-dm.env
ExecStart=/usr/local/bin/node server.ts
Restart=always
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/opt/ig-dm/data
ProtectHome=true

[Install]
WantedBy=multi-user.target
UNIT
cat > /etc/caddy/Caddyfile <<'CADDY'
$DOMAIN {
	@inbound path /ig-inbound
	handle @inbound {
		reverse_proxy 127.0.0.1:8791
	}
	handle {
		basicauth {
			$EDITOR_USER $EDITOR_HASH
		}
		reverse_proxy 127.0.0.1:8791
	}
}
CADDY
systemctl daemon-reload
systemctl enable --now ig-dm.service caddy
systemctl restart ig-dm.service
systemctl reload caddy || systemctl restart caddy
REMOTE
echo "Deployed to https://$DOMAIN"
