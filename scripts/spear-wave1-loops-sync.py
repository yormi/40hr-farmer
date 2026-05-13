#!/usr/bin/env python3
"""Push the SPEAR Wave 1 audience into Loops.so.

Reads promo/spear-wave1-audience.csv and upserts each row into Loops with:
  - email
  - firstName (from HubSpot)
  - spearWave1 = "yield"          (custom field used to target the campaign)
  - source    = "SPEAR Wave 1"    (visible in Loops contact view)

The /contacts/update endpoint is upsert: re-running the script updates the
same contacts without duplicates. Custom fields are auto-created by Loops on
first push.

Usage:
  python scripts/spear-wave1-loops-sync.py            # dry run, prints summary
  python scripts/spear-wave1-loops-sync.py --push     # actually push to Loops
  python scripts/spear-wave1-loops-sync.py --push --limit 5  # smoke push first 5
"""

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import urllib.request
import urllib.error

REPO_ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATH = REPO_ROOT / ".secrets" / "loops.env"
AUDIENCE_CSV_PATH = REPO_ROOT / "promo" / "spear-wave1-audience.csv"
SYNC_LOG_PATH = REPO_ROOT / "promo" / "spear-wave1-loops-sync.log.json"

LOOPS_ENDPOINT = "https://app.loops.so/api/v1/contacts/update"
SPEAR_WAVE_VALUE = "yield"
SPEAR_SOURCE_VALUE = "SPEAR Wave 1"
RATE_LIMIT_SLEEP_SECONDS = 0.12


def load_api_key() -> str:
    if not SECRETS_PATH.exists():
        sys.exit(f"Missing secrets file: {SECRETS_PATH}")
    for line in SECRETS_PATH.read_text().splitlines():
        if line.startswith("LOOPS_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("LOOPS_API_KEY not found in secrets file")


def post_contact(api_key: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode()
    request = urllib.request.Request(LOOPS_ENDPOINT, data=data, method="POST")
    request.add_header("Authorization", f"Bearer {api_key}")
    request.add_header("Content-Type", "application/json")
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true", help="actually push to Loops")
    parser.add_argument("--limit", type=int, default=None, help="cap rows pushed")
    args = parser.parse_args()

    if not AUDIENCE_CSV_PATH.exists():
        sys.exit(f"Missing audience CSV: {AUDIENCE_CSV_PATH}")

    rows: list[dict[str, str]] = []
    with AUDIENCE_CSV_PATH.open() as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rows.append(row)
    print(f"Read {len(rows)} rows from {AUDIENCE_CSV_PATH.relative_to(REPO_ROOT)}")

    if args.limit is not None:
        rows = rows[: args.limit]
        print(f"  -> limited to first {len(rows)} rows")

    if not args.push:
        print("\nDry run. Sample payload:")
        if rows:
            sample = rows[0]
            payload = {
                "email": sample["email"],
                "firstName": sample.get("firstname") or None,
                "spearWave1": SPEAR_WAVE_VALUE,
                "source": SPEAR_SOURCE_VALUE,
            }
            print(json.dumps(payload, indent=2))
        print(f"\nRe-run with --push to upsert {len(rows)} contacts into Loops.")
        return

    api_key = load_api_key()
    successes: list[dict] = []
    failures: list[dict] = []

    for index, row in enumerate(rows, start=1):
        email = (row.get("email") or "").strip()
        if not email:
            failures.append({"row": row, "reason": "empty email"})
            continue
        firstname = (row.get("firstname") or "").strip() or None
        payload = {
            "email": email,
            "firstName": firstname,
            "spearWave1": SPEAR_WAVE_VALUE,
            "source": SPEAR_SOURCE_VALUE,
        }
        if firstname is None:
            del payload["firstName"]

        status, response_body = post_contact(api_key, payload)
        if status == 200 and response_body.get("success"):
            successes.append({"email": email, "id": response_body.get("id")})
        else:
            failures.append({"email": email, "status": status, "response": response_body})

        if index % 50 == 0:
            print(f"  ... pushed {index}/{len(rows)} (ok={len(successes)} fail={len(failures)})")

        time.sleep(RATE_LIMIT_SLEEP_SECONDS)

    print(f"\nDone. Pushed {len(successes)} contacts, {len(failures)} failures.")
    SYNC_LOG_PATH.write_text(json.dumps({
        "pushedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "totalRows": len(rows),
        "successes": len(successes),
        "failures": failures,
    }, indent=2))
    print(f"Wrote sync log to {SYNC_LOG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
