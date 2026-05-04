#!/usr/bin/env python3
"""Extend the 40hr Farmer welcome email workflow on HubSpot.

Wraps the v4 workflow GET → strip server-managed fields → splice → PUT dance.
Stdlib only; reads HUBSPOT_API_KEY from env (`source .secrets/hubspot.env`).

Subcommands:
  --show                                 Print current chain.
  --append-email --email-id <id> --delay-days <n> [--dry-run]
                                         Append delay + email at the tail.
  --remove-tail [--dry-run]              Remove last (delay + email) pair.

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
        if typ == ACTION_TYPE_SEND_EMAIL:
            cid = a.get("fields", {}).get("content_id", "?")
            label = email_cache.get(cid, "")
            lines.append(f"  [{i}] action {aid}  send email {cid}  {label}")
        elif typ == ACTION_TYPE_DELAY:
            f = a.get("fields", {})
            mins = int(f.get("delta", "0"))
            unit = f.get("time_unit", "MINUTES")
            human = _humanize_delay(mins, unit)
            lines.append(f"  [{i}] action {aid}  delay {human}")
        else:
            lines.append(f"  [{i}] action {aid}  type={typ}  fields={a.get('fields')}")
    return "\n".join(lines) if lines else "  (empty chain)"


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


def append_email(doc: dict, email_id: str, delay_days: int) -> dict:
    """Return a new doc with (delay + send-email) appended after current tail."""
    new_doc = json.loads(json.dumps(doc))  # deep copy
    tail_id = _find_tail_action_id(new_doc)
    if tail_id is None:
        sys.exit("Cannot append: workflow has no actions yet.")

    delay_id, email_action_id = _next_action_ids(new_doc, count=2)
    delta_minutes = str(delay_days * 1440)

    delay_action = {
        "actionId": delay_id,
        "actionTypeId": ACTION_TYPE_DELAY,
        "type": "SINGLE_CONNECTION",
        "connection": {"edgeType": "STANDARD", "nextActionId": email_action_id},
        "fields": {"delta": delta_minutes, "time_unit": "MINUTES"},
    }
    email_action = {
        "actionId": email_action_id,
        "actionTypeId": ACTION_TYPE_SEND_EMAIL,
        "type": "SINGLE_CONNECTION",
        "fields": {"content_id": str(email_id)},
    }

    for a in new_doc["actions"]:
        if str(a["actionId"]) == tail_id:
            a["type"] = "SINGLE_CONNECTION"
            a["connection"] = {"edgeType": "STANDARD", "nextActionId": delay_id}
            break

    new_doc["actions"].extend([delay_action, email_action])
    _bump_next_available(new_doc, by=2)
    return new_doc


def remove_tail(doc: dict) -> dict:
    """Drop the last (delay, send-email) pair. Re-terminate the new tail."""
    new_doc = json.loads(json.dumps(doc))
    chain = chain_actions(new_doc)
    if len(chain) < 3:
        sys.exit("Cannot remove tail: chain has fewer than 3 actions.")
    last = chain[-1]
    second_last = chain[-2]
    third_last = chain[-3]
    if last.get("actionTypeId") != ACTION_TYPE_SEND_EMAIL:
        sys.exit(f"Tail action {last['actionId']} is not a send-email; refusing.")
    if second_last.get("actionTypeId") != ACTION_TYPE_DELAY:
        sys.exit(f"Action before tail ({second_last['actionId']}) is not a delay; refusing.")

    drop_ids = {str(last["actionId"]), str(second_last["actionId"])}
    new_doc["actions"] = [a for a in new_doc["actions"] if str(a["actionId"]) not in drop_ids]

    for a in new_doc["actions"]:
        if str(a["actionId"]) == str(third_last["actionId"]):
            a["type"] = "SINGLE_CONNECTION"
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
        new_doc = append_email(doc, args.email_id, args.delay_days)
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
