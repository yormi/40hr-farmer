#!/usr/bin/env python3
"""Extend the 40hr Farmer welcome email workflow on HubSpot.

Wraps the v4 workflow GET → strip server-managed fields → splice → PUT dance.
Stdlib only; auto-reads `.secrets/hubspot.env` (or `$HUBSPOT_API_KEY`).

Subcommands:
  --show                                 Print current chain.
  --append-email --email-id <id> --delay-days <n> [--final] [--dry-run]
                                         Append delay + email at the tail.
                                         By default, also appends a 365-day
                                         parking delay so build-as-you-go
                                         works (next --append-email auto-
                                         removes the parking before adding).
                                         --final skips the parking delay
                                         (use only for the genuinely-last
                                         email of the sequence).
  --remove-tail [--dry-run]              Remove last (delay + email) pair,
                                         and any trailing parking delay.

Workflow ID defaults to the production welcome sequence (1804689064).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.hubapi.com"
PROD_WORKFLOW_ID = "1804689064"
SERVER_MANAGED_FIELDS = ("createdAt", "updatedAt", "crmObjectCreationStatus", "id")
ACTION_TYPE_SEND_EMAIL = "0-4"
ACTION_TYPE_DELAY = "0-1"
PARKING_THRESHOLD_MINUTES = 30 * 1440  # any tail-position delay >= 30d is treated as parking
PARKING_DURATION_DAYS = 365


def _api_key() -> str:
    key = os.environ.get("HUBSPOT_API_KEY", "")
    if key:
        return key
    for candidate in (".secrets/hubspot.env", os.path.expanduser("~/.config/orisha/hubspot.env")):
        if os.path.isfile(candidate):
            with open(candidate) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("HUBSPOT_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("HUBSPOT_API_KEY not set and no .secrets/hubspot.env found.")


def _request(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        method=method,
        data=data,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        sys.exit(f"HTTP {e.code} on {method} {path}\n{body_text}")


def get_workflow(wf_id: str) -> dict:
    return _request("GET", f"/automation/v4/flows/{wf_id}")


def put_workflow(wf_id: str, doc: dict) -> dict:
    clean = {k: v for k, v in doc.items() if k not in SERVER_MANAGED_FIELDS}
    return _request("PUT", f"/automation/v4/flows/{wf_id}", clean)


def get_email_meta(email_id: str) -> dict:
    return _request("GET", f"/marketing/v3/emails/{email_id}")


def chain_actions(doc: dict) -> list[dict]:
    """Return actions in execution order, starting from startActionId."""
    by_id = {str(a["actionId"]): a for a in doc["actions"]}
    out: list[dict] = []
    cur = str(doc.get("startActionId", "1"))
    seen: set[str] = set()
    while cur and cur in by_id and cur not in seen:
        seen.add(cur)
        a = by_id[cur]
        out.append(a)
        cur = str(a.get("connection", {}).get("nextActionId") or "")
    return out


def render_chain(doc: dict, email_cache: dict[str, str]) -> str:
    lines: list[str] = []
    chain = chain_actions(doc)
    for i, a in enumerate(chain, 1):
        typ = a.get("actionTypeId")
        aid = a["actionId"]
        is_tail = i == len(chain)
        if typ == ACTION_TYPE_SEND_EMAIL:
            cid = a.get("fields", {}).get("content_id", "?")
            label = email_cache.get(cid, "")
            lines.append(f"  [{i}] action {aid}  send email {cid}  {label}")
        elif typ == ACTION_TYPE_DELAY:
            f = a.get("fields", {})
            mins = int(f.get("delta", "0"))
            unit = f.get("time_unit", "MINUTES")
            human = _humanize_delay(mins, unit)
            tag = "  [PARKING]" if is_tail and _is_parking_delay(a) else ""
            lines.append(f"  [{i}] action {aid}  delay {human}{tag}")
        else:
            lines.append(f"  [{i}] action {aid}  type={typ}  fields={a.get('fields')}")
    return "\n".join(lines) if lines else "  (empty chain)"


def _is_parking_delay(action: dict) -> bool:
    if action.get("actionTypeId") != ACTION_TYPE_DELAY:
        return False
    fields = action.get("fields", {})
    if fields.get("time_unit") != "MINUTES":
        return False
    try:
        return int(fields.get("delta", "0")) >= PARKING_THRESHOLD_MINUTES
    except (TypeError, ValueError):
        return False


def _strip_parking_tail(doc: dict) -> dict:
    """Drop a tail-position parking delay if present. Idempotent if absent."""
    chain = chain_actions(doc)
    if not chain or not _is_parking_delay(chain[-1]):
        return doc
    new_doc = json.loads(json.dumps(doc))
    parking = chain[-1]
    drop_id = str(parking["actionId"])
    new_doc["actions"] = [a for a in new_doc["actions"] if str(a["actionId"]) != drop_id]
    if len(chain) >= 2:
        prev_id = str(chain[-2]["actionId"])
        for a in new_doc["actions"]:
            if str(a["actionId"]) == prev_id:
                a.pop("connection", None)
                break
    return new_doc


def _humanize_delay(mins: int, unit: str) -> str:
    if unit != "MINUTES":
        return f"{mins} {unit.lower()}"
    if mins % 1440 == 0:
        return f"{mins // 1440}d"
    if mins % 60 == 0:
        return f"{mins // 60}h"
    return f"{mins}m"


def _next_action_ids(doc: dict, count: int = 1) -> list[str]:
    nxt = int(doc.get("nextAvailableActionId", 1))
    return [str(nxt + i) for i in range(count)]


def _bump_next_available(doc: dict, by: int) -> None:
    doc["nextAvailableActionId"] = int(doc.get("nextAvailableActionId", 1)) + by


def _find_tail_action_id(doc: dict) -> str | None:
    chain = chain_actions(doc)
    return str(chain[-1]["actionId"]) if chain else None


def append_email(doc: dict, email_id: str, delay_days: int, park_after: bool) -> dict:
    """Append (delay + email [+ parking]) at the tail.

    If the current tail is a parking delay, it is stripped first so the chain
    grows cleanly across many extensions.
    """
    new_doc = _strip_parking_tail(doc)
    new_doc = json.loads(json.dumps(new_doc))
    tail_id = _find_tail_action_id(new_doc)
    if tail_id is None:
        sys.exit("Cannot append: workflow has no actions yet.")

    n_new = 3 if park_after else 2
    new_ids = _next_action_ids(new_doc, count=n_new)
    delay_id = new_ids[0]
    email_action_id = new_ids[1]
    park_id = new_ids[2] if park_after else None

    delay_action = {
        "actionId": delay_id,
        "actionTypeId": ACTION_TYPE_DELAY,
        "type": "SINGLE_CONNECTION",
        "connection": {"edgeType": "STANDARD", "nextActionId": email_action_id},
        "fields": {"delta": str(delay_days * 1440), "time_unit": "MINUTES"},
    }
    email_action: dict = {
        "actionId": email_action_id,
        "actionTypeId": ACTION_TYPE_SEND_EMAIL,
        "type": "SINGLE_CONNECTION",
        "fields": {"content_id": str(email_id)},
    }
    new_actions = [delay_action, email_action]
    if park_after:
        email_action["connection"] = {"edgeType": "STANDARD", "nextActionId": park_id}
        new_actions.append({
            "actionId": park_id,
            "actionTypeId": ACTION_TYPE_DELAY,
            "type": "SINGLE_CONNECTION",
            "fields": {"delta": str(PARKING_DURATION_DAYS * 1440), "time_unit": "MINUTES"},
        })

    for a in new_doc["actions"]:
        if str(a["actionId"]) == tail_id:
            a["type"] = "SINGLE_CONNECTION"
            a["connection"] = {"edgeType": "STANDARD", "nextActionId": delay_id}
            break

    new_doc["actions"].extend(new_actions)
    _bump_next_available(new_doc, by=n_new)
    return new_doc


def remove_tail(doc: dict) -> dict:
    """Drop the last email + its preceding delay + any trailing parking delay."""
    new_doc = json.loads(json.dumps(doc))
    chain = chain_actions(new_doc)
    has_parking = bool(chain) and _is_parking_delay(chain[-1])
    min_len = 4 if has_parking else 3
    if len(chain) < min_len:
        sys.exit(f"Cannot remove tail: chain has {len(chain)} actions; need {min_len}.")

    if has_parking:
        parking = chain[-1]
        last_email = chain[-2]
        delay_before = chain[-3]
        new_anchor = chain[-4]
    else:
        parking = None
        last_email = chain[-1]
        delay_before = chain[-2]
        new_anchor = chain[-3]

    if last_email.get("actionTypeId") != ACTION_TYPE_SEND_EMAIL:
        sys.exit(f"Expected email at tail position; got actionTypeId={last_email.get('actionTypeId')}")
    if delay_before.get("actionTypeId") != ACTION_TYPE_DELAY:
        sys.exit(f"Expected delay before tail email; got actionTypeId={delay_before.get('actionTypeId')}")

    drop_ids = {str(last_email["actionId"]), str(delay_before["actionId"])}
    if parking:
        drop_ids.add(str(parking["actionId"]))

    new_doc["actions"] = [a for a in new_doc["actions"] if str(a["actionId"]) not in drop_ids]

    for a in new_doc["actions"]:
        if str(a["actionId"]) == str(new_anchor["actionId"]):
            a.pop("connection", None)
            break

    return new_doc


def _email_label_cache(doc: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for a in doc.get("actions", []):
        if a.get("actionTypeId") == ACTION_TYPE_SEND_EMAIL:
            cid = str(a.get("fields", {}).get("content_id", ""))
            if cid and cid not in out:
                try:
                    meta = get_email_meta(cid)
                    out[cid] = f'"{meta.get("name", "?")}"'
                except SystemExit:
                    out[cid] = "(metadata fetch failed)"
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workflow-id", default=PROD_WORKFLOW_ID, help=f"Workflow ID (default: {PROD_WORKFLOW_ID})")
    p.add_argument("--dry-run", action="store_true", help="Preview without PUT")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--show", action="store_true", help="Print current chain only")
    grp.add_argument("--append-email", action="store_true", help="Append delay + email at the tail")
    grp.add_argument("--remove-tail", action="store_true", help="Drop the last (delay + email) pair")
    p.add_argument("--email-id", help="HubSpot email ID for --append-email")
    p.add_argument("--delay-days", type=int, help="Delay in days before the new email")
    p.add_argument("--final", action="store_true",
                   help="Skip the trailing parking delay (use only for the genuinely-last email)")
    args = p.parse_args()

    doc = get_workflow(args.workflow_id)
    print(f"Workflow {args.workflow_id}  enabled={doc.get('isEnabled')}  revisionId={doc.get('revisionId')}")
    cache = _email_label_cache(doc)
    print("\nCurrent chain:")
    print(render_chain(doc, cache))

    if args.show:
        return

    if args.append_email:
        if not args.email_id or args.delay_days is None:
            sys.exit("--append-email requires --email-id and --delay-days")
        new_doc = append_email(doc, args.email_id, args.delay_days, park_after=not args.final)
    elif args.remove_tail:
        new_doc = remove_tail(doc)
    else:
        sys.exit("No operation selected.")

    cache_after = _email_label_cache(new_doc)
    print("\nProposed chain:")
    print(render_chain(new_doc, cache_after))

    if args.dry_run:
        print("\n[dry-run] No PUT issued.")
        return

    print(f"\nPUT /automation/v4/flows/{args.workflow_id} ...")
    result = put_workflow(args.workflow_id, new_doc)
    print(f"  OK  new revisionId={result.get('revisionId')}")
    if not doc.get("isEnabled"):
        print("  NOTE: workflow is disabled. Re-enable in HubSpot UI when ready (no API for this).")


if __name__ == "__main__":
    main()
