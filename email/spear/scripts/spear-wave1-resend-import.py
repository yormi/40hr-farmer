#!/usr/bin/env python3
"""Import the SPEAR Wave 1 audience into Resend, split 50/50 for A/B.

Reads email/spear/spear-wave1-audience.csv and pushes each row into ONE OF TWO
Resend audiences using a deterministic random shuffle (seed 42):

  Audience A — "SPEAR Wave 1 — A (Mechanism)"   ← Body A recipients
  Audience B — "SPEAR Wave 1 — B (Flip)"        ← Body B recipients

The script is idempotent: re-running it finds existing audiences by name
(creating them only on first run) and treats `contact already exists` as a
non-error.

Why two audiences instead of one with a Segment: Resend Segments are on
paid plans; pre-split audiences work on every tier and keep the broadcast
config simple (each broadcast targets exactly one audience).

Usage:
  python email/spear/scripts/spear-wave1-resend-import.py            # dry run, prints split summary
  python email/spear/scripts/spear-wave1-resend-import.py --push     # actually create audiences + push contacts
  python email/spear/scripts/spear-wave1-resend-import.py --push --limit 5  # smoke push first 5 per side
"""

import argparse
import csv
import json
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SECRETS_PATH = REPO_ROOT / ".secrets" / "resend.env"
AUDIENCE_CSV_PATH = REPO_ROOT / "email" / "spear" / "spear-wave1-audience.csv"
SYNC_LOG_PATH = REPO_ROOT / "email" / "spear" / "spear-wave1-resend-sync.log.json"

RESEND_BASE = "https://api.resend.com"
AUDIENCE_A_NAME = "SPEAR Wave 1 — A (Mechanism)"
AUDIENCE_B_NAME = "SPEAR Wave 1 — B (Flip)"
SHUFFLE_SEED = 42
USER_AGENT = "orisha-mailer/1.0 (+https://orisha.io)"
RATE_LIMIT_SLEEP_SECONDS = 0.12  # ~8 req/sec, under Resend's 10/sec limit


def load_api_key() -> str:
    if not SECRETS_PATH.exists():
        sys.exit(f"Missing secrets file: {SECRETS_PATH}")
    for line in SECRETS_PATH.read_text().splitlines():
        if line.startswith("RESEND_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("RESEND_API_KEY not found in secrets file")


def call(api_key: str, method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(f"{RESEND_BASE}{path}", data=data, method=method)
    request.add_header("Authorization", f"Bearer {api_key}")
    request.add_header("Content-Type", "application/json")
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode()
            return response.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        raw = error.read().decode()
        try:
            return error.code, json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            return error.code, {"raw": raw}


def find_or_create_audience(api_key: str, name: str) -> str:
    """Return the audience id; create if it doesn't exist."""
    status, body = call(api_key, "GET", "/audiences")
    if status != 200:
        sys.exit(f"GET /audiences failed: {status} {body}")
    for audience in body.get("data", []):
        if audience.get("name") == name:
            return audience["id"]
    status, body = call(api_key, "POST", "/audiences", {"name": name})
    if status != 201 or "id" not in body:
        sys.exit(f"POST /audiences failed: {status} {body}")
    return body["id"]


def add_contact(api_key: str, audience_id: str, email: str, first_name: str | None) -> tuple[bool, str]:
    """Returns (was_added_or_already_present, message)."""
    payload: dict = {"email": email}
    if first_name:
        payload["first_name"] = first_name
    status, body = call(api_key, "POST", f"/audiences/{audience_id}/contacts", payload)
    if status == 201 and body.get("id"):
        return True, "added"
    if status == 200 and body.get("id"):  # some Resend versions return 200
        return True, "added"
    error_msg = (body.get("message") or body.get("name") or json.dumps(body))[:120]
    if "already" in error_msg.lower() or status == 409:
        return True, "already-present"
    return False, f"status={status} {error_msg}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true", help="actually push to Resend")
    parser.add_argument("--limit", type=int, default=None, help="cap rows pushed per side (smoke)")
    args = parser.parse_args()

    if not AUDIENCE_CSV_PATH.exists():
        sys.exit(f"Missing audience CSV: {AUDIENCE_CSV_PATH}")

    rows: list[dict[str, str]] = []
    with AUDIENCE_CSV_PATH.open() as csv_file:
        for row in csv.DictReader(csv_file):
            if row.get("email"):
                rows.append(row)
    print(f"Read {len(rows)} rows from {AUDIENCE_CSV_PATH.relative_to(REPO_ROOT)}")

    # Deterministic 50/50 split
    shuffled = rows.copy()
    random.Random(SHUFFLE_SEED).shuffle(shuffled)
    midpoint = len(shuffled) // 2
    side_a = shuffled[:midpoint]
    side_b = shuffled[midpoint:]
    print(f"  Split: A={len(side_a)}, B={len(side_b)}  (deterministic shuffle seed={SHUFFLE_SEED})")

    if args.limit is not None:
        side_a = side_a[: args.limit]
        side_b = side_b[: args.limit]
        print(f"  -> limited to first {args.limit} per side")

    if not args.push:
        print("\nDry run. Sample contact from each side:")
        if side_a:
            print(f"  A[0]: {side_a[0]['email']}  firstname={side_a[0].get('firstname') or '(empty)'}")
        if side_b:
            print(f"  B[0]: {side_b[0]['email']}  firstname={side_b[0].get('firstname') or '(empty)'}")
        print(f"\nRe-run with --push to create audiences + import {len(side_a)+len(side_b)} contacts.")
        return

    api_key = load_api_key()
    audience_a_id = find_or_create_audience(api_key, AUDIENCE_A_NAME)
    audience_b_id = find_or_create_audience(api_key, AUDIENCE_B_NAME)
    print(f"\nAudience A: {AUDIENCE_A_NAME}  id={audience_a_id}")
    print(f"Audience B: {AUDIENCE_B_NAME}  id={audience_b_id}\n")

    results: dict = {"a": {"ok": 0, "fail": 0, "failures": []}, "b": {"ok": 0, "fail": 0, "failures": []}}
    for side_name, audience_id, contacts in [("a", audience_a_id, side_a), ("b", audience_b_id, side_b)]:
        print(f"Pushing side {side_name.upper()} ({len(contacts)} contacts)...")
        for index, row in enumerate(contacts, start=1):
            email = row["email"].strip()
            first_name = (row.get("firstname") or "").strip() or None
            ok, msg = add_contact(api_key, audience_id, email, first_name)
            if ok:
                results[side_name]["ok"] += 1
            else:
                results[side_name]["fail"] += 1
                results[side_name]["failures"].append({"email": email, "reason": msg})
            if index % 50 == 0:
                print(f"  {side_name.upper()}: {index}/{len(contacts)}  ok={results[side_name]['ok']}  fail={results[side_name]['fail']}")
            time.sleep(RATE_LIMIT_SLEEP_SECONDS)
        print(f"  {side_name.upper()} done: ok={results[side_name]['ok']}  fail={results[side_name]['fail']}")

    SYNC_LOG_PATH.write_text(
        json.dumps(
            {
                "pushedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "audienceAId": audience_a_id,
                "audienceBId": audience_b_id,
                "audienceAName": AUDIENCE_A_NAME,
                "audienceBName": AUDIENCE_B_NAME,
                "split": {"a": len(side_a), "b": len(side_b)},
                "results": results,
            },
            indent=2,
        )
    )
    print(f"\nWrote sync log to {SYNC_LOG_PATH.relative_to(REPO_ROOT)}")
    print(f"\nNEXT: use these audience IDs in Resend broadcasts:")
    print(f"  Body A → audience_id = {audience_a_id}")
    print(f"  Body B → audience_id = {audience_b_id}")


if __name__ == "__main__":
    main()
