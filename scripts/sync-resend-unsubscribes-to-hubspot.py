#!/usr/bin/env python3
"""Sync Resend audience unsubscribes back to HubSpot.

Iterates every Resend audience, collects contacts with `unsubscribed: true`,
and calls HubSpot's v1 subscriptions endpoint to globally opt each one out of
marketing email. Idempotent: HubSpot's PUT is a no-op if the contact is
already unsubscribed.

Why this exists: Resend handles the actual unsubscribe link (CASL-compliant,
{{{RESEND_UNSUBSCRIBE_URL}}} token in every broadcast). But HubSpot owns the
welcome workflow and other lifecycle sends. Without this sync, a contact who
unsubscribes via a Resend broadcast keeps receiving HubSpot emails — CASL
violation. This script closes the loop.

Runs hourly via `.github/workflows/sync-unsubscribes.yml`. Can also run locally:

  python scripts/sync-resend-unsubscribes-to-hubspot.py            # dry run
  python scripts/sync-resend-unsubscribes-to-hubspot.py --push     # actually sync

Auth: reads RESEND_API_KEY / HUBSPOT_API_KEY from env vars first (GitHub
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
RESEND_SECRETS_PATH = REPO_ROOT / ".secrets" / "resend.env"
HUBSPOT_SECRETS_PATH = REPO_ROOT / ".secrets" / "hubspot.env"
SYNC_LOG_PATH = REPO_ROOT / "promo" / "resend-hubspot-unsub-sync.log.json"

RESEND_BASE = "https://api.resend.com"
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


def call_resend(api_key: str, path: str) -> tuple[int, dict]:
    request = urllib.request.Request(f"{RESEND_BASE}{path}")
    request.add_header("Authorization", f"Bearer {api_key}")
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read().decode() or "{}")
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read().decode() or "{}")


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

    resend_key = load_key(RESEND_SECRETS_PATH, "RESEND_API_KEY")
    hubspot_key = load_key(HUBSPOT_SECRETS_PATH, "HUBSPOT_API_KEY")

    # Collect unsubscribed emails across all Resend audiences
    status, body = call_resend(resend_key, "/audiences")
    if status != 200:
        sys.exit(f"GET /audiences failed: {status} {body}")

    unsubscribed: list[dict] = []
    for audience in body.get("data", []):
        audience_id = audience["id"]
        audience_name = audience["name"]
        status, contacts_body = call_resend(resend_key, f"/audiences/{audience_id}/contacts")
        if status != 200:
            print(f"  WARN: GET /audiences/{audience_id}/contacts failed: {status}")
            continue
        for contact in contacts_body.get("data", []):
            if contact.get("unsubscribed"):
                unsubscribed.append(
                    {
                        "email": contact["email"],
                        "audience_id": audience_id,
                        "audience_name": audience_name,
                        "resend_contact_id": contact.get("id"),
                    }
                )

    print(f"Found {len(unsubscribed)} unsubscribed contact(s) across all Resend audiences")

    if not args.push:
        for entry in unsubscribed[:20]:
            print(f"  {entry['email']}  (audience: {entry['audience_name']})")
        if len(unsubscribed) > 20:
            print(f"  ...and {len(unsubscribed) - 20} more")
        print(f"\nRe-run with --push to mark them all unsubscribed in HubSpot.")
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
