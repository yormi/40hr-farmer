#!/usr/bin/env python3
"""Sync ESP unsubscribes back to HubSpot.

SCAFFOLD ONLY — ESP not yet chosen as of 2026-05-22 (Loops, Sequenzy, and
Resend all dropped; evaluating Postmark). The HubSpot-side opt-out call is
ready; the ESP-side "list everyone who unsubscribed" call must be wired up
once an ESP is locked. Search for `TODO(esp-pick)` below.

Why this exists: whichever ESP we use handles the actual unsubscribe link
(CASL-compliant). HubSpot owns the welcome workflow + other lifecycle sends.
Without this sync, a contact who unsubscribes via the ESP keeps receiving
HubSpot emails — CASL violation. This script closes the loop.

Runs hourly via `.github/workflows/sync-unsubscribes.yml`. Can also run locally:

  python scripts/sync-esp-unsubscribes-to-hubspot.py            # dry run
  python scripts/sync-esp-unsubscribes-to-hubspot.py --push     # actually sync

Auth: reads ESP_API_KEY / HUBSPOT_API_KEY from env vars first (GitHub
Actions path), then from .secrets/*.env files (local path).
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ESP_SECRETS_PATH = REPO_ROOT / ".secrets" / "esp.env"  # TODO(esp-pick): rename to chosen ESP
HUBSPOT_SECRETS_PATH = REPO_ROOT / ".secrets" / "hubspot.env"
SYNC_LOG_PATH = REPO_ROOT / "promo" / "esp-hubspot-unsub-sync.log.json"

HUBSPOT_BASE = "https://api.hubapi.com"
USER_AGENT = "orisha-mailer/1.0 (+https://orisha.io)"
RATE_LIMIT_SLEEP_SECONDS = 0.1


def load_key(path: Path, name: str) -> str:
    if os.environ.get(name):
        return os.environ[name]
    if not path.exists():
        sys.exit(f"Missing secrets file: {path} (and env var {name} not set)")
    for line in path.read_text().splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(f"{name} not found in {path} (and env var {name} not set)")


def fetch_esp_unsubscribes(esp_api_key: str) -> list[dict]:
    """Return list of dicts: [{"email": "...", "source": "...", ...}, ...].

    TODO(esp-pick): wire to the chosen ESP's unsubscribe-list endpoint.
    Each returned dict must include at least `email`. Other keys (source,
    list/audience name, contact id) are passed through to the sync log.
    """
    raise NotImplementedError(
        "ESP not chosen yet — wire this once Postmark (or other) is locked. "
        "See scripts/sync-esp-unsubscribes-to-hubspot.py."
    )


def hubspot_unsubscribe(api_key: str, email: str) -> tuple[int, dict]:
    email_encoded = urllib.parse.quote(email, safe="")
    data = json.dumps({"unsubscribeFromAll": True}).encode()
    request = urllib.request.Request(
        f"{HUBSPOT_BASE}/email/public/v1/subscriptions/{email_encoded}",
        data=data,
        method="PUT",
    )
    request.add_header("Authorization", f"Bearer {api_key}")
    request.add_header("Content-Type", "application/json")
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode()
            return response.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as error:
        raw = error.read().decode()
        try:
            return error.code, (json.loads(raw) if raw else {})
        except json.JSONDecodeError:
            return error.code, {"raw": raw[:200]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true", help="actually sync to HubSpot")
    args = parser.parse_args()

    esp_key = load_key(ESP_SECRETS_PATH, "ESP_API_KEY")
    hubspot_key = load_key(HUBSPOT_SECRETS_PATH, "HUBSPOT_API_KEY")

    unsubscribed = fetch_esp_unsubscribes(esp_key)
    print(f"Found {len(unsubscribed)} unsubscribed contact(s) from ESP")

    if not args.push:
        for entry in unsubscribed[:20]:
            print(f"  {entry['email']}  (source: {entry.get('source', '?')})")
        if len(unsubscribed) > 20:
            print(f"  ...and {len(unsubscribed) - 20} more")
        print("\nRe-run with --push to mark them all unsubscribed in HubSpot.")
        return

    synced = 0
    failures: list[dict] = []
    for entry in unsubscribed:
        email = entry["email"]
        status, body = hubspot_unsubscribe(hubspot_key, email)
        if status == 200:
            synced += 1
            print(f"  ✓ {email}")
        else:
            failures.append({"email": email, "status": status, "body": body})
            print(f"  ✗ {email}  status={status}  {json.dumps(body)[:140]}")
        time.sleep(RATE_LIMIT_SLEEP_SECONDS)

    print(f"\nDone. synced={synced}  failed={len(failures)}")
    SYNC_LOG_PATH.parent.mkdir(exist_ok=True)
    SYNC_LOG_PATH.write_text(
        json.dumps(
            {
                "syncedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "unsubscribedCount": len(unsubscribed),
                "synced": synced,
                "failures": failures,
            },
            indent=2,
        )
    )
    print(f"Wrote log to {SYNC_LOG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
