#!/usr/bin/env python3
"""Build the SPEAR Wave 1 contact list (engaged remainder minus Wave 0).

Pipeline:
  1. Read all memberships of HubSpot list 1722 (the SPEAR source list).
  2. Batch-read hs_email_last_open_date, email, firstname for each member.
  3. Filter to contacts whose last open is within the last 61 days (engaged).
  4. Subtract the 150 contact IDs already sent in Wave 0
     (variantA + variantB + variantC from promo/spear-wave0-sample.json).
  5. Write the full Wave 1 audience to promo/spear-wave1-sample.json and
     promo/spear-wave1-audience.csv (email, firstname) for Loops import.
  6. With --create-list, also create a HubSpot MANUAL list and add members
     (kept in HubSpot so the same audience can be re-used across platforms).

Usage:
  python scripts/spear-wave1-build.py                # dry run, prints summary + writes outputs
  python scripts/spear-wave1-build.py --create-list  # also creates the HubSpot list
"""

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import urllib.request
import urllib.error

REPO_ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATH = REPO_ROOT / ".secrets" / "hubspot.env"
WAVE0_SAMPLE_PATH = REPO_ROOT / "promo" / "spear-wave0-sample.json"
OUTPUT_JSON_PATH = REPO_ROOT / "promo" / "spear-wave1-sample.json"
OUTPUT_CSV_PATH = REPO_ROOT / "promo" / "spear-wave1-audience.csv"

SOURCE_LIST_ID = "1722"
ENGAGEMENT_DAYS = 61

WAVE1_LIST_NAME = "SPEAR Wave 1 - engaged remainder"


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


def batch_read_properties(
    api_key: str,
    contact_ids: list[str],
    properties: list[str],
) -> dict[str, dict[str, str | None]]:
    records: dict[str, dict[str, str | None]] = {}
    for index in range(0, len(contact_ids), 100):
        chunk = contact_ids[index : index + 100]
        payload = {
            "properties": properties,
            "inputs": [{"id": contact_id} for contact_id in chunk],
        }
        result = request(
            api_key,
            "POST",
            "https://api.hubapi.com/crm/v3/objects/contacts/batch/read",
            payload,
        )
        for record in result.get("results", []):
            records[record["id"]] = {
                prop: record["properties"].get(prop) for prop in properties
            }
    return records


def filter_engaged(
    records: dict[str, dict[str, str | None]],
    cutoff: datetime,
) -> list[str]:
    engaged: list[str] = []
    for contact_id, props in records.items():
        raw = props.get("hs_email_last_open_date")
        if not raw:
            continue
        opened = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if opened >= cutoff:
            engaged.append(contact_id)
    return engaged


def load_wave0_recipients() -> set[str]:
    if not WAVE0_SAMPLE_PATH.exists():
        sys.exit(f"Missing Wave 0 sample file: {WAVE0_SAMPLE_PATH}")
    data = json.loads(WAVE0_SAMPLE_PATH.read_text())
    return set(data.get("variantA", [])) | set(data.get("variantB", [])) | set(data.get("variantC", []))


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
    parser.add_argument("--create-list", action="store_true")
    args = parser.parse_args()

    api_key = load_api_key()

    print(f"Fetching memberships from list {SOURCE_LIST_ID}...")
    contact_ids = fetch_all_memberships(api_key)
    print(f"  -> {len(contact_ids)} members")

    print("Batch-reading hs_email_last_open_date, email, firstname for all members...")
    records = batch_read_properties(
        api_key,
        contact_ids,
        ["hs_email_last_open_date", "email", "firstname"],
    )
    has_any_open = sum(1 for props in records.values() if props.get("hs_email_last_open_date"))
    print(f"  -> {has_any_open} contacts have at least one recorded email open")

    cutoff = datetime.now(timezone.utc) - timedelta(days=ENGAGEMENT_DAYS)
    print(f"Engagement cutoff: opens >= {cutoff.isoformat()} ({ENGAGEMENT_DAYS} days ago)")
    engaged = filter_engaged(records, cutoff)
    print(f"  -> {len(engaged)} engaged contacts (Wave 0 + Wave 1 pool)")

    wave0_recipients = load_wave0_recipients()
    print(f"Loaded {len(wave0_recipients)} Wave 0 recipients from {WAVE0_SAMPLE_PATH.relative_to(REPO_ROOT)}")

    wave1_audience = [contact_id for contact_id in engaged if contact_id not in wave0_recipients]
    print(f"Wave 1 audience (engaged minus Wave 0): {len(wave1_audience)}")

    rows_with_email = [
        contact_id for contact_id in wave1_audience
        if records.get(contact_id, {}).get("email")
    ]
    missing_email = len(wave1_audience) - len(rows_with_email)
    if missing_email:
        print(f"  -> {missing_email} engaged contacts have no email property and will be skipped in the CSV")

    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV_PATH.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["email", "firstname", "contactId"])
        for contact_id in rows_with_email:
            props = records[contact_id]
            writer.writerow([props.get("email"), props.get("firstname") or "", contact_id])
    print(f"Wrote audience CSV ({len(rows_with_email)} rows) to {OUTPUT_CSV_PATH.relative_to(REPO_ROOT)}")

    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceListId": SOURCE_LIST_ID,
        "engagementWindowDays": ENGAGEMENT_DAYS,
        "engagementCutoff": cutoff.isoformat(),
        "sourceListSize": len(contact_ids),
        "engagedPoolSize": len(engaged),
        "wave0RecipientsCount": len(wave0_recipients),
        "wave1AudienceSize": len(wave1_audience),
        "wave1AudienceWithEmail": len(rows_with_email),
        "wave1ContactIds": wave1_audience,
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(output, indent=2))
    print(f"Wrote sample JSON to {OUTPUT_JSON_PATH.relative_to(REPO_ROOT)}")

    if not args.create_list:
        print("\nDry run complete. Re-run with --create-list to create the HubSpot list.")
        return

    print(f"\nCreating HubSpot static list '{WAVE1_LIST_NAME}'...")
    list_id = create_manual_list(api_key, WAVE1_LIST_NAME)
    print(f"  -> list id: {list_id}")

    print("Adding members...")
    add_members(api_key, list_id, wave1_audience)

    output["wave1ListId"] = list_id
    OUTPUT_JSON_PATH.write_text(json.dumps(output, indent=2))
    print(f"\nDone. List ready in HubSpot. ID saved to {OUTPUT_JSON_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
