#!/usr/bin/env python3
"""Build the SPEAR Wave 0 A/B canary lists.

Pipeline:
  1. Read all memberships of HubSpot list 1722 (the SPEAR source list).
  2. Batch-read hs_email_last_open_date for each member.
  3. Filter to contacts whose last open is within the last 61 days (engaged).
  4. Random-sample 100 with a fixed seed (reproducible).
  5. Split 50/50 into Variant A and Variant B.
  6. With --create-lists, create two HubSpot MANUAL lists and add members.

Usage:
  python email/spear/scripts/spear-wave0-build.py                # dry run, prints summary
  python email/spear/scripts/spear-wave0-build.py --create-lists # also creates the lists in HubSpot
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import urllib.request
import urllib.error

REPO_ROOT = Path(__file__).resolve().parents[3]
SECRETS_PATH = REPO_ROOT / ".secrets" / "hubspot.env"
OUTPUT_PATH = REPO_ROOT / "email" / "spear" / "spear-wave0-sample.json"

SOURCE_LIST_ID = "1722"
ENGAGEMENT_DAYS = 61
SAMPLE_SIZE = 100
RANDOM_SEED = 42

LIST_A_NAME = "SPEAR Wave 0 - Variant A (dream farm)"
LIST_B_NAME = "SPEAR Wave 0 - Variant B (cut hours, keep income)"


def load_api_key() -> str:
    if not SECRETS_PATH.exists():
        sys.exit(f"Missing secrets file: {SECRETS_PATH}")
    for line in SECRETS_PATH.read_text().splitlines():
        if line.startswith("HUBSPOT_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("HUBSPOT_API_KEY not found in secrets file")


def request(api_key: str, method: str, url: str, body: dict | None = None) -> dict:
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


def fetch_all_memberships(api_key: str) -> list[str]:
    contact_ids: list[str] = []
    after: str | None = None
    while True:
        params = "?limit=250"
        if after:
            params += f"&after={after}"
        result = request(
            api_key,
            "GET",
            f"https://api.hubapi.com/crm/v3/lists/{SOURCE_LIST_ID}/memberships{params}",
        )
        contact_ids.extend(member["recordId"] for member in result.get("results", []))
        paging = result.get("paging", {}).get("next")
        if not paging:
            break
        after = paging.get("after")
    return contact_ids


def batch_read_last_open(api_key: str, contact_ids: list[str]) -> dict[str, str | None]:
    open_dates: dict[str, str | None] = {}
    for index in range(0, len(contact_ids), 100):
        chunk = contact_ids[index : index + 100]
        payload = {
            "properties": ["hs_email_last_open_date"],
            "inputs": [{"id": contact_id} for contact_id in chunk],
        }
        result = request(
            api_key,
            "POST",
            "https://api.hubapi.com/crm/v3/objects/contacts/batch/read",
            payload,
        )
        for record in result.get("results", []):
            open_dates[record["id"]] = record["properties"].get("hs_email_last_open_date")
    return open_dates


def filter_engaged(
    open_dates: dict[str, str | None],
    cutoff: datetime,
) -> list[str]:
    engaged: list[str] = []
    for contact_id, raw in open_dates.items():
        if not raw:
            continue
        opened = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if opened >= cutoff:
            engaged.append(contact_id)
    return engaged


def create_manual_list(api_key: str, name: str) -> str:
    result = request(
        api_key,
        "POST",
        "https://api.hubapi.com/crm/v3/lists",
        {"name": name, "objectTypeId": "0-1", "processingType": "MANUAL"},
    )
    return result["list"]["listId"]


def add_members(api_key: str, list_id: str, contact_ids: list[str]) -> None:
    request(
        api_key,
        "PUT",
        f"https://api.hubapi.com/crm/v3/lists/{list_id}/memberships/add",
        contact_ids,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-lists", action="store_true")
    args = parser.parse_args()

    api_key = load_api_key()

    print(f"Fetching memberships from list {SOURCE_LIST_ID}...")
    contact_ids = fetch_all_memberships(api_key)
    print(f"  -> {len(contact_ids)} members")

    print("Batch-reading hs_email_last_open_date for all members...")
    open_dates = batch_read_last_open(api_key, contact_ids)
    has_any_open = sum(1 for raw in open_dates.values() if raw)
    print(f"  -> {has_any_open} contacts have at least one recorded email open")

    cutoff = datetime.now(timezone.utc) - timedelta(days=ENGAGEMENT_DAYS)
    print(f"Engagement cutoff: opens >= {cutoff.isoformat()} ({ENGAGEMENT_DAYS} days ago)")
    engaged = filter_engaged(open_dates, cutoff)
    print(f"  -> {len(engaged)} engaged contacts (canary source pool)")

    if len(engaged) < SAMPLE_SIZE:
        sys.exit(f"Not enough engaged contacts to sample {SAMPLE_SIZE}")

    random.seed(RANDOM_SEED)
    sample = random.sample(engaged, SAMPLE_SIZE)
    variant_a = sample[: SAMPLE_SIZE // 2]
    variant_b = sample[SAMPLE_SIZE // 2 :]
    print(f"Random sample seed={RANDOM_SEED}: {len(variant_a)} Variant A, {len(variant_b)} Variant B")

    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceListId": SOURCE_LIST_ID,
        "engagementWindowDays": ENGAGEMENT_DAYS,
        "engagementCutoff": cutoff.isoformat(),
        "sourceListSize": len(contact_ids),
        "engagedPoolSize": len(engaged),
        "sampleSize": SAMPLE_SIZE,
        "randomSeed": RANDOM_SEED,
        "variantA": variant_a,
        "variantB": variant_b,
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2))
    print(f"Wrote sample to {OUTPUT_PATH.relative_to(REPO_ROOT)}")

    if not args.create_lists:
        print("\nDry run complete. Re-run with --create-lists to create the HubSpot lists.")
        return

    print("\nCreating HubSpot static lists...")
    list_a_id = create_manual_list(api_key, LIST_A_NAME)
    list_b_id = create_manual_list(api_key, LIST_B_NAME)
    print(f"  -> Variant A list: {list_a_id} ({LIST_A_NAME})")
    print(f"  -> Variant B list: {list_b_id} ({LIST_B_NAME})")

    print("Adding members to Variant A...")
    add_members(api_key, list_a_id, variant_a)
    print("Adding members to Variant B...")
    add_members(api_key, list_b_id, variant_b)

    output["variantAListId"] = list_a_id
    output["variantBListId"] = list_b_id
    OUTPUT_PATH.write_text(json.dumps(output, indent=2))
    print(f"\nDone. Lists ready in HubSpot. IDs saved to {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
