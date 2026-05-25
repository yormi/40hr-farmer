#!/usr/bin/env python3
"""Build the SPEAR Wave 2 contact list (cold remainder minus waitlist signups).

Pipeline:
  1. Read all memberships of HubSpot list 1722 (SPEAR source list).
  2. Subtract the 150 Wave 0 recipients (variantA + B + C).
  3. Subtract the 852 Wave 1 recipients (sent via Resend on the engaged remainder).
  4. Subtract waitlist signups:
       - Anyone who submitted the V3 40hr Farmer form (7f28cb26-...)
       - PLUS anyone in HubSpot list 1175 ("Waitlist Tomato Course",
         which covers earlier legacy forms).
  5. Batch-read email + firstname for the remaining cold remainder.
  6. Deterministic 50/50 A/B split (seed 42).
  7. Distribute across N sending days (default 3) for sender-reputation warmup.
  8. Write per-day CSVs (one per body per day) plus a single full-audience CSV.

Usage:
  python email/spear/scripts/spear-wave2-build.py
  python email/spear/scripts/spear-wave2-build.py --days 3
"""

import argparse
import csv
import json
import random
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SECRETS_PATH = REPO_ROOT / ".secrets" / "hubspot.env"
WAVE0_SAMPLE_PATH = REPO_ROOT / "email" / "spear" / "spear-wave0-sample.json"
WAVE1_SAMPLE_PATH = REPO_ROOT / "email" / "spear" / "spear-wave1-sample.json"

OUTPUT_DIR = REPO_ROOT / "email" / "spear"
OUTPUT_JSON_PATH = OUTPUT_DIR / "spear-wave2-sample.json"
OUTPUT_CSV_PATH = OUTPUT_DIR / "spear-wave2-audience.csv"

SOURCE_LIST_ID = "1722"
WAITLIST_FORM_ID = "7f28cb26-8aea-432e-bf7f-c50a1484d0a3"
LEGACY_WAITLIST_LIST_ID = "1175"

SPLIT_SEED = 42


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


def fetch_list_memberships(api_key: str, list_id: str) -> list[str]:
    contact_ids: list[str] = []
    after: str | None = None
    while True:
        params = "?limit=250"
        if after:
            params += f"&after={after}"
        result = request(
            api_key,
            "GET",
            f"https://api.hubapi.com/crm/v3/lists/{list_id}/memberships{params}",
        )
        contact_ids.extend(member["recordId"] for member in result.get("results", []))
        paging = result.get("paging", {}).get("next")
        if not paging:
            break
        after = paging.get("after")
    return contact_ids


def fetch_form_submission_emails(api_key: str, form_id: str) -> set[str]:
    """Pull every email that ever submitted the given form."""
    emails: set[str] = set()
    after: str | None = None
    while True:
        params = "?limit=50"
        if after:
            params += f"&after={after}"
        result = request(
            api_key,
            "GET",
            f"https://api.hubapi.com/form-integrations/v1/submissions/forms/{form_id}{params}",
        )
        for submission in result.get("results", []):
            for value in submission.get("values", []):
                if value.get("name") == "email" and value.get("value"):
                    emails.add(value["value"].strip().lower())
        paging = result.get("paging", {}).get("next")
        if not paging:
            break
        after = paging.get("after")
    return emails


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


def load_wave_recipients(path: Path, *keys: str) -> set[str]:
    if not path.exists():
        sys.exit(f"Missing wave sample file: {path}")
    data = json.loads(path.read_text())
    out: set[str] = set()
    for key in keys:
        out |= set(data.get(key, []))
    return out


def write_audience_csv(path: Path, contact_ids: list[str], records: dict[str, dict[str, str | None]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with path.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["email", "firstname", "contactId"])
        for contact_id in contact_ids:
            props = records.get(contact_id, {})
            email = props.get("email")
            if not email:
                continue
            writer.writerow([email, props.get("firstname") or "", contact_id])
            written += 1
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=3, help="number of sending days to spread across (default 3)")
    args = parser.parse_args()

    api_key = load_api_key()

    print(f"Fetching memberships from source list {SOURCE_LIST_ID}...")
    source_ids = fetch_list_memberships(api_key, SOURCE_LIST_ID)
    print(f"  -> {len(source_ids)} members")

    wave0 = load_wave_recipients(WAVE0_SAMPLE_PATH, "variantA", "variantB", "variantC")
    wave1 = load_wave_recipients(WAVE1_SAMPLE_PATH, "wave1ContactIds")
    print(f"Wave 0 recipients: {len(wave0)}")
    print(f"Wave 1 recipients: {len(wave1)}")

    print(f"Fetching legacy waitlist list {LEGACY_WAITLIST_LIST_ID} memberships...")
    legacy_waitlist_ids = set(fetch_list_memberships(api_key, LEGACY_WAITLIST_LIST_ID))
    print(f"  -> {len(legacy_waitlist_ids)} contact ids")

    print(f"Fetching V3 waitlist form ({WAITLIST_FORM_ID}) submissions...")
    waitlist_emails = fetch_form_submission_emails(api_key, WAITLIST_FORM_ID)
    print(f"  -> {len(waitlist_emails)} unique submitter emails")

    cold_remainder = [
        contact_id for contact_id in source_ids
        if contact_id not in wave0 and contact_id not in wave1
    ]
    print(f"Cold remainder (source minus Waves 0+1): {len(cold_remainder)}")

    print("Batch-reading email + firstname for cold remainder...")
    records = batch_read_properties(api_key, cold_remainder, ["email", "firstname"])

    waitlist_filtered = []
    excluded_by_email = 0
    excluded_by_legacy_list = 0
    for contact_id in cold_remainder:
        if contact_id in legacy_waitlist_ids:
            excluded_by_legacy_list += 1
            continue
        email = (records.get(contact_id, {}).get("email") or "").strip().lower()
        if email and email in waitlist_emails:
            excluded_by_email += 1
            continue
        waitlist_filtered.append(contact_id)
    print(f"  -> excluded {excluded_by_legacy_list} via legacy waitlist list 1175")
    print(f"  -> excluded {excluded_by_email} via V3 form submission email match")
    print(f"Wave 2 final audience (after waitlist exclusion): {len(waitlist_filtered)}")

    # Deterministic 50/50 A/B split
    shuffled = list(waitlist_filtered)
    random.Random(SPLIT_SEED).shuffle(shuffled)
    half = len(shuffled) // 2
    body_a_ids = shuffled[:half]
    body_b_ids = shuffled[half:]
    print(f"Split: Body A = {len(body_a_ids)} | Body B = {len(body_b_ids)}")

    # Distribute across N sending days (round-robin)
    days = max(1, args.days)
    per_day_a: list[list[str]] = [[] for _ in range(days)]
    per_day_b: list[list[str]] = [[] for _ in range(days)]
    for index, contact_id in enumerate(body_a_ids):
        per_day_a[index % days].append(contact_id)
    for index, contact_id in enumerate(body_b_ids):
        per_day_b[index % days].append(contact_id)

    for day_index in range(days):
        a_path = OUTPUT_DIR / f"spear-wave2-day{day_index + 1}-bodyA.csv"
        b_path = OUTPUT_DIR / f"spear-wave2-day{day_index + 1}-bodyB.csv"
        a_written = write_audience_csv(a_path, per_day_a[day_index], records)
        b_written = write_audience_csv(b_path, per_day_b[day_index], records)
        print(f"  day {day_index + 1}: Body A {a_written}  |  Body B {b_written}")

    # Single full-audience CSV (everyone, with body assignment column)
    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV_PATH.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["email", "firstname", "contactId", "body", "day"])
        for day_index in range(days):
            for contact_id in per_day_a[day_index]:
                props = records.get(contact_id, {})
                email = props.get("email")
                if not email:
                    continue
                writer.writerow([email, props.get("firstname") or "", contact_id, "A", day_index + 1])
            for contact_id in per_day_b[day_index]:
                props = records.get(contact_id, {})
                email = props.get("email")
                if not email:
                    continue
                writer.writerow([email, props.get("firstname") or "", contact_id, "B", day_index + 1])
    print(f"Wrote full audience CSV to {OUTPUT_CSV_PATH.relative_to(REPO_ROOT)}")

    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceListId": SOURCE_LIST_ID,
        "sourceListSize": len(source_ids),
        "wave0Count": len(wave0),
        "wave1Count": len(wave1),
        "coldRemainderBeforeWaitlistExclusion": len(cold_remainder),
        "waitlistExcludedByLegacyList": excluded_by_legacy_list,
        "waitlistExcludedByV3FormEmail": excluded_by_email,
        "wave2AudienceSize": len(waitlist_filtered),
        "wave2BodyACount": len(body_a_ids),
        "wave2BodyBCount": len(body_b_ids),
        "splitSeed": SPLIT_SEED,
        "sendingDays": days,
        "perDayA": [len(chunk) for chunk in per_day_a],
        "perDayB": [len(chunk) for chunk in per_day_b],
        "wave2ContactIds": waitlist_filtered,
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(output, indent=2))
    print(f"Wrote sample JSON to {OUTPUT_JSON_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
