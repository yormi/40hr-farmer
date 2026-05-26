#!/usr/bin/env python3
"""Publish SPEAR Wave 2 audience as 6 HubSpot static lists.

Reads the per-day-per-body CSVs built by spear-wave2-build.py and creates
one HubSpot MANUAL (static) list per CSV, then adds the contact IDs.

The resulting lists can be selected as the audience for a HubSpot marketing
email send (one send per list, since each contains the recipients for one
body × one day).

Usage:
  # Dry run: print what would be created
  python email/spear/scripts/spear-wave2-publish-to-hubspot.py

  # Actually create the lists in HubSpot
  python email/spear/scripts/spear-wave2-publish-to-hubspot.py --create

Auth: reads HUBSPOT_API_KEY from env first, then from .secrets/hubspot.env.

List naming follows the pattern:
  SPEAR Wave 2 - Day {N} - Body {A|B} ({Mechanism|Flip})
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SECRETS_PATH = REPO_ROOT / ".secrets" / "hubspot.env"
OUTPUT_DIR = REPO_ROOT / "email" / "spear"
OUTPUT_PUBLISH_LOG = OUTPUT_DIR / "spear-wave2-hubspot-lists.json"

PER_DAY_PLAN = [
    {"day": 1, "body": "A", "label": "Mechanism", "csvs": ["spear-wave2-day1-bodyA.csv"]},
    {"day": 1, "body": "B", "label": "Flip",      "csvs": ["spear-wave2-day1-bodyB.csv"]},
    {"day": 2, "body": "A", "label": "Mechanism", "csvs": ["spear-wave2-day2-bodyA.csv"]},
    {"day": 2, "body": "B", "label": "Flip",      "csvs": ["spear-wave2-day2-bodyB.csv"]},
    {"day": 3, "body": "A", "label": "Mechanism", "csvs": ["spear-wave2-day3-bodyA.csv"]},
    {"day": 3, "body": "B", "label": "Flip",      "csvs": ["spear-wave2-day3-bodyB.csv"]},
]

BY_BODY_PLAN = [
    {"day": None, "body": "A", "label": "Mechanism", "csvs": ["spear-wave2-day1-bodyA.csv", "spear-wave2-day2-bodyA.csv", "spear-wave2-day3-bodyA.csv"]},
    {"day": None, "body": "B", "label": "Flip",      "csvs": ["spear-wave2-day1-bodyB.csv", "spear-wave2-day2-bodyB.csv", "spear-wave2-day3-bodyB.csv"]},
]


def list_name_for(entry: dict) -> str:
    if entry["day"] is None:
        return f"SPEAR Wave 2 - Body {entry['body']} ({entry['label']})"
    return f"SPEAR Wave 2 - Day {entry['day']} - Body {entry['body']} ({entry['label']})"


def load_api_key() -> str:
    if os.environ.get("HUBSPOT_API_KEY"):
        return os.environ["HUBSPOT_API_KEY"]
    if not SECRETS_PATH.exists():
        sys.exit(f"Missing secrets file: {SECRETS_PATH}")
    for line in SECRETS_PATH.read_text().splitlines():
        if line.startswith("HUBSPOT_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("HUBSPOT_API_KEY not found in secrets file")


def request(api_key: str, method: str, url: str, body: dict | list | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        body_text = error.read().decode()
        sys.exit(f"HTTP {error.code} on {method} {url}\n{body_text}")


def read_csv_contact_ids(csv_path: Path) -> list[str]:
    ids: list[str] = []
    with csv_path.open() as csv_file:
        for row in csv.DictReader(csv_file):
            cid = row.get("contactId", "").strip()
            if cid:
                ids.append(cid)
    return ids


def create_manual_list(api_key: str, name: str) -> str:
    result = request(
        api_key,
        "POST",
        "https://api.hubapi.com/crm/v3/lists",
        {"name": name, "objectTypeId": "0-1", "processingType": "MANUAL"},
    )
    return result["list"]["listId"]


def add_members(api_key: str, list_id: str, contact_ids: list[str]) -> None:
    for index in range(0, len(contact_ids), 1000):
        chunk = contact_ids[index : index + 1000]
        request(
            api_key,
            "PUT",
            f"https://api.hubapi.com/crm/v3/lists/{list_id}/memberships/add",
            chunk,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true", help="actually create the lists in HubSpot")
    parser.add_argument("--mode", choices=["by-body", "per-day"], default="by-body",
                        help="by-body: 2 lists, 3 days each merged (default). per-day: 6 lists, one per day per body.")
    args = parser.parse_args()

    api_key = load_api_key()

    plan = BY_BODY_PLAN if args.mode == "by-body" else PER_DAY_PLAN

    plan_with_counts: list[dict] = []
    total = 0
    for entry in plan:
        contact_ids: list[str] = []
        csv_paths: list[str] = []
        for csv_filename in entry["csvs"]:
            csv_path = OUTPUT_DIR / csv_filename
            if not csv_path.exists():
                sys.exit(
                    f"Missing audience CSV: {csv_path}\n"
                    f"Run `python email/spear/scripts/spear-wave2-build.py --days 3` first."
                )
            contact_ids.extend(read_csv_contact_ids(csv_path))
            csv_paths.append(str(csv_path.relative_to(REPO_ROOT)))
        list_name = list_name_for(entry)
        plan_with_counts.append({
            **entry,
            "csv_paths": csv_paths,
            "list_name": list_name,
            "contact_count": len(contact_ids),
            "contact_ids": contact_ids,
        })
        total += len(contact_ids)

    print(f"Plan ({args.mode}): {len(plan_with_counts)} HubSpot static lists, {total} total memberships\n")
    for entry in plan_with_counts:
        print(f"  {entry['list_name']:<50}  {entry['contact_count']:>5} contacts  ←  {' + '.join(entry['csv_paths'])}")

    if not args.create:
        print("\nDry run. Re-run with --create to create these lists in HubSpot.")
        return

    print("\nCreating lists in HubSpot...")
    published: list[dict] = []
    for entry in plan_with_counts:
        list_id = create_manual_list(api_key, entry["list_name"])
        add_members(api_key, list_id, entry["contact_ids"])
        published.append({
            "day": entry["day"],
            "body": entry["body"],
            "label": entry["label"],
            "csvs": entry["csv_paths"],
            "listName": entry["list_name"],
            "listId": list_id,
            "memberCount": entry["contact_count"],
        })
        print(f"  ✓ {entry['list_name']}  →  listId {list_id}  ({entry['contact_count']} members)")

    OUTPUT_PUBLISH_LOG.write_text(json.dumps({
        "publishedAt": datetime.now(timezone.utc).isoformat(),
        "lists": published,
    }, indent=2))
    print(f"\nDone. Saved list-id map to {OUTPUT_PUBLISH_LOG.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
