#!/usr/bin/env python3
"""Sync Postmark unsubscribes back to HubSpot.

Postmark hosts the CASL-compliant unsubscribe link (via {{{ pm:unsubscribe }}}).
When a recipient clicks it, Postmark adds them to the broadcast stream's
suppression list and silently drops future sends. HubSpot owns the welcome
workflow + other lifecycle sends, so without this sync a Postmark-side
unsubscribe wouldn't reach HubSpot — and HubSpot would keep emailing them.
CASL violation. This script closes the loop.

Runs every 20 minutes via `.github/workflows/sync-unsubscribes.yml`. Also
runnable locally:

  python scripts/sync-postmark-unsubscribes-to-hubspot.py            # dry run
  python scripts/sync-postmark-unsubscribes-to-hubspot.py --push     # actually sync

Auth: reads POSTMARK_SERVER_TOKEN / HUBSPOT_API_KEY from env vars first
(GitHub Actions path), then from .secrets/*.env files (local path).

Scope: syncs only `Origin == "Customer"` suppressions — i.e. recipient-initiated
unsubscribes. Hard bounces and spam complaints are handled by HubSpot's own
bounce/complaint processing for HubSpot-sent mail; not mirrored here.
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
POSTMARK_SECRETS_PATH = REPO_ROOT / ".secrets" / "postmark.env"
HUBSPOT_SECRETS_PATH = REPO_ROOT / ".secrets" / "hubspot.env"
SYNC_LOG_PATH = REPO_ROOT / ".cache" / "postmark-hubspot-unsub-sync.log.json"

POSTMARK_BASE = "https://api.postmarkapp.com"
POSTMARK_STREAM = os.environ.get("POSTMARK_MESSAGE_STREAM", "broadcast")
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


def fetch_postmark_unsubscribes(server_token: str, stream: str) -> list[dict]:
    """Fetch recipient-initiated unsubscribes from Postmark's suppression list.

    Filters to `Origin == "Customer"` (the recipient clicked unsubscribe).
    """
    url = f"{POSTMARK_BASE}/message-streams/{stream}/suppressions/dump"
    request = urllib.request.Request(url, method="GET")
    request.add_header("Accept", "application/json")
    request.add_header("X-Postmark-Server-Token", server_token)
    request.add_header("User-Agent", USER_AGENT)
    with urllib.request.urlopen(request) as response:
        payload = json.loads(response.read().decode())

    suppressions = payload.get("Suppressions", [])
    return [
        {
            "email": entry["EmailAddress"],
            "reason": entry.get("SuppressionReason", ""),
            "origin": entry.get("Origin", ""),
            "createdAt": entry.get("CreatedAt", ""),
        }
        for entry in suppressions
        if entry.get("Origin") == "Customer"
    ]


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

    postmark_token = load_key(POSTMARK_SECRETS_PATH, "POSTMARK_SERVER_TOKEN")
    hubspot_key = load_key(HUBSPOT_SECRETS_PATH, "HUBSPOT_API_KEY")

    unsubscribed = fetch_postmark_unsubscribes(postmark_token, POSTMARK_STREAM)
    print(f"Found {len(unsubscribed)} customer-initiated unsubscribe(s) on Postmark stream '{POSTMARK_STREAM}'")

    if not args.push:
        for entry in unsubscribed[:20]:
            print(f"  {entry['email']}  ({entry['reason']}, {entry['createdAt']})")
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
                "stream": POSTMARK_STREAM,
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
