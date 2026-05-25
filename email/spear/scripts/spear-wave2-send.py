#!/usr/bin/env python3
"""Send SPEAR Wave 2 batch via Postmark.

Reads a per-day-per-body CSV (built by spear-wave2-build.py), renders each
recipient's email with first-name token (or "there" fallback), and fires
through Postmark's broadcast stream one by one with rate limiting.

Idempotent via a sent-log at .cache/spear-wave2-sent-<tag>.log.json — if you
re-run the same tag, already-successful sends are skipped. Safe against
duplicate sends if a workflow retries.

Usage:
  # Dry run: prints first 3 rendered emails, sends nothing
  python email/spear/scripts/spear-wave2-send.py \\
    --csv email/spear/spear-wave2-day1-bodyA.csv --body A --tag <tag> --dry-run

  # Actual send
  python email/spear/scripts/spear-wave2-send.py \\
    --csv email/spear/spear-wave2-day1-bodyA.csv --body A --tag 2026-05-26-spear-wave2-day1-bodyA

Auth: reads POSTMARK_SERVER_TOKEN from env first (GitHub Actions path), then
from .secrets/postmark.env (local path).

Body templates and subjects are hardcoded below to match the locked Wave 1
copy in email/spear/orisha-list-spear.md. If those bodies change, update
this script in lockstep.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
POSTMARK_SECRETS_PATH = REPO_ROOT / ".secrets" / "postmark.env"
CACHE_DIR = REPO_ROOT / ".cache"

POSTMARK_BASE = "https://api.postmarkapp.com"
POSTMARK_STREAM = os.environ.get("POSTMARK_MESSAGE_STREAM", "broadcast")
POSTMARK_FROM = os.environ.get("POSTMARK_FROM", "guillaume@orisha.io")
USER_AGENT = "orisha-mailer/1.0 (+https://orisha.io)"

DEFAULT_RATE_LIMIT_SECONDS = 0.2  # ~5 sends/sec

BODIES = {
    "A": {
        "subject": "Cutting farm hours without cutting income",
        "cta_anchor": "leverage",
        "utm_content": "wave2-howto",
        "html_paragraphs": (
            "<p>Hey {firstname},</p>\n"
            "<p>Are you looking to do more with less, but aren&#39;t sure how?</p>\n"
            "<p>We&#39;re launching a program to guide farmers to do that. Starting with the most underappreciated opportunity on the farm.</p>\n"
            "<p>Worth a look? <a href=\"{cta_url}\">Check how it works!</a></p>"
        ),
        "text_paragraphs": (
            "Hey {firstname},\n\n"
            "Are you looking to do more with less, but aren't sure how?\n\n"
            "We're launching a program to guide farmers to do that. Starting with the most underappreciated opportunity on the farm.\n\n"
            "Worth a look? Check how it works: {cta_url}"
        ),
    },
    "B": {
        "subject": "Making the farm pay for the life you want",
        "cta_anchor": "story",
        "utm_content": "wave2-flip",
        "html_paragraphs": (
            "<p>Hey {firstname},</p>\n"
            "<p>A balanced life for a farmer? Possible? Some make it.</p>\n"
            "<p>Drew &amp; Allison at Ghost House Farm made the farm pay to replace Allison&#39;s off-farm paycheck.</p>\n"
            "<p><a href=\"{cta_url}\">Check how they did it and what the techniques they used can do for you!</a></p>"
        ),
        "text_paragraphs": (
            "Hey {firstname},\n\n"
            "A balanced life for a farmer? Possible? Some make it.\n\n"
            "Drew & Allison at Ghost House Farm made the farm pay to replace Allison's off-farm paycheck.\n\n"
            "Check how they did it and what the techniques they used can do for you: {cta_url}"
        ),
    },
}

HTML_TEMPLATE = (
    "<div style=\"font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;line-height:1.55;color:#111;\">\n"
    "{body_paragraphs}\n"
    "<p>Guillaume</p>\n"
    "</div>\n"
    "<div style=\"font-size:11px;color:#9ca3af;margin-top:32px;line-height:1.4;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;\">\n"
    "Orisha, 1535 ch. Ste-Foy, Qu&eacute;bec, QC G1S 2P1, Canada &middot; "
    "<a data-pm-no-track href=\"https://orisha.io\" style=\"color:#9ca3af;text-decoration:underline;\">orisha.io</a> &middot; "
    "<a data-pm-no-track href=\"{{{{{{ pm:unsubscribe }}}}}}\" style=\"color:#9ca3af;text-decoration:underline;\">Unsubscribe</a>\n"
    "</div>"
)

TEXT_TEMPLATE = (
    "{body_paragraphs}\n\n"
    "Guillaume\n\n"
    "--\n"
    "Orisha, 1535 ch. Ste-Foy, Quebec, QC G1S 2P1, Canada\n"
    "orisha.io\n"
    "Unsubscribe: {{{{{{ pm:unsubscribe }}}}}}"
)


def load_key(path: Path, name: str) -> str:
    if os.environ.get(name):
        return os.environ[name]
    if not path.exists():
        sys.exit(f"Missing secrets file: {path} (and env var {name} not set)")
    for line in path.read_text().splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(f"{name} not found in {path} (and env var {name} not set)")


def render_email(body_key: str, email: str, firstname: str) -> tuple[str, str, str]:
    body = BODIES[body_key]
    name = (firstname or "").strip() or "there"
    cta_url = (
        "https://the40hourfarmer.orisha.io/"
        "?utm_source=orisha-email&utm_medium=email&utm_campaign=spear-2026-05"
        f"&utm_content={body['utm_content']}#{body['cta_anchor']}"
    )
    html_paragraphs = body["html_paragraphs"].format(firstname=name, cta_url=cta_url)
    text_paragraphs = body["text_paragraphs"].format(firstname=name, cta_url=cta_url)
    html = HTML_TEMPLATE.format(body_paragraphs=html_paragraphs)
    text = TEXT_TEMPLATE.format(body_paragraphs=text_paragraphs)
    return body["subject"], html, text


def post_send(server_token: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode()
    request = urllib.request.Request(f"{POSTMARK_BASE}/email", data=data, method="POST")
    request.add_header("Accept", "application/json")
    request.add_header("Content-Type", "application/json")
    request.add_header("X-Postmark-Server-Token", server_token)
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        raw = error.read().decode()
        try:
            return error.code, json.loads(raw)
        except json.JSONDecodeError:
            return error.code, {"raw": raw[:200]}


def load_sent_log(path: Path) -> set[str]:
    if not path.exists():
        return set()
    payload = json.loads(path.read_text())
    return {entry["email"].lower() for entry in payload.get("sent", [])}


def append_sent_log(path: Path, email: str, message_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        payload = json.loads(path.read_text())
    else:
        payload = {"sent": [], "failures": []}
    payload["sent"].append({"email": email.lower(), "messageId": message_id, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    path.write_text(json.dumps(payload, indent=2))


def append_failure_log(path: Path, email: str, status: int, body: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        payload = json.loads(path.read_text())
    else:
        payload = {"sent": [], "failures": []}
    payload["failures"].append({"email": email.lower(), "status": status, "body": body, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    path.write_text(json.dumps(payload, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="path to per-day-per-body CSV")
    parser.add_argument("--body", required=True, choices=["A", "B"], help="body template to use")
    parser.add_argument("--tag", required=True, help="Postmark Tag for this send batch")
    parser.add_argument("--dry-run", action="store_true", help="print first 3 rendered emails and exit")
    parser.add_argument("--limit", type=int, default=0, help="cap on number of sends (0 = no cap)")
    parser.add_argument("--rate-seconds", type=float, default=DEFAULT_RATE_LIMIT_SECONDS, help="seconds between sends")
    args = parser.parse_args()

    csv_path = Path(args.csv).resolve()
    if not csv_path.exists():
        sys.exit(f"Missing CSV: {csv_path}")

    server_token = load_key(POSTMARK_SECRETS_PATH, "POSTMARK_SERVER_TOKEN")

    sent_log_path = CACHE_DIR / f"spear-wave2-sent-{args.tag}.log.json"
    already_sent = load_sent_log(sent_log_path)
    if already_sent:
        print(f"Found existing sent-log with {len(already_sent)} prior successful sends; will skip those.")

    rows: list[dict] = []
    with csv_path.open() as csv_file:
        for row in csv.DictReader(csv_file):
            rows.append(row)
    print(f"Loaded {len(rows)} rows from {csv_path.relative_to(REPO_ROOT)}")

    if args.dry_run:
        print("\n=== DRY RUN: first 3 rendered emails ===\n")
        for row in rows[:3]:
            subject, html, text = render_email(args.body, row["email"], row.get("firstname", ""))
            print(f"--- to {row['email']} (firstname={row.get('firstname','')!r}) ---")
            print(f"Subject: {subject}")
            print(f"Tag:     {args.tag}")
            print("HtmlBody (first 400 chars):")
            print(html[:400])
            print()
        return

    to_send = [row for row in rows if row["email"].lower() not in already_sent]
    if args.limit > 0:
        to_send = to_send[: args.limit]
    print(f"Will send to {len(to_send)} recipients (skipped {len(rows) - len(to_send)} already-sent / over-limit).")

    synced = 0
    failed = 0
    for row in to_send:
        email = row["email"]
        firstname = row.get("firstname", "")
        subject, html, text = render_email(args.body, email, firstname)
        payload = {
            "From": f"Guillaume at Orisha <{POSTMARK_FROM}>",
            "To": email,
            "Subject": subject,
            "HtmlBody": html,
            "TextBody": text,
            "ReplyTo": POSTMARK_FROM,
            "MessageStream": POSTMARK_STREAM,
            "Tag": args.tag,
            "TrackOpens": True,
            "TrackLinks": "HtmlAndText",
        }
        status, body = post_send(server_token, payload)
        if status == 200 and body.get("ErrorCode") == 0:
            synced += 1
            append_sent_log(sent_log_path, email, body.get("MessageID", ""))
            if synced % 50 == 0:
                print(f"  ... {synced} sent")
        else:
            failed += 1
            append_failure_log(sent_log_path, email, status, body)
            print(f"  ✗ {email}  status={status}  {json.dumps(body)[:140]}")
        time.sleep(args.rate_seconds)

    print(f"\nDone. tag={args.tag}  synced={synced}  failed={failed}")
    print(f"Sent log: {sent_log_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
